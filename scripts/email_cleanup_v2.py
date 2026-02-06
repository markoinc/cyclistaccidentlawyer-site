#!/usr/bin/env python3
"""Deep Email Cleanup v2 - Incremental saves, better warmup detection"""

import json
import requests
import time
import re
import sys
import os

USER_ID = "mark@kuriosbrand.com"
BASE_URL = f"https://gmail.googleapis.com/gmail/v1/users/{USER_ID}"
RESULTS_FILE = "/home/ec2-user/clawd/scripts/email_cleanup_results.json"
STATE_FILE = "/home/ec2-user/clawd/scripts/email_cleanup_state.json"

LABELS = {
    "prospects": "Label_1",
    "partners": "Label_2",
    "calls": "Label_3",
    "important": "Label_4",
    "junk": "Label_5",
}

def get_token():
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": "838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com",
        "client_secret": "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",
        "refresh_token": "1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw",
        "grant_type": "refresh_token"
    })
    return resp.json()["access_token"]

TOKEN = get_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Load or init state
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "processed_ids": [],
        "next_page_token": None,
        "batch_num": 0,
        "done": False,
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# Load or init results
def load_results():
    if os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE) as f:
            return json.load(f)
    return {
        "total_processed": 0,
        "trashed": [],
        "labeled": {"prospects": [], "partners": [], "calls": [], "important": []},
        "kept_unlabeled": [],
        "trash_categories": {
            "wordpress_updates": [],
            "wordpress_comments": [],
            "cold_outreach_spam": [],
            "warmup_emails": [],
            "newsletter_spam": [],
        },
        "errors": [],
    }

def save_results(results):
    with open(RESULTS_FILE, "w") as f:
        json.dump(results, f, indent=2, default=str)

def get_header(headers, name):
    for h in headers:
        if h["name"].lower() == name.lower():
            return h.get("value", "")
    return ""

# Warmup domain patterns - random fake-sounding domains used by warmup tools
WARMUP_DOMAIN_PATTERNS = [
    r"@.*flirt", r"@.*hookup", r"@.*dating", r"@.*romance", r"@.*love",
    r"@.*lusty", r"@.*sexy", r"@.*passion", r"@.*tempt", r"@.*desire",
    r"@.*haze", r"@.*swoon", r"@.*crave", r"@.*mingle", r"@.*daring",
    r"@.*bliss", r"@.*nuzzle", r"@.*ripe", r"@.*fling", r"@.*amour",
    r"@.*inferno", r"@.*hazard", r"@.*wix\.com$", r"@.*riskych",
    r"@.*sizzle", r"@.*charm", r"@.*affair", r"@.*lust", r"@.*spark",
    r"@.*heat", r"@.*fetish", r"@.*twilight", r"@.*eagle.*fling",
    r"@.*intimate", r"@.*whisper", r"@.*secret.*chat",
    r"@.*forbidden", r"@.*whimsy", r"@.*romantic",
]

def is_warmup_reply(subject, from_addr, to_addr, snippet):
    """Detect warmup campaign replies - inbound warmup from random domains"""
    subj_lower = subject.lower()
    from_lower = from_addr.lower()
    snippet_lower = snippet.lower()
    
    # Explicitly from Instantly support
    if "instantly" in from_lower and "support@instantly" in from_lower:
        return True
    
    # Check for "instantly-w" in subject (warmup tag)
    if "instantly-w" in subj_lower:
        return True
    
    # Contains 7ZW4TTH (Instantly tracking code) AND from a warmup-looking domain
    has_tracking = "7zw4tth" in subj_lower
    
    if has_tracking:
        for pattern in WARMUP_DOMAIN_PATTERNS:
            if re.search(pattern, from_lower, re.IGNORECASE):
                return True
    
    # Lemwarm / mailwarm / warmup keywords
    if any(w in f"{subj_lower} {from_lower} {snippet_lower}" for w in ["lemwarm", "mailwarm", "warmbox", "warmup", "warm-up", "inbox warm"]):
        return True
    
    # Instantly notification about warmup
    if "notifications@nt1.instantly.ai" in from_lower:
        return True
    if "instantly.ai" in from_lower and "positive reply" in snippet_lower:
        return True
    
    return False

def is_wordpress_notification(subject, from_addr, snippet):
    subj_lower = subject.lower()
    from_lower = from_addr.lower()
    text = f"{subj_lower} {snippet.lower()}"
    
    if "wordpress" not in from_lower and "wordpress" not in subj_lower:
        return False, None
    
    # Comment notifications
    comment_patterns = [r"please moderate", r"new comment on", r"comment.*moderation", r"comment.*awaiting"]
    for p in comment_patterns:
        if re.search(p, text):
            return True, "wordpress_comments"
    
    # Update notifications
    update_patterns = [r"has been updated", r"updated successfully", r"auto.?update", r"plugin.*updated", r"theme.*updated", r"background update"]
    for p in update_patterns:
        if re.search(p, text):
            return True, "wordpress_updates"
    
    return False, None

def is_cold_outreach(subject, from_addr, to_addr, snippet):
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    
    patterns = [
        r"seo (service|audit|pitch|proposal|package)",
        r"(working|growth) capital",
        r"google street view",
        r"virtual tour",
        r"web design (service|proposal|quote)",
        r"domain.*for sale",
        r"estimating service",
        r"(concrete|construction) estimat",
        r"(business|merchant) (loan|funding|cash advance)",
        r"boost your (ranking|traffic|seo|business)",
        r"hi mike",
        r"partnership opportunity",
        r"backlink",
        r"guest post",
        r"link building",
        r"press release",
        r"workers.?comp",
        r"insurance quote",
        r"payroll service",
        r"bookkeeping service",
        r"reputation management",
        r"fwd:.*mike",
        r"florida (concrete|paving) (contractor|coatings?)",
        r"payment terms.*estimating",
    ]
    
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            # Safety: don't trash if from a known partner or law-related
            if any(safe in from_lower for safe in ["law", "legal", "attorney", "esquire", "casesondemand", "inquire"]):
                return False
            return True
    return False

SAFE_SENDERS = [
    "stripe", "wise", "paypal", "invoice", "payment",
    "google", "searchconsole", "search-console",
    "businessprofile", "business-profile",
    "rb2b", "openai", "anthropic", "claude",
    "fireflies", "calendly", "zoom", "meet",
    "gemini", "notion", "slack", "discord",
    "namecheap", "godaddy", "cloudflare", "porkbun",
    "github", "vercel", "neon", "supabase",
    "lemlist", "apollo", "dataforseo",
    "gohighlevel", "leadconnector", "highlevel",
    "twilio", "sendgrid", "chase", "wellsfargo",
    "regus", "amazon", "aws", "microsoft",
    "linkedin", "meta", "facebook", "testflight",
    "apple", "ringba", "harbor", "nomachine",
    "hostmyapple", "webshare", "brave", "lovable",
    "whatsapp", "cj.com", "resultcalls", "dropbox",
    "fathom", "read.ai", "otter.ai", "canva",
    "veed", "rapidurlindex", "firstorion",
    "wise.com", "notifications@stripe",
]

PARTNER_EMAILS = [
    "carlos@kuriosbrand", "carlos@demandstudio",
    "max@casesondemand", "jeremy@casesondemand", "toye@casesondemand",
    "patrick@inquire2esquir", "Patrick@inquire2esquir",
    "scott@vegashurt", "Scott@vegashurt",
    "omeed@theinj", "ja.law.pllc@gmail",
    "jason@gcelaw", "brandon@inbounds",
    "zach@salespipelinepros",
    "josh@shanesmithlaw",
]

def is_safe_sender(from_addr):
    from_lower = from_addr.lower()
    for safe in SAFE_SENDERS:
        if safe.lower() in from_lower:
            return True
    return False

def is_partner(from_addr, subject, snippet):
    from_lower = from_addr.lower()
    for email_part in PARTNER_EMAILS:
        if email_part.lower() in from_lower:
            return True
    
    text = f"{from_addr} {subject} {snippet}".lower()
    partner_kw = ["cases on demand", "casesondemand", "inquired esquire", "inquire2esquir",
                  "poisson", "vegashurt", "gcelaw", "demandstudio"]
    for kw in partner_kw:
        if kw in text:
            return True
    return False

def is_call_transcript(subject, from_addr, snippet):
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    if any(x in from_lower for x in ["fireflies", "fathom", "otter.ai"]):
        return True
    if "gemini" in from_lower and "notes" in text:
        return True
    if "meetings-noreply@google" in from_lower and ("notes" in text or "recap" in text):
        return True
    patterns = [r"transcript", r"call summary", r"meeting summary", r"call recap", r"meeting recap"]
    for p in patterns:
        if re.search(p, text):
            return True
    return False

def is_prospect_lead(subject, from_addr, snippet):
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    if "rb2b" in from_lower:
        return True
    patterns = [r"new lead", r"form submission", r"new submission", r"contact form",
                r"looking for.*takeoff", r"your rb2b"]
    for p in patterns:
        if re.search(p, text):
            return True
    return False

def categorize_email(msg_id, subject, from_addr, to_addr, snippet, label_ids):
    if "TRASH" in (label_ids or []) or "SPAM" in (label_ids or []):
        return "skip", None, None, "Already in trash/spam"
    
    # WARMUP CHECK FIRST (high confidence trash)
    if is_warmup_reply(subject, from_addr, to_addr, snippet):
        return "trash", "warmup_emails", None, "Warmup email"
    
    # PARTNER CHECK (before any trash)
    if is_partner(from_addr, subject, snippet):
        return "label", None, "partners", "Partner email"
    
    # SAFE SENDER CHECK
    if is_safe_sender(from_addr):
        if is_call_transcript(subject, from_addr, snippet):
            return "label", None, "calls", "Call transcript"
        if is_prospect_lead(subject, from_addr, snippet):
            return "label", None, "prospects", "Prospect/lead"
        return "keep", None, None, f"Safe sender"
    
    # CALL TRANSCRIPT
    if is_call_transcript(subject, from_addr, snippet):
        return "label", None, "calls", "Call transcript"
    
    # PROSPECT/LEAD
    if is_prospect_lead(subject, from_addr, snippet):
        return "label", None, "prospects", "Prospect/lead"
    
    # WORDPRESS
    is_wp, wp_cat = is_wordpress_notification(subject, from_addr, snippet)
    if is_wp:
        return "trash", wp_cat, None, "WordPress notification"
    
    # COLD OUTREACH
    if is_cold_outreach(subject, from_addr, to_addr, snippet):
        return "trash", "cold_outreach_spam", None, "Cold outreach/spam"
    
    # FROM OWN EMAIL (outbound campaigns - keep)
    if "mark@kuriosbrand.com" in from_addr.lower():
        return "keep", None, None, "Own outbound email"
    
    return "keep", None, None, "Uncategorized"

def trash_message(msg_id):
    resp = requests.post(f"{BASE_URL}/messages/{msg_id}/trash", headers=HEADERS)
    return resp.status_code == 200

def label_message(msg_id, label_id):
    resp = requests.post(f"{BASE_URL}/messages/{msg_id}/modify", headers=HEADERS,
                        json={"addLabelIds": [label_id]})
    return resp.status_code == 200

def main():
    global TOKEN, HEADERS
    
    state = load_state()
    results = load_results()
    
    if state["done"]:
        print("Previous run completed. Delete state file to rerun.")
        print(f"Processed: {results['total_processed']}, Trashed: {len(results['trashed'])}")
        return
    
    thirty_days_ago = 1767484800  # Jan 4, 2026
    query = f"after:{thirty_days_ago}"
    
    processed_set = set(state["processed_ids"])
    page_token = state["next_page_token"]
    batch_num = state["batch_num"]
    
    print(f"Starting from batch {batch_num + 1}, already processed {len(processed_set)} messages")
    
    while True:
        batch_num += 1
        print(f"\n📦 Batch {batch_num}...")
        
        params = {"q": query, "maxResults": 50}
        if page_token:
            params["pageToken"] = page_token
        
        resp = requests.get(f"{BASE_URL}/messages", headers=HEADERS, params=params)
        if resp.status_code == 401:
            print("Token expired, refreshing...")
            TOKEN = get_token()
            HEADERS = {"Authorization": f"Bearer {TOKEN}"}
            resp = requests.get(f"{BASE_URL}/messages", headers=HEADERS, params=params)
        
        if resp.status_code != 200:
            print(f"ERROR: {resp.status_code} {resp.text[:200]}")
            break
        
        data = resp.json()
        messages = data.get("messages", [])
        next_token = data.get("nextPageToken")
        
        if not messages:
            print("No more messages.")
            state["done"] = True
            break
        
        print(f"   Processing {len(messages)} messages...")
        
        for msg_ref in messages:
            msg_id = msg_ref["id"]
            
            if msg_id in processed_set:
                continue
            
            # Get message
            msg_resp = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=HEADERS,
                                   params={"format": "metadata", "metadataHeaders": ["Subject", "From", "To", "Date"]})
            if msg_resp.status_code == 401:
                TOKEN = get_token()
                HEADERS = {"Authorization": f"Bearer {TOKEN}"}
                msg_resp = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=HEADERS,
                                       params={"format": "metadata", "metadataHeaders": ["Subject", "From", "To", "Date"]})
            
            if msg_resp.status_code != 200:
                results["errors"].append(f"Failed to fetch {msg_id}")
                continue
            
            msg = msg_resp.json()
            headers = msg.get("payload", {}).get("headers", [])
            subject = get_header(headers, "Subject")
            from_addr = get_header(headers, "From")
            to_addr = get_header(headers, "To")
            date_str = get_header(headers, "Date")
            snippet = msg.get("snippet", "")
            label_ids = msg.get("labelIds", [])
            
            results["total_processed"] += 1
            processed_set.add(msg_id)
            
            action, trash_cat, label_cat, reason = categorize_email(msg_id, subject, from_addr, to_addr, snippet, label_ids)
            
            email_info = {
                "id": msg_id, "subject": subject[:120], "from": from_addr[:100],
                "to": to_addr[:100] if to_addr else "", "date": date_str, "reason": reason,
            }
            
            if action == "trash":
                success = trash_message(msg_id)
                if success:
                    results["trash_categories"][trash_cat].append(email_info)
                    results["trashed"].append(email_info)
                    print(f"  🗑️  [{trash_cat}] {subject[:60]} | {from_addr[:40]}")
                else:
                    results["errors"].append(f"Trash failed: {msg_id}")
            elif action == "label":
                label_id = LABELS.get(label_cat)
                if label_id:
                    label_message(msg_id, label_id)
                    results["labeled"][label_cat].append(email_info)
                    print(f"  🏷️  [{label_cat}] {subject[:60]} | {from_addr[:40]}")
            elif action == "keep":
                results["kept_unlabeled"].append(email_info)
                print(f"  ✅ {subject[:60]} | {from_addr[:40]}")
            
            time.sleep(0.05)
        
        # Save state after each batch
        state["processed_ids"] = list(processed_set)
        state["next_page_token"] = next_token
        state["batch_num"] = batch_num
        save_state(state)
        save_results(results)
        print(f"   💾 Saved. Total: {results['total_processed']} processed, {len(results['trashed'])} trashed")
        
        if not next_token:
            print("\nNo more pages.")
            state["done"] = True
            break
        
        page_token = next_token
        time.sleep(0.3)
    
    save_state(state)
    save_results(results)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 FINAL REPORT")
    print("=" * 80)
    print(f"Total processed: {results['total_processed']}")
    print(f"Total trashed: {len(results['trashed'])}")
    for cat, items in results["trash_categories"].items():
        if items:
            print(f"  {cat}: {len(items)}")
    print(f"Total labeled: {sum(len(v) for v in results['labeled'].values())}")
    for cat, items in results["labeled"].items():
        if items:
            print(f"  {cat}: {len(items)}")
    print(f"Kept (unlabeled): {len(results['kept_unlabeled'])}")
    if results["errors"]:
        print(f"Errors: {len(results['errors'])}")

if __name__ == "__main__":
    main()
