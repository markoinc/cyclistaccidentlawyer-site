#!/usr/bin/env python3
"""Fix formatting on the master template - re-apply batches that failed."""

import json
import requests as req
import time

TOKEN_PATH = '/home/ec2-user/.config/gcal-pro/token.json'
SHEET_ID_PATH = '/home/ec2-user/clawd/data/master-template-sheet-id.txt'
BASE = 'https://sheets.googleapis.com/v4/spreadsheets'

C = {
    'navy':       {'red': 27/255, 'green': 42/255, 'blue': 74/255},
    'white':      {'red': 1.0, 'green': 1.0, 'blue': 1.0},
    'light_gray': {'red': 243/255, 'green': 243/255, 'blue': 243/255},
    'totals_bg':  {'red': 232/255, 'green': 237/255, 'blue': 245/255},
    'green_tab':  {'red': 52/255, 'green': 168/255, 'blue': 83/255},
    'orange_tab': {'red': 1.0, 'green': 109/255, 'blue': 1/255},
    'gray_tab':   {'red': 153/255, 'green': 153/255, 'blue': 153/255},
    'red_text':   {'red': 204/255, 'green': 0, 'blue': 0},
    'dk_green':   {'red': 0, 'green': 97/255, 'blue': 0},
    'black':      {'red': 0, 'green': 0, 'blue': 0},
    'green_bg':   {'red': 183/255, 'green': 225/255, 'blue': 183/255},
    'yellow_bg':  {'red': 255/255, 'green': 242/255, 'blue': 179/255},
    'red_bg':     {'red': 244/255, 'green': 199/255, 'blue': 195/255},
    'orange_bg':  {'red': 255/255, 'green': 229/255, 'blue': 194/255},
    'gray_bg':    {'red': 230/255, 'green': 230/255, 'blue': 230/255},
}

SID = {
    'dashboard': 0, 'profit_first': 1, 'pareto': 2, 'biz_4991': 3,
    'personal_0068': 4, 'biz_cc_0678': 5, 'sapphire_4252': 6, 'raw_data': 7,
}

def refresh_token():
    with open(TOKEN_PATH) as f:
        tok = json.load(f)
    resp = req.post('https://oauth2.googleapis.com/token', data={
        'client_id': tok['client_id'],
        'client_secret': tok['client_secret'],
        'refresh_token': tok['refresh_token'],
        'grant_type': 'refresh_token',
    })
    resp.raise_for_status()
    data = resp.json()
    tok['token'] = data['access_token']
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tok, f)
    return data['access_token']

def headers(token):
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def cell_fmt(sheet_id, row, col, end_row, end_col, bg=None, fg=None, bold=None, font_size=None, halign=None, number_fmt=None, italic=None, font_family=None):
    """Build a repeatCell request. Only includes explicitly set properties."""
    cell = {'userEnteredFormat': {}}
    fmt = cell['userEnteredFormat']
    fields = []
    
    if bg:
        fmt['backgroundColor'] = C[bg]
        fields.append('userEnteredFormat.backgroundColor')
    
    text_fmt = {}
    if fg:
        text_fmt['foregroundColor'] = C[fg]
        fields.append('userEnteredFormat.textFormat.foregroundColor')
    if bold is not None:
        text_fmt['bold'] = bold
        fields.append('userEnteredFormat.textFormat.bold')
    if italic is not None:
        text_fmt['italic'] = italic
        fields.append('userEnteredFormat.textFormat.italic')
    if font_size is not None:
        text_fmt['fontSize'] = font_size
        fields.append('userEnteredFormat.textFormat.fontSize')
    if font_family:
        text_fmt['fontFamily'] = font_family
        fields.append('userEnteredFormat.textFormat.fontFamily')
    if text_fmt:
        fmt['textFormat'] = text_fmt
    
    if halign:
        fmt['horizontalAlignment'] = halign
        fields.append('userEnteredFormat.horizontalAlignment')
    if number_fmt:
        fmt['numberFormat'] = {'type': 'NUMBER', 'pattern': number_fmt}
        fields.append('userEnteredFormat.numberFormat')
    
    if not fields:
        return None  # Skip empty format requests
    
    return {
        'repeatCell': {
            'range': {'sheetId': sheet_id, 'startRowIndex': row, 'endRowIndex': end_row, 'startColumnIndex': col, 'endColumnIndex': end_col},
            'cell': cell,
            'fields': ','.join(fields),
        }
    }

def col_width(sheet_id, col, width):
    return {
        'updateDimensionProperties': {
            'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col + 1},
            'properties': {'pixelSize': width},
            'fields': 'pixelSize',
        }
    }

def row_height(sheet_id, row, height):
    return {
        'updateDimensionProperties': {
            'range': {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': row, 'endIndex': row + 1},
            'properties': {'pixelSize': height},
            'fields': 'pixelSize',
        }
    }

def main():
    token = refresh_token()
    with open(SHEET_ID_PATH) as f:
        spreadsheet_id = f.read().strip()
    
    print(f"Fixing formatting on {spreadsheet_id}...")
    
    reqs = []
    
    # ══════════════════════════════════════════════════════════
    # Set default font Arial 10pt on all sheets
    # ══════════════════════════════════════════════════════════
    for sid_val in SID.values():
        reqs.append(cell_fmt(sid_val, 0, 0, 200, 10, font_family='Arial', font_size=10))
    
    # ══════════════════════════════════════════════════════════
    # PROFIT FIRST - Re-apply all formatting
    # ══════════════════════════════════════════════════════════
    sid = SID['profit_first']
    pf_widths = [200, 120, 120, 160, 160, 160]
    for i, w in enumerate(pf_widths):
        reqs.append(col_width(sid, i, w))
    
    # Title already merged in batch 1, just re-apply style
    reqs.append(cell_fmt(sid, 0, 0, 1, 6, bg='navy', fg='white', bold=True, font_size=14))
    reqs.append(row_height(sid, 0, 36))
    
    # Column headers
    reqs.append(cell_fmt(sid, 1, 0, 2, 6, bg='navy', fg='white', bold=True, font_size=11, halign='CENTER'))
    reqs.append(row_height(sid, 1, 30))
    
    # Currency columns D, E, F (indices 3, 4, 5)
    reqs.append(cell_fmt(sid, 2, 3, 7, 6, number_fmt='$#,##0.00;[Red]($#,##0.00)'))
    
    # Revenue row - totals style
    reqs.append(cell_fmt(sid, 2, 0, 3, 6, bg='totals_bg', bold=True))
    
    # Color coding rows based on target performance
    reqs.append(cell_fmt(sid, 3, 0, 4, 6, bg='yellow_bg'))  # Profit - close
    reqs.append(cell_fmt(sid, 4, 0, 5, 6, bg='red_bg'))      # Owner's Comp - off
    reqs.append(cell_fmt(sid, 5, 0, 6, 6, bg='red_bg'))      # Tax - off
    reqs.append(cell_fmt(sid, 6, 0, 7, 6, bg='red_bg', bold=True))  # OpEx - over
    
    # Notes
    reqs.append(cell_fmt(sid, 8, 0, 9, 6, bold=True, font_size=11))
    reqs.append(cell_fmt(sid, 9, 0, 13, 6, italic=True))
    
    # ══════════════════════════════════════════════════════════
    # PARETO ANALYSIS - Re-apply all formatting
    # ══════════════════════════════════════════════════════════
    sid = SID['pareto']
    pareto_widths = [60, 200, 130, 130, 100, 180]
    for i, w in enumerate(pareto_widths):
        reqs.append(col_width(sid, i, w))
    
    reqs.append(cell_fmt(sid, 0, 0, 1, 6, bg='navy', fg='white', bold=True, font_size=14))
    reqs.append(row_height(sid, 0, 36))
    
    reqs.append(cell_fmt(sid, 1, 0, 2, 6, bg='navy', fg='white', bold=True, font_size=11, halign='CENTER'))
    reqs.append(row_height(sid, 1, 30))
    
    # Currency columns
    reqs.append(cell_fmt(sid, 2, 2, 24, 4, number_fmt='$#,##0.00'))
    
    # Rank column center
    reqs.append(cell_fmt(sid, 2, 0, 24, 1, halign='CENTER'))
    
    # Items above 80% line (rows 2-7 = indices 2-8) - orange
    reqs.append(cell_fmt(sid, 2, 0, 8, 6, bg='orange_bg'))
    
    # Items below 80% line - light gray
    reqs.append(cell_fmt(sid, 8, 0, 24, 6, bg='gray_bg'))
    
    # Note rows
    reqs.append(cell_fmt(sid, 26, 0, 28, 6, bold=True, font_size=11, italic=True))
    
    # ══════════════════════════════════════════════════════════
    # TRANSACTION TABS - Re-apply all formatting
    # ══════════════════════════════════════════════════════════
    txn_tabs = [
        (SID['biz_4991'], 16),
        (SID['personal_0068'], 22),
        (SID['biz_cc_0678'], 9),
        (SID['sapphire_4252'], 12),
    ]
    txn_widths = [110, 250, 250, 130, 130, 250]
    
    for sid, data_rows in txn_tabs:
        for i, w in enumerate(txn_widths):
            reqs.append(col_width(sid, i, w))
        
        reqs.append(cell_fmt(sid, 0, 0, 1, 6, bg='navy', fg='white', bold=True, font_size=11, halign='CENTER'))
        reqs.append(row_height(sid, 0, 30))
        
        # Data font
        reqs.append(cell_fmt(sid, 1, 0, data_rows, 6, font_size=10, font_family='Arial'))
        
        # Amount column (D = index 3) - currency with red negatives
        reqs.append(cell_fmt(sid, 1, 3, data_rows, 4, number_fmt='$#,##0.00;[Red]($#,##0.00)', halign='RIGHT'))
        
        # Balance column (E = index 4)
        reqs.append(cell_fmt(sid, 1, 4, data_rows, 5, number_fmt='$#,##0.00', halign='RIGHT'))
    
    # ══════════════════════════════════════════════════════════
    # RAW DATA TAB - Re-apply
    # ══════════════════════════════════════════════════════════
    sid = SID['raw_data']
    for row in [0, 5, 10, 15]:
        reqs.append(cell_fmt(sid, row, 0, row + 1, 6, bg='navy', fg='white', bold=True, font_size=12))
        reqs.append(row_height(sid, row, 32))
    
    for row in [1, 6, 11, 16]:
        reqs.append(cell_fmt(sid, row, 0, row + 1, 6, italic=True, fg='gray_tab'))
    
    raw_widths = [200, 200, 200, 130, 130, 200]
    for i, w in enumerate(raw_widths):
        reqs.append(col_width(sid, i, w))
    
    # ══════════════════════════════════════════════════════════
    # DASHBOARD - Complete re-format of currency and specific rows
    # ══════════════════════════════════════════════════════════
    sid = SID['dashboard']
    dash_widths = [250, 200, 150, 130, 250, 130, 150]
    for i, w in enumerate(dash_widths):
        reqs.append(col_width(sid, i, w))
    
    # I need to match the exact row layout from build_dashboard_data.
    # Let me enumerate the dashboard row types manually based on the function:
    # Row 0: section_header (SECTION A)
    # Row 1: col_header
    # Rows 2-4: data
    # Row 5: total
    # Rows 6-7: blank
    # Row 8: section_header (SECTION B)
    # Row 9: col_header
    # Rows 10-12: data (SaaS)
    # Row 13: subtotal
    # Rows 14-15: data (Marketing)
    # Row 16: subtotal
    # Rows 17-18: data (Operations)
    # Row 19: subtotal
    # Row 20: data (Debt)
    # Row 21: subtotal
    # Row 22: data (Fees)
    # Row 23: subtotal
    # Row 24: data (ATM)
    # Row 25: subtotal
    # Row 26: total
    # Rows 27-28: blank
    # Row 29: section_header (SECTION C)
    # Row 30: col_header
    # Rows 31-32: data (Investments)
    # Row 33: subtotal
    # Rows 34-35: data (Living)
    # Row 36: subtotal
    # Rows 37-38: data (Food)
    # Row 39: subtotal
    # Rows 40-41: data (Subscriptions)
    # Row 42: subtotal
    # Row 43: data (Travel)
    # Row 44: subtotal
    # Row 45: data (Shopping)
    # Row 46: subtotal
    # Row 47: data (CC Payments)
    # Row 48: subtotal
    # Row 49: data (CC Interest)
    # Row 50: subtotal
    # Row 51: data (ATM)
    # Row 52: subtotal
    # Row 53: total
    # Rows 54-55: blank
    # Row 56: section_header (SECTION D)
    # Row 57: col_header
    # Rows 58-66: data (9 metrics)
    # Rows 67-68: blank
    # Row 69: section_header (SECTION E)
    # Row 70: col_header
    # Rows 71-75: data (5 flows)
    # Rows 76-77: blank
    # Row 78: section_header (SECTION F)
    # Row 79: col_header
    # Rows 80-84: data (5 debts)
    # Row 85: total
    # Rows 86-87: blank
    # Row 88: section_header (SECTION G)
    # Row 89: col_header
    # Rows 90-93: data (4 accounts)
    # Rows 94-95: blank
    # Row 96: section_header (SECTION H)
    # Row 97: col_header
    # Rows 98-103: data (6 assets)
    # Row 104: total (TOTAL ASSETS)
    # Row 105: total (TOTAL LIABILITIES)
    # Row 106: total (NET WORTH)
    # Rows 107-108: blank
    # Row 109: section_header (SECTION I)
    # Row 110: col_header
    # Rows 111-116: data (6 action items)
    
    section_headers = [0, 8, 29, 56, 69, 78, 88, 96, 109]
    col_headers = [1, 9, 30, 57, 70, 79, 89, 97, 110]
    subtotals = [13, 16, 19, 21, 23, 25, 33, 36, 39, 42, 44, 46, 48, 50, 52]
    totals = [5, 26, 53, 85, 104, 105, 106]
    
    for r in section_headers:
        reqs.append(cell_fmt(sid, r, 0, r + 1, 7, bg='navy', fg='white', bold=True, font_size=14))
        reqs.append(row_height(sid, r, 36))
    
    for r in col_headers:
        reqs.append(cell_fmt(sid, r, 0, r + 1, 7, bg='light_gray', bold=True, font_size=11, halign='CENTER'))
        reqs.append(row_height(sid, r, 28))
    
    for r in subtotals:
        reqs.append(cell_fmt(sid, r, 0, r + 1, 7, bg='light_gray', bold=True))
    
    for r in totals:
        reqs.append(cell_fmt(sid, r, 0, r + 1, 7, bg='totals_bg', bold=True, font_size=11))
    
    # Filter out None requests
    reqs = [r for r in reqs if r is not None]
    
    # Send in chunks
    chunk_size = 80
    for i in range(0, len(reqs), chunk_size):
        chunk = reqs[i:i+chunk_size]
        resp = req.post(
            f'{BASE}/{spreadsheet_id}:batchUpdate',
            headers=headers(token),
            json={'requests': chunk},
        )
        if resp.status_code != 200:
            print(f"⚠️  Chunk {i//chunk_size + 1} error: {resp.status_code}")
            print(resp.text[:500])
        else:
            print(f"✅ Chunk {i//chunk_size + 1} applied ({len(chunk)} requests)")
        time.sleep(0.3)
    
    print(f"\n✅ Formatting fix complete!")

if __name__ == '__main__':
    main()
