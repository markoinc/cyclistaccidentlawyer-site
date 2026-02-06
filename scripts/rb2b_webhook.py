#!/usr/bin/env python3
"""
Website Visitor Webhook Receiver + Lemlist Engagement → GHL Task Creator
24/7 monitoring — qualifies, enriches, and posts to Slack for Carlos.

Pipeline A (RB2B/Leadpipe):
1. Receive visitor data via webhook
2. Research: Is this a decision-maker at a law firm?
3. Qualify: PI/MVA practice? Senior role?
4. Enrich: Fill missing email, phone, LinkedIn via Apollo
5. Post to Slack #all-kurios with full lead card
6. Add to Lemlist campaign if qualified

Pipeline B (Lemlist → GHL):
1. Receive Lemlist activity webhooks (opens, clicks, replies, LinkedIn)
2. Find or create contact in GHL
3. Create call task assigned to Carlos

Run: systemctl start rb2b-webhook
"""

import json
import os
import sys
import logging
import requests
import re
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse

# Config
PORT = 8765
DATA_DIR = Path("/home/ec2-user/clawd/data/rb2b-leads")
DATA_DIR.mkdir(parents=True, exist_ok=True)

APOLLO_API_KEY = "t_j7hexbGUqksRuWZWi9hw"
BETTERCONTACT_API_KEY = "15fbeb3e1bd54b77520d"
BETTERCONTACT_URL = "https://app.bettercontact.rocks/api/v2/async"
BETTERCONTACT_WEBHOOK = "https://webhook.kuriosbrand.com/bettercontact/webhook"
SLACK_BOT_TOKEN = "xoxb-10282810458724-10430403445520-gPrahRZ2rbOV5IdrqTZwiGVz"
LEMLIST_API_KEY = "74625ab77cc446e66516d47ced121627"
LEMLIST_CAMPAIGN_ID = "cam_KA5TnGSZ89gao52tz"  # RB2B Website Visitors campaign
LEMLIST_COLD_CAMPAIGN_ID = "cam_hJKwvWuAQBjeE4gKv"  # Cold Outbound campaign

# Brave Search API (free research step)
BRAVE_API_KEY = "BSAFabv8OkC_Cj6F7BRgwUbCAJ_v_xX"
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

# Gemini Flash (cheap LLM qualification)
GEMINI_API_KEY = "AIzaSyCqkgVGAm6Ki8jN4y42JXxe7Cy5EChGyHk"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent"

# Slack webhook for posting leads
SLACK_CHANNEL = "C0A7RNYC6CF"  # #sierra-workspace ONLY — NO other channel for lead notifications
SLACK_LEADPIPE_CHANNEL = "C0A7RNYC6CF"  # #leadpipe-notifications

# GHL Config
GHL_API_KEY = "pit-9c041df9-b51b-4c7b-9329-241b528dc726"
GHL_LOCATION_ID = "OsNgWuy8oZzLbp5BXbnD"
GHL_BASE_URL = "https://services.leadconnectorhq.com"
GHL_CARLOS_USER_ID = "tODremxt6hpMOnvv0cHf"

# Lemlist events that trigger a call task (per Carlos: first email open + LinkedIn accept only)
CALL_TRIGGER_EVENTS = {
    "emailsOpened": "📧 Opened email",
    "linkedinInviteAccepted": "🤝 Accepted LinkedIn connection",
}

# Decision-maker titles (seniority check)
DECISION_MAKER_TITLES = [
    "partner", "managing partner", "senior partner", "founding partner",
    "owner", "founder", "co-founder",
    "ceo", "president", "principal",
    "director", "managing director",
    "cfo", "coo", "cmo",
    "of counsel", "general counsel",
    "head of", "vp ", "vice president",
    "chief", "executive",
    "attorney", "lawyer", "esquire",  # solo practitioners
    "intake", "business development", "marketing",  # relevant ops people
]

# PI/MVA keywords
PI_KEYWORDS = [
    "personal injury", "injury", "accident", "mva", "motor vehicle",
    "auto accident", "car accident", "truck accident", "tort",
    "negligence", "wrongful death", "slip and fall", "premises liability",
    "trial lawyer", "plaintiff", "litigation", "injury attorney",
    "injury lawyer", "pi attorney", "pi lawyer", "mass tort",
    "catastrophic", "medical malpractice", "wrongful", "damages",
    "dog bite", "pedestrian", "motorcycle", "uber", "lyft"
]

LEGAL_KEYWORDS = [
    "law", "legal", "attorney", "lawyer", "counsel", "firm",
    "esquire", "esq", "llp", "pllc", "practice", "associates",
    "advocacy", "litigation", "trial", "justice", "court"
]

# Non-qualified roles (filter out)
DISQUALIFY_TITLES = [
    "paralegal", "secretary", "receptionist", "intern", "student",
    "clerk", "assistant", "coordinator",  # unless marketing coordinator
]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(DATA_DIR / "webhook.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def normalize(text):
    """Lowercase and clean text for matching."""
    if not text:
        return ""
    return str(text).lower().strip()


def brave_search(query):
    """Search Brave for company info. Returns list of {title, url, description}."""
    try:
        resp = requests.get(
            BRAVE_SEARCH_URL,
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": BRAVE_API_KEY,
            },
            params={"q": query, "count": 3},
            timeout=8,
        )
        if resp.status_code == 200:
            results = []
            for r in resp.json().get("web", {}).get("results", []):
                results.append({
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "description": r.get("description", ""),
                })
            logger.info(f"  Brave search OK: {len(results)} results for '{query}'")
            return results
        else:
            logger.warning(f"  Brave search {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        logger.warning(f"  Brave search failed: {e}")
    return []


def fetch_website_text(url, max_chars=3000):
    """Fetch a website and extract visible text (practice areas, about page, etc.)."""
    if not url:
        return ""
    # Ensure URL has scheme
    if not url.startswith("http"):
        url = "https://" + url
    try:
        resp = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0 (compatible; LeadBot/1.0)"},
            allow_redirects=True,
        )
        if resp.status_code == 200:
            # Strip HTML tags for a rough text extraction
            text = re.sub(r'<script[^>]*>.*?</script>', ' ', resp.text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<style[^>]*>.*?</style>', ' ', text, flags=re.DOTALL | re.IGNORECASE)
            text = re.sub(r'<[^>]+>', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            logger.info(f"  Website fetch OK: {len(text)} chars from {url}")
            return text[:max_chars]
        else:
            logger.warning(f"  Website fetch {resp.status_code} for {url}")
    except Exception as e:
        logger.warning(f"  Website fetch failed for {url}: {e}")
    return ""


def gemini_qualify(company_name, title, industry, website_text, search_results):
    """
    Use Gemini Flash to decide if this is a PI/MVA law firm + decision-maker.
    Returns {qualified: bool, confidence: 0-100, reasons: []}
    """
    # Build search context
    search_context = ""
    for r in search_results:
        search_context += f"- {r.get('title', '')}: {r.get('description', '')}\n"

    prompt = f"""Given the following data about a website visitor, determine:
1. Is their company a Personal Injury (PI) or Motor Vehicle Accident (MVA) law firm?
2. Is this person a decision-maker (partner, owner, CEO, managing attorney, etc.)?

Company Name: {company_name}
Person's Title: {title}
Industry: {industry}

Search Results for this company:
{search_context if search_context else '(no search results available)'}

Company Website Text (excerpt):
{website_text[:2000] if website_text else '(not available)'}

Return ONLY valid JSON (no markdown, no code fences) with this exact structure:
{{"qualified": true/false, "confidence": 0-100, "reasons": ["reason1", "reason2"]}}

qualified = true ONLY if BOTH conditions are met:
- The company is a PI/MVA law firm (or has PI/MVA as a significant practice area)
- The person is a decision-maker or senior role

Be strict: general practice firms without clear PI/MVA focus = not qualified.
If insufficient data to determine, set qualified=false with low confidence."""

    try:
        resp = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.1, "maxOutputTokens": 1024},
            },
            timeout=10,
        )
        if resp.status_code == 200:
            text = resp.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            # Clean up response — strip markdown fences, fix JS booleans
            text = text.strip()
            if text.startswith("```"):
                text = re.sub(r'^```(?:json)?\s*', '', text)
                text = re.sub(r'\s*```$', '', text)
            # Fix trailing commas and other common LLM JSON issues
            text = re.sub(r',\s*}', '}', text)
            text = re.sub(r',\s*]', ']', text)
            logger.info(f"  Gemini raw: {text[:500]}")
            try:
                result = json.loads(text)
            except json.JSONDecodeError:
                # Try to extract qualified and confidence even from truncated JSON
                q_match = re.search(r'"qualified"\s*:\s*(true|false)', text, re.IGNORECASE)
                c_match = re.search(r'"confidence"\s*:\s*(\d+)', text)
                r_match = re.findall(r'"([^"]+)"', text)
                if q_match:
                    result = {
                        "qualified": q_match.group(1).lower() == "true",
                        "confidence": int(c_match.group(1)) if c_match else 50,
                        "reasons": [r for r in r_match if r not in ("qualified", "confidence", "reasons", "true", "false")]
                    }
                    logger.info(f"  Gemini JSON repaired from partial response")
                else:
                    raise
            logger.info(f"  Gemini OK: qualified={result.get('qualified')}, confidence={result.get('confidence')}")
            return result
        else:
            logger.warning(f"  Gemini {resp.status_code}: {resp.text[:300]}")
    except json.JSONDecodeError as e:
        logger.warning(f"  Gemini returned non-JSON: {e}")
    except Exception as e:
        logger.warning(f"  Gemini failed: {e}")

    # Fallback: return unknown
    return {"qualified": False, "confidence": 0, "reasons": ["Gemini analysis unavailable — manual review needed"]}


def quick_leadpipe_check(visitor):
    """
    Step 1: Quick FREE check using only Leadpipe data.
    Returns (dominated, reasons) where dominated means 'definitely not a fit, skip everything'.
    If not dominated, we proceed to Brave/Gemini.
    """
    company = normalize(visitor.get("companyName", ""))
    title = normalize(visitor.get("title", "") or visitor.get("linkedInHeadline", ""))
    industry = normalize(visitor.get("companyIndustry", ""))

    # Instant disqualify: clearly non-legal industries
    non_legal_industries = [
        "software", "technology", "retail", "restaurant", "food",
        "manufacturing", "construction", "real estate", "banking",
        "finance", "healthcare", "hospital", "pharma", "education",
        "university", "government", "nonprofit", "media", "entertainment",
        "agriculture", "mining", "energy", "telecom", "transportation",
        "automotive", "aerospace", "defense", "staffing", "recruiting",
    ]
    if industry:
        for nli in non_legal_industries:
            if nli in industry and "legal" not in industry and "law" not in industry:
                return "skip", [f"❌ Non-legal industry: {industry}"]

    # Instant disqualify: disqualifying titles
    for dq in DISQUALIFY_TITLES:
        if dq in title and "marketing" not in title:
            return "skip", [f"❌ Non-decision-maker title: {title}"]

    # Check for legal signals in available data
    searchable = f"{company} {title} {industry}"
    has_legal_signal = any(kw in searchable for kw in LEGAL_KEYWORDS)
    has_pi_signal = any(kw in searchable for kw in PI_KEYWORDS)
    has_dm_signal = any(kw in title for kw in DECISION_MAKER_TITLES) if title else True

    reasons = []
    if has_legal_signal:
        reasons.append("✅ Legal signals in Leadpipe data")
    if has_pi_signal:
        reasons.append("✅ PI/MVA signals in Leadpipe data")
    if has_dm_signal:
        reasons.append("✅ Decision-maker title detected" if title else "⚠️ No title — needs verification")

    # If no legal signal at all, mark for deeper research (don't skip — Brave might find it)
    if not has_legal_signal and not has_pi_signal:
        reasons.append("⚠️ No legal/PI signals in Leadpipe data — will research")

    return "continue", reasons


def enrich_with_bettercontact(visitor):
    """Enrich visitor via BetterContact waterfall (20+ providers). 
    Async: submits request, polls for results (up to 60s).
    Falls back to Apollo if BetterContact fails."""
    
    first = visitor.get("firstName", "")
    last = visitor.get("lastName", "")
    company = visitor.get("companyName", "")
    domain = visitor.get("companyWebsite", "") or visitor.get("company_website", "")
    linkedin = visitor.get("linkedInUrl", "") or visitor.get("linkedin_url", "") or visitor.get("linkedinUrl", "")
    
    if not first or not last:
        logger.info("   BetterContact: skipping (no name)")
        return enrich_with_apollo(visitor)
    
    # Clean domain
    if domain:
        domain = domain.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]
    
    payload = {
        "data": [{
            "first_name": first,
            "last_name": last,
            "company": company,
        }],
        "enrich_email_address": True,
        "enrich_phone_number": True
    }
    
    # Add optional fields if available
    if domain:
        payload["data"][0]["company_domain"] = domain
    if linkedin:
        payload["data"][0]["linkedin_url"] = linkedin
    
    try:
        # Submit enrichment request
        resp = requests.post(
            BETTERCONTACT_URL,
            headers={"Content-Type": "application/json", "X-API-Key": BETTERCONTACT_API_KEY},
            json=payload,
            timeout=10
        )
        
        resp_data = resp.json()
        if resp.status_code not in (200, 201, 202) or not resp_data.get("success"):
            logger.error(f"   BetterContact submit failed ({resp.status_code}): {resp.text[:200]}")
            return enrich_with_apollo(visitor)
        
        request_id = resp_data["id"]
        logger.info(f"   BetterContact: submitted (id: {request_id}), polling...")
        
        # Poll for results (waterfall takes 10-60s typically)
        import time
        for attempt in range(36):  # Max 3 minutes (36 x 5s) — wait for full waterfall
            time.sleep(5)
            poll_resp = requests.get(
                f"{BETTERCONTACT_URL}/{request_id}",
                headers={"X-API-Key": BETTERCONTACT_API_KEY},
                timeout=10
            )
            
            if poll_resp.status_code != 200:
                continue
                
            result = poll_resp.json()
            
            if result.get("status") == "terminated":
                data = result.get("data", [{}])
                if data and data[0].get("enriched"):
                    contact = data[0]
                    enriched = {
                        "email": contact.get("contact_email_address", ""),
                        "phone": contact.get("contact_phone_number", ""),
                        "title": contact.get("contact_job_title", ""),
                        "company": contact.get("company_name", company),
                        "linkedin_url": contact.get("contact_linkedin_profile_url", ""),
                        "company_website": contact.get("company_website_url", ""),
                        "email_status": contact.get("contact_email_address_status", ""),
                        "enrichment_source": f"BetterContact ({contact.get('email_provider', 'waterfall')})",
                    }
                    logger.info(f"   BetterContact: ✅ found email={enriched.get('email')}, phone={enriched.get('phone')}, status={enriched.get('email_status')}")
                    return enriched
                else:
                    logger.info(f"   BetterContact: no results found after waterfall")
                    break
            elif result.get("status") == "in progress":
                if attempt % 6 == 0:  # Log every 30s to avoid spam
                    logger.info(f"   BetterContact: still processing ({(attempt+1)*5}s elapsed)...")
                continue
            else:
                logger.info(f"   BetterContact: unexpected status: {result.get('status')}")
                break
        
        # BetterContact didn't find anything or timed out — fall back to Apollo
        logger.info(f"   BetterContact: falling back to Apollo")
        return enrich_with_apollo(visitor)
        
    except Exception as e:
        logger.error(f"   BetterContact error: {e}")
        return enrich_with_apollo(visitor)


def _extract_phone_from_apollo(data):
    """Extract best phone number from Apollo person data (direct > org)."""
    phone = ""
    phones = data.get("phone_numbers", [])
    if phones:
        # Prefer direct/mobile over HQ
        for p in phones:
            ptype = (p.get("type", "") or "").lower()
            num = p.get("sanitized_number", "") or p.get("raw_number", "")
            if num and ptype in ("mobile", "direct", "personal"):
                phone = num
                break
        if not phone:
            # Take any phone
            for p in phones:
                num = p.get("sanitized_number", "") or p.get("raw_number", "")
                if num:
                    phone = num
                    break
    # Fallback: organization phone
    if not phone:
        org = data.get("organization", {})
        if org.get("phone"):
            phone = org["phone"]
    return phone


def enrich_with_apollo(visitor):
    """Enrich visitor data with Apollo for email + phone."""
    enriched = {}
    APOLLO_MATCH_HEADERS = {"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY}

    # Try by LinkedIn URL first
    linkedin_url = visitor.get("linkedInUrl", "") or visitor.get("linkedin_url", "") or visitor.get("linkedinUrl", "")
    if linkedin_url:
        try:
            resp = requests.post(
                "https://api.apollo.io/v1/people/match",
                headers=APOLLO_MATCH_HEADERS,
                json={"linkedin_url": linkedin_url},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json().get("person", {})
                if data:
                    enriched = {
                        "email": data.get("email", ""),
                        "phone": _extract_phone_from_apollo(data),
                        "title": data.get("title", ""),
                        "company": data.get("organization", {}).get("name", ""),
                        "city": data.get("city", ""),
                        "state": data.get("state", ""),
                        "apollo_id": data.get("id", ""),
                        "linkedin_url": data.get("linkedin_url", linkedin_url),
                        "company_website": data.get("organization", {}).get("website_url", ""),
                    }
                    logger.info(f"Apollo enriched (LinkedIn): email={enriched.get('email', 'none')}, phone={enriched.get('phone', 'none')}")
                    return enriched
        except Exception as e:
            logger.error(f"Apollo LinkedIn enrichment failed: {e}")

    # Try by email
    email = visitor.get("email", "")
    if email:
        try:
            resp = requests.post(
                "https://api.apollo.io/v1/people/match",
                headers=APOLLO_MATCH_HEADERS,
                json={"email": email},
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json().get("person", {})
                if data:
                    enriched = {
                        "email": data.get("email", email),
                        "phone": _extract_phone_from_apollo(data),
                        "title": data.get("title", ""),
                        "company": data.get("organization", {}).get("name", ""),
                        "city": data.get("city", ""),
                        "state": data.get("state", ""),
                        "apollo_id": data.get("id", ""),
                        "linkedin_url": data.get("linkedin_url", ""),
                        "company_website": data.get("organization", {}).get("website_url", ""),
                    }
                    if enriched.get("phone"):
                        logger.info(f"Apollo enriched (email): phone={enriched['phone']}")
                        return enriched
        except Exception as e:
            logger.error(f"Apollo email enrichment failed: {e}")

    # Fallback: try by name + company
    first = visitor.get("firstName", "")
    last = visitor.get("lastName", "")
    company = visitor.get("companyName", "")
    if first and last:
        try:
            payload = {
                "first_name": first,
                "last_name": last,
            }
            if company:
                payload["organization_name"] = company
            
            resp = requests.post(
                "https://api.apollo.io/v1/people/match",
                headers=APOLLO_MATCH_HEADERS,
                json=payload,
                timeout=10
            )
            if resp.status_code == 200:
                data = resp.json().get("person", {})
                if data:
                    enriched = {
                        "email": data.get("email", "") or enriched.get("email", ""),
                        "phone": _extract_phone_from_apollo(data) or enriched.get("phone", ""),
                        "title": data.get("title", ""),
                        "company": data.get("organization", {}).get("name", company),
                        "city": data.get("city", ""),
                        "state": data.get("state", ""),
                        "apollo_id": data.get("id", ""),
                        "linkedin_url": data.get("linkedin_url", ""),
                        "company_website": data.get("organization", {}).get("website_url", ""),
                    }
                    logger.info(f"Apollo enriched (name): email={enriched.get('email', 'none')}, phone={enriched.get('phone', 'none')}")
                    return enriched
        except Exception as e:
            logger.error(f"Apollo name enrichment failed: {e}")

    return enriched


def qualify_visitor(visitor):
    """
    Multi-step qualification pipeline (saves Apollo credits):
    1. Quick Leadpipe data check — FREE
    2. Brave Search: "{company} personal injury law firm" — FREE
    3. Web Fetch: scrape company website for practice areas — FREE
    4. Gemini Flash: LLM analysis of all collected data — ~$0.0001
    Returns (qualification_level, reasons)
    """
    company = visitor.get("companyName", "")
    title = visitor.get("title", "") or visitor.get("linkedInHeadline", "")
    industry = visitor.get("companyIndustry", "")
    company_website = visitor.get("companyWebsite", "")
    all_reasons = []

    # ── Step 1: Quick Leadpipe data check (FREE) ──
    logger.info(f"  [Step 1/4] Leadpipe data check")
    check_result, check_reasons = quick_leadpipe_check(visitor)
    all_reasons.extend(check_reasons)

    if check_result == "skip":
        logger.info(f"  → Skipped at Step 1: {check_reasons}")
        return "disqualified", all_reasons

    # ── Step 2: Brave Search (FREE) ──
    search_results = []
    if company:
        logger.info(f"  [Step 2/4] Brave search: '{company} personal injury law firm'")
        search_results = brave_search(f"{company} personal injury law firm")
        if search_results:
            all_reasons.append(f"🔍 Brave: {len(search_results)} results found")
            # Extract website URL from search if we don't have one
            if not company_website:
                for sr in search_results:
                    url = sr.get("url", "")
                    if url and company.lower().replace(" ", "") in url.lower().replace(" ", ""):
                        company_website = url
                        all_reasons.append(f"🌐 Found website via search: {url}")
                        break
        else:
            all_reasons.append("🔍 Brave: no results")
    else:
        logger.info(f"  [Step 2/4] Brave search: skipped (no company name)")
        all_reasons.append("🔍 Brave: skipped (no company)")

    # ── Step 3: Scrape company website (FREE) ──
    website_text = ""
    if company_website:
        logger.info(f"  [Step 3/4] Fetching website: {company_website}")
        website_text = fetch_website_text(company_website)
        if website_text:
            all_reasons.append(f"🌐 Website scraped: {len(website_text)} chars")
        else:
            all_reasons.append("🌐 Website: could not fetch")
    else:
        logger.info(f"  [Step 3/4] Website fetch: skipped (no URL)")
        all_reasons.append("🌐 Website: no URL available")

    # ── Step 4: Gemini Flash LLM analysis (~$0.0001) ──
    logger.info(f"  [Step 4/4] Gemini Flash analysis")
    gemini_result = gemini_qualify(company, title, industry, website_text, search_results)

    qualified = gemini_result.get("qualified", False)
    confidence = gemini_result.get("confidence", 0)
    gemini_reasons = gemini_result.get("reasons", [])

    all_reasons.append(f"🤖 Gemini: qualified={qualified}, confidence={confidence}")
    for gr in gemini_reasons:
        all_reasons.append(f"   → {gr}")

    # ── Final decision ──
    if qualified and confidence >= 60:
        return "qualified", all_reasons
    elif qualified and confidence >= 30:
        return "review", all_reasons
    elif not qualified and confidence < 40:
        return "disqualified", all_reasons
    else:
        return "review", all_reasons


def post_to_slack(visitor, enriched, qualification, reasons, pages_viewed=None):
    """Post qualified lead card to Slack #all-kurios."""
    
    # Build the lead card
    name = f"{visitor.get('firstName', '?')} {visitor.get('lastName', '')}"
    company = enriched.get("company") or visitor.get("companyName", "Unknown")
    title = enriched.get("title") or visitor.get("title", "")
    email = enriched.get("email") or visitor.get("email", "")
    phone = enriched.get("phone") or visitor.get("phone", "")
    linkedin = enriched.get("linkedin_url") or visitor.get("linkedInUrl", "") or visitor.get("linkedin_url", "")
    city = enriched.get("city") or visitor.get("city", "")
    state = enriched.get("state") or visitor.get("state", "")
    location = f"{city}, {state}" if city and state else (state or city or "")
    page = visitor.get("pageUrl", "") or visitor.get("page_url", "") or ""
    website = enriched.get("company_website", "")
    
    # Emoji based on qualification
    emoji = "🟢" if qualification == "qualified" else "🟡" if qualification == "review" else "🔴"
    
    # Build message
    lines = [
        f"{emoji} *NEW WEBSITE VISITOR — {qualification.upper()}*",
        "",
        f"*{name}*",
    ]
    if title:
        lines.append(f"{title}")
    lines.append(f"🏢 {company}")
    if location:
        lines.append(f"📍 {location}")
    lines.append("")
    
    if email:
        lines.append(f"📧 {email}")
    if phone:
        lines.append(f"📱 {phone}")
    if linkedin:
        lines.append(f"🔗 <{linkedin}|LinkedIn>")
    if website:
        lines.append(f"🌐 <{website}|{website}>")
    
    lines.append("")
    if page:
        lines.append(f"📄 Visited: {page}")
    
    lines.append("")
    lines.append("*Qualification:*")
    for r in reasons:
        lines.append(f"  {r}")
    
    if qualification == "qualified" and email:
        lines.append("")
        lines.append("✅ *Added to Lemlist campaign — outreach will begin automatically*")
    elif qualification == "qualified" and not email:
        lines.append("")
        lines.append("⚠️ *Qualified but no email found — Carlos, manual outreach needed via LinkedIn*")
    elif qualification == "review":
        lines.append("")
        lines.append("👀 *Needs review — Carlos, check if this is a fit*")
    
    # Add Leadpipe enrichment data if available
    intent = visitor.get("_intentScore", "")
    sessions = visitor.get("_sessions", 0)
    pageviews = visitor.get("_pageviews", 0)
    if intent or sessions:
        lines.append("")
        lines.append("*Leadpipe Data:*")
        if intent:
            intent_emoji = "🔥" if intent == "high" else "🟡" if intent == "medium" else "⚪"
            lines.append(f"  {intent_emoji} Intent: {intent}")
        if sessions:
            lines.append(f"  👁️ {sessions} sessions, {pageviews} pageviews")
        pricing_pv = visitor.get("_pricingPageViews", 0)
        demo_pv = visitor.get("_demoPageViews", 0)
        if pricing_pv:
            lines.append(f"  💰 Viewed pricing page {pricing_pv}x")
        if demo_pv:
            lines.append(f"  🎯 Viewed demo page {demo_pv}x")
    
    message = "\n".join(lines)
    
    # Post directly to Slack
    slack_post_message(SLACK_LEADPIPE_CHANNEL, message)
    
    logger.info(f"📬 Slack message posted: {name} ({qualification})")
    return message


def slack_post_message(channel, text):
    """Post a message directly to Slack via Bot API."""
    try:
        resp = requests.post(
            "https://slack.com/api/chat.postMessage",
            headers={
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-Type": "application/json",
            },
            json={
                "channel": channel,
                "text": text,
            },
            timeout=10
        )
        data = resp.json()
        if data.get("ok"):
            logger.info(f"  ✅ Slack message sent to {channel}")
        else:
            logger.error(f"  ❌ Slack error: {data.get('error')}")
        return data.get("ok", False)
    except Exception as e:
        logger.error(f"  Slack post failed: {e}")
        return False


def add_to_lemlist(lead_data, campaign_id=None):
    """Add a qualified, enriched lead to the Lemlist campaign."""
    email = lead_data.get("email", "")
    if not email:
        logger.warning(f"No email for {lead_data.get('firstName', '')} {lead_data.get('lastName', '')} - skipping Lemlist")
        return False

    cid = campaign_id or LEMLIST_CAMPAIGN_ID
    
    try:
        resp = requests.post(
            f"https://api.lemlist.com/api/campaigns/{cid}/leads/{email}",
            auth=("", LEMLIST_API_KEY),
            json={
                "firstName": lead_data.get("firstName", ""),
                "lastName": lead_data.get("lastName", ""),
                "companyName": lead_data.get("companyName", ""),
                "phone": lead_data.get("phone", ""),
                "linkedinUrl": lead_data.get("linkedin_url", "") or lead_data.get("linkedInUrl", ""),
                "title": lead_data.get("title", ""),
                "city": lead_data.get("city", ""),
                "state": lead_data.get("state", ""),
                "companyUrl": lead_data.get("company_website", ""),
                "source": "website_visitor",
                "visitedPage": lead_data.get("pageUrl", ""),
                "visitDate": datetime.utcnow().isoformat(),
            },
            timeout=10
        )
        if resp.status_code == 200:
            logger.info(f"✅ Added to Lemlist ({cid}): {email}")
            return True
        else:
            logger.error(f"Lemlist error {resp.status_code}: {resp.text[:200]}")
            return False
    except Exception as e:
        logger.error(f"Lemlist add failed: {e}")
        return False


def save_visitor(visitor, qualification, reasons, enriched=None, added_to_lemlist=False):
    """Save visitor data to local JSON file for tracking."""
    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "qualification": qualification,
        "reasons": reasons,
        "visitor": visitor,
        "enriched": enriched or {},
        "added_to_lemlist": added_to_lemlist,
    }

    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filepath = DATA_DIR / f"visitors-{date_str}.json"

    existing = []
    if filepath.exists():
        try:
            existing = json.loads(filepath.read_text())
        except:
            existing = []

    existing.append(record)
    filepath.write_text(json.dumps(existing, indent=2))
    return record


def process_visitor(visitor):
    """
    Full pipeline (Apollo-credit-saving version):
    1. Qualify using FREE sources (Leadpipe data + Brave + website scrape + Gemini)
    2. ONLY if qualified → Apollo enrich (email, phone, LinkedIn)
    3. Post ALL visitors to Slack (qualified or not)
    4. Add qualified leads with email to Lemlist campaign
    """
    name = f"{visitor.get('firstName', '?')} {visitor.get('lastName', '')}"
    company = visitor.get("companyName", "Unknown")

    logger.info(f"📍 New visitor: {name} from {company}")

    enriched = {}
    added = False

    # ── Step 1: Qualify using FREE pipeline (no Apollo) ──
    qualification, reasons = qualify_visitor(visitor)
    logger.info(f"   Qualification: {qualification} — {', '.join(reasons[:3])}")

    # ── Step 2: BetterContact waterfall enrich (falls back to Apollo) ──
    if qualification in ("qualified", "review"):
        logger.info(f"   💰 BetterContact waterfall enrichment (qualified/review lead)")
        enriched = enrich_with_bettercontact(visitor)
        if enriched.get("email"):
            source = enriched.get("enrichment_source", "enrichment")
            reasons.append(f"📧 {source}: found email {enriched['email']}")
        elif enriched:
            reasons.append("📧 Enrichment: no email found")
        else:
            reasons.append("📧 Enrichment: no data found")
    else:
        logger.info(f"   ⏭️ Skipping enrichment (disqualified — saving credits)")
        reasons.append("📧 Enrichment: skipped (not qualified)")

    # ── Step 3: Post ALL visitors to Slack ──
    post_to_slack(visitor, enriched, qualification, reasons)

    # ── Step 4: Add to Lemlist if qualified + has email ──
    merged = {**visitor}
    for k, v in enriched.items():
        if v and not merged.get(k):
            merged[k] = v

    if qualification == "qualified" and (enriched.get("email") or visitor.get("email")):
        lead = {**merged}
        added = add_to_lemlist(lead)
        if added:
            reasons.append("✅ Added to Lemlist campaign")
        else:
            reasons.append("⚠️ Lemlist add failed")

    # ── Step 5: Save everything ──
    save_visitor(visitor, qualification, reasons, enriched, added)

    return qualification, reasons


def ghl_find_contact(email=None, phone=None):
    """Find a contact in GHL by email or phone."""
    if not email and not phone:
        return None
    
    query = email or phone
    try:
        resp = requests.get(
            f"{GHL_BASE_URL}/contacts/search/duplicate",
            headers={
                "Authorization": f"Bearer {GHL_API_KEY}",
                "Version": "2021-07-28",
            },
            params={
                "locationId": GHL_LOCATION_ID,
                "email": email or "",
                "phone": phone or "",
            },
            timeout=10
        )
        if resp.status_code == 200:
            contact = resp.json().get("contact")
            if contact:
                logger.info(f"  GHL: Found existing contact {contact.get('id')} for {query}")
                return contact
    except Exception as e:
        logger.error(f"GHL contact search failed: {e}")
    
    return None


def ghl_create_contact(lead_data):
    """Create a new contact in GHL."""
    try:
        payload = {
            "locationId": GHL_LOCATION_ID,
            "firstName": lead_data.get("firstName", ""),
            "lastName": lead_data.get("lastName", ""),
            "email": lead_data.get("email", ""),
            "phone": lead_data.get("phone", ""),
            "companyName": lead_data.get("companyName", ""),
            "source": "Lemlist Engagement",
            "tags": ["lemlist-engaged", "call-needed"],
        }
        # Remove empty values
        payload = {k: v for k, v in payload.items() if v}
        payload["locationId"] = GHL_LOCATION_ID  # Always required
        
        resp = requests.post(
            f"{GHL_BASE_URL}/contacts/",
            headers={
                "Authorization": f"Bearer {GHL_API_KEY}",
                "Version": "2021-07-28",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10
        )
        if resp.status_code in (200, 201):
            contact = resp.json().get("contact", {})
            logger.info(f"  GHL: Created contact {contact.get('id')}")
            return contact
        else:
            logger.error(f"GHL create contact failed {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        logger.error(f"GHL create contact error: {e}")
    
    return None


def ghl_create_call_task(contact_id, lead_name, event_label, lead_data=None):
    """Create a call task in GHL assigned to Carlos."""
    from datetime import timedelta
    import pytz
    
    # Business hours: 7am-7pm CST only
    cst = pytz.timezone("America/Chicago")
    now_cst = datetime.utcnow().replace(tzinfo=pytz.utc).astimezone(cst)
    
    call_start_hour = 8   # 8am CT (Carlos's calling hours)
    call_end_hour = 17    # 5pm CT
    
    if call_start_hour <= now_cst.hour < call_end_hour:
        # Within business hours — due in 2 hours (but cap at 7pm)
        due_cst = now_cst + timedelta(hours=2)
        if due_cst.hour >= call_end_hour:
            due_cst = due_cst.replace(hour=call_end_hour, minute=0, second=0, microsecond=0)
    else:
        # Outside business hours — due at 7am next business day
        if now_cst.hour >= call_end_hour:
            next_day = now_cst + timedelta(days=1)
        else:
            next_day = now_cst  # before 7am same day
        due_cst = next_day.replace(hour=call_start_hour, minute=0, second=0, microsecond=0)
    
    due_date = due_cst.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    # Build task body with context
    body_lines = [
        f"🔥 HOT LEAD — {event_label}",
        f"",
        f"Name: {lead_name}",
    ]
    if lead_data:
        if lead_data.get("email"):
            body_lines.append(f"Email: {lead_data['email']}")
        if lead_data.get("phone"):
            body_lines.append(f"Phone: {lead_data['phone']}")
        if lead_data.get("companyName"):
            body_lines.append(f"Company: {lead_data['companyName']}")
        if lead_data.get("linkedinUrl"):
            body_lines.append(f"LinkedIn: {lead_data['linkedinUrl']}")
    body_lines.append(f"")
    body_lines.append(f"Source: Lemlist campaign engagement")
    body_lines.append(f"Action: Call this prospect ASAP")
    
    try:
        resp = requests.post(
            f"{GHL_BASE_URL}/contacts/{contact_id}/tasks",
            headers={
                "Authorization": f"Bearer {GHL_API_KEY}",
                "Version": "2021-07-28",
                "Content-Type": "application/json",
            },
            json={
                "title": f"📞 Call {lead_name} — {event_label}",
                "body": "\n".join(body_lines),
                "dueDate": due_date,
                "completed": False,
                "assignedTo": GHL_CARLOS_USER_ID,
            },
            timeout=10
        )
        if resp.status_code in (200, 201):
            task = resp.json().get("task", {})
            logger.info(f"  GHL: ✅ Task created: {task.get('id')} — Call {lead_name}")
            return task
        else:
            logger.error(f"GHL task create failed {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        logger.error(f"GHL task create error: {e}")
    
    return None


def post_task_notification_to_slack(lead_name, event_label, lead_data=None):
    """Post a notification to Slack when a call task is created."""
    lines = [
        f"📞 *CALL TASK CREATED*",
        f"",
        f"*{lead_name}* — {event_label}",
    ]
    if lead_data:
        if lead_data.get("email"):
            lines.append(f"📧 {lead_data['email']}")
        if lead_data.get("phone"):
            lines.append(f"📱 {lead_data['phone']}")
        if lead_data.get("companyName"):
            lines.append(f"🏢 {lead_data['companyName']}")
    lines.append(f"")
    lines.append(f"Assigned to: Carlos | Due: 2 hours")
    lines.append(f"_Task created in GHL automatically_")
    
    message = "\n".join(lines)
    
    # Post directly to Slack
    slack_post_message(SLACK_LEADPIPE_CHANNEL, message)
    
    logger.info(f"  📬 Slack task notification posted for {lead_name}")


def process_lemlist_event(payload):
    """
    Process a Lemlist webhook event:
    - Check if it's a call-trigger event
    - Find/create contact in GHL
    - Create call task assigned to Carlos
    """
    event_type = payload.get("type", "")
    
    # Only process call-trigger events
    if event_type not in CALL_TRIGGER_EVENTS:
        logger.info(f"  Lemlist event '{event_type}' — not a call trigger, skipping")
        return {"status": "skipped", "reason": f"Event {event_type} not a call trigger"}
    
    event_label = CALL_TRIGGER_EVENTS[event_type]
    
    # Extract lead info from Lemlist payload
    email = payload.get("email", "") or payload.get("leadEmail", "")
    first_name = payload.get("firstName", "") or payload.get("leadFirstName", "")
    last_name = payload.get("lastName", "") or payload.get("leadLastName", "")
    lead_name = f"{first_name} {last_name}".strip() or email or "Unknown"
    phone = payload.get("phone", "") or payload.get("leadPhone", "")
    company = payload.get("companyName", "") or payload.get("leadCompanyName", "")
    linkedin = payload.get("linkedinUrl", "") or payload.get("leadLinkedinUrl", "")
    
    logger.info(f"🔔 Lemlist trigger: {event_label} — {lead_name} ({email})")
    
    # Enrich phone if missing — use Apollo with X-Api-Key header
    if not phone and (email or (first_name and last_name)):
        logger.info(f"  📱 Phone missing — enriching via Apollo...")
        try:
            apollo_headers = {"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY}
            match_payload = {}
            if email:
                match_payload["email"] = email
            elif first_name and last_name:
                match_payload["first_name"] = first_name
                match_payload["last_name"] = last_name
                if company:
                    match_payload["organization_name"] = company
            
            aresp = requests.post("https://api.apollo.io/v1/people/match",
                headers=apollo_headers, json=match_payload, timeout=10)
            if aresp.status_code == 200:
                person = aresp.json().get("person", {})
                phone = _extract_phone_from_apollo(person)
                if phone:
                    logger.info(f"  📱 Apollo found phone: {phone}")
                else:
                    logger.info(f"  📱 Apollo: no phone found")
        except Exception as e:
            logger.warning(f"  📱 Apollo phone enrichment failed: {e}")
    
    lead_data = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": phone,
        "companyName": company,
        "linkedinUrl": linkedin,
    }
    
    # Step 0.5: Qualification gate — only create tasks for PI/MVA decision-makers
    logger.info(f"  🔍 Running qualification check...")
    visitor_for_qual = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "companyName": company,
        "title": payload.get("title", "") or payload.get("leadTitle", ""),
        "linkedInUrl": linkedin,
        "companyIndustry": payload.get("companyIndustry", "") or payload.get("industry", ""),
    }
    
    # Get title/company from Apollo if we already looked them up
    if not visitor_for_qual["title"] and email:
        try:
            apollo_headers = {"Content-Type": "application/json", "X-Api-Key": APOLLO_API_KEY}
            aresp = requests.post("https://api.apollo.io/v1/people/match",
                headers=apollo_headers, json={"email": email}, timeout=10)
            if aresp.status_code == 200:
                person = aresp.json().get("person", {})
                visitor_for_qual["title"] = person.get("title", "")
                if not company:
                    company = person.get("organization", {}).get("name", "")
                    lead_data["companyName"] = company
                    visitor_for_qual["companyName"] = company
                visitor_for_qual["companyWebsite"] = person.get("organization", {}).get("website_url", "")
        except Exception as e:
            logger.warning(f"  Apollo lookup for qualification failed: {e}")
    
    qualification, qual_reasons = qualify_visitor(visitor_for_qual)
    logger.info(f"  🔍 Qualification: {qualification} (reasons: {', '.join(qual_reasons[:3])})")
    
    if qualification == "disqualified":
        logger.info(f"  ❌ Lead disqualified — skipping call task for {lead_name}")
        # Post to Slack as skipped
        slack_post_message(SLACK_LEADPIPE_CHANNEL,
            f"⏭️ *Lemlist engagement skipped (unqualified)*\n\n"
            f"*{lead_name}* — {event_label}\n"
            f"🏢 {company}\n"
            f"Reason: {', '.join(qual_reasons[:3])}\n"
            f"_No call task created — lead did not pass PI/MVA qualification_")
        return {"status": "skipped", "reason": "Lead not qualified as PI/MVA decision-maker"}
    
    # Step 1: Find or create contact in GHL
    contact = ghl_find_contact(email=email, phone=phone)
    
    if not contact:
        contact = ghl_create_contact(lead_data)
    
    if not contact:
        logger.error(f"  Could not find/create GHL contact for {lead_name}")
        return {"status": "error", "reason": "Could not find/create GHL contact"}
    
    contact_id = contact.get("id")
    
    # Step 2: Check for duplicate tasks (don't spam)
    try:
        resp = requests.get(
            f"{GHL_BASE_URL}/contacts/{contact_id}/tasks",
            headers={
                "Authorization": f"Bearer {GHL_API_KEY}",
                "Version": "2021-07-28",
            },
            timeout=10
        )
        if resp.status_code == 200:
            existing_tasks = resp.json().get("tasks", [])
            # Skip if there's an uncompleted call task from the last 24h
            for task in existing_tasks:
                if not task.get("completed") and "Call" in task.get("title", ""):
                    logger.info(f"  ⏭️ Skipping — existing open call task for {lead_name}")
                    return {"status": "skipped", "reason": "Existing open call task"}
    except Exception as e:
        logger.warning(f"  Could not check existing tasks: {e}")
    
    # Step 3: Create call task
    task = ghl_create_call_task(contact_id, lead_name, event_label, lead_data)
    
    if task:
        # Step 4: Notify Slack
        post_task_notification_to_slack(lead_name, event_label, lead_data)
        return {"status": "ok", "task_id": task.get("id")}
    
    return {"status": "error", "reason": "Task creation failed"}


def normalize_leadpipe_payload(raw_payload):
    """
    Convert Leadpipe's nested payload format to our flat visitor format.
    Leadpipe sends: { event, timestamp, organizationId, data: { ... } }
    We need: { firstName, lastName, companyName, email, phone, title, ... }
    """
    # Handle nested Leadpipe format
    data = raw_payload
    if "payload" in raw_payload:
        data = raw_payload.get("payload", {}).get("data", {})
    elif "data" in raw_payload and isinstance(raw_payload.get("data"), dict):
        # Could be { event: ..., data: { ... } }
        if raw_payload.get("event") == "visitor.identified":
            data = raw_payload.get("data", {})
    
    # If it already looks flat (has firstName at top level), use as-is
    if "firstName" in raw_payload and "payload" not in raw_payload:
        data = raw_payload
    
    # Extract best email (prefer business)
    email = ""
    business_emails = data.get("businessEmails", [])
    personal_emails = data.get("personalEmails", [])
    if business_emails:
        email = business_emails[0]
    elif data.get("email"):
        email = data["email"]
    elif personal_emails:
        email = personal_emails[0]
    
    # Extract all phones
    phone = ""
    phones = data.get("phones", [])
    if phones:
        phone = phones[0]
    all_phones = phones
    
    # Build normalized visitor
    visitor = {
        "firstName": data.get("firstName", ""),
        "lastName": data.get("lastName", ""),
        "email": email,
        "phone": phone,
        "companyName": data.get("companyName", ""),
        "title": data.get("jobTitle", "") or data.get("title", ""),
        "linkedInUrl": data.get("linkedinUrl", ""),
        "companyIndustry": data.get("industry", ""),
        "companyDescription": data.get("headline", ""),
        "linkedInHeadline": data.get("headline", ""),
        "city": data.get("city", "") or data.get("companyCity", ""),
        "state": data.get("state", "") or data.get("companyState", ""),
        "companyWebsite": data.get("companyDomain", ""),
        "pageUrl": "",
        # Leadpipe-specific enrichment data (keep it all)
        "_source": "leadpipe",
        "_seniority": data.get("seniority", "") or data.get("seniorityLevelRaw", ""),
        "_department": data.get("department", "") or data.get("departmentRaw", ""),
        "_intentScore": data.get("intentScore", ""),
        "_sessions": data.get("sessions", 0),
        "_pageviews": data.get("pageviews", 0),
        "_pricingPageViews": data.get("pricingPageViews", 0),
        "_demoPageViews": data.get("demoPageViews", 0),
        "_companySize": data.get("companySize", ""),
        "_companyRevenue": data.get("companyTotalRevenue", 0),
        "_companyEmployeeCount": data.get("companyEmployeeCount", 0),
        "_ageRange": data.get("ageRange", ""),
        "_enrichmentLevel": data.get("enrichmentLevel", ""),
        "_visitedPages": data.get("visitedPages", []),
        "_referrer": data.get("referrer", ""),
        "_utmSource": data.get("utmSource", ""),
        "_utmMedium": data.get("utmMedium", ""),
        "_utmCampaign": data.get("utmCampaign", ""),
        "_allEmails": data.get("emails", []),
        "_allPhones": all_phones,
    }
    
    # Set page URL from visited pages
    visited = data.get("visitedPages", [])
    if visited:
        visitor["pageUrl"] = visited[0] if isinstance(visited[0], str) else ""
    elif data.get("landingPage"):
        visitor["pageUrl"] = data["landingPage"]
    
    return visitor


def save_raw_payload(raw_payload):
    """Save raw webhook payload for debugging."""
    raw_dir = DATA_DIR / "raw-payloads"
    raw_dir.mkdir(exist_ok=True)
    raw_file = raw_dir / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{raw_payload.get('payload', {}).get('data', {}).get('firstName', 'unknown')}.json"
    raw_file.write_text(json.dumps({"timestamp": datetime.utcnow().isoformat(), "payload": raw_payload}, indent=2))


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        # Route based on path
        if self.path in ("/rb2b/webhook", "/leadpipe/webhook", "/webhook", "/"):
            # Pipeline A: Website visitor — normalize Leadpipe format then process
            logger.info(f"📨 Visitor webhook received on {self.path}")
            
            # Save raw payload for debugging
            save_raw_payload(payload)
            
            # Normalize Leadpipe/RB2B payload to our flat format
            visitor = normalize_leadpipe_payload(payload)
            logger.info(f"  Normalized: {visitor.get('firstName')} {visitor.get('lastName')} @ {visitor.get('companyName')}")
            
            qualification, reasons = process_visitor(visitor)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "ok",
                "qualification": qualification,
                "reasons": reasons
            }).encode())

        elif self.path == "/bettercontact/webhook":
            # BetterContact async enrichment callback (optional — we primarily poll)
            logger.info(f"📨 BetterContact webhook callback received")
            save_raw_payload(payload)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')

        elif self.path == "/lemlist/webhook":
            # Pipeline B: Lemlist engagement → GHL call task
            logger.info(f"📨 Lemlist webhook received: {json.dumps(payload)[:500]}")
            result = process_lemlist_event(payload)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_GET(self):
        if self.path in ("/rb2b/health", "/leadpipe/health", "/health"):
            # Count today's visitors
            date_str = datetime.utcnow().strftime("%Y-%m-%d")
            filepath = DATA_DIR / f"visitors-{date_str}.json"
            today_count = 0
            qualified_count = 0
            if filepath.exists():
                try:
                    visitors = json.loads(filepath.read_text())
                    today_count = len(visitors)
                    qualified_count = sum(1 for v in visitors if v.get("qualification") == "qualified")
                except:
                    pass
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "healthy",
                "service": "visitor-webhook",
                "today": {
                    "total_visitors": today_count,
                    "qualified": qualified_count,
                },
                "uptime": str(datetime.utcnow())
            }).encode())
            return
        
        # Also accept GET on webhook path (for RB2B / Lemlist verification)
        if self.path in ("/rb2b/webhook", "/leadpipe/webhook", "/webhook", "/lemlist/webhook"):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ready"}')
            return
            
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        logger.info(f"HTTP: {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    logger.info(f"🚀 Visitor Webhook server running on port {PORT}")
    logger.info(f"   Endpoints: POST /rb2b/webhook | /leadpipe/webhook | /webhook")
    logger.info(f"   Endpoints: POST /lemlist/webhook (engagement → GHL tasks)")
    logger.info(f"   Health:    GET  /health")
    logger.info(f"   Pipeline A: Qualify → Enrich (BetterContact waterfall → Apollo fallback) → Slack → Lemlist")
    logger.info(f"   Pipeline B: Lemlist event → GHL contact → Call task (Carlos)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        server.server_close()
