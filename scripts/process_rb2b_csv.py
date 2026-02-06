#!/usr/bin/env python3
"""
Process RB2B CSV export: filter for legal/PI firms, enrich with Apollo, load into Lemlist.
"""

import csv
import json
import requests
import time
import sys
from pathlib import Path

CSV_PATH = "/home/ec2-user/.clawdbot/media/inbound/62c04f8b-8f21-4f27-a435-db3cda2465c0.csv"
OUTPUT_DIR = Path("/home/ec2-user/clawd/data/rb2b-leads")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

APOLLO_API_KEY = "t_j7hexbGUqksRuWZWi9hw"
LEMLIST_API_KEY = "74625ab77cc446e66516d47ced121627"
LEMLIST_CAMPAIGN_ID = "cam_KA5TnGSZ89gao52tz"

# Strict legal keywords
LEGAL_KEYWORDS = [
    "law", "legal", "attorney", "lawyer", "counsel", "firm",
    "esquire", "esq", "llp", "pllc", "practice", "litigat",
    "paralegal", "legal assistant", "law clerk"
]

PI_KEYWORDS = [
    "personal injury", "injury", "accident", "mva", "motor vehicle",
    "auto accident", "car accident", "truck accident", "tort",
    "negligence", "wrongful death", "slip and fall", "premises liability",
    "trial lawyer", "plaintiff", "injury attorney", "injury lawyer",
    "pi attorney", "pi lawyer", "mass tort", "catastrophic"
]

def classify_lead(row):
    """Classify a lead. Returns (tier, reason)."""
    company = row.get("CompanyName", "").lower()
    title = row.get("Title", "").lower()
    industry = row.get("Industry", "").lower()
    website = row.get("Website", "").lower().strip()
    linkedin = row.get("LinkedInUrl", "").lower()
    tags = row.get("Tags", "").lower()
    filters = row.get("FilterMatches", "").lower()
    
    searchable = f"{company} {title} {industry} {website} {linkedin} {tags} {filters}"
    
    # Tier 1: Explicitly PI/accident law
    pi_match = any(kw in searchable for kw in PI_KEYWORDS)
    legal_match = any(kw in searchable for kw in LEGAL_KEYWORDS)
    
    if pi_match and legal_match:
        return "TIER1_PI_LAW", "PI/MVA law firm or legal professional"
    
    # Check website for legal indicators
    legal_domains = ["law", "legal", "attorney", "lawyer", "esq", "firm"]
    if any(d in website for d in legal_domains):
        if pi_match:
            return "TIER1_PI_LAW", f"Legal website ({website}) + PI signal"
        return "TIER2_LEGAL", f"Legal website ({website})"
    
    # Company name has legal indicators
    if legal_match and not any(x in searchable for x in ["education", "school", "university", "college", "church", "non-profit"]):
        if pi_match:
            return "TIER1_PI_LAW", "Legal company + PI keywords"
        return "TIER2_LEGAL", "Legal company (not confirmed PI)"
    
    # Title is legal
    if any(kw in title for kw in ["attorney", "lawyer", "paralegal", "legal assistant", "counsel", "partner"]):
        if pi_match:
            return "TIER1_PI_LAW", "Legal professional + PI signal"
        return "TIER2_LEGAL", f"Legal professional ({title})"
    
    # RB2B tagged as PI but we can't confirm legal
    if "personal injury" in filters:
        # Check if it's actually legal-adjacent
        if legal_match or any(d in website for d in legal_domains):
            return "TIER1_PI_LAW", "RB2B PI filter + legal signal"
        return "TIER3_PI_TAGGED", "RB2B tagged PI but not confirmed legal"
    
    return "SKIP", "Not legal/PI related"


def enrich_with_apollo(row):
    """Enrich a lead with Apollo data."""
    enriched = {}
    
    # Try LinkedIn URL first (person profiles only)
    linkedin = row.get("LinkedInUrl", "")
    if linkedin and "/in/" in linkedin:
        try:
            resp = requests.post(
                "https://api.apollo.io/v1/people/match",
                headers={"Content-Type": "application/json"},
                json={"api_key": APOLLO_API_KEY, "linkedin_url": linkedin},
                timeout=10
            )
            if resp.status_code == 200:
                person = resp.json().get("person", {})
                if person:
                    enriched["email"] = person.get("email", "")
                    phones = person.get("phone_numbers", [])
                    enriched["phone"] = phones[0].get("sanitized_number", "") if phones else ""
                    enriched["apollo_title"] = person.get("title", "")
                    enriched["apollo_company"] = person.get("organization", {}).get("name", "")
                    enriched["apollo_id"] = person.get("id", "")
                    org = person.get("organization", {})
                    enriched["company_phone"] = org.get("phone", "")
                    enriched["company_industry"] = org.get("industry", "")
                    print(f"  ✅ Apollo (LinkedIn): {enriched.get('email', 'no email')}")
                    return enriched
            time.sleep(0.5)  # Rate limit
        except Exception as e:
            print(f"  ⚠️ Apollo error: {e}")
    
    # Try company LinkedIn for org search
    if linkedin and "/company/" in linkedin:
        first = row.get("FirstName", "")
        last = row.get("LastName", "")
        company = row.get("CompanyName", "")
        
        # Search for people at this company
        try:
            resp = requests.post(
                "https://api.apollo.io/v1/mixed_people/search",
                headers={"Content-Type": "application/json"},
                json={
                    "api_key": APOLLO_API_KEY,
                    "q_organization_name": company,
                    "person_titles": ["attorney", "partner", "lawyer", "managing partner", "founder", "owner"],
                    "per_page": 3
                },
                timeout=10
            )
            if resp.status_code == 200:
                people = resp.json().get("people", [])
                if people:
                    person = people[0]  # Top result
                    enriched["email"] = person.get("email", "")
                    phones = person.get("phone_numbers", [])
                    enriched["phone"] = phones[0].get("sanitized_number", "") if phones else ""
                    enriched["apollo_title"] = person.get("title", "")
                    enriched["apollo_name"] = f"{person.get('first_name', '')} {person.get('last_name', '')}"
                    enriched["apollo_id"] = person.get("id", "")
                    enriched["contact_source"] = "apollo_org_search"
                    print(f"  ✅ Apollo (org search): {enriched.get('apollo_name', '?')} - {enriched.get('email', 'no email')}")
                    return enriched
            time.sleep(0.5)
        except Exception as e:
            print(f"  ⚠️ Apollo org search error: {e}")
    
    # Try by name + company
    first = row.get("FirstName", "")
    last = row.get("LastName", "")
    company = row.get("CompanyName", "")
    if first and last:
        try:
            resp = requests.post(
                "https://api.apollo.io/v1/people/match",
                headers={"Content-Type": "application/json"},
                json={
                    "api_key": APOLLO_API_KEY,
                    "first_name": first,
                    "last_name": last,
                    "organization_name": company
                },
                timeout=10
            )
            if resp.status_code == 200:
                person = resp.json().get("person", {})
                if person:
                    enriched["email"] = person.get("email", "")
                    phones = person.get("phone_numbers", [])
                    enriched["phone"] = phones[0].get("sanitized_number", "") if phones else ""
                    enriched["apollo_title"] = person.get("title", "")
                    enriched["apollo_id"] = person.get("id", "")
                    print(f"  ✅ Apollo (name): {enriched.get('email', 'no email')}")
                    return enriched
            time.sleep(0.5)
        except Exception as e:
            print(f"  ⚠️ Apollo name match error: {e}")
    
    print(f"  ❌ No Apollo match")
    return enriched


def add_to_lemlist(lead):
    """Add lead to Lemlist campaign."""
    email = lead.get("email", "")
    if not email:
        return False, "no email"
    
    try:
        payload = {
            "firstName": lead.get("firstName", ""),
            "lastName": lead.get("lastName", ""),
            "companyName": lead.get("companyName", ""),
            "phone": lead.get("phone", ""),
            "linkedinUrl": lead.get("linkedinUrl", ""),
            "title": lead.get("title", ""),
            "city": lead.get("city", ""),
            "state": lead.get("state", ""),
            "website": lead.get("website", ""),
            "source": "rb2b_csv_import",
            "tier": lead.get("tier", ""),
            "classification": lead.get("classification", ""),
        }
        
        resp = requests.post(
            f"https://api.lemlist.com/api/campaigns/{LEMLIST_CAMPAIGN_ID}/leads/{email}",
            auth=("", LEMLIST_API_KEY),
            json=payload,
            timeout=10
        )
        if resp.status_code == 200:
            return True, "added"
        else:
            return False, f"HTTP {resp.status_code}: {resp.text[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("RB2B CSV Lead Processing")
    print("=" * 60)
    
    # Read CSV
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    print(f"\n📊 Total leads in CSV: {len(rows)}")
    
    # Classify all leads
    tier1 = []  # PI law firms - auto-enrich & load
    tier2 = []  # Legal but not confirmed PI - enrich & review
    tier3 = []  # RB2B tagged PI but not legal - review
    skipped = []
    
    for row in rows:
        tier, reason = classify_lead(row)
        row["_tier"] = tier
        row["_reason"] = reason
        
        if tier == "TIER1_PI_LAW":
            tier1.append(row)
        elif tier == "TIER2_LEGAL":
            tier2.append(row)
        elif tier == "TIER3_PI_TAGGED":
            tier3.append(row)
        else:
            skipped.append(row)
    
    print(f"\n🎯 TIER 1 (PI/MVA Law): {len(tier1)}")
    for r in tier1:
        name = f"{r.get('FirstName', '')} {r.get('LastName', '')}".strip() or r.get("CompanyName", "?")
        print(f"   • {name} — {r['_reason']}")
    
    print(f"\n📋 TIER 2 (Legal, needs PI verification): {len(tier2)}")
    for r in tier2:
        name = f"{r.get('FirstName', '')} {r.get('LastName', '')}".strip() or r.get("CompanyName", "?")
        print(f"   • {name} — {r['_reason']}")
    
    print(f"\n🏷️ TIER 3 (RB2B PI-tagged, unconfirmed): {len(tier3)}")
    for r in tier3:
        name = f"{r.get('FirstName', '')} {r.get('LastName', '')}".strip() or r.get("CompanyName", "?")
        print(f"   • {name} — {r['_reason']}")
    
    print(f"\n⏭️ Skipped (not legal/PI): {len(skipped)}")
    
    # Process Tier 1 + Tier 2 leads
    process_leads = tier1 + tier2
    results = {
        "total_csv": len(rows),
        "tier1_count": len(tier1),
        "tier2_count": len(tier2),
        "tier3_count": len(tier3),
        "skipped_count": len(skipped),
        "enriched": [],
        "added_to_lemlist": [],
        "failed_enrich": [],
        "no_email": []
    }
    
    print(f"\n{'=' * 60}")
    print(f"🔍 Enriching {len(process_leads)} leads with Apollo...")
    print(f"{'=' * 60}")
    
    for row in process_leads:
        name = f"{row.get('FirstName', '')} {row.get('LastName', '')}".strip() or row.get("CompanyName", "?")
        print(f"\n→ {name} ({row.get('CompanyName', '?')})")
        
        # Check if we already have an email from RB2B
        existing_email = row.get("WorkEmail", "").strip()
        
        enriched = enrich_with_apollo(row)
        
        email = enriched.get("email") or existing_email
        
        lead_data = {
            "firstName": enriched.get("apollo_name", "").split()[0] if enriched.get("apollo_name") else row.get("FirstName", ""),
            "lastName": " ".join(enriched.get("apollo_name", "").split()[1:]) if enriched.get("apollo_name") else row.get("LastName", ""),
            "email": email,
            "companyName": enriched.get("apollo_company") or row.get("CompanyName", ""),
            "phone": enriched.get("phone") or enriched.get("company_phone", ""),
            "linkedinUrl": row.get("LinkedInUrl", ""),
            "title": enriched.get("apollo_title") or row.get("Title", ""),
            "city": row.get("City", ""),
            "state": row.get("State", ""),
            "website": row.get("Website", "").strip(),
            "tier": row["_tier"],
            "classification": row["_reason"],
            "pageViews": row.get("AllTimePageViews", ""),
            "lastSeen": row.get("LastSeenAt", ""),
        }
        
        results["enriched"].append(lead_data)
        
        if email:
            lead_data["email"] = email
            success, msg = add_to_lemlist(lead_data)
            if success:
                print(f"  📧 Added to Lemlist: {email}")
                results["added_to_lemlist"].append(lead_data)
            else:
                print(f"  ⚠️ Lemlist: {msg}")
                lead_data["lemlist_error"] = msg
                results["failed_enrich"].append(lead_data)
        else:
            print(f"  📭 No email found — skipping Lemlist")
            results["no_email"].append(lead_data)
        
        time.sleep(0.3)  # Rate limit
    
    # Also process Tier 3 for Apollo enrichment only (don't add to Lemlist yet)
    print(f"\n{'=' * 60}")
    print(f"🔍 Enriching {len(tier3)} Tier 3 leads (review queue)...")
    print(f"{'=' * 60}")
    
    tier3_enriched = []
    for row in tier3:
        name = f"{row.get('FirstName', '')} {row.get('LastName', '')}".strip() or row.get("CompanyName", "?")
        print(f"\n→ {name} ({row.get('CompanyName', '?')})")
        
        enriched = enrich_with_apollo(row)
        existing_email = row.get("WorkEmail", "").strip()
        email = enriched.get("email") or existing_email
        
        lead_data = {
            "firstName": row.get("FirstName", ""),
            "lastName": row.get("LastName", ""),
            "email": email,
            "companyName": row.get("CompanyName", ""),
            "phone": enriched.get("phone", ""),
            "linkedinUrl": row.get("LinkedInUrl", ""),
            "title": enriched.get("apollo_title") or row.get("Title", ""),
            "city": row.get("City", ""),
            "state": row.get("State", ""),
            "website": row.get("Website", "").strip(),
            "tier": "TIER3_PI_TAGGED",
            "classification": row["_reason"],
            "apollo_data": enriched
        }
        tier3_enriched.append(lead_data)
    
    results["tier3_enriched"] = tier3_enriched
    
    # Save results
    output_path = OUTPUT_DIR / "csv-import-results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n{'=' * 60}")
    print(f"📊 FINAL RESULTS")
    print(f"{'=' * 60}")
    print(f"Total CSV leads:           {len(rows)}")
    print(f"Tier 1 (PI Law):           {len(tier1)}")
    print(f"Tier 2 (Legal):            {len(tier2)}")
    print(f"Tier 3 (PI-tagged):        {len(tier3)}")
    print(f"Skipped:                   {len(skipped)}")
    print(f"Added to Lemlist:          {len(results['added_to_lemlist'])}")
    print(f"No email found:            {len(results['no_email'])}")
    print(f"Lemlist errors:            {len(results['failed_enrich'])}")
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
