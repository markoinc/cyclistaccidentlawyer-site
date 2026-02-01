#!/usr/bin/env python3
"""
Fill gaps to reach 20/20 Meta Ads and Sales transcripts
"""

import os
import json
import random
import time
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

sys.stdout.reconfigure(line_buffering=True)

PROXY_USER = "dtwmetwu"
PROXY_PASS = "ww846x37mmd9"

# Additional videos to fill gaps
ADDITIONAL_VIDEOS = [
    # Meta Ads (need 2 more)
    {"id": "le19PPUNaYk", "title": "How To Scale Facebook Ads In 2026 - Nick Theriot", "category": "meta-ads"},
    {"id": "5vB86woZHow", "title": "Facebook Ads Have Changed in 2026 - NEW Strategy", "category": "meta-ads"},
    {"id": "pXp3gCRFR1k", "title": "Meta Ads Testing Strategy 2026", "category": "meta-ads"},
    {"id": "N3QgWVEuDiQ", "title": "Facebook Ads Full Tutorial 2026 Complete", "category": "meta-ads"},
    
    # Sales (need 6 more) - Discovery calls and sales trainers
    {"id": "n4RkGGMLLQw", "title": "How To Sell AI Automations - Discovery Calls 2026", "category": "sales"},
    {"id": "TbUHOj3pcIA", "title": "How to Run a Discovery Call in Tech Sales", "category": "sales"},
    {"id": "JeqtQZbJGtA", "title": "Perfect Your Sales Discovery Calls in 2025", "category": "sales"},
    {"id": "ZvPU47K_1aA", "title": "How to Handle ANY Sales Objection - Patrick Dang", "category": "sales"},
    {"id": "0eGMgI7h_Oo", "title": "Cold Calling Tips That Actually Work 2025", "category": "sales"},
    {"id": "Qh7pJvPVEWI", "title": "Sales Discovery Questions That Close Deals", "category": "sales"},
    {"id": "5Gkn7kFj0hY", "title": "B2B Sales Process Complete Breakdown", "category": "sales"},
    {"id": "4lqvl_hhZz4", "title": "How to Sell on Sales Calls - Full Training", "category": "sales"},
    {"id": "G_RjLcCpSN0", "title": "Sales Pitch Framework That Wins", "category": "sales"},
    {"id": "lJnBJh4Jm0U", "title": "Closing High Ticket Deals Masterclass", "category": "sales"},
]

def fetch_with_proxy(video_id, title, max_retries=3):
    for attempt in range(max_retries):
        try:
            proxy_num = random.randint(1, 215000)
            proxy_config = WebshareProxyConfig(
                proxy_username=f"{PROXY_USER}-{proxy_num}",
                proxy_password=PROXY_PASS,
            )
            
            ytt = YouTubeTranscriptApi(proxy_config=proxy_config)
            transcript = ytt.fetch(video_id)
            text = "\n".join([item.text for item in transcript])
            return {"success": True, "text": text, "chars": len(text)}
            
        except Exception as e:
            error_msg = str(e)
            if "Subtitles are disabled" in error_msg or "No transcripts" in error_msg or "Could not retrieve" in error_msg:
                return {"success": False, "error": "No transcript available", "skip": True}
            if attempt < max_retries - 1:
                print(f"    Retry {attempt + 1}/{max_retries}", flush=True)
                time.sleep(2)
            else:
                return {"success": False, "error": error_msg[:200]}

def save_transcript(video, text, output_dir):
    filename = f"{output_dir}/{video['id']}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {video['title']}\n")
        f.write(f"# Video: https://www.youtube.com/watch?v={video['id']}\n")
        f.write(f"# Category: {video['category']}\n\n")
        f.write(text)
    return filename

def main():
    meta_dir = "/home/ec2-user/clawd/data/transcripts/meta-ads"
    sales_dir = "/home/ec2-user/clawd/data/transcripts/sales"
    
    existing_meta = set(f.replace('.txt', '') for f in os.listdir(meta_dir) if f.endswith('.txt'))
    existing_sales = set(f.replace('.txt', '') for f in os.listdir(sales_dir) if f.endswith('.txt'))
    
    needed_meta = 20 - len(existing_meta)
    needed_sales = 20 - len(existing_sales)
    
    print(f"Current: {len(existing_meta)} meta-ads, {len(existing_sales)} sales", flush=True)
    print(f"Need: {needed_meta} more meta-ads, {needed_sales} more sales\n", flush=True)
    
    # Filter to only new videos
    new_videos = [v for v in ADDITIONAL_VIDEOS if v['id'] not in existing_meta and v['id'] not in existing_sales]
    
    if not new_videos:
        print("No new videos to fetch!", flush=True)
        return
    
    meta_added = 0
    sales_added = 0
    
    for i, video in enumerate(new_videos, 1):
        # Check if we've hit targets
        current_meta = len(existing_meta) + meta_added
        current_sales = len(existing_sales) + sales_added
        
        if video['category'] == 'meta-ads' and current_meta >= 20:
            continue
        if video['category'] == 'sales' and current_sales >= 20:
            continue
            
        print(f"[{i}/{len(new_videos)}] {video['title'][:55]}...", flush=True)
        
        result = fetch_with_proxy(video['id'], video['title'])
        
        if result['success']:
            output_dir = meta_dir if video['category'] == 'meta-ads' else sales_dir
            save_transcript(video, result['text'], output_dir)
            print(f"  ✓ Saved ({result['chars']:,} chars)", flush=True)
            
            if video['category'] == 'meta-ads':
                meta_added += 1
            else:
                sales_added += 1
        elif result.get('skip'):
            print(f"  ⊘ No transcript available", flush=True)
        else:
            print(f"  ✗ {result['error'][:60]}", flush=True)
        
        time.sleep(0.5)
    
    final_meta = len([f for f in os.listdir(meta_dir) if f.endswith('.txt')])
    final_sales = len([f for f in os.listdir(sales_dir) if f.endswith('.txt')])
    
    print(f"\n{'='*60}", flush=True)
    print(f"Final totals:", flush=True)
    print(f"  Meta Ads: {final_meta}/20", flush=True)
    print(f"  Sales: {final_sales}/20", flush=True)

if __name__ == "__main__":
    main()
