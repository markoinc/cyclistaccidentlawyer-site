#!/usr/bin/env python3
"""
Scrape Jacky Chou's Build in Public Notion page for On-Page SEO content.
Uses rotating residential proxies to avoid rate limits.
"""

import json
import requests
import time
import re
import random
from collections import defaultdict

BASE_URL = "https://indexsy.notion.site/api/v3"
PAGE_ID = "fe9a18a6-ded3-47fb-89e9-9012d2a67de8"

# Proxy config
PROXY_HOST = "p.webshare.io"
PROXY_PORT = 80
PROXY_USER_BASE = "dtwmetwu"
PROXY_PASS = "ww846x37mmd9"

def get_proxy():
    """Get a random rotating proxy."""
    user_num = random.randint(1, 10000)
    proxy_user = f"{PROXY_USER_BASE}-{user_num}"
    proxy_url = f"http://{proxy_user}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
    return {"http": proxy_url, "https": proxy_url}

def load_page_chunk(page_id, cursor=None, use_proxy=True):
    """Load a chunk of the Notion page."""
    url = f"{BASE_URL}/loadPageChunk"
    payload = {
        "pageId": page_id,
        "limit": 100,
        "cursor": cursor or {"stack": []},
        "chunkNumber": 0,
        "verticalColumns": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        proxies = get_proxy() if use_proxy else None
        resp = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=30)
        
        if resp.status_code == 429:
            print("Rate limited, waiting 60s...")
            time.sleep(60)
            return load_page_chunk(page_id, cursor, use_proxy)
            
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.ProxyError as e:
        print(f"Proxy error, retrying without proxy: {e}")
        return load_page_chunk(page_id, cursor, use_proxy=False)
    except Exception as e:
        print(f"Error loading chunk: {e}")
        return None

def extract_text_from_block(block):
    """Extract text content from a Notion block."""
    if not block or 'value' not in block:
        return "", ""
    
    value = block['value']
    block_type = value.get('type', '')
    properties = value.get('properties', {})
    
    # Extract title/text
    title_arr = properties.get('title', [])
    text_parts = []
    
    for part in title_arr:
        if isinstance(part, list) and len(part) > 0:
            text_parts.append(str(part[0]))
    
    text = " ".join(text_parts)
    
    return block_type, text

def get_all_blocks(page_id):
    """Fetch all blocks from a Notion page."""
    all_blocks = {}
    cursor = None
    chunk_num = 0
    
    while True:
        print(f"  Chunk {chunk_num}...", end=" ", flush=True)
        data = load_page_chunk(page_id, cursor)
        
        if not data:
            print("FAILED")
            break
            
        record_map = data.get('recordMap', {})
        blocks = record_map.get('block', {})
        
        print(f"got {len(blocks)} blocks")
        
        for block_id, block in blocks.items():
            all_blocks[block_id] = block
        
        # Check cursor for more data
        new_cursor = data.get('cursor', {})
        if not new_cursor.get('stack'):
            break
            
        cursor = new_cursor
        chunk_num += 1
        time.sleep(2)  # Longer delay
        
        if chunk_num > 20:  # Safety limit
            print("  Hit safety limit")
            break
    
    return all_blocks

# SEO-related keyword patterns
SEO_PATTERNS = {
    'title_tags': [
        r'title\s*tag', r'title\s*formula', r'headline', r'<title>', r'page title',
        r'meta title', r'seo title', r'title optimization'
    ],
    'meta_descriptions': [
        r'meta\s*desc', r'description\s*tag', r'meta tag', r'snippet',
        r'serp preview', r'search preview'
    ],
    'internal_linking': [
        r'internal\s*link', r'interlink', r'cross[-\s]?link', r'anchor\s*text',
        r'link\s*building', r'pillar\s*page', r'hub\s*page', r'silo',
        r'contextual\s*link', r'footer\s*link', r'sidebar\s*link', r'link\s*strategy'
    ],
    'content_structure': [
        r'h1', r'h2', r'h3', r'heading', r'subhead', r'content\s*structure',
        r'article\s*structure', r'outline', r'table\s*of\s*contents', r'toc',
        r'paragraph', r'bullet', r'list', r'formatting'
    ],
    'keyword_placement': [
        r'keyword\s*(place|dens|position)', r'keyword\s*in\s*title',
        r'keyword\s*in\s*h1', r'keyword\s*prominence', r'term\s*frequency',
        r'tf-idf', r'lsi', r'semantic', r'related\s*keyword', r'secondary\s*keyword'
    ],
    'page_speed': [
        r'page\s*speed', r'core\s*web\s*vital', r'lcp', r'fid', r'cls',
        r'lighthouse', r'pagespeed', r'loading', r'performance',
        r'image\s*optim', r'lazy\s*load', r'cdn', r'cache', r'compression'
    ],
    'content_optimization': [
        r'content\s*optim', r'content\s*quality', r'word\s*count', r'length',
        r'readability', r'engagement', r'helpful\s*content', r'e-?e-?a-?t',
        r'topical\s*auth', r'content\s*brief', r'surfer', r'clearscope', r'frase'
    ],
    'onpage_seo': [
        r'on-?page\s*seo', r'technical\s*seo', r'audit', r'checklist',
        r'seo\s*best\s*practice', r'optimization', r'ranking\s*factor'
    ]
}

def categorize_content(text):
    """Categorize text by SEO topic."""
    if not text or len(text) < 10:
        return None
        
    text_lower = text.lower()
    
    for category, patterns in SEO_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return category
    
    # General SEO check
    general_keywords = ['seo', 'rank', 'google', 'search', 'organic', 'traffic']
    if any(kw in text_lower for kw in general_keywords):
        return 'general_seo'
    
    return None

def main():
    print("=" * 60)
    print("Scraping Jacky Chou Build in Public - SEO Content")
    print("Using rotating residential proxies")
    print("=" * 60)
    
    # Wait a bit before starting (to clear any rate limits)
    print("\nStarting scrape...")
    time.sleep(2)
    
    # Fetch main page
    print(f"\nFetching main page: {PAGE_ID}")
    blocks = get_all_blocks(PAGE_ID)
    print(f"Found {len(blocks)} blocks in main page")
    
    if len(blocks) == 0:
        print("ERROR: No blocks fetched. Rate limit may still be active.")
        return
    
    # Get linked page IDs from content
    linked_pages = set()
    for block_id, block in blocks.items():
        if not block or 'value' not in block:
            continue
        value = block['value']
        if value.get('type') == 'page':
            linked_pages.add(block_id)
        content = value.get('content', [])
        for cid in content:
            if cid and cid not in blocks:
                linked_pages.add(cid)
    
    print(f"Found {len(linked_pages)} potential linked pages")
    
    # Fetch content from linked pages (limited)
    all_blocks = dict(blocks)
    pages_fetched = 0
    max_pages = 30  # Limit to avoid excessive requests
    
    for page_id in list(linked_pages)[:max_pages]:
        if page_id in all_blocks:
            continue
        print(f"\nFetching page {pages_fetched+1}/{max_pages}: {page_id[:8]}...")
        page_blocks = get_all_blocks(page_id)
        all_blocks.update(page_blocks)
        pages_fetched += 1
        time.sleep(3)
    
    print(f"\nTotal blocks collected: {len(all_blocks)}")
    
    # Categorize and extract content
    content_by_category = defaultdict(list)
    all_content = []
    
    for block_id, block in all_blocks.items():
        block_type, text = extract_text_from_block(block)
        
        if not text or len(text) < 5:
            continue
        
        # Store all meaningful content
        all_content.append({
            'type': block_type,
            'text': text,
            'id': block_id[:8]
        })
        
        # Categorize
        category = categorize_content(text)
        if category:
            content_by_category[category].append({
                'type': block_type,
                'text': text
            })
    
    # Generate comprehensive report
    report = f"""# Jacky Chou Build in Public - On-Page SEO & Content SOPs

**Source:** https://indexsy.notion.site/Build-in-Public-References-fe9a18a6ded347fb89e99012d2a67de8
**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC')}
**Total Blocks Analyzed:** {len(all_blocks)}
**Pages Crawled:** {pages_fetched + 1}
**SEO-Related Items Found:** {sum(len(v) for v in content_by_category.values())}

---

## Table of Contents

1. [Title Tag Formulas](#title-tag-formulas)
2. [Meta Description Templates](#meta-description-templates)
3. [Internal Linking Strategies](#internal-linking-strategies)
4. [Content Structure & Formatting](#content-structure--formatting)
5. [Keyword Placement](#keyword-placement)
6. [Page Speed & Core Web Vitals](#page-speed--core-web-vitals)
7. [Content Optimization](#content-optimization)
8. [General On-Page SEO](#general-on-page-seo)
9. [Raw Content](#raw-content)

---

"""

    # Add each category
    category_names = {
        'title_tags': 'Title Tag Formulas',
        'meta_descriptions': 'Meta Description Templates',
        'internal_linking': 'Internal Linking Strategies',
        'content_structure': 'Content Structure & Formatting',
        'keyword_placement': 'Keyword Placement',
        'page_speed': 'Page Speed & Core Web Vitals',
        'content_optimization': 'Content Optimization',
        'onpage_seo': 'General On-Page SEO',
        'general_seo': 'Additional SEO Insights'
    }
    
    for category, items in content_by_category.items():
        name = category_names.get(category, category.replace('_', ' ').title())
        report += f"## {name}\n\n"
        report += f"*{len(items)} items found*\n\n"
        
        for item in items:
            block_type = item['type']
            text = item['text']
            
            if block_type in ['header', 'sub_header']:
                report += f"### {text}\n\n"
            elif block_type == 'bulleted_list':
                report += f"- {text}\n"
            elif block_type == 'numbered_list':
                report += f"1. {text}\n"
            elif block_type == 'quote':
                report += f"> {text}\n\n"
            elif block_type == 'callout':
                report += f"📌 **{text}**\n\n"
            elif block_type == 'toggle':
                report += f"<details><summary>{text}</summary></details>\n\n"
            else:
                report += f"{text}\n\n"
        
        report += "\n---\n\n"
    
    # Add raw content section
    report += "## Raw Content\n\n"
    report += "*Full extracted content from all pages (first 500 items)*\n\n"
    
    for item in all_content[:500]:
        text = item['text']
        if len(text) > 500:
            text = text[:500] + "..."
        report += f"- [{item['type']}] {text}\n"
    
    # Save report
    output_path = "/home/ec2-user/clawd/data/jacky-brain/onpage-seo-sops.md"
    with open(output_path, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: {output_path}")
    print(f"Total content length: {len(report):,} characters")
    
    # Save categorized JSON
    json_path = "/home/ec2-user/clawd/data/jacky-brain/seo-content-categorized.json"
    with open(json_path, 'w') as f:
        json.dump({
            'categories': {k: v for k, v in content_by_category.items()},
            'stats': {
                'total_blocks': len(all_blocks),
                'pages_crawled': pages_fetched + 1,
                'seo_items': sum(len(v) for v in content_by_category.values())
            }
        }, f, indent=2)
    
    print(f"JSON data saved to: {json_path}")
    
    # Print summary
    print("\n📊 Summary by Category:")
    for category, items in sorted(content_by_category.items(), key=lambda x: -len(x[1])):
        print(f"  {category}: {len(items)} items")

if __name__ == "__main__":
    main()
