#!/usr/bin/env python3
"""
Scrape YouTube transcripts using WebShare residential proxies.
"""

import os
import json
import random
import time
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig

# Proxy config
PROXY_USER = "dtwmetwu"
PROXY_PASS = "ww846x37mmd9"
PROXY_HOST = "p.webshare.io"
PROXY_PORT = 80

# All videos to transcribe
META_ADS_VIDEOS = [
    # Batch 2 - Creative/Copywriting/Scaling
    {"id": "KKp3rA0QK9A", "title": "How to Write Winning Meta Ad Scripts ($450M Spent)", "category": "meta-ads"},
    {"id": "Tj2oufaLQjg", "title": "The Creative Process I Use To Make Winning Meta Ads", "category": "meta-ads"},
    {"id": "MLCNXcF_brM", "title": "How to Create AI UGC Ads That Get 3.8x ROAS", "category": "meta-ads"},
    {"id": "ZQiAxA3JpJc", "title": "The New Way To Use Lookalike Audience On Meta Ads 2026", "category": "meta-ads"},
    {"id": "cs23-HQp12s", "title": "BEST Strategy to Scale Facebook Ads in 2026", "category": "meta-ads"},
    {"id": "4jCF6Fug9To", "title": "Copy This NEW Meta Ads Strategy (Post-Andromeda)", "category": "meta-ads"},
    {"id": "E_wZJhuSK5U", "title": "NEW BEST Facebook Ads Campaign Structure 2026", "category": "meta-ads"},
    # Add more Meta Ads videos
    {"id": "rJm3YQHl_U4", "title": "How to Run Facebook Ads for Beginners 2025", "category": "meta-ads"},
    {"id": "0J2hI4gNKLs", "title": "Meta Ads Complete Tutorial 2025", "category": "meta-ads"},
    {"id": "7eVdJPwHj1E", "title": "Facebook Ads Strategy for Lead Generation", "category": "meta-ads"},
    {"id": "N_4P8RNNQJQ", "title": "How To Create Converting Facebook Ads Creative", "category": "meta-ads"},
    {"id": "F8jDYjlLCZg", "title": "Meta Ads for Local Business Marketing", "category": "meta-ads"},
    {"id": "WtMv0CYVc_4", "title": "Facebook Ads Targeting 2025 - What Works Now", "category": "meta-ads"},
    {"id": "N3m5fLTvJk0", "title": "How I Spend $1M/Month on Meta Ads Profitably", "category": "meta-ads"},
    {"id": "SFZ1Vw5gNt4", "title": "Meta Ads Creative Testing Framework", "category": "meta-ads"},
    {"id": "o7zGXPQYeqA", "title": "Best Meta Ads CBO vs ABO Strategy 2025", "category": "meta-ads"},
    {"id": "IhPZN9wXQ3o", "title": "Facebook Lead Ads Complete Guide", "category": "meta-ads"},
    {"id": "CG7O8a3RDTY", "title": "Meta Advantage+ Shopping Campaigns Tutorial", "category": "meta-ads"},
    {"id": "C-dS9x7A4cw", "title": "How to Lower CPM on Facebook Ads", "category": "meta-ads"},
    {"id": "SJ7OjJJjV8Q", "title": "Meta Ads Retargeting Strategy That Works", "category": "meta-ads"},
]

SALES_VIDEOS = [
    # Sales/Funnels/High-Ticket Closing
    {"id": "jdQOWrXNa_A", "title": "The Perfect Sales Script for Any Call", "category": "sales"},
    {"id": "llDikI2hTtk", "title": "How to Close High Ticket Clients", "category": "sales"},
    {"id": "1X-rL17mlP4", "title": "Sales Call Framework That Books Meetings", "category": "sales"},
    {"id": "xV7xJXSxQKs", "title": "Cold Calling Scripts That Actually Work 2025", "category": "sales"},
    {"id": "SqLcT00Jjyk", "title": "How to Handle ANY Sales Objection", "category": "sales"},
    {"id": "Q3kLXzJEHkw", "title": "B2B Sales Prospecting - Complete Guide", "category": "sales"},
    {"id": "YPdmCcUqfLQ", "title": "SPIN Selling Explained - How to Use It", "category": "sales"},
    {"id": "F6_qDMSXHQA", "title": "Follow Up Sequences That Close Deals", "category": "sales"},
    {"id": "1EiC9bvVGnk", "title": "Discovery Calls - How to Run Them Properly", "category": "sales"},
    {"id": "Cz3WcZLRaWc", "title": "Building a Sales Funnel That Converts", "category": "sales"},
    {"id": "X9p_8qGZnno", "title": "How to Qualify Leads Faster", "category": "sales"},
    {"id": "LBG8CdvqwjA", "title": "Sales Mindset - Psychology of Closing", "category": "sales"},
    {"id": "XA6oaGtPEhk", "title": "Client Onboarding Process That Retains", "category": "sales"},
    {"id": "Xj0QaJW8iQQ", "title": "Price Anchoring and Negotiation Tactics", "category": "sales"},
    {"id": "3LPY5qQHp-8", "title": "SMS Follow Up That Gets Responses", "category": "sales"},
    {"id": "Eo7H6_V-n14", "title": "Agency Sales - How to Sign 10K+ Clients", "category": "sales"},
    {"id": "WIHVpNZZj1c", "title": "Referral System That Brings Warm Leads", "category": "sales"},
    {"id": "N2zZ_P2e79M", "title": "Case Study Selling - Show Results Close Deals", "category": "sales"},
    {"id": "EYzJq28VYzQ", "title": "Consultative Selling for Agencies", "category": "sales"},
    {"id": "9JLnr5b3p8w", "title": "How to Build Trust on Sales Calls", "category": "sales"},
]

def get_random_proxy():
    """Get a random proxy from the pool."""
    proxy_num = random.randint(1, 215000)
    return f"{PROXY_USER}-{proxy_num}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"

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
            if attempt < max_retries - 1:
                print(f"    Retry {attempt + 1}/{max_retries} (proxy {proxy_num})")
                time.sleep(1)
            else:
                return {"success": False, "error": error_msg}

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
    
    all_videos = META_ADS_VIDEOS + SALES_VIDEOS
    results = {"success": [], "failed": []}
    
    print(f"Fetching {len(all_videos)} video transcripts...")
    print(f"Using WebShare residential proxies\n")
    
    for i, video in enumerate(all_videos, 1):
        print(f"[{i}/{len(all_videos)}] {video['title'][:60]}...")
        
        result = fetch_with_proxy(video['id'], video['title'])
        
        if result['success']:
            output_dir = meta_dir if video['category'] == 'meta-ads' else sales_dir
            filename = save_transcript(video, result['text'], output_dir)
            print(f"  ✓ Saved ({result['chars']:,} chars)")
            results['success'].append({
                "title": video['title'],
                "id": video['id'],
                "category": video['category'],
                "chars": result['chars']
            })
        else:
            print(f"  ✗ Failed: {result['error'][:80]}")
            results['failed'].append({
                "title": video['title'],
                "id": video['id'],
                "category": video['category'],
                "error": result['error'][:200]
            })
        
        # Small delay between requests
        time.sleep(0.5)
    
    # Save summary
    summary_file = "/home/ec2-user/clawd/data/transcripts/summary.json"
    with open(summary_file, 'w') as f:
        json.dump({
            "total": len(all_videos),
            "successful": len(results['success']),
            "failed": len(results['failed']),
            "meta_ads_count": len([v for v in results['success'] if v['category'] == 'meta-ads']),
            "sales_count": len([v for v in results['success'] if v['category'] == 'sales']),
            "results": results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Done! {len(results['success'])}/{len(all_videos)} transcripts saved")
    print(f"  Meta Ads: {len([v for v in results['success'] if v['category'] == 'meta-ads'])}")
    print(f"  Sales: {len([v for v in results['success'] if v['category'] == 'sales'])}")
    print(f"\nSummary saved to: {summary_file}")

if __name__ == "__main__":
    main()
