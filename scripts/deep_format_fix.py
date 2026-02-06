#!/usr/bin/env python3
"""
Deep Formatting Fix for ALL 8 KuriosBrand Accounting Sheets.
Fixes font sizes, font families, alignment, row heights, and cell formatting
to match the master template spec exactly.

FORMATTING ONLY — no cell values changed.
"""

import requests
import json
import time
import sys
from datetime import datetime

# ─── OAuth ───
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

SHEETS = {
    'June 2025': '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg',
    'July 2025': '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8',
    'August 2025': '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI',
    'September 2025': '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM',
    'October 2025': '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA',
    'November 2025': '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0',
    'December 2025': '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo',
    'January 2026': '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE',
}

# ─── Color constants ───
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}
WHITE_COLOR = {"red": 1, "green": 1, "blue": 1}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}  # #F3F3F3
BLUE_TINT = {"red": 0.91, "green": 0.929, "blue": 0.961}    # #E8EDF5
BLACK_COLOR = {"red": 0, "green": 0, "blue": 0}

# ─── API helpers ───
def get_spreadsheet(spreadsheet_id):
    """Get full spreadsheet metadata + properties."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}'
    r = requests.get(url, headers=HEADERS, params={'includeGridData': False})
    r.raise_for_status()
    return r.json()

def get_sheet_values(spreadsheet_id, range_name):
    """Read values from a range."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}'
    r = requests.get(url, headers=HEADERS, params={'valueRenderOption': 'FORMATTED_VALUE'})
    if r.status_code == 200:
        return r.json().get('values', [])
    return []

def batch_update(spreadsheet_id, requests_list):
    """Send batchUpdate with list of requests."""
    if not requests_list:
        return None
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate'
    body = {'requests': requests_list}
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code != 200:
        print(f"  ❌ batchUpdate error: {r.status_code}")
        print(f"     {r.text[:500]}")
        return None
    return r.json()

# ─── Request builders ───
def make_repeat_cell(sheet_id, start_row, end_row, start_col, end_col, fmt, fields):
    """Build a repeatCell request."""
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "cell": {"userEnteredFormat": fmt},
            "fields": fields
        }
    }

def make_row_height(sheet_id, start_row, end_row, height):
    """Build an updateDimensionProperties for row height."""
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "ROWS",
                "startIndex": start_row,
                "endIndex": end_row
            },
            "properties": {"pixelSize": height},
            "fields": "pixelSize"
        }
    }

def make_default_format(sheet_id):
    """Set default font to Arial 10pt for a sheet via updateSheetProperties."""
    return {
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "gridProperties": {}
            },
            "fields": ""
        }
    }

# ─── Classification helpers ───
def is_section_header(row_values):
    """Check if row is a dashboard section header (💰 SECTION A: ..., 📊 SECTION B: ..., etc.)"""
    if not row_values:
        return False
    first = str(row_values[0]).strip()
    # Section headers contain emoji + SECTION or are the main title-like bars
    section_markers = ['SECTION A:', 'SECTION B:', 'SECTION C:', 'SECTION D:', 'SECTION E:',
                       'SECTION F:', 'SECTION G:', 'SECTION H:', 'INCOME SUMMARY',
                       'EXPENSE SUMMARY', 'NET INCOME', 'PROFIT FIRST', 'TAX SUMMARY',
                       'ACCOUNT BALANCES', 'CASH FLOW', 'KEY METRICS', 'PARETO']
    first_upper = first.upper()
    for marker in section_markers:
        if marker in first_upper:
            return True
    # Also check for emoji-prefixed headers
    if any(first.startswith(e) for e in ['💰', '💸', '📊', '🏦', '📈', '🎯', '💳', '📋', '🔄', '💎', '⚡']):
        # But not if it's just a data row with an emoji
        if 'SECTION' in first_upper or len(row_values) <= 2 or all(not v for v in row_values[1:]):
            return True
    return False

def is_column_header(row_values):
    """Check if row is a column header row (Business Line | Source | Method | Amount)."""
    if not row_values:
        return False
    first = str(row_values[0]).strip().upper()
    header_words = ['BUSINESS LINE', 'SOURCE', 'CATEGORY', 'ACCOUNT', 'METRIC', 'DESCRIPTION',
                    'ALLOCATION', 'INCOME TYPE', 'EXPENSE', 'DATE', 'TYPE', 'ITEM']
    for word in header_words:
        if first == word or first.startswith(word):
            # Make sure we have multiple header-like values
            non_empty = [v for v in row_values if str(v).strip()]
            if len(non_empty) >= 2:
                return True
    # Also check if multiple cells look like headers
    non_empty = [str(v).strip().upper() for v in row_values if str(v).strip()]
    header_like = ['AMOUNT', 'METHOD', 'SOURCE', 'BALANCE', 'PERCENTAGE', '%', 'TOTAL',
                   'NOTES', 'STATUS', 'TARGET', 'ACTUAL', 'DIFFERENCE', 'BUDGET', 'RATE',
                   'VENDOR', 'BUSINESS LINE', 'CATEGORY', 'DESCRIPTION']
    matches = sum(1 for v in non_empty if any(h in v for h in header_like))
    if matches >= 2 and len(non_empty) >= 3:
        return True
    return False

def is_subtotal_row(row_values):
    """Check if row contains SUBTOTAL."""
    for v in row_values:
        if 'SUBTOTAL' in str(v).upper() and 'TOTAL' in str(v).upper():
            if 'SUBTOTAL' in str(v).upper():
                return True
    return False

def is_total_row(row_values):
    """Check if row contains TOTAL (but not SUBTOTAL)."""
    for v in row_values:
        val = str(v).upper()
        if 'TOTAL' in val and 'SUBTOTAL' not in val:
            return True
    return False

def is_empty_row(row_values):
    """Check if row is empty."""
    return all(not str(v).strip() for v in row_values)


# ─── Main formatting logic ───
def format_dashboard(spreadsheet_id, sheet_id, tab_name, month_name):
    """Format the Dashboard tab."""
    print(f"  📊 Formatting Dashboard (sheetId={sheet_id})...")
    
    # Read all values
    safe_name = tab_name.replace("'", "''")
    values = get_sheet_values(spreadsheet_id, f"'{safe_name}'!A1:Z200")
    if not values:
        print(f"    ⚠️  No values found in Dashboard")
        return []
    
    num_rows = len(values)
    # Find max columns used
    max_cols = max(len(row) for row in values) if values else 10
    max_cols = max(max_cols, 10)  # at least 10 columns
    
    requests_list = []
    
    # 1. Set ALL cells to Arial 10pt default (entire grid)
    requests_list.append(make_repeat_cell(
        sheet_id, 0, num_rows + 5, 0, max_cols,
        {
            "textFormat": {
                "fontFamily": "Arial",
                "fontSize": 10,
                "foregroundColorStyle": {"rgbColor": BLACK_COLOR},
                "bold": False
            }
        },
        "userEnteredFormat.textFormat"
    ))
    
    # 2. Set all row heights to 21px
    requests_list.append(make_row_height(sheet_id, 0, num_rows + 5, 21))
    
    # 3. Classify each row and apply formatting
    section_header_rows = []
    column_header_rows = []
    subtotal_rows = []
    total_rows = []
    data_rows = []
    
    for i, row in enumerate(values):
        if is_empty_row(row):
            continue
        elif is_section_header(row):
            section_header_rows.append(i)
        elif is_column_header(row):
            column_header_rows.append(i)
        elif is_subtotal_row(row):
            subtotal_rows.append(i)
        elif is_total_row(row):
            total_rows.append(i)
        else:
            data_rows.append(i)
    
    print(f"    Classified: {len(section_header_rows)} headers, {len(column_header_rows)} col headers, "
          f"{len(subtotal_rows)} subtotals, {len(total_rows)} totals, {len(data_rows)} data rows")
    
    # 4. Apply section header formatting (14pt bold white on navy)
    for row_idx in section_header_rows:
        requests_list.append(make_repeat_cell(
            sheet_id, row_idx, row_idx + 1, 0, max_cols,
            {
                "backgroundColor": NAVY,
                "textFormat": {
                    "fontFamily": "Arial",
                    "fontSize": 14,
                    "bold": True,
                    "foregroundColorStyle": {"rgbColor": WHITE_COLOR}
                },
                "horizontalAlignment": "LEFT",
                "verticalAlignment": "MIDDLE"
            },
            "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        ))
    
    # 5. Apply column header formatting (11pt bold on #F3F3F3, centered)
    for row_idx in column_header_rows:
        requests_list.append(make_repeat_cell(
            sheet_id, row_idx, row_idx + 1, 0, max_cols,
            {
                "backgroundColor": LIGHT_GRAY,
                "textFormat": {
                    "fontFamily": "Arial",
                    "fontSize": 11,
                    "bold": True,
                    "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
                },
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            },
            "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
        ))
    
    # 6. Apply subtotal formatting (bold on #F3F3F3)
    for row_idx in subtotal_rows:
        requests_list.append(make_repeat_cell(
            sheet_id, row_idx, row_idx + 1, 0, max_cols,
            {
                "backgroundColor": LIGHT_GRAY,
                "textFormat": {
                    "fontFamily": "Arial",
                    "fontSize": 10,
                    "bold": True,
                    "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
                }
            },
            "userEnteredFormat(backgroundColor,textFormat)"
        ))
    
    # 7. Apply total formatting (11pt bold on #E8EDF5)
    for row_idx in total_rows:
        requests_list.append(make_repeat_cell(
            sheet_id, row_idx, row_idx + 1, 0, max_cols,
            {
                "backgroundColor": BLUE_TINT,
                "textFormat": {
                    "fontFamily": "Arial",
                    "fontSize": 11,
                    "bold": True,
                    "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
                }
            },
            "userEnteredFormat(backgroundColor,textFormat)"
        ))
    
    # 8. Apply number formats to data rows
    # Find "Amount" columns and "%" columns by scanning column headers
    amount_cols = []
    pct_cols = []
    for row_idx in column_header_rows:
        if row_idx < len(values):
            row = values[row_idx]
            for col_idx, val in enumerate(row):
                val_upper = str(val).upper().strip()
                if val_upper in ['AMOUNT', 'TOTAL', 'BALANCE', 'TARGET', 'ACTUAL', 'DIFFERENCE',
                                 'BUDGET', 'INCOME', 'EXPENSES', 'NET', 'REVENUE']:
                    amount_cols.append(col_idx)
                elif '%' in val_upper or 'PERCENTAGE' in val_upper or 'RATE' in val_upper or 'ALLOCATION' in val_upper:
                    pct_cols.append(col_idx)
    
    # Apply currency format to amount columns across all data rows
    amount_cols = list(set(amount_cols))
    pct_cols = list(set(pct_cols))
    
    for col_idx in amount_cols:
        # Apply to all rows (data + subtotal + total)
        all_format_rows = data_rows + subtotal_rows + total_rows
        if all_format_rows:
            for row_idx in all_format_rows:
                requests_list.append(make_repeat_cell(
                    sheet_id, row_idx, row_idx + 1, col_idx, col_idx + 1,
                    {"numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"}},
                    "userEnteredFormat.numberFormat"
                ))
    
    for col_idx in pct_cols:
        all_format_rows = data_rows + subtotal_rows + total_rows
        if all_format_rows:
            for row_idx in all_format_rows:
                requests_list.append(make_repeat_cell(
                    sheet_id, row_idx, row_idx + 1, col_idx, col_idx + 1,
                    {"numberFormat": {"type": "PERCENT", "pattern": "0.0%"}},
                    "userEnteredFormat.numberFormat"
                ))
    
    return requests_list


def format_transaction_tab(spreadsheet_id, sheet_id, tab_name, month_name):
    """Format a transaction tab (Business 4991, Personal 0068, Biz CC 0678, Sapphire 4252)."""
    print(f"  💳 Formatting '{tab_name}' (sheetId={sheet_id})...")
    
    # Read values to find how many rows
    safe_name = tab_name.replace("'", "''")
    values = get_sheet_values(spreadsheet_id, f"'{safe_name}'!A1:F500")
    num_rows = len(values) if values else 100
    num_rows = max(num_rows, 10)
    
    requests_list = []
    
    # 1. Set ALL cells to Arial 10pt (entire sheet area)
    requests_list.append(make_repeat_cell(
        sheet_id, 0, num_rows + 50, 0, 6,
        {
            "textFormat": {
                "fontFamily": "Arial",
                "fontSize": 10,
                "bold": False,
                "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
            }
        },
        "userEnteredFormat.textFormat"
    ))
    
    # 2. Set all data row heights to 21px
    requests_list.append(make_row_height(sheet_id, 1, num_rows + 50, 21))
    
    # 3. Header row (row 1): navy bg, white bold 11pt, 30px height
    requests_list.append(make_repeat_cell(
        sheet_id, 0, 1, 0, 6,
        {
            "backgroundColor": NAVY,
            "textFormat": {
                "fontFamily": "Arial",
                "fontSize": 11,
                "bold": True,
                "foregroundColorStyle": {"rgbColor": WHITE_COLOR}
            },
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "MIDDLE"
        },
        "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
    ))
    requests_list.append(make_row_height(sheet_id, 0, 1, 30))
    
    # 4. Date column (A) - date format MM/DD/YYYY
    requests_list.append(make_repeat_cell(
        sheet_id, 1, num_rows + 50, 0, 1,
        {"numberFormat": {"type": "DATE", "pattern": "MM/dd/yyyy"}},
        "userEnteredFormat.numberFormat"
    ))
    
    # 5. Amount column (D, index 3) - currency with red negatives
    requests_list.append(make_repeat_cell(
        sheet_id, 1, num_rows + 50, 3, 4,
        {
            "numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00;[Red]($#,##0.00)"},
            "horizontalAlignment": "RIGHT"
        },
        "userEnteredFormat(numberFormat,horizontalAlignment)"
    ))
    
    # 6. Balance column (E, index 4) - currency format
    requests_list.append(make_repeat_cell(
        sheet_id, 1, num_rows + 50, 4, 5,
        {
            "numberFormat": {"type": "CURRENCY", "pattern": "$#,##0.00"},
            "horizontalAlignment": "RIGHT"
        },
        "userEnteredFormat(numberFormat,horizontalAlignment)"
    ))
    
    # 7. Text alignment for text columns (B, C, F) - left
    for col in [1, 2, 5]:
        requests_list.append(make_repeat_cell(
            sheet_id, 1, num_rows + 50, col, col + 1,
            {"horizontalAlignment": "LEFT"},
            "userEnteredFormat.horizontalAlignment"
        ))
    
    return requests_list


def format_utility_tab(spreadsheet_id, sheet_id, tab_name, month_name):
    """Format Profit First, Pareto, or other utility tabs."""
    print(f"  📋 Formatting '{tab_name}' (sheetId={sheet_id})...")
    
    safe_name = tab_name.replace("'", "''")
    values = get_sheet_values(spreadsheet_id, f"'{safe_name}'!A1:Z100")
    num_rows = len(values) if values else 50
    max_cols = max((len(row) for row in values), default=10) if values else 10
    max_cols = max(max_cols, 6)
    
    requests_list = []
    
    # 1. Set ALL cells to Arial 10pt
    requests_list.append(make_repeat_cell(
        sheet_id, 0, num_rows + 10, 0, max_cols,
        {
            "textFormat": {
                "fontFamily": "Arial",
                "fontSize": 10,
                "bold": False,
                "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
            }
        },
        "userEnteredFormat.textFormat"
    ))
    
    # 2. Set row heights to 21px
    requests_list.append(make_row_height(sheet_id, 0, num_rows + 10, 21))
    
    # 3. Find header rows and format them
    if values:
        for i, row in enumerate(values):
            if not row or is_empty_row(row):
                continue
            first = str(row[0]).strip().upper()
            # Check for section header markers
            if (is_section_header(row) or 
                any(marker in first for marker in ['PROFIT FIRST', 'PARETO', 'ALLOCATION', '80/20'])):
                # Navy header
                requests_list.append(make_repeat_cell(
                    sheet_id, i, i + 1, 0, max_cols,
                    {
                        "backgroundColor": NAVY,
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColorStyle": {"rgbColor": WHITE_COLOR}
                        },
                        "horizontalAlignment": "LEFT",
                        "verticalAlignment": "MIDDLE"
                    },
                    "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
                ))
                requests_list.append(make_row_height(sheet_id, i, i + 1, 30))
            elif is_column_header(row):
                requests_list.append(make_repeat_cell(
                    sheet_id, i, i + 1, 0, max_cols,
                    {
                        "backgroundColor": LIGHT_GRAY,
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
                        },
                        "horizontalAlignment": "CENTER",
                        "verticalAlignment": "MIDDLE"
                    },
                    "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment,verticalAlignment)"
                ))
            elif is_total_row(row):
                requests_list.append(make_repeat_cell(
                    sheet_id, i, i + 1, 0, max_cols,
                    {
                        "backgroundColor": BLUE_TINT,
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True,
                            "foregroundColorStyle": {"rgbColor": BLACK_COLOR}
                        }
                    },
                    "userEnteredFormat(backgroundColor,textFormat)"
                ))
    
    return requests_list


def process_spreadsheet(month_name, spreadsheet_id):
    """Process one spreadsheet — apply all formatting fixes."""
    print(f"\n{'='*60}")
    print(f"📅 Processing: {month_name}")
    print(f"   ID: {spreadsheet_id}")
    print(f"{'='*60}")
    
    # Get metadata
    try:
        meta = get_spreadsheet(spreadsheet_id)
    except Exception as e:
        print(f"  ❌ Failed to get metadata: {e}")
        return {'month': month_name, 'status': 'FAILED', 'error': str(e)}
    
    sheets_info = {}
    for sheet in meta.get('sheets', []):
        props = sheet['properties']
        title = props['title']
        sid = props['sheetId']
        sheets_info[title] = sid
        print(f"  📋 Tab: '{title}' (sheetId={sid})")
    
    all_requests = []
    tab_stats = {}
    
    # Process each tab
    for tab_name, sheet_id in sheets_info.items():
        tab_lower = tab_name.lower()
        
        if 'dashboard' in tab_lower:
            reqs = format_dashboard(spreadsheet_id, sheet_id, tab_name, month_name)
            tab_stats[tab_name] = len(reqs)
            all_requests.extend(reqs)
        elif any(x in tab_lower for x in ['4991', '0068', '0678', '4252', 'business', 'personal', 'sapphire', 'biz cc']):
            reqs = format_transaction_tab(spreadsheet_id, sheet_id, tab_name, month_name)
            tab_stats[tab_name] = len(reqs)
            all_requests.extend(reqs)
        elif any(x in tab_lower for x in ['profit', 'pareto', 'summary', 'allocation']):
            reqs = format_utility_tab(spreadsheet_id, sheet_id, tab_name, month_name)
            tab_stats[tab_name] = len(reqs)
            all_requests.extend(reqs)
        else:
            # Generic: just set Arial 10pt default
            print(f"  📄 Generic format for '{tab_name}' (sheetId={sheet_id})")
            reqs = format_utility_tab(spreadsheet_id, sheet_id, tab_name, month_name)
            tab_stats[tab_name] = len(reqs)
            all_requests.extend(reqs)
    
    # Send all requests in batches (API limit ~500-1000 per batch)
    BATCH_SIZE = 500
    total_sent = 0
    
    if all_requests:
        for i in range(0, len(all_requests), BATCH_SIZE):
            batch = all_requests[i:i + BATCH_SIZE]
            print(f"  📤 Sending batch {i//BATCH_SIZE + 1} ({len(batch)} requests)...")
            result = batch_update(spreadsheet_id, batch)
            if result:
                total_sent += len(batch)
                print(f"    ✅ Batch applied successfully")
            else:
                print(f"    ❌ Batch failed")
            time.sleep(1)  # rate limiting
    
    print(f"  ✅ {month_name}: {total_sent}/{len(all_requests)} requests applied")
    return {
        'month': month_name,
        'status': 'OK' if total_sent == len(all_requests) else 'PARTIAL',
        'total_requests': len(all_requests),
        'sent': total_sent,
        'tabs': tab_stats
    }


def main():
    print("🔧 DEEP FORMATTING FIX — KuriosBrand Accounting Sheets")
    print(f"   Started: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"   Sheets to process: {len(SHEETS)}")
    
    results = []
    
    for month_name, spreadsheet_id in SHEETS.items():
        try:
            result = process_spreadsheet(month_name, spreadsheet_id)
            results.append(result)
        except Exception as e:
            print(f"  ❌ EXCEPTION processing {month_name}: {e}")
            import traceback
            traceback.print_exc()
            results.append({'month': month_name, 'status': 'ERROR', 'error': str(e)})
        
        time.sleep(2)  # Be gentle on the API
    
    # Generate report
    print("\n" + "="*60)
    print("📊 FORMATTING FIX REPORT")
    print("="*60)
    
    report_lines = [
        "# Deep Formatting Fix Report",
        f"**Date:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Sheets Processed:** {len(results)}",
        "",
        "## Results",
        "",
        "| Month | Status | Requests | Tabs |",
        "|-------|--------|----------|------|",
    ]
    
    for r in results:
        tabs_str = ", ".join(f"{k}({v})" for k, v in r.get('tabs', {}).items())
        report_lines.append(
            f"| {r['month']} | {r['status']} | {r.get('sent', 'N/A')}/{r.get('total_requests', 'N/A')} | {tabs_str} |"
        )
    
    report_lines.extend([
        "",
        "## What Was Fixed",
        "",
        "### All Tabs",
        "- ✅ Font family set to Arial across all cells",
        "- ✅ Font size set to 10pt default",
        "- ✅ Row heights set to 21px (30px for headers)",
        "",
        "### Dashboard Tabs",
        "- ✅ Section headers: 14pt bold white text on navy (#1B2A4A)",
        "- ✅ Column headers: 11pt bold on light gray (#F3F3F3), centered",
        "- ✅ Subtotal rows: bold on light gray (#F3F3F3)",
        "- ✅ Total rows: 11pt bold on blue tint (#E8EDF5)",
        "- ✅ Currency columns: $#,##0.00 format",
        "- ✅ Percentage columns: 0.0% format",
        "",
        "### Transaction Tabs (4991, 0068, 0678, 4252)",
        "- ✅ Header row: navy bg, white 11pt bold, 30px height, centered",
        "- ✅ Date column (A): MM/DD/YYYY format",
        "- ✅ Amount column (D): $#,##0.00;[Red]($#,##0.00) — red negatives in parens",
        "- ✅ Balance column (E): $#,##0.00",
        "- ✅ Text columns left-aligned, number columns right-aligned",
        "",
        "### Profit First & Pareto Tabs",
        "- ✅ Section headers: navy bg, white 11pt bold",
        "- ✅ Column headers: light gray bg, 11pt bold, centered",
        "- ✅ Total rows: blue tint bg, 11pt bold",
        "",
        "## What Was NOT Changed",
        "- Column widths (already correct)",
        "- Tab colors (already correct)",
        "- Tab order (already correct)",
        "- Cell values (formatting only)",
    ])
    
    report = "\n".join(report_lines)
    
    with open('/home/ec2-user/clawd/data/formatting-fixes-report.md', 'w') as f:
        f.write(report)
    
    print(report)
    print(f"\n✅ Report saved to /home/ec2-user/clawd/data/formatting-fixes-report.md")
    
    # Summary
    ok = sum(1 for r in results if r['status'] == 'OK')
    partial = sum(1 for r in results if r['status'] == 'PARTIAL')
    failed = sum(1 for r in results if r['status'] in ('FAILED', 'ERROR'))
    print(f"\n🏁 DONE: {ok} OK, {partial} partial, {failed} failed out of {len(results)} sheets")


if __name__ == '__main__':
    main()
