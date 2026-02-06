#!/usr/bin/env python3
"""
January 2026 Accounting Sheet Builder
Creates a beautiful Google Sheet for Marko's Chase Personal 0068 account.
"""

import csv
import json
import sys
import requests as req
from io import StringIO
from collections import defaultdict, OrderedDict

# === CONFIGURATION ===
TOKEN_FILE = '/home/ec2-user/.config/gcal-pro/token.json'
CSV_FILE = '/home/ec2-user/.clawdbot/media/inbound/69300223-3d85-4a27-8ab7-189e87f6ffd4.csv'
SHEET_ID_FILE = '/home/ec2-user/clawd/data/jan-2026-sheet-id.txt'
SHARE_EMAIL = 'mark@kuriosbrand.com'

# Sheet IDs (set in create request)
DASH_ID = 0
TXN_ID = 1
RAW_ID = 2

# === COLORS (RGB 0-1 floats) ===
def rgb(r, g, b):
    return {'red': r/255, 'green': g/255, 'blue': b/255}

NAVY = rgb(27, 42, 74)
MED_NAVY = rgb(44, 62, 107)
SECTION_BG = rgb(35, 55, 92)
WHITE = rgb(255, 255, 255)
LIGHT_GRAY = rgb(245, 246, 250)
VERY_LIGHT_BLUE = rgb(235, 240, 250)
INCOME_GREEN_BG = rgb(232, 248, 240)
EXPENSE_RED_BG = rgb(255, 235, 238)
GREEN_TEXT = rgb(39, 174, 96)
RED_TEXT = rgb(214, 48, 49)
DARK_TEXT = rgb(44, 62, 80)
TOTAL_BG = rgb(225, 232, 245)
METRIC_BG = rgb(248, 249, 252)
NOTE_BG = rgb(255, 253, 245)
BORDER_COLOR = rgb(200, 206, 218)
ACCENT_GOLD = rgb(243, 156, 18)

# ============================================================
# TOKEN MANAGEMENT
# ============================================================
def refresh_token():
    with open(TOKEN_FILE) as f:
        creds = json.load(f)
    
    # Try existing token first
    token = creds.get('token', '')
    if token:
        r = req.get('https://www.googleapis.com/oauth2/v1/tokeninfo',
                     params={'access_token': token})
        if r.status_code == 200:
            print(f"✓ Token valid ({r.json().get('expires_in', '?')}s remaining)")
            return token
    
    # Refresh
    print("Refreshing token...")
    r = req.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token'
    })
    r.raise_for_status()
    new_token = r.json()['access_token']
    
    creds['token'] = new_token
    with open(TOKEN_FILE, 'w') as f:
        json.dump(creds, f, indent=2)
    
    print(f"✓ Token refreshed")
    return new_token

# ============================================================
# CSV PARSING
# ============================================================
def parse_csv():
    with open(CSV_FILE, 'r') as f:
        content = f.read()
    
    reader = csv.reader(StringIO(content))
    header = next(reader)
    
    rows = []
    for row in reader:
        if len(row) < 6:
            continue
        detail = row[0].strip()
        date = row[1].strip()
        desc = row[2].strip()
        try:
            amount = float(row[3].strip())
        except (ValueError, IndexError):
            continue
        txn_type = row[4].strip() if len(row) > 4 else ''
        balance_str = row[5].strip() if len(row) > 5 else ''
        try:
            balance = float(balance_str) if balance_str else None
        except ValueError:
            balance = None
        
        rows.append({
            'detail': detail,
            'date': date,
            'description': desc,
            'amount': amount,
            'type': txn_type,
            'balance': balance
        })
    
    # Reverse for chronological order
    rows.reverse()
    
    # Calculate starting balance
    first_with_bal = next((r for r in rows if r['balance'] is not None), None)
    if first_with_bal:
        starting_balance = first_with_bal['balance'] - first_with_bal['amount']
    else:
        starting_balance = 155.64
    
    # Calculate running balance
    running = starting_balance
    for r in rows:
        running += r['amount']
        running = round(running, 2)
        r['running_balance'] = running
    
    print(f"✓ Parsed {len(rows)} transactions")
    print(f"  Starting balance: ${starting_balance:.2f}")
    print(f"  Ending balance: ${running:.2f}")
    
    return rows, starting_balance, running

# ============================================================
# CATEGORIZATION
# ============================================================
EXPENSE_CATEGORIES = OrderedDict([
    ('🏧 ATM/Cash', 'atm'),
    ('📈 Investments', 'invest'),
    ('💳 CC Payments', 'cc'),
    ('🎓 Student Loan', 'student'),
    ('📺 Subscriptions', 'subs'),
    ('✈️ Travel', 'travel'),
    ('💰 Savings Transfers', 'savings'),
    ('🔄 Transfers to Business', 'business'),
    ('🏠 Other', 'other'),
])

INCOME_CATEGORIES = OrderedDict([
    ('💼 Business Transfers In', 'biz_in'),
    ('💰 From Savings', 'sav_in'),
    ('📈 Investment Returns', 'invest_in'),
    ('🔄 Other Credits', 'other_in'),
])

def categorize(desc, amount):
    d = desc.upper()
    
    # ATM/Cash
    if 'ATM WITHDRAW' in d or 'ATM DEBIT' in d:
        return 'atm'
    if 'NON-CHASE ATM FEE' in d:
        return 'atm'
    if 'FOREIGN EXCHANGE' in d:
        return 'atm'
    
    # Investments (debits)
    if ('ROBINHOOD' in d and 'DEBITS' in d) or 'ORIG CO NAME:ROBINHOOD' in d:
        if amount < 0:
            return 'invest'
    if ('ACORNS INVEST' in d or 'ACORNS ROUND' in d) and amount < 0:
        return 'invest'
    
    # Acorns subscription fee
    if 'SUBSCRIPTION' in d and 'ACORNS' in d:
        return 'subs'
    
    # CC Payment
    if 'CHASE CREDIT CRD AUTOPAY' in d:
        return 'cc'
    
    # Student Loan
    if 'DEPT EDUCATION' in d or 'STUDENT LN' in d:
        return 'student'
    
    # Subscriptions
    if 'HULU' in d:
        return 'subs'
    if 'SOLSTICE' in d and amount < 0:
        return 'subs'
    if 'PATREON' in d:
        return 'subs'
    
    # Travel
    if 'IBERIA' in d or 'LATAM AIRLIN' in d:
        return 'travel'
    if 'AIRALO' in d:
        return 'travel'
    
    # Savings transfers
    if 'TRANSFER TO  SAV' in d or 'TRANSFER TO SAV' in d:
        return 'savings'
    
    # Business transfers
    if 'TRANSFER TO CHK ...4991' in d or 'TRANSFER TO  CHK ...4991' in d:
        return 'business'
    
    # === INCOME CATEGORIES ===
    # Business transfers in
    if ('TRANSFER FROM CHK ...4991' in d or 'TRANSFER FROM  CHK ...4991' in d) and amount > 0:
        return 'biz_in'
    
    # Savings in
    if ('TRANSFER FROM SAV ...7036' in d or 'TRANSFER FROM  SAV ...7036' in d) and amount > 0:
        return 'sav_in'
    
    # Investment returns
    if 'ROBINHOOD SECURITIES' in d or 'REAL TIME TRANSFER' in d and 'ROBINHOOD' in d:
        if amount > 0:
            return 'invest_in'
    if 'ACORNS INVEST' in d and amount > 0:
        return 'invest_in'
    
    # ODP
    if 'ODP' in d or 'TOT ODP' in d:
        return 'other_in'
    
    # Solstice refund
    if 'SOLSTICE' in d and amount > 0:
        return 'other_in'
    
    # Kula Community
    if 'KULA' in d:
        return 'other'
    
    # Default
    if amount < 0:
        return 'other'
    return 'other_in'

def clean_vendor(desc, amount):
    d = desc.upper()
    
    if 'HULU' in d:
        return 'Hulu'
    if 'ATM DEBIT' in d:
        loc = extract_location(desc)
        return f'ATM Withdrawal — {loc}'
    if 'ORIG CO NAME:ACORNS INVEST' in d:
        return 'Acorns Invest'
    if 'ACORNS INVEST' in d and 'TRANSFER' in d:
        if amount > 0:
            return 'Acorns (Return)'
        return 'Acorns Invest'
    if 'ACORNS ROUND' in d:
        return 'Acorns Round-Ups'
    if 'SUBSCRIPTION' in d and 'ACORNS' in d:
        return 'Acorns (Subscription Fee)'
    if 'ORIG CO NAME:ROBINHOOD' in d:
        return 'Robinhood'
    if 'ROBINHOOD' in d and 'DEBITS' in d:
        return 'Robinhood'
    if 'REAL TIME TRANSFER' in d and 'ROBINHOOD' in d:
        return 'Robinhood (Transfer In)'
    if 'TOT ODP' in d:
        return 'Overdraft Protection Credit'
    if 'ODP TRANSFER' in d:
        return 'ODP from Savings'
    if 'NON-CHASE ATM FEE' in d:
        return 'Non-Chase ATM Fee'
    if 'FOREIGN EXCHANGE' in d:
        loc = extract_fx_location(desc)
        return f'Foreign Exchange Fee — {loc}'
    if 'NON-CHASE ATM WITHDRAW' in d:
        loc = extract_location(desc)
        return f'ATM Withdrawal — {loc}'
    if 'TRANSFER TO  SAV ...7036' in d or 'TRANSFER TO SAV ...7036' in d:
        return '→ Savings (7036)'
    if 'TRANSFER FROM SAV ...7036' in d or 'TRANSFER FROM  SAV ...7036' in d:
        return '← Savings (7036)'
    if 'TRANSFER FROM CHK ...4991' in d or 'TRANSFER FROM  CHK ...4991' in d:
        return '← Business Checking (4991)'
    if 'TRANSFER TO CHK ...4991' in d or 'TRANSFER TO  CHK ...4991' in d:
        return '→ Business Checking (4991)'
    if 'AIRALO' in d:
        return 'Airalo (eSIM)'
    if 'PATREON' in d:
        return 'Patreon Membership'
    if 'CHASE CREDIT CRD AUTOPAY' in d:
        return 'Chase Sapphire CC Payment'
    if 'DEPT EDUCATION' in d:
        return 'Student Loan Payment'
    if 'IBERIA' in d:
        return 'Iberia Airlines'
    if 'LATAM AIRLIN' in d:
        return 'LATAM Airlines'
    if 'SOLSTICE' in d:
        if amount > 0:
            return 'Solstice Dental (Refund)'
        return 'Solstice Dental Insurance'
    if 'KULA COMMUNITY' in d:
        return 'Kula Community — Pisac'
    return desc[:50]

def extract_location(desc):
    d = desc.upper()
    if 'PISAC' in d or ('CALLE BOL' in d and ('PISAC' in d or '564' in d)):
        return 'Pisac, Peru'
    if 'CALLE BOL' in d:
        return 'Calle Bolognesi, Peru'
    if 'AV LA CUL' in d:
        return 'Cusco, Peru'
    if 'AV  FEDER' in d or 'AV FEDER' in d:
        return 'Cusco, Peru'
    if 'PISAC, CU' in d:
        return 'Pisac, Peru'
    return 'Peru'

def extract_fx_location(desc):
    d = desc.upper()
    if 'CALLE BOL' in d:
        return 'Calle Bolognesi'
    if 'AV LA CUL' in d:
        return 'Cusco'
    if 'AV  FEDER' in d or 'AV FEDER' in d:
        return 'Cusco'
    if 'KULA COMM' in d:
        return 'Kula Community'
    if 'PISAC' in d:
        return 'Pisac'
    return 'Peru'

def get_category_label(cat_key):
    for label, key in list(EXPENSE_CATEGORIES.items()) + list(INCOME_CATEGORIES.items()):
        if key == cat_key:
            return label
    return cat_key

# ============================================================
# PROCESS TRANSACTIONS
# ============================================================
def process_transactions(rows):
    for r in rows:
        r['category'] = categorize(r['description'], r['amount'])
        r['vendor'] = clean_vendor(r['description'], r['amount'])
        r['cat_label'] = get_category_label(r['category'])
    
    # Build category summaries
    expense_cats = defaultdict(lambda: {'total': 0, 'count': 0})
    income_cats = defaultdict(lambda: {'total': 0, 'count': 0})
    
    for r in rows:
        cat = r['category']
        if cat in [v for v in EXPENSE_CATEGORIES.values()]:
            expense_cats[cat]['total'] += r['amount']
            expense_cats[cat]['count'] += 1
        elif cat in [v for v in INCOME_CATEGORIES.values()]:
            income_cats[cat]['total'] += r['amount']
            income_cats[cat]['count'] += 1
    
    total_income = sum(r['amount'] for r in rows if r['amount'] > 0)
    total_expenses = sum(r['amount'] for r in rows if r['amount'] < 0)
    
    # Key metrics
    atm_withdrawals = sum(r['amount'] for r in rows 
                          if 'ATM WITHDRAW' in r['description'].upper() or 'ATM DEBIT' in r['description'].upper())
    atm_fees = sum(r['amount'] for r in rows if 'NON-CHASE ATM FEE' in r['description'].upper())
    fx_fees = sum(r['amount'] for r in rows if 'FOREIGN EXCHANGE' in r['description'].upper())
    invest_total = sum(r['amount'] for r in rows 
                       if r['category'] == 'invest')
    
    return {
        'expense_cats': dict(expense_cats),
        'income_cats': dict(income_cats),
        'total_income': total_income,
        'total_expenses': total_expenses,
        'atm_withdrawals': atm_withdrawals,
        'atm_fees': atm_fees,
        'fx_fees': fx_fees,
        'invest_total': invest_total,
    }

# ============================================================
# GOOGLE SHEETS API HELPERS
# ============================================================
def sheets_api(token, method, url, body=None):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    if method == 'POST':
        r = req.post(url, headers=headers, json=body)
    elif method == 'PUT':
        r = req.put(url, headers=headers, json=body)
    else:
        r = req.get(url, headers=headers)
    
    if r.status_code not in (200, 201):
        print(f"API Error {r.status_code}: {r.text[:500]}")
        r.raise_for_status()
    return r.json()

# Formatting helper functions
def merge_req(sheet_id, r1, r2, c1, c2):
    return {
        'mergeCells': {
            'range': {'sheetId': sheet_id, 'startRowIndex': r1, 'endRowIndex': r2,
                      'startColumnIndex': c1, 'endColumnIndex': c2},
            'mergeType': 'MERGE_ALL'
        }
    }

def repeat_cell_req(sheet_id, r1, r2, c1, c2, bg=None, fg=None, bold=False, 
                     font_size=None, h_align=None, v_align=None, num_fmt=None,
                     font_family=None, wrap=