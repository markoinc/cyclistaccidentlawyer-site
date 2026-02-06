#!/usr/bin/env python3
"""
Rebuild January 2026 Dashboard — KuriosBrand Financial Overview
Reads all 4 transaction tabs, categorizes, calculates, and writes a fully formatted Dashboard.
"""

import requests
import json
import re
import sys
from datetime import datetime

# ─── CONFIG ───
SPREADSHEET_ID = '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE'
DASHBOARD_SHEET_ID = 0  # gid for Dashboard tab

OAUTH = {
    'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
    'client_secret': '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',
    'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
    'grant_type': 'refresh_token'
}

# Tab names
TABS = [
    '💼 Business 4991',
    '👤 Personal 0068',
    '💳 Biz CC 0678',
    '💎 Sapphire 4252',
]

# ─── COLORS ───
NAVY = {'red': 0.106, 'green': 0.165, 'blue': 0.290}  # #1B2A4A
WHITE = {'red': 1, 'green': 1, 'blue': 1}
LIGHT_GRAY = {'red': 0.953, 'green': 0.953, 'blue': 0.953}  # #F3F3F3
TOTALS_BG = {'red': 0.910, 'green': 0.929, 'blue': 0.898}  # #E8EDF5 approx
TOTALS_BG_ACTUAL = {'red': 0.910, 'green': 0.929, 'blue': 0.949}  # #E8EDF5
GREEN_TEXT = {'red': 0, 'green': 0.380, 'blue': 0}  # #006100
RED_TEXT = {'red': 0.800, 'green': 0, 'blue': 0}  # #CC0000
BLACK = {'red': 0, 'green': 0, 'blue': 0}
ALT_ROW = {'red': 0.941, 'green': 0.957, 'blue': 1.0}  # #F0F4FF

def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data=OAUTH)
    r.raise_for_status()
    return r.json()['access_token']

def sheets_get(token, ranges):
    """Batch get multiple ranges."""
    params = [('ranges', r) for r in ranges]
    params.append(('valueRenderOption', 'UNFORMATTED_VALUE'))
    params.append(('dateTimeRenderOption', 'FORMATTED_STRING'))
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values:batchGet'
    r = requests.get(url, headers={'Authorization': f'Bearer {token}'}, params=params)
    r.raise_for_status()
    return r.json()

def sheets_update(token, body):
    """batchUpdate for formatting."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate'
    r = requests.post(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }, json=body)
    r.raise_for_status()
    return r.json()

def sheets_values_update(token, range_name, values):
    """Write values to a range."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_name}'
    r = requests.put(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }, params={'valueInputOption': 'USER_ENTERED'}, json={'values': values})
    r.raise_for_status()
    return r.json()

def sheets_clear(token, range_name):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{range_name}:clear'
    r = requests.post(url, headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }, json={})
    r.raise_for_status()
    return r.json()

def parse_amount(val):
    """Parse a value into a float amount."""
    if val is None or val == '':
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).replace('$', '').replace(',', '').strip()
    # Handle parentheses for negatives
    if s.startswith('(') and s.endswith(')'):
        s = '-' + s[1:-1]
    try:
        return float(s)
    except:
        return 0.0

def parse_rows(raw_values):
    """Parse raw sheet values into list of dicts."""
    if not raw_values:
        return []
    rows = []
    # Skip header row
    for row in raw_values[1:]:
        # Pad to 6 columns
        while len(row) < 6:
            row.append('')
        date_str = str(row[0]).strip() if row[0] else ''
        vendor = str(row[1]).strip() if row[1] else ''
        category = str(row[2]).strip() if row[2] else ''
        amount = parse_amount(row[3])
        balance = parse_amount(row[4])
        notes = str(row[5]).strip() if row[5] else ''
        if not date_str and not vendor:
            continue
        rows.append({
            'date': date_str,
            'vendor': vendor,
            'category': category,
            'amount': amount,
            'balance': balance,
            'notes': notes,
        })
    return rows

# ─── CATEGORIZATION RULES ───

def is_transfer(row, tab):
    """Determine if a transaction is an inter-account transfer to exclude."""
    v = row['vendor'].lower()
    cat = row['category'].lower()
    
    # Explicit transfer category
    if 'transfer' in cat and '🔄' in row['category']:
        return True
    
    # Common transfer patterns
    transfer_keywords = [
        'transfer to', 'transfer from', 'online transfer',
        'chase credit crd', 'payment to chase card',
        'chase crd epay', 'automatic payment',
        'save', 'savings',
    ]
    for kw in transfer_keywords:
        if kw in v:
            return True
    
    # CC Payments from checking accounts
    if tab in ['💼 Business 4991', '👤 Personal 0068']:
        if 'chase credit crd' in v or 'payment to chase card' in v or 'chase crd epay' in v:
            return True
    
    # CC Payment received on CC side
    if tab in ['💳 Biz CC 0678', '💎 Sapphire 4252']:
        if 'payment' in v and 'thank you' in v:
            return True
        if 'automatic payment' in v:
            return True
    
    return False

def is_income(row, tab):
    """Determine if a transaction is income."""
    if row['amount'] <= 0:
        return False
    v = row['vendor'].lower()
    cat = row['category'].lower()
    
    # Alexander Shtabsky $500 Zelle is NOT income (personal ATM cash favor)
    if 'shtabsky' in v or 'alexander s' in v:
        return False
    
    # Stripe Capital loan disbursement is NOT income
    if 'stripe' in v and row['amount'] >= 4000 and row['amount'] <= 4300:
        print(f"  ⚠️ Excluding Stripe Capital disbursement: ${row['amount']:,.2f} on {row['date']}")
        return False
    
    if tab == '💼 Business 4991':
        # Deposits, Zelle received, Stripe
        if 'zelle' in v and row['amount'] > 0:
            return True
        if 'stripe' in v and row['amount'] > 0:
            return True
        if 'deposit' in v and row['amount'] > 0:
            return True
        if '💵' in row['category']:
            return True
        if 'revenue' in cat or 'income' in cat:
            return True
        # Credit Strong or any other credit
        if 'credit strong' in v or 'creditstrong' in v:
            return True
    
    return False

def classify_income(row):
    """Classify income into business line, source, method."""
    v = row['vendor'].lower()
    notes = row['notes'].lower()
    
    # Determine method
    method = 'Other'
    if 'zelle' in v:
        method = 'Zelle'
    elif 'stripe' in v:
        method = 'Stripe'
    elif 'deposit' in v:
        method = 'Deposit'
    
    # Determine source and business line
    source = row['vendor']
    biz_line = '🚗 MVA Lead Gen'
    note = ''
    
    # Known MVA clients
    mva_clients = {
        'anthony reddin': ('Anthony Reddin', 'Retainer'),
        'reddin': ('Anthony Reddin', 'Retainer'),
        'aci enterprise': ('ACI Enterprise', 'Retainer'),
        'aci': ('ACI Enterprise', 'Retainer'),
        'a-z mobile': ('A-Z Mobile Apps', 'Retainer'),
        'a z mobile': ('A-Z Mobile Apps', 'Retainer'),
        'jonathan bible': ('Jonathan Bible', 'Retainer'),
        'bible': ('Jonathan Bible', 'Retainer'),
        'christian willard': ('Christian Willard', 'Per-lead'),
        'willard': ('Christian Willard', 'Per-lead'),
    }
    
    matched = False
    for key, (name, note_text) in mva_clients.items():
        if key in v or key in notes:
            source = name
            note = note_text
            matched = True
            break
    
    if not matched:
        if 'stripe' in v:
            source = 'Stripe (MVA clients)'
            note = 'Net after fees + Stripe Capital 20%'
        elif 'credit strong' in v or 'creditstrong' in v:
            biz_line = '🔧 SEO / One-Time'
            source = 'Credit Strong'
            note = 'Monthly'
            method = 'Stripe' if 'stripe' in v else method
    
    return biz_line, source, method, note

def classify_biz_expense(row, tab):
    """Classify a business expense into category."""
    v = row['vendor'].lower()
    cat = row['category']
    amount = abs(row['amount'])
    
    # Category mapping based on vendor keywords
    saas_keywords = ['highlevel', 'high level', 'gohighlevel', 'go high level',
                     'openai', 'anthropic', 'chatgpt', 'claude',
                     'semrush', 'ahrefs', 'dataforseo', 'data for seo',
                     'google workspace', 'gsuite', 'google llc',
                     'zapier', 'make.com', 'n8n', 'pabbly',
                     'canva', 'adobe', 'namecheap', 'godaddy', 'cloudflare',
                     'twilio', 'callrail', 'call rail', 'calendly',
                     'slack', 'notion', 'clickup', 'asana',
                     'typeform', 'jotform', 'webflow', 'carrd',
                     'github', 'heroku', 'vercel', 'netlify', 'aws', 'amazon web',
                     'digital ocean', 'vultr', 'linode',
                     'loom', 'zoom', 'krisp', 'grammarly',
                     'clawdbot', 'cursor', 'replit',
                     'basecamp', 'lemlist', 'instantly', 'smartlead',
                     'apollo', 'bettercontact', 'better contact',
                     'phantom', 'phantombuster', 'apify',
                     'webshare', 'brightdata', 'bright data',
                     'neon', 'supabase', 'firebase',
                     'mailgun', 'sendgrid', 'postmark',
                     'stripe billing', 'close.com', 'close crm',
                     'pipedrive', 'hubspot',
                     'wordpress', 'elementor', 'divi',
                     'envato', 'themeforest',
                     'monday.com', 'airtable',
                     'siteground', 'bluehost', 'hostinger',
                     'screaming frog', 'spyfu', 'moz',
                     'surfer seo', 'surferseo', 'jasper', 'frase',
                     'descript', 'riverside',
                     'intercom', 'drift', 'tidio', 'crisp',
                     'hootsuite', 'buffer', 'sprout',
                     'later', 'planoly',
                     'quickbooks', 'xero', 'freshbooks', 'wave',
                     'gusto', 'justworks',
                     ]
    
    ads_keywords = ['meta ads', 'facebook ads', 'facebk', 'fb ads',
                    'google ads', 'goog ads', 'adwords',
                    'bing ads', 'microsoft ads',
                    'tiktok ads', 'linkedin ads',
                    'taboola', 'outbrain',
                    'meta platform', 'facebook', 'fb ',
                    ]
    
    ops_keywords = ['office', 'cowork', 'wework', 'regus',
                    'uber', 'lyft', 'parking',
                    'staples', 'office depot',
                    'insurance', 'liability',
                    'legal', 'attorney', 'lawyer',
                    'accountant', 'cpa', 'bookkeeper',
                    'internet', 'comcast', 'spectrum',
                    'phone', 't-mobile', 'verizon', 'at&t',
                    'usps', 'ups', 'fedex',
                    'tax', 'irs',
                    'misc', 'supply', 'supplies',
                    ]
    
    debt_keywords = ['loan', 'stripe capital', 'capital repay',
                     'payment - thank', 'discover',
                     'sba', 'line of credit',
                     'kabbage', 'bluevine', 'ondeck',
                     ]
    
    fee_keywords = ['fee', 'interest', 'finance charge',
                    'service charge', 'monthly fee',
                    'overdraft', 'nsf',
                    'annual fee',
                    ]
    
    atm_keywords = ['atm', 'cash withdrawal', 'cash back',
                    'cash advance',
                    ]
    
    # Check categories in order of specificity
    for kw in atm_keywords:
        if kw in v:
            return '🏧 Business ATM / Cash', 'No'
    
    for kw in fee_keywords:
        if kw in v:
            return '💰 Business Fees & Interest', 'Monthly' if 'monthly' in v or 'service charge' in v else 'No'
    
    for kw in debt_keywords:
        if kw in v:
            return '💳 Debt Payments', 'Monthly'
    
    for kw in ads_keywords:
        if kw in v:
            return '📣 Marketing / Ads', 'Variable'
    
    for kw in saas_keywords:
        if kw in v:
            return '📱 SaaS & Tools', 'Monthly'
    
    for kw in ops_keywords:
        if kw in v:
            return '🏢 Operations', 'Variable'
    
    # Use the category from the sheet if it has emoji prefix
    if '📱' in cat:
        return '📱 SaaS & Tools', 'Monthly'
    elif '📣' in cat:
        return '📣 Marketing / Ads', 'Variable'
    elif '🏢' in cat:
        return '🏢 Operations', 'Variable'
    elif '💳' in cat and 'debt' in cat.lower():
        return '💳 Debt Payments', 'Monthly'
    elif '💰' in cat:
        return '💰 Business Fees & Interest', 'Monthly'
    elif '🏧' in cat:
        return '🏧 Business ATM / Cash', 'No'
    
    # Default to Operations
    return '🏢 Operations', 'No'

def classify_personal_expense(row, tab):
    """Classify a personal expense into category."""
    v = row['vendor'].lower()
    cat = row['category']
    amount = row['amount']  # negative for expenses
    
    invest_keywords = ['robinhood', 'acorns', 'schwab', 'fidelity', 'vanguard',
                       'webull', 'etrade', 'ameritrade', 'coinbase', 'kraken',
                       'binance', 'gemini',
                       ]
    
    living_keywords = ['rent', 'landlord', 'property', 'electric', 'gas bill',
                       'water', 'utility', 'utilities', 'comcast', 'spectrum',
                       'internet', 'wifi', 'power', 'energy',
                       'laundry', 'dry clean',
                       'grocery', 'groceries', 'trader joe', 'whole foods',
                       'walmart', 'target', 'costco', 'safeway', 'kroger',
                       'bodega', 'corner store', 'supermarket',
                       'pharmacy', 'cvs', 'walgreen', 'rite aid',
                       'metro', 'subway', 'bus', 'transit',
                       'local', 'misc local',
                       ]
    
    food_keywords = ['restaurant', 'cafe', 'coffee', 'starbucks', 'dunkin',
                     'mcdonald', 'burger', 'pizza', 'sushi', 'taco',
                     'chipotle', 'panera', 'subway', 'wendy',
                     'doordash', 'uber eat', 'ubereats', 'grubhub', 'postmates',
                     'seamless', 'caviar', 'rappi', 'deliveroo',
                     'bar', 'pub', 'brewery', 'wine',
                     'food', 'dining', 'eat', 'cook',
                     'bakery', 'deli', 'bagel',
                     ]
    
    subscription_keywords = ['hulu', 'netflix', 'spotify', 'apple music',
                             'disney', 'hbo', 'paramount', 'peacock',
                             'youtube premium', 'prime video',
                             'audible', 'kindle',
                             'patreon', 'substack', 'medium',
                             'solstice', 'calm', 'headspace',
                             'subscription', 'recurring',
                             'icloud', 'google one', 'dropbox',
                             'nordvpn', 'expressvpn',
                             'xbox', 'playstation', 'ps plus',
                             'nintendo',
                             ]
    
    travel_keywords = ['airline', 'airfare', 'flight', 'airport',
                       'united', 'delta', 'american air', 'southwest',
                       'jetblue', 'spirit', 'frontier', 'avianca',
                       'latam', 'copa', 'volaris',
                       'hotel', 'airbnb', 'hostel', 'booking.com',
                       'expedia', 'kayak', 'trivago',
                       'airalo', 'esim', 'e-sim',
                       'rental car', 'hertz', 'avis', 'enterprise rent',
                       'travel', 'trip',
                       'international', 'foreign',
                       'global', 'intl',
                       ]
    
    shopping_keywords = ['amazon', 'amzn', 'ebay', 'etsy',
                         'best buy', 'apple store', 'microsoft store',
                         'nike', 'adidas', 'zara', 'h&m',
                         'uniqlo', 'gap', 'old navy',
                         'nordstrom', 'macys', 'bloomingdale',
                         'clothing', 'shoes', 'apparel',
                         'electronics', 'gadget',
                         'shopping', 'retail', 'store',
                         'wish', 'shein', 'temu',
                         ]
    
    cc_payment_keywords = ['payment to chase card', 'chase credit crd',
                           'chase crd epay', 'epay',
                           'credit card payment', 'cc payment',
                           'payment thank you',
                           ]
    
    cc_fee_keywords = ['interest charge', 'finance charge',
                       'annual fee', 'late fee',
                       'interest on',
                       'purchase interest',
                       'cash advance interest',
                       ]
    
    atm_keywords = ['atm', 'cash withdrawal', 'cash back',
                    'foreign transaction', 'fx fee', 'intl fee',
                    'international fee', 'currency',
                    'non-chase', 'non chase',
                    ]
    
    loan_keywords = ['dept of ed', 'department of education',
                     'student loan', 'navient', 'nelnet',
                     'great lakes', 'fedloan', 'mohela',
                     'aidvantage', 'student aid',
                     'dept of educ',
                     ]
    
    # CC interest/fees (for Sapphire tab)
    if tab == '💎 Sapphire 4252':
        for kw in cc_fee_keywords:
            if kw in v:
                return '💰 CC Interest & Fees (Personal)', 'Monthly'
        for kw in cc_payment_keywords:
            if kw in v:
                return None, None  # This is a transfer, skip
    
    # Student loans
    for kw in loan_keywords:
        if kw in v:
            return '🎓 Student Loans', 'Monthly'
    
    # ATM / Cash / FX
    for kw in atm_keywords:
        if kw in v:
            return '🏧 ATM / Cash / FX Fees', 'No'
    
    # CC Payments from personal checking
    if tab == '👤 Personal 0068':
        for kw in cc_payment_keywords:
            if kw in v:
                return '💳 CC Payments (Personal)', 'Monthly'
    
    # CC Interest & Fees
    for kw in cc_fee_keywords:
        if kw in v:
            return '💰 CC Interest & Fees (Personal)', 'Monthly'
    
    # Investments
    for kw in invest_keywords:
        if kw in v:
            return '📈 Investments (Net Flows)', 'Daily' if 'daily' in v else 'Variable'
    
    # Travel (check before food/living to catch restaurants in travel context)
    for kw in travel_keywords:
        if kw in v:
            return '✈️ Travel', 'No'
    
    # Subscriptions
    for kw in subscription_keywords:
        if kw in v:
            return '📺 Subscriptions', 'Monthly'
    
    # Food & Dining
    for kw in food_keywords:
        if kw in v:
            return '🍔 Food & Dining', 'No'
    
    # Shopping
    for kw in shopping_keywords:
        if kw in v:
            return '🛍️ Shopping & Misc', 'No'
    
    # Living
    for kw in living_keywords:
        if kw in v:
            return '🏠 Living / Local', 'Monthly' if any(k in v for k in ['rent', 'electric', 'internet', 'utility']) else 'No'
    
    # Use category from sheet
    if '📈' in cat:
        return '📈 Investments (Net Flows)', 'Variable'
    elif '🏠' in cat:
        return '🏠 Living / Local', 'Variable'
    elif '🍔' in cat:
        return '🍔 Food & Dining', 'No'
    elif '📺' in cat:
        return '📺 Subscriptions', 'Monthly'
    elif '✈️' in cat:
        return '✈️ Travel', 'No'
    elif '🛍️' in cat or 'shopping' in cat.lower():
        return '🛍️ Shopping & Misc', 'No'
    elif '💳' in cat and 'payment' in cat.lower():
        return '💳 CC Payments (Personal)', 'Monthly'
    elif '💰' in cat:
        return '💰 CC Interest & Fees (Personal)', 'Monthly'
    elif '🏧' in cat:
        return '🏧 ATM / Cash / FX Fees', 'No'
    elif '🎓' in cat:
        return '🎓 Student Loans', 'Monthly'
    
    # Default
    return '🛍️ Shopping & Misc', 'No'

# ─── FORMATTING HELPERS ───

def fmt_currency(val):
    """Format as currency string."""
    if val >= 0:
        return f'${val:,.2f}'
    else:
        return f'-${abs(val):,.2f}'

def fmt_pct(val):
    """Format as percentage."""
    return f'{val:.1f}%'

def make_color(color_dict):
    return {
        'red': color_dict.get('red', 0),
        'green': color_dict.get('green', 0),
        'blue': color_dict.get('blue', 0),
    }

def bg_format(row_idx, col_start, col_end, bg_color, bold=False, font_size=10, font_color=None):
    """Create a repeatCell formatting request."""
    cell_format = {
        'backgroundColor': make_color(bg_color),
        'textFormat': {
            'bold': bold,
            'fontSize': font_size,
        }
    }
    fields = 'userEnteredFormat.backgroundColor,userEnteredFormat.textFormat.bold,userEnteredFormat.textFormat.fontSize'
    
    if font_color:
        cell_format['textFormat']['foregroundColor'] = make_color(font_color)
        fields += ',userEnteredFormat.textFormat.foregroundColor'
    
    return {
        'repeatCell': {
            'range': {
                'sheetId': DASHBOARD_SHEET_ID,
                'startRowIndex': row_idx,
                'endRowIndex': row_idx + 1,
                'startColumnIndex': col_start,
                'endColumnIndex': col_end,
            },
            'cell': {'userEnteredFormat': cell_format},
            'fields': fields,
        }
    }

def merge_cells(row_idx, col_start, col_end):
    return {
        'mergeCells': {
            'range': {
                'sheetId': DASHBOARD_SHEET_ID,
                'startRowIndex': row_idx,
                'endRowIndex': row_idx + 1,
                'startColumnIndex': col_start,
                'endColumnIndex': col_end,
            },
            'mergeType': 'MERGE_ALL',
        }
    }

def number_format_request(start_row, end_row, start_col, end_col, pattern):
    return {
        'repeatCell': {
            'range': {
                'sheetId': DASHBOARD_SHEET_ID,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col,
            },
            'cell': {
                'userEnteredFormat': {
                    'numberFormat': {
                        'type': 'NUMBER',
                        'pattern': pattern,
                    }
                }
            },
            'fields': 'userEnteredFormat.numberFormat',
        }
    }

# ─── MAIN ───

def main():
    print("=" * 60)
    print("🔄 REBUILDING January 2026 Dashboard")
    print("=" * 60)
    
    # Step 0: Get token
    print("\n📌 Getting OAuth token...")
    token = get_token()
    print("✅ Token acquired")
    
    # Step 1: Read all tabs in one batch
    print("\n📌 Reading all 4 transaction tabs...")
    ranges = [f"'{tab}'!A:F" for tab in TABS]
    result = sheets_get(token, ranges)
    
    all_data = {}
    for i, tab in enumerate(TABS):
        vr = result.get('valueRanges', [])[i]
        raw = vr.get('values', [])
        rows = parse_rows(raw)
        all_data[tab] = rows
        print(f"  ✅ {tab}: {len(rows)} transactions")
    
    # Step 2: Categorize everything
    print("\n📌 Categorizing transactions...")
    
    # ─── INCOME ───
    income_items = []
    for tab in TABS:
        for row in all_data[tab]:
            if is_transfer(row, tab):
                continue
            if is_income(row, tab):
                biz_line, source, method, note = classify_income(row)
                income_items.append({
                    'biz_line': biz_line,
                    'source': source,
                    'method': method,
                    'amount': row['amount'],
                    'note': note,
                    'vendor': row['vendor'],
                    'date': row['date'],
                })
    
    print(f"  ✅ Income items: {len(income_items)}")
    for item in income_items:
        print(f"     {item['date']} | {item['source']} | {item['method']} | ${item['amount']:,.2f} | {item['vendor']}")
    
    # ─── BUSINESS EXPENSES ───
    biz_expenses = []
    for tab in ['💼 Business 4991', '💳 Biz CC 0678']:
        for row in all_data[tab]:
            if is_transfer(row, tab):
                continue
            if is_income(row, tab):
                continue
            if row['amount'] >= 0:
                # Positive on CC could be a refund, but skip credits on checking that aren't income
                if tab == '💳 Biz CC 0678' and row['amount'] > 0:
                    # CC refund - include as negative expense (credit)
                    pass
                else:
                    continue
            
            cat, recurring = classify_biz_expense(row, tab)
            biz_expenses.append({
                'category': cat,
                'vendor': row['vendor'],
                'amount': row['amount'],
                'recurring': recurring,
                'notes': row['notes'],
                'date': row['date'],
                'tab': tab,
            })
    
    print(f"  ✅ Business expenses: {len(biz_expenses)}")
    
    # ─── PERSONAL EXPENSES ───
    personal_expenses = []
    for tab in ['👤 Personal 0068', '💎 Sapphire 4252']:
        for row in all_data[tab]:
            if is_transfer(row, tab):
                continue
            # Skip income on personal
            if tab == '👤 Personal 0068' and row['amount'] > 0:
                # Could be transfer FROM business or other income - skip positive
                continue
            if tab == '💎 Sapphire 4252' and row['amount'] > 0:
                # Payment received on CC (transfer) - skip
                continue
            
            cat, recurring = classify_personal_expense(row, tab)
            if cat is None:
                continue  # Marked as transfer
            
            personal_expenses.append({
                'category': cat,
                'vendor': row['vendor'],
                'amount': row['amount'],
                'recurring': recurring,
                'notes': row['notes'],
                'date': row['date'],
                'tab': tab,
            })
    
    print(f"  ✅ Personal expenses: {len(personal_expenses)}")
    
    # ─── AGGREGATE ───
    
    # Income by business line
    income_by_line = {}
    for item in income_items:
        bl = item['biz_line']
        if bl not in income_by_line:
            income_by_line[bl] = []
        income_by_line[bl].append(item)
    
    total_income = sum(i['amount'] for i in income_items)
    print(f"\n💰 Total Income: ${total_income:,.2f}")
    
    for bl, items in income_by_line.items():
        subtotal = sum(i['amount'] for i in items)
        print(f"   {bl}: ${subtotal:,.2f}")
    
    # Business expenses by category
    biz_by_cat = {}
    biz_cat_order = ['📱 SaaS & Tools', '📣 Marketing / Ads', '🏢 Operations',
                     '💳 Debt Payments', '💰 Business Fees & Interest', '🏧 Business ATM / Cash']
    for exp in biz_expenses:
        cat = exp['category']
        if cat not in biz_by_cat:
            biz_by_cat[cat] = []
        biz_by_cat[cat].append(exp)
    
    total_biz_exp = sum(e['amount'] for e in biz_expenses)
    print(f"\n📊 Total Business Expenses: ${total_biz_exp:,.2f}")
    for cat in biz_cat_order:
        items = biz_by_cat.get(cat, [])
        if items:
            subtotal = sum(i['amount'] for i in items)
            print(f"   {cat}: ${subtotal:,.2f} ({len(items)} items)")
    
    # Personal expenses by category
    personal_by_cat = {}
    personal_cat_order = [
        '📈 Investments (Net Flows)', '🏠 Living / Local', '🍔 Food & Dining',
        '📺 Subscriptions', '✈️ Travel', '🛍️ Shopping & Misc',
        '💳 CC Payments (Personal)', '💰 CC Interest & Fees (Personal)',
        '🏧 ATM / Cash / FX Fees', '🎓 Student Loans',
    ]
    for exp in personal_expenses:
        cat = exp['category']
        if cat not in personal_by_cat:
            personal_by_cat[cat] = []
        personal_by_cat[cat].append(exp)
    
    total_personal_exp = sum(e['amount'] for e in personal_expenses)
    print(f"\n👤 Total Personal Expenses: ${total_personal_exp:,.2f}")
    for cat in personal_cat_order:
        items = personal_by_cat.get(cat, [])
        if items:
            subtotal = sum(i['amount'] for i in items)
            print(f"   {cat}: ${subtotal:,.2f} ({len(items)} items)")
    
    # ─── MONEY FLOWS ───
    flows = []
    # Find transfers from business to personal
    for row in all_data['💼 Business 4991']:
        v = row['vendor'].lower()
        if row['amount'] < 0 and ('transfer' in v or 'online transfer' in v):
            if 'savings' not in v and 'save' not in v:
                # Could be biz → personal or biz → CC
                if 'chase credit' in v or 'chase crd' in v or 'payment to chase' in v:
                    flows.append(('Business → Biz CC', '4991', '0678', abs(row['amount']), 'CC Payment'))
                else:
                    flows.append(('Business → Personal', '4991', '0068', abs(row['amount']), 'Owner draw'))
    
    for row in all_data['👤 Personal 0068']:
        v = row['vendor'].lower()
        if row['amount'] < 0:
            if 'robinhood' in v:
                flows.append(('Personal → Investments', '0068', 'Robinhood', abs(row['amount']), 'Stock buys'))
            elif 'acorns' in v:
                flows.append(('Personal → Investments', '0068', 'Acorns', abs(row['amount']), 'Index funds'))
            elif 'savings' in v or 'save' in v:
                flows.append(('Personal → Savings', '0068', '7036', abs(row['amount']), 'Auto-saves'))
    
    # ─── BUILD DASHBOARD CONTENT ───
    print("\n📌 Building dashboard content...")
    
    rows_data = []  # List of row values
    format_requests = []  # Formatting requests
    
    row_idx = 0
    
    # === SECTION A: INCOME SUMMARY ===
    # Section header
    rows_data.append(['💰 SECTION A: INCOME SUMMARY', '', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    # Column headers
    rows_data.append(['Business Line', 'Source', 'Method', 'Amount', '% of Total', 'Notes'])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    income_line_order = ['🚗 MVA Lead Gen', '🏗️ Rank & Rent', '🔧 SEO / One-Time']
    
    for bl in income_line_order:
        items = income_by_line.get(bl, [])
        if items:
            # Consolidate by source
            by_source = {}
            for item in items:
                key = (item['source'], item['method'])
                if key not in by_source:
                    by_source[key] = {'amount': 0, 'note': item['note']}
                by_source[key]['amount'] += item['amount']
            
            for (source, method), data in by_source.items():
                pct = (data['amount'] / total_income * 100) if total_income else 0
                rows_data.append([bl, source, method, data['amount'], f'{pct:.1f}%', data['note']])
                row_idx += 1
        
        # Subtotal for this business line
        subtotal = sum(i['amount'] for i in items) if items else 0
        pct = (subtotal / total_income * 100) if total_income else 0
        rows_data.append(['', f'SUBTOTAL: {bl}', '', subtotal, f'{pct:.1f}%', ''])
        format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=10))
        row_idx += 1
    
    # Total income
    rows_data.append(['', 'TOTAL INCOME', '', total_income, '100%', ''])
    format_requests.append(bg_format(row_idx, 0, 6, TOTALS_BG_ACTUAL, bold=True, font_size=11))
    row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION B: BUSINESS EXPENSES ===
    rows_data.append(['📊 SECTION B: BUSINESS EXPENSES', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Category', 'Vendor', 'Amount', 'Recurring?', 'Notes', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    for cat in biz_cat_order:
        items = biz_by_cat.get(cat, [])
        if items:
            for item in sorted(items, key=lambda x: x['amount']):
                rows_data.append([cat, item['vendor'], item['amount'], item['recurring'], item['notes'], ''])
                row_idx += 1
            
            subtotal = sum(i['amount'] for i in items)
            rows_data.append([f'SUBTOTAL: {cat}', '', subtotal, '', '', ''])
            format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True))
            row_idx += 1
    
    rows_data.append(['TOTAL BUSINESS EXPENSES', '', total_biz_exp, '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, TOTALS_BG_ACTUAL, bold=True, font_size=11))
    row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION C: PERSONAL EXPENSES ===
    rows_data.append(['👤 SECTION C: PERSONAL EXPENSES', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Category', 'Vendor', 'Amount', 'Recurring?', 'Notes', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    for cat in personal_cat_order:
        items = personal_by_cat.get(cat, [])
        if items:
            for item in sorted(items, key=lambda x: x['amount']):
                rows_data.append([cat, item['vendor'], item['amount'], item['recurring'], item['notes'], ''])
                row_idx += 1
            
            subtotal = sum(i['amount'] for i in items)
            rows_data.append([f'SUBTOTAL: {cat}', '', subtotal, '', '', ''])
            format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True))
            row_idx += 1
        else:
            # Show category even if empty
            rows_data.append([cat, '(none this month)', 0, '', '', ''])
            row_idx += 1
    
    rows_data.append(['TOTAL PERSONAL EXPENSES', '', total_personal_exp, '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, TOTALS_BG_ACTUAL, bold=True, font_size=11))
    row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION D: KEY METRICS ===
    biz_profit = total_income + total_biz_exp  # biz_exp is negative
    profit_margin = (biz_profit / total_income * 100) if total_income else 0
    
    # Meta Ads total
    meta_total = sum(abs(e['amount']) for e in biz_expenses if '📣' in e['category'])
    saas_total = sum(abs(e['amount']) for e in biz_expenses if '📱' in e['category'])
    
    # Revenue per client (unique MVA clients)
    mva_items = income_by_line.get('🚗 MVA Lead Gen', [])
    mva_clients_set = set()
    for item in mva_items:
        if item['source'] not in ('Stripe (MVA clients)',):
            mva_clients_set.add(item['source'])
    num_clients = len(mva_clients_set) if mva_clients_set else 1
    rev_per_client = total_income / num_clients if num_clients else 0
    
    # Status indicators
    margin_status = '🟢' if profit_margin >= 50 else ('🟡' if profit_margin >= 25 else '🔴')
    
    rows_data.append(['📈 SECTION D: KEY METRICS', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Metric', 'Value', 'Target', 'Status', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    metrics = [
        ['Total Revenue', total_income, '', ''],
        ['Total Business Expenses', total_biz_exp, '', ''],
        ['Business Profit (Loss)', biz_profit, '', '🟢' if biz_profit > 0 else '🔴'],
        ['Profit Margin', f'{profit_margin:.1f}%', '50%+', margin_status],
        ['Meta Ad Spend', -meta_total, '', ''],
        ['Ad Spend as % of Revenue', f'{(meta_total/total_income*100):.1f}%' if total_income else 'N/A', '<30%', '🔴' if total_income and meta_total/total_income > 0.3 else '🟢'],
        ['SaaS & Tools Total', -saas_total, '', ''],
        ['Revenue Per Client', rev_per_client, '', ''],
        ['Active MVA Clients', num_clients, '10+', '🟡' if num_clients < 10 else '🟢'],
        ['Total Personal Expenses', total_personal_exp, '', ''],
        ['Burn Rate (Biz + Personal)', total_biz_exp + total_personal_exp, '', ''],
    ]
    
    for m in metrics:
        rows_data.append(m + ['', ''])
        row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION E: MONEY FLOW ===
    rows_data.append(['🔄 SECTION E: MONEY FLOW', '', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Flow', 'From', 'To', 'Amount', 'Notes', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    # Aggregate flows by type
    flow_agg = {}
    for flow in flows:
        key = (flow[0], flow[1], flow[2])
        if key not in flow_agg:
            flow_agg[key] = {'amount': 0, 'notes': flow[4]}
        flow_agg[key]['amount'] += flow[3]
    
    for (flow_name, from_acct, to_acct), data in flow_agg.items():
        rows_data.append([flow_name, from_acct, to_acct, data['amount'], data['notes'], ''])
        row_idx += 1
    
    if not flow_agg:
        rows_data.append(['(No flows detected)', '', '', '', '', ''])
        row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION F: DEBT TRACKING ===
    rows_data.append(['🏦 SECTION F: DEBT TRACKING', '', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Account', 'Balance', 'Limit', 'Utilization', 'Min Payment', 'Actual Payment'])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    # Get closing balances from transaction tabs
    # Last row balance for each CC tab
    biz_cc_rows = all_data.get('💳 Biz CC 0678', [])
    sapphire_rows = all_data.get('💎 Sapphire 4252', [])
    
    # Find the most recent balance (first or last row depending on sort order)
    biz_cc_balance = 0
    if biz_cc_rows:
        # Try last row first
        for r in reversed(biz_cc_rows):
            if r['balance'] != 0:
                biz_cc_balance = abs(r['balance'])
                break
        if biz_cc_balance == 0:
            for r in biz_cc_rows:
                if r['balance'] != 0:
                    biz_cc_balance = abs(r['balance'])
                    break
    
    sapphire_balance = 0
    if sapphire_rows:
        for r in reversed(sapphire_rows):
            if r['balance'] != 0:
                sapphire_balance = abs(r['balance'])
                break
        if sapphire_balance == 0:
            for r in sapphire_rows:
                if r['balance'] != 0:
                    sapphire_balance = abs(r['balance'])
                    break
    
    # Student loan payment
    student_loan_payment = sum(abs(e['amount']) for e in personal_expenses if '🎓' in e['category'])
    
    # CC payments
    biz_cc_payment = sum(abs(f[3]) for key, f_data in flow_agg.items() 
                         for f in [(*key, f_data['amount'], f_data['notes'])] 
                         if 'CC' in key[0])
    
    # Stripe Capital remaining
    stripe_capital_remaining = 4705  # from TOOLS.md
    
    debt_items = [
        ['Student Loans', 'TBD', '—', '—', 'TBD', student_loan_payment if student_loan_payment else 'TBD'],
        ['Sapphire 4252', sapphire_balance, 9300, f'{sapphire_balance/9300*100:.0f}%' if sapphire_balance else '0%', 'TBD', 'TBD'],
        ['Ink CC 0678', biz_cc_balance, 5500, f'{biz_cc_balance/5500*100:.0f}%' if biz_cc_balance else '0%', 'TBD', 'TBD'],
        ['Stripe Capital Loan', stripe_capital_remaining, '—', '—', '20% of deposits', 'Auto-deducted'],
    ]
    
    total_debt = sapphire_balance + biz_cc_balance + stripe_capital_remaining
    
    for item in debt_items:
        rows_data.append(item)
        row_idx += 1
    
    rows_data.append(['TOTAL DEBT', total_debt, '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, TOTALS_BG_ACTUAL, bold=True, font_size=11))
    row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION G: ACCOUNT BALANCES ===
    rows_data.append(['💰 SECTION G: ACCOUNT BALANCES', '', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Account', 'Opening', 'Closing', 'Change', 'Notes', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    # Get opening and closing balances from transaction data
    for tab in ['💼 Business 4991', '👤 Personal 0068']:
        tab_data = all_data.get(tab, [])
        if tab_data:
            # Find first and last non-zero balances
            opening = None
            closing = None
            for r in tab_data:
                if r['balance'] != 0:
                    if opening is None:
                        opening = r['balance']
                    closing = r['balance']
            
            if opening is not None and closing is not None:
                change = closing - opening
                acct_name = tab.replace('💼 ', '').replace('👤 ', '')
                rows_data.append([acct_name, opening, closing, change, '', ''])
                row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION H: ASSETS & NET WORTH ===
    rows_data.append(['💎 SECTION H: ASSETS & NET WORTH', '', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Asset', 'Value', 'Change', 'Notes', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    asset_items = [
        ['Business Equity (Rank & Rent)', 150000, '—', 'Portfolio valuation'],
        ['Robinhood', 'TBD', 'TBD', 'Stocks'],
        ['Acorns', 'TBD', 'TBD', 'Index funds'],
        ['Bitcoin', 'TBD', 'TBD', ''],
        ['Solana', 'TBD', 'TBD', ''],
        ['Cash (all accounts)', 'TBD', '', 'Sum of Section G'],
    ]
    
    for item in asset_items:
        rows_data.append(item + ['', ''])
        row_idx += 1
    
    rows_data.append(['TOTAL ASSETS', 'TBD', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, TOTALS_BG_ACTUAL, bold=True))
    row_idx += 1
    
    rows_data.append(['TOTAL LIABILITIES', -total_debt, '', 'From Section F', '', ''])
    row_idx += 1
    
    rows_data.append(['NET WORTH', 'TBD', 'TBD', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, TOTALS_BG_ACTUAL, bold=True, font_size=11))
    row_idx += 1
    
    # 2 blank rows
    rows_data.append(['']); row_idx += 1
    rows_data.append(['']); row_idx += 1
    
    # === SECTION I: ACTION ITEMS ===
    rows_data.append(['📝 SECTION I: ACTION ITEMS', '', '', '', '', ''])
    format_requests.append(bg_format(row_idx, 0, 6, NAVY, bold=True, font_size=14, font_color=WHITE))
    format_requests.append(merge_cells(row_idx, 0, 6))
    row_idx += 1
    
    rows_data.append(['Priority', 'Action', 'Status', 'Due', 'Notes', ''])
    format_requests.append(bg_format(row_idx, 0, 6, LIGHT_GRAY, bold=True, font_size=11))
    row_idx += 1
    
    action_items = [
        ['🔴 HIGH', 'Reduce Meta Ad spend or improve ROAS', '⬜', '', f'Currently {(meta_total/total_income*100):.0f}% of revenue' if total_income else ''],
        ['🔴 HIGH', 'Cancel unused SaaS subscriptions', '⬜', '', f'SaaS total: ${saas_total:,.2f}'],
        ['🟡 MED', 'Add 3+ MVA clients to diversify revenue', '⬜', '', f'Currently {num_clients} clients'],
        ['🟡 MED', 'Pay down Stripe Capital faster', '⬜', '', f'${stripe_capital_remaining:,.2f} remaining'],
        ['🟡 MED', 'Review Rank & Rent revenue potential', '⬜', '', '$0 this month'],
        ['🟢 LOW', 'Update investment balances (H)', '⬜', '', 'Robinhood, Acorns, crypto'],
        ['🟢 LOW', 'Set up auto-pay on all CCs', '⬜', '', 'Avoid late fees'],
    ]
    
    for item in action_items:
        rows_data.append(item + [''])
        row_idx += 1
    
    print(f"\n📌 Total rows to write: {row_idx}")
    
    # ─── Step 3: WRITE TO SHEET ───
    print("\n📌 Clearing Dashboard tab...")
    sheets_clear(token, "'📊 Dashboard'!A:Z")
    print("✅ Dashboard cleared")
    
    # Unmerge all existing merges first
    print("📌 Unmerging existing cells...")
    try:
        # Get current sheet info to find merges
        info_url = f'https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}?fields=sheets.merges,sheets.properties'
        info_r = requests.get(info_url, headers={'Authorization': f'Bearer {token}'})
        info_r.raise_for_status()
        sheets_info = info_r.json()
        
        unmerge_requests = []
        for sheet in sheets_info.get('sheets', []):
            if sheet.get('properties', {}).get('sheetId') == DASHBOARD_SHEET_ID:
                merges = sheet.get('merges', [])
                for merge in merges:
                    unmerge_requests.append({'unmergeCells': {'range': merge}})
        
        if unmerge_requests:
            sheets_update(token, {'requests': unmerge_requests})
            print(f"  ✅ Unmerged {len(unmerge_requests)} cell ranges")
    except Exception as e:
        print(f"  ⚠️ Unmerge warning: {e}")
    
    # Write all values
    print("📌 Writing dashboard values...")
    sheets_values_update(token, "'📊 Dashboard'!A1", rows_data)
    print(f"✅ Wrote {len(rows_data)} rows")
    
    # Apply formatting
    print("📌 Applying formatting...")
    
    # Add column width requests
    col_widths = [
        {'updateDimensionProperties': {
            'range': {'sheetId': DASHBOARD_SHEET_ID, 'dimension': 'COLUMNS', 'startIndex': 0, 'endIndex': 1},
            'properties': {'pixelSize': 280}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': DASHBOARD_SHEET_ID, 'dimension': 'COLUMNS', 'startIndex': 1, 'endIndex': 2},
            'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': DASHBOARD_SHEET_ID, 'dimension': 'COLUMNS', 'startIndex': 2, 'endIndex': 3},
            'properties': {'pixelSize': 140}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': DASHBOARD_SHEET_ID, 'dimension': 'COLUMNS', 'startIndex': 3, 'endIndex': 4},
            'properties': {'pixelSize': 140}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': DASHBOARD_SHEET_ID, 'dimension': 'COLUMNS', 'startIndex': 4, 'endIndex': 5},
            'properties': {'pixelSize': 120}, 'fields': 'pixelSize'}},
        {'updateDimensionProperties': {
            'range': {'sheetId': DASHBOARD_SHEET_ID, 'dimension': 'COLUMNS', 'startIndex': 5, 'endIndex': 6},
            'properties': {'pixelSize': 250}, 'fields': 'pixelSize'}},
    ]
    
    # Currency formatting for amount columns
    # We need to figure out which rows have amounts in column C (index 2) or D (index 3)
    # For Sections A: amount is col D (index 3)
    # For Sections B, C: amount is col C (index 2)
    # Apply currency format broadly to cols C and D
    currency_fmt = number_format_request(0, row_idx, 2, 5, '$#,##0.00;[Red]($#,##0.00)')
    
    all_requests = col_widths + format_requests + [currency_fmt]
    
    # Freeze first row? Actually the dashboard doesn't have a single header row, so skip
    
    # Batch in chunks of 100 to avoid API limits
    chunk_size = 100
    for i in range(0, len(all_requests), chunk_size):
        chunk = all_requests[i:i+chunk_size]
        sheets_update(token, {'requests': chunk})
        print(f"  ✅ Applied formatting batch {i//chunk_size + 1} ({len(chunk)} requests)")
    
    print("\n" + "=" * 60)
    print("✅ DASHBOARD REBUILD COMPLETE!")
    print("=" * 60)
    
    # ─── GENERATE REPORT ───
    report = f"""# January 2026 Dashboard Rebuild Report

**Generated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
**Sheet:** [January 2026 — KuriosBrand Financial Overview](https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID})

## Summary

### 💰 Section A: Income Summary
| Business Line | Amount | % |
|---------------|--------|---|
| 🚗 MVA Lead Gen | ${sum(i['amount'] for i in income_by_line.get('🚗 MVA Lead Gen', [])):,.2f} | {sum(i['amount'] for i in income_by_line.get('🚗 MVA Lead Gen', []))/total_income*100:.1f}% |
| 🏗️ Rank & Rent | ${sum(i['amount'] for i in income_by_line.get('🏗️ Rank & Rent', [])):,.2f} | {sum(i['amount'] for i in income_by_line.get('🏗️ Rank & Rent', []))/total_income*100 if total_income else 0:.1f}% |
| 🔧 SEO / One-Time | ${sum(i['amount'] for i in income_by_line.get('🔧 SEO / One-Time', [])):,.2f} | {sum(i['amount'] for i in income_by_line.get('🔧 SEO / One-Time', []))/total_income*100 if total_income else 0:.1f}% |
| **TOTAL** | **${total_income:,.2f}** | **100%** |

### 📊 Section B: Business Expenses
| Category | Amount | # Items |
|----------|--------|---------|
"""
    for cat in biz_cat_order:
        items = biz_by_cat.get(cat, [])
        subtotal = sum(i['amount'] for i in items)
        report += f"| {cat} | ${subtotal:,.2f} | {len(items)} |\n"
    report += f"| **TOTAL** | **${total_biz_exp:,.2f}** | **{len(biz_expenses)}** |\n"
    
    report += f"""
### 👤 Section C: Personal Expenses
| Category | Amount | # Items |
|----------|--------|---------|
"""
    for cat in personal_cat_order:
        items = personal_by_cat.get(cat, [])
        subtotal = sum(i['amount'] for i in items)
        report += f"| {cat} | ${subtotal:,.2f} | {len(items)} |\n"
    report += f"| **TOTAL** | **${total_personal_exp:,.2f}** | **{len(personal_expenses)}** |\n"
    
    report += f"""
### 📈 Key Metrics
- **Business Profit:** ${biz_profit:,.2f}
- **Profit Margin:** {profit_margin:.1f}%
- **Meta Ad Spend:** ${meta_total:,.2f} ({meta_total/total_income*100:.1f}% of revenue)
- **SaaS Total:** ${saas_total:,.2f}
- **Active MVA Clients:** {num_clients}
- **Revenue Per Client:** ${rev_per_client:,.2f}

### Verification vs Expected
| Metric | Expected | Actual | Match? |
|--------|----------|--------|--------|
| Total Income | $9,321.79 | ${total_income:,.2f} | {'✅' if abs(total_income - 9321.79) < 1 else '⚠️'} |
| Total Biz Expenses | ~$9,608.71 | ${abs(total_biz_exp):,.2f} | {'✅' if abs(abs(total_biz_exp) - 9608.71) < 100 else '⚠️'} |
| Meta Ads | ~$5,984.18 | ${meta_total:,.2f} | {'✅' if abs(meta_total - 5984.18) < 100 else '⚠️'} |
| SaaS | ~$1,679.30 | ${saas_total:,.2f} | {'✅' if abs(saas_total - 1679.30) < 100 else '⚠️'} |

### Sections Built
- [x] A: Income Summary (grouped by business line)
- [x] B: Business Expenses (6 categories)
- [x] C: Personal Expenses (10 categories)
- [x] D: Key Metrics
- [x] E: Money Flow
- [x] F: Debt Tracking
- [x] G: Account Balances
- [x] H: Assets & Net Worth
- [x] I: Action Items

### Formatting Applied
- Navy section headers (#1B2A4A) with white 14pt bold text
- Gray subtotal rows (#F3F3F3)
- Navy total rows (#E8EDF5)
- Column headers: 11pt bold on gray
- Currency formatting on amount columns
- Column widths set
- 2 blank rows between sections
- Merged cells for section headers

### Income Detail
"""
    for item in income_items:
        report += f"- {item['date']} | {item['source']} via {item['method']} | ${item['amount']:,.2f}\n"
    
    report += f"""
### Notes
- Alexander Shtabsky $500 excluded (personal ATM cash favor, not income)
- Inter-account transfers excluded from expenses
- CC payments excluded from expenses (internal flow)
- Stripe deposits reflect net after fees + 20% Stripe Capital deduction
- TBD values in Sections G, H need manual entry (investment balances, crypto)
"""
    
    # Write report
    report_path = '/home/ec2-user/clawd/data/jan2026-dashboard-rebuild-report.md'
    with open(report_path, 'w') as f:
        f.write(report)
    print(f"\n📄 Report saved to {report_path}")
    
    return report

if __name__ == '__main__':
    try:
        report = main()
        print("\n🎉 Done!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
