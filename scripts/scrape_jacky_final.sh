#!/bin/bash
# Scrape Jacky Chou Build in Public Notion page

OUTPUT_DIR="/home/ec2-user/clawd/data/jacky-brain"
mkdir -p "$OUTPUT_DIR"

PROXY="http://dtwmetwu-7500:ww846x37mmd9@p.webshare.io:80"
PAGE_ID="fe9a18a6-ded3-47fb-89e9-9012d2a67de8"

fetch_chunk() {
    local page_id=$1
    local cursor=$2
    local output=$3
    local proxy_num=$((RANDOM % 10000 + 1))
    local proxy="http://dtwmetwu-${proxy_num}:ww846x37mmd9@p.webshare.io:80"
    
    curl -s --proxy "$proxy" \
        -H 'Content-Type: application/json' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36' \
        -H 'Accept: application/json' \
        -H 'Accept-Language: en-US,en;q=0.9' \
        -H 'Origin: https://indexsy.notion.site' \
        -H 'Referer: https://indexsy.notion.site/Build-in-Public-References-fe9a18a6ded347fb89e99012d2a67de8' \
        'https://indexsy.notion.site/api/v3/loadPageChunk' \
        -d "{
            \"pageId\": \"$page_id\",
            \"limit\": 300,
            \"cursor\": $cursor,
            \"chunkNumber\": 0,
            \"verticalColumns\": false
        }" > "$output"
}

echo "=== Scraping Jacky Chou Build in Public ==="
echo "Output directory: $OUTPUT_DIR"

# Fetch main page chunks
echo ""
echo "Fetching main page..."

cursor='{"stack":[]}'
chunk_num=1

while true; do
    output="$OUTPUT_DIR/chunk_${chunk_num}.json"
    echo "  Chunk $chunk_num..."
    fetch_chunk "$PAGE_ID" "$cursor" "$output"
    
    # Check if valid JSON
    if ! jq -e . "$output" > /dev/null 2>&1; then
        echo "    ERROR: Invalid JSON in chunk $chunk_num"
        cat "$output" | head -100
        break
    fi
    
    # Get block count
    block_count=$(jq '.recordMap.block | length' "$output" 2>/dev/null || echo "0")
    echo "    Got $block_count blocks"
    
    # Check for next cursor
    next_cursor=$(jq -c '.cursor' "$output" 2>/dev/null)
    has_stack=$(jq '.cursor.stack | length > 0' "$output" 2>/dev/null)
    
    if [ "$has_stack" != "true" ]; then
        echo "  No more chunks to fetch"
        break
    fi
    
    cursor="$next_cursor"
    chunk_num=$((chunk_num + 1))
    sleep 2
    
    if [ $chunk_num -gt 15 ]; then
        echo "  Safety limit reached"
        break
    fi
done

echo ""
echo "Merging chunks..."

# Merge all chunks and extract content
python3 << 'PYTHON'
import json
import glob
import os
from collections import defaultdict

output_dir = "/home/ec2-user/clawd/data/jacky-brain"
chunks = sorted(glob.glob(f"{output_dir}/chunk_*.json"))

all_blocks = {}
for chunk_file in chunks:
    try:
        with open(chunk_file) as f:
            data = json.load(f)
        blocks = data.get('recordMap', {}).get('block', {})
        all_blocks.update(blocks)
    except:
        continue

print(f"Total blocks collected: {len(all_blocks)}")

# Extract text from blocks
def extract_text(block):
    if not block or 'value' not in block:
        return "", ""
    
    value = block['value']
    block_type = value.get('type', '')
    properties = value.get('properties', {})
    
    title_arr = properties.get('title', [])
    text_parts = []
    
    for part in title_arr:
        if isinstance(part, list) and len(part) > 0:
            text_parts.append(str(part[0]))
    
    return block_type, " ".join(text_parts)

# SEO-related keyword patterns
seo_keywords = [
    'seo', 'title', 'meta', 'description', 'keyword', 'content', 'optimize', 
    'ranking', 'serp', 'link', 'internal', 'external', 'anchor', 'heading',
    'h1', 'h2', 'h3', 'structure', 'schema', 'speed', 'core web vitals',
    'lcp', 'fid', 'cls', 'page speed', 'image', 'alt', 'compression',
    'topical', 'cluster', 'silo', 'pillar', 'hub', 'spoke', 'article',
    'blog', 'post', 'word count', 'format', 'writing', 'outline', 'brief',
    'template', 'checklist', 'audit', 'on-page', 'onpage', 'technical',
    'crawl', 'index', 'canonical', 'url', 'slug', 'permalink',
    'featured snippet', 'rich result', 'faq', 'people also ask',
    'parasite', 'programmatic', 'ai content', 'surfer', 'clearscope',
    'google', 'algorithm', 'update', 'traffic', 'clicks', 'ctr',
    'entity', 'semantic', 'nlp', 'topic', 'relevance', 'backlink',
    'authority', 'trust', 'expertise', 'e-e-a-t', 'eeat', 'eat',
    'helpful content', 'hcu', 'ranking factor', 'nap', 'local'
]

def is_seo_related(text):
    if not text:
        return False
    text_lower = text.lower()
    return any(kw in text_lower for kw in seo_keywords)

# Categorize content
content_by_category = defaultdict(list)
all_content = []

for block_id, block in all_blocks.items():
    block_type, text = extract_text(block)
    
    if not text or len(text) < 5:
        continue
    
    all_content.append({
        'type': block_type,
        'text': text,
        'id': block_id[:8]
    })
    
    text_lower = text.lower()
    
    # Categorize
    if 'title tag' in text_lower or 'title formula' in text_lower or 'headline formula' in text_lower:
        content_by_category['title_tags'].append(text)
    elif 'meta desc' in text_lower or 'meta description' in text_lower:
        content_by_category['meta_descriptions'].append(text)
    elif 'internal link' in text_lower or 'interlink' in text_lower or 'anchor text' in text_lower:
        content_by_category['internal_linking'].append(text)
    elif 'heading' in text_lower or 'h1' in text_lower or 'structure' in text_lower or 'outline' in text_lower:
        content_by_category['content_structure'].append(text)
    elif 'keyword' in text_lower:
        content_by_category['keyword_placement'].append(text)
    elif 'page speed' in text_lower or 'core web' in text_lower or 'lcp' in text_lower or 'performance' in text_lower:
        content_by_category['page_speed'].append(text)
    elif 'content' in text_lower and ('optim' in text_lower or 'quality' in text_lower or 'brief' in text_lower):
        content_by_category['content_optimization'].append(text)
    elif 'on-page' in text_lower or 'onpage' in text_lower or 'audit' in text_lower or 'checklist' in text_lower:
        content_by_category['onpage_seo'].append(text)
    elif is_seo_related(text):
        content_by_category['general_seo'].append(text)

# Generate report
import time
report = f"""# Jacky Chou Build in Public - On-Page SEO & Content SOPs

**Source:** https://indexsy.notion.site/Build-in-Public-References-fe9a18a6ded347fb89e99012d2a67de8
**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC')}
**Total Blocks Analyzed:** {len(all_blocks)}
**SEO-Related Items Found:** {sum(len(v) for v in content_by_category.values())}

---

## 📋 Quick Navigation

1. [Title Tag Formulas](#-title-tag-formulas)
2. [Meta Description Templates](#-meta-description-templates)
3. [Internal Linking Strategies](#-internal-linking-strategies)
4. [Content Structure & Formatting](#-content-structure--formatting)
5. [Keyword Placement](#-keyword-placement)
6. [Page Speed & Core Web Vitals](#-page-speed--core-web-vitals)
7. [Content Optimization](#-content-optimization)
8. [On-Page SEO Checklists](#-on-page-seo-checklists)
9. [General SEO Insights](#-general-seo-insights)
10. [All Extracted Content](#-all-extracted-content)

---

"""

category_info = {
    'title_tags': ('📌 Title Tag Formulas', 'Proven title formulas from Jacky Chou'),
    'meta_descriptions': ('📝 Meta Description Templates', 'Meta description best practices'),
    'internal_linking': ('🔗 Internal Linking Strategies', 'Interlinking and anchor text strategies'),
    'content_structure': ('📑 Content Structure & Formatting', 'Headings, outlines, and article structure'),
    'keyword_placement': ('🎯 Keyword Placement', 'Where and how to place keywords'),
    'page_speed': ('⚡ Page Speed & Core Web Vitals', 'Performance optimization tips'),
    'content_optimization': ('✍️ Content Optimization', 'Content quality and optimization'),
    'onpage_seo': ('✅ On-Page SEO Checklists', 'Audits and checklists'),
    'general_seo': ('🔍 General SEO Insights', 'Other SEO strategies and insights')
}

for category, items in content_by_category.items():
    title, desc = category_info.get(category, (category.replace('_', ' ').title(), ''))
    report += f"## {title}\n\n*{desc}*\n\n**{len(items)} items found**\n\n"
    
    for item in items[:100]:  # Limit per category
        # Clean up the text
        item = item.strip()
        if len(item) > 500:
            item = item[:500] + "..."
        report += f"- {item}\n"
    
    report += "\n---\n\n"

# Add all content section
report += "## 📚 All Extracted Content\n\n"
report += f"*Complete dump of all {len(all_content)} content blocks*\n\n"

for item in all_content:
    text = item['text']
    if len(text) > 300:
        text = text[:300] + "..."
    block_type = item['type']
    
    if block_type == 'header':
        report += f"\n### {text}\n"
    elif block_type == 'sub_header':
        report += f"\n#### {text}\n"
    elif block_type == 'sub_sub_header':
        report += f"\n##### {text}\n"
    elif block_type in ['bulleted_list', 'numbered_list']:
        report += f"- {text}\n"
    elif block_type == 'quote':
        report += f"> {text}\n\n"
    elif block_type == 'callout':
        report += f"💡 **{text}**\n\n"
    elif block_type == 'page':
        report += f"\n📄 **{text}**\n\n"
    elif block_type == 'toggle':
        report += f"\n▸ {text}\n"
    else:
        if text:
            report += f"{text}\n\n"

# Save report
output_path = f"{output_dir}/onpage-seo-sops.md"
with open(output_path, 'w') as f:
    f.write(report)

print(f"Report saved to: {output_path}")
print(f"Report size: {len(report):,} characters")

# Also save JSON
json_path = f"{output_dir}/seo-content.json"
with open(json_path, 'w') as f:
    json.dump({
        'categories': dict(content_by_category),
        'all_content': all_content[:1000],
        'stats': {
            'total_blocks': len(all_blocks),
            'seo_items': sum(len(v) for v in content_by_category.values())
        }
    }, f, indent=2)
print(f"JSON saved to: {json_path}")

# Print summary
print("\n📊 Summary by Category:")
for cat, items in sorted(content_by_category.items(), key=lambda x: -len(x[1])):
    print(f"  {cat}: {len(items)} items")
PYTHON

echo ""
echo "Done!"
