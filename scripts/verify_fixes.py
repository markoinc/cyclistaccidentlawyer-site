#!/usr/bin/env python3
"""Verify the dashboard fixes were applied correctly."""
import requests
import json

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
    return []

# ============ VERIFY OCTOBER 2025 ============
print("=" * 60)
print("VERIFY: OCTOBER 2025 — Sections F-I")
print("=" * 60)

oct_dash = read_sheet(OCT_ID, "'📊 Dashboard'!A199:F240")
for i, row in enumerate(oct_dash):
    if row:  # skip truly empty rows
        print(f"  Row {199+i}: {row}")

# ============ VERIFY JULY 2025 ============
print("\n" + "=" * 60)
print("VERIFY: JULY 2025 — Formatting + Sections")
print("=" * 60)

# Check the new categories in Section C
print("\n--- Section C end (missing categories added) ---")
jul_c = read_sheet(JUL_ID, "'📊 Dashboard'!A153:D165")
for i, row in enumerate(jul_c):
    print(f"  Row {153+i}: {row}")

# Check Section G (Account Balances)
print("\n--- Section G: Account Balances ---")
jul_g = read_sheet(JUL_ID, "'📊 Dashboard'!A198:D210")
for i, row in enumerate(jul_g):
    if row:
        print(f"  Row {198+i}: {row}")

# Check Section H relabeling
print("\n--- Section H header ---")
jul_h = read_sheet(JUL_ID, "'📊 Dashboard'!A207:D210")
for i, row in enumerate(jul_h):
    if row:
        print(f"  Row {207+i}: {row}")

# Check Section I relabeling
print("\n--- Section I header ---")
jul_i = read_sheet(JUL_ID, "'📊 Dashboard'!A221:D225")
for i, row in enumerate(jul_i):
    if row:
        print(f"  Row {221+i}: {row}")

# Verify subtotal formatting
print("\n--- Verify subtotal row formatting (spot check rows 48, 91, 102) ---")
url = f'https://sheets.googleapis.com/v4/spreadsheets/{JUL_ID}?ranges=%F0%9F%93%8A%20Dashboard!A48:D48&ranges=%F0%9F%93%8A%20Dashboard!A91:D91&ranges=%F0%9F%93%8A%20Dashboard!A102:D102&fields=sheets.data.rowData.values(formattedValue,effectiveFormat.backgroundColor,effectiveFormat.textFormat)'
r = requests.get(url, headers=HEADERS)
if r.status_code == 200:
    data = r.json()
    for sheet_data in data['sheets'][0]['data']:
        rows = sheet_data.get('rowData', [])
        for row in rows:
            for v in row.get('values', []):
                fv = v.get('formattedValue', '')
                if fv:
                    bg = v.get('effectiveFormat', {}).get('backgroundColor', {})
                    tf = v.get('effectiveFormat', {}).get('textFormat', {})
                    fg = tf.get('foregroundColor', {})
                    print(f"  '{fv}' | BG: r={bg.get('red',0):.2f} g={bg.get('green',0):.2f} b={bg.get('blue',0):.2f} | FG: r={fg.get('red',1):.2f} g={fg.get('green',1):.2f} b={fg.get('blue',1):.2f} | Bold: {tf.get('bold', False)}")
                    break

print("\n✅ Verification complete")
