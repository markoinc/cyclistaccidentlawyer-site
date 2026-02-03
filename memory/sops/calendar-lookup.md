# Google Calendar Lookup SOP

**Created:** 2026-02-03

---

## Authentication

Token: `~/.config/gcal-pro/token.json`
Calendar ID: `mark@kuriosbrand.com` (NOT 'primary')

---

## Searching for Events

```python
import json, requests
from datetime import datetime, timedelta

with open('~/.config/gcal-pro/token.json') as f:
    token = json.load(f)['token']

now = datetime.utcnow()
time_min = now.isoformat() + 'Z'
time_max = (now + timedelta(days=30)).isoformat() + 'Z'

url = 'https://www.googleapis.com/calendar/v3/calendars/mark@kuriosbrand.com/events'
params = {
    'timeMin': time_min,
    'timeMax': time_max,
    'maxResults': 50,
    'singleEvents': True,
    'orderBy': 'startTime',
    'q': 'SEARCH_TERM'  # e.g., 'Joan' or 'follow up'
}
headers = {'Authorization': f'Bearer {token}'}
r = requests.get(url, params=params, headers=headers)

for event in r.json().get('items', []):
    start = event.get('start', {}).get('dateTime', '')
    print(f"{start} - {event.get('summary', 'No title')}")
```

---

## Common Use Cases

### Finding a follow-up call
```python
params['q'] = 'Joan'  # Or contact name
```

### Getting today's events
```python
time_max = (now + timedelta(days=1)).isoformat() + 'Z'
```

### Getting this week
```python
time_max = (now + timedelta(days=7)).isoformat() + 'Z'
```

---

## Calendar Skill

Full skill at: `/home/ec2-user/clawd/skills/gcal-pro/SKILL.md`

Quick commands:
- `python scripts/gcal_core.py today`
- `python scripts/gcal_core.py search -q "meeting"`
- `python scripts/gcal_core.py week`
