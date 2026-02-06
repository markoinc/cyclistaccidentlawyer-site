#!/usr/bin/env python3
"""Read existing dashboard data from October and July 2025 sheets."""
import requests
import json

# Get OAuth token
r = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
    'grant_type': 'refresh_token'
})
TOKEN = r.json()['access_token']
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

OCT_ID = '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA'
JUL_ID = '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8'

def read_sheet(sheet_id, range_name):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}'
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json().get('values', [])
    else:
        print(f"Error reading {range_name}: {r.status_code} {r.text[:200]}")
        return []

def get_sheet_metadata(sheet_id):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?fields=sheets(properties(title,sheetId))'
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Error: {r.status_code} {r.text[:200]}")
        return {}

# ============ OCTOBER 2025 ============
print("=" * 60)
print("OCTOBER 2025 SHEET")
print("=" * 60)

oct_meta = get_sheet_metadata(OCT_ID)
print("\nTabs:")
for s in oct_meta.get('sheets', []):
    p = s['properties']
    print(f"  {p['title']} (sheetId: {p['sheetId']})")

# Read dashboard
oct_dash = read_sheet(OCT_ID, "'📊 Dashboard'!A1:F200")
print(f"\nDashboard rows: {len(oct_dash)}")
for i, row in enumerate(oct_dash):
    print(f"  Row {i+1}: {row}")

# Read business transactions for balance data
print("\n--- Business 4991 (first 5, last 5) ---")
oct_biz = read_sheet(OCT_ID, "'💼 Business 4991'!A1:F100")
if oct_biz:
    for row in oct_biz[:5]:
        print(f"  {row}")
    print("  ...")
    for row in oct_biz[-5:]:
        print(f"  {row}")

print("\n--- Personal 0068 (first 5, last 5) ---")
oct_per = read_sheet(OCT_ID, "'👤 Personal 0068'!A1:F100")
if oct_per:
    for row in oct_per[:5]:
        print(f"  {row}")
    print("  ...")
    for row in oct_per[-5:]:
        print(f"  {row}")

# Read CC tabs for debt data
print("\n--- Sapphire 4252 (first 5, last 5) ---")
oct_sap = read_sheet(OCT_ID, "'💎 Sapphire 4252'!A1:F50")
if oct_sap:
    for row in oct_sap[:5]:
        print(f"  {row}")
    print("  ...")
    for row in oct_sap[-5:]:
        print(f"  {row}")

print("\n--- Ink CC 0678 (first 5, last 5) ---")
oct_ink = read_sheet(OCT_ID, "'💳 Biz CC 0678'!A1:F50")
if oct_ink:
    for row in oct_ink[:5]:
        print(f"  {row}")
    print("  ...")
    for row in oct_ink[-5:]:
        print(f"  {row}")

# ============ JULY 2025 ============
print("\n" + "=" * 60)
print("JULY 2025 SHEET")
print("=" * 60)

jul_meta = get_sheet_metadata(JUL_ID)
print("\nTabs:")
for s in jul_meta.get('sheets', []):
    p = s['properties']
    print(f"  {p['title']} (sheetId: {p['sheetId']})")

# Read dashboard
jul_dash = read_sheet(JUL_ID, "'📊 Dashboard'!A1:F200")
print(f"\nDashboard rows: {len(jul_dash)}")
for i, row in enumerate(jul_dash):
    print(f"  Row {i+1}: {row}")

# Read personal transactions for missing categories
print("\n--- July Personal 0068 (first 5, last 5) ---")
jul_per = read_sheet(JUL_ID, "'👤 Personal 0068'!A1:F100")
if jul_per:
    for row in jul_per[:5]:
        print(f"  {row}")
    print("  ...")
    for row in jul_per[-5:]:
        print(f"  {row}")

print("\n--- July Sapphire 4252 (first 5, last 5) ---")
jul_sap = read_sheet(JUL_ID, "'💎 Sapphire 4252'!A1:F100")
if jul_sap:
    for row in jul_sap[:5]:
        print(f"  {row}")
    print("  ...")
    for row in jul_sap[-5:]:
        print(f"  {row}")
