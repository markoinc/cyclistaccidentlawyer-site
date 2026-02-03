# Gmail Sending SOP

**Created:** 2026-02-03
**Source:** Joan Suh email workflow

---

## Authentication

Token stored at: `~/.config/gcal-pro/token.json`
- Has Gmail send scope
- Authenticated as: sierra@kuriosbrand.com
- Can send FROM: mark@kuriosbrand.com (workspace alias)

---

## Sending Code Template

```python
import json, requests, base64
from email.mime.text import MIMEText

# Load token
with open('~/.config/gcal-pro/token.json') as f:
    data = json.load(f)
    token = data['token']

# Create email
message = MIMEText(body)
message['to'] = 'recipient@email.com'
message['cc'] = 'sierra@kuriosbrand.com, carlos@kuriosbrand.com'
message['from'] = 'mark@kuriosbrand.com'
message['subject'] = 'Subject Line'

raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

# Send
url = 'https://gmail.googleapis.com/gmail/v1/users/me/messages/send'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}
r = requests.post(url, headers=headers, json={'raw': raw})
```

---

## Standard CCs for Sales Emails

- sierra@kuriosbrand.com (always)
- carlos@kuriosbrand.com (for MVA sales)

---

## Signature Format

```
Mark Gundrum
kuriosbrand.com
```

**DO NOT INCLUDE:**
- ❌ KuriosBrand LLC
- ❌ Phone number
- ❌ Address
- ❌ Title

---

## Before Sending Checklist

1. [ ] Draft reviewed and approved by Marko
2. [ ] Signature is correct (just name + website)
3. [ ] Follow-up date pulled from Google Calendar
4. [ ] CC list confirmed
5. [ ] Subject line clear and benefit-focused
