#!/usr/bin/env python3
"""Download YouTube video audio and transcribe using OpenAI Whisper API"""
import os
import sys
import subprocess
from openai import OpenAI

# Load API key from .env.local
with open('/home/ec2-user/clawd/.env.local') as f:
    for line in f:
        if line.startswith('OPENAI_API_KEY='):
            os.environ['OPENAI_API_KEY'] = line.strip().split('=', 1)[1]

client = OpenAI()

def download_audio(url, output_path):
    """Download audio from YouTube video"""
    cmd = [
        'yt-dlp',
        '-x',  # Extract audio
        '--audio-format', 'mp3',
        '--audio-quality', '5',  # Medium quality to keep file size down
        '-o', output_path,
        '--no-playlist',
        url
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error downloading: {result.stderr}")
        return False
    return True

def transcribe_audio(audio_path):
    """Transcribe audio using OpenAI Whisper API"""
    with open(audio_path, 'rb') as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    return transcript

def get_video_info(url):
    """Get video title and duration"""
    cmd = ['yt-dlp', '--print', '%(title)s|||%(channel)s|||%(duration_string)s', '--no-playlist', url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        parts = result.stdout.strip().split('|||')
        return {
            'title': parts[0] if len(parts) > 0 else 'Unknown',
            'channel': parts[1] if len(parts) > 1 else 'Unknown',
            'duration': parts[2] if len(parts) > 2 else 'Unknown'
        }
    return {'title': 'Unknown', 'channel': 'Unknown', 'duration': 'Unknown'}

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python transcribe.py <youtube_url> <output_name>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_name = sys.argv[2]
    base_dir = '/home/ec2-user/clawd/data/meta-ads-knowledge/batch3'
    
    # Get video info
    print(f"Getting info for: {url}")
    info = get_video_info(url)
    print(f"Title: {info['title']}")
    print(f"Channel: {info['channel']}")
    print(f"Duration: {info['duration']}")
    
    # Download audio
    audio_path = f"{base_dir}/{output_name}.mp3"
    print(f"\nDownloading audio to {audio_path}...")
    if not download_audio(url, audio_path):
        print("Failed to download audio")
        sys.exit(1)
    
    # Transcribe
    print("\nTranscribing with OpenAI Whisper...")
    transcript = transcribe_audio(audio_path)
    
    # Save transcript
    transcript_path = f"{base_dir}/{output_name}.md"
    with open(transcript_path, 'w') as f:
        f.write(f"# {info['title']}\n\n")
        f.write(f"**Channel:** {info['channel']}\n")
        f.write(f"**Duration:** {info['duration']}\n")
        f.write(f"**URL:** {url}\n\n")
        f.write("---\n\n")
        f.write(transcript)
    
    print(f"\nTranscript saved to: {transcript_path}")
    
    # Clean up audio file to save space
    os.remove(audio_path)
    print(f"Audio file removed: {audio_path}")
