#!/usr/bin/env python3
"""Create GHL tasks for IG outreach on launched leads with Instagram profiles."""

import requests
import time
import json

API_KEY = "pit-9c041df9-b51b-4c7b-9329-241b528dc726"
LOCATION_ID = "OsNgWuy8oZzLbp5BXbnD"
BASE_URL = "https://services.leadconnectorhq.com"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Version": "2021-07-28",
    "Content-Type": "application/json"
}

# The 21 launched leads with Instagram profiles
leads = [
    {"name": "Andrew Snyder", "ig": "https://www.instagram.com/kryderlawgroupllc/"},
    {"name": "Almarie Rodriguez", "ig": "https://www.instagram.com/drodriguezlaw/"},
    {"name": "Adrian Martinez", "ig": "https://www.instagram.com/adrianlawfirm/"},
    {"name": "Benjamin Drake", "ig": "https://www.instagram.com/drakelawgroup/"},
    {"name": "Alan Siegel", "ig": "https://www.instagram.com/attorney.alan/"},
    {"name": "Glen Lerner", "ig": "https://www.instagram.com/glenlarsonlaw/"},
    {"name": "Amy Mutrux", "ig": "https://www.instagram.com/lawyertyson/"},
    {"name": "Courtney Lane", "ig": "https://www.instagram.com/lanefosterlawyer/"},
    {"name": "Carrie Capouellez", "ig": "https://www.instagram.com/crcesquire/"},
    {"name": "Carrie Cox", "ig": "https://www.instagram.com/ifbbcarrielawyer/"},
    {"name": "Eric Chaffin", "ig": "https://www.instagram.com/chaffinluhana/"},
    {"name": "Danielle S", "ig": "https://www.instagram.com/lawofficesofdaniellebanks/"},
    {"name": "Alan Feldman", "ig": "https://www.instagram.com/personalinjuryhouston/"},
    {"name": "Evan Golden", "ig": "https://www.instagram.com/evansinjurylaw/"},
    {"name": "Darl Champion", "ig": "https://www.instagram.com/winwithchampion/"},
    {"name": "Brett Emison", "ig": "https://www.instagram.com/langdonandemison/"},
    {"name": "Christopher Keith", "ig": "https://www.instagram.com/ligoriligorilaw/"},
    {"name": "Alix Miller", "ig": "https://www.instagram.com/millermillerlawfirm/"},
    {"name": "Denis Farrell", "ig": "https://www.instagram.com/farrellfamilylawyers/"},
    {"name": "Greg Ward", "ig": "https://www.instagram.com/attorneygregward/"},
    {"name": "Beth Halperin", "ig": "https://www.instagram.com/halperinlawcenter/"},
]

results = {"created": [], "not_found": [], "errors": []}

for lead in leads:
    name = lead["name"]
    ig_url = lead["ig"]
    ig_handle = ig_url.rstrip("/").split("/")[-1]
    
    # Search for contact
    resp = requests.get(
        f"{BASE_URL}/contacts/",
        params={"locationId": LOCATION_ID, "query": name, "limit": 1},
        headers=HEADERS
    )
    time.sleep(0.3)
    
    if resp.status_code != 200:
        print(f"❌ Search failed for {name}: {resp.status_code}")
        results["errors"].append({"name": name, "error": f"Search {resp.status_code}"})
        continue
    
    data = resp.json()
    contacts = data.get("contacts", [])
    
    if not contacts:
        print(f"⚠️  Not found in GHL: {name}")
        results["not_found"].append(name)
        continue
    
    contact = contacts[0]
    contact_id = contact["id"]
    contact_name = contact.get("contactName", name)
    
    # Create task for IG outreach
    task_body = {
        "title": f"IG Outreach: {contact_name}",
        "body": f"Send Instagram DM to @{ig_handle}\n\nProfile: {ig_url}\n\nIntroduce our MVA lead gen service. Personalize based on their firm.",
        "dueDate": "2026-02-07T17:00:00.000Z",  # Due in 2 days
        "completed": False,
        "assignedTo": "oQw4JVZvHiUxJccAvgXm"  # Carlos's user ID from the contact assignment
    }
    
    task_resp = requests.post(
        f"{BASE_URL}/contacts/{contact_id}/tasks",
        headers=HEADERS,
        json=task_body
    )
    time.sleep(0.3)
    
    if task_resp.status_code in (200, 201):
        task_data = task_resp.json()
        task_id = task_data.get("task", {}).get("id", "unknown")
        print(f"✅ Created task for {contact_name} (@{ig_handle}) — task {task_id}")
        results["created"].append({"name": contact_name, "ig": ig_handle, "task_id": task_id})
    else:
        print(f"❌ Task creation failed for {contact_name}: {task_resp.status_code} {task_resp.text}")
        results["errors"].append({"name": contact_name, "error": f"Task {task_resp.status_code}: {task_resp.text}"})

print(f"\n--- SUMMARY ---")
print(f"✅ Created: {len(results['created'])}")
print(f"⚠️  Not found: {len(results['not_found'])}")
print(f"❌ Errors: {len(results['errors'])}")

if results["not_found"]:
    print(f"\nNot found: {', '.join(results['not_found'])}")
if results["errors"]:
    print(f"\nErrors: {json.dumps(results['errors'], indent=2)}")
