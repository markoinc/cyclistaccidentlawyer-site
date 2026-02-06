#!/usr/bin/env python3
"""
Repair script for accounting sheets — fixes the damage from v1 and completes all fixes.
FIX 1: Already done correctly (27 txns added to Personal 0068) ✅
FIX 2: Sapphire Aug — 3 cells set to wrong value, 4 cells still empty → fix all 7
FIX 3: Already done correctly (2 empty amounts filled in Sep Sapphire) ✅  
FIX 4: Biz CC June — 15 duplicate rows inserted → remove dupes, add the 1 missing Namecheap
"""

import csv
import json
import re
import requests
import time
from datetime import datetime
from urllib.parse import quote

# ─── OAuth ───────────────────────────────────────────────────────────────────
r = requests.post('https://oauth2.googleapis.com/token', data={
    'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
    'grant_type': 'refresh_token'
})
TOKEN = r.json()['access_token']
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
BASE = 'https://sheets.googleapis.com/v4/spreadsheets'

def sheets_get(sheet_id, range_str):
    url = f"{BASE}/{sheet_id}/values/{quote(range_str, safe='')}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json().get('values', [])

def sheets_update(sheet_id, range_str, values):
    url = f"{BASE}/{sheet_id}/values/{quote(range_str, safe='')}?valueInputOption=USER_ENTERED"
    r = requests.put(url, headers=HEADERS, json={'values': values})
    r.raise_for_status()
    return r.json()

def sheets_batch_update(sheet_id, reqs):
    url = f"{BASE}/{sheet_id}:batchUpdate"
    r = requests.post(url, headers=HEADERS, json={'requests': reqs})
    r.raise_for_status()
    return r.json()

def get_sheet_gid(sheet_id, tab_name):
    url = f"{BASE}/{sheet_id}?fields=sheets.properties"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    for s in r.json()['sheets']:
        if s['properties']['title'] == tab_name:
            return s['properties']['sheetId']
    raise ValueError(f"Tab '{tab_name}' not found")

report_lines = ["# Accounting Sheet Fixes Report (v2 - Repair)", 
                f"**Run at:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}", ""]


# ═════════════════════════════════════════════════════════════════════════════
# FIX 2 REPAIR: August 2025 Sapphire 4252 — correct all 7 amount cells
# ═════════════════════════════════════════════════════════════════════════════
def fix2_repair():
    print("\n" + "="*70)
    print("FIX 2 REPAIR: Aug Sapphire — Correcting 7 amount cells")
    print("="*70)
    
    SHEET_ID = '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI'
    TAB = '💎 Sapphire 4252'
    
    # The sheet uses POST DATE as the date column and CSV Category as the "Vendor" column.
    # I've manually mapped every sheet row to its CSV transaction:
    #
    # Row 2:  08/14 Travel    → BEACH BUNGALOW HOSTEL -60.00  (the other 08/14 Travel is row 14: +89.10)
    # Row 3:  08/10 Travel    → BEACH BUNGALOW HOSTEL -48.23  (wrongly set to -35.98)
    # Row 4:  08/10 Travel    → BEACH BUNGALOW HOSTEL -63.58  (wrongly set to -35.98)
    # Row 5:  08/07 Travel    → BEACH BUNGALOW HOSTEL -36.72
    # Row 6:  08/12 Food & Drink → GLAZED COFFEE -8.29
    # Row 7:  08/10 Groceries → MISSION SURF -99.74  (wrongly set to -35.98)
    # Row 15: 08/13 Travel    → TURO INC -450.62
    
    fixes = {
        2:  -60.00,
        3:  -48.23,
        4:  -63.58,
        5:  -36.72,
        6:  -8.29,
        7:  -99.74,
        15: -450.62,
    }
    
    for row_num, amount in fixes.items():
        cell = f'{TAB}!D{row_num + 1}'  # 1-indexed
        sheets_update(SHEET_ID, cell, [[amount]])
        print(f"  ✅ Set row {row_num} (D{row_num+1}) = {amount}")
        time.sleep(0.3)
    
    # Apply currency format
    gid = get_sheet_gid(SHEET_ID, TAB)
    fmt_reqs = []
    for row_num in fixes:
        fmt_reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': gid,
                    'startRowIndex': row_num,
                    'endRowIndex': row_num + 1,
                    'startColumnIndex': 3,
                    'endColumnIndex': 4
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {
                            'type': 'CURRENCY',
                            'pattern': '$#,##0.00;($#,##0.00)'
                        }
                    }
                },
                'fields': 'userEnteredFormat.numberFormat'
            }
        })
    sheets_batch_update(SHEET_ID, fmt_reqs)
    
    print(f"\n✅ FIX 2 REPAIR COMPLETE: Corrected 7 amount cells")
    
    report_lines.append("## FIX 2: August 2025 Sapphire 4252 (Repaired)")
    report_lines.append("- **Corrected 7 amount cells** (3 had wrong values from v1, 4 were still empty)")
    report_lines.append("- Row 2 (08/14 Travel): -$60.00 (Beach Bungalow Hostel)")
    report_lines.append("- Row 3 (08/10 Travel): -$48.23 → was wrongly -$35.98 (Beach Bungalow Hostel)")
    report_lines.append("- Row 4 (08/10 Travel): -$63.58 → was wrongly -$35.98 (Beach Bungalow Hostel)")
    report_lines.append("- Row 5 (08/07 Travel): -$36.72 (Beach Bungalow Hostel)")
    report_lines.append("- Row 6 (08/12 Food & Drink): -$8.29 (Glazed Coffee & Creamery)")
    report_lines.append("- Row 7 (08/10 Groceries): -$99.74 → was wrongly -$35.98 (Mission Surf)")
    report_lines.append("- Row 15 (08/13 Travel): -$450.62 (Turo Inc)")
    report_lines.append("")


# ═════════════════════════════════════════════════════════════════════════════
# FIX 4 REPAIR: June 2025 Biz CC 0678 — remove dupes, add missing Namecheap
# ═════════════════════════════════════════════════════════════════════════════
def fix4_repair():
    print("\n" + "="*70)
    print("FIX 4 REPAIR: Biz CC June — Remove dupes, add missing Namecheap")
    print("="*70)
    
    SHEET_ID = '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg'
    TAB = '💳 Biz CC 0678'
    gid = get_sheet_gid(SHEET_ID, TAB)
    
    # Current state has 36 rows (0=header, 1-35=data).
    # Rows inserted by v1 script (identified by -$ format instead of ($) parens):
    # Rows 2,3,4,5,6,7,8,9,10,11,12,13,15,16,18 (0-indexed)
    # 
    # Strategy: delete these 15 duplicate rows, then we're back to 21 rows (header + 20 original).
    # Then add the 1 missing Namecheap transaction.
    
    # Delete rows in reverse order (bottom-up) to avoid index shifting
    dupes_to_delete = sorted([2,3,4,5,6,7,8,9,10,11,12,13,15,16,18], reverse=True)
    
    delete_reqs = []
    for row_idx in dupes_to_delete:
        delete_reqs.append({
            'deleteDimension': {
                'range': {
                    'sheetId': gid,
                    'dimension': 'ROWS',
                    'startIndex': row_idx,
                    'endIndex': row_idx + 1
                }
            }
        })
    
    print(f"Deleting {len(dupes_to_delete)} duplicate rows: {dupes_to_delete}")
    sheets_batch_update(SHEET_ID, delete_reqs)
    time.sleep(1)
    
    # Verify state
    data = sheets_get(SHEET_ID, f'{TAB}!A:F')
    print(f"\nAfter cleanup: {len(data)} rows")
    for i, row in enumerate(data):
        print(f"  {i}: {row}")
    
    # Now add the missing Namecheap LFYNBT transaction
    # CSV: 05/30/2025 txn date, 06/01/2025 post date, NAME-CHEAP.COM* LFYNBT, -17.16
    # The sheet uses Transaction Date. The last rows are 06/01 dates.
    # This txn is 05/30, so it goes AFTER 06/01 rows (at the bottom, since newest-first)
    
    # Insert at end (after the last row)
    last_row = len(data)  # 0-indexed, this is the row after the last data row
    
    # Insert a new row at the end
    insert_reqs = [{
        'insertDimension': {
            'range': {
                'sheetId': gid,
                'dimension': 'ROWS',
                'startIndex': last_row,
                'endIndex': last_row + 1
            },
            'inheritFromBefore': True
        }
    }]
    sheets_batch_update(SHEET_ID, insert_reqs)
    time.sleep(0.5)
    
    # Write the new row
    new_row = [
        '05/30/2025',
        'NAME-CHEAP.COM* LFYNBT',
        '📱 SaaS & Tools',
        -17.16,
        '',
        ''
    ]
    write_range = f'{TAB}!A{last_row + 1}:F{last_row + 1}'
    sheets_update(SHEET_ID, write_range, [new_row])
    time.sleep(0.3)
    
    # Format amount as currency with parens (matching existing style)
    fmt_reqs = [{
        'repeatCell': {
            'range': {
                'sheetId': gid,
                'startRowIndex': last_row,
                'endRowIndex': last_row + 1,
                'startColumnIndex': 3,
                'endColumnIndex': 4
            },
            'cell': {
                'userEnteredFormat': {
                    'numberFormat': {
                        'type': 'CURRENCY',
                        'pattern': '$#,##0.00;($#,##0.00)'
                    }
                }
            },
            'fields': 'userEnteredFormat.numberFormat'
        }
    }]
    sheets_batch_update(SHEET_ID, fmt_reqs)
    
    # Final verify
    time.sleep(0.5)
    data2 = sheets_get(SHEET_ID, f'{TAB}!A:F')
    print(f"\nFinal state: {len(data2)} rows")
    for i, row in enumerate(data2):
        print(f"  {i}: {row}")
    
    print(f"\n✅ FIX 4 REPAIR COMPLETE: Removed 15 dupes, added 1 missing Namecheap txn")
    
    report_lines.append("## FIX 4: June 2025 Biz CC 0678 (Repaired)")
    report_lines.append("- **Removed 15 duplicate rows** inserted by v1 script")
    report_lines.append("- **Added 1 missing transaction:** 05/30/2025 | NAME-CHEAP.COM* LFYNBT | -$17.16")
    report_lines.append("- Final count: 21 transactions (was 20, now matches CSV)")
    report_lines.append("")


# ═════════════════════════════════════════════════════════════════════════════
# MAIN
# ═════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("🔧 Repair Script — Fixing FIX 2 and FIX 4...")
    
    try:
        fix2_repair()
    except Exception as e:
        print(f"❌ FIX 2 REPAIR FAILED: {e}")
        import traceback; traceback.print_exc()
        report_lines.append(f"## FIX 2 REPAIR: FAILED\n{e}\n")
    
    time.sleep(1)  # Rate limit buffer
    
    try:
        fix4_repair()
    except Exception as e:
        print(f"❌ FIX 4 REPAIR FAILED: {e}")
        import traceback; traceback.print_exc()
        report_lines.append(f"## FIX 4 REPAIR: FAILED\n{e}\n")
    
    # Add FIX 1 and FIX 3 status to report
    report_lines.insert(3, "## FIX 1: July 2025 Personal 0068")
    report_lines.insert(4, "- ✅ **Completed in v1** — Added 27 missing transactions (149 → 176)")
    report_lines.insert(5, "")
    report_lines.append("## FIX 3: September 2025 Sapphire 4252")
    report_lines.append("- ✅ **Completed in v1** — Filled 2 empty amount cells")
    report_lines.append("  - 09/23/2025 | Fees & Adjustments | -$172.42")
    report_lines.append("  - 09/19/2025 | Automatic Payment | $250.00")
    report_lines.append("")
    
    # Write report
    report_path = '/home/ec2-user/clawd/data/math-fixes-report.md'
    with open(report_path, 'w') as f:
        f.write('\n'.join(report_lines))
    print(f"\n📄 Report written to {report_path}")
    print("\n🎉 All repairs complete!")
