#!/usr/bin/env python3
"""
Run this on your Windows machine to fetch YouTube transcripts.
Requires: pip install youtube-transcript-api
"""

from youtube_transcript_api import YouTubeTranscriptApi
import json
import os

# All videos to transcribe
VIDEOS = [
    # Batch 2 - Creative/Copywriting/Scaling
    {"id": "KKp3rA0QK9A", "title": "How to Write Winning Meta Ad Scripts ($450M Spent)", "batch": "batch2"},
    {"id": "Tj2oufaLQjg", "title": "The Creative Process I Use To Make Winning Meta Ads", "batch": "batch2"},
    {"id": "MLCNXcF_brM", "title": "How to Create AI UGC Ads That Get 3.8x ROAS", "batch": "batch2"},
    {"id": "ZQiAxA3JpJc", "title": "The New Way To Use Lookalike Audience On Meta Ads 2026", "batch": "batch2"},
    {"id": "cs23-HQp12s", "title": "BEST Strategy to Scale Facebook Ads in 2026", "batch": "batch2"},
    {"id": "4jCF6Fug9To", "title": "Copy This NEW Meta Ads Strategy (Post-Andromeda)", "batch": "batch2"},
    {"id": "E_wZJhuSK5U", "title": "NEW BEST Facebook Ads Campaign Structure 2026", "batch": "batch2"},
]

def fetch_transcript(video_id, title):
    """Fetch transcript for a single video."""
    try:
        ytt = YouTubeTranscriptApi()
        transcript = ytt.fetch(video_id)
        text = "\n".join([item.text for item in transcript])
        return {"success": True, "text": text, "chars": len(text)}
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    output_dir = "meta_ads_transcripts"
    os.makedirs(output_dir, exist_ok=True)
    
    results = {"success": [], "failed": []}
    
    for i, video in enumerate(VIDEOS, 1):
        print(f"[{i}/{len(VIDEOS)}] Fetching: {video['title'][:50]}...")
        result = fetch_transcript(video["id"], video["title"])
        
        if result["success"]:
            # Save transcript
            filename = f"{output_dir}/{video['batch']}_{video['id']}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {video['title']}\n")
                f.write(f"# Video: https://www.youtube.com/watch?v={video['id']}\n\n")
                f.write(result["text"])
            
            print(f"  ✓ Saved ({result['chars']} chars)")
            results["success"].append(video["title"])
        else:
            print(f"  ✗ Failed: {result['error'][:100]}")
            results["failed"].append({"title": video["title"], "error": result["error"][:200]})
    
    # Save summary
    with open(f"{output_dir}/_summary.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Done! {len(results['success'])}/{len(VIDEOS)} transcripts saved to {output_dir}/")
    print(f"Send me the {output_dir} folder when done!")

if __name__ == "__main__":
    main()
