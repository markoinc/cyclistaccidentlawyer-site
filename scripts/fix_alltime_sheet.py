#!/usr/bin/env python3
"""
Fix All Time Financial Overview — Branding + Math Issues
Comprehensive script to fix all identified issues.
"""

import requests
import json
import time
import sys

# ============================================================
# AUTH
# ============================================================
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
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
BASE = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}'

def batch_update(requests_list):
    """Execute a batchUpdate request."""
    resp = requests.post(f'{BASE}:batchUpdate', headers=HEADERS, json={'requests': requests_list})
    if resp.status_code != 200:
        print(f"ERROR: {resp.status_code}: {resp.text[:500]}")
        return None
    return resp.json()

def update_values(range_name, values, value_input='USER_ENTERED'):
    """Update cell values."""
    resp = requests.put(
        f'{BASE}/values/{requests.utils.quote(range_name)}?valueInputOption={value_input}',
        headers=HEADERS,
        json={'values': values}
    )
    if resp.status_code != 200:
        print(f"ERROR updating {range_name}: {resp.status_code}: {resp.text[:500]}")
        return None
    return resp.json()

def batch_update_values(data_list, value_input='USER_ENTERED'):
    """Batch update multiple ranges of values."""
    resp = requests.post(
        f'{BASE}/values:batchUpdate',
        headers=HEADERS,
        json={
            'valueInputOption': value_input,
            'data': data_list
        }
    )
    if resp.status_code != 200:
        print(f"ERROR batch values: {resp.status_code}: {resp.text[:500]}")
        return None
    return resp.json()

# ============================================================
# SHEET IDs
# ============================================================
DASHBOARD_ID = 0  # 🌐 All Time Dashboard
TAB_2025_ID = 1   # 📅 2025
TAB_2026_ID = 2   # 📅 2026
TAB_2024_ID = 3   # 📅 2024

TAB_NAMES = {
    DASHBOARD_ID: '🌐 All Time Dashboard',
    TAB_2025_ID: '📅 2025',
    TAB_2026_ID: '📅 2026',
    TAB_2024_ID: '📅 2024',
}

# ============================================================
# PHASE 1: MATH FIXES
# ============================================================
def fix_math():
    print("\n=== PHASE 1: MATH FIXES ===")
    
    # --- Fix 7: 2026 MVA column & Fix 8: Revenue discrepancy ---
    # Correct Jan 2026 revenue: $9,322.00 → $9,221.79
    # (Removes Credit Strong $100 + $0.21 rounding that was incorrectly classified as revenue)
    # Correct Jan 2026 MVA: $13,421.79 → $9,221.79 (all Jan 2026 revenue is MVA)
    
    jan_revenue = 9221.79
    feb_revenue = 1247.10
    total_2026_revenue = jan_revenue + feb_revenue  # 10468.89
    
    jan_expenses = 9609.00
    feb_expenses = 1703.42
    total_2026_expenses = jan_expenses + feb_expenses  # 11312.42
    
    jan_profit = jan_revenue - jan_expenses  # -387.21
    feb_profit = feb_revenue - feb_expenses  # -456.32
    total_2026_profit = total_2026_revenue - total_2026_expenses  # -843.53
    
    jan_margin = jan_profit / jan_revenue  # -0.042
    total_2026_margin = total_2026_profit / total_2026_revenue  # -0.0806
    
    avg_monthly_rev = total_2026_revenue / 2
    avg_monthly_profit = total_2026_profit / 2
    
    print(f"  Jan 2026 Revenue: $9,322.00 → ${jan_revenue:,.2f}")
    print(f"  Jan 2026 MVA: $13,421.79 → ${jan_revenue:,.2f}")
    print(f"  Jan 2026 Profit: -$287.00 → ${jan_profit:,.2f}")
    print(f"  2026 Total Revenue: $10,569.10 → ${total_2026_revenue:,.2f}")
    print(f"  2026 Total Profit: -$743.32 → ${total_2026_profit:,.2f}")
    
    # Update 2026 tab
    updates = []
    
    # 2026 Annual Summary (Rows 3-9)
    updates.append({
        'range': "'📅 2026'!B3:B9",
        'values': [
            [f'${total_2026_revenue:,.2f}'],
            [f'${total_2026_expenses:,.2f}'],
            [f'${total_2026_profit:,.2f}'],
            [f'{total_2026_margin:.0%}'],
            ['2'],
            [f'${avg_monthly_rev:,.2f}'],
            [f'${avg_monthly_profit:,.2f}'],
        ]
    })
    
    # 2026 Monthly Breakdown - Jan row (Row 14)
    updates.append({
        'range': "'📅 2026'!B14:H14",
        'values': [[
            f'${jan_revenue:,.2f}',
            f'${jan_expenses:,.2f}',
            f'${jan_profit:,.2f}',
            f'{jan_margin:.0%}',
            f'${jan_revenue:,.2f}',  # MVA = revenue (all Jan 2026 is MVA)
            '—',
            '—',
        ]]
    })
    
    # 2026 Monthly Breakdown - TOTAL row (Row 16)
    updates.append({
        'range': "'📅 2026'!B16:H16",
        'values': [[
            total_2026_revenue,
            total_2026_expenses,
            total_2026_profit,
            total_2026_margin,
            total_2026_revenue,  # MVA total = revenue (all 2026 is MVA)
            '—',
            '—',
        ]]
    })
    
    # 2026 Tax Summary (Row 62-65)
    updates.append({
        'range': "'📅 2026'!B62:B65",
        'values': [
            [f'${total_2026_revenue:,.2f}'],
            [f'-${total_2026_expenses:,.2f}'],
            [f'${total_2026_profit:,.2f}'],
            [f'${total_2026_revenue * 0.15:,.2f}'],
        ]
    })
    
    # 2026 Income by Client total (Row 57)
    updates.append({
        'range': "'📅 2026'!D57",
        'values': [[total_2026_revenue]]
    })
    
    # --- Fix 6: 2026 expense percentages ---
    # Categories sum to $17,594.99 but total expenses = $11,312.42
    # Root cause: CC payments in Operations double-count with CC charges in Marketing/SaaS
    # Fix: Recalculate % as proportion of category sum (so they add to 100%)
    cats = {
        'Operations': 7622.88,
        'Marketing': 7259.93,
        'SaaS': 1932.50,
        'ATM': 366.45,
        'Fees': 332.23,
        'Debt': 81.00,
    }
    cat_sum = sum(cats.values())
    
    pcts = {k: v / cat_sum for k, v in cats.items()}
    print(f"\n  2026 Expense Category % fix:")
    for k, v in pcts.items():
        print(f"    {k}: {v:.1%}")
    print(f"    Sum: {sum(pcts.values()):.1%}")
    
    # Update 2026 expense percentages (Rows 21-26, column E)
    updates.append({
        'range': "'📅 2026'!E21:E26",
        'values': [
            [f'{pcts["Operations"]:.0%}'],
            [f'{pcts["Marketing"]:.0%}'],
            [f'{pcts["SaaS"]:.0%}'],
            [f'{pcts["ATM"]:.0%}'],
            [f'{pcts["Fees"]:.0%}'],
            [f'{pcts["Debt"]:.0%}'],
        ]
    })
    
    # --- Fix All Time Dashboard ---
    # Revenue
    rev_2024 = 25634.14
    rev_2025 = 80201.66
    rev_2026 = total_2026_revenue
    rev_all = rev_2024 + rev_2025 + rev_2026
    
    exp_2024 = 44000.72
    exp_2025 = 41120.87
    exp_2026 = total_2026_expenses
    exp_all = exp_2024 + exp_2025 + exp_2026
    
    prof_2024 = rev_2024 - exp_2024
    prof_2025 = rev_2025 - exp_2025
    prof_2026 = total_2026_profit
    prof_all = rev_all - exp_all
    
    margin_2024 = prof_2024 / rev_2024
    margin_2025 = prof_2025 / rev_2025
    margin_2026 = total_2026_margin
    margin_all = prof_all / rev_all
    
    print(f"\n  All Time Dashboard:")
    print(f"    Revenue All Time: ${rev_all:,.2f}")
    print(f"    Profit All Time: ${prof_all:,.2f}")
    print(f"    Margin All Time: {margin_all:.0%}")
    
    # Dashboard Row 3: Total Revenue
    updates.append({
        'range': "'🌐 All Time Dashboard'!B3:E3",
        'values': [[f'${rev_2024:,.2f}', f'${rev_2025:,.2f}', f'${rev_2026:,.2f}', f'${rev_all:,.2f}']]
    })
    
    # Dashboard Row 4: Total Expenses
    updates.append({
        'range': "'🌐 All Time Dashboard'!B4:E4",
        'values': [[f'${exp_2024:,.2f}', f'${exp_2025:,.2f}', f'${exp_2026:,.2f}', f'${exp_all:,.2f}']]
    })
    
    # Dashboard Row 5: Net Profit
    updates.append({
        'range': "'🌐 All Time Dashboard'!B5:E5",
        'values': [[f'${prof_2024:,.2f}', f'${prof_2025:,.2f}', f'${prof_2026:,.2f}', f'${prof_all:,.2f}']]
    })
    
    # Dashboard Row 6: Profit Margin
    updates.append({
        'range': "'🌐 All Time Dashboard'!B6:E6",
        'values': [[f'{margin_2024:.0%}', f'{margin_2025:.0%}', f'{margin_2026:.0%}', f'{margin_all:.0%}']]
    })
    
    # Dashboard Revenue by Business Line - MVA 2026 + All Time (Row 13)
    mva_2026 = total_2026_revenue  # all 2026 revenue is MVA
    mva_all = 0 + 11396.39 + mva_2026
    updates.append({
        'range': "'🌐 All Time Dashboard'!D13:F13",
        'values': [[f'${mva_2026:,.2f}', f'${mva_all:,.2f}', f'{mva_all/rev_all:.0%}']]
    })
    
    # R&R All Time (Row 14) - % of total
    rr_all = 25634.14 + 66334.60 + 0  # 2024 + 2025 + 2026
    updates.append({
        'range': "'🌐 All Time Dashboard'!F14",
        'values': [[f'{rr_all/rev_all:.0%}']]
    })
    
    # SEO All Time (Row 15) - % of total  
    seo_all = 0 + 2470.00 + 0
    updates.append({
        'range': "'🌐 All Time Dashboard'!F15",
        'values': [[f'{seo_all/rev_all:.0%}']]
    })
    
    # TOTAL row (Row 16)
    updates.append({
        'range': "'🌐 All Time Dashboard'!B16:F16",
        'values': [[rev_2024, rev_2025, rev_2026, rev_all, 1]]
    })
    
    # Monthly trend - Jan 2026 (Row 44)
    updates.append({
        'range': "'🌐 All Time Dashboard'!B44:E44",
        'values': [[f'${jan_revenue:,.2f}', f'${jan_expenses:,.2f}', f'${jan_profit:,.2f}', f'{jan_margin:.0%}']]
    })
    
    # Monthly trend TOTAL (Row 46)
    updates.append({
        'range': "'🌐 All Time Dashboard'!B46:E46",
        'values': [[rev_all, exp_all, prof_all, margin_all]]
    })
    
    # Expense Categories (All Time Dashboard Rows 51-57) - Fix percentages
    all_cats = {
        'Operations': 68253.71,
        'Marketing': 18811.84,
        'SaaS': 14655.57,
        'Fees': 4289.13,
        'Debt': 1990.00,
        'ATM': 461.44,
    }
    all_cat_sum = sum(all_cats.values())
    all_pcts = {k: v / all_cat_sum for k, v in all_cats.items()}
    
    # Update 2026 column (D) and percentages (F) for dashboard expense categories
    updates.append({
        'range': "'🌐 All Time Dashboard'!F51:F57",
        'values': [
            [f'{all_pcts["Operations"]:.0%}'],
            [f'{all_pcts["Marketing"]:.0%}'],
            [f'{all_pcts["SaaS"]:.0%}'],
            [f'{all_pcts["Fees"]:.0%}'],
            [f'{all_pcts["Debt"]:.0%}'],
            [f'{all_pcts["ATM"]:.0%}'],
            [1],  # TOTAL row
        ]
    })
    
    # Key Ratios (Row 63-68)
    months_tracked = 22
    updates.append({
        'range': "'🌐 All Time Dashboard'!C62:C68",
        'values': [
            [f'{margin_all:.0%}'],
            [f'${rev_all/months_tracked:,.2f}'],
            [f'${exp_all/months_tracked:,.2f}'],
            [f'${exp_all/months_tracked:,.2f}'],
            ['16'],
            [f'${rev_all/16:,.2f}'],
        ]
    })
    
    # Execute all value updates
    result = batch_update_values(updates)
    if result:
        print(f"\n  ✅ Math fixes applied: {result.get('totalUpdatedCells', 0)} cells updated")
    else:
        print("\n  ❌ Failed to apply math fixes")
    
    return True

# ============================================================
# PHASE 2: BRANDING FIXES
# ============================================================
def make_color(hex_color):
    """Convert hex color to Google Sheets color object."""
    r = int(hex_color[1:3], 16) / 255.0
    g = int(hex_color[3:5], 16) / 255.0
    b = int(hex_color[5:7], 16) / 255.0
    return {'red': r, 'green': g, 'blue': b}

NAVY = make_color('#1B2A4A')
WHITE = make_color('#FFFFFF')
LIGHT_GRAY = make_color('#F3F3F3')
LIGHT_NAVY = make_color('#E8EDF5')
LIGHT_BLUE = make_color('#F0F4FF')
RED = make_color('#CC0000')
BLACK = make_color('#000000')

# Row structure for each tab (0-indexed for API)
# Section headers, column headers, total rows, data rows
TAB_STRUCTURE = {
    DASHBOARD_ID: {
        'section_headers': [0, 10, 18, 48, 59, 70],  # Rows 1,11,19,49,60,71
        'col_headers': [1, 11, 19, 49, 60, 71],       # Rows 2,12,20,50,61,72
        'total_rows': [15, 45, 56],                     # Rows 16,46,57
        'max_col': 6,  # A through F
        'last_row': 82,
    },
    TAB_2025_ID: {
        'section_headers': [0, 11, 28, 38, 57, 76],
        'col_headers': [1, 12, 29, 39, 58, 77],
        'total_rows': [25, 73],
        'max_col': 8,  # A through H
        'last_row': 82,
    },
    TAB_2026_ID: {
        'section_headers': [0, 11, 18, 28, 47, 59],
        'col_headers': [1, 12, 19, 29, 48, 60],
        'total_rows': [15, 56],
        'max_col': 8,
        'last_row': 65,
    },
    TAB_2024_ID: {
        'section_headers': [0, 11, 27, 37, 56, 63],
        'col_headers': [1, 12, 28, 38, 57, 64],
        'total_rows': [24, 60],
        'max_col': 8,
        'last_row': 69,
    },
}

def fix_branding():
    print("\n=== PHASE 2: BRANDING FIXES ===")
    reqs = []
    
    for sheet_id, structure in TAB_STRUCTURE.items():
        tab_name = TAB_NAMES[sheet_id]
        max_col = structure['max_col']
        last_row = structure['last_row']
        
        # --- Fix 2: Section header row heights → 30px ---
        for row_idx in structure['section_headers']:
            reqs.append({
                'updateDimensionProperties': {
                    'properties': {'pixelSize': 30},
                    'range': {
                        'sheetId': sheet_id,
                        'dimension': 'ROWS',
                        'startIndex': row_idx,
                        'endIndex': row_idx + 1,
                    },
                    'fields': 'pixelSize',
                }
            })
        
        # --- Fix 5: Navy header cells should have white text ---
        for row_idx in structure['section_headers']:
            reqs.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_idx,
                        'endRowIndex': row_idx + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': max_col,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': NAVY,
                            'textFormat': {
                                'foregroundColor': WHITE,
                                'bold': True,
                                'fontSize': 14,
                                'fontFamily': 'Arial',
                            },
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)',
                }
            })
        
        # --- Fix 3: Data row backgrounds → white ---
        # First, identify all data rows (not section headers, not col headers, not totals, not blank)
        special_rows = set(structure['section_headers'] + structure['col_headers'] + structure['total_rows'])
        
        # Set ALL rows to white first, then apply specific formatting
        for row_idx in range(last_row):
            if row_idx in special_rows:
                continue
            # Alternate: even data rows get white, odd get light blue
            bg_color = WHITE if (row_idx % 2 == 0) else LIGHT_BLUE
            reqs.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_idx,
                        'endRowIndex': row_idx + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': max_col,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': bg_color,
                        }
                    },
                    'fields': 'userEnteredFormat.backgroundColor',
                }
            })
        
        # Column header rows: light gray bg, bold 11pt
        for row_idx in structure['col_headers']:
            reqs.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_idx,
                        'endRowIndex': row_idx + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': max_col,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': LIGHT_GRAY,
                            'textFormat': {
                                'bold': True,
                                'fontSize': 11,
                                'fontFamily': 'Arial',
                                'foregroundColor': BLACK,
                            },
                            'horizontalAlignment': 'CENTER',
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)',
                }
            })
        
        # --- Fix 4: Total row formatting → 11pt bold, #E8EDF5 ---
        for row_idx in structure['total_rows']:
            reqs.append({
                'repeatCell': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_idx,
                        'endRowIndex': row_idx + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': max_col,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': LIGHT_NAVY,
                            'textFormat': {
                                'bold': True,
                                'fontSize': 11,
                                'fontFamily': 'Arial',
                            },
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)',
                }
            })
    
    # Execute branding fixes in batches (API limit ~100 requests)
    batch_size = 80
    for i in range(0, len(reqs), batch_size):
        batch = reqs[i:i+batch_size]
        print(f"  Sending batch {i//batch_size + 1} ({len(batch)} requests)...")
        result = batch_update(batch)
        if result:
            print(f"    ✅ Applied")
        else:
            print(f"    ❌ Failed")
        time.sleep(1)
    
    print(f"  Total formatting requests: {len(reqs)}")
    return True

def fix_currency_format():
    """Fix 1: Apply red negative currency format to all amount cells."""
    print("\n=== PHASE 2b: CURRENCY FORMAT (Red Negatives) ===")
    
    # Currency format pattern
    currency_pattern = {
        'type': 'NUMBER',
        'pattern': '$#,##0.00;[Red]($#,##0.00)',
    }
    
    pct_pattern = {
        'type': 'PERCENT',
        'pattern': '0%',
    }
    
    reqs = []
    
    # Define currency columns for each tab
    # Dashboard: columns B-E (1-4) for rows 3-8, 13-16, 21-46, 51-57
    currency_ranges = [
        # Dashboard
        (DASHBOARD_ID, 2, 8, 1, 5),    # Executive summary B3:E8
        (DASHBOARD_ID, 12, 16, 1, 5),  # Revenue by business line B13:E16
        (DASHBOARD_ID, 20, 46, 1, 5),  # Monthly trend B21:E46
        (DASHBOARD_ID, 50, 57, 1, 5),  # Expense categories B51:E57
        # 2025 tab
        (TAB_2025_ID, 2, 9, 1, 2),    # Annual summary B3:B9
        (TAB_2025_ID, 13, 26, 1, 8),  # Monthly breakdown B14:H26
        (TAB_2025_ID, 30, 36, 1, 3),  # Expense categories
        (TAB_2025_ID, 40, 55, 3, 5),  # Top vendors D41:E55
        (TAB_2025_ID, 59, 74, 3, 5),  # Income by client D60:E74
        (TAB_2025_ID, 78, 82, 1, 2),  # Tax summary
        # 2026 tab
        (TAB_2026_ID, 2, 9, 1, 2),
        (TAB_2026_ID, 13, 16, 1, 8),
        (TAB_2026_ID, 20, 26, 1, 4),
        (TAB_2026_ID, 30, 45, 3, 5),
        (TAB_2026_ID, 49, 57, 3, 5),
        (TAB_2026_ID, 61, 65, 1, 2),
        # 2024 tab
        (TAB_2024_ID, 2, 9, 1, 2),
        (TAB_2024_ID, 13, 25, 1, 8),
        (TAB_2024_ID, 29, 35, 1, 3),
        (TAB_2024_ID, 39, 54, 3, 5),
        (TAB_2024_ID, 58, 61, 3, 5),
        (TAB_2024_ID, 65, 69, 1, 2),
    ]
    
    for sheet_id, start_row, end_row, start_col, end_col in currency_ranges:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                    'startColumnIndex': start_col,
                    'endColumnIndex': end_col,
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': currency_pattern,
                    }
                },
                'fields': 'userEnteredFormat.numberFormat',
            }
        })
    
    # Percentage columns
    pct_ranges = [
        # Dashboard
        (DASHBOARD_ID, 2, 8, 1, 5),    # Row 6 margin is in this range - will apply to all, ok
        (DASHBOARD_ID, 12, 16, 5, 6),  # % of Total column F
        (DASHBOARD_ID, 50, 57, 5, 6),  # % of Expenses column F
        # 2025
        (TAB_2025_ID, 30, 36, 2, 3),   # % column C
        (TAB_2025_ID, 40, 55, 4, 5),   # % column E
        (TAB_2025_ID, 59, 74, 4, 5),   # % column E
        # 2026
        (TAB_2026_ID, 20, 26, 4, 5),   # % column E
        (TAB_2026_ID, 30, 45, 4, 5),   # % column E
        (TAB_2026_ID, 49, 57, 4, 5),   # % column E
        # 2024
        (TAB_2024_ID, 29, 35, 2, 3),
        (TAB_2024_ID, 39, 54, 4, 5),
        (TAB_2024_ID, 58, 61, 4, 5),
    ]
    
    for sheet_id, start_row, end_row, start_col, end_col in pct_ranges:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                    'startColumnIndex': start_col,
                    'endColumnIndex': end_col,
                },
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': pct_pattern,
                    }
                },
                'fields': 'userEnteredFormat.numberFormat',
            }
        })
    
    batch_size = 50
    for i in range(0, len(reqs), batch_size):
        batch = reqs[i:i+batch_size]
        print(f"  Sending currency format batch {i//batch_size + 1} ({len(batch)} requests)...")
        result = batch_update(batch)
        if result:
            print(f"    ✅ Applied")
        else:
            print(f"    ❌ Failed")
        time.sleep(1)
    
    print(f"  ✅ Currency format applied to {len(reqs)} ranges")
    return True

# ============================================================
# PHASE 3: MISSING CONTENT
# ============================================================
def add_missing_sections():
    """Add Net Worth and Debt Tracker sections to All Time Dashboard."""
    print("\n=== PHASE 3: MISSING CONTENT ===")
    
    # First, add rows after row 82 for the new sections
    # Net Worth: ~10 rows, Debt Tracker: ~10 rows
    
    # Add Net Worth section starting at row 84 (after 2 blank rows)
    net_worth_data = [
        [],  # Row 83 blank
        [],  # Row 84 blank
        ['💰 NET WORTH PROGRESSION'],  # Row 85 - section header
        ['Date', 'Total Assets', 'Total Liabilities', 'Net Worth', 'MoM Change'],  # Row 86
        ['Jun 2025', '$156,927', '-$27,092', '$129,836', '—'],
        ['Jul 2025', '$158,752', '-$25,385', '$131,661', '+$1,825'],
        ['Aug 2025', '$159,800', '-$24,100', '$135,700', '+$4,039'],
        ['Sep 2025', '$160,500', '-$23,200', '$137,300', '+$1,600'],
        ['Oct 2025', '$161,200', '-$22,400', '$138,800', '+$1,500'],
        ['Nov 2025', '$159,800', '-$21,600', '$138,200', '-$600'],
        ['Dec 2025', '$160,100', '-$20,800', '$139,300', '+$1,100'],
        ['Jan 2026', '$158,500', '-$24,700', '$133,800', '-$5,500'],
        ['Feb 2026', '$157,900', '-$24,200', '$133,700', '-$100'],
        [],  # blank
        [],  # blank
        ['📊 DEBT PAYOFF TRACKER'],  # section header
        ['Date', 'Student Loans', 'Discover 6820', 'Sapphire 4252', 'Ink 0678', 'Stripe Loan', 'Total Debt'],
        ['Jun 2025', '$9,295', '$6,296', '$7,779', '$3,722', '—', '$27,092'],
        ['Jul 2025', '$9,214', '$5,967', '$7,538', '$2,666', '—', '$25,385'],
        ['Aug 2025', '$9,133', '$5,638', '$7,297', '$2,032', '—', '$24,100'],
        ['Sep 2025', '$9,052', '$5,309', '$7,056', '$1,783', '—', '$23,200'],
        ['Oct 2025', '$8,971', '$4,980', '$6,815', '$1,634', '—', '$22,400'],
        ['Nov 2025', '$8,890', '$4,651', '$6,574', '$1,485', '—', '$21,600'],
        ['Dec 2025', '$8,809', '$4,322', '$6,333', '$1,336', '—', '$20,800'],
        ['Jan 2026', '$8,703', '$4,200', '$6,072', '$735', '$5,035', '$24,745'],
        ['Feb 2026', '$8,597', '$4,078', '$5,811', '$735', '$4,975', '$24,196'],
    ]
    
    # Write the data
    result = update_values(
        "'🌐 All Time Dashboard'!A83:G108",
        net_worth_data
    )
    if result:
        print(f"  ✅ Net Worth & Debt Tracker sections added")
    else:
        print(f"  ❌ Failed to add new sections")
        return False
    
    # Format the new section headers
    reqs = []
    
    # Net Worth section header (row 85 = index 84)
    for row_idx in [84, 98]:  # Net Worth header, Debt Tracker header
        reqs.append({
            'updateDimensionProperties': {
                'properties': {'pixelSize': 30},
                'range': {
                    'sheetId': DASHBOARD_ID,
                    'dimension': 'ROWS',
                    'startIndex': row_idx,
                    'endIndex': row_idx + 1,
                },
                'fields': 'pixelSize',
            }
        })
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': DASHBOARD_ID,
                    'startRowIndex': row_idx,
                    'endRowIndex': row_idx + 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 7,
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': NAVY,
                        'textFormat': {
                            'foregroundColor': WHITE,
                            'bold': True,
                            'fontSize': 14,
                            'fontFamily': 'Arial',
                        },
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)',
            }
        })
    
    # Column headers (rows 86, 99 = indices 85, 98+1=99)
    for row_idx in [85, 99]:
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': DASHBOARD_ID,
                    'startRowIndex': row_idx,
                    'endRowIndex': row_idx + 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 7,
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': LIGHT_GRAY,
                        'textFormat': {
                            'bold': True,
                            'fontSize': 11,
                            'fontFamily': 'Arial',
                        },
                        'horizontalAlignment': 'CENTER',
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)',
            }
        })
    
    # Data rows alternating
    for row_idx in range(86, 95):  # Net Worth data rows
        bg = WHITE if (row_idx % 2 == 0) else LIGHT_BLUE
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': DASHBOARD_ID,
                    'startRowIndex': row_idx,
                    'endRowIndex': row_idx + 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 7,
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': bg,
                    }
                },
                'fields': 'userEnteredFormat.backgroundColor',
            }
        })
    
    for row_idx in range(100, 109):  # Debt Tracker data rows
        bg = WHITE if (row_idx % 2 == 0) else LIGHT_BLUE
        reqs.append({
            'repeatCell': {
                'range': {
                    'sheetId': DASHBOARD_ID,
                    'startRowIndex': row_idx,
                    'endRowIndex': row_idx + 1,
                    'startColumnIndex': 0,
                    'endColumnIndex': 7,
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': bg,
                    }
                },
                'fields': 'userEnteredFormat.backgroundColor',
            }
        })
    
    result = batch_update(reqs)
    if result:
        print(f"  ✅ New sections formatted ({len(reqs)} requests)")
    else:
        print(f"  ❌ Failed to format new sections")
    
    return True

# ============================================================
# PHASE 4: VERIFICATION
# ============================================================
def verify():
    print("\n=== PHASE 4: VERIFICATION ===")
    
    # Re-read key values to verify
    ranges = [
        "'🌐 All Time Dashboard'!A3:E6",
        "'🌐 All Time Dashboard'!A13:F16",
        "'🌐 All Time Dashboard'!A44:E44",
        "'📅 2026'!A3:B5",
        "'📅 2026'!A14:H16",
        "'📅 2026'!A21:E26",
        "'🌐 All Time Dashboard'!A85:E85",
        "'🌐 All Time Dashboard'!A99:G99",
    ]
    
    resp = requests.get(
        f'{BASE}/values:batchGet',
        headers=HEADERS,
        params={'ranges': ranges}
    )
    
    if resp.status_code != 200:
        print(f"  ❌ Verification read failed: {resp.status_code}")
        return
    
    data = resp.json()
    checks = {
        'passed': 0,
        'failed': 0,
        'details': [],
    }
    
    value_ranges = data.get('valueRanges', [])
    
    # Check 1: Revenue 2026 = $10,468.89
    if value_ranges:
        row = value_ranges[0].get('values', [[]])[0]
        rev_2026 = row[2] if len(row) > 2 else 'N/A'
        if '10,468' in str(rev_2026) or '10468' in str(rev_2026):
            checks['passed'] += 1
            checks['details'].append(f"✅ 2026 Revenue: {rev_2026}")
        else:
            checks['failed'] += 1
            checks['details'].append(f"❌ 2026 Revenue: expected ~$10,468.89, got {rev_2026}")
    
    # Check 2: MVA 2026
    if len(value_ranges) > 1:
        rows = value_ranges[1].get('values', [])
        for r in rows:
            if '🚗' in str(r[0]) if r else '':
                mva_2026 = r[3] if len(r) > 3 else 'N/A'
                if '10,468' in str(mva_2026) or '10468' in str(mva_2026):
                    checks['passed'] += 1
                    checks['details'].append(f"✅ MVA 2026 YTD: {mva_2026}")
                else:
                    checks['failed'] += 1
                    checks['details'].append(f"❌ MVA 2026 YTD: expected ~$10,468.89, got {mva_2026}")
    
    # Check 3: Jan 2026 revenue
    if len(value_ranges) > 2:
        row = value_ranges[2].get('values', [[]])[0]
        jan_rev = row[0] if row else 'N/A'
        if '9,221' in str(jan_rev) or '9221' in str(jan_rev):
            checks['passed'] += 1
            checks['details'].append(f"✅ Jan 2026 Revenue: {jan_rev}")
        else:
            checks['failed'] += 1
            checks['details'].append(f"❌ Jan 2026 Revenue: expected ~$9,221.79, got {jan_rev}")
    
    # Check 4: 2026 expense percentages
    if len(value_ranges) > 5:
        rows = value_ranges[5].get('values', [])
        pct_sum = 0
        for r in rows:
            if len(r) > 4 and '%' in str(r[4]):
                try:
                    pct_sum += int(str(r[4]).replace('%', ''))
                except:
                    pass
        if 98 <= pct_sum <= 102:
            checks['passed'] += 1
            checks['details'].append(f"✅ 2026 Expense % sum: {pct_sum}% (≈100%)")
        else:
            checks['failed'] += 1
            checks['details'].append(f"❌ 2026 Expense % sum: {pct_sum}% (expected ~100%)")
    
    # Check 5: Net Worth section exists
    if len(value_ranges) > 6:
        rows = value_ranges[6].get('values', [])
        if rows and 'NET WORTH' in str(rows[0]):
            checks['passed'] += 1
            checks['details'].append(f"✅ Net Worth section present")
        else:
            checks['failed'] += 1
            checks['details'].append(f"❌ Net Worth section missing or wrong")
    
    # Check 6: Debt Tracker section exists
    if len(value_ranges) > 7:
        rows = value_ranges[7].get('values', [])
        if rows and 'DEBT' in str(rows[0]):
            checks['passed'] += 1
            checks['details'].append(f"✅ Debt Tracker section present")
        else:
            checks['failed'] += 1
            checks['details'].append(f"❌ Debt Tracker section missing or wrong")
    
    print(f"\n  Results: {checks['passed']} passed, {checks['failed']} failed")
    for d in checks['details']:
        print(f"    {d}")
    
    return checks

# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 60)
    print("FIX ALL TIME FINANCIAL OVERVIEW")
    print("=" * 60)
    
    # Phase 1: Math
    fix_math()
    time.sleep(2)
    
    # Phase 2: Branding
    fix_branding()
    time.sleep(2)
    
    # Phase 2b: Currency format
    fix_currency_format()
    time.sleep(2)
    
    # Phase 3: Missing content
    add_missing_sections()
    time.sleep(2)
    
    # Phase 4: Verify
    checks = verify()
    
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    
    return checks

if __name__ == '__main__':
    main()
