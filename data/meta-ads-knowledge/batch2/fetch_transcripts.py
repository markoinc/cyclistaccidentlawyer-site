#!/usr/bin/env python3
"""Fetch YouTube transcripts for Meta Ads course videos - Batch 2"""

import json
from youtube_transcript_api import YouTubeTranscriptApi

# Selected videos for batch 2
VIDEOS = [
    {
        "id": "KKp3rA0QK9A",
        "title": "How to Write Winning Meta Ad Scripts ($450M Spent)",
        "creator": "Fraggell (Fraser Cottrell)",
        "topic": "Ad Creative / Copywriting",
        "url": "https://www.youtube.com/watch?v=KKp3rA0QK9A"
    },
    {
        "id": "Tj2oufaLQjg",
        "title": "The Creative Process I Use To Make Winning Meta Ads Over And Over Again",
        "creator": "Andrew Faris",
        "topic": "Creative Process",
        "url": "https://www.youtube.com/watch?v=Tj2oufaLQjg"
    },
    {
        "id": "MLCNXcF_brM",
        "title": "How to Create AI UGC Ads That Get 3.8x ROAS (Full Tutorial)",
        "creator": "Unknown",
        "topic": "UGC / Video Ads",
        "url": "https://www.youtube.com/watch?v=MLCNXcF_brM"
    },
    {
        "id": "ZQiAxA3JpJc",
        "title": "The New Way To Use Lookalike Audience On Meta Ads in 2026",
        "creator": "Nestuge",
        "topic": "Lookalike Audiences",
        "url": "https://www.youtube.com/watch?v=ZQiAxA3JpJc"
    },
    {
        "id": "cs23-HQp12s",
        "title": "I Found the BEST Strategy to Scale Facebook Ads in 2026",
        "creator": "Skale It Agency",
        "topic": "Scaling Strategy",
        "url": "https://www.youtube.com/watch?v=cs23-HQp12s"
    },
    {
        "id": "4jCF6Fug9To",
        "title": "Copy This NEW Meta Ads Strategy, It'll Blow Up Your Business (Post-Andromeda)",
        "creator": "Charley T (Disrupter School)",
        "topic": "Post-Andromeda Strategy",
        "url": "https://www.youtube.com/watch?v=4jCF6Fug9To"
    },
    {
        "id": "E_wZJhuSK5U",
        "title": "The NEW BEST Facebook Ads Campaign Structure for 2026",
        "creator": "Charley T (Disrupter School)",
        "topic": "Campaign Structure",
        "url": "https://www.youtube.com/watch?v=E_wZJhuSK5U"
    }
]

def format_transcript(transcript_data):
    """Format transcript data into readable text"""
    return " ".join([entry.text for entry in transcript_data])

def fetch_and_save(api, video):
    """Fetch transcript and save to file"""
    video_id = video["id"]
    filename = f"{video_id}_{video['topic'].replace('/', '-').replace(' ', '_')}.txt"
    
    try:
        # Fetch transcript using new API (instantiated object)
        transcript_data = api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
        text = format_transcript(transcript_data)
        
        # Save transcript
        with open(filename, 'w') as f:
            f.write(f"Title: {video['title']}\n")
            f.write(f"Creator: {video['creator']}\n")
            f.write(f"Topic: {video['topic']}\n")
            f.write(f"URL: {video['url']}\n")
            f.write(f"Video ID: {video_id}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        
        print(f"✓ Saved: {filename} ({len(text)} chars)")
        return True
        
    except Exception as e:
        print(f"✗ Error for {video['title']}: {str(e)}")
        return False

if __name__ == "__main__":
    import os
    os.chdir('/home/ec2-user/clawd/data/meta-ads-knowledge/batch2')
    
    # Initialize API client
    api = YouTubeTranscriptApi()
    
    success = 0
    failed = 0
    
    for video in VIDEOS:
        if fetch_and_save(api, video):
            success += 1
        else:
            failed += 1
    
    print(f"\nCompleted: {success} success, {failed} failed")
