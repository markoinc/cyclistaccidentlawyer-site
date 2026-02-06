#!/usr/bin/env python3
"""
Fix Accountant View spreadsheet:
1. Branding fixes (tab colors, headers, red negatives, fonts, row heights)
2. Create missing tabs (Cash Flow, General Ledger, 1099 Tracking)
"""

import requests
import json
import csv
import re
from datetime import datetime
from collections import defaultdict

# ============================================================
# AUTH & CONFIG
# ============================================================
def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

TOKEN = get_token()
SHEET_ID = '1vtXJCdbWOskKU-zxEJCOlXBTVhd7vHclWEdWwJgFZ9o'
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
API_BASE = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}'

# Colors as RGB fractions
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}      # #1B2A4A
WHITE = {"red": 1.0, "green": 1.0, "blue": 1.0}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}  # #F3F3F3
LIGHT_NAVY = {"red": 0.910, "green": 0.929, "blue": 0.949}  # #E8EDF5
GREEN_TAB = {"red": 0.204, "green": 0.659, "blue": 0.325}   # #34A853
BLUE_TAB = {"red": 0.263, "green": 0.522, "blue": 0.957}    # #4285F4
ORANGE_TAB = {"red": 1.0, "green": 0.427, "blue": 0.004}    # #FF6D01
RED_TEXT = {"red": 0.8, "green": 0.0, "blue": 0.0}           # #CC0000

# Sheet IDs from metadata
SHEET_IDS = {
    'Summary': 0,
    'Chart of Accounts': 1,
    'Income Statement 2024': 7,
    'Income Statement 2025': 2,
    'Income Statement 2026': 3,
    'Schedule C Summary': 4,
    'Balance Sheet': 5,
    'Bank Reconciliation': 6,
}

# ============================================================
# HELPERS
# ============================================================
def color_obj(c):
    return {"red": c["red"], "green": c["green"], "blue": c["blue"]}

def batch_update(requests_list):
    """Execute a batch update."""
    body = {"requests": requests_list}
    r = requests.post(f'{API_BASE}:batchUpdate', headers=HEADERS, json=body)
    if r.status_code != 200:
        print(f"ERROR batch_update: {r.status_code}")
        print(r.text[:2000])
        return None
    return r.json()

def get_sheet_data(range_str):
    """Get values from a range."""
    import urllib.parse
    encoded = urllib.parse.quote(range_str)
    r = requests.get(f'{API_BASE}/values/{encoded}', headers=HEADERS)
    if r.status_code == 200:
        return r.json().get('values', [])
    return []

def update_values(range_str, values, value_input_option='USER_ENTERED'):
    """Update values in a range."""
    import urllib.parse
    encoded = urllib.parse.quote(range_str)
    body = {
        "values": values,
        "majorDimension": "ROWS"
    }
    r = requests.put(
        f'{API_BASE}/values/{encoded}?valueInputOption={value_input_option}',
        headers=HEADERS, json=body
    )
    if r.status_code != 200:
        print(f"ERROR update_values: {r.status_code} - {r.text[:500]}")
    return r.json() if r.status_code == 200 else None

def append_values(range_str, values, value_input_option='USER_ENTERED'):
    """Append values."""
    import urllib.parse
    encoded = urllib.parse.quote(range_str)
    body = {
        "values": values,
        "majorDimension": "ROWS"
    }
    r = requests.post(
        f'{API_BASE}/values/{encoded}:append?valueInputOption={value_input_option}&insertDataOption=INSERT_ROWS',
        headers=HEADERS, json=body
    )
    return r.json() if r.status_code == 200 else None

# ============================================================
# PART 1: BRANDING FIXES
# ============================================================
def build_branding_requests():
    reqs = []
    
    # ---- 1. Tab colors ----
    tab_colors = {
        'Summary': None,  # White/default
        'Chart of Accounts': NAVY,
        'Income Statement 2024': GREEN_TAB,
        'Income Statement 2025': GREEN_TAB,
        'Income Statement 2026': GREEN_TAB,
        'Schedule C Summary': ORANGE_TAB,
        'Balance Sheet': BLUE_TAB,
        'Bank Reconciliation': NAVY,
    }
    
    for tab_name, color in tab_colors.items():
        if color is not None:
            reqs.append({
                "updateSheetProperties": {
                    "properties": {
                        "sheetId": SHEET_IDS[tab_name],
                        "tabColorStyle": {"rgbColor": color_obj(color)}
                    },
                    "fields": "tabColorStyle"
                }
            })
    
    return reqs

def build_header_fix_requests():
    """Fix section headers from dark gray to navy, and fix row heights."""
    reqs = []
    
    # For each sheet, we need to find section header rows and fix their formatting.
    # Based on the audit, here are the known header rows:
    
    # Summary: Rows 1 (title), 3 (Entity Info header), 17 (Bank Accounts header), 26 (Notes header)
    # Chart of Accounts: Row 1 (title), 3 (header row)
    # Income Statements: Row 1-2 (title/subtitle), Row 4 (column headers)
    # Schedule C: Row 1-2 (title/subtitle), Row 4 (header)
    # Balance Sheet: Row 1-2 (title/subtitle)
    # Bank Reconciliation: Row 1-2 (title/subtitle), Row 4 (header)
    
    # I'll query each sheet to find exact header rows then apply formatting
    
    # Instead of hardcoding rows, let me define them based on my reading of the data:
    header_rows_map = {
        'Summary': {
            'section_headers': [0, 2, 16, 25],  # 0-indexed: title, entity info, bank accounts, notes
            'column_headers': [17],  # bank accounts column header row
        },
        'Chart of Accounts': {
            'section_headers': [0, 2],  # title, COA header
            'column_headers': [3],  # column header row (Acct#, Name, etc.)
            'category_headers': [5, 16, 22, 27, 32, 37],  # ASSETS, LIABILITIES, EQUITY, REVENUE, COGS, OPEX
        },
        'Income Statement 2024': {
            'section_headers': [0, 1],  # title, subtitle
            'column_headers': [3],      # month column headers
            'section_labels': [4, 6, 9, 13, 16, 18, 30, 33],  # REVENUE, TOTAL REV, COST, TOTAL COST, GROSS, OPEX, TOTAL OPEX, NET
        },
        'Income Statement 2025': {
            'section_headers': [0, 1],
            'column_headers': [3],
            'section_labels': [4, 6, 9, 13, 16, 18, 33, 36],
        },
        'Income Statement 2026': {
            'section_headers': [0, 1],
            'column_headers': [3],
            'section_labels': [4, 6, 9, 13, 16, 18, 30, 33],
        },
        'Schedule C Summary': {
            'section_headers': [0, 1],
            'column_headers': [3],
            'category_headers': [4, 8],  # INCOME, EXPENSES headers
        },
        'Balance Sheet': {
            'section_headers': [0, 1],
        },
        'Bank Reconciliation': {
            'section_headers': [0, 1],
            'column_headers': [3],
        },
    }
    
    return header_rows_map

def build_formatting_requests_for_sheet(sid, sheet_name, total_rows, total_cols):
    """Build formatting requests for a specific sheet."""
    reqs = []
    
    # ---- Global font: Arial 10pt for entire sheet ----
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": sid,
                "startRowIndex": 0,
                "endRowIndex": total_rows,
                "startColumnIndex": 0,
                "endColumnIndex": total_cols,
            },
            "cell": {
                "userEnteredFormat": {
                    "textFormat": {
                        "fontFamily": "Arial",
                        "fontSize": 10
                    }
                }
            },
            "fields": "userEnteredFormat.textFormat.fontFamily,userEnteredFormat.textFormat.fontSize"
        }
    })
    
    # ---- Default row height: 21px for all rows ----
    reqs.append({
        "updateDimensionProperties": {
            "range": {
                "sheetId": sid,
                "dimension": "ROWS",
                "startIndex": 0,
                "endIndex": total_rows,
            },
            "properties": {"pixelSize": 21},
            "fields": "pixelSize"
        }
    })
    
    return reqs

def format_section_header_row(sid, row_idx, end_col=14):
    """Format a section header row: navy bg, white bold 14pt text, 30px height."""
    return [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": end_col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color_obj(NAVY),
                        "textFormat": {
                            "foregroundColor": color_obj(WHITE),
                            "fontFamily": "Arial",
                            "fontSize": 14,
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sid,
                    "dimension": "ROWS",
                    "startIndex": row_idx,
                    "endIndex": row_idx + 1,
                },
                "properties": {"pixelSize": 30},
                "fields": "pixelSize"
            }
        }
    ]

def format_column_header_row(sid, row_idx, end_col=14):
    """Format a column/sub-header row: light gray bg, 11pt bold, 30px height."""
    return [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": end_col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color_obj(LIGHT_GRAY),
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
            }
        },
        {
            "updateDimensionProperties": {
                "range": {
                    "sheetId": sid,
                    "dimension": "ROWS",
                    "startIndex": row_idx,
                    "endIndex": row_idx + 1,
                },
                "properties": {"pixelSize": 30},
                "fields": "pixelSize"
            }
        }
    ]

def format_total_row(sid, row_idx, end_col=14):
    """Format a total row: light navy bg, 11pt bold."""
    return [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": end_col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color_obj(LIGHT_NAVY),
                        "textFormat": {
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
            }
        }
    ]

def format_category_header_row(sid, row_idx, end_col=14):
    """Format a category label row: navy bg, white bold 11pt, like ASSETS, LIABILITIES etc."""
    return [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": row_idx,
                    "endRowIndex": row_idx + 1,
                    "startColumnIndex": 0,
                    "endColumnIndex": end_col,
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": color_obj(NAVY),
                        "textFormat": {
                            "foregroundColor": color_obj(WHITE),
                            "fontFamily": "Arial",
                            "fontSize": 11,
                            "bold": True
                        }
                    }
                },
                "fields": "userEnteredFormat.backgroundColor,userEnteredFormat.textFormat"
            }
        }
    ]


# ============================================================
# PART 1A: Discover actual row structure by reading sheet data
# ============================================================
def discover_and_format_sheets():
    """Read each sheet, discover header/total rows, and build formatting requests."""
    all_reqs = []
    
    for sheet_name, sid in SHEET_IDS.items():
        print(f"Processing {sheet_name} (sid={sid})...")
        
        # Get data
        data = get_sheet_data(f"'{sheet_name}'!A1:Z100")
        if not data:
            print(f"  No data for {sheet_name}")
            continue
        
        num_rows = len(data)
        max_cols = max(len(row) for row in data) if data else 1
        end_col = min(max_cols + 1, 26)  # cap at Z
        
        # Base formatting: Arial 10pt, 21px rows
        all_reqs.extend(build_formatting_requests_for_sheet(sid, sheet_name, max(num_rows, 50), end_col))
        
        # Now discover rows by content
        for i, row in enumerate(data):
            if not row:
                continue
            
            first_cell = str(row[0]).strip() if row else ""
            
            # Title rows (row 0-1): "KuriosBrand LLC" or "For the Year"
            if i <= 1 and ('KuriosBrand' in first_cell or 'For the' in first_cell or 
                          'IRS Schedule' in first_cell or 'Monthly Snapshots' in first_cell or
                          'Comparison' in first_cell):
                all_reqs.extend(format_section_header_row(sid, i, end_col))
                continue
            
            # Section headers in Summary
            if sheet_name == 'Summary':
                if first_cell in ('Entity Information', 'Bank Accounts & Financial Institutions', 'Notes'):
                    all_reqs.extend(format_section_header_row(sid, i, end_col))
                elif first_cell == 'Account' and len(row) > 3:
                    all_reqs.extend(format_column_header_row(sid, i, end_col))
            
            # Chart of Accounts
            elif sheet_name == 'Chart of Accounts':
                if first_cell == 'Chart of Accounts — KuriosBrand LLC':
                    all_reqs.extend(format_section_header_row(sid, i, end_col))
                elif first_cell == 'Account #':
                    all_reqs.extend(format_column_header_row(sid, i, end_col))
                elif first_cell in ('ASSETS', 'LIABILITIES', 'EQUITY', 'REVENUE', 
                                    'COST OF GOODS SOLD', 'OPERATING EXPENSES', 'PERSONAL'):
                    all_reqs.extend(format_category_header_row(sid, i, end_col))
            
            # Income Statements
            elif 'Income Statement' in sheet_name:
                # Column header row (Jan, Feb, Mar...)
                if len(row) > 2 and str(row[1]).strip() in ('Jan', 'Feb', 'Jun'):
                    all_reqs.extend(format_column_header_row(sid, i, end_col))
                
                # Section labels that are like total rows
                if 'TOTAL' in first_cell.upper():
                    all_reqs.extend(format_total_row(sid, i, end_col))
                elif first_cell in ('GROSS PROFIT', 'NET INCOME', 'NET OPERATING INCOME'):
                    all_reqs.extend(format_total_row(sid, i, end_col))
                elif first_cell in ('REVENUE', 'COST OF REVENUE', 'OPERATING EXPENSES'):
                    all_reqs.extend(format_category_header_row(sid, i, end_col))
            
            # Schedule C
            elif sheet_name == 'Schedule C Summary':
                if first_cell == 'Line':
                    all_reqs.extend(format_column_header_row(sid, i, end_col))
                elif first_cell in ('INCOME', 'EXPENSES'):
                    all_reqs.extend(format_category_header_row(sid, i, end_col))
                elif 'TOTAL' in first_cell.upper() or 'NET PROFIT' in first_cell.upper():
                    all_reqs.extend(format_total_row(sid, i, end_col))
            
            # Balance Sheet
            elif sheet_name == 'Balance Sheet':
                if first_cell in ('ASSETS', 'EQUITY', 'LIABILITIES'):
                    all_reqs.extend(format_category_header_row(sid, i, end_col))
                elif 'Total' in first_cell or 'TOTAL' in first_cell:
                    all_reqs.extend(format_total_row(sid, i, end_col))
            
            # Bank Reconciliation
            elif sheet_name == 'Bank Reconciliation':
                if first_cell == 'Month':
                    all_reqs.extend(format_column_header_row(sid, i, end_col))
    
    return all_reqs

def build_currency_format_requests():
    """Apply red-negative currency format to all currency cells in income statements."""
    reqs = []
    
    # Income Statement sheets: currency cells are columns B through N (indices 1-13) 
    # for data rows (skip header rows)
    currency_format = {
        "type": "NUMBER",
        "pattern": "$#,##0.00;[Red]($#,##0.00)"
    }
    
    for sheet_name in ['Income Statement 2024', 'Income Statement 2025', 'Income Statement 2026']:
        sid = SHEET_IDS[sheet_name]
        # Apply currency format to B5:N40 (rows 4-39, cols 1-13)
        reqs.append({
            "repeatCell": {
                "range": {
                    "sheetId": sid,
                    "startRowIndex": 4,
                    "endRowIndex": 40,
                    "startColumnIndex": 1,
                    "endColumnIndex": 14,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": currency_format
                    }
                },
                "fields": "userEnteredFormat.numberFormat"
            }
        })
    
    # Schedule C: columns C, D, E (2025 Total, 2026 YTD) - indices 2-4
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": SHEET_IDS['Schedule C Summary'],
                "startRowIndex": 4,
                "endRowIndex": 35,
                "startColumnIndex": 2,
                "endColumnIndex": 5,
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": currency_format
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    # Balance Sheet: all numeric columns
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": SHEET_IDS['Balance Sheet'],
                "startRowIndex": 4,
                "endRowIndex": 25,
                "startColumnIndex": 1,
                "endColumnIndex": 26,
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": currency_format
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    # Bank Reconciliation: currency columns
    reqs.append({
        "repeatCell": {
            "range": {
                "sheetId": SHEET_IDS['Bank Reconciliation'],
                "startRowIndex": 4,
                "endRowIndex": 15,
                "startColumnIndex": 1,
                "endColumnIndex": 10,
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": currency_format
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    return reqs

def build_percentage_format_requests():
    """Apply 0.0% format to percentage rows."""
    reqs = []
    pct_format = {"type": "NUMBER", "pattern": "0.0%"}
    
    # Income Statements have margin % rows. We need to find them.
    # Based on the data: Gross Margin %, Net Margin % rows
    # These are the rows after GROSS PROFIT and NET INCOME
    for sheet_name in ['Income Statement 2024', 'Income Statement 2025', 'Income Statement 2026']:
        sid = SHEET_IDS[sheet_name]
        data = get_sheet_data(f"'{sheet_name}'!A1:A40")
        for i, row in enumerate(data):
            if row and 'Margin %' in str(row[0]):
                reqs.append({
                    "repeatCell": {
                        "range": {
                            "sheetId": sid,
                            "startRowIndex": i,
                            "endRowIndex": i + 1,
                            "startColumnIndex": 1,
                            "endColumnIndex": 14,
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "numberFormat": pct_format
                            }
                        },
                        "fields": "userEnteredFormat.numberFormat"
                    }
                })
    
    return reqs

# ============================================================
# PART 2: CSV DATA PARSING
# ============================================================
def parse_csv(filepath):
    """Parse Chase CSV and return list of dicts."""
    records = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records

def parse_date(date_str):
    """Parse MM/DD/YYYY date string."""
    try:
        return datetime.strptime(date_str.strip(), '%m/%d/%Y')
    except:
        return None

def load_all_csvs():
    """Load all CSV transaction data."""
    biz = parse_csv('/home/ec2-user/clawd/data/chase-exports/business-4991-alltime.csv')
    personal = parse_csv('/home/ec2-user/clawd/data/chase-exports/personal-0068-alltime.csv')
    bizcc = parse_csv('/home/ec2-user/clawd/data/chase-exports/bizcc-0678-alltime.csv')
    sapphire = parse_csv('/home/ec2-user/clawd/data/chase-exports/sapphire-4252-alltime.csv')
    return biz, personal, bizcc, sapphire

def get_amount(row, account_type='checking'):
    """Extract amount from a row."""
    if account_type == 'checking':
        return float(row.get('Amount', 0))
    else:
        return float(row.get('Amount', 0))

def get_date(row, account_type='checking'):
    """Get posting date from row."""
    if account_type == 'checking':
        return parse_date(row.get('Posting Date', ''))
    else:
        return parse_date(row.get('Post Date', '') or row.get('Transaction Date', ''))

def categorize_biz_transaction(desc, amount):
    """Categorize a business checking transaction."""
    desc_upper = desc.upper()
    
    # Revenue (credits)
    if amount > 0:
        if 'TRANSFER' in desc_upper and ('CHK' in desc_upper or 'SAV' in desc_upper):
            return 'Transfer In', '1000'
        if 'STRIPE' in desc_upper:
            return 'Service Revenue', '4000'
        if 'ZELLE' in desc_upper:
            return 'Service Revenue', '4000'
        if any(w in desc_upper for w in ['DEPOSIT', 'CREDIT']):
            return 'Service Revenue', '4000'
        return 'Other Income', '4020'
    
    # Expenses (debits)
    if 'TRANSFER' in desc_upper and ('CHK' in desc_upper or 'SAV' in desc_upper):
        return 'Transfer Out', '3100'
    if 'FACEBK' in desc_upper or 'META' in desc_upper or 'FACEBOOK' in desc_upper:
        return 'Advertising - Meta/Facebook', '5000'
    if 'GOOGLE' in desc_upper and ('ADS' in desc_upper or 'ADWORDS' in desc_upper or 'AD' in desc_upper):
        return 'Advertising - Google Ads', '5010'
    if 'GOOGLE' in desc_upper and 'DOMAINS' in desc_upper:
        return 'Domains & Hosting', '6130'
    if 'HIGHLEVEL' in desc_upper or 'GOHIGHLEVEL' in desc_upper:
        return 'SaaS & Software', '6000'
    if any(w in desc_upper for w in ['OPENAI', 'ANTHROPIC', 'CHATGPT', 'CURSOR', 'GITHUB', 
                                       'NOTION', 'ZAPIER', 'MAKE.COM', 'AIRTABLE',
                                       'SEMRUSH', 'AHREFS', 'CANVA', 'FIGMA', 'SLACK',
                                       'LEMLIST', 'INSTANTLY', 'TWILIO', 'STRIPE FEE',
                                       'CALENDLY', 'ZOOM', 'LOOM', 'GRAMMARLY',
                                       'NAMECHEAP', 'CLOUDFLARE', 'VERCEL', 'NETLIFY',
                                       'HEROKU', 'DIGITAL OCEAN', 'AWS', 'AZURE',
                                       'BRAVE.COM', 'CALLRAIL', 'CLOSE.COM', 'HUBSPOT']):
        return 'SaaS & Software', '6000'
    if any(w in desc_upper for w in ['REGUS', 'COWORK', 'WEWORK', 'MAILBOX']):
        return 'Office & Coworking', '6020'
    if any(w in desc_upper for w in ['T-MOBILE', 'VERIZON', 'AIRALO', 'MINT MOBILE']):
        return 'Telecommunications', '6030'
    if any(w in desc_upper for w in ['SPECTRUM', 'COMCAST', 'AT&T INTERNET']):
        return 'Internet Service', '6040'
    if any(w in desc_upper for w in ['HARBOR COMPLIANCE', 'WI DFI', 'REGISTERED AGENT',
                                       'LEGALZOOM', 'INCFILE']):
        return 'Professional Services', '6050'
    if any(w in desc_upper for w in ['MONTHLY SERVICE FEE', 'SERVICE CHARGE', 'MAINTENANCE FEE',
                                       'WIRE FEE', 'OVERDRAFT']):
        return 'Bank Fees & Interest', '6060'
    if 'INTEREST CHARGE' in desc_upper:
        return 'Credit Card Interest', '6070'
    if any(w in desc_upper for w in ['SAFETYWING', 'TRIWEST', 'TRICARE', 'INSURANCE']):
        return 'Insurance', '6080'
    if any(w in desc_upper for w in ['UDEMY', 'COURSERA', 'SKILLSHARE', 'MASTERCLASS']):
        return 'Education & Training', '6140'
    if 'ZELLE' in desc_upper and amount < 0:
        return 'Contractor Labor', '6120'
    if any(w in desc_upper for w in ['WISE', 'PAYPAL', 'VENMO']) and amount < 0:
        return 'Contractor Labor', '6120'
    if any(w in desc_upper for w in ['ATM', 'CASH ADVANCE']):
        return 'ATM / Cash', '6150'
    if 'STRIPE CAPITAL' in desc_upper or 'LOAN' in desc_upper:
        return 'Loan Repayment', '6110'
    if any(w in desc_upper for w in ['DOMAIN', 'NAMECHEAP', 'GODADDY', 'HOSTINGER', 
                                       'SITEGROUND', 'BLUEHOST']):
        return 'Domains & Hosting', '6130'
    
    return 'Miscellaneous', '6150'

def categorize_bizcc_transaction(desc, amount, category_hint=''):
    """Categorize a business credit card transaction."""
    desc_upper = desc.upper()
    cat_upper = category_hint.upper()
    
    if amount > 0:
        return 'CC Payment', '2000'
    
    if 'FACEBK' in desc_upper or 'META' in desc_upper or 'FACEBOOK' in desc_upper:
        return 'Advertising - Meta/Facebook', '5000'
    if 'GOOGLE' in desc_upper and 'ADS' in desc_upper:
        return 'Advertising - Google Ads', '5010'
    if 'INTEREST' in desc_upper:
        return 'Credit Card Interest', '6070'
    if any(w in desc_upper for w in ['OPENAI', 'ANTHROPIC', 'CHATGPT', 'CURSOR', 'GITHUB',
                                       'NOTION', 'ZAPIER', 'MAKE.COM', 'SEMRUSH', 'AHREFS',
                                       'CANVA', 'SLACK', 'LEMLIST', 'INSTANTLY', 'TWILIO',
                                       'CALENDLY', 'ZOOM', 'LOOM', 'BRAVE.COM', 'CALLRAIL',
                                       'HIGHLEVEL', 'CLOSE.COM', 'HUBSPOT', 'GRAMMARLY']):
        return 'SaaS & Software', '6000'
    if any(w in desc_upper for w in ['NAMECHEAP', 'GODADDY', 'CLOUDFLARE', 'DOMAIN',
                                       'HOSTINGER', 'GOOGLE DOMAINS']):
        return 'Domains & Hosting', '6130'
    if 'PROFESSIONAL' in cat_upper:
        if 'FACEBK' in desc_upper:
            return 'Advertising - Meta/Facebook', '5000'
        return 'Professional Services', '6050'
    
    return 'Miscellaneous', '6150'

# ============================================================
# PART 3: BUILD CASH FLOW STATEMENT
# ============================================================
def build_cash_flow_data():
    """Build cash flow statement data for 2024, 2025, 2026."""
    biz, personal, bizcc, sapphire = load_all_csvs()
    
    # Net income from the Income Statements (already verified)
    net_income = {
        2024: -2567.10,
        2025: 43239.89,
        2026: -169.92,
    }
    
    # For cash flow, we need:
    # Operating: Net income + non-cash adjustments (for cash basis, minimal)
    # Investing: Equipment, investments
    # Financing: Loans, owner draws/contributions
    
    # Parse business checking for financing activities
    financing_by_year = defaultdict(lambda: {
        'loan_proceeds': 0.0,
        'loan_payments': 0.0,
        'owner_draws': 0.0,
        'owner_contributions': 0.0,
    })
    
    investing_by_year = defaultdict(lambda: {
        'investments': 0.0,
        'equipment': 0.0,
    })
    
    for row in biz:
        dt = get_date(row, 'checking')
        if not dt:
            continue
        year = dt.year
        amt = get_amount(row, 'checking')
        desc = row.get('Description', '').upper()
        
        # Owner draws (transfers to personal)
        if 'TRANSFER' in desc and '0068' in desc and amt < 0:
            financing_by_year[year]['owner_draws'] += amt
        
        # Owner contributions (transfers from personal) 
        if 'TRANSFER' in desc and '0068' in desc and amt > 0:
            financing_by_year[year]['owner_contributions'] += amt
        
        # Loan proceeds
        if 'STRIPE' in desc and 'CAPITAL' in desc and amt > 0:
            financing_by_year[year]['loan_proceeds'] += amt
        if ('LOAN' in desc or 'STRIPE CAPITAL' in desc) and amt > 0 and 'TRANSFER' not in desc:
            if amt > 1000:  # Loan disbursement
                financing_by_year[year]['loan_proceeds'] += amt
        
        # Loan payments
        if 'STRIPE' in desc and amt < 0 and ('CAPITAL' in desc or 'LOAN' in desc):
            financing_by_year[year]['loan_payments'] += amt
    
    # Check for Stripe Capital loan ($4200 in Jan 2026)
    # Already counted in the loop above from transfers
    
    # For personal account - investment flows
    for row in personal:
        dt = get_date(row, 'checking')
        if not dt:
            continue
        year = dt.year
        amt = get_amount(row, 'checking')
        desc = row.get('Description', '').upper()
        
        if any(w in desc for w in ['ROBINHOOD', 'ACORNS', 'COINBASE', 'CRYPTO']):
            investing_by_year[year]['investments'] += amt
    
    # Build the data structure
    cash_flow = {}
    
    # Get beginning cash balances from business checking
    biz_sorted = sorted(biz, key=lambda r: get_date(r, 'checking') or datetime(2020,1,1))
    
    # Calculate annual cash changes from business checking
    cash_changes = defaultdict(float)
    for row in biz_sorted:
        dt = get_date(row, 'checking')
        if not dt:
            continue
        cash_changes[dt.year] += get_amount(row, 'checking')
    
    for year in [2024, 2025, 2026]:
        ni = net_income.get(year, 0)
        fin = financing_by_year[year]
        inv = investing_by_year[year]
        
        # Operating activities = Net Income (cash basis, so minimal adjustments)
        operating_total = ni
        
        # Investing (personal investments are NOT in business cash flow, skip)
        investing_total = 0
        
        # Financing
        financing_total = fin['loan_proceeds'] + fin['loan_payments'] + fin['owner_draws'] + fin['owner_contributions']
        
        net_change = operating_total + investing_total + financing_total
        
        cash_flow[year] = {
            'net_income': ni,
            'operating_total': operating_total,
            'investing_total': investing_total,
            'loan_proceeds': fin['loan_proceeds'],
            'loan_payments': fin['loan_payments'],
            'owner_draws': fin['owner_draws'],
            'owner_contributions': fin['owner_contributions'],
            'financing_total': financing_total,
            'net_change': net_change,
        }
    
    return cash_flow

# ============================================================
# PART 4: BUILD GENERAL LEDGER
# ============================================================
def build_general_ledger_data():
    """Build general ledger with all transactions categorized by GL account."""
    biz, personal, bizcc, sapphire = load_all_csvs()
    
    gl_entries = []
    
    # Business checking (4991)
    for row in biz:
        dt = get_date(row, 'checking')
        if not dt:
            continue
        amt = get_amount(row, 'checking')
        desc = row.get('Description', '').strip()
        # Clean description
        desc_clean = re.sub(r'\s+', ' ', desc)[:80]
        
        cat, gl_acct = categorize_biz_transaction(desc, amt)
        
        gl_entries.append({
            'date': dt,
            'account': gl_acct,
            'category': cat,
            'description': desc_clean,
            'debit': abs(amt) if amt < 0 else 0,
            'credit': amt if amt > 0 else 0,
            'source': 'Biz Checking 4991',
        })
    
    # Business CC (0678)
    for row in bizcc:
        dt = get_date(row, 'cc')
        if not dt:
            continue
        amt = get_amount(row, 'cc')
        desc = row.get('Description', '').strip()
        desc_clean = re.sub(r'\s+', ' ', desc)[:80]
        cat_hint = row.get('Category', '')
        
        cat, gl_acct = categorize_bizcc_transaction(desc, amt, cat_hint)
        
        gl_entries.append({
            'date': dt,
            'account': gl_acct,
            'category': cat,
            'description': desc_clean,
            'debit': abs(amt) if amt < 0 else 0,
            'credit': amt if amt > 0 else 0,
            'source': 'Biz CC 0678',
        })
    
    # Sort by date, then account
    gl_entries.sort(key=lambda x: (x['account'], x['date']))
    
    return gl_entries

# ============================================================
# PART 5: BUILD 1099 TRACKING
# ============================================================
def build_1099_data():
    """Find all vendor/contractor payments > $600 per calendar year that would need 1099."""
    biz, personal, bizcc, sapphire = load_all_csvs()
    
    # Track payments to individuals/contractors
    vendor_payments = defaultdict(lambda: defaultdict(float))
    vendor_details = defaultdict(list)
    
    # Patterns that indicate contractor/individual payments
    contractor_indicators = ['ZELLE', 'WISE', 'PAYPAL', 'VENMO']
    
    # Exclude patterns (not contractors)
    exclude_patterns = ['TRANSFER TO', 'TRANSFER FROM', 'ONLINE TRANSFER', 'CREDIT CARD',
                       'STRIPE', 'ROBINHOOD', 'ACORNS', 'COINBASE', 'ATM', 'WELLS FARGO']
    
    for row in biz:
        dt = get_date(row, 'checking')
        if not dt:
            continue
        amt = get_amount(row, 'checking')
        if amt >= 0:
            continue  # Only debits
        
        desc = row.get('Description', '').strip()
        desc_upper = desc.upper()
        
        # Skip excluded patterns
        if any(exc in desc_upper for exc in exclude_patterns):
            continue
        
        # Look for Zelle payments (most likely to be contractor payments)
        if 'ZELLE' in desc_upper:
            # Extract recipient name from Zelle description
            # Typical format: "ORIG CO NAME:name ZELLE" or "Zelle payment to NAME"
            name = extract_zelle_name(desc)
            if name:
                vendor_payments[name][dt.year] += abs(amt)
                vendor_details[name].append({
                    'date': dt.strftime('%m/%d/%Y'),
                    'amount': abs(amt),
                    'description': desc[:80],
                    'source': 'Biz 4991'
                })
        
        # PayPal, Wise payments
        elif any(w in desc_upper for w in ['PAYPAL', 'WISE']):
            name = extract_payment_name(desc)
            if name:
                vendor_payments[name][dt.year] += abs(amt)
                vendor_details[name].append({
                    'date': dt.strftime('%m/%d/%Y'),
                    'amount': abs(amt),
                    'description': desc[:80],
                    'source': 'Biz 4991'
                })
    
    # Filter to > $600 in any year
    qualifying_vendors = {}
    for vendor, yearly in vendor_payments.items():
        for year, total in yearly.items():
            if total >= 600:
                if vendor not in qualifying_vendors:
                    qualifying_vendors[vendor] = {}
                qualifying_vendors[vendor][year] = total
    
    return qualifying_vendors, vendor_details

def extract_zelle_name(desc):
    """Extract recipient name from Zelle payment description."""
    desc_clean = re.sub(r'\s+', ' ', desc)
    
    # Pattern: "Zelle payment to NAME" or "ZELLE ... NAME"
    # Chase format: "ORIG CO NAME:MARK GUNDRUM    CO ENTRY DESCR:ZELLE"
    # or: "Zelle payment to John Doe"
    
    patterns = [
        r'Zelle\s+(?:payment\s+)?(?:to|from)\s+(.+?)(?:\s+(?:TRANSACTION|$))',
        r'ORIG CO NAME:(.+?)\s+CO ENTRY',
        r'ZELLE\s+(?:PAYMENT|SEND).*?(?:TO|FROM)\s+(.+?)(?:\s+(?:CONFIRM|TRANSACTION|$))',
    ]
    
    for pat in patterns:
        match = re.search(pat, desc_clean, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            # Clean up
            name = re.sub(r'\s+', ' ', name).strip()
            if len(name) > 3 and name.upper() != 'MARK GUNDRUM':
                return name
    
    # Try to extract from the description more broadly
    if 'ZELLE' in desc.upper():
        # Look for a name pattern
        match = re.search(r'(?:TO|FROM)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', desc)
        if match:
            name = match.group(1).strip()
            if name.upper() != 'MARK GUNDRUM':
                return name
    
    return None

def extract_payment_name(desc):
    """Extract name from PayPal/Wise description."""
    desc_clean = re.sub(r'\s+', ' ', desc)
    
    patterns = [
        r'PAYPAL\s+\*(.+?)(?:\s+\d|$)',
        r'WISE\s+(.+?)(?:\s+\d|$)',
    ]
    
    for pat in patterns:
        match = re.search(pat, desc_clean, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    
    return None

# ============================================================
# PART 6: CREATE NEW TABS AND POPULATE
# ============================================================
def create_new_tabs():
    """Create Cash Flow, General Ledger, and 1099 Tracking tabs."""
    reqs = []
    
    # Cash Flow Statement (sheetId 100)
    reqs.append({
        "addSheet": {
            "properties": {
                "sheetId": 100,
                "title": "Cash Flow Statement",
                "index": 7,  # After Balance Sheet
                "tabColorStyle": {"rgbColor": color_obj(BLUE_TAB)},
                "gridProperties": {
                    "rowCount": 200,
                    "columnCount": 10,
                    "frozenRowCount": 2
                }
            }
        }
    })
    
    # General Ledger (sheetId 101)
    reqs.append({
        "addSheet": {
            "properties": {
                "sheetId": 101,
                "title": "General Ledger",
                "index": 9,  # After Schedule C
                "tabColorStyle": {"rgbColor": color_obj(NAVY)},
                "gridProperties": {
                    "rowCount": 5000,
                    "columnCount": 10,
                    "frozenRowCount": 1
                }
            }
        }
    })
    
    # 1099 Tracking (sheetId 102)
    reqs.append({
        "addSheet": {
            "properties": {
                "sheetId": 102,
                "title": "1099 Tracking",
                "index": 10,
                "tabColorStyle": {"rgbColor": color_obj(ORANGE_TAB)},
                "gridProperties": {
                    "rowCount": 200,
                    "columnCount": 10,
                    "frozenRowCount": 3
                }
            }
        }
    })
    
    return reqs

def populate_cash_flow():
    """Populate Cash Flow Statement tab."""
    cash_flow = build_cash_flow_data()
    
    rows = [
        ["KuriosBrand LLC — Statement of Cash Flows"],
        ["For the Years 2024, 2025, and 2026 YTD"],
        [""],
        ["", "2024", "2025", "2026 YTD"],
        ["OPERATING ACTIVITIES"],
        ["  Net Income", cash_flow[2024]['net_income'], cash_flow[2025]['net_income'], cash_flow[2026]['net_income']],
        ["  Adjustments to reconcile:"],
        ["    (Cash basis - no non-cash adjustments)", 0, 0, 0],
        ["NET CASH FROM OPERATING ACTIVITIES", cash_flow[2024]['operating_total'], cash_flow[2025]['operating_total'], cash_flow[2026]['operating_total']],
        [""],
        ["INVESTING ACTIVITIES"],
        ["  Equipment Purchases", 0, 0, 0],
        ["  Other Investments", 0, 0, 0],
        ["NET CASH FROM INVESTING ACTIVITIES", cash_flow[2024]['investing_total'], cash_flow[2025]['investing_total'], cash_flow[2026]['investing_total']],
        [""],
        ["FINANCING ACTIVITIES"],
        ["  Loan Proceeds (Stripe Capital)", cash_flow[2024]['loan_proceeds'], cash_flow[2025]['loan_proceeds'], cash_flow[2026]['loan_proceeds']],
        ["  Loan Repayments", cash_flow[2024]['loan_payments'], cash_flow[2025]['loan_payments'], cash_flow[2026]['loan_payments']],
        ["  Owner Draws (Transfers to Personal)", cash_flow[2024]['owner_draws'], cash_flow[2025]['owner_draws'], cash_flow[2026]['owner_draws']],
        ["  Owner Contributions (Transfers from Personal)", cash_flow[2024]['owner_contributions'], cash_flow[2025]['owner_contributions'], cash_flow[2026]['owner_contributions']],
        ["NET CASH FROM FINANCING ACTIVITIES", cash_flow[2024]['financing_total'], cash_flow[2025]['financing_total'], cash_flow[2026]['financing_total']],
        [""],
        ["NET CHANGE IN CASH", cash_flow[2024]['net_change'], cash_flow[2025]['net_change'], cash_flow[2026]['net_change']],
        [""],
        ["Notes:"],
        ["1. KuriosBrand uses cash basis accounting; operating activities equal net income."],
        ["2. Stripe Capital loan of $4,200 disbursed January 23, 2026 (total repayment: $5,035)."],
        ["3. Owner draws represent transfers from business checking to personal checking."],
        ["4. No significant investing activities for the periods presented."],
    ]
    
    return rows

def populate_general_ledger():
    """Populate General Ledger tab."""
    gl_entries = build_general_ledger_data()
    
    rows = [
        ["GL Acct", "Account Name", "Date", "Description", "Debit", "Credit", "Source"],
    ]
    
    # Group by GL account
    current_acct = None
    for entry in gl_entries:
        acct = entry['account']
        
        # Add section header when account changes
        if acct != current_acct:
            current_acct = acct
            rows.append([])  # blank separator
            rows.append([acct, entry['category'], "", "", "", "", ""])
        
        rows.append([
            acct,
            entry['category'],
            entry['date'].strftime('%m/%d/%Y'),
            entry['description'],
            f"={entry['debit']}" if entry['debit'] > 0 else "",
            f"={entry['credit']}" if entry['credit'] > 0 else "",
            entry['source'],
        ])
    
    return rows

def populate_1099_tracking():
    """Populate 1099 Tracking tab."""
    qualifying, details = build_1099_data()
    
    rows = [
        ["KuriosBrand LLC — 1099-NEC Tracking"],
        ["Vendors/Contractors Paid >= $600 in a Calendar Year"],
        [""],
        ["Vendor/Contractor", "2024 Total", "2025 Total", "2026 YTD", "1099 Required?", "TIN on File?", "Notes"],
    ]
    
    if not qualifying:
        rows.append(["No qualifying vendors found above $600 threshold.", "", "", "", "", "", ""])
        rows.append([""])
        rows.append(["Note: Review Zelle payments, Wise transfers, and PayPal payments manually."])
        rows.append(["Chase Zelle descriptions may not always clearly identify recipients."])
    else:
        for vendor, yearly_totals in sorted(qualifying.items()):
            rows.append([
                vendor,
                yearly_totals.get(2024, 0),
                yearly_totals.get(2025, 0),
                yearly_totals.get(2026, 0),
                "Yes" if any(v >= 600 for v in yearly_totals.values()) else "Review",
                "No",
                ""
            ])
    
    rows.append([""])
    rows.append(["DETAILED PAYMENT LOG"])
    rows.append(["Vendor", "Date", "Amount", "Description", "Account"])
    
    for vendor, txns in sorted(details.items()):
        for txn in sorted(txns, key=lambda x: x['date']):
            rows.append([
                vendor,
                txn['date'],
                txn['amount'],
                txn['description'],
                txn['source'],
            ])
    
    rows.append([""])
    rows.append(["Notes:"])
    rows.append(["1. 1099-NEC required for non-corporate contractors paid >= $600 in a calendar year."])
    rows.append(["2. Corporations (LLC taxed as Corp, S-Corp, C-Corp) are generally exempt."])
    rows.append(["3. Request W-9 from all contractors before first payment."])
    rows.append(["4. File 1099-NEC by January 31 of the following year."])
    rows.append(["5. Some Zelle payments may not parse vendor names - review manually."])
    
    return rows

def format_new_tab(sid, data_rows, end_col=8):
    """Build formatting requests for a new tab."""
    reqs = []
    
    # Global font
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": len(data_rows) + 5,
                      "startColumnIndex": 0, "endColumnIndex": end_col},
            "cell": {"userEnteredFormat": {"textFormat": {"fontFamily": "Arial", "fontSize": 10}}},
            "fields": "userEnteredFormat.textFormat.fontFamily,userEnteredFormat.textFormat.fontSize"
        }
    })
    
    # Default row heights
    reqs.append({
        "updateDimensionProperties": {
            "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": 0, "endIndex": len(data_rows) + 5},
            "properties": {"pixelSize": 21},
            "fields": "pixelSize"
        }
    })
    
    return reqs

def format_cash_flow_tab():
    """Format Cash Flow Statement tab."""
    sid = 100
    reqs = []
    
    # Title rows (0-1): navy header
    reqs.extend(format_section_header_row(sid, 0, 5))
    reqs.extend(format_section_header_row(sid, 1, 5))
    
    # Column headers (row 3)
    reqs.extend(format_column_header_row(sid, 3, 5))
    
    # Section headers: OPERATING, INVESTING, FINANCING
    section_rows = [4, 10, 15]
    for r in section_rows:
        reqs.extend(format_category_header_row(sid, r, 5))
    
    # Total rows
    total_rows = [8, 13, 20, 22]
    for r in total_rows:
        reqs.extend(format_total_row(sid, r, 5))
    
    # Currency format for data cells
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 25,
                      "startColumnIndex": 1, "endColumnIndex": 4},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "$#,##0.00;[Red]($#,##0.00)"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    # Row heights for headers
    for r in [0, 1]:
        reqs.append({
            "updateDimensionProperties": {
                "range": {"sheetId": sid, "dimension": "ROWS", "startIndex": r, "endIndex": r+1},
                "properties": {"pixelSize": 30},
                "fields": "pixelSize"
            }
        })
    
    return reqs

def format_general_ledger_tab(num_rows):
    """Format General Ledger tab."""
    sid = 101
    reqs = []
    
    # Column header (row 0)
    reqs.extend(format_column_header_row(sid, 0, 7))
    
    # Currency format for debit/credit columns (E, F = indices 4, 5)
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": num_rows,
                      "startColumnIndex": 4, "endColumnIndex": 6},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "$#,##0.00;[Red]($#,##0.00)"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    return reqs

def format_1099_tab():
    """Format 1099 Tracking tab."""
    sid = 102
    reqs = []
    
    # Title rows (0-1)
    reqs.extend(format_section_header_row(sid, 0, 7))
    reqs.extend(format_section_header_row(sid, 1, 7))
    
    # Column header row (row 3)
    reqs.extend(format_column_header_row(sid, 3, 7))
    
    # Currency format
    reqs.append({
        "repeatCell": {
            "range": {"sheetId": sid, "startRowIndex": 4, "endRowIndex": 50,
                      "startColumnIndex": 1, "endColumnIndex": 4},
            "cell": {"userEnteredFormat": {"numberFormat": {"type": "NUMBER", "pattern": "$#,##0.00;[Red]($#,##0.00)"}}},
            "fields": "userEnteredFormat.numberFormat"
        }
    })
    
    return reqs


# ============================================================
# PART 7: Also need to scan biz transactions for Zelle more carefully
# ============================================================
def analyze_zelle_payments():
    """Deep scan of Zelle payments from business checking."""
    biz = parse_csv('/home/ec2-user/clawd/data/chase-exports/business-4991-alltime.csv')
    
    zelle_payments = []
    for row in biz:
        desc = row.get('Description', '')
        if 'ZELLE' in desc.upper() or 'Zelle' in desc:
            dt = get_date(row, 'checking')
            amt = get_amount(row, 'checking')
            if amt < 0:  # Outgoing
                zelle_payments.append({
                    'date': dt,
                    'amount': abs(amt),
                    'description': re.sub(r'\s+', ' ', desc.strip())[:120],
                    'year': dt.year if dt else 0,
                })
    
    return zelle_payments


# ============================================================
# MAIN EXECUTION
# ============================================================
def main():
    print("=" * 60)
    print("FIXING ACCOUNTANT VIEW SPREADSHEET")
    print("=" * 60)
    
    # ---- Step 1: Apply branding fixes to existing tabs ----
    print("\n--- Step 1: Building branding requests ---")
    all_reqs = []
    
    # Tab colors
    all_reqs.extend(build_branding_requests())
    print(f"  Tab color requests: {len(all_reqs)}")
    
    # Execute tab colors first
    if all_reqs:
        result = batch_update(all_reqs)
        print(f"  Tab colors applied: {'OK' if result else 'FAILED'}")
    
    # ---- Step 2: Discover and format sheet headers/rows ----
    print("\n--- Step 2: Formatting existing sheets ---")
    format_reqs = discover_and_format_sheets()
    print(f"  Formatting requests: {len(format_reqs)}")
    
    # Add currency format
    currency_reqs = build_currency_format_requests()
    format_reqs.extend(currency_reqs)
    print(f"  + Currency format requests: {len(currency_reqs)}")
    
    # Add percentage format
    pct_reqs = build_percentage_format_requests()
    format_reqs.extend(pct_reqs)
    print(f"  + Percentage format requests: {len(pct_reqs)}")
    
    # Execute in batches (API limit)
    batch_size = 100
    for i in range(0, len(format_reqs), batch_size):
        batch = format_reqs[i:i+batch_size]
        result = batch_update(batch)
        print(f"  Batch {i//batch_size + 1}: {'OK' if result else 'FAILED'} ({len(batch)} requests)")
    
    # ---- Step 3: Create new tabs ----
    print("\n--- Step 3: Creating new tabs ---")
    new_tab_reqs = create_new_tabs()
    result = batch_update(new_tab_reqs)
    print(f"  New tabs created: {'OK' if result else 'FAILED'}")
    if not result:
        print("  Tabs may already exist, continuing...")
    
    # ---- Step 4: Populate Cash Flow ----
    print("\n--- Step 4: Populating Cash Flow Statement ---")
    cf_data = populate_cash_flow()
    result = update_values("'Cash Flow Statement'!A1", cf_data)
    print(f"  Cash Flow data: {'OK' if result else 'FAILED'} ({len(cf_data)} rows)")
    
    # Format Cash Flow
    cf_format_reqs = format_cash_flow_tab()
    cf_format_reqs.extend(format_new_tab(100, cf_data, 5))
    result = batch_update(cf_format_reqs)
    print(f"  Cash Flow formatting: {'OK' if result else 'FAILED'}")
    
    # ---- Step 5: Populate General Ledger ----
    print("\n--- Step 5: Populating General Ledger ---")
    gl_data = populate_general_ledger()
    print(f"  GL entries: {len(gl_data)} rows")
    
    # Write in batches (values API has limits)
    gl_batch_size = 1000
    for i in range(0, len(gl_data), gl_batch_size):
        batch = gl_data[i:i+gl_batch_size]
        if i == 0:
            result = update_values("'General Ledger'!A1", batch)
        else:
            result = update_values(f"'General Ledger'!A{i+1}", batch)
        print(f"  GL batch {i//gl_batch_size + 1}: {'OK' if result else 'FAILED'} ({len(batch)} rows)")
    
    # Format GL
    gl_format_reqs = format_general_ledger_tab(len(gl_data))
    gl_format_reqs.extend(format_new_tab(101, gl_data, 7))
    result = batch_update(gl_format_reqs)
    print(f"  GL formatting: {'OK' if result else 'FAILED'}")
    
    # ---- Step 6: Populate 1099 Tracking ----
    print("\n--- Step 6: Populating 1099 Tracking ---")
    
    # First, let's analyze Zelle payments to see what we find
    zelle = analyze_zelle_payments()
    print(f"  Found {len(zelle)} outgoing Zelle payments from business checking")
    for z in zelle[:10]:
        print(f"    {z['date'].strftime('%m/%d/%Y') if z['date'] else '??'}: ${z['amount']:.2f} - {z['description'][:60]}")
    
    tracking_data = populate_1099_tracking()
    result = update_values("'1099 Tracking'!A1", tracking_data)
    print(f"  1099 data: {'OK' if result else 'FAILED'} ({len(tracking_data)} rows)")
    
    # Format 1099
    t1099_format_reqs = format_1099_tab()
    t1099_format_reqs.extend(format_new_tab(102, tracking_data, 7))
    result = batch_update(t1099_format_reqs)
    print(f"  1099 formatting: {'OK' if result else 'FAILED'}")
    
    # ---- Step 7: Verify ----
    print("\n--- Step 7: Verification ---")
    
    # Check revenue consistency
    for year in [2024, 2025, 2026]:
        is_data = get_sheet_data(f"'Income Statement {year}'!A1:N10")
        for row in is_data:
            if row and 'TOTAL REVENUE' in str(row[0]):
                total_col = row[-1] if row else 'N/A'
                print(f"  IS {year} Total Revenue: {total_col}")
    
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)

if __name__ == '__main__':
    main()
