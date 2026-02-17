#!/usr/bin/env python3
"""
Notion Page Scraper - Extract all content from Jacky Chou's Build in Public Notion
Uses the Splitbee public API to access public Notion pages
"""

import json
import time
import sys
import os
import requests
from typing import Dict, List, Any, Optional

BASE_URL = "https://notion-api.splitbee.io/v1/page"
OUTPUT_DIR = os.path.expanduser("~/clawd/data/jacky-brain")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_page(page_id: str) -> Optional[Dict]:
    """Fetch a single Notion page by ID"""
    # Clean the ID (remove dashes for API)
    clean_id = page_id.replace("-", "")
    url = f"{BASE_URL}/{clean_id}"
    
    for attempt in range(3):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            elif resp.status_code == 429:
                print(f"  Rate limited, waiting {10 * (attempt + 1)}s...")
                time.sleep(10 * (attempt + 1))
            else:
                print(f"  Error {resp.status_code} for {page_id}")
                return None
        except Exception as e:
            print(f"  Exception: {e}")
            time.sleep(5)
    return None

def extract_text_from_rich_text(rich_text: List) -> str:
    """Extract plain text from Notion rich text array"""
    if not rich_text:
        return ""
    text_parts = []
    for item in rich_text:
        if isinstance(item, list):
            text_parts.append(item[0] if item else "")
        elif isinstance(item, str):
            text_parts.append(item)
    return "".join(text_parts)

def extract_block_content(block: Dict) -> str:
    """Extract content from a single block"""
    if "value" not in block:
        return ""
    
    value = block["value"]
    block_type = value.get("type", "")
    properties = value.get("properties", {})
    
    content = []
    
    if block_type == "page":
        title = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n## {title}\n")
        
    elif block_type == "text":
        text = extract_text_from_rich_text(properties.get("title", []))
        if text:
            content.append(text + "\n")
            
    elif block_type == "header":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n# {text}\n")
        
    elif block_type == "sub_header":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n## {text}\n")
        
    elif block_type == "sub_sub_header":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n### {text}\n")
        
    elif block_type == "bulleted_list":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"• {text}\n")
        
    elif block_type == "numbered_list":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"1. {text}\n")
        
    elif block_type == "to_do":
        text = extract_text_from_rich_text(properties.get("title", []))
        checked = properties.get("checked", [[False]])[0][0] if "checked" in properties else False
        checkbox = "[x]" if checked else "[ ]"
        content.append(f"- {checkbox} {text}\n")
        
    elif block_type == "toggle":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n<details>\n<summary>{text}</summary>\n")
        
    elif block_type == "quote":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n> {text}\n")
        
    elif block_type == "callout":
        text = extract_text_from_rich_text(properties.get("title", []))
        content.append(f"\n> 💡 {text}\n")
        
    elif block_type == "code":
        text = extract_text_from_rich_text(properties.get("title", []))
        language = extract_text_from_rich_text(properties.get("language", [[""]]))
        content.append(f"\n```{language}\n{text}\n```\n")
        
    elif block_type == "divider":
        content.append("\n---\n")
        
    elif block_type == "bookmark":
        link = properties.get("link", [[""]])[0][0] if "link" in properties else ""
        title = extract_text_from_rich_text(properties.get("title", []))
        if link:
            content.append(f"🔗 [{title or link}]({link})\n")
            
    elif block_type == "image":
        source = value.get("format", {}).get("display_source", "")
        if not source:
            # Try to get from properties
            source_prop = value.get("properties", {}).get("source", [[""]])
            source = source_prop[0][0] if source_prop else ""
        if source:
            content.append(f"\n![Image]({source})\n")
            
    elif block_type == "video":
        source = value.get("format", {}).get("display_source", "")
        if source:
            content.append(f"\n🎥 Video: {source}\n")
        else:
            # Check for embedded video URL
            embed = value.get("properties", {}).get("source", [[""]])
            if embed:
                content.append(f"\n🎥 Video: {embed[0][0]}\n")
                
    elif block_type == "embed":
        source = value.get("format", {}).get("display_source", "")
        if not source:
            source_prop = value.get("properties", {}).get("source", [[""]])
            source = source_prop[0][0] if source_prop else ""
        if source:
            content.append(f"\n📎 Embed: {source}\n")
            
    elif block_type == "table":
        content.append("\n[Table]\n")
        
    elif block_type == "column_list":
        pass  # Container, children handled separately
        
    elif block_type == "column":
        pass  # Container, children handled separately
    
    return "".join(content)

def process_page_data(page_data: Dict) -> str:
    """Process all blocks in a page and return markdown content"""
    content_parts = []
    
    for block_id, block in page_data.items():
        text = extract_block_content(block)
        if text:
            content_parts.append(text)
    
    return "".join(content_parts)

def get_subpages(page_data: Dict) -> List[Dict]:
    """Extract subpage references from page data"""
    subpages = []
    
    for block_id, block in page_data.items():
        if "value" not in block:
            continue
        value = block["value"]
        if value.get("type") == "page" and block_id != list(page_data.keys())[0]:
            title = ""
            if "properties" in value and "title" in value["properties"]:
                title = extract_text_from_rich_text(value["properties"]["title"])
            subpages.append({
                "id": block_id,
                "title": title
            })
    
    return subpages

def main():
    print("=" * 60)
    print("Jacky Chou Notion Scraper")
    print("=" * 60)
    
    # Load main page
    main_page_id = "fe9a18a6ded347fb89e99012d2a67de8"
    
    print(f"\nFetching main page: {main_page_id}")
    main_data = fetch_page(main_page_id)
    
    if not main_data:
        print("ERROR: Could not fetch main page!")
        sys.exit(1)
    
    # Save raw main page data
    with open(os.path.join(OUTPUT_DIR, "main_page_raw.json"), "w") as f:
        json.dump(main_data, f, indent=2)
    
    # Get all subpages
    subpages = get_subpages(main_data)
    print(f"\nFound {len(subpages)} subpages to process")
    
    # Process main page
    all_content = []
    all_content.append("# Jacky Chou - Build in Public References\n")
    all_content.append("*Extracted from Notion*\n\n")
    all_content.append("---\n\n")
    
    # Process each subpage
    processed = 0
    errors = 0
    
    for i, page in enumerate(subpages):
        page_id = page["id"]
        title = page["title"]
        
        print(f"\n[{i+1}/{len(subpages)}] Fetching: {title[:60]}...")
        
        page_data = fetch_page(page_id)
        
        if page_data:
            content = process_page_data(page_data)
            if content:
                all_content.append(f"\n# {title}\n")
                all_content.append(f"*Page ID: {page_id}*\n\n")
                all_content.append(content)
                all_content.append("\n---\n")
                processed += 1
        else:
            errors += 1
            all_content.append(f"\n# {title}\n")
            all_content.append(f"*Error fetching page: {page_id}*\n")
            all_content.append("\n---\n")
        
        # Rate limiting
        if (i + 1) % 10 == 0:
            print(f"  Progress: {i+1}/{len(subpages)} ({processed} successful, {errors} errors)")
            time.sleep(1)
    
    # Save final output
    output_path = os.path.join(OUTPUT_DIR, "notion-full-dump.md")
    with open(output_path, "w") as f:
        f.write("".join(all_content))
    
    print("\n" + "=" * 60)
    print(f"COMPLETE!")
    print(f"  Pages processed: {processed}")
    print(f"  Errors: {errors}")
    print(f"  Output: {output_path}")
    print("=" * 60)

if __name__ == "__main__":
    main()
