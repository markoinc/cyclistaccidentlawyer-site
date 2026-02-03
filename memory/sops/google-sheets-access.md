# Google Sheets Access SOP

**Created:** 2026-02-03

---

## Authentication

Token: `~/.config/gcal-pro/token.json`
- Has Drive + Sheets scopes
- Authenticated as: sierra@kuriosbrand.com

---

## Key Sheets

| Sheet | ID | Purpose |
|-------|-------|---------|
| Kurios MVA Appointments | `1iu8lHRKAt_eDoHr6SreDktQhwT8l0R-VFpfvObKHtMQ` | Main CRM/pipeline |
| Kurios Performance Stats | `1Ka5HMSXoxsffYX3W-jlNURMkFiNuA7FcptM4tkx6h7c` | Pricing/stats |
| Exa Contacts Master | `1pl6K1kVHgxipiqro8bdZh6TzPTBaRs0-5adIaF2y9dk` | Lead lists |

---

## Reading a Sheet

```python
import json, requests

with open('~/.config/gcal-pro/token.json') as f:
    token = json.load(f)['token']

sheet_id = 'SHEET_ID_HERE'
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A:Z'
headers = {'Authorization': f'Bearer {token}'}
r = requests.get(url, headers=headers)
data = r.json()
```

---

## Listing All Sheets

```python
url = 'https://www.googleapis.com/drive/v3/files'
params = {
    'q': "mimeType='application/vnd.google-apps.spreadsheet'",
    'pageSize': 25,
    'fields': 'files(id,name,modifiedTime)'
}
headers = {'Authorization': f'Bearer {token}'}
r = requests.get(url, params=params, headers=headers)
```

---

## Writing to a Sheet

```python
url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A1:Z1:append'
params = {'valueInputOption': 'USER_ENTERED'}
body = {'values': [['col1', 'col2', 'col3']]}
r = requests.post(url, headers=headers, params=params, json=body)
```
