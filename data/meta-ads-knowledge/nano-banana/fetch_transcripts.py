#!/usr/bin/env python3
"""Fetch YouTube transcripts for Nano Banana Pro videos"""

from youtube_transcript_api import YouTubeTranscriptApi
import json
import os

# Videos about Nano Banana Pro + Meta Ads
VIDEOS = [
    {"id": "gtvTGN6kKPk", "title": "Nano Banana Pro Just Changed Facebook Ads Forever! (Review & Tutorial)", "channel": "Sam Piliero"},
    {"id": "HtU2mwNu4gw", "title": "How to Make 10x More Facebook Ads Using Nano Banana AI (Full Tutorial)", "channel": "Davie Fogarty"},
    {"id": "Z-sotFK_4kU", "title": "The Nano Banana + n8n System for Unlimited FB Ads (Copy This Workflow)", "channel": "AI Foundations"},
    {"id": "Bw2AlObv7dg", "title": "How to use Nano Banana Pro for AI Advertising (Full Workflow)", "channel": "Roboverse AI"},
    {"id": "CldGNJhBaNw", "title": "Nano Banana Pro Cinematic AI Ads! (Full Tutorial)", "channel": "Make AI Ads"},
    {"id": "P7pH_1zFKbE", "title": "Create Cinematic AI Ads With Nano Banana Pro + Kling AI - Full Guide", "channel": "Dan Kieft"},
    {"id": "-rRFb2mx2cI", "title": "How to Create VIRAL Social Media Ads with AI - New Nano Banana Pro", "channel": "Unknown"},
    {"id": "-ER91HHWy-Q", "title": "Cinematic AI Ads with Nano Banana Pro (Full Tutorial)", "channel": "Applied AI"},
    {"id": "vldtt351qU8", "title": "Nano Banana Pro Just Changed Facebook Ads Forever (and nobody even realized)", "channel": "Davie Fogarty"},
    {"id": "YbztbmMtDZM", "title": "Create AI UGC Ads With Nano Banana That ACTUALLY Look REAL", "channel": "Dan Kieft"},
    {"id": "letYpIfiweA", "title": "Design Meta Ads with Nano Banana | AI Image Generation", "channel": "Unknown"},
    {"id": "TZcn8nOJHH4", "title": "How I Generate Unlimited Ad Creative with Nano Banana + n8n", "channel": "The Recap"},
]

OUTPUT_DIR = "/home/ec2-user/clawd/data/meta-ads-knowledge/nano-banana"

def fetch_transcript(ytt_api, video_id, title, channel):
    """Fetch transcript for a single video"""
    try:
        # Fetch transcript directly with English preference
        transcript_data = ytt_api.fetch(video_id, languages=['en', 'en-US', 'en-GB'])
        
        # Convert to list format
        transcript_list = list(transcript_data)
        
        # Combine into full text
        full_text = " ".join([entry['text'] for entry in transcript_list])
        
        # Calculate duration from last entry
        if transcript_list:
            last_entry = transcript_list[-1]
            duration_seconds = last_entry['start'] + last_entry.get('duration', 0)
            duration_min = int(duration_seconds // 60)
            duration_sec = int(duration_seconds % 60)
            duration_str = f"{duration_min}:{duration_sec:02d}"
        else:
            duration_str = "Unknown"
        
        return {
            "success": True,
            "video_id": video_id,
            "title": title,
            "channel": channel,
            "duration": duration_str,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "transcript": full_text,
            "transcript_segments": transcript_list
        }
    except Exception as e:
        return {"success": False, "video_id": video_id, "title": title, "error": str(e)}

def main():
    # Initialize API once
    ytt_api = YouTubeTranscriptApi()
    
    results = []
    successful = 0
    
    for video in VIDEOS:
        print(f"Fetching: {video['title'][:60]}...")
        result = fetch_transcript(ytt_api, video['id'], video['title'], video['channel'])
        results.append(result)
        
        if result['success']:
            successful += 1
            # Save individual transcript
            safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in video['title'])[:50]
            filename = f"{video['id']}_{safe_title}.md"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'w') as f:
                f.write(f"# {result['title']}\n\n")
                f.write(f"**URL:** {result['url']}\n")
                f.write(f"**Channel:** {result['channel']}\n")
                f.write(f"**Duration:** {result['duration']}\n\n")
                f.write("## Transcript\n\n")
                f.write(result['transcript'])
            
            print(f"  ✓ Saved: {filename}")
        else:
            print(f"  ✗ Error: {result.get('error', 'Unknown')}")
    
    # Save summary
    summary = {
        "total_videos": len(VIDEOS),
        "successful": successful,
        "failed": len(VIDEOS) - successful,
        "videos": [
            {
                "id": r['video_id'],
                "title": r.get('title'),
                "channel": r.get('channel'),
                "url": f"https://www.youtube.com/watch?v={r['video_id']}",
                "duration": r.get('duration'),
                "success": r['success'],
                "error": r.get('error')
            }
            for r in results
        ]
    }
    
    with open(os.path.join(OUTPUT_DIR, "summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nComplete: {successful}/{len(VIDEOS)} transcripts fetched")
    return results

if __name__ == "__main__":
    main()
