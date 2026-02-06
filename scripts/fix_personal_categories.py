#!/usr/bin/env python3
"""
Fix missing personal expense categories across all remaining sheets.
Reads transaction data from CSVs, calculates amounts, and inserts
missing category rows into each sheet's Dashboard Section C.
"""

import csv
import json
import re
import requests
import time
from datetime import datetime
from collections import defaultdict

# ============================================================
# OAuth
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
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

# ============================================================
# Sheet definitions
# ============================================================
SHEETS = {
    'June 2025': {
        'id': '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg',
        'month': 6, 'year': 2025,
        'missing': ['✈️ Travel', '💰 CC Interest & Fees (Personal)', '🏧 ATM / Cash / FX Fees']
    },
    'August 2025': {
        'id': '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI',
        'month': 8, 'year': 2025,
        'missing': ['💰 CC Interest & Fees (Personal)', '🛍️ Shopping & Misc']
    },
    'September 2025': {
        'id': '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM',
        'month': 9, 'year': 2025,
        'missing': ['🍔 Food & Dining', '💰 CC Interest & Fees (Personal)', '🛍️ Shopping & Misc']
    },
    'October 2025': {
        'id': '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA',
        'month': 10, 'year': 2025,
        'missing': ['🍔 Food & Dining', '💰 CC Interest & Fees (Personal)', '🛍️ Shopping & Misc']
    },
    'November 2025': {
        'id': '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0',
        'month': 11, 'year': 2025,
        'missing': ['🍔 Food & Dining', '💰 CC Interest & Fees (Personal)', '🛍️ Shopping & Misc']
    },
    'December 2025': {
        'id': '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo',
        'month': 12, 'year': 2025,
        'missing': ['🍔 Food & Dining', '💰 CC Interest & Fees (Personal)', '🛍️ Shopping & Misc']
    },
}

# Category emoji prefixes for fuzzy matching
CATEGORY_EMOJIS = {
    '✈️ Travel': '✈️',
    '💰 CC Interest & Fees (Personal)': '💰',
    '🏧 ATM / Cash / FX Fees': '🏧',
    '🍔 Food & Dining': '🍔',
    '🛍️ Shopping & Misc': '🛍️',
}

# ============================================================
# Load and parse CSV data
# ============================================================
def load_personal_0068():
    """Load Personal 0068 transactions."""
    txns = []
    with open('/home/ec2-user/clawd/data/chase-exports/personal-0068-alltime.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row['Posting Date'].strip(), '%m/%d/%Y')
                amount = float(row['Amount'].strip().replace(',', ''))
                txns.append({
                    'date': date,
                    'month': date.month,
                    'year': date.year,
                    'description': row['Description'].strip(),
                    'amount': amount,
                    'type': row['Type'].strip(),
                    'details': row['Details'].strip(),
                    'source': 'Personal 0068'
                })
            except (ValueError, KeyError) as e:
                continue
    return txns

def load_sapphire_4252():
    """Load Sapphire 4252 transactions."""
    txns = []
    with open('/home/ec2-user/clawd/data/chase-exports/sapphire-4252-alltime.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row['Post Date'].strip(), '%m/%d/%Y')
                amount = float(row['Amount'].strip().replace(',', ''))
                txns.append({
                    'date': date,
                    'month': date.month,
                    'year': date.year,
                    'description': row['Description'].strip(),
                    'amount': amount,
                    'type': row['Type'].strip(),
                    'category': row.get('Category', '').strip(),
                    'source': 'Sapphire 4252'
                })
            except (ValueError, KeyError) as e:
                continue
    return txns

print("Loading CSV data...")
personal_txns = load_personal_0068()
sapphire_txns = load_sapphire_4252()
print(f"  Personal 0068: {len(personal_txns)} transactions")
print(f"  Sapphire 4252: {len(sapphire_txns)} transactions")

# ============================================================
# Transaction categorization
# ============================================================
def categorize_for_food(txn):
    """Check if transaction is food/dining."""
    desc = txn['description'].upper()
    food_keywords = [
        'DOORDASH', 'DD *DOORDASH', 'UBEREATS', 'UBER EATS', 'GRUBHUB',
        'MCDONALD', 'WENDY', 'BURGER', 'PIZZA', 'TACO', 'CHIPOTLE',
        'STARBUCKS', 'DUNKIN', 'COFFEE', 'CAFE', 'BAKERY',
        'RESTAURANT', 'GRILL', 'KITCHEN', 'DINER', 'BISTRO',
        'BAR ', 'PUB ', 'TAVERN', 'BREWERY', 'TAPROOM',
        'KROGER', 'WALMART', 'TARGET', 'TRADER JOE', 'WHOLE FOODS',
        'ALDI', 'COSTCO', 'SAFEWAY', 'RALPHS', 'VONS',
        'GROCERIES', 'GROCERY', 'MARKET', 'FOOD', 'DINING',
        'RAISING CANE', 'CHICK-FIL', 'SUBWAY', 'PANERA',
        "AUNTIE ANNE", 'BANZAI', 'SHAKE SHACK', 'VELVET TACO',
        'CANELA CAFE', 'TST*', 'SQ *', 'FISH MARKET',
        'FRESH THYME', 'TOM THUMB', 'CENTRAL MARKET', 'PARKIT MARKET',
        'PIZZERIA', 'GLAZED COFFEE', "NICO'S", 'BAJA BEACH CAFE',
        'ICE CREAM', 'OCEANS', 'CREAMERY', 'SMOOTHIE',
        'IHOP', 'DENNYS', 'APPLEBEE', 'OLIVE GARDEN',
        'POPEYES', 'KFC', 'DOMINO', 'PAPA JOHN',
        'NOODLE', 'SUSHI', 'THAI', 'CHINESE', 'MEXICAN',
        'WAFFLE', 'PANCAKE', 'BRUNCH', 'BREAKFAST',
        'MADCHICKE', 'COLIVING',  # some food from Colombia
    ]
    
    # Check Sapphire categories
    if txn.get('category', '') in ['Food & Drink', 'Groceries']:
        return True
    
    for kw in food_keywords:
        if kw in desc:
            return True
    return False

def categorize_for_travel(txn):
    """Check if transaction is travel."""
    desc = txn['description'].upper()
    travel_keywords = [
        'AIRLINE', 'AIRLINES', 'SOUTHWEST', 'UNITED', 'DELTA', 'AMERICAN AIR',
        'SPIRIT', 'JETBLUE', 'FRONTIER', 'LATAM', 'SWA*',
        'HOTEL', 'HOSTEL', 'AIRBNB', 'MOTEL', 'INN', 'LODGE',
        'TURO', 'HERTZ', 'ENTERPRISE', 'AVIS', 'BUDGET', 'NATIONAL',
        'AIRALO', 'ONWARD TICKET', 'TRAVEL GUARD',
        'HOSTELWORLD', 'BOOKING.COM', 'EXPEDIA',
        'BEACH BUNGALOW', 'MASAYA', 'ITH HOSTEL', 'MISSION BAY',
        'COUCHSURFING', 'COLIVING',
        'UBER   *TRIP', 'LYFT',
        'WISE', 'BOLD CASA',  # travel spending abroad
        'SOUTHWES', 'SWA ', 'FLIGHT',
    ]
    
    if txn.get('category', '') == 'Travel':
        return True
    
    for kw in travel_keywords:
        if kw in desc:
            return True
    return False

def categorize_for_cc_interest(txn):
    """Check if transaction is CC interest/fees on Sapphire 4252."""
    desc = txn['description'].upper()
    if txn['source'] == 'Sapphire 4252':
        if 'INTEREST CHARGE' in desc or 'ANNUAL MEMBERSHIP FEE' in desc or 'LATE FEE' in desc:
            return True
        if txn.get('category', '') == 'Fees & Adjustments' and txn['amount'] < 0:
            # Include fee adjustments that are charges (not credits)
            if 'STATEMENT CREDIT' not in desc:
                return True
    return False

def categorize_for_atm_cash_fx(txn):
    """Check if transaction is ATM/Cash/FX fee."""
    desc = txn['description'].upper()
    if txn['source'] == 'Personal 0068':
        if 'ATM' in desc and ('WITHDRAW' in desc or 'FEE' in desc):
            return True
        if 'FOREIGN EXCHANGE' in desc:
            return True
        if txn.get('type', '') == 'ATM':
            return True
        if txn.get('type', '') == 'FEE_TRANSACTION' and ('ATM' in desc or 'FOREIGN' in desc):
            return True
    return False

def categorize_for_shopping(txn):
    """Check if transaction is shopping/misc."""
    desc = txn['description'].upper()
    shopping_keywords = [
        'AMAZON', 'AMZN', 'TARGET', 'WALMART', 'OLD NAVY', 'GAP',
        'BEST BUY', 'HOME DEPOT', 'LOWES', 'IKEA',
        'CVS', 'WALGREENS', 'RITE AID',
        'APPLE STORE', 'APPLE.COM',
        'EBAY', 'ETSY',
        'MISSION SURF', 'WELKES', 'DOWNER HARDWARE',
        'PAYPAL', 'APPLE CASH', 'VENMO',
        'GOFUNDME', 'DONATION',
    ]
    
    if txn.get('category', '') == 'Shopping':
        return True
    
    for kw in shopping_keywords:
        if kw in desc:
            return True
    return False

def get_monthly_txns(month, year):
    """Get all transactions for a specific month from both accounts."""
    p_txns = [t for t in personal_txns if t['month'] == month and t['year'] == year]
    s_txns = [t for t in sapphire_txns if t['month'] == month and t['year'] == year]
    return p_txns, s_txns

def calculate_category_data(month, year, category_name):
    """Calculate category data from CSVs for a specific month."""
    p_txns, s_txns = get_monthly_txns(month, year)
    all_txns = p_txns + s_txns
    
    # Filter based on category
    if category_name == '🍔 Food & Dining':
        filtered = [t for t in all_txns if categorize_for_food(t) and t['amount'] < 0]
    elif category_name == '✈️ Travel':
        filtered = [t for t in all_txns if categorize_for_travel(t) and t['amount'] < 0]
    elif category_name == '💰 CC Interest & Fees (Personal)':
        filtered = [t for t in all_txns if categorize_for_cc_interest(t)]
    elif category_name == '🏧 ATM / Cash / FX Fees':
        filtered = [t for t in all_txns if categorize_for_atm_cash_fx(t) and t['amount'] < 0]
    elif category_name == '🛍️ Shopping & Misc':
        filtered = [t for t in all_txns if categorize_for_shopping(t) and t['amount'] < 0]
    else:
        filtered = []
    
    if not filtered:
        return None
    
    # Group by vendor/description for detail rows
    vendor_groups = defaultdict(lambda: {'count': 0, 'total': 0.0, 'descriptions': []})
    
    for t in filtered:
        # Clean up description for grouping
        desc = t['description']
        vendor = clean_vendor_name(desc, category_name)
        vendor_groups[vendor]['count'] += 1
        vendor_groups[vendor]['total'] += t['amount']
        vendor_groups[vendor]['descriptions'].append(desc)
    
    total = sum(t['amount'] for t in filtered)
    count = len(filtered)
    
    return {
        'vendors': dict(vendor_groups),
        'total': total,
        'count': count,
    }

def clean_vendor_name(desc, category):
    """Clean transaction description into a readable vendor name."""
    desc_upper = desc.upper().strip()
    
    # ATM / Cash / FX
    if 'NON-CHASE ATM FEE' in desc_upper:
        return 'ATM Fees'
    if 'NON-CHASE ATM WITHDRAW' in desc_upper:
        return 'ATM Withdrawals'
    if 'FOREIGN EXCHANGE RATE' in desc_upper:
        return 'Foreign Exchange Fees'
    if desc_upper.startswith('ATM') or 'ATM' in desc_upper:
        return 'ATM Withdrawals'
    
    # CC Interest & Fees
    if 'PURCHASE INTEREST CHARGE' in desc_upper:
        return 'Sapphire 4252 Interest'
    if 'ANNUAL MEMBERSHIP FEE' in desc_upper:
        return 'Sapphire Annual Fee'
    if 'LATE FEE' in desc_upper:
        return 'Late Fee'
    if 'STATEMENT CREDIT' in desc_upper:
        return 'Statement Credit'
    
    # Travel
    if 'SOUTHWEST' in desc_upper or 'SWA' in desc_upper or 'SOUTHWES' in desc_upper:
        return 'Southwest Airlines'
    if 'UNITED' in desc_upper and 'AIR' not in desc_upper:
        return 'United Airlines'
    if 'LATAM' in desc_upper:
        return 'LATAM Airlines'
    if 'AIRBNB' in desc_upper:
        return 'Airbnb'
    if 'HOSTEL' in desc_upper or 'HOSTELWORLD' in desc_upper:
        return 'Hostels'
    if 'BEACH BUNGALOW' in desc_upper:
        return 'Beach Bungalow Hostel'
    if 'TURO' in desc_upper:
        return 'Turo Car Rental'
    if 'AIRALO' in desc_upper:
        return 'Airalo (eSIM)'
    if 'UBER' in desc_upper and 'TRIP' in desc_upper:
        return 'Uber (rides)'
    if 'LYFT' in desc_upper:
        return 'Lyft'
    if 'TRAVEL GUARD' in desc_upper:
        return 'Travel Insurance'
    if 'ONWARD TICKET' in desc_upper:
        return 'Onward Ticket'
    if 'COLIVING' in desc_upper:
        return 'Coliving'
    if 'BOLD CASA' in desc_upper:
        return 'Accommodation (Colombia)'
    if 'WISE' in desc_upper:
        return 'Wise Transfers'
    if 'MASAYA' in desc_upper:
        return 'Masaya Hostel'
    if 'ITH HOSTEL' in desc_upper:
        return 'ITH Hostel'
    if 'MISSION BAY' in desc_upper:
        return 'Mission Bay Hotel'
    
    # Food
    if 'DOORDASH' in desc_upper or 'DD *DOORDASH' in desc_upper:
        return 'DoorDash'
    if 'STARBUCKS' in desc_upper:
        return 'Starbucks'
    if 'KROGER' in desc_upper:
        return 'Kroger'
    if 'TRADER JOE' in desc_upper:
        return 'Trader Joe\'s'
    if 'RALPHS' in desc_upper:
        return 'Ralphs'
    if 'VONS' in desc_upper:
        return 'Vons'
    if 'WALMART' in desc_upper:
        return 'Walmart'
    if 'FRESH THYME' in desc_upper:
        return 'Fresh Thyme'
    if 'CENTRAL MARKET' in desc_upper:
        return 'Central Market'
    if 'TOM THUMB' in desc_upper:
        return 'Tom Thumb'
    if 'TARGET' in desc_upper:
        return 'Target'
    if 'RAISING CANE' in desc_upper:
        return "Raising Cane's"
    if 'SHAKE SHACK' in desc_upper:
        return 'Shake Shack'
    if 'VELVET TACO' in desc_upper:
        return 'Velvet Taco'
    if 'CANELA CAFE' in desc_upper:
        return 'Canela Cafe'
    if 'BAJA BEACH CAFE' in desc_upper:
        return 'Baja Beach Cafe'
    if 'GLAZED COFFEE' in desc_upper:
        return 'Glazed Coffee'
    if 'FISH MARKET' in desc_upper:
        return "Nico's Fish Market"
    if 'PIZZERIA' in desc_upper:
        return 'Pizzeria'
    if 'SPARROW HILL' in desc_upper:
        return 'Sparrow Hill Farm'
    if 'IHOP' in desc_upper:
        return 'IHOP'
    if 'PEROT' in desc_upper:
        return 'Perot Museum'
    
    # Shopping
    if 'AMAZON' in desc_upper or 'AMZN' in desc_upper:
        return 'Amazon'
    if 'TARGET' in desc_upper:
        return 'Target'
    if 'CVS' in desc_upper:
        return 'CVS'
    if 'APPLE CASH' in desc_upper:
        return 'Apple Cash'
    if 'PAYPAL' in desc_upper:
        return 'PayPal'
    if 'GOFUNDME' in desc_upper:
        return 'GoFundMe'
    if 'VENMO' in desc_upper:
        return 'Venmo'
    if 'OLD NAVY' in desc_upper:
        return 'Old Navy'
    if 'MISSION SURF' in desc_upper:
        return 'Mission Surf'
    if 'WELKES' in desc_upper:
        return 'Welkes House of Roses'
    
    # Generic cleanup
    # Take first meaningful part of description
    parts = desc.split()
    if len(parts) > 3:
        return ' '.join(parts[:3])
    return desc[:40]

def fmt_money(amount):
    """Format as ($X.XX) for negative or $X.XX for positive."""
    if amount < 0:
        return f'(${abs(amount):,.2f})'
    return f'${amount:,.2f}'

# ============================================================
# Google Sheets API helpers
# ============================================================
def read_dashboard(sheet_id):
    """Read full dashboard data."""
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/'📊 Dashboard'!A1:H250"
    resp = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    data = resp.json()
    return data.get('values', [])

def get_dashboard_sheet_id(spreadsheet_id):
    """Get the actual sheetId for the Dashboard tab."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?fields=sheets.properties'
    resp = requests.get(url, headers={'Authorization': f'Bearer {TOKEN}'})
    data = resp.json()
    for sheet in data.get('sheets', []):
        if '📊' in sheet['properties']['title'] or 'Dashboard' in sheet['properties']['title']:
            return sheet['properties']['sheetId']
    return 0

def find_insertion_point(rows):
    """Find the row index where missing categories should be inserted.
    Returns (insert_row_index, has_total_row)
    """
    section_c_start = None
    section_d_start = None
    total_personal_row = None
    last_content_row = None
    
    for i, row in enumerate(rows):
        text = ' '.join(str(c) for c in row).upper() if row else ''
        if 'SECTION C' in text:
            section_c_start = i
        if section_c_start is not None and ('SECTION D' in text or 'KEY METRICS' in text):
            section_d_start = i
            break
        if section_c_start is not None and 'TOTAL PERSONAL' in text:
            total_personal_row = i
        if section_c_start is not None and row and any(str(c).strip() for c in row):
            last_content_row = i
    
    if total_personal_row is not None:
        return total_personal_row, True
    elif section_d_start is not None:
        # Insert before the blank rows before Section D
        insert_at = section_d_start
        # Go back past blank rows
        while insert_at > 0 and (not rows[insert_at - 1] or not any(str(c).strip() for c in rows[insert_at - 1])):
            insert_at -= 1
        return insert_at, False
    elif last_content_row is not None:
        return last_content_row + 1, False
    else:
        return len(rows), False

def check_category_exists(rows, category_name):
    """Check if a category already exists in the dashboard (fuzzy match)."""
    emoji = CATEGORY_EMOJIS.get(category_name, '')
    
    # Define what to search for
    search_terms = []
    if category_name == '🍔 Food & Dining':
        search_terms = ['🍔', 'FOOD', 'DINING']
    elif category_name == '💰 CC Interest & Fees (Personal)':
        search_terms = ['💰 CC', 'CC INTEREST', 'CC INT']
    elif category_name == '🏧 ATM / Cash / FX Fees':
        search_terms = ['🏧 ATM']  # Must start with this
    elif category_name == '✈️ Travel':
        search_terms = ['✈️ TRAVEL', '✈️']
    elif category_name == '🛍️ Shopping & Misc':
        search_terms = ['🛍️ SHOP', '🛍️']
    
    for i, row in enumerate(rows):
        if not row:
            continue
        cell_text = str(row[0]).upper().strip()
        for term in search_terms:
            if term.upper() in cell_text:
                # Check if it's a category header (not a subtotal)
                if 'SUBTOTAL' not in cell_text and 'TOTAL' not in cell_text:
                    return True
    return False

def build_category_rows(category_name, data):
    """Build the rows for a category section."""
    if data is None or data['count'] == 0:
        # Still add the category with $0.00
        rows = [
            [category_name],
            ['', '(No transactions this month)', '0', '$0.00'],
            ['', '', f'{category_name.split(" ", 1)[1] if " " in category_name else category_name} Subtotal', '$0.00'],
        ]
        return rows
    
    rows = [[category_name]]
    
    # Sort vendors by total amount (most negative first)
    sorted_vendors = sorted(data['vendors'].items(), key=lambda x: x[1]['total'])
    
    for vendor, info in sorted_vendors:
        rows.append(['', vendor, str(info['count']), fmt_money(info['total'])])
    
    # Subtotal row
    cat_short = category_name.split('(')[0].strip()  # Remove "(Personal)" etc
    # Extract a short name for the subtotal
    subtotal_names = {
        '🍔 Food & Dining': 'Food/Dining Subtotal',
        '✈️ Travel': 'Travel Subtotal',
        '💰 CC Interest & Fees (Personal)': 'CC Interest/Fees Subtotal',
        '🏧 ATM / Cash / FX Fees': 'ATM/Cash/FX Subtotal',
        '🛍️ Shopping & Misc': 'Shopping/Misc Subtotal',
    }
    subtotal_name = subtotal_names.get(category_name, f'{category_name} Subtotal')
    rows.append(['', '', subtotal_name, fmt_money(data['total'])])
    
    return rows

def insert_rows_via_api(spreadsheet_id, dashboard_gid, insert_at_row, new_rows):
    """Insert new rows into the dashboard using batchUpdate."""
    # First, insert blank rows
    num_rows = len(new_rows)
    
    insert_req = {
        'requests': [
            {
                'insertDimension': {
                    'range': {
                        'sheetId': dashboard_gid,
                        'dimension': 'ROWS',
                        'startIndex': insert_at_row,
                        'endIndex': insert_at_row + num_rows,
                    },
                    'inheritFromBefore': True,
                }
            }
        ]
    }
    
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate'
    resp = requests.post(url, headers=HEADERS, json=insert_req)
    if resp.status_code != 200:
        print(f"  ERROR inserting rows: {resp.status_code} {resp.text[:200]}")
        return False
    
    # Now write the data
    # Convert row index to A1 notation
    start_row = insert_at_row + 1  # 1-indexed
    end_row = start_row + num_rows - 1
    range_str = f"'📊 Dashboard'!A{start_row}:D{end_row}"
    
    write_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_str}?valueInputOption=RAW"
    write_data = {'values': new_rows}
    resp = requests.put(write_url, headers=HEADERS, json=write_data)
    if resp.status_code != 200:
        print(f"  ERROR writing data: {resp.status_code} {resp.text[:200]}")
        return False
    
    return True

def format_subtotal_rows(spreadsheet_id, dashboard_gid, insert_at_row, new_rows):
    """Apply formatting to subtotal rows and category headers."""
    requests_list = []
    
    for i, row in enumerate(new_rows):
        actual_row = insert_at_row + i
        
        # Category header row (first cell has emoji)
        if row and len(row) >= 1 and row[0] and any(e in str(row[0]) for e in ['📈', '🏠', '🍔', '📺', '✈️', '🛍️', '💳', '💰', '🏧']):
            requests_list.append({
                'repeatCell': {
                    'range': {
                        'sheetId': dashboard_gid,
                        'startRowIndex': actual_row,
                        'endRowIndex': actual_row + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 4,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {'bold': True},
                        }
                    },
                    'fields': 'userEnteredFormat.textFormat.bold',
                }
            })
        
        # Subtotal row (has "Subtotal" in it)
        row_text = ' '.join(str(c) for c in row) if row else ''
        if 'Subtotal' in row_text or 'SUBTOTAL' in row_text:
            requests_list.append({
                'repeatCell': {
                    'range': {
                        'sheetId': dashboard_gid,
                        'startRowIndex': actual_row,
                        'endRowIndex': actual_row + 1,
                        'startColumnIndex': 0,
                        'endColumnIndex': 4,
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'textFormat': {'bold': True},
                            'backgroundColor': {
                                'red': 0.953, 'green': 0.953, 'blue': 0.953, 'alpha': 1.0
                            },
                        }
                    },
                    'fields': 'userEnteredFormat.textFormat.bold,userEnteredFormat.backgroundColor',
                }
            })
    
    if requests_list:
        url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate'
        resp = requests.post(url, headers=HEADERS, json={'requests': requests_list})
        if resp.status_code != 200:
            print(f"  WARNING: formatting failed: {resp.status_code} {resp.text[:200]}")
            return False
    return True

# ============================================================
# Main processing
# ============================================================
report_lines = []
report_lines.append("# Personal Categories Fix Report")
report_lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n")
report_lines.append("---\n")

for sheet_name, config in SHEETS.items():
    print(f"\n{'='*60}")
    print(f"Processing: {sheet_name}")
    print(f"{'='*60}")
    
    report_lines.append(f"\n## {sheet_name}")
    report_lines.append(f"**Spreadsheet ID:** `{config['id']}`\n")
    
    # Read current dashboard
    rows = read_dashboard(config['id'])
    dashboard_gid = get_dashboard_sheet_id(config['id'])
    print(f"  Dashboard has {len(rows)} rows, GID={dashboard_gid}")
    
    # Find insertion point
    insert_at, has_total = find_insertion_point(rows)
    print(f"  Insert point: row {insert_at} (has TOTAL row: {has_total})")
    
    categories_added = []
    categories_skipped = []
    total_rows_inserted = 0
    
    # Process each missing category
    all_new_rows = []
    for cat in config['missing']:
        print(f"\n  Checking: {cat}")
        
        # Check if it already exists
        if check_category_exists(rows, cat):
            print(f"    → Already exists, skipping")
            categories_skipped.append(cat)
            report_lines.append(f"- **{cat}**: ⏭️ Already exists (skipped)")
            continue
        
        # Calculate from CSV data
        data = calculate_category_data(config['month'], config['year'], cat)
        
        if data:
            print(f"    → Found {data['count']} transactions, total: {fmt_money(data['total'])}")
            for vendor, info in sorted(data['vendors'].items(), key=lambda x: x[1]['total']):
                print(f"      {vendor}: {info['count']}x = {fmt_money(info['total'])}")
        else:
            print(f"    → No transactions found for this category")
        
        # Build the rows
        cat_rows = build_category_rows(cat, data)
        all_new_rows.extend(cat_rows)
        
        categories_added.append({
            'name': cat,
            'data': data,
            'rows': len(cat_rows),
        })
        
        if data:
            report_lines.append(f"- **{cat}**: ✅ Added ({data['count']} txns, {fmt_money(data['total'])})")
            for vendor, info in sorted(data['vendors'].items(), key=lambda x: x[1]['total']):
                report_lines.append(f"  - {vendor}: {info['count']}x = {fmt_money(info['total'])}")
        else:
            report_lines.append(f"- **{cat}**: ✅ Added (no transactions, $0.00)")
    
    # Insert all new rows at once
    if all_new_rows:
        print(f"\n  Inserting {len(all_new_rows)} rows at position {insert_at}...")
        success = insert_rows_via_api(config['id'], dashboard_gid, insert_at, all_new_rows)
        
        if success:
            print(f"  ✅ Rows inserted successfully")
            # Apply formatting
            format_subtotal_rows(config['id'], dashboard_gid, insert_at, all_new_rows)
            print(f"  ✅ Formatting applied")
            report_lines.append(f"\n**Result:** {len(all_new_rows)} rows inserted at row {insert_at + 1}")
        else:
            print(f"  ❌ Failed to insert rows")
            report_lines.append(f"\n**Result:** ❌ FAILED to insert rows")
    else:
        print(f"\n  No rows to insert (all categories already exist)")
        report_lines.append(f"\n**Result:** No changes needed")
    
    # Rate limiting
    time.sleep(1)

# Write report
report_lines.append("\n---\n")
report_lines.append("## Summary\n")
report_lines.append("| Sheet | Categories Added | Categories Skipped |")
report_lines.append("|-------|-----------------|-------------------|")
for sheet_name, config in SHEETS.items():
    report_lines.append(f"| {sheet_name} | See above | See above |")

report_content = '\n'.join(report_lines)
with open('/home/ec2-user/clawd/data/personal-categories-fix-report.md', 'w') as f:
    f.write(report_content)

print("\n\n" + "="*60)
print("DONE! Report saved to /home/ec2-user/clawd/data/personal-categories-fix-report.md")
print("="*60)
