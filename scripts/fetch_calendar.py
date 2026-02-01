#!/usr/bin/env python3
"""Fetch calendar events and output as JSON for dashboard."""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add gcal-pro scripts to path
GCAL_PATH = Path.home() / "clawd" / "skills" / "gcal-pro" / "scripts"
sys.path.insert(0, str(GCAL_PATH))

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
except ImportError:
    print(json.dumps({"error": "Google API not installed"}))
    sys.exit(1)

TOKEN_PATH = Path.home() / ".config" / "gcal-pro" / "token.json"
CALENDAR_ID = "mark@kuriosbrand.com"

def get_calendar_service():
    """Get authenticated calendar service."""
    if not TOKEN_PATH.exists():
        return None
    
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    return build('calendar', 'v3', credentials=creds)

def fetch_events(days=7):
    """Fetch upcoming events."""
    service = get_calendar_service()
    if not service:
        return {"error": "Not authenticated"}
    
    now = datetime.utcnow()
    time_min = now.isoformat() + 'Z'
    time_max = (now + timedelta(days=days)).isoformat() + 'Z'
    
    try:
        events_result = service.events().list(
            calendarId=CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            maxResults=20,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        formatted = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))
            
            formatted.append({
                'id': event['id'],
                'title': event.get('summary', 'No title'),
                'start': start,
                'end': end,
                'location': event.get('location', ''),
                'description': event.get('description', ''),
                'allDay': 'date' in event['start']
            })
        
        return {
            'events': formatted,
            'count': len(formatted),
            'updated': datetime.utcnow().isoformat() + 'Z'
        }
    
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    result = fetch_events()
    print(json.dumps(result, indent=2))
