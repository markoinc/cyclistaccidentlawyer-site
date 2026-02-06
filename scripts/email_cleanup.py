#!/usr/bin/env python3
"""Deep Email Cleanup for mark@kuriosbrand.com - Last 30 Days"""

import json
import requests
import time
import re
import sys
from datetime import datetime, timezone, timedelta

# Config
USER_ID = "mark@kuriosbrand.com"
BASE_URL = f"https://gmail.googleapis.com/gmail/v1/users/{USER_ID}"

# Label IDs
LABELS = {
    "prospects": "Label_1",
    "partners": "Label_2",
    "calls": "Label_3",
    "important": "Label_4",
    "junk": "Label_5",
}

# Refresh token
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

# Tracking
stats = {
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
    "urgent_items": [],
    "errors": [],
}

# Keywords/patterns for categorization
WP_UPDATE_PATTERNS = [
    r"wordpress.*auto.?update",
    r"wordpress.*update",
    r"\[.*\].*has been updated",
    r"\[.*\].*updated successfully",
    r"your site.*updated",
    r"plugin.*updated",
    r"theme.*updated",
    r"wordpress.*\d+\.\d+",
    r"background update.*finished",
    r"some plugins.*updated",
    r"some themes.*updated",
    r"has been updated to",
    r"auto.?update.*completed",
    r"wordpress\s+\d+\.\d+(\.\d+)?\s+is available",
    r"please update",
]

WP_COMMENT_PATTERNS = [
    r"new comment on",
    r"comment.*moderation",
    r"comment.*awaiting",
    r"pingback",
    r"trackback",
    r"\[.*\].*comment:",
    r"\[.*\].*please moderate",
    r"a new comment on the post",
]

COLD_OUTREACH_PATTERNS = [
    r"seo (service|audit|pitch|proposal|package)",
    r"(working|growth) capital",
    r"google street view",
    r"google maps.*photo",
    r"virtual tour",
    r"web design (service|proposal|quote)",
    r"domain.*for sale",
    r"domain.*expir",
    r"estimating service",
    r"(concrete|construction) estimat",
    r"(business|merchant) (loan|funding|cash advance)",
    r"lead gen.*service",
    r"marketing agency",
    r"boost your (ranking|traffic|seo|business)",
    r"hi mike",  # common spam misname
    r"quick question about your (website|business)",
    r"noticed your (website|business)",
    r"i came across your",
    r"i was browsing",
    r"partnership opportunity",
    r"collaboration opportunity",
    r"backlink",
    r"guest post",
    r"link building",
    r"press release",
    r"yellow letters",
    r"workers.?comp",
    r"insurance quote",
    r"payroll service",
    r"bookkeeping service",
    r"reputation management",
]

WARMUP_PATTERNS = [
    r"instantly\.ai",
    r"lemwarm",
    r"warmup",
    r"warm.?up",
    r"mailwarm",
    r"email warm",
    r"warmbox",
    r"inbox warm",
]

# Partner identifiers
PARTNER_PATTERNS = [
    r"cases on demand",
    r"casesondemand",
    r"inquired esquire",
    r"inquiredesquire",
    r"carlos",
    r"max\b",
    r"jeremy",
    r"patrick",
    r"scott poisson",
    r"poisson",
    r"law firm",
    r"legal",
    r"attorney",
    r"esquire",
]

PARTNER_EMAILS = [
    "carlos", "max", "jeremy", "patrick", "scott", "poisson",
    "casesondemand", "inquiredesquire", "inquired",
]

# Important senders we NEVER trash
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
    "twilio", "sendgrid",
]

# Concrete site domains (WordPress notifications from these = trash)
CONCRETE_SITE_PATTERNS = [
    r"concrete",
    r"masonry",
    r"paving",
    r"foundation",
    r"driveway",
    r"flatwork",
    r"stamped",
    r"decorative",
    r"wordpress@",
    r"wordpress",
]

def get_header(headers, name):
    """Extract header value by name"""
    for h in headers:
        if h["name"].lower() == name.lower():
            return h.get("value", "")
    return ""

def is_wordpress_update(subject, from_addr, snippet):
    """Check if email is a WordPress auto-update notification"""
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    
    # Must be from WordPress or contain WP update patterns
    is_wp_sender = "wordpress" in from_lower or "wp-" in from_lower
    
    for pattern in WP_UPDATE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            if is_wp_sender or "wordpress" in text:
                return True
    return False

def is_wordpress_comment(subject, from_addr, snippet):
    """Check if email is WordPress comment spam/moderation"""
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    
    for pattern in WP_COMMENT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            if "wordpress" in from_lower or "wordpress" in text or "@" in from_lower:
                return True
    return False

def is_cold_outreach(subject, from_addr, to_addr, snippet):
    """Check if email is cold outreach/spam"""
    text = f"{subject} {snippet}".lower()
    
    for pattern in COLD_OUTREACH_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def is_warmup(subject, from_addr, snippet):
    """Check if email is a warmup campaign email"""
    text = f"{subject} {from_addr} {snippet}".lower()
    for pattern in WARMUP_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def is_safe_sender(from_addr):
    """Check if sender is on the safe list"""
    from_lower = from_addr.lower()
    for safe in SAFE_SENDERS:
        if safe in from_lower:
            return True
    return False

def is_partner(from_addr, subject, snippet):
    """Check if email is from a partner"""
    text = f"{from_addr} {subject} {snippet}".lower()
    from_lower = from_addr.lower()
    
    for email_part in PARTNER_EMAILS:
        if email_part in from_lower:
            return True
    
    for pattern in PARTNER_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def is_call_transcript(subject, from_addr, snippet):
    """Check if email is a meeting/call transcript"""
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    
    patterns = [
        r"transcript", r"call summary", r"meeting summary",
        r"meeting notes", r"recording", r"call recording",
        r"fireflies", r"gemini.*notes", r"google meet",
        r"fathom", r"otter\.ai", r"call recap",
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    if "fireflies" in from_lower or "fathom" in from_lower or "otter" in from_lower:
        return True
    return False

def is_prospect_lead(subject, from_addr, snippet):
    """Check if email looks like it's from a prospect or lead"""
    text = f"{subject} {snippet}".lower()
    from_lower = from_addr.lower()
    
    patterns = [
        r"(free|get a) (quote|estimate|consultation)",
        r"interested in",
        r"need (concrete|paving|masonry|foundation)",
        r"looking for (a |)(contractor|concrete|paving)",
        r"contact form",
        r"new lead",
        r"form submission",
        r"new submission",
        r"inquiry",
        r"request a quote",
        r"rb2b",
    ]
    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    if "rb2b" in from_lower:
        return True
    return False

def categorize_email(msg_id, subject, from_addr, to_addr, snippet, label_ids):
    """Categorize an email and return action"""
    # Already in TRASH or SPAM? Skip
    if "TRASH" in (label_ids or []) or "SPAM" in (label_ids or []):
        return "skip", None, "Already in trash/spam"
    
    from_lower = from_addr.lower()
    subject_lower = subject.lower()
    
    # SAFE SENDERS - never trash
    if is_safe_sender(from_addr):
        # Sub-categorize
        if is_call_transcript(subject, from_addr, snippet):
            return "label", "calls", f"Call transcript from safe sender"
        if is_partner(from_addr, subject, snippet):
            return "label", "partners", f"Partner email"
        if is_prospect_lead(subject, from_addr, snippet):
            return "label", "prospects", f"Prospect/lead from safe sender"
        return "keep", None, f"Safe sender: {from_addr}"
    
    # PARTNER check (before trash checks)
    if is_partner(from_addr, subject, snippet):
        return "label", "partners", f"Partner email"
    
    # CALL TRANSCRIPT check
    if is_call_transcript(subject, from_addr, snippet):
        return "label", "calls", f"Call transcript"
    
    # PROSPECT/LEAD check
    if is_prospect_lead(subject, from_addr, snippet):
        return "label", "prospects", f"Prospect/lead email"
    
    # TRASH CHECKS
    # WordPress updates
    if is_wordpress_update(subject, from_addr, snippet):
        return "trash", "wordpress_updates", f"WordPress update notification"
    
    # WordPress comments
    if is_wordpress_comment(subject, from_addr, snippet):
        return "trash", "wordpress_comments", f"WordPress comment notification"
    
    # Warmup emails
    if is_warmup(subject, from_addr, snippet):
        return "trash", "warmup_emails", f"Warmup campaign email"
    
    # Cold outreach
    if is_cold_outreach(subject, from_addr, to_addr, snippet):
        # Extra safety: don't trash if it looks like it might be from a real prospect
        if any(x in from_lower for x in ["law", "legal", "attorney", "esquire"]):
            return "label", "prospects", f"Possible legal prospect (spared from cold outreach trash)"
        return "trash", "cold_outreach_spam", f"Cold outreach/spam"
    
    # Default: keep without label
    return "keep", None, f"Uncategorized - keeping"

def fetch_messages(query, page_token=None):
    """Fetch message list"""
    params = {"q": query, "maxResults": 50}
    if page_token:
        params["pageToken"] = page_token
    
    resp = requests.get(f"{BASE_URL}/messages", headers=HEADERS, params=params)
    if resp.status_code != 200:
        print(f"ERROR fetching messages: {resp.status_code} {resp.text}", file=sys.stderr)
        return None, None
    
    data = resp.json()
    messages = data.get("messages", [])
    next_token = data.get("nextPageToken")
    return messages, next_token

def get_message(msg_id):
    """Get message details"""
    resp = requests.get(f"{BASE_URL}/messages/{msg_id}", headers=HEADERS, 
                       params={"format": "metadata", "metadataHeaders": ["Subject", "From", "To", "Date"]})
    if resp.status_code != 200:
        print(f"ERROR getting message {msg_id}: {resp.status_code}", file=sys.stderr)
        return None
    return resp.json()

def trash_message(msg_id):
    """Move message to trash"""
    resp = requests.post(f"{BASE_URL}/messages/{msg_id}/trash", headers=HEADERS)
    return resp.status_code == 200

def label_message(msg_id, label_id):
    """Add label to message"""
    resp = requests.post(f"{BASE_URL}/messages/{msg_id}/modify", headers=HEADERS,
                        json={"addLabelIds": [label_id]})
    return resp.status_code == 200

def process_batch(messages):
    """Process a batch of messages"""
    global TOKEN, HEADERS
    
    for msg_ref in messages:
        msg_id = msg_ref["id"]
        
        # Get message details
        msg = get_message(msg_id)
        if not msg:
            stats["errors"].append(f"Failed to fetch {msg_id}")
            continue
        
        headers = msg.get("payload", {}).get("headers", [])
        subject = get_header(headers, "Subject")
        from_addr = get_header(headers, "From")
        to_addr = get_header(headers, "To")
        date_str = get_header(headers, "Date")
        snippet = msg.get("snippet", "")
        label_ids = msg.get("labelIds", [])
        
        stats["total_processed"] += 1
        
        action, category, reason = categorize_email(msg_id, subject, from_addr, to_addr, snippet, label_ids)
        
        email_info = {
            "id": msg_id,
            "subject": subject[:100],
            "from": from_addr[:80],
            "to": to_addr[:80] if to_addr else "",
            "date": date_str,
            "reason": reason,
            "snippet": snippet[:100],
        }
        
        if action == "trash":
            success = trash_message(msg_id)
            if success:
                stats["trash_categories"][category].append(email_info)
                stats["trashed"].append(email_info)
                print(f"  🗑️  TRASHED [{category}]: {subject[:60]} | From: {from_addr[:40]}")
            else:
                stats["errors"].append(f"Failed to trash {msg_id}: {subject[:50]}")
                print(f"  ❌ FAILED TO TRASH: {subject[:60]}")
                
        elif action == "label":
            label_id = LABELS.get(category)
            if label_id:
                success = label_message(msg_id, label_id)
                if success:
                    stats["labeled"][category].append(email_info)
                    print(f"  🏷️  LABELED [{category}]: {subject[:60]} | From: {from_addr[:40]}")
                else:
                    stats["errors"].append(f"Failed to label {msg_id}: {subject[:50]}")
                    
        elif action == "keep":
            stats["kept_unlabeled"].append(email_info)
            print(f"  ✅ KEPT: {subject[:60]} | From: {from_addr[:40]}")
            
        elif action == "skip":
            print(f"  ⏭️  SKIP (already trashed/spam): {subject[:60]}")
        
        # Rate limiting
        time.sleep(0.1)

def main():
    global TOKEN, HEADERS
    
    # 30 days ago epoch (Jan 4, 2026)
    thirty_days_ago = int((datetime(2026, 1, 4, tzinfo=timezone.utc)).timestamp())
    query = f"after:{thirty_days_ago}"
    
    print(f"🔍 Querying emails after {datetime.fromtimestamp(thirty_days_ago, tz=timezone.utc)}")
    print(f"   Query: {query}")
    print("=" * 80)
    
    page = 0
    page_token = None
    
    while True:
        page += 1
        print(f"\n📦 Batch {page}...")
        
        messages, next_token = fetch_messages(query, page_token)
        
        if messages is None:
            # Maybe token expired, refresh
            print("Refreshing token...")
            TOKEN = get_token()
            HEADERS = {"Authorization": f"Bearer {TOKEN}"}
            messages, next_token = fetch_messages(query, page_token)
            if messages is None:
                print("FATAL: Cannot fetch messages after refresh")
                break
        
        if not messages:
            print("No more messages.")
            break
        
        print(f"   Processing {len(messages)} messages...")
        process_batch(messages)
        
        if not next_token:
            print("\nNo more pages.")
            break
        
        page_token = next_token
        print(f"   Next page token: {next_token[:20]}...")
        time.sleep(0.5)
    
    # Generate report
    print("\n" + "=" * 80)
    print("📊 EMAIL CLEANUP REPORT")
    print("=" * 80)
    
    print(f"\n1. TOTAL EMAILS PROCESSED: {stats['total_processed']}")
    
    print(f"\n2. TOTAL TRASHED: {len(stats['trashed'])}")
    for cat, emails in stats["trash_categories"].items():
        if emails:
            print(f"   - {cat}: {len(emails)}")
            for e in emails[:5]:
                print(f"     • {e['subject'][:70]} | {e['from'][:50]}")
            if len(emails) > 5:
                print(f"     ... and {len(emails) - 5} more")
    
    print(f"\n3. TOTAL LABELED: {sum(len(v) for v in stats['labeled'].values())}")
    for cat, emails in stats["labeled"].items():
        if emails:
            print(f"   - {cat} (Sierra/{cat.title()}): {len(emails)}")
            for e in emails:
                print(f"     • {e['subject'][:70]} | {e['from'][:50]} | {e['date']}")
    
    print(f"\n4. KEPT (unlabeled): {len(stats['kept_unlabeled'])}")
    for e in stats["kept_unlabeled"]:
        print(f"   • {e['subject'][:70]} | {e['from'][:50]}")
    
    if stats["errors"]:
        print(f"\n5. ERRORS: {len(stats['errors'])}")
        for err in stats["errors"]:
            print(f"   ❌ {err}")
    
    # Save detailed results to JSON
    with open("/home/ec2-user/clawd/scripts/email_cleanup_results.json", "w") as f:
        json.dump(stats, f, indent=2, default=str)
    
    print(f"\n✅ Detailed results saved to email_cleanup_results.json")

if __name__ == "__main__":
    main()
