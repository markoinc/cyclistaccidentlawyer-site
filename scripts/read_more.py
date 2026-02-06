#!/usr/bin/env python3
"""Read additional data from both sheets."""
import requests

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

# July - read beyond row 199
print("=== JULY DASHBOARD rows 190-250 ===")
jul_extra = read_sheet(JUL_ID, "'📊 Dashboard'!A190:F250")
for i, row in enumerate(jul_extra):
    print(f"  Row {190+i}: {row}")

# October - get all business transactions for opening/closing balance
print("\n=== OCT Business 4991 - ALL (for opening/closing) ===")
oct_biz = read_sheet(OCT_ID, "'💼 Business 4991'!A1:F200")
if oct_biz:
    print(f"  Total rows: {len(oct_biz)}")
    print(f"  First data: {oct_biz[1] if len(oct_biz) > 1 else 'N/A'}")
    print(f"  Last data: {oct_biz[-1]}")
    # Find earliest and latest entries
    for row in oct_biz[1:]:
        if len(row) >= 5 and row[4]:
            print(f"  Date: {row[0]}, Balance: {row[4]}")

print("\n=== OCT Personal 0068 - ALL (for opening/closing) ===")
oct_per = read_sheet(OCT_ID, "'👤 Personal 0068'!A1:F200")
if oct_per:
    print(f"  Total rows: {len(oct_per)}")
    print(f"  First data: {oct_per[1] if len(oct_per) > 1 else 'N/A'}")
    print(f"  Last data: {oct_per[-1]}")
    for row in oct_per[1:]:
        if len(row) >= 5 and row[4]:
            print(f"  Date: {row[0]}, Balance: {row[4]}")

# October Discover balance
print("\n=== OCT Discover (check for tab) ===")
# Actually Discover isn't a tab - we need to find it from transactions
# Let's check what CC payments look like
print("\n=== OCT - all CC/debt related from Personal ===")
for row in oct_per[1:]:
    if len(row) >= 3 and ('CC' in str(row[2]) or 'Payment' in str(row[2]) or 'Discover' in str(row[1]) or 'DEPT' in str(row[1])):
        print(f"  {row}")

# July - get opening/closing balances for context
print("\n=== JUL Business 4991 balances ===")
jul_biz = read_sheet(JUL_ID, "'💼 Business 4991'!A1:F200")
if jul_biz:
    print(f"  Total rows: {len(jul_biz)}")
    for row in jul_biz[1:]:
        if len(row) >= 5 and row[4]:
            print(f"  Date: {row[0]}, Balance: {row[4]}")

print("\n=== JUL Personal 0068 balances ===")
jul_per = read_sheet(JUL_ID, "'👤 Personal 0068'!A1:F200")
if jul_per:
    print(f"  Total rows: {len(jul_per)}")
    # Show first and last with balances
    balances = [(i, row) for i, row in enumerate(jul_per[1:]) if len(row) >= 5 and row[4]]
    if balances:
        print(f"  First: {balances[0][1]}")
        print(f"  Last: {balances[-1][1]}")

# Check July dashboard formatting via get with includeGridData
print("\n=== JULY Dashboard - check for subtotal row formatting ===")
# We'll get formatting info via spreadsheets.get with includeGridData
url = f'https://sheets.googleapis.com/v4/spreadsheets/{JUL_ID}?ranges=%F0%9F%93%8A%20Dashboard!A1:F200&fields=sheets.data.rowData.values(formattedValue,effectiveFormat.backgroundColor,effectiveFormat.textFormat)'
r = requests.get(url, headers=HEADERS)
if r.status_code == 200:
    data = r.json()
    rows = data['sheets'][0]['data'][0].get('rowData', [])
    print(f"  Total rows with data: {len(rows)}")
    # Find subtotal/total rows and their formatting
    for i, row in enumerate(rows):
        vals = row.get('values', [])
        for v in vals:
            fv = v.get('formattedValue', '')
            if 'subtotal' in fv.lower() or 'total' in fv.lower() or 'SECTION' in fv:
                bg = v.get('effectiveFormat', {}).get('backgroundColor', {})
                tf = v.get('effectiveFormat', {}).get('textFormat', {})
                fg = tf.get('foregroundColor', {})
                print(f"  Row {i+1}: '{fv}' | BG: r={bg.get('red',0):.2f} g={bg.get('green',0):.2f} b={bg.get('blue',0):.2f} | FG: r={fg.get('red',1):.2f} g={fg.get('green',1):.2f} b={fg.get('blue',1):.2f} | Bold: {tf.get('bold', False)}")
                break
else:
    print(f"  Error: {r.status_code}")
