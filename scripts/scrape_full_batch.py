#!/usr/bin/env python3
"""
Scrape 20 Meta Ads + 20 Sales YouTube transcripts
Meta: within 3 months | Sales: within 6 months
Using WebShare residential proxies
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

# 20 META ADS VIDEOS (within 3 months - Nov 2025 to Feb 2026)
META_ADS_VIDEOS = [
    # Already scraped (keeping for reference)
    {"id": "KKp3rA0QK9A", "title": "How to Write Winning Meta Ad Scripts ($450M Spent)", "category": "meta-ads"},
    {"id": "Tj2oufaLQjg", "title": "The Creative Process I Use To Make Winning Meta Ads", "category": "meta-ads"},
    {"id": "MLCNXcF_brM", "title": "How to Create AI UGC Ads That Get 3.8x ROAS", "category": "meta-ads"},
    {"id": "ZQiAxA3JpJc", "title": "The New Way To Use Lookalike Audience On Meta Ads 2026", "category": "meta-ads"},
    {"id": "cs23-HQp12s", "title": "BEST Strategy to Scale Facebook Ads in 2026", "category": "meta-ads"},
    {"id": "4jCF6Fug9To", "title": "Copy This NEW Meta Ads Strategy (Post-Andromeda)", "category": "meta-ads"},
    {"id": "E_wZJhuSK5U", "title": "NEW BEST Facebook Ads Campaign Structure 2026", "category": "meta-ads"},
    {"id": "R1SXcw9leZs", "title": "Complete Facebook Ads Course for 2026 (Step-By-Step)", "category": "meta-ads"},
    {"id": "rXv2hBcIm4U", "title": "The NEW Way to Advertise on Facebook in 2026", "category": "meta-ads"},
    {"id": "kuSq-pmNfnM", "title": "The Complete Playbook To Running Meta Ads in 2026", "category": "meta-ads"},
    {"id": "mZWJCjhZanQ", "title": "The Only Facebook Ads Tutorial You Need for 2025", "category": "meta-ads"},
    {"id": "TtJbgsG8yB0", "title": "Ultimate Facebook Ads Guide for 2025 Beginner Walkthrough", "category": "meta-ads"},
    # New from search (Jan/Dec 2025-2026)
    {"id": "2AzazfGUums", "title": "How To Setup Meta Ads In 2026", "category": "meta-ads"},
    {"id": "Gb3_SXgUDhI", "title": "The NEW Way to Run Facebook Ads in 2026 (Sam Piliero)", "category": "meta-ads"},
    {"id": "KKUhIG_Z2Sc", "title": "The BEST Meta Ads Strategy for 2026", "category": "meta-ads"},
    {"id": "dAJyqo6wnq4", "title": "The BEST Facebook Ads Tutorial For Beginners in 2026", "category": "meta-ads"},
    {"id": "L83waCBHBwU", "title": "If I Started Facebook Ads in 2026 Id Do This", "category": "meta-ads"},
    {"id": "0cj09Aa3de8", "title": "Facebook Ads NEW Rules for 2026", "category": "meta-ads"},
    {"id": "HBf_6nB_plU", "title": "How to Run Meta Ads for Clients in 2026", "category": "meta-ads"},
    {"id": "qJnLIUWPW94", "title": "Meta Ads Creative Strategy That Actually Works 2026", "category": "meta-ads"},
]

# 20 SALES VIDEOS (within 6 months - Aug 2025 to Feb 2026)
SALES_VIDEOS = [
    # Already scraped
    {"id": "_KBGwvb3fYU", "title": "How to Become a High Ticket Closer in 2025 (Full Guide)", "category": "sales"},
    {"id": "wOIZv2Eef3Q", "title": "FREE High Ticket Sales Training For 2026 From a 10M Closer", "category": "sales"},
    {"id": "4HutGHR7H1k", "title": "Ultimate Guide to High Ticket Sales (7+ hour Course)", "category": "sales"},
    {"id": "Gsb1BaXx4Zk", "title": "Full Guide to High Ticket Closing for Beginners", "category": "sales"},
    {"id": "165NwKPSueQ", "title": "HIGH-TICKET REMOTE CLOSING How to GET STARTED", "category": "sales"},
    # New from search (recent)
    {"id": "IMuUU0PiW6M", "title": "42 Minutes of Sales Training That Will Explode Your Sales 2026 - Jeremy Miner", "category": "sales"},
    {"id": "9nPrEzGOIrY", "title": "The Ultimate Sales Training for Closers - Andy Elliott", "category": "sales"},
    {"id": "vwRLeB60sGc", "title": "5 Power Moves to Shape Your 2026 Sales Year", "category": "sales"},
    {"id": "XHHSpRLSWCk", "title": "25 minutes of SALES TRAINING that will Explode Your Business 2025", "category": "sales"},
    {"id": "QCYy0GddJWY", "title": "Sales Training 5 Must-Have SKILLS to Close More BUSINESS 2025", "category": "sales"},
    {"id": "tf81pRuGsDo", "title": "How to DESTROY Any Sales Objection", "category": "sales"},
    {"id": "3aR0ed2em74", "title": "Alex Hormozi 7 Sales Closing Tips After Prospect Says No", "category": "sales"},
    {"id": "oZ18-kMrmKw", "title": "Alex Hormozi Lead Generation Strategy for 2025", "category": "sales"},
    {"id": "E3eyQhV3TK8", "title": "The Perfect Setup to Close Anyone - Andy Elliott", "category": "sales"},
    {"id": "UGeXntw2quY", "title": "What Are the Best Closing Techniques in Sales - Matt Easton", "category": "sales"},
    {"id": "TnZFEXH3zGs", "title": "How to Handle I Need to Think About It Objection", "category": "sales"},
    {"id": "Dq_LuFwcLI4", "title": "The Only Sales Video You Need to Watch in 2025", "category": "sales"},
    {"id": "wDvLxFnMEmY", "title": "How I Close 40 Percent of My Sales Calls", "category": "sales"},
    {"id": "z2K8CjJVxJo", "title": "7 Figure Sales Script Breakdown - Cole Gordon Style", "category": "sales"},
    {"id": "KbYhfk4HfmY", "title": "Sales Call Framework That Books High Ticket Clients", "category": "sales"},
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
    os.makedirs(meta_dir, exist_ok=True)
    os.makedirs(sales_dir, exist_ok=True)
    
    existing_meta = set(f.replace('.txt', '') for f in os.listdir(meta_dir) if f.endswith('.txt'))
    existing_sales = set(f.replace('.txt', '') for f in os.listdir(sales_dir) if f.endswith('.txt'))
    
    new_meta = [v for v in META_ADS_VIDEOS if v['id'] not in existing_meta]
    new_sales = [v for v in SALES_VIDEOS if v['id'] not in existing_sales]
    all_videos = new_meta + new_sales
    
    print(f"Already have: {len(existing_meta)} meta-ads, {len(existing_sales)} sales", flush=True)
    print(f"Fetching {len(all_videos)} new transcripts...\n", flush=True)
    
    if len(all_videos) == 0:
        print("All videos already scraped!", flush=True)
        return
    
    results = {"success": [], "failed": [], "no_transcript": []}
    
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
        elif result.get('skip'):
            print(f"  ⊘ No transcript available", flush=True)
            results['no_transcript'].append({"title": video['title'], "id": video['id']})
        else:
            print(f"  ✗ {result['error'][:60]}", flush=True)
            results['failed'].append({"title": video['title'], "id": video['id'], "error": result['error']})
        
        time.sleep(0.5)
    
    final_meta = len([f for f in os.listdir(meta_dir) if f.endswith('.txt')])
    final_sales = len([f for f in os.listdir(sales_dir) if f.endswith('.txt')])
    
    summary = {
        "total_meta_ads": final_meta,
        "total_sales": final_sales,
        "target_meta": 20,
        "target_sales": 20,
        "new_success": len(results['success']),
        "no_transcript": len(results['no_transcript']),
        "failed": len(results['failed']),
        "results": results
    }
    
    with open("/home/ec2-user/clawd/data/transcripts/summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}", flush=True)
    print(f"Done! Total transcripts:", flush=True)
    print(f"  Meta Ads: {final_meta}/20", flush=True)
    print(f"  Sales: {final_sales}/20", flush=True)
    print(f"\nThis run: {len(results['success'])} success, {len(results['no_transcript'])} no transcript, {len(results['failed'])} failed", flush=True)

if __name__ == "__main__":
    main()
