#!/usr/bin/env python3
"""
Build personal finance tabs in the All Time Financial Overview sheet.
Creates: 👤 Personal Overview, 👤 Personal 0068, 💎 Personal 4252
Updates: 📅 2024, 📅 2025, 📅 2026 with personal spending sections
"""

import csv
import json
import re
import requests
from collections import defaultdict
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================
SHEET_ID = '1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ'
CSV_0068 = '/home/ec2-user/clawd/data/chase-exports/personal-0068-alltime.csv'
CSV_4252 = '/home/ec2-user/clawd/data/chase-exports/sapphire-4252-alltime.csv'
REPORT_PATH = '/home/ec2-user/clawd/data/personal-data-report.md'

# Colors
NAVY = {"red": 0.106, "green": 0.165, "blue": 0.290}  # #1B2A4A
WHITE = {"red": 1, "green": 1, "blue": 1}
LIGHT_GRAY = {"red": 0.953, "green": 0.953, "blue": 0.953}  # #F3F3F3
PERSONAL_BLUE = {"red": 0.259, "green": 0.522, "blue": 0.957}  # #4285F4
TOTALS_BG = {"red": 0.910, "green": 0.929, "blue": 0.949}  # #E8EDF5
LIGHT_BLUE_TAB = {"red": 0.259, "green": 0.522, "blue": 0.957}  # #4285F4

# ============================================================
# CATEGORIZATION ENGINE
# ============================================================

def categorize_0068(description, amount, txn_type):
    """Categorize personal checking (0068) transactions."""
    desc_upper = description.upper()
    
    # === INCOME (credits) ===
    if amount > 0:
        if '4991' in desc_upper or ('TRANSFER FROM CHK' in desc_upper and '4991' in desc_upper):
            return '💵 Owner\'s Draw'
        if 'ONLINE TRANSFER FROM CHK' in desc_upper and '4991' in desc_upper:
            return '💵 Owner\'s Draw'
        if 'ZELLE FROM' in desc_upper or 'Zelle from' in description:
            return '💵 Zelle Income'
        if 'TRANSFER FROM' in desc_upper or 'ODP TRANSFER' in desc_upper:
            return '🔄 Transfer'
        if 'DIRECT DEP' in desc_upper or 'PAYROLL' in desc_upper:
            return '💵 Income'
        if 'REFUND' in desc_upper or 'CREDIT' in desc_upper:
            return '💵 Refund'
        return '💵 Other Income'
    
    # === SPENDING (debits) ===
    # Investments
    if 'ROBINHOOD' in desc_upper:
        return '📈 Investment'
    if 'ACORNS' in desc_upper:
        return '📈 Investment'
    if 'COINBASE' in desc_upper or 'CRYPTO' in desc_upper:
        return '📈 Investment'
    
    # Transfers between own accounts
    if 'TRANSFER TO  SAV' in desc_upper or 'TRANSFER TO SAV' in desc_upper:
        return '🔄 Transfer'
    if 'ONLINE TRANSFER TO' in desc_upper and ('7036' in desc_upper or 'SAV' in desc_upper):
        return '🔄 Transfer'
    if 'ONLINE TRANSFER TO' in desc_upper and '4991' in desc_upper:
        return '🔄 Transfer'
    if txn_type == 'ACCT_XFER' and amount < 0:
        return '🔄 Transfer'
    
    # ATM / Cash
    if 'ATM' in desc_upper:
        return '🏧 ATM / Cash / FX'
    if 'FOREIGN EXCHANGE' in desc_upper or 'FX' in desc_upper:
        return '🏧 ATM / Cash / FX'
    
    # Student Loans / Debt
    if 'DEPT EDUCATION' in desc_upper or 'STUDENT LN' in desc_upper or 'STUDENT LOAN' in desc_upper:
        return '💳 Debt Payment'
    if 'DISCOVER' in desc_upper and ('PAYMENT' in desc_upper or 'EPAY' in desc_upper):
        return '💳 CC Payment'
    if 'CHASE CREDIT CRD' in desc_upper or 'PAYMENT TO CHASE' in desc_upper:
        return '💳 CC Payment'
    if 'CREDIT STRONG' in desc_upper:
        return '💳 Debt Payment'
    if 'AFFIRM' in desc_upper:
        return '💳 Debt Payment'
    
    # Food & Dining
    food_keywords = ['DOORDASH', 'GRUBHUB', 'UBER EATS', 'UBEREATS', 'MCDONALD', 'CHIPOTLE', 
                     'STARBUCKS', 'DUNKIN', 'SUBWAY', 'NOODLES', 'WHOLEFDS', 'WHOLE FOODS',
                     'TRADER JOE', 'ALDI', 'KROGER', 'WALMART', 'PICK N SAVE', 'PIGGLY', 
                     'TACO BELL', 'WENDY', 'BURGER KING', 'FIVE GUYS', 'CHICK-FIL',
                     'PANERA', 'JIMMY JOHN', 'DOMINO', 'PIZZA', 'SUSHI', 'PANDA EXPRESS',
                     'POPEYES', 'KFC', 'ARBY', 'DENNY', 'IHOP', 'WAFFLE', 'CULVER',
                     'QDOBA', 'PORTILLO', 'RESTAURANT', 'CAFE', 'COFFEE', 'BAKERY',
                     'GLAZED', 'COLECTIVO', 'KNUCKLEHEADS', 'STOP N GO', 'BUEN PROVECHO',
                     'FOOD', 'DELI', 'MARKET', 'GRILL', 'TAVERN', 'BAR & ', 'PUB',
                     'FRESH THYME', 'TARGET STORE', 'SNACK', 'GUSTOS', 'VIENA',
                     'FAMOUS FAMIGLIA', 'EL SOL', 'GORDITAS', 'TACOS', 'TAQUERIA',
                     'SAKURA', 'RAMEN', 'THAI', 'WOK', 'CHOPSTIX', 'ASIAN', 'CHINA']
    if any(kw in desc_upper for kw in food_keywords):
        # Distinguish groceries from dining
        grocery_kw = ['WHOLEFDS', 'WHOLE FOODS', 'TRADER JOE', 'ALDI', 'KROGER', 'PICK N SAVE', 
                      'PIGGLY', 'FRESH THYME', 'TARGET STORE', 'WALMART']
        if any(kw in desc_upper for kw in grocery_kw):
            return '🍔 Food & Dining'
        return '🍔 Food & Dining'
    
    # Transportation
    transport_kw = ['UBER', 'LYFT', 'GAS', 'SHELL', 'BP ', 'EXXON', 'CHEVRON', 'SPEEDWAY',
                    'KWIK TRIP', 'CITGO', 'PARKING', 'METRO', 'BUS', 'TRANSIT']
    if any(kw in desc_upper for kw in transport_kw):
        if 'UBER EATS' not in desc_upper and 'UBEREATS' not in desc_upper:
            return '🚗 Transportation'
    
    # Subscriptions / Entertainment
    sub_kw = ['SPOTIFY', 'NETFLIX', 'HULU', 'DISNEY+', 'DISNEY PLUS', 'YOUTUBE', 'APPLE.COM',
              'PATREON', 'AMAZON PRIME', 'HBO', 'PARAMOUNT', 'PEACOCK', 'CRUNCHYROLL',
              'AUDIBLE', 'KINDLE', 'APPLE MUSIC', 'TIDAL', 'DEEZER', 'PLEX']
    if any(kw in desc_upper for kw in sub_kw):
        return '📺 Subscription'
    
    # Travel  
    travel_kw = ['AIRBNB', 'HOTEL', 'AIRLINE', 'LATAM', 'UNITED', 'DELTA', 'AMERICAN AIR',
                 'SOUTHWEST', 'SPIRIT', 'FRONTIER', 'JETBLUE', 'BOOKING.COM', 'EXPEDIA',
                 'HOSTEL', 'TURO', 'FLIGHT', 'AIRALO', 'HOSTELWORLD', 'BUNGALOW']
    if any(kw in desc_upper for kw in travel_kw):
        return '✈️ Travel'
    
    # Shopping
    shop_kw = ['AMAZON', 'AMZN', 'BEST BUY', 'WALMART', 'TARGET', 'EBAY', 'ETSY',
               'APPLE STORE', 'IKEA', 'HOME DEPOT', 'LOWES', 'MARSHALLS', 'TJ MAXX',
               'ROSS', 'COSTCO', 'WALGREENS', 'CVS']
    if any(kw in desc_upper for kw in shop_kw):
        return '🛍️ Shopping & Misc'
    
    # Housing
    housing_kw = ['RENT', 'LEASE', 'LANDLORD', 'PROPERTY', 'ELECTRIC', 'GAS BILL',
                  'WATER BILL', 'WE ENERGIES', 'INTERNET', 'SPECTRUM', 'COMCAST',
                  'AT&T', 'VERIZON', 'T-MOBILE', 'TMOBILE']
    if any(kw in desc_upper for kw in housing_kw):
        return '🏠 Living / Local'
    
    # Health
    health_kw = ['PHARMACY', 'MEDICAL', 'DOCTOR', 'HOSPITAL', 'CLINIC', 'DENTAL',
                 'CVS/PHARMACY', 'WALGREENS', 'GYM', 'FITNESS', 'PLANET FITNESS']
    if any(kw in desc_upper for kw in health_kw):
        return '💊 Health'
    
    # Phone / Tech
    tech_kw = ['APPLE.COM/BILL', 'T-MOBILE', 'VERIZON', 'AT&T WIRELESS']
    if any(kw in desc_upper for kw in tech_kw):
        return '📱 Phone / Tech'
    
    # Venmo (social/misc spending)
    if 'VENMO' in desc_upper:
        return '🛍️ Shopping & Misc'
    
    # Zelle outgoing
    if 'ZELLE TO' in desc_upper or 'Zelle to' in description:
        return '🛍️ Shopping & Misc'
    
    # Fees
    if 'FEE' in desc_upper and ('MONTHLY' in desc_upper or 'SERVICE' in desc_upper or 'MAINT' in desc_upper):
        return '💰 Interest & Fees'
    if txn_type == 'FEE_TRANSACTION':
        return '💰 Interest & Fees'
    
    return '🛍️ Shopping & Misc'


def categorize_4252(description, amount, category_hint):
    """Categorize Sapphire CC (4252) transactions."""
    desc_upper = description.upper()
    
    # Payments
    if 'PAYMENT' in desc_upper and amount > 0:
        return '💳 CC Payment'
    if 'PAYMENT THANK YOU' in desc_upper:
        return '💳 CC Payment'
    if 'AUTOMATIC PAYMENT' in desc_upper:
        return '💳 CC Payment'
    
    # Interest & Fees
    if 'INTEREST CHARGE' in desc_upper:
        return '💰 Interest & Fees'
    if 'MEMBERSHIP FEE' in desc_upper or 'ANNUAL FEE' in desc_upper:
        return '💰 Interest & Fees'
    if 'STATEMENT CREDIT' in desc_upper:
        return '💰 Interest & Fees'
    
    # Business expenses on personal card (Facebook/Google Ads)
    if 'FACEBK' in desc_upper or 'META' in desc_upper:
        return '📣 Business Ad Spend'
    if 'GOOGLE *ADS' in desc_upper:
        return '📣 Business Ad Spend'
    if 'APF*SAINT AUGUSTINE' in desc_upper:
        return '📣 Business Ad Spend'
    
    # Travel
    travel_kw = ['AIRBNB', 'HOTEL', 'AIRLINE', 'LATAM', 'TURO', 'HOSTEL', 'BUNGALOW',
                 'UBER   TRIP', 'AIRALO']
    if any(kw in desc_upper for kw in travel_kw):
        return '✈️ Travel'
    if category_hint and 'Travel' in category_hint:
        return '✈️ Travel'
    
    # Food
    food_kw = ['GLAZED', 'CAFE', 'COFFEE', 'RESTAURANT', 'FOOD', 'SNACK', 'FAMIGLIA',
               'GUSTOS', 'VIENA']
    if any(kw in desc_upper for kw in food_kw):
        return '🍔 Food & Dining'
    if category_hint and 'Food' in category_hint:
        return '🍔 Food & Dining'
    
    # Shopping
    if category_hint and 'Shopping' in category_hint:
        return '🛍️ Shopping & Misc'
    if 'USPS' in desc_upper:
        return '🛍️ Shopping & Misc'
    
    return '🛍️ Shopping & Misc'


# ============================================================
# PARSE CSV FILES
# ============================================================

def parse_0068(filepath):
    """Parse Chase personal checking CSV."""
    transactions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 5:
                continue
            detail = row[0].strip()
            date_str = row[1].strip()
            desc = row[2].strip().strip('"')
            try:
                amount = float(row[3].strip())
            except ValueError:
                continue
            txn_type = row[4].strip()
            balance_str = row[5].strip() if len(row) > 5 else ''
            try:
                balance = float(balance_str) if balance_str else None
            except ValueError:
                balance = None
            
            try:
                date = datetime.strptime(date_str, '%m/%d/%Y')
            except ValueError:
                continue
            
            # Clean up description - take first meaningful part
            vendor = clean_vendor_0068(desc)
            category = categorize_0068(desc, amount, txn_type)
            
            transactions.append({
                'date': date,
                'date_str': date_str,
                'vendor': vendor,
                'description': desc,
                'amount': amount,
                'balance': balance,
                'type': txn_type,
                'category': category,
                'year': date.year,
                'month': date.month,
                'month_key': f"{date.year}-{date.month:02d}"
            })
    
    return transactions


def parse_4252(filepath):
    """Parse Chase Sapphire CC CSV."""
    transactions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 6:
                continue
            txn_date = row[0].strip()
            post_date = row[1].strip()
            desc = row[2].strip()
            cat_hint = row[3].strip()
            txn_type = row[4].strip()
            try:
                amount = float(row[5].strip())
            except ValueError:
                continue
            
            try:
                date = datetime.strptime(post_date, '%m/%d/%Y')
            except ValueError:
                continue
            
            vendor = clean_vendor_4252(desc)
            category = categorize_4252(desc, amount, cat_hint)
            
            transactions.append({
                'date': date,
                'date_str': post_date,
                'vendor': vendor,
                'description': desc,
                'amount': amount,
                'balance': None,
                'type': txn_type,
                'category': category,
                'chase_category': cat_hint,
                'year': date.year,
                'month': date.month,
                'month_key': f"{date.year}-{date.month:02d}"
            })
    
    return transactions


def clean_vendor_0068(desc):
    """Extract clean vendor name from 0068 description."""
    desc = desc.strip('"')
    # Common patterns
    if 'ONLINE TRANSFER FROM CHK' in desc and '4991' in desc:
        return 'Transfer from Business 4991'
    if 'ONLINE TRANSFER TO  SAV' in desc or 'ONLINE TRANSFER TO SAV' in desc:
        return 'Transfer to Savings 7036'
    if 'Online Transfer to  SAV' in desc:
        return 'Transfer to Savings 7036'
    if 'Online Transfer from CHK' in desc and '4991' in desc:
        return 'Transfer from Business 4991'
    if 'Online Transfer from  CHK' in desc and '4991' in desc:
        return 'Transfer from Business 4991'
    if 'ODP TRANSFER FROM SAVINGS' in desc:
        return 'ODP Transfer from Savings'
    if 'ROBINHOOD' in desc.upper():
        return 'Robinhood'
    if 'ACORNS' in desc.upper() and 'ROUND' in desc.upper():
        return 'Acorns Round-Ups'
    if 'ACORNS' in desc.upper():
        return 'Acorns Invest'
    if 'NON-CHASE ATM WITHDRAW' in desc.upper():
        return 'ATM Withdrawal'
    if 'NON-CHASE ATM FEE' in desc.upper():
        return 'ATM Fee'
    if 'FOREIGN EXCHANGE' in desc.upper():
        return 'FX Rate Adjustment Fee'
    if 'DEPT EDUCATION' in desc.upper():
        return 'Student Loan Payment'
    if 'VENMO' in desc.upper():
        # Try to extract Venmo recipient
        return 'Venmo Payment'
    if 'ZELLE TO' in desc or 'Zelle to' in desc:
        match = re.search(r'(?:ZELLE TO|Zelle to)\s+(.+?)(?:\s+\d|$)', desc, re.IGNORECASE)
        if match:
            return f'Zelle to {match.group(1).strip()[:30]}'
        return 'Zelle Payment'
    if 'ZELLE FROM' in desc or 'Zelle from' in desc:
        match = re.search(r'(?:ZELLE FROM|Zelle from)\s+(.+?)(?:\s+\d|$)', desc, re.IGNORECASE)
        if match:
            return f'Zelle from {match.group(1).strip()[:30]}'
        return 'Zelle Received'
    
    # POS DEBIT - clean up
    if desc.startswith('POS DEBIT'):
        cleaned = desc.replace('POS DEBIT', '').strip()
        # Take first meaningful chunk
        parts = cleaned.split()
        if parts:
            return ' '.join(parts[:4]).strip()
    
    # DEBIT CARD style
    # Take first ~4 words for vendor
    words = desc.split()
    if len(words) > 6:
        return ' '.join(words[:4]).strip()
    return desc[:50].strip()


def clean_vendor_4252(desc):
    """Extract clean vendor name from 4252 description."""
    desc = desc.strip()
    if 'FACEBK' in desc:
        return 'Facebook Ads'
    if 'GOOGLE *ADS' in desc:
        return 'Google Ads'
    if 'PAYMENT THANK YOU' in desc:
        return 'CC Payment'
    if 'AUTOMATIC PAYMENT' in desc:
        return 'CC Payment (Auto)'
    if 'PURCHASE INTEREST' in desc:
        return 'Interest Charge'
    if 'ANNUAL MEMBERSHIP' in desc:
        return 'Annual Membership Fee'
    if 'STATEMENT CREDIT' in desc:
        return 'Statement Credit'
    return desc[:40].strip()


# ============================================================
# GOOGLE SHEETS API HELPERS
# ============================================================

def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']


def batch_update(token, requests_list):
    """Execute a batchUpdate on the spreadsheet."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate'
    body = {'requests': requests_list}
    resp = requests.post(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }, json=body)
    if resp.status_code != 200:
        print(f"batchUpdate error: {resp.status_code}")
        print(resp.text[:1000])
    return resp.json()


def update_values(token, range_str, values, input_option='USER_ENTERED'):
    """Write values to a range."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{requests.utils.quote(range_str)}?valueInputOption={input_option}'
    body = {'values': values}
    resp = requests.put(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }, json=body)
    if resp.status_code != 200:
        print(f"updateValues error for {range_str}: {resp.status_code}")
        print(resp.text[:500])
    return resp.json()


def fmt_currency(val):
    """Format a number as currency string."""
    if val is None:
        return ''
    if val < 0:
        return f'-${abs(val):,.2f}'
    return f'${val:,.2f}'


def fmt_currency_formula(val):
    """Return raw number for Sheets to format."""
    return round(val, 2)


# ============================================================
# BUILD SHEET CONTENT
# ============================================================

def build_transaction_log(transactions, account_name):
    """Build rows for a transaction log tab, grouped by month."""
    rows = []
    
    # Sort by date descending
    sorted_txns = sorted(transactions, key=lambda x: x['date'], reverse=True)
    
    current_month = None
    month_subtotal = 0
    month_count = 0
    
    for txn in sorted_txns:
        month_key = txn['month_key']
        month_name = txn['date'].strftime('%B %Y')
        
        if month_key != current_month:
            # Close previous month
            if current_month is not None:
                rows.append(['', '', f'SUBTOTAL: {prev_month_name}', month_subtotal, '', f'{month_count} transactions'])
                rows.append([])  # blank row
            
            current_month = month_key
            prev_month_name = month_name
            month_subtotal = 0
            month_count = 0
            
            # Month header
            rows.append([f'📅 {month_name}', '', '', '', '', ''])
        
        month_subtotal += txn['amount']
        month_count += 1
        
        rows.append([
            txn['date_str'],
            txn['vendor'],
            txn['category'],
            txn['amount'],
            txn['balance'] if txn['balance'] is not None else '',
            ''
        ])
    
    # Close last month
    if current_month is not None:
        rows.append(['', '', f'SUBTOTAL: {prev_month_name}', month_subtotal, '', f'{month_count} transactions'])
    
    return rows


def build_monthly_summary(transactions):
    """Build monthly spending/income summaries."""
    monthly = defaultdict(lambda: defaultdict(float))
    
    for txn in transactions:
        mk = txn['month_key']
        cat = txn['category']
        monthly[mk][cat] += txn['amount']
    
    return monthly


def build_category_totals(transactions):
    """Build category totals."""
    cats = defaultdict(float)
    for txn in transactions:
        cats[txn['category']] += txn['amount']
    return dict(sorted(cats.items(), key=lambda x: x[1]))


def build_yearly_summary(transactions):
    """Build yearly spending/income summaries."""
    yearly = defaultdict(lambda: defaultdict(float))
    for txn in transactions:
        yr = str(txn['year'])
        cat = txn['category']
        yearly[yr][cat] += txn['amount']
    return yearly


# ============================================================
# MAIN BUILD
# ============================================================

def main():
    print("🔄 Parsing CSV files...")
    txns_0068 = parse_0068(CSV_0068)
    txns_4252 = parse_4252(CSV_4252)
    
    print(f"  ✅ 0068: {len(txns_0068)} transactions parsed")
    print(f"  ✅ 4252: {len(txns_4252)} transactions parsed")
    
    # Print category breakdown for verification
    cats_0068 = build_category_totals(txns_0068)
    cats_4252 = build_category_totals(txns_4252)
    
    print("\n📊 0068 Category Breakdown:")
    for cat, total in sorted(cats_0068.items(), key=lambda x: x[1]):
        print(f"  {cat}: {fmt_currency(total)}")
    
    print("\n📊 4252 Category Breakdown:")
    for cat, total in sorted(cats_4252.items(), key=lambda x: x[1]):
        print(f"  {cat}: {fmt_currency(total)}")
    
    # Get OAuth token
    print("\n🔑 Getting OAuth token...")
    TOKEN = get_token()
    print("  ✅ Token acquired")
    
    # ============================================================
    # STEP 1: Create new tabs
    # ============================================================
    print("\n📝 Creating new tabs...")
    
    new_tab_ids = {
        'personal_overview': 200,
        'personal_0068': 201,
        'personal_4252': 202,
    }
    
    create_requests = [
        {
            'addSheet': {
                'properties': {
                    'sheetId': new_tab_ids['personal_overview'],
                    'title': '👤 Personal Overview',
                    'index': 1,  # After dashboard
                    'tabColorStyle': {'rgbColor': LIGHT_BLUE_TAB},
                    'gridProperties': {'frozenRowCount': 0, 'columnCount': 15}
                }
            }
        },
        {
            'addSheet': {
                'properties': {
                    'sheetId': new_tab_ids['personal_0068'],
                    'title': '👤 Personal 0068',
                    'index': 2,
                    'tabColorStyle': {'rgbColor': LIGHT_BLUE_TAB},
                    'gridProperties': {'frozenRowCount': 1, 'rowCount': max(len(txns_0068) + 200, 2000), 'columnCount': 6}
                }
            }
        },
        {
            'addSheet': {
                'properties': {
                    'sheetId': new_tab_ids['personal_4252'],
                    'title': '💎 Personal 4252',
                    'index': 3,
                    'tabColorStyle': {'rgbColor': LIGHT_BLUE_TAB},
                    'gridProperties': {'frozenRowCount': 1, 'rowCount': max(len(txns_4252) + 200, 500), 'columnCount': 6}
                }
            }
        }
    ]
    
    # Delete if they already exist (idempotent)
    meta_url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets(properties(sheetId,title))'
    meta_resp = requests.get(meta_url, headers={'Authorization': f'Bearer {TOKEN}'})
    existing_sheets = {s['properties']['title']: s['properties']['sheetId'] for s in meta_resp.json()['sheets']}
    
    delete_requests = []
    for title in ['👤 Personal Overview', '👤 Personal 0068', '💎 Personal 4252']:
        if title in existing_sheets:
            delete_requests.append({'deleteSheet': {'sheetId': existing_sheets[title]}})
    
    if delete_requests:
        print(f"  Deleting {len(delete_requests)} existing tabs...")
        batch_update(TOKEN, delete_requests)
    
    result = batch_update(TOKEN, create_requests)
    print("  ✅ New tabs created")
    
    # ============================================================
    # STEP 2: Populate 👤 Personal 0068 transaction log
    # ============================================================
    print("\n📝 Building Personal 0068 transaction log...")
    
    header_0068 = ['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']
    log_0068 = build_transaction_log(txns_0068, 'Personal Checking 0068')
    all_rows_0068 = [header_0068] + log_0068
    
    update_values(TOKEN, "'👤 Personal 0068'!A1", all_rows_0068)
    print(f"  ✅ Wrote {len(all_rows_0068)} rows")
    
    # ============================================================
    # STEP 3: Populate 💎 Personal 4252 transaction log
    # ============================================================
    print("\n📝 Building Personal 4252 transaction log...")
    
    header_4252 = ['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']
    log_4252 = build_transaction_log(txns_4252, 'Sapphire CC 4252')
    all_rows_4252 = [header_4252] + log_4252
    
    update_values(TOKEN, "'💎 Personal 4252'!A1", all_rows_4252)
    print(f"  ✅ Wrote {len(all_rows_4252)} rows")
    
    # ============================================================
    # STEP 4: Build 👤 Personal Overview dashboard
    # ============================================================
    print("\n📝 Building Personal Overview dashboard...")
    
    # Combine all personal transactions
    all_personal = txns_0068 + txns_4252
    
    # --- Build monthly summaries ---
    monthly_0068 = build_monthly_summary(txns_0068)
    monthly_4252 = build_monthly_summary(txns_4252)
    yearly_0068 = build_yearly_summary(txns_0068)
    yearly_4252 = build_yearly_summary(txns_4252)
    
    # Get all unique months sorted
    all_months = sorted(set(list(monthly_0068.keys()) + list(monthly_4252.keys())))
    all_years = sorted(set([t['year'] for t in all_personal]))
    
    # Define spending categories (debits)
    spending_cats = [
        '📈 Investment', '🏠 Living / Local', '🍔 Food & Dining', '📺 Subscription',
        '✈️ Travel', '🛍️ Shopping & Misc', '💳 CC Payment', '💳 Debt Payment',
        '💰 Interest & Fees', '🏧 ATM / Cash / FX', '🔄 Transfer', '📣 Business Ad Spend',
        '💊 Health', '📱 Phone / Tech', '🚗 Transportation'
    ]
    
    income_cats = ["💵 Owner's Draw", '💵 Zelle Income', '💵 Income', '💵 Refund', '💵 Other Income']
    
    overview_rows = []
    
    # SECTION A: PERSONAL INCOME
    overview_rows.append(['💰 PERSONAL INCOME SUMMARY'])
    overview_rows.append([])
    
    # Yearly income summary
    overview_rows.append(['Source', '2024', '2025', '2026 YTD', 'All Time'])
    
    for cat in income_cats:
        row = [cat]
        total = 0
        for yr in ['2024', '2025', '2026']:
            val_0068 = yearly_0068.get(yr, {}).get(cat, 0)
            val_4252 = yearly_4252.get(yr, {}).get(cat, 0)
            combined = val_0068 + val_4252
            total += combined
            row.append(combined if combined != 0 else '')
        row.append(total if total != 0 else '')
        overview_rows.append(row)
    
    # Total income row
    row = ['TOTAL INCOME']
    all_time_income = 0
    for yr in ['2024', '2025', '2026']:
        yr_total = 0
        for cat in income_cats:
            yr_total += yearly_0068.get(yr, {}).get(cat, 0) + yearly_4252.get(yr, {}).get(cat, 0)
        all_time_income += yr_total
        row.append(yr_total if yr_total != 0 else '')
    row.append(all_time_income)
    overview_rows.append(row)
    
    overview_rows.append([])
    overview_rows.append([])
    
    # SECTION B: PERSONAL SPENDING BY CATEGORY
    overview_rows.append(['💸 PERSONAL SPENDING BY CATEGORY'])
    overview_rows.append([])
    overview_rows.append(['Category', '2024', '2025', '2026 YTD', 'All Time', '% of Total'])
    
    yearly_spending_totals = {'2024': 0, '2025': 0, '2026': 0}
    all_time_spending = 0
    cat_all_time = {}
    
    for cat in spending_cats:
        row = [cat]
        cat_total = 0
        for yr in ['2024', '2025', '2026']:
            val_0068 = yearly_0068.get(yr, {}).get(cat, 0)
            val_4252 = yearly_4252.get(yr, {}).get(cat, 0)
            combined = val_0068 + val_4252
            cat_total += combined
            yearly_spending_totals[yr] += combined
            row.append(combined if combined != 0 else '')
        all_time_spending += cat_total
        cat_all_time[cat] = cat_total
        row.append(cat_total if cat_total != 0 else '')
        row.append('')  # % placeholder
        overview_rows.append(row)
    
    # Total spending row
    row = ['TOTAL SPENDING']
    for yr in ['2024', '2025', '2026']:
        row.append(yearly_spending_totals[yr])
    row.append(all_time_spending)
    row.append('100%')
    overview_rows.append(row)
    
    # Now go back and fill in percentages
    if all_time_spending != 0:
        # We'll set formulas after writing — for now, calculate
        pass
    
    overview_rows.append([])
    overview_rows.append([])
    
    # SECTION C: PERSONAL CASH FLOW
    overview_rows.append(['📈 PERSONAL CASH FLOW (Monthly)'])
    overview_rows.append([])
    overview_rows.append(['Month', 'Income', 'Spending', 'Net Cash Flow', 'Running Total'])
    
    running_total = 0
    for mk in all_months:
        month_date = datetime.strptime(mk + '-01', '%Y-%m-%d')
        month_label = month_date.strftime('%b %Y')
        
        income = 0
        spending = 0
        for cat in income_cats:
            income += monthly_0068.get(mk, {}).get(cat, 0) + monthly_4252.get(mk, {}).get(cat, 0)
        for cat in spending_cats:
            spending += monthly_0068.get(mk, {}).get(cat, 0) + monthly_4252.get(mk, {}).get(cat, 0)
        
        net = income + spending  # spending is negative
        running_total += net
        
        overview_rows.append([month_label, income, spending, net, running_total])
    
    overview_rows.append([])
    overview_rows.append([])
    
    # SECTION D: CREDIT CARD SUMMARY (4252)
    overview_rows.append(['💎 SAPPHIRE 4252 SUMMARY'])
    overview_rows.append([])
    overview_rows.append(['Category', '2024', '2025', '2026 YTD', 'All Time'])
    
    for cat in sorted(cats_4252.keys(), key=lambda x: cats_4252[x]):
        row = [cat]
        for yr in ['2024', '2025', '2026']:
            val = yearly_4252.get(yr, {}).get(cat, 0)
            row.append(val if val != 0 else '')
        row.append(cats_4252[cat])
        overview_rows.append(row)
    
    # Total row
    total_4252 = sum(cats_4252.values())
    row = ['TOTAL']
    for yr in ['2024', '2025', '2026']:
        yr_total = sum(yearly_4252.get(yr, {}).values())
        row.append(yr_total if yr_total != 0 else '')
    row.append(total_4252)
    overview_rows.append(row)
    
    overview_rows.append([])
    overview_rows.append([])
    
    # SECTION E: MONTHLY SPENDING HEATMAP
    overview_rows.append(['📊 MONTHLY SPENDING BREAKDOWN (0068 Checking)'])
    overview_rows.append([])
    
    # Header with categories
    active_cats = [c for c in spending_cats if any(monthly_0068.get(mk, {}).get(c, 0) != 0 for mk in all_months)]
    heatmap_header = ['Month'] + active_cats + ['TOTAL']
    overview_rows.append(heatmap_header)
    
    for mk in all_months:
        month_date = datetime.strptime(mk + '-01', '%Y-%m-%d')
        month_label = month_date.strftime('%b %Y')
        row = [month_label]
        row_total = 0
        for cat in active_cats:
            val = monthly_0068.get(mk, {}).get(cat, 0)
            row_total += val
            row.append(val if val != 0 else '')
        row.append(row_total)
        overview_rows.append(row)
    
    # Write Personal Overview
    update_values(TOKEN, "'👤 Personal Overview'!A1", overview_rows)
    print(f"  ✅ Wrote {len(overview_rows)} rows to Personal Overview")
    
    # ============================================================
    # STEP 5: Format all new tabs
    # ============================================================
    print("\n🎨 Applying formatting...")
    
    format_requests = []
    
    # --- Format Personal Overview ---
    sid = new_tab_ids['personal_overview']
    
    # Column widths
    col_widths = [200, 130, 130, 130, 130, 100, 130, 130, 130, 130, 130, 130, 130, 130, 130]
    for i, w in enumerate(col_widths):
        format_requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': sid, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i+1},
                'properties': {'pixelSize': w},
                'fields': 'pixelSize'
            }
        })
    
    # Find section header rows and format them
    section_rows = []
    for i, row in enumerate(overview_rows):
        if row and len(row) > 0 and isinstance(row[0], str):
            label = row[0]
            if label.startswith('💰 PERSONAL') or label.startswith('💸 PERSONAL') or \
               label.startswith('📈 PERSONAL') or label.startswith('💎 SAPPHIRE') or \
               label.startswith('📊 MONTHLY'):
                section_rows.append(i)
                # Navy background, white text, 14pt bold
                format_requests.append({
                    'repeatCell': {
                        'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': NAVY,
                                'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 14, 'fontFamily': 'Arial'},
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                })
                # Merge the header row
                format_requests.append({
                    'mergeCells': {
                        'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 5},
                        'mergeType': 'MERGE_ALL'
                    }
                })
                # Row height 30px
                format_requests.append({
                    'updateDimensionProperties': {
                        'range': {'sheetId': sid, 'dimension': 'ROWS', 'startIndex': i, 'endIndex': i+1},
                        'properties': {'pixelSize': 30},
                        'fields': 'pixelSize'
                    }
                })
            
            # Column headers (Source, Category, Month, etc.)
            if label in ['Source', 'Category', 'Month'] and i > 0:
                format_requests.append({
                    'repeatCell': {
                        'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': LIGHT_GRAY,
                                'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                })
            
            # TOTAL rows
            if label.startswith('TOTAL'):
                format_requests.append({
                    'repeatCell': {
                        'range': {'sheetId': sid, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 15},
                        'cell': {
                            'userEnteredFormat': {
                                'backgroundColor': TOTALS_BG,
                                'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                            }
                        },
                        'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                    }
                })
    
    # Currency format for columns B-E on overview (rows with numbers)
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': len(overview_rows), 'startColumnIndex': 1, 'endColumnIndex': 15},
            'cell': {
                'userEnteredFormat': {
                    'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                    'fontFamily': 'Arial', 'fontSize': 10
                }
            },
            'fields': 'userEnteredFormat(numberFormat,fontFamily,fontSize)'
        }
    })
    
    # Default font for all text
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid, 'startRowIndex': 0, 'endRowIndex': len(overview_rows), 'startColumnIndex': 0, 'endColumnIndex': 1},
            'cell': {
                'userEnteredFormat': {
                    'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                }
            },
            'fields': 'userEnteredFormat(textFormat)'
        }
    })
    
    # --- Format 0068 Transaction Log ---
    sid_0068 = new_tab_ids['personal_0068']
    
    # Column widths
    widths_0068 = [110, 250, 200, 130, 130, 200]
    for i, w in enumerate(widths_0068):
        format_requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': sid_0068, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i+1},
                'properties': {'pixelSize': w},
                'fields': 'pixelSize'
            }
        })
    
    # Header row - navy
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid_0068, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': NAVY,
                    'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                    'horizontalAlignment': 'CENTER'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    })
    # Header row height
    format_requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': sid_0068, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 30},
            'fields': 'pixelSize'
        }
    })
    
    # Currency format for Amount and Balance columns (D, E)
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid_0068, 'startRowIndex': 1, 'endRowIndex': len(all_rows_0068), 'startColumnIndex': 3, 'endColumnIndex': 5},
            'cell': {
                'userEnteredFormat': {
                    'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                    'fontFamily': 'Arial', 'fontSize': 10
                }
            },
            'fields': 'userEnteredFormat(numberFormat,fontFamily,fontSize)'
        }
    })
    
    # Default font
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid_0068, 'startRowIndex': 1, 'endRowIndex': len(all_rows_0068), 'startColumnIndex': 0, 'endColumnIndex': 3},
            'cell': {
                'userEnteredFormat': {
                    'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                }
            },
            'fields': 'userEnteredFormat(textFormat)'
        }
    })
    
    # Format month header rows and subtotal rows for 0068
    for i, row in enumerate(all_rows_0068):
        if i == 0:
            continue
        if row and len(row) > 0 and isinstance(row[0], str) and row[0].startswith('📅'):
            # Month header - light blue background
            format_requests.append({
                'repeatCell': {
                    'range': {'sheetId': sid_0068, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.886, 'green': 0.937, 'blue': 0.992},  # Light blue
                            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
        if row and len(row) > 2 and isinstance(row[2], str) and 'SUBTOTAL' in str(row[2]):
            format_requests.append({
                'repeatCell': {
                    'range': {'sheetId': sid_0068, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': TOTALS_BG,
                            'textFormat': {'bold': True, 'fontSize': 10, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
    
    # --- Format 4252 Transaction Log ---
    sid_4252 = new_tab_ids['personal_4252']
    
    widths_4252 = [110, 250, 200, 130, 130, 200]
    for i, w in enumerate(widths_4252):
        format_requests.append({
            'updateDimensionProperties': {
                'range': {'sheetId': sid_4252, 'dimension': 'COLUMNS', 'startIndex': i, 'endIndex': i+1},
                'properties': {'pixelSize': w},
                'fields': 'pixelSize'
            }
        })
    
    # Header row
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid_4252, 'startRowIndex': 0, 'endRowIndex': 1, 'startColumnIndex': 0, 'endColumnIndex': 6},
            'cell': {
                'userEnteredFormat': {
                    'backgroundColor': NAVY,
                    'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                    'horizontalAlignment': 'CENTER'
                }
            },
            'fields': 'userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)'
        }
    })
    format_requests.append({
        'updateDimensionProperties': {
            'range': {'sheetId': sid_4252, 'dimension': 'ROWS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 30},
            'fields': 'pixelSize'
        }
    })
    
    # Currency format
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid_4252, 'startRowIndex': 1, 'endRowIndex': len(all_rows_4252), 'startColumnIndex': 3, 'endColumnIndex': 5},
            'cell': {
                'userEnteredFormat': {
                    'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                    'fontFamily': 'Arial', 'fontSize': 10
                }
            },
            'fields': 'userEnteredFormat(numberFormat,fontFamily,fontSize)'
        }
    })
    
    # Default font
    format_requests.append({
        'repeatCell': {
            'range': {'sheetId': sid_4252, 'startRowIndex': 1, 'endRowIndex': len(all_rows_4252), 'startColumnIndex': 0, 'endColumnIndex': 3},
            'cell': {
                'userEnteredFormat': {
                    'textFormat': {'fontFamily': 'Arial', 'fontSize': 10}
                }
            },
            'fields': 'userEnteredFormat(textFormat)'
        }
    })
    
    # Format month headers and subtotals for 4252
    for i, row in enumerate(all_rows_4252):
        if i == 0:
            continue
        if row and len(row) > 0 and isinstance(row[0], str) and row[0].startswith('📅'):
            format_requests.append({
                'repeatCell': {
                    'range': {'sheetId': sid_4252, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': {'red': 0.886, 'green': 0.937, 'blue': 0.992},
                            'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
        if row and len(row) > 2 and isinstance(row[2], str) and 'SUBTOTAL' in str(row[2]):
            format_requests.append({
                'repeatCell': {
                    'range': {'sheetId': sid_4252, 'startRowIndex': i, 'endRowIndex': i+1, 'startColumnIndex': 0, 'endColumnIndex': 6},
                    'cell': {
                        'userEnteredFormat': {
                            'backgroundColor': TOTALS_BG,
                            'textFormat': {'bold': True, 'fontSize': 10, 'fontFamily': 'Arial'},
                        }
                    },
                    'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                }
            })
    
    # Apply all formatting in batches (API limit is ~100 per request)
    batch_size = 80
    for i in range(0, len(format_requests), batch_size):
        batch = format_requests[i:i+batch_size]
        print(f"  Applying format batch {i//batch_size + 1} ({len(batch)} requests)...")
        batch_update(TOKEN, batch)
    
    print("  ✅ Formatting applied")
    
    # ============================================================
    # STEP 6: Update year tabs with personal spending sections
    # ============================================================
    print("\n📝 Updating year tabs with personal spending...")
    
    year_tab_map = {'2024': 3, '2025': 1, '2026': 2}  # sheetId mapping
    
    for year_str, sheet_id in year_tab_map.items():
        print(f"\n  Processing 📅 {year_str}...")
        
        # Read current tab to find where to append
        tab_name = f'📅 {year_str}'
        read_url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{requests.utils.quote(tab_name)}!A1:H200'
        read_resp = requests.get(read_url, headers={'Authorization': f'Bearer {TOKEN}'})
        existing = read_resp.json().get('values', [])
        
        # Find last row with data
        last_row = len(existing)
        start_row = last_row + 2  # 2 blank rows after existing content
        
        # Build personal spending section for this year
        personal_rows = []
        personal_rows.append([])
        personal_rows.append([])
        personal_rows.append([f'👤 {year_str} PERSONAL SPENDING'])
        personal_rows.append([])
        personal_rows.append(['Category', 'Total', '% of Spending'])
        
        yr_cats_0068 = yearly_0068.get(year_str, {})
        yr_cats_4252 = yearly_4252.get(year_str, {})
        
        # Combine categories
        yr_combined = defaultdict(float)
        for cat, val in yr_cats_0068.items():
            yr_combined[cat] += val
        for cat, val in yr_cats_4252.items():
            yr_combined[cat] += val
        
        # Separate income vs spending
        yr_spending = {}
        yr_income = {}
        for cat, val in yr_combined.items():
            if cat.startswith('💵'):
                yr_income[cat] = val
            else:
                yr_spending[cat] = val
        
        total_spending = sum(yr_spending.values())
        
        # Sort by amount (most negative first)
        for cat, val in sorted(yr_spending.items(), key=lambda x: x[1]):
            pct = f'{val/total_spending*100:.0f}%' if total_spending != 0 else '0%'
            personal_rows.append([cat, val, pct])
        
        personal_rows.append(['TOTAL SPENDING', total_spending, '100%'])
        
        personal_rows.append([])
        personal_rows.append([])
        personal_rows.append([f'💵 {year_str} PERSONAL INCOME'])
        personal_rows.append([])
        personal_rows.append(['Source', 'Total'])
        
        total_income_yr = 0
        for cat, val in sorted(yr_income.items(), key=lambda x: -x[1]):
            personal_rows.append([cat, val])
            total_income_yr += val
        personal_rows.append(['TOTAL INCOME', total_income_yr])
        
        personal_rows.append([])
        personal_rows.append(['💰 NET PERSONAL CASH FLOW', total_income_yr + total_spending])
        
        # Monthly breakdown
        personal_rows.append([])
        personal_rows.append([])
        personal_rows.append([f'📅 {year_str} MONTHLY PERSONAL BREAKDOWN'])
        personal_rows.append([])
        personal_rows.append(['Month', "Owner's Draws", 'Other Income', 'Total Spending', 'Net Cash Flow'])
        
        months_in_year = sorted([mk for mk in all_months if mk.startswith(year_str)])
        for mk in months_in_year:
            month_date = datetime.strptime(mk + '-01', '%Y-%m-%d')
            month_label = month_date.strftime('%B')
            
            draws = monthly_0068.get(mk, {}).get("💵 Owner's Draw", 0) + monthly_4252.get(mk, {}).get("💵 Owner's Draw", 0)
            other_income = sum(
                monthly_0068.get(mk, {}).get(c, 0) + monthly_4252.get(mk, {}).get(c, 0)
                for c in income_cats if c != "💵 Owner's Draw"
            )
            spending = sum(
                monthly_0068.get(mk, {}).get(c, 0) + monthly_4252.get(mk, {}).get(c, 0)
                for c in spending_cats
            )
            net = draws + other_income + spending
            
            personal_rows.append([month_label, draws, other_income, spending, net])
        
        # Write to year tab
        range_str = f"'{tab_name}'!A{start_row}"
        update_values(TOKEN, range_str, personal_rows)
        print(f"    ✅ Wrote {len(personal_rows)} rows starting at row {start_row}")
        
        # Format section headers in year tabs
        yr_format_reqs = []
        for i, row in enumerate(personal_rows):
            abs_row = start_row - 1 + i  # 0-indexed
            if row and len(row) > 0 and isinstance(row[0], str):
                label = row[0]
                if label.startswith('👤') or label.startswith('💵') and 'PERSONAL' in label or label.startswith('📅') and 'MONTHLY PERSONAL' in label:
                    yr_format_reqs.append({
                        'repeatCell': {
                            'range': {'sheetId': sheet_id, 'startRowIndex': abs_row, 'endRowIndex': abs_row+1, 'startColumnIndex': 0, 'endColumnIndex': 8},
                            'cell': {
                                'userEnteredFormat': {
                                    'backgroundColor': PERSONAL_BLUE,
                                    'textFormat': {'foregroundColorStyle': {'rgbColor': WHITE}, 'bold': True, 'fontSize': 14, 'fontFamily': 'Arial'},
                                }
                            },
                            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                        }
                    })
                    yr_format_reqs.append({
                        'mergeCells': {
                            'range': {'sheetId': sheet_id, 'startRowIndex': abs_row, 'endRowIndex': abs_row+1, 'startColumnIndex': 0, 'endColumnIndex': 5},
                            'mergeType': 'MERGE_ALL'
                        }
                    })
                
                if label in ['Category', 'Source', 'Month']:
                    yr_format_reqs.append({
                        'repeatCell': {
                            'range': {'sheetId': sheet_id, 'startRowIndex': abs_row, 'endRowIndex': abs_row+1, 'startColumnIndex': 0, 'endColumnIndex': 8},
                            'cell': {
                                'userEnteredFormat': {
                                    'backgroundColor': LIGHT_GRAY,
                                    'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                                }
                            },
                            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                        }
                    })
                
                if label.startswith('TOTAL') or label.startswith('💰 NET'):
                    yr_format_reqs.append({
                        'repeatCell': {
                            'range': {'sheetId': sheet_id, 'startRowIndex': abs_row, 'endRowIndex': abs_row+1, 'startColumnIndex': 0, 'endColumnIndex': 8},
                            'cell': {
                                'userEnteredFormat': {
                                    'backgroundColor': TOTALS_BG,
                                    'textFormat': {'bold': True, 'fontSize': 11, 'fontFamily': 'Arial'},
                                }
                            },
                            'fields': 'userEnteredFormat(backgroundColor,textFormat)'
                        }
                    })
        
        # Currency format for year tab personal section
        yr_format_reqs.append({
            'repeatCell': {
                'range': {'sheetId': sheet_id, 'startRowIndex': start_row - 1, 'endRowIndex': start_row - 1 + len(personal_rows), 'startColumnIndex': 1, 'endColumnIndex': 6},
                'cell': {
                    'userEnteredFormat': {
                        'numberFormat': {'type': 'CURRENCY', 'pattern': '$#,##0.00;[Red]($#,##0.00)'},
                        'fontFamily': 'Arial', 'fontSize': 10
                    }
                },
                'fields': 'userEnteredFormat(numberFormat,fontFamily,fontSize)'
            }
        })
        
        if yr_format_reqs:
            batch_update(TOKEN, yr_format_reqs)
            print(f"    ✅ Formatted personal section")
    
    # ============================================================
    # STEP 7: Generate Report
    # ============================================================
    print("\n📄 Generating report...")
    
    report = generate_report(txns_0068, txns_4252, cats_0068, cats_4252, 
                            yearly_0068, yearly_4252, monthly_0068, monthly_4252, all_months)
    
    with open(REPORT_PATH, 'w') as f:
        f.write(report)
    
    print(f"  ✅ Report written to {REPORT_PATH}")
    print("\n🎉 DONE! All personal finance data has been added to the sheet.")


def generate_report(txns_0068, txns_4252, cats_0068, cats_4252, 
                    yearly_0068, yearly_4252, monthly_0068, monthly_4252, all_months):
    """Generate the markdown report."""
    
    income_cats = ["💵 Owner's Draw", '💵 Zelle Income', '💵 Income', '💵 Refund', '💵 Other Income']
    spending_cats = [
        '📈 Investment', '🏠 Living / Local', '🍔 Food & Dining', '📺 Subscription',
        '✈️ Travel', '🛍️ Shopping & Misc', '💳 CC Payment', '💳 Debt Payment',
        '💰 Interest & Fees', '🏧 ATM / Cash / FX', '🔄 Transfer', '📣 Business Ad Spend',
        '💊 Health', '📱 Phone / Tech', '🚗 Transportation'
    ]
    
    lines = []
    lines.append("# 👤 Personal Finance Data Report")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Sheet:** All Time Financial Overview")
    lines.append("")
    lines.append("---")
    lines.append("")
    
    # Summary
    lines.append("## 📊 Summary")
    lines.append("")
    lines.append(f"| Account | Transactions | Date Range |")
    lines.append(f"|---------|-------------|------------|")
    
    if txns_0068:
        dates_0068 = sorted([t['date'] for t in txns_0068])
        lines.append(f"| Chase Personal 0068 | {len(txns_0068)} | {dates_0068[0].strftime('%m/%d/%Y')} — {dates_0068[-1].strftime('%m/%d/%Y')} |")
    if txns_4252:
        dates_4252 = sorted([t['date'] for t in txns_4252])
        lines.append(f"| Sapphire CC 4252 | {len(txns_4252)} | {dates_4252[0].strftime('%m/%d/%Y')} — {dates_4252[-1].strftime('%m/%d/%Y')} |")
    
    lines.append(f"| **Total** | **{len(txns_0068) + len(txns_4252)}** | |")
    lines.append("")
    
    # 0068 Breakdown
    lines.append("## 💰 Personal Checking (0068) — Category Breakdown")
    lines.append("")
    lines.append("| Category | All Time | Count |")
    lines.append("|----------|---------|-------|")
    
    cat_counts = defaultdict(int)
    for t in txns_0068:
        cat_counts[t['category']] += 1
    
    for cat, total in sorted(cats_0068.items(), key=lambda x: x[1]):
        lines.append(f"| {cat} | {fmt_currency(total)} | {cat_counts.get(cat, 0)} |")
    
    total_0068 = sum(cats_0068.values())
    lines.append(f"| **TOTAL** | **{fmt_currency(total_0068)}** | **{len(txns_0068)}** |")
    lines.append("")
    
    # Income analysis
    total_draws = sum(t['amount'] for t in txns_0068 if t['category'] == "💵 Owner's Draw")
    total_zelle = sum(t['amount'] for t in txns_0068 if t['category'] == '💵 Zelle Income')
    lines.append("### 💵 Personal Income Breakdown")
    lines.append("")
    lines.append(f"- **Owner's Draws (4991 → 0068):** {fmt_currency(total_draws)}")
    lines.append(f"- **Zelle Received:** {fmt_currency(total_zelle)}")
    lines.append(f"- **Other Income:** {fmt_currency(sum(t['amount'] for t in txns_0068 if t['category'] in ['💵 Income', '💵 Refund', '💵 Other Income']))}")
    lines.append("")
    
    # 4252 Breakdown
    lines.append("## 💎 Sapphire CC (4252) — Category Breakdown")
    lines.append("")
    lines.append("| Category | All Time | Count |")
    lines.append("|----------|---------|-------|")
    
    cat_counts_4252 = defaultdict(int)
    for t in txns_4252:
        cat_counts_4252[t['category']] += 1
    
    for cat, total in sorted(cats_4252.items(), key=lambda x: x[1]):
        lines.append(f"| {cat} | {fmt_currency(total)} | {cat_counts_4252.get(cat, 0)} |")
    
    total_4252 = sum(cats_4252.values())
    lines.append(f"| **TOTAL** | **{fmt_currency(total_4252)}** | **{len(txns_4252)}** |")
    lines.append("")
    
    # Yearly Summary
    lines.append("## 📅 Yearly Summary")
    lines.append("")
    
    for year_str in ['2024', '2025', '2026']:
        yr_income = sum(
            yearly_0068.get(year_str, {}).get(c, 0) + yearly_4252.get(year_str, {}).get(c, 0)
            for c in income_cats
        )
        yr_spending = sum(
            yearly_0068.get(year_str, {}).get(c, 0) + yearly_4252.get(year_str, {}).get(c, 0)
            for c in spending_cats
        )
        yr_net = yr_income + yr_spending
        
        lines.append(f"### {year_str}")
        lines.append(f"- Income: {fmt_currency(yr_income)}")
        lines.append(f"- Spending: {fmt_currency(yr_spending)}")
        lines.append(f"- Net Cash Flow: {fmt_currency(yr_net)}")
        lines.append("")
    
    # Top spending categories
    lines.append("## 🏆 Top Personal Spending Categories (All Time)")
    lines.append("")
    
    all_cats = defaultdict(float)
    for t in txns_0068 + txns_4252:
        if not t['category'].startswith('💵') and t['amount'] < 0:
            all_cats[t['category']] += t['amount']
    
    lines.append("| Rank | Category | Amount |")
    lines.append("|------|----------|--------|")
    for rank, (cat, val) in enumerate(sorted(all_cats.items(), key=lambda x: x[1]), 1):
        lines.append(f"| {rank} | {cat} | {fmt_currency(val)} |")
    lines.append("")
    
    # Tabs created
    lines.append("## ✅ Tabs Created/Updated")
    lines.append("")
    lines.append("| Tab | Description | Rows |")
    lines.append("|-----|-------------|------|")
    lines.append(f"| 👤 Personal Overview | Dashboard with income, spending, cash flow | N/A |")
    lines.append(f"| 👤 Personal 0068 | Transaction log — {len(txns_0068)} transactions | {len(txns_0068)} |")
    lines.append(f"| 💎 Personal 4252 | Transaction log — {len(txns_4252)} transactions | {len(txns_4252)} |")
    lines.append(f"| 📅 2024 | Updated with personal spending section | — |")
    lines.append(f"| 📅 2025 | Updated with personal spending section | — |")
    lines.append(f"| 📅 2026 | Updated with personal spending section | — |")
    lines.append("")
    
    lines.append("## 🎨 Formatting Applied")
    lines.append("")
    lines.append("- Tab colors: Light blue (#4285F4) for personal tabs")
    lines.append("- Section headers: Navy (#1B2A4A) for overview, Blue (#4285F4) for year tab personal sections")
    lines.append("- Column headers: Gray (#F3F3F3)")
    lines.append("- Currency: $#,##0.00;[Red]($#,##0.00)")
    lines.append("- Font: Arial 10pt")
    lines.append("- Transaction logs: Grouped by month with subtotals")
    lines.append("")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    main()
