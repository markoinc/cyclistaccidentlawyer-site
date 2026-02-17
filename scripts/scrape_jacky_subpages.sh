#!/bin/bash
# Scrape specific Jacky Chou subpages with SEO content

OUTPUT_DIR="/home/ec2-user/clawd/data/jacky-brain/subpages"
mkdir -p "$OUTPUT_DIR"

# Key SEO-related pages
PAGES=(
    "2efe1e50-bed2-80e9-ba25-e1269f615779|Complete_AI_SEO_GEO_Course"
    "220e1e50-bed2-8026-b5ac-e5bdf1dcacd3|65_Point_Local_SEO_Checklist"
    "235e1e50-bed2-8014-81c1-c6d92f64cfd2|Complete_Local_SEO_Course"
    "234e1e50-bed2-8040-80a5-f8a8fcda0b8e|Complete_Rank_and_Rent_Course"
    "214e1e50-bed2-8047-be32-f80e2159df1d|Local_SEO_Audit_Mistakes"
    "1e3e1e50-bed2-802b-bb06-da86e24e222e|OnSite_SEO_Checklist_Local"
    "1d8e1e50-bed2-80fb-876b-dc4811a30db1|65_Point_Checklist_2025"
    "1d0e1e50-bed2-80a8-9efe-e477970e0328|Easy_Local_SEO_WINS"
    "14ae1e50-bed2-80d9-8d4b-ff88c1279bd9|OnPage_SEO_7Point_Checklist"
    "2dfe1e50-bed2-8023-b63a-c0793e1af1ba|Topical_Authority_2026"
    "2e8e1e50-bed2-8090-b9a6-d58f3e861b0e|5_Minute_SEO_Hack"
)

fetch_page() {
    local page_id=$1
    local output=$2
    local proxy_num=$((RANDOM % 10000 + 1))
    local proxy="http://dtwmetwu-${proxy_num}:ww846x37mmd9@p.webshare.io:80"
    
    curl -s --proxy "$proxy" \
        -H 'Content-Type: application/json' \
        -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36' \
        -H 'Accept: application/json' \
        -H 'Accept-Language: en-US,en;q=0.9' \
        -H 'Origin: https://indexsy.notion.site' \
        'https://indexsy.notion.site/api/v3/loadPageChunk' \
        -d "{
            \"pageId\": \"$page_id\",
            \"limit\": 500,
            \"cursor\": {\"stack\":[]},
            \"chunkNumber\": 0,
            \"verticalColumns\": false
        }" > "$output"
}

echo "=== Fetching SEO Subpages ==="
echo ""

for page_info in "${PAGES[@]}"; do
    IFS='|' read -r page_id name <<< "$page_info"
    output="$OUTPUT_DIR/${name}.json"
    
    echo "Fetching: $name"
    fetch_page "$page_id" "$output"
    
    if jq -e . "$output" > /dev/null 2>&1; then
        block_count=$(jq '.recordMap.block | length' "$output" 2>/dev/null || echo "0")
        echo "  Got $block_count blocks"
    else
        echo "  ERROR: Invalid response"
        rm -f "$output"
    fi
    
    sleep 2
done

echo ""
echo "Processing subpages..."

# Process all subpages and extract content
python3 << 'PYTHON'
import json
import glob
import os
from collections import defaultdict
import time

output_dir = "/home/ec2-user/clawd/data/jacky-brain/subpages"
subpage_files = glob.glob(f"{output_dir}/*.json")

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

all_seo_content = []
page_contents = {}

for subpage_file in subpage_files:
    page_name = os.path.basename(subpage_file).replace('.json', '')
    
    try:
        with open(subpage_file) as f:
            data = json.load(f)
        
        blocks = data.get('recordMap', {}).get('block', {})
        
        page_content = []
        for block_id, block in blocks.items():
            block_type, text = extract_text(block)
            if text:
                page_content.append({
                    'type': block_type,
                    'text': text
                })
                all_seo_content.append({
                    'page': page_name,
                    'type': block_type,
                    'text': text
                })
        
        page_contents[page_name] = page_content
        print(f"  {page_name}: {len(page_content)} content blocks")
        
    except Exception as e:
        print(f"  Error processing {page_name}: {e}")

print(f"\nTotal content items: {len(all_seo_content)}")

# Generate detailed report
report = f"""# Jacky Chou - Detailed On-Page SEO SOPs

**Source:** Build in Public Notion - Subpages
**Scraped:** {time.strftime('%Y-%m-%d %H:%M:%S UTC')}
**Total Content Items:** {len(all_seo_content)}
**Pages Processed:** {len(page_contents)}

---

"""

# Add each page's content
for page_name, content_list in page_contents.items():
    title = page_name.replace('_', ' ')
    report += f"## 📄 {title}\n\n"
    report += f"*{len(content_list)} items*\n\n"
    
    for item in content_list:
        text = item['text']
        block_type = item['type']
        
        if block_type == 'header':
            report += f"\n### {text}\n\n"
        elif block_type == 'sub_header':
            report += f"\n#### {text}\n\n"
        elif block_type == 'sub_sub_header':
            report += f"\n##### {text}\n\n"
        elif block_type in ['bulleted_list']:
            report += f"- {text}\n"
        elif block_type in ['numbered_list']:
            report += f"1. {text}\n"
        elif block_type == 'to_do':
            report += f"- [ ] {text}\n"
        elif block_type == 'quote':
            report += f"> {text}\n\n"
        elif block_type == 'callout':
            report += f"💡 **{text}**\n\n"
        elif block_type == 'toggle':
            report += f"\n<details><summary>{text}</summary></details>\n\n"
        elif block_type == 'code':
            report += f"```\n{text}\n```\n\n"
        elif block_type == 'divider':
            report += "\n---\n\n"
        elif block_type == 'page':
            report += f"\n📄 **{text}**\n\n"
        else:
            if text.strip():
                report += f"{text}\n\n"
    
    report += "\n---\n\n"

# Save detailed report
output_path = "/home/ec2-user/clawd/data/jacky-brain/onpage-seo-detailed.md"
with open(output_path, 'w') as f:
    f.write(report)

print(f"\nDetailed report saved to: {output_path}")
print(f"Report size: {len(report):,} characters")

# Save JSON
json_path = "/home/ec2-user/clawd/data/jacky-brain/subpages-content.json"
with open(json_path, 'w') as f:
    json.dump({
        'pages': page_contents,
        'all_content': all_seo_content
    }, f, indent=2)
print(f"JSON saved to: {json_path}")
PYTHON

echo ""
echo "Done!"
