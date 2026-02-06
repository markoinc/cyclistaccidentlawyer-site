#!/usr/bin/env python3
"""Fix navy header text color for a single sheet"""
import requests, json, time, sys

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
WHITE = {'red': 1, 'green': 1, 'blue': 1}

SHEETS = {
    'June 2025': '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg',
    'July 2025': '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8',
    'August 2025': '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI',
    'September 2025': '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM',
    'October 2025': '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA',
    'November 2025': '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0',
    'December 2025': '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo',
    'January 2026': '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE'
}

def is_navy(bg):
    if not bg: return False
    r = bg.get('red', 0)
    g = bg.get('green', 0)
    b = bg.get('blue', 0)
    return (abs(r - 0.106) < 0.06 and abs(g - 0.165) < 0.06 and abs(b - 0.290) < 0.06)

def is_white(fg):
    if not fg: return False
    return fg.get('red', 0) > 0.9 and fg.get('green', 0) > 0.9 and fg.get('blue', 0) > 0.9

def fix_sheet_tab(spreadsheet_id, sheet_id, sheet_title, month):
    """Fix navy headers for a single tab"""
    # Get grid data for this specific tab only
    url = (f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}'
           f'?ranges={sheet_title.replace(" ", "%20")}' 
           f'&fields=sheets(data(rowData(values(effectiveFormat(backgroundColor,textFormat(foregroundColor,foregroundColorStyle))))))')
    
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 200:
        # Try URL-encoded
        import urllib.parse
        encoded = urllib.parse.quote(sheet_title)
        url = (f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}'
               f'?ranges={encoded}'
               f'&fields=sheets(data(rowData(values(effectiveFormat(backgroundColor,textFormat(foregroundColor,foregroundColorStyle))))))')
        r = requests.get(url, headers=HEADERS)
    
    if r.status_code != 200:
        print(f"    Could not read tab '{sheet_title}': {r.status_code}")
        return 0
    
    data = r.json()
    fixes = []
    
    for sheet in data.get('sheets', []):
        for grid in sheet.get('data', []):
            for row_idx, row in enumerate(grid.get('rowData', [])):
                for col_idx, cell in enumerate(row.get('values', [])):
                    ef = cell.get('effectiveFormat', {})
                    bg = ef.get('backgroundColor', {})
                    tf = ef.get('textFormat', {})
                    fg = tf.get('foregroundColor', {})
                    fgs = tf.get('foregroundColorStyle', {}).get('rgbColor', {})
                    
                    actual_fg = fgs if fgs else fg
                    
                    if is_navy(bg) and not is_white(actual_fg):
                        fixes.append({
                            'repeatCell': {
                                'range': {
                                    'sheetId': sheet_id,
                                    'startRowIndex': row_idx,
                                    'endRowIndex': row_idx + 1,
                                    'startColumnIndex': col_idx,
                                    'endColumnIndex': col_idx + 1
                                },
                                'cell': {
                                    'userEnteredFormat': {
                                        'textFormat': {
                                            'foregroundColorStyle': {'rgbColor': WHITE}
                                        }
                                    }
                                },
                                'fields': 'userEnteredFormat.textFormat.foregroundColorStyle'
                            }
                        })
    
    if fixes:
        batch_url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate'
        # Send in batches
        for i in range(0, len(fixes), 50):
            batch = fixes[i:i+50]
            r = requests.post(batch_url, headers=HEADERS, json={'requests': batch})
            if r.status_code != 200:
                print(f"    Batch error: {r.status_code} {r.text[:100]}")
            time.sleep(0.5)
        print(f"    ✅ {sheet_title}: Fixed {len(fixes)} cells")
    else:
        print(f"    ✓ {sheet_title}: All good")
    
    return len(fixes)

def fix_month(month, spreadsheet_id):
    """Fix all tabs in a month's spreadsheet"""
    print(f"\n--- {month} ---")
    
    # Get tab metadata
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?fields=sheets(properties(sheetId,title))'
    r = requests.get(url, headers=HEADERS)
    tabs = r.json().get('sheets', [])
    
    total = 0
    for tab in tabs:
        sid = tab['properties']['sheetId']
        title = tab['properties']['title']
        count = fix_sheet_tab(spreadsheet_id, sid, title, month)
        total += count
        time.sleep(1)
    
    print(f"  Total fixed for {month}: {total}")
    return total

# Process specific month or all
if len(sys.argv) > 1:
    month = sys.argv[1]
    if month in SHEETS:
        fix_month(month, SHEETS[month])
    else:
        print(f"Unknown month: {month}")
else:
    grand_total = 0
    for month, sid in SHEETS.items():
        count = fix_month(month, sid)
        grand_total += count
        time.sleep(2)
    print(f"\n{'='*40}")
    print(f"Grand total cells fixed: {grand_total}")
