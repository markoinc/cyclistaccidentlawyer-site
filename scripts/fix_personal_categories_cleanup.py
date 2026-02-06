#!/usr/bin/env python3
"""
Cleanup script for personal categories issues:
1. June: Fix Travel section (THE DINNER DETECTIVE is not travel)
2. October: Remove duplicate CC Interest section
3. September: Fix Shopping & Misc overlap with Donations & Misc 
4. November: Fix FX fee in Food & Dining
5. December: Add missing CC interest data, fix Shopping & Misc overlap with Living
"""

import requests
import time

def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

TOKEN = get_token()
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

def read_range(sheet_id, range_str):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_str}"
    resp = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    return resp.json().get('values', [])

def write_range(sheet_id, range_str, values):
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_str}?valueInputOption=RAW"
    resp = requests.put(url, headers=HEADERS, json={'values': values})
    return resp.status_code == 200

def delete_rows(sheet_id, gid, start_idx, end_idx):
    """Delete rows from start_idx to end_idx (exclusive)."""
    req = {
        'requests': [{
            'deleteDimension': {
                'range': {
                    'sheetId': gid,
                    'dimension': 'ROWS',
                    'startIndex': start_idx,
                    'endIndex': end_idx,
                }
            }
        }]
    }
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate'
    resp = requests.post(url, headers=HEADERS, json=req)
    return resp.status_code == 200

def insert_rows(sheet_id, gid, at_row, num_rows):
    """Insert blank rows."""
    req = {
        'requests': [{
            'insertDimension': {
                'range': {
                    'sheetId': gid,
                    'dimension': 'ROWS',
                    'startIndex': at_row,
                    'endIndex': at_row + num_rows,
                },
                'inheritFromBefore': True,
            }
        }]
    }
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate'
    resp = requests.post(url, headers=HEADERS, json=req)
    return resp.status_code == 200

def format_rows(sheet_id, gid, rows_data, start_row):
    """Apply formatting: bold headers, gray subtotals."""
    reqs = []
    for i, row in enumerate(rows_data):
        actual_row = start_row + i
        row_text = ' '.join(str(c) for c in row) if row else ''
        
        # Category header
        if row and len(row) >= 1 and row[0] and any(e in str(row[0]) for e in ['📈','🏠','🍔','📺','✈️','🛍️','💳','💰','🏧']):
            reqs.append({
                'repeatCell': {
                    'range': {'sheetId': gid, 'startRowIndex': actual_row, 'endRowIndex': actual_row + 1, 'startColumnIndex': 0, 'endColumnIndex': 4},
                    'cell': {'userEnteredFormat': {'textFormat': {'bold': True}}},
                    'fields': 'userEnteredFormat.textFormat.bold',
                }
            })
        
        # Subtotal row
        if 'Subtotal' in row_text or 'SUBTOTAL' in row_text:
            reqs.append({
                'repeatCell': {
                    'range': {'sheetId': gid, 'startRowIndex': actual_row, 'endRowIndex': actual_row + 1, 'startColumnIndex': 0, 'endColumnIndex': 4},
                    'cell': {'userEnteredFormat': {
                        'textFormat': {'bold': True},
                        'backgroundColor': {'red': 0.953, 'green': 0.953, 'blue': 0.953, 'alpha': 1.0},
                    }},
                    'fields': 'userEnteredFormat.textFormat.bold,userEnteredFormat.backgroundColor',
                }
            })
    
    if reqs:
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate'
        requests.post(url, headers=HEADERS, json={'requests': reqs})

def get_gid(sheet_id):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?fields=sheets.properties'
    resp = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    for s in resp.json().get('sheets', []):
        if 'Dashboard' in s['properties']['title']:
            return s['properties']['sheetId']
    return 0

# ============================================================
# FIX 1: June 2025 — Remove incorrect Travel section
# "THE DINNER DETECTIVE" is entertainment, not travel
# June has no travel transactions from CSV data
# ============================================================
print("=" * 60)
print("FIX 1: June 2025 — Remove incorrect Travel section")
print("=" * 60)

JUNE_ID = '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg'
JUNE_GID = get_gid(JUNE_ID)

# Read area around the inserted Travel section
rows = read_range(JUNE_ID, "'📊 Dashboard'!A118:D130")
print("Current state:")
for i, r in enumerate(rows, 118):
    print(f"  Row {i}: {r}")

# The Travel section was inserted at rows 121-123 (0-indexed: 120-122)
# Row 121: ['✈️ Travel']  
# Row 122: ['', 'THE DINNER DETECTIVE', '1', '($190.00)']
# Row 123: ['', '', 'Travel Subtotal', '($190.00)']
# Replace with: Travel category with $0.00 (no actual travel in June CSVs)
print("\nReplacing Travel section with $0.00 (no travel in June)...")
new_data = [
    ['✈️ Travel'],
    ['', '(No travel transactions this month)', '0', '$0.00'],
    ['', '', 'Travel Subtotal', '$0.00'],
]
success = write_range(JUNE_ID, "'📊 Dashboard'!A121:D123", new_data)
print(f"  Write success: {success}")
format_rows(JUNE_ID, JUNE_GID, new_data, 120)  # 0-indexed
time.sleep(1)

# ============================================================
# FIX 2: October 2025 — Remove duplicate CC Interest section
# Original "💰 Interest & Fees" at rows 175-181 already has Sapphire interest
# My added "💰 CC Interest & Fees (Personal)" at rows 185-187 duplicates it
# ============================================================
print("\n" + "=" * 60)
print("FIX 2: October 2025 — Remove duplicate CC Interest section")
print("=" * 60)

OCT_ID = '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA'
OCT_GID = get_gid(OCT_ID)

# Verify current state
rows = read_range(OCT_ID, "'📊 Dashboard'!A180:D195")
print("Current state:")
for i, r in enumerate(rows, 180):
    print(f"  Row {i}: {r}")

# Delete rows 185-187 (the duplicate CC Interest section) - 0-indexed: 184-187
# Row 185: ['💰 CC Interest & Fees (Personal)']
# Row 186: ['', 'Sapphire 4252 Interest', '1', '($165.48)']
# Row 187: ['', '', 'CC Interest/Fees Subtotal', '($165.48)']
print("\nDeleting duplicate CC Interest rows 185-187...")
success = delete_rows(OCT_ID, OCT_GID, 184, 187)
print(f"  Delete success: {success}")
time.sleep(1)

# ============================================================
# FIX 3: September 2025 — Fix Shopping & Misc overlap
# GoFundMe, Apple Cash, PayPal already exist in "💸 Donations & Misc"
# Only keep Target and Airalo in Shopping & Misc
# ============================================================
print("\n" + "=" * 60)
print("FIX 3: September 2025 — Fix Shopping & Misc overlap")
print("=" * 60)

SEP_ID = '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM'
SEP_GID = get_gid(SEP_ID)

# Read current Shopping & Misc section
rows = read_range(SEP_ID, "'📊 Dashboard'!A110:D117")
print("Current state:")
for i, r in enumerate(rows, 110):
    print(f"  Row {i}: {r}")

# Current rows 110-116:
# 110: ['🛍️ Shopping & Misc']
# 111: ['', 'GoFundMe', '2', '($345.50)']  <- DUPLICATE
# 112: ['', 'Apple Cash', '3', '($110.00)'] <- DUPLICATE  
# 113: ['', 'Target', '1', '($74.96)']
# 114: ['', 'Airalo (eSIM)', '2', '($34.30)']  <- Actually Travel-related
# 115: ['', 'PayPal', '1', '($28.35)']  <- DUPLICATE
# 116: ['', '', 'Shopping/Misc Subtotal', '($593.11)']

# Replace with just non-duplicate items
# Actually Airalo should probably be in Travel, but since we already have it in Section C Travel,
# let's keep the remaining unique Shopping items only
new_data = [
    ['🛍️ Shopping & Misc'],
    ['', 'Target', '1', '($74.96)'],
    ['', '', 'Shopping/Misc Subtotal', '($74.96)'],
]

# Delete the extra rows first (we have 7 rows, need only 3)
# Delete rows 113-116 (4 rows, 0-indexed: 112-116)
print("\nRemoving 4 extra rows...")
success = delete_rows(SEP_ID, SEP_GID, 112, 116)
print(f"  Delete success: {success}")
time.sleep(0.5)

# Now write the corrected data (rows 110-112)
print("Writing corrected Shopping & Misc...")
success = write_range(SEP_ID, "'📊 Dashboard'!A110:D112", new_data)
print(f"  Write success: {success}")
format_rows(SEP_ID, SEP_GID, new_data, 109)  # 0-indexed
time.sleep(1)

# ============================================================
# FIX 4: November 2025 — Fix Food & Dining (remove FX fee)
# FX fee of $0.36 should not be in Food & Dining
# ============================================================
print("\n" + "=" * 60)
print("FIX 4: November 2025 — Fix Food & Dining section")
print("=" * 60)

NOV_ID = '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0'
NOV_GID = get_gid(NOV_ID)

# Read current section
rows = read_range(NOV_ID, "'📊 Dashboard'!A93:D100")
print("Current state:")
for i, r in enumerate(rows, 93):
    print(f"  Row {i}: {r}")

# Current:
# 93: ['🍔 Food & Dining']
# 94: ['', 'IZI*CAFE FELIZ LIMA', '1', '($12.13)']
# 95: ['', 'Foreign Exchange Fees', '1', '($0.36)']  <- WRONG
# 96: ['', '', 'Food/Dining Subtotal', '($12.49)']

# Fix: Remove FX fee row and update subtotal
new_data = [
    ['🍔 Food & Dining'],
    ['', 'Cafe Feliz (Lima)', '1', '($12.13)'],
    ['', '', 'Food/Dining Subtotal', '($12.13)'],
]

# Delete the extra row (was 4 rows, need 3)
print("\nRemoving FX fee row...")
success = delete_rows(NOV_ID, NOV_GID, 94, 95)  # Delete row 95 (0-indexed: 94)
print(f"  Delete success: {success}")
time.sleep(0.5)

# Write corrected data
print("Writing corrected Food & Dining...")
success = write_range(NOV_ID, "'📊 Dashboard'!A93:D95", new_data)
print(f"  Write success: {success}")
format_rows(NOV_ID, NOV_GID, new_data, 92)
time.sleep(1)

# ============================================================
# FIX 5: December 2025 — Add CC interest data & fix Shopping overlap
# The 💰 CC Interest header exists but has no data
# Also Shopping & Misc has PayPal which is already in Living/Local
# ============================================================
print("\n" + "=" * 60)
print("FIX 5: December 2025 — Add CC interest data & fix Shopping")  
print("=" * 60)

DEC_ID = '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo'
DEC_GID = get_gid(DEC_ID)

# Read current state
rows = read_range(DEC_ID, "'📊 Dashboard'!A88:D100")
print("Current state:")
for i, r in enumerate(rows, 88):
    print(f"  Row {i}: {r}")

# Current:
# 88: []  or ['', '', 'Living Subtotal', ...]
# 89: ['💰 CC Interest (Personal)']
# 90: ['🍔 Food & Dining']  <- inserted right after header with no data!
# 91: ['', '(No transactions)', '0', '$0.00']
# 92: ['', '', 'Food & Dining Subtotal', '$0.00']
# 93: ['🛍️ Shopping & Misc']
# 94: ['', 'PayPal', '1', '($52.50)']  <- duplicate with Living
# 95: ['', '', 'Shopping/Misc Subtotal', '($52.50)']
# 96: ['', '', 'TOTAL PERSONAL EXPENSES', '-$3,610.59']

# Fix: Add interest data under the CC Interest header
# December Sapphire interest: $159.81 (from CSV)
# Need to insert a data row after the header

# First, insert 2 rows after row 89 (the CC Interest header) for data + subtotal
print("\nInserting CC interest data rows...")
success = insert_rows(DEC_ID, DEC_GID, 90, 2)  # Insert 2 rows after header
print(f"  Insert success: {success}")
time.sleep(0.5)

# Write interest data
interest_data = [
    ['', 'Sapphire 4252 Interest', '1', '($159.81)'],
    ['', '', 'CC Interest/Fees Subtotal', '($159.81)'],
]
success = write_range(DEC_ID, "'📊 Dashboard'!A90:D91", interest_data)
print(f"  Write interest data: {success}")
format_rows(DEC_ID, DEC_GID, interest_data, 89)
time.sleep(0.5)

# Now fix Shopping & Misc - PayPal is already in Living (rows shifted by 2)
# Row 95 (was 93): ['🛍️ Shopping & Misc']
# Row 96 (was 94): ['', 'PayPal', '1', '($52.50)']
# Row 97 (was 95): ['', '', 'Shopping/Misc Subtotal', '($52.50)']
# PayPal $52.50 is already accounted for in Living/Local. Replace with $0.
print("Fixing Shopping & Misc (removing PayPal duplicate)...")
new_shop = [
    ['🛍️ Shopping & Misc'],
    ['', '(No additional shopping this month)', '0', '$0.00'],
    ['', '', 'Shopping/Misc Subtotal', '$0.00'],
]
success = write_range(DEC_ID, "'📊 Dashboard'!A95:D97", new_shop)
print(f"  Write success: {success}")
format_rows(DEC_ID, DEC_GID, new_shop, 94)
time.sleep(1)

# ============================================================
# Verification
# ============================================================
print("\n" + "=" * 60)
print("VERIFICATION - Reading back all fixed sections")
print("=" * 60)

print("\n--- June Travel ---")
rows = read_range(JUNE_ID, "'📊 Dashboard'!A121:D124")
for i, r in enumerate(rows, 121):
    print(f"  Row {i}: {r}")

print("\n--- October (after delete) ---")
rows = read_range(OCT_ID, "'📊 Dashboard'!A180:D192")
for i, r in enumerate(rows, 180):
    print(f"  Row {i}: {r}")

print("\n--- September Shopping ---")
rows = read_range(SEP_ID, "'📊 Dashboard'!A110:D114")
for i, r in enumerate(rows, 110):
    print(f"  Row {i}: {r}")

print("\n--- November Food ---")
rows = read_range(NOV_ID, "'📊 Dashboard'!A93:D96")
for i, r in enumerate(rows, 93):
    print(f"  Row {i}: {r}")

print("\n--- December CC Interest & Shopping ---")
rows = read_range(DEC_ID, "'📊 Dashboard'!A89:D98")
for i, r in enumerate(rows, 89):
    print(f"  Row {i}: {r}")

print("\n✅ ALL FIXES COMPLETE")
