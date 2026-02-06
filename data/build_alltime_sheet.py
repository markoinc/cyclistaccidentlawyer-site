#!/usr/bin/env python3
"""
Build the KuriosBrand All Time Financial Overview Google Sheet.
Processes all Chase CSV exports, categorizes transactions, classifies income,
and creates a comprehensive multi-tab Google Sheet.
"""

import csv
import json
import os
import re
import sys
from datetime import datetime
from collections import defaultdict
import urllib.request
import urllib.parse

# ============================================================
# 1. OAuth Token Refresh
# ============================================================

def refresh_token():
    token_path = os.path.expanduser("~/.config/gcal-pro/token.json")
    with open(token_path) as f:
        token_data = json.load(f)
    
    data = urllib.parse.urlencode({
        'client_id': token_data['client_id'],
        'client_secret': token_data['client_secret'],
        'refresh_token': token_data['refresh_token'],
        'grant_type': 'refresh_token'
    }).encode()
    
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data)
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    return result['access_token']

ACCESS_TOKEN = refresh_token()
print(f"✅ OAuth token refreshed")

def sheets_api(method, url, body=None):
    """Make a Google Sheets/Drive API request."""
    req = urllib.request.Request(url, method=method)
    req.add_header('Authorization', f'Bearer {ACCESS_TOKEN}')
    req.add_header('Content-Type', 'application/json')
    if body:
        data = json.dumps(body).encode()
        req.data = data
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"API Error {e.code}: {err_body[:500]}")
        raise

# ============================================================
# 2. Parse CSV Files
# ============================================================

BASE_DIR = "/home/ec2-user/clawd/data/chase-exports"

def parse_checking_csv(filepath):
    """Parse Chase checking account CSV (business-4991, personal-0068)."""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 4:
                continue
            details = row[0].strip()
            date_str = row[1].strip()
            desc = row[2].strip().strip('"')
            try:
                amount = float(row[3].strip())
            except:
                continue
            txn_type = row[4].strip() if len(row) > 4 else ''
            balance = None
            if len(row) > 5 and row[5].strip():
                try:
                    balance = float(row[5].strip())
                except:
                    pass
            try:
                date = datetime.strptime(date_str, '%m/%d/%Y')
            except:
                continue
            txns.append({
                'date': date,
                'description': desc,
                'amount': amount,
                'type': txn_type,
                'balance': balance,
                'details': details,
            })
    return txns

def parse_cc_csv(filepath, has_card_col=False):
    """Parse Chase credit card CSV (bizcc-0678, sapphire-4252)."""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if len(row) < 6:
                continue
            offset = 1 if has_card_col else 0
            date_str = row[0 + offset].strip()
            desc = row[2 + offset].strip()
            category = row[3 + offset].strip()
            txn_type = row[4 + offset].strip()
            try:
                amount = float(row[5 + offset].strip())
            except:
                continue
            try:
                date = datetime.strptime(date_str, '%m/%d/%Y')
            except:
                continue
            txns.append({
                'date': date,
                'description': desc,
                'amount': amount,
                'type': txn_type,
                'category': category,
                'details': 'CREDIT' if amount > 0 else 'DEBIT',
            })
    return txns

print("📂 Parsing CSV files...")
biz_4991 = parse_checking_csv(f"{BASE_DIR}/business-4991-alltime.csv")
personal_0068 = parse_checking_csv(f"{BASE_DIR}/personal-0068-alltime.csv")
bizcc_0678 = parse_cc_csv(f"{BASE_DIR}/bizcc-0678-alltime.csv", has_card_col=True)
sapphire_4252 = parse_cc_csv(f"{BASE_DIR}/sapphire-4252-alltime.csv", has_card_col=False)

print(f"  Business 4991: {len(biz_4991)} transactions")
print(f"  Personal 0068: {len(personal_0068)} transactions")
print(f"  Biz CC 0678: {len(bizcc_0678)} transactions")
print(f"  Sapphire 4252: {len(sapphire_4252)} transactions")

# ============================================================
# 3. Classify Income & Categorize Expenses
# ============================================================

def classify_income(txn, account):
    """Classify income by business line based on rules."""
    desc = txn['description'].upper()
    date = txn['date']
    amount = txn['amount']
    
    if amount <= 0:
        return None, None
    
    # Skip transfers between own accounts
    if 'ONLINE TRANSFER FROM' in desc and ('CHK' in desc or 'SAV' in desc):
        return None, None
    if 'ODP TRANSFER' in desc:
        return None, None
    if 'ACCT_XFER' in txn.get('type', ''):
        return None, None
    
    # Credit Strong is not income
    if 'CREDIT STRONG' in desc:
        return None, None
    
    # Stripe deposits
    if 'STRIPE' in desc:
        source = 'Stripe'
        if date >= datetime(2025, 11, 1):
            return '🚗 MVA Lead Gen', source
        else:
            return '🏗️ Rank & Rent', source
    
    # Zelle income classification
    if 'ZELLE PAYMENT FROM' in desc:
        # Extract sender name
        sender = desc.replace('ZELLE PAYMENT FROM ', '').split(' ')[0:4]
        sender_str = ' '.join(sender).strip()
        
        # Jan 2026+ Zelle clients = MVA
        if date >= datetime(2026, 1, 1):
            if any(name in desc for name in ['A-Z MOBILE', 'ACI ENTERPRISE', 'ANTHONY REDDIN', 
                                              'CHRISTIAN WILLARD', 'JONATHAN BIBLE', 'ALEXANDER SHTABSKY']):
                return '🚗 MVA Lead Gen', extract_zelle_sender(desc)
        
        # Nov 2025+ transition
        if date >= datetime(2025, 11, 1):
            if any(name in desc for name in ['ACI ENTERPRISE', 'ANTHONY REDDIN', 'CHRISTIAN WILLARD',
                                              'JONATHAN BIBLE', 'A-Z MOBILE', 'ALEXANDER SHTABSKY']):
                return '🚗 MVA Lead Gen', extract_zelle_sender(desc)
        
        # Eddy Orozco = SEO
        if 'EDDY OROZCO' in desc:
            return '🔧 SEO / One-Time', 'Eddy Orozco'
        
        # ACI Enterprise, Willard before Nov 2025 = Rank & Rent
        if 'ACI ENTERPRISE' in desc:
            return '🏗️ Rank & Rent', 'ACI Enterprise'
        if 'WILLARD' in desc:
            return '🏗️ Rank & Rent', 'Willard Construction'
        
        # Omar Sanchez = Rank & Rent
        if 'OMAR SANCHEZ' in desc:
            return '🏗️ Rank & Rent', 'Omar Sanchez'
        
        # Jonathan Bible before Nov 2025
        if 'JONATHAN BIBLE' in desc:
            return '🏗️ Rank & Rent', 'Jonathan Bible'
        
        # David Monter = SEO
        if 'DAVID MONTER' in desc:
            return '🔧 SEO / One-Time', 'David Monter'
        
        # Default other Zelle income
        return '🔧 SEO / One-Time', extract_zelle_sender(desc)
    
    return None, None

def extract_zelle_sender(desc):
    """Extract the sender name from a Zelle description."""
    match = re.search(r'ZELLE PAYMENT FROM (.+?)(?:\s+(?:WFCT|BAC|JPM|PNC|BBT|HNA|\d{5,}))', desc, re.I)
    if match:
        name = match.group(1).strip()
        # Title case
        return name.title()
    # Fallback
    parts = desc.upper().replace('ZELLE PAYMENT FROM ', '').split()
    return ' '.join(parts[:3]).title()

def extract_vendor_name(desc):
    """Extract a clean vendor name from description."""
    desc_upper = desc.upper().strip().strip('"')
    
    # Stripe
    if 'STRIPE' in desc_upper:
        return 'Stripe Fees'
    
    # Meta/Facebook
    if any(kw in desc_upper for kw in ['FACEBK', 'FACEBOOK', 'META']):
        return 'Meta Ads'
    
    # Google Ads
    if 'GOOGLE *ADS' in desc_upper or 'GOOGLE ADS' in desc_upper:
        return 'Google Ads'
    
    # Google Workspace
    if 'GOOGLE *WORKSPACE' in desc_upper:
        return 'Google Workspace'
    
    # Google Cloud
    if 'GOOGLE *CLOUD' in desc_upper:
        return 'Google Cloud'
    
    # HighLevel
    if 'HIGHLEVEL' in desc_upper or 'GOHIGHLEVEL' in desc_upper or 'LEADCONNECTOR' in desc_upper:
        return 'HighLevel'
    
    # Others
    vendor_map = {
        'CLOUDFLARE': 'Cloudflare',
        'NAMECHEAP': 'Namecheap', 'NAME-CHEAP': 'Namecheap',
        'CHATGPT': 'OpenAI', 'OPENAI': 'OpenAI',
        'WEBSHARE': 'Webshare',
        'INVIDEO': 'InVideo',
        'LEMLIST': 'Lemlist',
        '10WEB': '10Web',
        'HOSTMYAPPL': 'HostMyApple',
        'SPOTIFY': 'Spotify',
        'BRAVE.COM': 'Brave',
        'CANVA': 'Canva',
        'DUDA': 'Duda',
        'CALLRAIL': 'CallRail',
        'TWILIO': 'Twilio',
        'ZAPIER': 'Zapier',
        'CREDIT STRONG': 'Credit Strong',
        'CHASE CREDIT CRD': 'Chase CC Autopay',
        'WI DFI': 'WI DFI Loan',
        'SEMRUSH': 'Semrush',
        'ROBINHOOD': 'Robinhood',
        'ACORNS': 'Acorns',
        'HULU': 'Hulu',
    }
    for kw, name in vendor_map.items():
        if kw in desc_upper:
            return name
    
    # Zelle
    if 'ZELLE PAYMENT TO' in desc_upper:
        sender = extract_zelle_sender(desc_upper.replace('ZELLE PAYMENT TO', 'ZELLE PAYMENT FROM'))
        return f'Zelle to {sender}'
    
    # Fallback: first meaningful words
    clean = re.sub(r'(DEBIT|CREDIT|POS DEBIT|ORIG CO NAME:|CO ENTRY DESCR:.*)', '', desc_upper).strip()
    words = clean.split()[:3]
    return ' '.join(words).title()[:30] if words else 'Other'

def categorize_biz_expense(txn):
    """Categorize a business expense transaction."""
    desc = txn['description'].upper()
    amount = txn['amount']
    
    if amount >= 0:
        return None  # Not an expense
    
    # Skip transfers between own accounts
    if 'ONLINE TRANSFER TO' in desc and ('CHK' in desc or 'SAV' in desc):
        return '🔄 Transfer'
    if 'ACCT_XFER' in txn.get('type', ''):
        return '🔄 Transfer'
    
    # Zelle outbound payments (to contractors etc.)
    if 'ZELLE PAYMENT TO' in desc:
        return '🏢 Operations'
    
    # Marketing / Ads
    if any(kw in desc for kw in ['META', 'FACEBOOK', 'FACEBK', 'GOOGLE *ADS', 'GOOGLE ADS']):
        return '📣 Marketing / Ads'
    
    # SaaS & Tools
    saas_keywords = ['HIGHLEVEL', 'GOHIGHLEVEL', 'CHATGPT', 'OPENAI', 'NAMECHEAP', 'NAME-CHEAP',
                     'CLOUDFLARE', 'WEBSHARE', 'INVIDEO', 'LEMLIST', '10WEB', 'HOSTMYAPPL',
                     'GOOGLE *WORKSPACE', 'GOOGLE *CLOUD', 'CANVA', 'DUDA', 'ZAPIER', 'TWILIO',
                     'CALENDLY', 'SEMRUSH', 'AHREFS', 'LOOM', 'NOTION', 'SLACK', 'ZOOM',
                     'CALLRAIL', 'PANDADOC', 'BRAVE.COM', 'SPOTIFY', 'DROPBOX', 'GRAMMARLY',
                     'NETLIFY', 'VERCEL', 'GITHUB', 'WORDPRESS', 'ELEMENTOR', 'TYPEFORM',
                     'MAILCHIMP', 'CONVERTKIT', 'MANYCHAT', 'LEADCONNECTOR', 'INSTANTLY',
                     'SNOV', 'HUNTER', 'APOLLO', 'BETTERCONTACT', 'CLOSE.COM', 'HUBSPOT',
                     'SALESFORCE', 'PIPEDRIVE', 'MONDAY', 'CLICKUP', 'ASANA', 'TRELLO',
                     'STRIPE FEE', 'CURSOR', 'ANTHROPIC', 'CLAUDE', 'MIDJOURNEY',
                     'HEROKU', 'DIGITALOCEAN', 'AWS', 'LINODE', 'VULTR', 'RENDER',
                     'GODADDY', 'HOVER', 'GOOGLE *GOOGLE STORAGE', 'SITEGROUND']
    if any(kw in desc for kw in saas_keywords):
        return '📱 SaaS & Tools'
    
    # Debt payments
    if 'CHASE CREDIT CRD' in desc or 'AUTOPAY' in desc:
        return '💳 Debt Payment'
    if 'CREDIT STRONG' in desc:
        return '💳 Debt Payment'
    if 'STUDENT LOAN' in desc or 'DEPT OF ED' in desc or 'GREAT LAKES' in desc or 'NELNET' in desc or 'MOHELA' in desc:
        return '💳 Debt Payment'
    if 'WI DFI' in desc:
        return '💳 Debt Payment'
    
    # Fees
    if any(kw in desc for kw in ['SERVICE CHARGE', 'MONTHLY FEE', 'WIRE FEE', 'OVERDRAFT',
                                   'INSUFFICIENT', 'NSF']):
        return '💰 Fees & Interest'
    
    # ATM
    if 'ATM' in desc:
        return '🏧 ATM / Cash'
    
    # Operations (default for other business expenses)
    return '🏢 Operations'

def categorize_cc_expense(txn, is_business=True):
    """Categorize a credit card expense."""
    desc = txn['description'].upper()
    amount = txn['amount']
    cc_category = txn.get('category', '').upper()
    txn_type = txn.get('type', '').upper()
    
    # Payments are not expenses (they're debt payments from checking)
    if txn_type == 'PAYMENT':
        return '💳 CC Payment'
    
    # Adjustments/Credits
    if txn_type in ('ADJUSTMENT', 'RETURN'):
        if 'STATEMENT CREDIT' in desc:
            return '💰 Fees & Interest'  # cashback/credits offset fees
        return '💰 Fees & Interest'
    
    if amount >= 0:
        return None  # Credits/payments
    
    # Interest charges
    if 'INTEREST CHARGE' in desc:
        return '💰 Fees & Interest'
    
    # Annual fee
    if 'ANNUAL MEMBERSHIP FEE' in desc or 'ANNUAL FEE' in desc:
        return '💰 Fees & Interest'
    
    # Marketing
    if any(kw in desc for kw in ['FACEBK', 'FACEBOOK', 'META', 'GOOGLE *ADS', 'GOOGLE ADS']):
        return '📣 Marketing / Ads'
    
    # SaaS
    saas_kw = ['NAMECHEAP', 'NAME-CHEAP', 'SPOTIFY', 'BRAVE.COM', 'HOSTMYAPPL', 'CLOUDFLARE',
               'CANVA', 'OPENAI', 'CHATGPT', 'SEMRUSH', 'DUDA', 'CALLRAIL',
               'TWILIO', 'ZAPIER', 'MANYCHAT', 'INSTANTLY', 'LEMLIST', 'APOLLO',
               'INVIDEO', '10WEB', 'WEBSHARE', 'LEADCONNECTOR', 'CURSOR']
    if any(kw in desc for kw in saas_kw):
        return '📱 SaaS & Tools'
    
    if is_business:
        # WI DFI = credit building loan payments
        if 'WI DFI' in desc:
            return '💳 Debt Payment'
        return '🏢 Operations'
    else:
        # Personal CC
        if 'AIRBNB' in desc or 'LATAM' in desc or 'AIRLINE' in desc or 'HOTEL' in desc:
            return '✈️ Travel'
        if 'AIRALO' in desc:
            return '✈️ Travel'
        return '🛍️ Shopping & Misc'

def categorize_personal_expense(txn):
    """Categorize a personal checking expense."""
    desc = txn['description'].upper()
    amount = txn['amount']
    
    if amount >= 0:
        return None
    
    # Skip transfers to own accounts
    if 'ONLINE TRANSFER TO' in desc and ('SAV' in desc or 'CHK' in desc):
        return '🔄 Transfer'
    if 'ACCT_XFER' in txn.get('type', ''):
        return '🔄 Transfer'
    
    # Investments
    if 'ROBINHOOD' in desc:
        return '📈 Investment'
    if 'ACORNS' in desc:
        return '📈 Investment'
    
    # ATM
    if 'ATM' in desc:
        return '🏧 ATM / Cash'
    
    # FX Fees
    if 'FOREIGN EXCHANGE' in desc or 'FX' in desc:
        return '🏧 ATM / Cash'
    if 'NON-CHASE ATM FEE' in desc:
        return '🏧 ATM / Cash'
    
    # Subscriptions
    subs = ['HULU', 'NETFLIX', 'DISNEY', 'AMAZON PRIME', 'YOUTUBE PREMIUM', 'SPOTIFY',
            'APPLE.COM/BILL', 'ICLOUD', 'GOOGLE ONE']
    if any(kw in desc for kw in subs):
        return '📺 Subscription'
    
    # Food
    food_kw = ['UBER EATS', 'DOORDASH', 'GRUBHUB', 'MCDONALD', 'STARBUCKS', 'CHIPOTLE',
               'SUBWAY', 'WENDY', 'BURGER', 'PIZZA', 'TACO', 'RESTAURANT', 'DINE', 'CAFE',
               'COFFEE', 'BAKERY', 'SUSHI', 'THAI', 'PANERA']
    if any(kw in desc for kw in food_kw):
        return '🍔 Food & Dining'
    
    # Travel
    if any(kw in desc for kw in ['AIRBNB', 'AIRLINE', 'LATAM', 'HOTEL', 'BOOKING.COM',
                                   'EXPEDIA', 'KAYAK', 'AIRALO']):
        return '✈️ Travel'
    
    # Shopping
    if any(kw in desc for kw in ['AMAZON', 'WALMART', 'TARGET', 'APPLE.COM', 'BEST BUY']):
        return '🛍️ Shopping & Misc'
    
    # Default to living/local
    return '🏠 Living / Local'

# ============================================================
# 4. Process All Transactions
# ============================================================

print("\n🔄 Processing transactions...")

# Monthly data structures
monthly_revenue = defaultdict(float)  # (year, month) -> total revenue
monthly_expenses = defaultdict(float)  # (year, month) -> total expenses
monthly_biz_line = defaultdict(lambda: defaultdict(float))  # (year, month) -> {line: amount}
monthly_expense_cat = defaultdict(lambda: defaultdict(float))  # (year, month) -> {cat: amount}
monthly_income_by_client = defaultdict(lambda: defaultdict(float))  # (year, month) -> {client: amount}
monthly_income_client_line = {}  # client -> business_line
monthly_income_client_method = {}  # client -> method

# Top vendors tracking
vendor_spending = defaultdict(float)  # vendor -> total spent
vendor_category = {}  # vendor -> category

# Process Business 4991 - Income and Expenses
for txn in biz_4991:
    ym = (txn['date'].year, txn['date'].month)
    
    if txn['amount'] > 0:
        biz_line, source = classify_income(txn, 'business')
        if biz_line and source:
            monthly_revenue[ym] += txn['amount']
            monthly_biz_line[ym][biz_line] += txn['amount']
            monthly_income_by_client[ym][source] += txn['amount']
            monthly_income_client_line[source] = biz_line
            method = 'Stripe' if 'STRIPE' in txn['description'].upper() else 'Zelle'
            monthly_income_client_method[source] = method
    else:
        cat = categorize_biz_expense(txn)
        if cat and cat != '🔄 Transfer':
            monthly_expenses[ym] += abs(txn['amount'])
            monthly_expense_cat[ym][cat] += abs(txn['amount'])
            # Track vendor
            vendor_name = extract_vendor_name(txn['description'])
            vendor_spending[vendor_name] += abs(txn['amount'])
            vendor_category[vendor_name] = cat

# Process Biz CC 0678 - Expenses
for txn in bizcc_0678:
    ym = (txn['date'].year, txn['date'].month)
    cat = categorize_cc_expense(txn, is_business=True)
    
    if cat and cat != '💳 CC Payment' and txn['amount'] < 0:
        monthly_expenses[ym] += abs(txn['amount'])
        monthly_expense_cat[ym][cat] += abs(txn['amount'])
        vendor_name = extract_vendor_name(txn['description'])
        vendor_spending[vendor_name] += abs(txn['amount'])
        vendor_category[vendor_name] = cat
    elif cat == '💰 Fees & Interest' and txn['amount'] > 0:
        # Statement credits offset expenses
        pass

# Process Sapphire 4252 - Personal expenses (but ads are business)
for txn in sapphire_4252:
    ym = (txn['date'].year, txn['date'].month)
    desc_upper = txn['description'].upper()
    
    # Facebook/Meta ads on Sapphire are business expenses
    if any(kw in desc_upper for kw in ['FACEBK', 'FACEBOOK', 'META']) and txn['amount'] < 0:
        monthly_expenses[ym] += abs(txn['amount'])
        monthly_expense_cat[ym]['📣 Marketing / Ads'] += abs(txn['amount'])
        vendor_spending['Meta Ads (Sapphire)'] += abs(txn['amount'])
        vendor_category['Meta Ads (Sapphire)'] = '📣 Marketing / Ads'
        continue
    
    # Google Ads on Sapphire
    if ('GOOGLE *ADS' in desc_upper or 'GOOGLE ADS' in desc_upper):
        if txn['amount'] < 0:
            monthly_expenses[ym] += abs(txn['amount'])
            monthly_expense_cat[ym]['📣 Marketing / Ads'] += abs(txn['amount'])
            vendor_spending['Google Ads (Sapphire)'] += abs(txn['amount'])
            vendor_category['Google Ads (Sapphire)'] = '📣 Marketing / Ads'
        continue
    
    # Interest and fees on CC are business costs
    if 'INTEREST CHARGE' in desc_upper and txn['amount'] < 0:
        monthly_expenses[ym] += abs(txn['amount'])
        monthly_expense_cat[ym]['💰 Fees & Interest'] += abs(txn['amount'])
        vendor_spending['Sapphire Interest'] += abs(txn['amount'])
        vendor_category['Sapphire Interest'] = '💰 Fees & Interest'
        continue
    
    if 'ANNUAL MEMBERSHIP FEE' in desc_upper and txn['amount'] < 0:
        monthly_expenses[ym] += abs(txn['amount'])
        monthly_expense_cat[ym]['💰 Fees & Interest'] += abs(txn['amount'])
        vendor_spending['Sapphire Annual Fee'] += abs(txn['amount'])
        vendor_category['Sapphire Annual Fee'] = '💰 Fees & Interest'
        continue

# Note: Personal 0068 expenses are personal, not business - we track separately for context
personal_monthly_spending = defaultdict(float)
for txn in personal_0068:
    ym = (txn['date'].year, txn['date'].month)
    if txn['amount'] < 0:
        cat = categorize_personal_expense(txn)
        if cat and cat != '🔄 Transfer':
            personal_monthly_spending[ym] += abs(txn['amount'])

# ============================================================
# 5. Build Monthly Summary Data
# ============================================================

# Get all months with data
all_months = sorted(set(list(monthly_revenue.keys()) + list(monthly_expenses.keys())))

# Use verified monthly data where available
verified_data = {
    (2025, 6): {'revenue': 9023, 'expenses': 4253, 'profit': 4769, 'margin': 0.52},
    (2025, 7): {'revenue': 12688, 'expenses': 3851, 'profit': 5737, 'margin': 0.45},
    (2025, 8): {'revenue': 7848, 'expenses': 2660, 'profit': 5188, 'margin': 0.66},
    (2025, 9): {'revenue': 6510, 'expenses': 1962, 'profit': 4547, 'margin': 0.70},
    (2025, 11): {'revenue': 5071, 'expenses': 2035, 'profit': 3036, 'margin': 0.60},
    (2025, 12): {'revenue': 6326, 'expenses': 3611, 'profit': 2715, 'margin': 0.43},
    (2026, 1): {'revenue': 9322, 'expenses': 9609, 'profit': -287, 'margin': -0.03},
}

print("\n📊 Monthly Summary:")
print(f"{'Month':<12} {'Revenue':>10} {'Expenses':>10} {'Profit':>10} {'Margin':>8}")
print("-" * 55)

monthly_summary = {}
for ym in sorted(all_months):
    year, month = ym
    if ym in verified_data:
        d = verified_data[ym]
        monthly_summary[ym] = d
    else:
        rev = monthly_revenue.get(ym, 0)
        exp = monthly_expenses.get(ym, 0)
        profit = rev - exp
        margin = profit / rev if rev > 0 else 0
        monthly_summary[ym] = {'revenue': round(rev, 2), 'expenses': round(exp, 2), 
                                'profit': round(profit, 2), 'margin': round(margin, 2)}
    
    d = monthly_summary[ym]
    month_name = datetime(year, month, 1).strftime('%b %Y')
    if d['revenue'] > 0 or d['expenses'] > 0:
        print(f"{month_name:<12} ${d['revenue']:>9,.0f} ${d['expenses']:>9,.0f} ${d['profit']:>9,.0f} {d['margin']:>7.0%}")

# ============================================================
# 6. Create Google Sheet
# ============================================================

print("\n📝 Creating Google Sheet...")

FOLDER_ID = "1XlNibgutZc0eVrI6tkgexTA3RusGepwX"

# Create spreadsheet
create_body = {
    "properties": {
        "title": "📊 KuriosBrand — All Time Financial Overview"
    },
    "sheets": [
        {
            "properties": {
                "title": "🌐 All Time Dashboard",
                "sheetId": 0,
                "tabColorStyle": {"rgbColor": {"red": 0.984, "green": 0.737, "blue": 0.016}}  # Gold #FBBC04
            }
        },
        {
            "properties": {
                "title": "📅 2025",
                "sheetId": 1,
                "tabColorStyle": {"rgbColor": {"red": 0.106, "green": 0.165, "blue": 0.290}}  # Navy #1B2A4A
            }
        },
        {
            "properties": {
                "title": "📅 2026",
                "sheetId": 2,
                "tabColorStyle": {"rgbColor": {"red": 0.106, "green": 0.165, "blue": 0.290}}
            }
        },
        {
            "properties": {
                "title": "📅 2024",
                "sheetId": 3,
                "tabColorStyle": {"rgbColor": {"red": 0.106, "green": 0.165, "blue": 0.290}}
            }
        }
    ]
}

result = sheets_api('POST', 'https://sheets.googleapis.com/v4/spreadsheets', create_body)
SPREADSHEET_ID = result['spreadsheetId']
print(f"✅ Created sheet: {SPREADSHEET_ID}")

# Move to folder
move_url = f"https://www.googleapis.com/drive/v3/files/{SPREADSHEET_ID}?addParents={FOLDER_ID}&fields=id,parents"
sheets_api('PATCH', move_url)
print(f"✅ Moved to folder: {FOLDER_ID}")

# ============================================================
# 7. Helper Functions for Building Sheet Content
# ============================================================

def navy_header(text, cols=8):
    """Section header row with navy background."""
    return {
        'values': [text] + [''] * (cols - 1),
        'formats': [{
            'backgroundColor': {'red': 0.106, 'green': 0.165, 'blue': 0.290},
            'textFormat': {'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}, 
                          'bold': True, 'fontSize': 14},
            'horizontalAlignment': 'LEFT'
        }] * cols,
        'merge': (0, cols)
    }

def col_header(values):
    """Column header row."""
    return {
        'values': values,
        'formats': [{
            'backgroundColor': {'red': 0.953, 'green': 0.953, 'blue': 0.953},
            'textFormat': {'bold': True, 'fontSize': 11},
            'horizontalAlignment': 'CENTER'
        }] * len(values)
    }

def data_row(values, bold=False, bg=None):
    """Data row."""
    fmt = {}
    if bold:
        fmt['textFormat'] = {'bold': True}
    if bg == 'subtotal':
        fmt['backgroundColor'] = {'red': 0.953, 'green': 0.953, 'blue': 0.953}
    elif bg == 'total':
        fmt['backgroundColor'] = {'red': 0.910, 'green': 0.929, 'blue': 0.949}
    return {'values': values, 'formats': [fmt] * len(values)}

def empty_row(cols=8):
    return {'values': [''] * cols, 'formats': [{}] * cols}

def fmt_currency(val):
    """Format a number as currency string."""
    if val is None or val == '':
        return ''
    if isinstance(val, str):
        return val
    if val < 0:
        return f"-${abs(val):,.2f}"
    return f"${val:,.2f}"

def fmt_pct(val):
    """Format as percentage."""
    if val is None or val == '':
        return ''
    if isinstance(val, str):
        return val
    return f"{val:.0%}"

# ============================================================
# 8. Build All Time Dashboard Data
# ============================================================

print("\n🏗️ Building All Time Dashboard...")

# Calculate yearly aggregates
yearly_data = defaultdict(lambda: {'revenue': 0, 'expenses': 0, 'profit': 0})
for ym, data in monthly_summary.items():
    year = ym[0]
    if data['revenue'] > 0 or data['expenses'] > 0:
        yearly_data[year]['revenue'] += data['revenue']
        yearly_data[year]['expenses'] += data['expenses']
        yearly_data[year]['profit'] += data['profit']

for year in yearly_data:
    if yearly_data[year]['revenue'] > 0:
        yearly_data[year]['margin'] = yearly_data[year]['profit'] / yearly_data[year]['revenue']
    else:
        yearly_data[year]['margin'] = 0

# All-time totals
alltime_revenue = sum(d['revenue'] for d in yearly_data.values())
alltime_expenses = sum(d['expenses'] for d in yearly_data.values())
alltime_profit = alltime_revenue - alltime_expenses
alltime_margin = alltime_profit / alltime_revenue if alltime_revenue > 0 else 0

# Best/worst months
best_month = max(((ym, d) for ym, d in monthly_summary.items() if d['revenue'] > 0), 
                  key=lambda x: x[1]['revenue'], default=None)
worst_month = min(((ym, d) for ym, d in monthly_summary.items() if d['revenue'] > 0),
                   key=lambda x: x[1]['revenue'], default=None)

# Revenue by business line per year
yearly_biz_line = defaultdict(lambda: defaultdict(float))
for ym, lines in monthly_biz_line.items():
    year = ym[0]
    for line, amount in lines.items():
        yearly_biz_line[year][line] += amount

# Expense categories per year
yearly_expense_cat = defaultdict(lambda: defaultdict(float))
for ym, cats in monthly_expense_cat.items():
    year = ym[0]
    for cat, amount in cats.items():
        yearly_expense_cat[year][cat] += amount

# Now build the actual cell data for each tab
# We'll use the batchUpdate API with cell data

def build_alltime_rows():
    """Build all rows for the All Time Dashboard tab."""
    rows = []
    
    # Section 1: Executive Summary
    rows.append(navy_header('💰 EXECUTIVE SUMMARY', 6))
    rows.append(col_header(['Metric', '2024', '2025', '2026 YTD', 'All Time', '']))
    
    y24 = yearly_data.get(2024, {'revenue': 0, 'expenses': 0, 'profit': 0, 'margin': 0})
    y25 = yearly_data.get(2025, {'revenue': 0, 'expenses': 0, 'profit': 0, 'margin': 0})
    y26 = yearly_data.get(2026, {'revenue': 0, 'expenses': 0, 'profit': 0, 'margin': 0})
    
    rows.append(data_row(['Total Revenue', fmt_currency(y24['revenue']), fmt_currency(y25['revenue']),
                           fmt_currency(y26['revenue']), fmt_currency(alltime_revenue), '']))
    rows.append(data_row(['Total Expenses', fmt_currency(y24['expenses']), fmt_currency(y25['expenses']),
                           fmt_currency(y26['expenses']), fmt_currency(alltime_expenses), '']))
    rows.append(data_row(['Net Profit', fmt_currency(y24['profit']), fmt_currency(y25['profit']),
                           fmt_currency(y26['profit']), fmt_currency(alltime_profit), ''], bold=True, bg='total'))
    rows.append(data_row(['Profit Margin', fmt_pct(y24.get('margin', 0)), fmt_pct(y25.get('margin', 0)),
                           fmt_pct(y26.get('margin', 0)), fmt_pct(alltime_margin), '']))
    
    if best_month:
        bm_name = datetime(best_month[0][0], best_month[0][1], 1).strftime('%b %Y')
        rows.append(data_row(['Best Month', '', '', '', f"{bm_name} ({fmt_currency(best_month[1]['revenue'])})", '']))
    if worst_month:
        wm_name = datetime(worst_month[0][0], worst_month[0][1], 1).strftime('%b %Y')
        rows.append(data_row(['Worst Month', '', '', '', f"{wm_name} ({fmt_currency(worst_month[1]['revenue'])})", '']))
    
    rows.append(empty_row(6))
    rows.append(empty_row(6))
    
    # Section 2: Revenue by Business Line
    rows.append(navy_header('📊 REVENUE BY BUSINESS LINE', 6))
    rows.append(col_header(['Business Line', '2024', '2025', '2026 YTD', 'All Time', '% of Total']))
    
    lines = ['🚗 MVA Lead Gen', '🏗️ Rank & Rent', '🔧 SEO / One-Time']
    for line in lines:
        v24 = yearly_biz_line[2024].get(line, 0)
        v25 = yearly_biz_line[2025].get(line, 0)
        v26 = yearly_biz_line[2026].get(line, 0)
        total = v24 + v25 + v26
        pct = total / alltime_revenue if alltime_revenue > 0 else 0
        rows.append(data_row([line, fmt_currency(v24), fmt_currency(v25), fmt_currency(v26),
                               fmt_currency(total), fmt_pct(pct)]))
    
    rows.append(data_row(['TOTAL', fmt_currency(y24['revenue']), fmt_currency(y25['revenue']),
                           fmt_currency(y26['revenue']), fmt_currency(alltime_revenue), '100%'], bold=True, bg='total'))
    
    rows.append(empty_row(6))
    rows.append(empty_row(6))
    
    # Section 3: Monthly Revenue Trend
    rows.append(navy_header('📈 MONTHLY REVENUE TREND', 6))
    rows.append(col_header(['Month', 'Revenue', 'Expenses', 'Profit', 'Margin', 'Primary Line']))
    
    for ym in sorted(monthly_summary.keys()):
        d = monthly_summary[ym]
        if d['revenue'] <= 0 and d['expenses'] <= 0:
            continue
        month_name = datetime(ym[0], ym[1], 1).strftime('%b %Y')
        
        # Determine primary business line
        lines_for_month = monthly_biz_line.get(ym, {})
        if lines_for_month:
            primary = max(lines_for_month.items(), key=lambda x: x[1])[0]
        else:
            primary = '—'
        
        rows.append(data_row([month_name, fmt_currency(d['revenue']), fmt_currency(d['expenses']),
                               fmt_currency(d['profit']), fmt_pct(d['margin']), primary]))
    
    # Totals row
    rows.append(data_row(['TOTAL', fmt_currency(alltime_revenue), fmt_currency(alltime_expenses),
                           fmt_currency(alltime_profit), fmt_pct(alltime_margin), ''], bold=True, bg='total'))
    
    rows.append(empty_row(6))
    rows.append(empty_row(6))
    
    # Section 4: Expense Categories
    rows.append(navy_header('💸 EXPENSE CATEGORIES (ALL TIME)', 6))
    rows.append(col_header(['Category', '2024', '2025', '2026 YTD', 'All Time', '% of Expenses']))
    
    all_cats = sorted(set(
        list(yearly_expense_cat[2024].keys()) + 
        list(yearly_expense_cat[2025].keys()) + 
        list(yearly_expense_cat[2026].keys())
    ))
    
    # Sort by all-time amount descending
    cat_totals = {}
    for cat in all_cats:
        if cat in ('🔄 Transfer', '💳 CC Payment'):
            continue
        cat_totals[cat] = sum(yearly_expense_cat[y].get(cat, 0) for y in [2024, 2025, 2026])
    
    for cat in sorted(cat_totals.keys(), key=lambda c: cat_totals[c], reverse=True):
        v24 = yearly_expense_cat[2024].get(cat, 0)
        v25 = yearly_expense_cat[2025].get(cat, 0)
        v26 = yearly_expense_cat[2026].get(cat, 0)
        total = cat_totals[cat]
        pct = total / alltime_expenses if alltime_expenses > 0 else 0
        rows.append(data_row([cat, fmt_currency(v24), fmt_currency(v25), fmt_currency(v26),
                               fmt_currency(total), fmt_pct(pct)]))
    
    rows.append(data_row(['TOTAL', fmt_currency(y24['expenses']), fmt_currency(y25['expenses']),
                           fmt_currency(y26['expenses']), fmt_currency(alltime_expenses), '100%'], bold=True, bg='total'))
    
    rows.append(empty_row(6))
    rows.append(empty_row(6))
    
    # Section 5: Key Ratios & Health Metrics
    rows.append(navy_header('🏥 KEY RATIOS & HEALTH METRICS', 6))
    rows.append(col_header(['Metric', 'Target', 'Current', 'Trend', '', '']))
    
    avg_monthly_rev = alltime_revenue / max(len([ym for ym in monthly_summary if monthly_summary[ym]['revenue'] > 0]), 1)
    avg_monthly_exp = alltime_expenses / max(len([ym for ym in monthly_summary if monthly_summary[ym]['expenses'] > 0]), 1)
    num_clients = len(set(monthly_income_client_line.keys()))
    rev_per_client = alltime_revenue / num_clients if num_clients > 0 else 0
    
    metrics = [
        ['Profit Margin', '>50%', fmt_pct(alltime_margin), '📈' if alltime_margin > 0.5 else '📉'],
        ['Avg Monthly Revenue', '—', fmt_currency(avg_monthly_rev), ''],
        ['Avg Monthly Expenses', '—', fmt_currency(avg_monthly_exp), ''],
        ['Monthly Burn Rate', '—', fmt_currency(avg_monthly_exp), ''],
        ['Active Clients (All Time)', '—', str(num_clients), ''],
        ['Revenue Per Client', '—', fmt_currency(rev_per_client), ''],
        ['Months Tracked', '—', str(len([ym for ym in monthly_summary if monthly_summary[ym]['revenue'] > 0])), ''],
    ]
    
    for m in metrics:
        rows.append(data_row(m + ['', '']))
    
    rows.append(empty_row(6))
    rows.append(empty_row(6))
    
    # Section 6: Business Pivot Timeline
    rows.append(navy_header('🔄 BUSINESS PIVOT TIMELINE', 6))
    rows.append(col_header(['Date', 'Event', 'Impact', '', '', '']))
    
    timeline = [
        ['Feb 2024', 'First Stripe deposit recorded', 'Rank & Rent business begins'],
        ['Jun 2024', 'Steady Stripe income established', 'Monthly Stripe deposits ~$2-3k'],
        ['Oct 2024', 'Willard Construction large payments', 'Rank & Rent scaling ($9k Zelle)'],
        ['Jun 2025', 'First fully tracked month', 'Revenue: $9,023 | Profit: $4,769'],
        ['Jul 2025', 'Best revenue month ($12,688)', 'Peak Rank & Rent + SEO period'],
        ['Sep 2025', 'Best margin month (70%)', 'Low expenses, steady income'],
        ['Nov 2025', 'MVA Lead Gen business begins', 'Business pivot starts'],
        ['Dec 2025', 'Transition month R&R → MVA', 'Mix of both business lines'],
        ['Jan 2026', 'First unprofitable month (-$287)', 'Heavy Meta Ads scaling for MVA'],
        ['Jan 2026', 'Stripe Capital loan ($4,200)', 'Growth capital for MVA expansion'],
    ]
    
    for t in timeline:
        rows.append(data_row(t + ['', '', '']))
    
    return rows

def build_year_rows(year, months_range=None):
    """Build rows for a year dashboard tab."""
    rows = []
    
    if months_range is None:
        months_range = range(1, 13)
    
    # Filter to months with data
    year_months = [(year, m) for m in months_range if (year, m) in monthly_summary and 
                   (monthly_summary[(year, m)]['revenue'] > 0 or monthly_summary[(year, m)]['expenses'] > 0)]
    
    if not year_months:
        # Check if we have any transaction data at all for this year
        year_months_with_any = [(year, m) for m in months_range 
                                if any(t['date'].year == year and t['date'].month == m 
                                       for t in biz_4991 + bizcc_0678 + sapphire_4252)]
        if year_months_with_any:
            year_months = year_months_with_any
    
    yd = yearly_data.get(year, {'revenue': 0, 'expenses': 0, 'profit': 0, 'margin': 0})
    
    # Section 1: Annual Summary
    rows.append(navy_header(f'💰 {year} ANNUAL SUMMARY', 8))
    rows.append(col_header(['Metric', 'Value', '', '', '', '', '', '']))
    
    num_months = len(year_months)
    avg_rev = yd['revenue'] / num_months if num_months > 0 else 0
    avg_profit = yd['profit'] / num_months if num_months > 0 else 0
    
    summary_metrics = [
        ['Total Revenue', fmt_currency(yd['revenue'])],
        ['Total Business Expenses', fmt_currency(yd['expenses'])],
        ['Net Business Profit', fmt_currency(yd['profit'])],
        ['Profit Margin', fmt_pct(yd.get('margin', 0))],
        ['Months Tracked', str(num_months)],
        ['Avg Monthly Revenue', fmt_currency(avg_rev)],
        ['Avg Monthly Profit', fmt_currency(avg_profit)],
    ]
    
    for m in summary_metrics:
        rows.append(data_row(m + [''] * 6))
    
    rows.append(empty_row(8))
    rows.append(empty_row(8))
    
    # Section 2: Monthly Breakdown
    rows.append(navy_header(f'📅 {year} MONTHLY BREAKDOWN', 8))
    rows.append(col_header(['Month', 'Revenue', 'Expenses', 'Profit', 'Margin', '🚗 MVA', '🏗️ R&R', '🔧 SEO']))
    
    for m in months_range:
        ym = (year, m)
        d = monthly_summary.get(ym, {'revenue': 0, 'expenses': 0, 'profit': 0, 'margin': 0})
        if d['revenue'] <= 0 and d['expenses'] <= 0:
            continue
        month_name = datetime(year, m, 1).strftime('%b')
        lines = monthly_biz_line.get(ym, {})
        mva = lines.get('🚗 MVA Lead Gen', 0)
        rr = lines.get('🏗️ Rank & Rent', 0)
        seo = lines.get('🔧 SEO / One-Time', 0)
        rows.append(data_row([month_name, fmt_currency(d['revenue']), fmt_currency(d['expenses']),
                               fmt_currency(d['profit']), fmt_pct(d['margin']),
                               fmt_currency(mva) if mva > 0 else '—',
                               fmt_currency(rr) if rr > 0 else '—',
                               fmt_currency(seo) if seo > 0 else '—']))
    
    # Year total
    mva_total = sum(monthly_biz_line.get((year, m), {}).get('🚗 MVA Lead Gen', 0) for m in months_range)
    rr_total = sum(monthly_biz_line.get((year, m), {}).get('🏗️ Rank & Rent', 0) for m in months_range)
    seo_total = sum(monthly_biz_line.get((year, m), {}).get('🔧 SEO / One-Time', 0) for m in months_range)
    
    rows.append(data_row(['TOTAL', fmt_currency(yd['revenue']), fmt_currency(yd['expenses']),
                           fmt_currency(yd['profit']), fmt_pct(yd.get('margin', 0)),
                           fmt_currency(mva_total) if mva_total > 0 else '—',
                           fmt_currency(rr_total) if rr_total > 0 else '—',
                           fmt_currency(seo_total) if seo_total > 0 else '—'], bold=True, bg='total'))
    
    rows.append(empty_row(8))
    rows.append(empty_row(8))
    
    # Section 3: Expense Categories
    rows.append(navy_header(f'💸 {year} EXPENSE CATEGORIES', 8))
    
    # Get months with data for column headers
    active_months = [m for m in months_range if (year, m) in monthly_expense_cat and monthly_expense_cat[(year, m)]]
    
    if len(active_months) <= 6:
        # Show per-month
        month_labels = [datetime(year, m, 1).strftime('%b') for m in active_months]
        rows.append(col_header(['Category'] + month_labels + ['Total', '% of Exp'] + [''] * (8 - len(month_labels) - 3)))
        
        cats_for_year = set()
        for m in active_months:
            cats_for_year.update(monthly_expense_cat.get((year, m), {}).keys())
        cats_for_year = {c for c in cats_for_year if c not in ('🔄 Transfer', '💳 CC Payment')}
        
        cat_yearly_totals = {c: sum(monthly_expense_cat.get((year, m), {}).get(c, 0) for m in active_months) for c in cats_for_year}
        
        for cat in sorted(cats_for_year, key=lambda c: cat_yearly_totals[c], reverse=True):
            vals = [fmt_currency(monthly_expense_cat.get((year, m), {}).get(cat, 0)) 
                    if monthly_expense_cat.get((year, m), {}).get(cat, 0) > 0 else '—' 
                    for m in active_months]
            total = cat_yearly_totals[cat]
            pct = total / yd['expenses'] if yd['expenses'] > 0 else 0
            padding = [''] * (8 - len(vals) - 3)
            rows.append(data_row([cat] + vals + [fmt_currency(total), fmt_pct(pct)] + padding))
    else:
        rows.append(col_header(['Category', 'Total', '% of Expenses', '', '', '', '', '']))
        cats_for_year = yearly_expense_cat.get(year, {})
        cats_filtered = {k: v for k, v in cats_for_year.items() if k not in ('🔄 Transfer', '💳 CC Payment')}
        for cat in sorted(cats_filtered.keys(), key=lambda c: cats_filtered[c], reverse=True):
            total = cats_filtered[cat]
            pct = total / yd['expenses'] if yd['expenses'] > 0 else 0
            rows.append(data_row([cat, fmt_currency(total), fmt_pct(pct), '', '', '', '', '']))
    
    rows.append(empty_row(8))
    rows.append(empty_row(8))
    
    # Section 4: Top Vendors
    rows.append(navy_header(f'🏪 {year} TOP VENDORS', 8))
    rows.append(col_header(['Rank', 'Vendor', 'Category', 'Total Spent', '% of Expenses', '', '', '']))
    
    # Calculate per-year vendor spending
    year_vendor_spending = defaultdict(float)
    year_vendor_cat = {}
    
    for txn in biz_4991:
        if txn['date'].year == year and txn['amount'] < 0:
            cat = categorize_biz_expense(txn)
            if cat and cat != '🔄 Transfer':
                name = extract_vendor_name(txn['description'])
                year_vendor_spending[name] += abs(txn['amount'])
                year_vendor_cat[name] = cat
    
    for txn in bizcc_0678:
        if txn['date'].year == year and txn['amount'] < 0:
            cat = categorize_cc_expense(txn, is_business=True)
            if cat and cat != '💳 CC Payment':
                name = extract_vendor_name(txn['description'])
                year_vendor_spending[name] += abs(txn['amount'])
                year_vendor_cat[name] = cat
    
    for txn in sapphire_4252:
        if txn['date'].year == year and txn['amount'] < 0:
            desc_upper = txn['description'].upper()
            if any(kw in desc_upper for kw in ['FACEBK', 'FACEBOOK', 'META', 'GOOGLE *ADS']):
                name = extract_vendor_name(txn['description'])
                year_vendor_spending[name] += abs(txn['amount'])
                year_vendor_cat[name] = '📣 Marketing / Ads'
            elif 'INTEREST' in desc_upper or 'ANNUAL' in desc_upper:
                name = extract_vendor_name(txn['description'])
                year_vendor_spending[name] += abs(txn['amount'])
                year_vendor_cat[name] = '💰 Fees & Interest'
    
    sorted_vendors = sorted(year_vendor_spending.items(), key=lambda x: x[1], reverse=True)[:15]
    for i, (vendor, total) in enumerate(sorted_vendors, 1):
        pct = total / yd['expenses'] if yd['expenses'] > 0 else 0
        rows.append(data_row([str(i), vendor, year_vendor_cat.get(vendor, ''), 
                               fmt_currency(total), fmt_pct(pct), '', '', '']))
    
    rows.append(empty_row(8))
    rows.append(empty_row(8))
    
    # Section 5: Income by Client
    rows.append(navy_header(f'👥 {year} INCOME BY CLIENT', 8))
    rows.append(col_header(['Client', 'Business Line', 'Method', 'Total', '% of Revenue', '', '', '']))
    
    year_client_totals = defaultdict(float)
    for m in months_range:
        ym = (year, m)
        for client, amount in monthly_income_by_client.get(ym, {}).items():
            year_client_totals[client] += amount
    
    sorted_clients = sorted(year_client_totals.items(), key=lambda x: x[1], reverse=True)
    for client, total in sorted_clients:
        pct = total / yd['revenue'] if yd['revenue'] > 0 else 0
        line = monthly_income_client_line.get(client, '🔧 SEO / One-Time')
        method = monthly_income_client_method.get(client, 'Zelle')
        rows.append(data_row([client, line, method, fmt_currency(total), fmt_pct(pct), '', '', '']))
    
    rows.append(data_row(['TOTAL', '', '', fmt_currency(yd['revenue']), '100%', '', '', ''], bold=True, bg='total'))
    
    rows.append(empty_row(8))
    rows.append(empty_row(8))
    
    # Section 6: Tax Summary
    rows.append(navy_header(f'🧾 {year} TAX SUMMARY', 8))
    rows.append(col_header(['Metric', 'Value', '', '', '', '', '', '']))
    
    taxable = yd['profit']
    tax_15 = yd['revenue'] * 0.15
    
    tax_rows = [
        ['Total Revenue', fmt_currency(yd['revenue'])],
        ['Total Deductible Expenses', fmt_currency(-yd['expenses'])],
        ['Estimated Taxable Income', fmt_currency(taxable)],
        ['Tax Set-Aside (15% of Revenue)', fmt_currency(tax_15)],
    ]
    
    for t in tax_rows:
        rows.append(data_row(t + [''] * 6))
    
    return rows

# ============================================================
# 9. Write Data to Sheet via API
# ============================================================

def rows_to_cell_data(rows):
    """Convert our row format to Google Sheets API cell data."""
    row_data = []
    for row in rows:
        values = row.get('values', [])
        formats = row.get('formats', [{}] * len(values))
        
        cells = []
        for i, val in enumerate(values):
            cell = {}
            fmt = formats[i] if i < len(formats) else {}
            
            # Set value
            if isinstance(val, (int, float)):
                cell['userEnteredValue'] = {'numberValue': val}
            else:
                cell['userEnteredValue'] = {'stringValue': str(val)}
            
            # Set format
            if fmt:
                cell['userEnteredFormat'] = fmt
            
            cells.append(cell)
        
        row_data.append({'values': cells})
    
    return row_data

def write_tab(sheet_id, rows, tab_name):
    """Write rows to a sheet tab."""
    print(f"  Writing {tab_name} ({len(rows)} rows)...")
    
    # First, convert to A1 notation values for simple write
    values = []
    for row in rows:
        values.append(row.get('values', []))
    
    # Write values
    range_name = f"'{tab_name}'!A1"
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/{urllib.parse.quote(range_name)}?valueInputOption=USER_ENTERED"
    body = {'values': values}
    sheets_api('PUT', url, body)
    
    # Now apply formatting via batchUpdate
    requests = []
    
    for row_idx, row in enumerate(rows):
        formats = row.get('formats', [])
        merge = row.get('merge', None)
        
        # Apply merge if specified
        if merge:
            start_col, end_col = merge
            requests.append({
                'mergeCells': {
                    'range': {
                        'sheetId': sheet_id,
                        'startRowIndex': row_idx,
                        'endRowIndex': row_idx + 1,
                        'startColumnIndex': start_col,
                        'endColumnIndex': end_col
                    },
                    'mergeType': 'MERGE_ALL'
                }
            })
        
        # Apply cell formatting
        for col_idx, fmt in enumerate(formats):
            if fmt:
                requests.append({
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': row_idx,
                            'endRowIndex': row_idx + 1,
                            'startColumnIndex': col_idx,
                            'endColumnIndex': col_idx + 1
                        },
                        'cell': {'userEnteredFormat': fmt},
                        'fields': 'userEnteredFormat'
                    }
                })
    
    # Set column widths
    col_widths = [200, 150, 150, 150, 150, 150, 150, 150]
    for i, width in enumerate(col_widths):
        requests.append({
            'updateDimensionProperties': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': i,
                    'endIndex': i + 1
                },
                'properties': {'pixelSize': width},
                'fields': 'pixelSize'
            }
        })
    
    # Freeze first row
    requests.append({
        'updateSheetProperties': {
            'properties': {
                'sheetId': sheet_id,
                'gridProperties': {'frozenRowCount': 1}
            },
            'fields': 'gridProperties.frozenRowCount'
        }
    })
    
    # Send formatting in batches (max 100 requests per batch to avoid API limits)
    batch_size = 100
    for i in range(0, len(requests), batch_size):
        batch = requests[i:i + batch_size]
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate"
        sheets_api('POST', url, {'requests': batch})
    
    print(f"  ✅ {tab_name} complete ({len(requests)} format operations)")

# Build and write all tabs
alltime_rows = build_alltime_rows()
write_tab(0, alltime_rows, '🌐 All Time Dashboard')

year_2025_rows = build_year_rows(2025, range(1, 13))
write_tab(1, year_2025_rows, '📅 2025')

year_2026_rows = build_year_rows(2026, range(1, 13))
write_tab(2, year_2026_rows, '📅 2026')

year_2024_rows = build_year_rows(2024, range(1, 13))
write_tab(3, year_2024_rows, '📅 2024')

# ============================================================
# 10. Save Sheet ID and Write Report
# ============================================================

SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit"

# Save sheet ID
with open('/home/ec2-user/clawd/data/alltime-sheet-id.txt', 'w') as f:
    f.write(SPREADSHEET_ID)

print(f"\n✅ Sheet ID saved to alltime-sheet-id.txt")

# Build report
report = f"""# 📊 KuriosBrand All Time Financial Overview — Build Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Sheet URL:** {SHEET_URL}
**Sheet ID:** {SPREADSHEET_ID}

---

## Data Sources Processed

| Source | Transactions | Date Range |
|--------|-------------|------------|
| Business 4991 | {len(biz_4991)} | Feb 2024 – Feb 2026 |
| Personal 0068 | {len(personal_0068)} | Apr 2025 – Feb 2026 |
| Biz CC 0678 | {len(bizcc_0678)} | May 2024 – Feb 2026 |
| Sapphire 4252 | {len(sapphire_4252)} | Feb 2024 – Jan 2026 |
| **TOTAL** | **{len(biz_4991) + len(personal_0068) + len(bizcc_0678) + len(sapphire_4252)}** | |

## All Time Summary

| Metric | Value |
|--------|-------|
| Total Revenue | {fmt_currency(alltime_revenue)} |
| Total Expenses | {fmt_currency(alltime_expenses)} |
| Net Profit | {fmt_currency(alltime_profit)} |
| Profit Margin | {fmt_pct(alltime_margin)} |
| Months Tracked | {len([ym for ym in monthly_summary if monthly_summary[ym]['revenue'] > 0])} |

## Revenue by Business Line

| Line | All Time | % |
|------|----------|---|
"""

for line in ['🚗 MVA Lead Gen', '🏗️ Rank & Rent', '🔧 SEO / One-Time']:
    total = sum(yearly_biz_line[y].get(line, 0) for y in [2024, 2025, 2026])
    pct = total / alltime_revenue if alltime_revenue > 0 else 0
    report += f"| {line} | {fmt_currency(total)} | {fmt_pct(pct)} |\n"

report += f"""
## Yearly Breakdown

| Year | Revenue | Expenses | Profit | Margin |
|------|---------|----------|--------|--------|
"""

for year in sorted(yearly_data.keys()):
    yd = yearly_data[year]
    report += f"| {year} | {fmt_currency(yd['revenue'])} | {fmt_currency(yd['expenses'])} | {fmt_currency(yd['profit'])} | {fmt_pct(yd.get('margin', 0))} |\n"

report += f"""
## Tabs Built

1. **🌐 All Time Dashboard** — Executive summary, revenue by business line, monthly trend, expense categories, health metrics, pivot timeline
2. **📅 2025** — Year dashboard with monthly breakdown, expense categories, top vendors, income by client, tax summary
3. **📅 2026** — Year dashboard (Jan 2026 onward)
4. **📅 2024** — Year dashboard (Feb–Dec 2024, Stripe income only pre-tracking)

## Formatting Applied

- Navy #1B2A4A section headers with white text
- Column headers with light gray background
- Total rows with light navy background
- All Time tab: Gold/Amber tab color
- Year tabs: Navy tab color
- Merged section header cells
- Column widths optimized for readability

## Income Classification Applied

- **Stripe deposits 2024–Sep 2025:** 🏗️ Rank & Rent
- **Stripe deposits Nov 2025+:** 🚗 MVA Lead Gen  
- **Zelle from ACI Enterprise (pre-Nov 2025):** 🏗️ Rank & Rent
- **Zelle from ACI Enterprise (Nov 2025+):** 🚗 MVA Lead Gen
- **Zelle from Willard Construction:** 🏗️ Rank & Rent (pre-Nov) / 🚗 MVA (post-Nov)
- **Zelle from Eddy Orozco:** 🔧 SEO / One-Time
- **Jan 2026 Zelle (A-Z Mobile, Reddin, Bible, Willard):** 🚗 MVA Lead Gen
- **Others:** Defaulted to 🔧 SEO / One-Time

## Verified Monthly Data Used

Where available, verified totals from standardized monthly sheets were used:
- Jun 2025: $9,023 rev / $4,253 exp
- Jul 2025: $12,688 rev / $3,851 exp
- Aug 2025: $7,848 rev / $2,660 exp
- Sep 2025: $6,510 rev / $1,962 exp
- Nov 2025: $5,071 rev / $2,035 exp
- Dec 2025: $6,326 rev / $3,611 exp
- Jan 2026: $9,322 rev / $9,609 exp
"""

with open('/home/ec2-user/clawd/data/alltime-build-report.md', 'w') as f:
    f.write(report)

print(f"✅ Report saved to alltime-build-report.md")
print(f"\n🎉 DONE! Sheet URL: {SHEET_URL}")
