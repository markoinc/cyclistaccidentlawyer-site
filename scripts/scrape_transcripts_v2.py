#!/usr/bin/env python3
"""
Scrape YouTube transcripts using WebShare residential proxies.
V2 - Using verified video IDs from search results
"""

import os
import json
import random
import time
import sys
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# Proxy config
PROXY_USER = "dtwmetwu"
PROXY_PASS = "ww846x37mmd9"

# VERIFIED Meta Ads Videos (from search + already scraped)
META_ADS_VIDEOS = [
    # Already scraped successfully
    {"id": "KKp3rA0QK9A", "title": "How to Write Winning Meta Ad Scripts ($450M Spent)", "category": "meta-ads"},
    {"id": "Tj2oufaLQjg", "title": "The Creative Process I Use To Make Winning Meta Ads", "category": "meta-ads"},
    {"id": "MLCNXcF_brM", "title": "How to Create AI UGC Ads That Get 3.8x ROAS", "category": "meta-ads"},
    {"id": "ZQiAxA3JpJc", "title": "The New Way To Use Lookalike Audience On Meta Ads 2026", "category": "meta-ads"},
    {"id": "cs23-HQp12s", "title": "BEST Strategy to Scale Facebook Ads in 2026", "category": "meta-ads"},
    {"id": "4jCF6Fug9To", "title": "Copy This NEW Meta Ads Strategy (Post-Andromeda)", "category": "meta-ads"},
    {"id": "E_wZJhuSK5U", "title": "NEW BEST Facebook Ads Campaign Structure 2026", "category": "meta-ads"},
    # New verified videos from search
    {"id": "R1SXcw9leZs", "title": "Complete Facebook Ads Course for 2026 (Step-By-Step)", "category": "meta-ads"},
    {"id": "rXv2hBcIm4U", "title": "The NEW Way to Advertise on Facebook in 2026", "category": "meta-ads"},
    {"id": "kuSq-pmNfnM", "title": "The Complete Playbook To Running Meta Ads in 2026", "category": "meta-ads"},
    {"id": "mZWJCjhZanQ", "title": "The Only Facebook Ads Tutorial You Need for 2025", "category": "meta-ads"},
    {"id": "TtJbgsG8yB0", "title": "Ultimate Facebook Ads Guide for 2025 Beginner Walkthrough", "category": "meta-ads"},
]

SALES_VIDEOS = [
    # Verified from search
    {"id": "_KBGwvb3fYU", "title": "How to Become a High Ticket Closer in 2025 (Full Guide)", "category": "sales"},
    {"id": "wOIZv2Eef3Q", "title": "FREE High Ticket Sales Training For 2026 | From a $10M Closer", "category": "sales"},
    {"id": "4HutGHR7H1k", "title": "Ultimate Guide to High Ticket Sales (7+hour Course)", "category": "sales"},
    {"id": "Gsb1BaXx4Zk", "title": "Full Guide to High Ticket Closing for Beginners", "category": "sales"},
    {"id": "165NwKPSueQ", "title": "HIGH-TICKET REMOTE CLOSING: How to GET STARTED", "category": "sales"},
]

def fetch_with_proxy(video_id, title, max_retries=3):
    """Fetch transcript using WebShare proxy."""
    for attempt in range(max_retries):
        try:
            proxy_num = random.randint(1, 215000)
            proxy_config = WebshareProxyConfig(
                proxy_username=f"{PROXY_USER}-{proxy_num}",
                proxy_password=PROXY_PASS,
            )
            
            ytt = YouTubeTranscriptApi(proxy_config=proxy_config)
            transcript = ytt.fetch(video_id)
            
            # Join all text segments
            text = "\n".join([item.text for item in transcript])
            return {"success": True, "text": text, "chars": len(text)}
            
        except Exception as e:
            error_msg = str(e)
            if "Subtitles are disabled" in error_msg or "No transcripts" in error_msg:
                # Don't retry if no transcripts available
                return {"success": False, "error": "No transcript available"}
            if attempt < max_retries - 1:
                print(f"    Retry {attempt + 1}/{max_retries}", flush=True)
                time.sleep(2)
            else:
                return {"success": False, "error": error_msg[:200]}

def save_transcript(video, text, output_dir):
    """Save transcript to file."""
    filename = f"{output_dir}/{video['id']}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {video['title']}\n")
        f.write(f"# Video: https://www.youtube.com/watch?v={video['id']}\n")
        f.write(f"# Category: {video['category']}\n\n")
        f.write(text)
    return filename

def main():
    # Output directories
    meta_dir = "/home/ec2-user/clawd/data/transcripts/meta-ads"
    sales_dir = "/home/ec2-user/clawd/data/transcripts/sales"
    os.makedirs(meta_dir, exist_ok=True)
    os.makedirs(sales_dir, exist_ok=True)
    
    # Skip already-scraped videos
    existing_meta = set(f.replace('.txt', '') for f in os.listdir(meta_dir) if f.endswith('.txt'))
    existing_sales = set(f.replace('.txt', '') for f in os.listdir(sales_dir) if f.endswith('.txt'))
    
    # Filter to only new videos
    new_meta = [v for v in META_ADS_VIDEOS if v['id'] not in existing_meta]
    new_sales = [v for v in SALES_VIDEOS if v['id'] not in existing_sales]
    all_videos = new_meta + new_sales
    
    print(f"Already have: {len(existing_meta)} meta-ads, {len(existing_sales)} sales", flush=True)
    print(f"Fetching {len(all_videos)} new transcripts...\n", flush=True)
    
    results = {"success": [], "failed": []}
    
    for i, video in enumerate(all_videos, 1):
        print(f"[{i}/{len(all_videos)}] {video['title'][:55]}...", flush=True)
        
        result = fetch_with_proxy(video['id'], video['title'])
        
        if result['success']:
            output_dir = meta_dir if video['category'] == 'meta-ads' else sales_dir
            save_transcript(video, result['text'], output_dir)
            print(f"  ✓ Saved ({result['chars']:,} chars)", flush=True)
            results['success'].append({
                "title": video['title'],
                "id": video['id'],
                "category": video['category'],
                "chars": result['chars']
            })
        else:
            print(f"  ✗ {result['error'][:60]}", flush=True)
            results['failed'].append({
                "title": video['title'],
                "id": video['id'],
                "error": result['error']
            })
        
        time.sleep(0.5)
    
    # Count totals
    final_meta = len([f for f in os.listdir(meta_dir) if f.endswith('.txt')])
    final_sales = len([f for f in os.listdir(sales_dir) if f.endswith('.txt')])
    
    # Save summary
    summary = {
        "total_meta_ads": final_meta,
        "total_sales": final_sales,
        "new_success": len(results['success']),
        "new_failed": len(results['failed']),
        "results": results
    }
    
    summary_file = "/home/ec2-user/clawd/data/transcripts/summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}", flush=True)
    print(f"Done! Total transcripts:", flush=True)
    print(f"  Meta Ads: {final_meta}", flush=True)
    print(f"  Sales: {final_sales}", flush=True)
    print(f"\nNew this run: {len(results['success'])} success, {len(results['failed'])} failed", flush=True)

if __name__ == "__main__":
    main()
