#!/usr/bin/env python3
"""Fetch YouTube transcript using youtube-transcript-api"""
import sys
import re
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_transcript(video_id):
    """Fetch transcript for video"""
    try:
        ytt_api = YouTubeTranscriptApi()
        
        # Try to list available transcripts
        transcript_list = ytt_api.list(video_id)
        
        # Find best transcript (prefer manual English, then auto-generated)
        transcript = None
        for t in transcript_list:
            if t.language_code == 'en' and not t.is_generated:
                transcript = t
                break
        
        if not transcript:
            for t in transcript_list:
                if t.language_code.startswith('en'):
                    transcript = t
                    break
        
        if not transcript and transcript_list:
            transcript = transcript_list[0]
        
        if transcript:
            data = ytt_api.fetch(transcript)
            full_text = ' '.join([item.text for item in data])
            return full_text
        else:
            return "ERROR: No transcript available"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fetch_transcript.py <youtube_url_or_id>")
        sys.exit(1)
    
    video_input = sys.argv[1]
    video_id = extract_video_id(video_input)
    
    if not video_id:
        print(f"Could not extract video ID from: {video_input}")
        sys.exit(1)
    
    print(f"Fetching transcript for video: {video_id}")
    transcript = fetch_transcript(video_id)
    print(transcript)
