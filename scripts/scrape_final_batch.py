#!/usr/bin/env python3
"""
Final batch to reach 20/20 - using creators known to have transcripts
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

# Ben Heath (reliable transcripts) + other verified
FINAL_BATCH = [
    # Meta Ads - Ben Heath and others with transcripts
    {"id": "ufwk5iZfYKQ", "title": "Best Facebook Ads Tutorial For Beginners 2025 - Ben Heath", "category": "meta-ads"},
    {"id": "Q_96rFPCdPA", "title": "Facebook Ads Mistakes to Avoid in 2025 - Ben Heath", "category": "meta-ads"},
    {"id": "GdB1UOGD9_Q", "title": "How I Structure Facebook Ad Campaigns - Ben Heath", "category": "meta-ads"},
    {"id": "eN5OuL_Fxjg", "title": "Facebook Ads Budget Strategy 2025", "category": "meta-ads"},
    
    # Sales - verified creators with transcripts
    {"id": "BxGMYxDO0D0", "title": "Sales Training COMPLETE Course - Everything to Know", "category": "sales"},
    {"id": "E3pRPAYU-j0", "title": "How to Sell Anything to Anyone - Sales Mastery", "category": "sales"},
    {"id": "qgVg4hv10YM", "title": "Sales Techniques That Close More Deals", "category": "sales"},
    {"id": "hZDDxzQfmjk", "title": "The Art of Closing Sales - Full Training", "category": "sales"},
    {"id": "cKD0AXGV4Gc", "title": "B2B Sales Strategy That Works", "category": "sales"},
    {"id": "Mv_-Mx6n6mU", "title": "Cold Email That Gets Responses - Sales Outreach", "category": "sales"},
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
                return {"success": False, "error": "No transcript", "skip": True}
            if attempt < max_retries - 1:
                print(f"    Retry {attempt + 1}/{max_retries}", flush=True)
                time.sleep(2)
            else:
                return {"success": False, "error": error_msg[:100]}

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
    
    print(f"Current: {len(existing_meta)} meta-ads, {len(existing_sales)} sales", flush=True)
    
    new_videos = [v for v in FINAL_BATCH if v['id'] not in existing_meta and v['id'] not in existing_sales]
    
    for i, video in enumerate(new_videos, 1):
        current_meta = len([f for f in os.listdir(meta_dir) if f.endswith('.txt')])
        current_sales = len([f for f in os.listdir(sales_dir) if f.endswith('.txt')])
        
        if current_meta >= 20 and current_sales >= 20:
            print("Target reached!", flush=True)
            break
            
        print(f"[{i}/{len(new_videos)}] {video['title'][:55]}...", flush=True)
        
        result = fetch_with_proxy(video['id'], video['title'])
        
        if result['success']:
            output_dir = meta_dir if video['category'] == 'meta-ads' else sales_dir
            save_transcript(video, result['text'], output_dir)
            print(f"  ✓ Saved ({result['chars']:,} chars)", flush=True)
        elif result.get('skip'):
            print(f"  ⊘ No transcript", flush=True)
        else:
            print(f"  ✗ {result['error'][:50]}", flush=True)
        
        time.sleep(0.5)
    
    final_meta = len([f for f in os.listdir(meta_dir) if f.endswith('.txt')])
    final_sales = len([f for f in os.listdir(sales_dir) if f.endswith('.txt')])
    
    print(f"\n{'='*60}", flush=True)
    print(f"FINAL: Meta Ads {final_meta}/20, Sales {final_sales}/20", flush=True)

if __name__ == "__main__":
    main()
