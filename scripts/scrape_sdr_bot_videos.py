#!/usr/bin/env python3
"""
Scrape YouTube transcripts for AI SDR Bot knowledge base.
Focus: Appointment booking, lead qualification, follow-up automation, omnichannel chatbots
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

# AI SDR Bot focused videos - verified from search
SDR_BOT_VIDEOS = [
    # GHL AI Chatbot / Appointment Setter
    {"id": "00XNr2XV9R0", "title": "How to Build an Ai Chatbot & Appointment Setter with GoHighLevel 2024", "category": "ghl-chatbot"},
    {"id": "ScIaMx2EcLY", "title": "Build an Ai Appointment Setter on FB/IG/SMS in GoHighLevel 2024", "category": "ghl-chatbot"},
    {"id": "OSG8ge19lzs", "title": "Building An AI Appointment Booking Bot Using GoHighlevel Conversation AI", "category": "ghl-chatbot"},
    {"id": "WTQxWc6a6n0", "title": "GoHighLevel AI Appointment Booking Bot Step-by-Step Guide", "category": "ghl-chatbot"},
    {"id": "9Lf9XurozJE", "title": "The Best Ai Booking For Gohighlevel 2024 - Zappychat Full Install", "category": "ghl-chatbot"},
    {"id": "XFZ7X11eNio", "title": "Build an AI Appointment Setter for GHL with Retell AI & n8n", "category": "ghl-chatbot"},
    {"id": "fCPRlxDbgq0", "title": "AI Voice Calling Appointment Setter In GoHighLevel In 10 Mins", "category": "ghl-chatbot"},
    {"id": "HQKJ3kLLwEw", "title": "How To Build an AI Appointment Booking Bot In GoHighLevel Tutorial", "category": "ghl-chatbot"},
    {"id": "kwT07RiI9O0", "title": "Vapi AI Appointment Setter To GoHighLevel Outbound w Make.com 2024", "category": "ghl-chatbot"},
    
    # VAPI Voice AI Agents
    {"id": "VNdF3B6-tyQ", "title": "Build a Voice Agent in 15 Minutes Using VAPI Easiest Tutorial", "category": "vapi-voice"},
    {"id": "for9mjbTJSc", "title": "Build an AI Appointment-Booking Voice Agent in 10 Minutes GHL VAPI", "category": "vapi-voice"},
    {"id": "y-cq_Qo4zVo", "title": "I Built an AI Voice Receptionist with Vapi and n8n MCP", "category": "vapi-voice"},
    {"id": "qUQLbPWxbdk", "title": "How to build AI voice agents with Vapi Full course", "category": "vapi-voice"},
    {"id": "Z0m_62T_L84", "title": "How to Connect Vapi AI Voice Agent with GoHighLevel to Book Appointments", "category": "vapi-voice"},
    {"id": "jDPXWMUVUPE", "title": "Vapi Phone Agents Full Course 2024 2 Hours", "category": "vapi-voice"},
    {"id": "d09rNjVE_Xo", "title": "Next-Gen AI Voice Assistant VAPI x MAKE in 2024", "category": "vapi-voice"},
    {"id": "QIqiH02wn1E", "title": "VAPI AI Tutorial Build an AI Voice Sales Agent 2025", "category": "vapi-voice"},
    {"id": "faK6uB10ROw", "title": "How to train your Voice AI Agent on Company knowledge Vapi Tutorial", "category": "vapi-voice"},
    {"id": "u_4Jw7itFtk", "title": "How To Build An AI Customer Service Voice Agent Advanced VAPI Tutorial", "category": "vapi-voice"},
    
    # n8n Lead Qualification & Automation
    {"id": "hBD_1rl9hzc", "title": "Build This Lead Qualification AI Agent from Scratch in N8N", "category": "n8n-automation"},
    {"id": "P9TfIvtYExQ", "title": "I Built a Lead Generation AI Agent with no code on n8n", "category": "n8n-automation"},
    {"id": "MeDdqAe8Irc", "title": "How to EASILY Create a Lead Qualification AI Agent in N8N", "category": "n8n-automation"},
    {"id": "tbsotEYWJ1E", "title": "I Built an AI Agent That Instantly Researches and Qualifies Leads n8n", "category": "n8n-automation"},
    {"id": "ROSdQjkOWhY", "title": "Step-by-Step Tutorial Create a Simple AI Chatbot with n8n", "category": "n8n-automation"},
    {"id": "3uperu7slI8", "title": "Automate Meta Lead Forms to WhatsApp Build an AI Agent to Qualify Leads", "category": "n8n-automation"},
    {"id": "7_PeuTsx7UM", "title": "N8N Full Course Build AI Automations in 2026 For Beginners", "category": "n8n-automation"},
    {"id": "XPK7D1qd2XY", "title": "How I Built a Fully Automated Lead Gen System n8n Tutorial", "category": "n8n-automation"},
    
    # Follow-up Sequences & Automation
    {"id": "-R4VuSkJbes", "title": "How to Automate Lead Follow-Up Using AI Email SMS Ads", "category": "followup"},
    {"id": "cZ8rK6UXinE", "title": "How to Write Email Sequences in Seconds New AI Feature", "category": "followup"},
    {"id": "AHCUA_WRpMk", "title": "Create An Automated SMS Follow Up Sequence", "category": "followup"},
    {"id": "kE6dQKhMZGQ", "title": "Write Personalized Email Sequences for Every Lead Using AI", "category": "followup"},
    {"id": "5t9xXCz4DzM", "title": "How to Automate Sales Follow-up Emails with N8N and Fireflies", "category": "followup"},
    {"id": "POnfpotsrQM", "title": "How to EASILY Automate Email Follow Ups with AI Step by Step", "category": "followup"},
    
    # Omnichannel / Multi-platform Chatbots
    {"id": "6yeFiMgelsA", "title": "Omnichannel AI Agent Automate WhatsApp Instagram Facebook SMS with AI", "category": "omnichannel"},
    {"id": "XOrYCzaN_r4", "title": "Build an Omnichannel AI Agent for WhatsApp Instagram Facebook No Code", "category": "omnichannel"},
    {"id": "qupOB0N5KOw", "title": "How To Create An Instagram Chatbot With ManyChat Full DM Automation 2024", "category": "omnichannel"},
    {"id": "SpT3Uo9en9M", "title": "Connect ChatGPT Instagram Facebook Whatsapp Step by Step Manychat", "category": "omnichannel"},
    {"id": "WqiKhE4jaj8", "title": "How to Create AI Instagram Chatbot in 2024 Manychat Tutorial", "category": "omnichannel"},
    {"id": "kpGHfxcj4K0", "title": "How To Create AI Telegram Chatbot in 2025 Free Template", "category": "omnichannel"},
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
            
            text = "\n".join([item.text for item in transcript])
            return {"success": True, "text": text, "chars": len(text)}
            
        except Exception as e:
            error_msg = str(e)
            if "Subtitles are disabled" in error_msg or "No transcripts" in error_msg:
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
    output_dir = "/home/ec2-user/clawd/data/transcripts/sdr-bot"
    os.makedirs(output_dir, exist_ok=True)
    
    existing = set(f.replace('.txt', '') for f in os.listdir(output_dir) if f.endswith('.txt'))
    new_videos = [v for v in SDR_BOT_VIDEOS if v['id'] not in existing]
    
    print(f"Already have: {len(existing)} transcripts", flush=True)
    print(f"Fetching {len(new_videos)} new transcripts...\n", flush=True)
    
    results = {"success": [], "failed": [], "no_transcript": []}
    
    for i, video in enumerate(new_videos, 1):
        print(f"[{i}/{len(new_videos)}] {video['title'][:55]}...", flush=True)
        
        result = fetch_with_proxy(video['id'], video['title'])
        
        if result['success']:
            save_transcript(video, result['text'], output_dir)
            print(f"  ✓ Saved ({result['chars']:,} chars)", flush=True)
            results['success'].append({
                "title": video['title'],
                "id": video['id'],
                "category": video['category'],
                "chars": result['chars']
            })
        elif "No transcript" in result.get('error', ''):
            print(f"  ⚠ No transcript available", flush=True)
            results['no_transcript'].append({"title": video['title'], "id": video['id']})
        else:
            print(f"  ✗ {result['error'][:60]}", flush=True)
            results['failed'].append({"title": video['title'], "id": video['id'], "error": result['error']})
        
        time.sleep(0.5)
    
    # Count by category
    final_files = [f for f in os.listdir(output_dir) if f.endswith('.txt')]
    
    summary = {
        "total_transcripts": len(final_files),
        "new_success": len(results['success']),
        "no_transcript": len(results['no_transcript']),
        "failed": len(results['failed']),
        "results": results
    }
    
    summary_file = "/home/ec2-user/clawd/data/transcripts/sdr-bot-summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*60}", flush=True)
    print(f"Done! Total SDR bot transcripts: {len(final_files)}", flush=True)
    print(f"New: {len(results['success'])} success, {len(results['no_transcript'])} no transcript, {len(results['failed'])} failed", flush=True)

if __name__ == "__main__":
    main()
