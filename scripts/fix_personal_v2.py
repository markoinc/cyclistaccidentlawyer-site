#!/usr/bin/env python3
"""Fix header row formatting and percentages."""
import requests

def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

SHEET_ID = '1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ'
TOKEN = get_token()
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}

def batch_update(reqs):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate'
    resp = requests.post(url, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}, json={'requests': reqs})
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code}: {resp.text[:300]}")
    return resp.status_code == 200

def update_values(range_str, values):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{requests.utils.quote(range_str)}?valueInputOption=RAW'
    resp = requests.put(url, headers={'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}, json={'values': values})
    return resp.status_code == 200

def read_tab(tab):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{requests.utils.quote(tab)}!A1:P200'
    return requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'}).json().get('values', [])

# ============================================================
# Fix Personal Overview - column header rows should be plain text, not currency
# ============================================================
print("🔧 Fixing Personal Overview headers...")
sid = 200
rows = read_tab('👤 Personal Overview')

# Find all column header rows (rows where first cell is Source/Category/Month)
header_row_indices = []
for i, row in enumerate(rows):
    if row and row[0] in ['Source', 'Category', 'Month']:
        header_row_indices.append(i)

print(f"  Header rows at: {header_row_indices}")

# Re-write the header values as raw text to undo currency formatting
for i in header_row_indices:
    row = rows[i]
    # Make sure the year columns show as text "2024", "2025", "2026 YTD" not numbers
    update_values(f"'👤 Personal Overview'!A{i+1}", [row])

# Clear formatting on header rows for columns B onward  
fix_reqs = []
for i in header_row_indices:
    # Set these cells to automatic number format (text)
    fix_reqs.append({
        'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 1, 'endColumnIndex': 6},
            'cell': {
                'userEnteredFormat': {
                    'numberFormat': {'type': 'TEXT'},
                    'backgroundColor': LIGHT_GRAY,
                    'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'}
                }
            },
            'fields': 'userEnteredFormat(numberFormat,backgroundColor,textFormat)'
        }
    })

# Also fix the percentage column in spending section
# Find the % of Total column
for i, row in enumerate(rows):
    if row and len(row) > 5 and row[5] == '% of Total':
        # Set column F as percentage format from this row onward
        fix_reqs.append({
            'repeatCell': {
                'range': {'sheetId': sid, 'startRowIndex': i+1, 'endRowIndex': i+20, 'startColumnIndex': 5, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {'type': 'PERCENT', 'pattern': '0%'},
                        'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                    }
                },
                'fields': 'userEnteredFormat(numberFormat,textFormat)'
            }
        })

if fix_reqs:
    batch_update(fix_reqs)
    print("  ✅ Headers fixed")

# ============================================================
# Now fix the year tab percentage columns too
# ============================================================
print("\n🔧 Fixing year tab personal section formatting...")

for tab_name, sid_yr in [('📅 2024', 3), ('📅 2025', 1), ('📅 2026', 2)]:
    rows_yr = read_tab(tab_name)
    
    fix_yr = []
    for i, row in enumerate(rows_yr):
        if not row:
            continue
        # Find "% of Spending" column and format as percentage
        if len(row) > 2 and row[2] == '% of Spending':
            # Format percentage column from here down ~20 rows
            fix_yr.append({
                'repeatCell': {
                    'range': {'sheetId': sid_yr, 'startRowIndex': i+1, 'endRowIndex': i+20, 'startColumnIndex': 2, 'endColumnIndex': 3},
                    'cell': {
                        'userEnteredFormat': {
                            'numberFormat': {'type': 'PERCENT', 'pattern': '0%'},
                            'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                        }
                    },
                    'fields': 'userEnteredFormat(numberFormat,textFormat)'
                }
            })
        # Fix column header rows in personal section  
        if row[0] in ['Category', 'Source', 'Month'] and i > 50:
            fix_yr.append({
                'repeatCell': {
                    'range': {'sheetId': sid_yr, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                    'cell': {
                        'userEnteredFormat': {
                            'numberFormat': {'type': 'TEXT'},
                            'backgroundColor': LIGHT_GRAY,
                            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'}
                        }
                    },
                    'fields': 'userEnteredFormat(numberFormat,backgroundColor,textFormat)'
                }
            })
            # Re-write values as text
            update_values(f"'{tab_name}'!A{i+1}", [row])
    
    if fix_yr:
        batch_update(fix_yr)
        print(f"  ✅ {tab_name} fixed")

# ============================================================
# Fix the overview data: rewrite header rows with plain text values
# ============================================================
print("\n🔧 Rewriting header row values...")

# The header rows need to have the year labels as text
header_values = ['Source', '2024', '2025', '2026 YTD', 'All Time']
cat_header = ['Category', '2024', '2025', '2026 YTD', 'All Time', '% of Total']
month_header = ['Month', 'Income', 'Spending', 'Net Cash Flow', 'Running Total']

for i, row in enumerate(rows):
    if row and row[0] == 'Source':
        update_values(f"'👤 Personal Overview'!A{i+1}", [header_values])
        print(f"  Row {i+1}: Source header rewritten")
    if row and row[0] == 'Category' and len(row) > 4:
        update_values(f"'👤 Personal Overview'!A{i+1}", [cat_header])
        print(f"  Row {i+1}: Category header rewritten")
    if row and row[0] == 'Month' and len(row) > 3:
        if 'Income' in str(row[1]) if len(row) > 1 else False:
            update_values(f"'👤 Personal Overview'!A{i+1}", [month_header])
            print(f"  Row {i+1}: Month header rewritten")

print("\n✅ All fixes applied!")
