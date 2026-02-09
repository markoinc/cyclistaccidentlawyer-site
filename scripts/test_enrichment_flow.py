#!/usr/bin/env python3
"""Test the full RB2B → BetterContact → Slack flow with 4 leads"""

import json
import requests
import time
from pathlib import Path

# Config
BETTERCONTACT_API_KEY = "15fbeb3e1bd54b77520d"
QUALIFIED_LEADS_FILE = Path("/home/ec2-user/clawd/services/lead-webhook/logs/rb2b-qualified.jsonl")

def load_leads(limit=4):
    """Load qualified leads from JSONL"""
    leads = []
    with open(QUALIFIED_LEADS_FILE) as f:
        for line in f:
            if line.strip():
                leads.append(json.loads(line))
    return leads[-limit:]  # Get last N leads

def enrich_batch_with_bettercontact(leads):
    """Send batch of leads to BetterContact for async enrichment"""
    url = "https://app.bettercontact.rocks/api/v2/async"
    
    headers = {
        "X-API-Key": BETTERCONTACT_API_KEY,
        "Content-Type": "application/json"
    }
    
    # Build data array
    data = []
    for lead in leads:
        # Extract domain from website
        website = lead.get("website", "")
        domain = website.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0] if website else ""
        
        data.append({
            "first_name": lead.get("firstName", ""),
            "last_name": lead.get("lastName", ""),
            "company": lead.get("companyName", ""),
            "company_domain": domain,
            "linkedin_url": lead.get("linkedinUrl", ""),
            "custom_fields": {
                "uuid": f"{lead.get('firstName', '')}-{lead.get('lastName', '')}-{int(time.time())}",
                "title": lead.get("jobTitle", ""),
                "state": lead.get("state", "")
            }
        })
    
    payload = {
        "data": data,
        "enrich_email_address": True,
        "enrich_phone_number": True
    }
    
    print(f"📤 Sending {len(data)} leads to BetterContact...")
    print(f"   Endpoint: {url}")
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        print(f"   Status: {resp.status_code}")
        
        if resp.status_code in [200, 201, 202]:
            result = resp.json()
            print(f"   ✅ Success! Response: {json.dumps(result, indent=2)[:500]}")
            return result
        else:
            print(f"   ❌ Error: {resp.text[:500]}")
            return {"error": resp.status_code, "message": resp.text}
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return {"error": str(e)}

def poll_enrichment_status(batch_id, max_attempts=20):
    """Poll for enrichment completion"""
    url = f"https://app.bettercontact.rocks/api/v2/async/{batch_id}"
    headers = {"X-API-Key": BETTERCONTACT_API_KEY}
    
    print(f"\n⏳ Polling for results (batch: {batch_id})...")
    
    for attempt in range(max_attempts):
        try:
            resp = requests.get(url, headers=headers, timeout=30)
            
            if resp.status_code == 200:
                data = resp.json()
                status = data.get("status", "")
                
                if status == "completed":
                    print(f"   ✅ Completed!")
                    return data
                elif status == "failed":
                    print(f"   ❌ Failed: {data}")
                    return data
                else:
                    print(f"   Status: {status} (attempt {attempt + 1}/{max_attempts})")
            else:
                print(f"   Poll error {resp.status_code}: {resp.text[:200]}")
            
            time.sleep(5)
        except Exception as e:
            print(f"   Poll exception: {e}")
            time.sleep(3)
    
    return {"error": "timeout", "message": "Polling timed out"}

def main():
    print("🚀 Testing Full Enrichment Flow with 4 Leads")
    print("=" * 60)
    
    # Load leads
    leads = load_leads(4)
    print(f"✅ Loaded {len(leads)} qualified leads:\n")
    
    for i, lead in enumerate(leads, 1):
        print(f"   {i}. {lead.get('fullName')} - {lead.get('jobTitle')} @ {lead.get('companyName')}")
    
    # Send to BetterContact
    print("\n" + "-" * 60)
    result = enrich_batch_with_bettercontact(leads)
    
    # Check for batch ID
    batch_id = result.get("id") or result.get("batch_id") or result.get("request_id")
    
    if batch_id:
        # Poll for results
        final_result = poll_enrichment_status(batch_id)
        
        # Save results
        output = {
            "leads": leads,
            "enrichment_request": result,
            "enrichment_result": final_result
        }
    else:
        output = {
            "leads": leads,
            "enrichment_response": result
        }
    
    # Save
    output_file = Path("/home/ec2-user/clawd/data/enrichment-test-results.json")
    output_file.write_text(json.dumps(output, indent=2))
    print(f"\n✅ Results saved to {output_file}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(json.dumps(output, indent=2)[:2000])

if __name__ == "__main__":
    main()
