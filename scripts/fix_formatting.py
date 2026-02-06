#!/usr/bin/env python3
"""Fix formatting for August & September dashboards — currency, debt table widths, final polish."""

import json
import requests

def refresh_token():
    with open('/home/ec2-user/.config/gcal-pro/token.json') as f:
        creds = json.load(f)
    resp = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token'
    })
    return resp.json()['access_token']

TOKEN = refresh_token()
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

def rgb(hex_str):
    h = hex_str.lstrip('#')
    return {'red': int(h[0:2],16)/255, 'green': int(h[2:4],16)/255, 'blue': int(h[4:6],16)/255}

NAVY = rgb('#1B2A4A')
WHITE = rgb('#FFFFFF')
DARK_BLUE = rgb('#2C3E6B')
LIGHT_BLUE = rgb('#E8EDF3')
LIGHT_GREEN = rgb('#E8F5E9')
DARK_GREEN = rgb('#1B5E20')
LIGHT_GRAY = rgb('#F5F5F5')
SUBTOTAL_BG = rgb('#D5DDE8')

CURRENCY_FMT = {'type': 'CURRENCY', 'pattern': '"$"#,##0.00;("$"#,##0.00)'}
PERCENT_FMT = {'type': 'PERCENT', 'pattern': '0.0%'}

def sheets_batch_update(spreadsheet_id, requests_list):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate'
    body = {'requests': requests_list}
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} {r.text[:500]}")
    return r.json()

def get_sheet_metadata(spreadsheet_id):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?includeGridData=false'
    r = requests.get(url, headers=HEADERS)
    return r.json()

def format_range(sheet_id, start_row, end_row, start_col, end_col, fmt):
    return {
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'cell': {'userEnteredFormat': fmt},
            'fields': 'userEnteredFormat'
        }
    }

def set_col_width(sheet_id, col, width):
    return {
        'updateDimensionProperties': {
            'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col+1},
            'properties': {'pixelSize': width},
            'fields': 'pixelSize'
        }
    }

def apply_polish(spreadsheet_id):
    """Apply final formatting polish to the dashboard."""
    meta = get_sheet_metadata(spreadsheet_id)
    
    dashboard_id = None
    for s in meta['sheets']:
        if s['properties']['title'] == '📊 Dashboard':
            dashboard_id = s['properties']['sheetId']
            break
    
    if dashboard_id is None:
        print(f"Dashboard not found in {spreadsheet_id}")
        return
    
    reqs = []
    
    # Expand to 8 columns for debt tracking
    widths = {0: 200, 1: 280, 2: 130, 3: 140, 4: 110, 5: 110, 6: 100, 7: 140}
    for col, w in widths.items():
        reqs.append(set_col_width(dashboard_id, col, w))
    
    # Apply currency format to column D (index 3) for all data rows  
    reqs.append(format_range(dashboard_id, 4, 200, 3, 4, {
        'numberFormat': CURRENCY_FMT,
        'horizontalAlignment': 'RIGHT'
    }))
    
    # Apply right alignment to column C for subtotals  
    reqs.append(format_range(dashboard_id, 4, 200, 2, 3, {
        'horizontalAlignment': 'RIGHT'
    }))
    
    # Apply debt tracking formatting (wider section with 6 cols)
    # Find the debt section - it starts at different rows per sheet
    # We need to read the data to find it
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{requests.utils.quote("📊 Dashboard!A1:A200")}'
    r = requests.get(url, headers=HEADERS)
    data = r.json().get('values', [])
    
    debt_row = None
    balance_row = None
    asset_row = None
    action_row = None
    
    for i, row in enumerate(data):
        if row and 'DEBT TRACKING' in str(row[0]):
            debt_row = i
        elif row and 'ACCOUNT BALANCES' in str(row[0]):
            balance_row = i
        elif row and 'ASSETS' in str(row[0]):
            asset_row = i
        elif row and 'ACTION ITEMS' in str(row[0]):
            action_row = i
    
    # Format debt tracking table header
    if debt_row is not None:
        # Section header
        reqs.append(format_range(dashboard_id, debt_row, debt_row+1, 0, 6, {
            'backgroundColorStyle': {'rgbColor': NAVY},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11}
        }))
        # Column headers
        reqs.append(format_range(dashboard_id, debt_row+1, debt_row+2, 0, 6, {
            'backgroundColorStyle': {'rgbColor': DARK_BLUE},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 10},
            'horizontalAlignment': 'CENTER'
        }))
        # Data rows
        reqs.append(format_range(dashboard_id, debt_row+2, debt_row+8, 1, 3, {
            'numberFormat': CURRENCY_FMT,
            'horizontalAlignment': 'RIGHT'
        }))
        # Total rows (bold)
        reqs.append(format_range(dashboard_id, debt_row+7, debt_row+9, 0, 6, {
            'backgroundColorStyle': {'rgbColor': NAVY},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 10}
        }))
    
    # Format balance table
    if balance_row is not None:
        reqs.append(format_range(dashboard_id, balance_row, balance_row+1, 0, 4, {
            'backgroundColorStyle': {'rgbColor': NAVY},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11}
        }))
        reqs.append(format_range(dashboard_id, balance_row+1, balance_row+2, 0, 4, {
            'backgroundColorStyle': {'rgbColor': DARK_BLUE},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 10}
        }))
    
    # Format assets table
    if asset_row is not None:
        reqs.append(format_range(dashboard_id, asset_row, asset_row+1, 0, 4, {
            'backgroundColorStyle': {'rgbColor': NAVY},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11}
        }))
        
        # Find Net Worth row for special highlight
        for i in range(asset_row, min(asset_row+20, len(data))):
            if i < len(data) and data[i] and 'Net Worth' in str(data[i][0]):
                reqs.append(format_range(dashboard_id, i, i+1, 0, 4, {
                    'backgroundColorStyle': {'rgbColor': DARK_GREEN},
                    'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 12}
                }))
            elif i < len(data) and data[i] and 'Total Assets' in str(data[i][0]):
                reqs.append(format_range(dashboard_id, i, i+1, 0, 4, {
                    'backgroundColorStyle': {'rgbColor': LIGHT_GREEN},
                    'textFormat': {'bold': True, 'fontSize': 10}
                }))
            elif i < len(data) and data[i] and 'Total Liabilities' in str(data[i][0]):
                reqs.append(format_range(dashboard_id, i, i+1, 0, 4, {
                    'backgroundColorStyle': {'rgbColor': rgb('#FFEBEE')},
                    'textFormat': {'bold': True, 'fontSize': 10}
                }))
    
    # Format action items
    if action_row is not None:
        reqs.append(format_range(dashboard_id, action_row, action_row+1, 0, 4, {
            'backgroundColorStyle': {'rgbColor': NAVY},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11}
        }))
        reqs.append(format_range(dashboard_id, action_row+1, action_row+2, 0, 4, {
            'backgroundColorStyle': {'rgbColor': DARK_BLUE},
            'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 10}
        }))
    
    # Apply all formatting
    if reqs:
        sheets_batch_update(spreadsheet_id, reqs)
        print(f"Applied {len(reqs)} formatting requests to {spreadsheet_id}")

# Process both sheets
AUG_ID = '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI'
SEPT_ID = '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM'

print("Polishing August 2025...")
apply_polish(AUG_ID)

print("Polishing September 2025...")
apply_polish(SEPT_ID)

print("\n✅ Formatting polish complete!")
print(f"August:    https://docs.google.com/spreadsheets/d/{AUG_ID}")
print(f"September: https://docs.google.com/spreadsheets/d/{SEPT_ID}")
