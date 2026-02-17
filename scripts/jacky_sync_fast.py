#!/usr/bin/env python3
"""Fast sync of Jacky Chou Build in Public content to Notion database."""

import requests
import json
import time
import sys
from pathlib import Path

# Config
NOTION_API_KEY = Path("~/.config/notion/api_key").expanduser().read_text().strip()
DATABASE_ID = "2f89371d-3030-8185-adbd-e6e4febece73"
SOURCE_PAGE_ID = "fe9a18a6-ded3-47fb-89e9-9012d2a67de8"
PROGRESS_FILE = Path("/tmp/jacky_sync_progress.json")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_existing_titles():
    """Get all existing page titles from our database."""
    titles = set()
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
            
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        if resp.status_code != 200:
            break
            
        data = resp.json()
        for page in data.get("results", []):
            title_prop = page.get("properties", {}).get("Name", {})
            if title_prop.get("title"):
                title_text = "".join([t.get("plain_text", "") for t in title_prop["title"]])
                titles.add(title_text.lower().strip())
                
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")
        
    return titles

def get_all_pages():
    """Get all pages from source."""
    # Get all block IDs
    url = "https://www.notion.so/api/v3/loadPageChunk"
    all_content = []
    
    for chunk in range(5):
        payload = {
            "pageId": SOURCE_PAGE_ID,
            "limit": 200,
            "cursor": {"stack": []},
            "chunkNumber": chunk,
            "verticalColumns": False
        }
        
        resp = requests.post(url, json=payload, timeout=30)
        if resp.status_code != 200:
            break
            
        data = resp.json()
        blocks = data.get("recordMap", {}).get("block", {})
        
        parent = blocks.get(SOURCE_PAGE_ID, {}).get("value", {})
        content = parent.get("content", [])
        all_content.extend(content)
        
        if not data.get("cursor", {}).get("stack"):
            break
    
    all_content = list(set(all_content))
    if SOURCE_PAGE_ID in all_content:
        all_content.remove(SOURCE_PAGE_ID)
    
    # Get page details in batches
    pages = []
    for i in range(0, len(all_content), 100):
        batch = all_content[i:i+100]
        reqs = [{"pointer": {"table": "block", "id": pid}, "version": -1} for pid in batch]
        
        resp = requests.post("https://www.notion.so/api/v3/syncRecordValues", json={"requests": reqs}, timeout=30)
        if resp.status_code != 200:
            continue
            
        data = resp.json()
        for block_id, block_data in data.get("recordMap", {}).get("block", {}).items():
            value = block_data.get("value", {})
            if value.get("type") == "page":
                props = value.get("properties", {})
                title_arr = props.get("title", [[""]])
                title = title_arr[0][0] if title_arr and title_arr[0] else "Untitled"
                
                # Check if created in last 2 years
                created = value.get("created_time", 0)
                two_years_ago = (time.time() - (2 * 365 * 24 * 60 * 60)) * 1000
                if created >= two_years_ago:
                    pages.append({"id": block_id, "title": title})
                    
    return pages

def categorize(title):
    """Categorize and determine type."""
    t = title.lower()
    
    if any(kw in t for kw in ["local seo", "gbp", "google business", "gmb", "map pack", "snack pack"]):
        cat = "Local SEO"
    elif any(kw in t for kw in ["schema", "technical", "structured", "core web"]):
        cat = "Technical SEO"
    elif any(kw in t for kw in ["ai", "chatgpt", "llm", "geo", "generative", "perplexity"]):
        cat = "AI SEO"
    elif any(kw in t for kw in ["link", "backlink", "outreach", "pbn", "dr"]):
        cat = "Link Building"
    elif any(kw in t for kw in ["content", "writing", "blog", "keyword"]):
        cat = "Content"
    elif any(kw in t for kw in ["reddit", "social", "twitter"]):
        cat = "Reddit"
    else:
        cat = "General"
        
    typ = "SOP" if any(kw in t for kw in ["how to", "guide", "checklist", "step"]) else "Training"
    
    return cat, typ

def create_page(title, category, page_type):
    """Create a minimal page quickly."""
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title[:2000]}}]},
            "Type": {"select": {"name": page_type}},
            "Source": {"select": {"name": "Jacky Chou"}},
            "Project": {"select": {"name": "SEO"}},
            "Status": {"select": {"name": "Final"}},
            "Tags": {"multi_select": [{"name": category}]}
        },
        "children": [
            {
                "object": "block",
                "type": "callout",
                "callout": {
                    "rich_text": [{"type": "text", "text": {"content": f"Jacky Chou Build in Public - {category}"}}],
                    "icon": {"emoji": "📺"}
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": f"Source: https://indexsy.notion.site"}}]}
            }
        ]
    }
    
    resp = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload, timeout=30)
    return resp.status_code == 200

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"synced": [], "created": 0, "skipped": 0, "errors": 0}

def save_progress(progress):
    PROGRESS_FILE.write_text(json.dumps(progress))

def main():
    print("=" * 60)
    print("Jacky Chou Build in Public → Notion Sync (FAST)")
    print("=" * 60)
    
    # Load progress
    progress = load_progress()
    synced_ids = set(progress.get("synced", []))
    
    # Get existing titles
    print("Checking existing pages...")
    existing = get_existing_titles()
    print(f"Found {len(existing)} existing pages")
    
    # Get all source pages
    print("Loading source pages...")
    pages = get_all_pages()
    print(f"Found {len(pages)} source pages")
    
    # Sync
    created = progress.get("created", 0)
    skipped = progress.get("skipped", 0)
    errors = progress.get("errors", 0)
    
    for i, page in enumerate(pages):
        pid = page["id"]
        title = page["title"]
        
        # Skip already processed
        if pid in synced_ids:
            continue
            
        # Skip duplicates
        if title.lower().strip() in existing:
            print(f"[{i+1}/{len(pages)}] SKIP: {title[:50]}")
            skipped += 1
            synced_ids.add(pid)
            continue
            
        # Create page
        cat, typ = categorize(title)
        print(f"[{i+1}/{len(pages)}] CREATE: {title[:50]}...")
        
        if create_page(title, cat, typ):
            created += 1
            existing.add(title.lower().strip())
        else:
            errors += 1
            
        synced_ids.add(pid)
        
        # Save progress every 10
        if i % 10 == 0:
            save_progress({"synced": list(synced_ids), "created": created, "skipped": skipped, "errors": errors})
            
        time.sleep(0.35)  # Rate limit ~3/sec
        
    # Final save
    save_progress({"synced": list(synced_ids), "created": created, "skipped": skipped, "errors": errors})
    
    print("\n" + "=" * 60)
    print(f"SYNC COMPLETE")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors: {errors}")
    print("=" * 60)

if __name__ == "__main__":
    main()
