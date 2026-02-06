#!/usr/bin/env python3
"""Batch 3 Standardization: November 2025, December 2025, January 2026"""

import json, urllib.request, urllib.parse, time, sys

# Get fresh token
t = json.load(open('/home/ec2-user/.config/gcal-pro/token.json'))
data = urllib.parse.urlencode({
    'client_id': t['client_id'],
    'client_secret': t['client_secret'],
    'refresh_token': t['refresh_token'],
    'grant_type': 'refresh_token'
}).encode()
req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
resp = json.loads(urllib.request.urlopen(req).read())
TOKEN = resp['access_token']

def api_call(url, method='GET', body=None):
    """Make Google Sheets API call"""
    headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
    if body:
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"API Error {e.code}: {error_body[:500]}")
        raise

def batch_update(sheet_id, requests_list):
    """Execute batch update"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}:batchUpdate'
    return api_call(url, 'POST', {'requests': requests_list})

def update_values(sheet_id, range_str, values, input_option='USER_ENTERED'):
    """Update cell values"""
    encoded_range = urllib.parse.quote(range_str)
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}?valueInputOption={input_option}'
    return api_call(url, 'PUT', {'values': values})

def get_values(sheet_id, range_str):
    """Get cell values"""
    encoded_range = urllib.parse.quote(range_str)
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_range}'
    return api_call(url).get('values', [])

def get_sheet_info(sheet_id):
    """Get spreadsheet metadata"""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}?fields=properties.title,sheets.properties'
    return api_call(url)

def rgb(hex_color):
    """Convert hex color to RGB dict"""
    h = hex_color.lstrip('#')
    return {
        'red': int(h[0:2], 16) / 255.0,
        'green': int(h[2:4], 16) / 255.0,
        'blue': int(h[4:6], 16) / 255.0
    }

NAVY = rgb('1B2A4A')
WHITE = {'red': 1, 'green': 1, 'blue': 1}
LIGHT_GRAY = rgb('F3F3F3')
TOTAL_BG = rgb('E8EDF5')
GREEN_TAB = rgb('34A853')
ORANGE_TAB = rgb('FF6D01')
NAVY_TAB = rgb('1B2A4A')
GRAY_TAB = rgb('999999')

def format_section_header(sheet_gid, row, col_count=6):
    """Format a section header row with navy bg, white text"""
    return [
        {
            'repeatCell': {
                'range': {'sheetId': sheet_gid, 'startRowIndex': row, 'endRowIndex': row + 1, 'startColumnIndex': 0, 'endColumnIndex': col_count},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': NAVY,
                        'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 14},
                        'horizontalAlignment': 'LEFT'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        }
    ]

def format_subheader(sheet_gid, row, col_count=6):
    """Format a sub-header row"""
    return [
        {
            'repeatCell': {
                'range': {'sheetId': sheet_gid, 'startRowIndex': row, 'endRowIndex': row + 1, 'startColumnIndex': 0, 'endColumnIndex': col_count},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': LIGHT_GRAY,
                        'textFormat': {'bold': True, 'fontSize': 11}
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }
    ]

def format_total_row(sheet_gid, row, col_count=6):
    """Format a total row"""
    return [
        {
            'repeatCell': {
                'range': {'sheetId': sheet_gid, 'startRowIndex': row, 'endRowIndex': row + 1, 'startColumnIndex': 0, 'endColumnIndex': col_count},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': TOTAL_BG,
                        'textFormat': {'bold': True, 'fontSize': 11}
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }
    ]

def format_transaction_tab(sheet_gid):
    """Format a transaction tab with standard headers"""
    return [
        # Header row formatting
        {
            'repeatCell': {
                'range': {'sheetId': sheet_gid, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': NAVY,
                        'textFormat': {'foregroundColor': WHITE, 'bold': True, 'fontSize': 11},
                        'horizontalAlignment': 'CENTER'
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
            }
        },
        # Freeze row 1
        {
            'updateSheetProperties': {
                'properties': {'sheetId': sheet_gid, 'gridProperties': {'frozenRowCount': 1}},
                'fields': 'gridProperties.frozenRowCount'
            }
        },
        # Column widths: 110 / 250 / 250 / 130 / 130 / 250
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 110}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2}, 'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3}, 'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4}, 'properties': {'pixelSize': 130}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5}, 'properties': {'pixelSize': 130}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6}, 'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
        # Row height for header
        {'updateDimensionProperties': {'range': {'sheetId': sheet_gid, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1}, 'properties': {'pixelSize': 30}, 'fields': 'pixelSize'}},
        # Default font size 10
        {
            'repeatCell': {
                'range': {'sheetId': sheet_gid, 'startRowIndex': 1, 'endRowIndex': 500, 'startColumnIndex': 0, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'textFormat': {'fontSize': 10}
                    }
                },
                'fields': 'userEnteredFormat.textFormat.fontSize'
            }
        }
    ]

# ============================================================
# SHEET IDs
# ============================================================
NOV_ID = '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0'
DEC_ID = '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo'
JAN_ID = '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE'

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    print(f"Running standardization for: {target}")
    print(f"Token: {TOKEN[:20]}...")

