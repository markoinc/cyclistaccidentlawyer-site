#!/usr/bin/env python3
"""Sync Jacky Chou Build in Public content to Notion database."""

import requests
import json
import time
import re
from pathlib import Path

# Config
NOTION_API_KEY = Path("~/.config/notion/api_key").expanduser().read_text().strip()
DATABASE_ID = "2f89371d-3030-8185-adbd-e6e4febece73"
SOURCE_PAGE_ID = "fe9a18a6-ded3-47fb-89e9-9012d2a67de8"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_existing_titles():
    """Get all existing page titles from our database to avoid duplicates."""
    titles = set()
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    has_more = True
    start_cursor = None
    
    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor
            
        resp = requests.post(url, headers=HEADERS, json=payload)
        if resp.status_code != 200:
            print(f"Error querying database: {resp.text}")
            break
            
        data = resp.json()
        for page in data.get("results", []):
            title_prop = page.get("properties", {}).get("Name", {})
            if title_prop.get("title"):
                title_text = "".join([t.get("plain_text", "") for t in title_prop["title"]])
                titles.add(title_text.lower().strip())
                
        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor")
        
    print(f"Found {len(titles)} existing pages in database")
    return titles

def get_source_page_ids():
    """Get all child page IDs from the Build in Public References page."""
    url = "https://www.notion.so/api/v3/loadPageChunk"
    all_ids = []
    cursor = {"stack": []}
    
    # We need to paginate to get all IDs
    for chunk in range(5):  # Should be enough for ~200 pages
        payload = {
            "pageId": SOURCE_PAGE_ID,
            "limit": 100,
            "cursor": cursor,
            "chunkNumber": chunk,
            "verticalColumns": False
        }
        
        resp = requests.post(url, json=payload)
        if resp.status_code != 200:
            print(f"Error loading page chunk: {resp.text}")
            break
            
        data = resp.json()
        blocks = data.get("recordMap", {}).get("block", {})
        
        for block_id, block_data in blocks.items():
            if block_id == SOURCE_PAGE_ID:
                # This is the parent page with content list
                content = block_data.get("value", {}).get("content", [])
                all_ids.extend(content)
                
        cursor = data.get("cursor", {"stack": []})
        if not cursor.get("stack"):
            break
            
    # Remove the parent page ID and dedupe
    all_ids = list(set(all_ids))
    if SOURCE_PAGE_ID in all_ids:
        all_ids.remove(SOURCE_PAGE_ID)
        
    print(f"Found {len(all_ids)} block IDs in source page")
    return all_ids

def get_page_details(page_ids):
    """Get details for pages using syncRecordValues."""
    pages = []
    
    # Batch requests (max 100 per request)
    for i in range(0, len(page_ids), 50):
        batch = page_ids[i:i+50]
        requests_list = [{"pointer": {"table": "block", "id": pid}, "version": -1} for pid in batch]
        
        resp = requests.post(
            "https://www.notion.so/api/v3/syncRecordValues",
            json={"requests": requests_list}
        )
        
        if resp.status_code != 200:
            print(f"Error syncing records: {resp.text}")
            continue
            
        data = resp.json()
        blocks = data.get("recordMap", {}).get("block", {})
        
        for block_id, block_data in blocks.items():
            value = block_data.get("value", {})
            block_type = value.get("type")
            
            if block_type == "page":
                props = value.get("properties", {})
                title_arr = props.get("title", [[""]])
                title = title_arr[0][0] if title_arr and title_arr[0] else "Untitled"
                
                pages.append({
                    "id": block_id,
                    "title": title,
                    "created_time": value.get("created_time"),
                    "last_edited_time": value.get("last_edited_time")
                })
                
        time.sleep(0.3)  # Rate limit
        
    print(f"Found {len(pages)} pages (filtered from {len(page_ids)} blocks)")
    return pages

def get_page_content(page_id):
    """Get the full content of a page."""
    url = "https://www.notion.so/api/v3/loadPageChunk"
    payload = {
        "pageId": page_id,
        "limit": 100,
        "cursor": {"stack": []},
        "chunkNumber": 0,
        "verticalColumns": False
    }
    
    resp = requests.post(url, json=payload)
    if resp.status_code != 200:
        return []
        
    data = resp.json()
    blocks = data.get("recordMap", {}).get("block", {})
    
    content_blocks = []
    page_data = blocks.get(page_id, {}).get("value", {})
    content_ids = page_data.get("content", [])
    
    for cid in content_ids:
        if cid in blocks:
            block = blocks[cid].get("value", {})
            block_type = block.get("type")
            props = block.get("properties", {})
            
            if block_type in ["text", "bulleted_list", "numbered_list", "toggle", "quote", "callout"]:
                title = props.get("title", [[""]])
                if title and title[0]:
                    text = "".join([t[0] if isinstance(t, list) else str(t) for t in title])
                    content_blocks.append({"type": block_type, "text": text})
            elif block_type == "header":
                title = props.get("title", [[""]])
                if title and title[0]:
                    text = "".join([t[0] if isinstance(t, list) else str(t) for t in title])
                    content_blocks.append({"type": "heading_1", "text": text})
            elif block_type == "sub_header":
                title = props.get("title", [[""]])
                if title and title[0]:
                    text = "".join([t[0] if isinstance(t, list) else str(t) for t in title])
                    content_blocks.append({"type": "heading_2", "text": text})
            elif block_type == "sub_sub_header":
                title = props.get("title", [[""]])
                if title and title[0]:
                    text = "".join([t[0] if isinstance(t, list) else str(t) for t in title])
                    content_blocks.append({"type": "heading_3", "text": text})
                    
    return content_blocks

def categorize_episode(title):
    """Categorize episode based on title."""
    title_lower = title.lower()
    
    if any(kw in title_lower for kw in ["local seo", "gbp", "google business", "local pack", "gmb", "map pack"]):
        return "Local SEO"
    elif any(kw in title_lower for kw in ["schema", "technical", "structured data", "core web", "site speed"]):
        return "Technical SEO"
    elif any(kw in title_lower for kw in ["ai", "chatgpt", "llm", "geo", "generative", "perplexity", "claude"]):
        return "AI SEO / GEO"
    elif any(kw in title_lower for kw in ["link building", "backlink", "outreach", "dr", "domain rating", "link", "links"]):
        return "Link Building"
    elif any(kw in title_lower for kw in ["content", "writing", "blog", "article", "keyword"]):
        return "Content Strategy"
    elif any(kw in title_lower for kw in ["reddit", "social", "twitter", "linkedin"]):
        return "Reddit Marketing"
    else:
        return "General SEO"

def determine_type(title):
    """Determine if this is Training or SOP based on title."""
    title_lower = title.lower()
    if any(kw in title_lower for kw in ["how to", "guide", "checklist", "sop", "process", "step by step"]):
        return "SOP"
    return "Training"

def create_notion_page(title, content_blocks, category):
    """Create a page in our Notion database."""
    url = "https://api.notion.com/v1/pages"
    
    # Build children blocks
    children = []
    
    # Add category as a callout
    children.append({
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": f"Category: {category}"}}],
            "icon": {"emoji": "📚"}
        }
    })
    
    for block in content_blocks[:95]:  # Notion API limit is 100 blocks
        if block["type"] == "heading_1":
            children.append({
                "object": "block",
                "type": "heading_1",
                "heading_1": {"rich_text": [{"type": "text", "text": {"content": block["text"][:2000]}}]}
            })
        elif block["type"] == "heading_2":
            children.append({
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"type": "text", "text": {"content": block["text"][:2000]}}]}
            })
        elif block["type"] == "heading_3":
            children.append({
                "object": "block",
                "type": "heading_3",
                "heading_3": {"rich_text": [{"type": "text", "text": {"content": block["text"][:2000]}}]}
            })
        elif block["type"] == "bulleted_list":
            children.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": block["text"][:2000]}}]}
            })
        elif block["type"] == "numbered_list":
            children.append({
                "object": "block",
                "type": "numbered_list_item",
                "numbered_list_item": {"rich_text": [{"type": "text", "text": {"content": block["text"][:2000]}}]}
            })
        else:
            # Default to paragraph
            children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"type": "text", "text": {"content": block["text"][:2000]}}]}
            })
    
    if not children:
        children.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": [{"type": "text", "text": {"content": "Content from Jacky Chou's Build in Public series."}}]}
        })
    
    page_type = determine_type(title)
    
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
        "children": children
    }
    
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        print(f"Error creating page '{title[:50]}...': {resp.status_code} - {resp.text[:200]}")
        return False
    return True

def is_recent(page):
    """Check if page was created in the last 2 years."""
    created = page.get("created_time", 0)
    if created:
        # created_time is in milliseconds
        two_years_ago = (time.time() - (2 * 365 * 24 * 60 * 60)) * 1000
        return created >= two_years_ago
    return True  # If no date, include it

def main():
    print("=" * 60)
    print("Jacky Chou Build in Public → Notion Sync")
    print("=" * 60)
    
    # Step 1: Get existing pages to avoid duplicates
    existing_titles = get_existing_titles()
    
    # Step 2: Get all page IDs from source
    page_ids = get_source_page_ids()
    
    # Step 3: Get page details
    pages = get_page_details(page_ids)
    
    # Step 4: Filter for recent pages
    recent_pages = [p for p in pages if is_recent(p)]
    print(f"Filtered to {len(recent_pages)} recent pages (last 2 years)")
    
    # Step 5: Create pages
    created = 0
    skipped = 0
    errors = 0
    
    for i, page in enumerate(recent_pages):
        title = page["title"]
        title_lower = title.lower().strip()
        
        # Skip if already exists
        if title_lower in existing_titles:
            print(f"[{i+1}/{len(recent_pages)}] SKIP (exists): {title[:60]}")
            skipped += 1
            continue
            
        # Get content
        print(f"[{i+1}/{len(recent_pages)}] Syncing: {title[:60]}...")
        content = get_page_content(page["id"])
        category = categorize_episode(title)
        
        # Create page
        if create_notion_page(title, content, category):
            created += 1
            existing_titles.add(title_lower)  # Track to avoid re-creating
        else:
            errors += 1
            
        time.sleep(0.5)  # Rate limit
        
    print("\n" + "=" * 60)
    print(f"SYNC COMPLETE")
    print(f"  Created: {created}")
    print(f"  Skipped (duplicates): {skipped}")
    print(f"  Errors: {errors}")
    print("=" * 60)

if __name__ == "__main__":
    main()
