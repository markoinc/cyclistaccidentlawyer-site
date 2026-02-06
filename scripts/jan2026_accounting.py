#!/usr/bin/env python3
"""
January 2026 — KuriosBrand Financial Overview
Complete accounting sheet builder for all 4 accounts.
"""

import csv
import json
import re
import io
import requests
from datetime import datetime, timedelta
from collections import defaultdict

# ── Auth ──────────────────────────────────────────────────────────────────────
def get_token():
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": "838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com",
        "client_secret": "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",
        "refresh_token": "1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw",
        "grant_type": "refresh_token"
    })
    return r.json()["access_token"]

TOKEN = get_token()
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# ── File Paths ────────────────────────────────────────────────────────────────
FILES = {
    "personal_0068": "/home/ec2-user/.clawdbot/media/inbound/69300223-3d85-4a27-8ab7-189e87f6ffd4.csv",
    "business_4991": "/home/ec2-user/.clawdbot/media/inbound/4c49e3bf-d868-436d-96df-59725155a2af.csv",
    "biz_cc_0678": "/home/ec2-user/.clawdbot/media/inbound/a862171a-b76d-4627-9a67-1d9be4937e25.csv",
    "sapphire_4252": "/home/ec2-user/.clawdbot/media/inbound/ddb34375-098a-4941-8b7e-0dc4abc900c3.csv",
}

# ── Parse CSVs ────────────────────────────────────────────────────────────────
def parse_checking(filepath, account_name):
    """Parse Chase checking CSV (Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #)"""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get('Description', '').strip().strip('"')
            date_str = row.get('Posting Date', '').strip()
            amount_str = row.get('Amount', '').strip()
            balance_str = row.get('Balance', '').strip()
            detail_type = row.get('Details', '').strip()
            txn_type = row.get('Type', '').strip()
            
            if not date_str or not amount_str:
                continue
            
            try:
                date = datetime.strptime(date_str, '%m/%d/%Y')
                amount = float(amount_str.replace(',', ''))
            except (ValueError, TypeError):
                continue
            
            try:
                balance = float(balance_str.replace(',', '')) if balance_str else None
            except (ValueError, TypeError):
                balance = None
            
            txns.append({
                'date': date,
                'date_str': date_str,
                'description': desc,
                'amount': amount,
                'balance': balance,
                'detail_type': detail_type,
                'txn_type': txn_type,
                'account': account_name,
            })
    return txns

def parse_cc(filepath, account_name, has_card_col=True):
    """Parse Chase CC CSV"""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            desc = row.get('Description', '').strip()
            if has_card_col:
                date_str = row.get('Transaction Date', '').strip()
                post_date_str = row.get('Post Date', '').strip()
            else:
                date_str = row.get('Transaction Date', '').strip()
                post_date_str = row.get('Post Date', '').strip()
            
            amount_str = row.get('Amount', '').strip()
            category = row.get('Category', '').strip()
            cc_type = row.get('Type', '').strip()
            
            if not date_str or not amount_str:
                continue
            
            try:
                date = datetime.strptime(date_str, '%m/%d/%Y')
                amount = float(amount_str.replace(',', ''))
            except (ValueError, TypeError):
                continue
            
            txns.append({
                'date': date,
                'date_str': date_str,
                'post_date': post_date_str,
                'description': desc,
                'amount': amount,
                'balance': None,
                'category': category,
                'cc_type': cc_type,
                'account': account_name,
            })
    return txns

# ── Load all data ─────────────────────────────────────────────────────────────
print("Loading transaction data...")
personal_0068 = parse_checking(FILES["personal_0068"], "Personal 0068")
business_4991 = parse_checking(FILES["business_4991"], "Business 4991")
biz_cc_0678 = parse_cc(FILES["biz_cc_0678"], "Biz CC 0678", has_card_col=True)
sapphire_4252 = parse_cc(FILES["sapphire_4252"], "Sapphire 4252", has_card_col=False)

# Filter to January 2026 only (some Feb transactions bleed in)
JAN_START = datetime(2026, 1, 1)
JAN_END = datetime(2026, 1, 31, 23, 59, 59)

def filter_jan(txns):
    return [t for t in txns if JAN_START <= t['date'] <= JAN_END]

personal_0068_jan = filter_jan(personal_0068)
business_4991_jan = filter_jan(business_4991)
biz_cc_0678_jan = filter_jan(biz_cc_0678)
sapphire_4252_jan = filter_jan(sapphire_4252)

print(f"Personal 0068: {len(personal_0068)} total, {len(personal_0068_jan)} in Jan")
print(f"Business 4991: {len(business_4991)} total, {len(business_4991_jan)} in Jan")
print(f"Biz CC 0678: {len(biz_cc_0678)} total, {len(biz_cc_0678_jan)} in Jan")
print(f"Sapphire 4252: {len(sapphire_4252)} total, {len(sapphire_4252_jan)} in Jan")

# ── Categorization ────────────────────────────────────────────────────────────
def clean_vendor(desc):
    """Extract clean vendor name from messy Chase descriptions"""
    desc_upper = desc.upper()
    
    # Business 4991 / Personal patterns
    patterns = [
        (r'STRIPE\s+TRANSFER', 'Stripe'),
        (r'STRIPE', 'Stripe'),
        (r'Zelle payment from ACI ENTERPRISE', 'ACI Enterprise (Zelle)'),
        (r'Zelle payment from A-Z MOBILE APPS', 'A-Z Mobile Apps (Zelle)'),
        (r'Zelle payment from ANTHONY REDDIN', 'Anthony Reddin (Zelle)'),
        (r'Zelle payment from ALEXANDER SHTABSKY', 'Alexander Shtabsky (Zelle)'),
        (r'Zelle payment from JONATHAN BIBLE', 'Jonathan Bible (Zelle)'),
        (r'Zelle payment from CHRISTIAN WILLARD', 'Christian Willard (Zelle)'),
        (r'Zelle payment to Jonathan Bible', 'Jonathan Bible (Zelle Out)'),
        (r'GOHIGHLEVEL|HIGHLEVEL AGENCY', 'GoHighLevel (Agency)'),
        (r'HIGHLEVEL INC', 'GoHighLevel'),
        (r'10WEB\.IO', '10web.io'),
        (r'GOOGLE \*Workspace_ku', 'Google Workspace (Kurios)'),
        (r'GOOGLE \*Workspace_co', 'Google Workspace (Co)'),
        (r'GOOGLE \*CLOUD', 'Google Cloud'),
        (r'GOOGLE \*Gemini', 'Google Gemini'),
        (r'GOOGLE \*ADS914', 'Google Ads (914)'),
        (r'GOOGLE \*ADS270', 'Google Ads (270)'),
        (r'GOOGLE \*Google One', 'Google One'),
        (r'CHATGPT|OPENAI', 'OpenAI / ChatGPT'),
        (r'CLAUDE\.AI|ANTHROPIC', 'Claude AI (Anthropic)'),
        (r'LEMLIST', 'Lemlist'),
        (r'INSTANTLY', 'Instantly'),
        (r'NAME-?CHEAP', 'Namecheap'),
        (r'SAFETYWING', 'SafetyWing'),
        (r'T-?MOBILE|TMOBILE', 'T-Mobile'),
        (r'CREDIT STRONG|Credit Strong', 'Credit Strong'),
        (r'SELF LENDER', 'Self Lender'),
        (r'AFFIRM', 'Affirm'),
        (r'Wise\s', 'Wise'),
        (r'FACEBK|FACEBOOK|META', 'Meta / Facebook Ads'),
        (r'FLOWITH', 'Flowith'),
        (r'LOVABLE', 'Lovable'),
        (r'EXA\.AI', 'Exa.ai'),
        (r'APIFY', 'Apify'),
        (r'REVID', 'Revid'),
        (r'PERPLEXITY', 'Perplexity'),
        (r'MONTHLY SERVICE FEE', 'Chase Monthly Service Fee'),
        (r'STOP PAYMENT FEE', 'Chase Stop Payment Fee'),
        (r'ROBINHOOD\s+DEBITS', 'Robinhood (Recurring Buy)'),
        (r'REAL TIME TRANSFER.*Robinhood', 'Robinhood (Withdrawal)'),
        (r'Acorns Invest\s+Transfer', 'Acorns (Invest)'),
        (r'Acorns Round-Ups', 'Acorns (Round-Ups)'),
        (r'Subscription\s+Acorns', 'Acorns (Subscription Fee)'),
        (r'NON-CHASE ATM WITHDRAW', 'ATM Withdrawal'),
        (r'NON-CHASE ATM FEE', 'Non-Chase ATM Fee'),
        (r'FOREIGN EXCHANGE', 'Foreign Exchange Fee'),
        (r'Online Transfer to\s+SAV.*7036', 'Transfer to Savings 7036'),
        (r'Online Transfer from SAV.*7036', 'Transfer from Savings 7036'),
        (r'Online Transfer from\s*CHK.*4991', 'Transfer from Biz 4991'),
        (r'Online Transfer to\s*CHK.*4991', 'Transfer to Biz 4991'),
        (r'Online Transfer from\s*CHK.*0068', 'Transfer from Personal 0068'),
        (r'Online Transfer to\s*CHK.*0068', 'Transfer to Personal 0068'),
        (r'ODP TRANSFER FROM SAVINGS', 'ODP from Savings 7036'),
        (r'TOT ODP', 'Overdraft Protection Credit'),
        (r'CHASE CREDIT CRD AUTOPAY', 'Chase Sapphire Autopay'),
        (r'CHASE CREDIT CRD.*AUTOPAYBUSSEC', 'Chase Biz CC Autopay'),
        (r'Payment to Chase card ending in 4252', 'Payment to Sapphire 4252'),
        (r'Payment to Chase card ending in 0678', 'Payment to Biz CC 0678'),
        (r'DEPT EDUCATION\s+STUDENT', 'Student Loan (Dept of Ed)'),
        (r'IBERIA', 'Iberia Airlines'),
        (r'LATAM AIRLIN', 'LATAM Airlines'),
        (r'AIRALO', 'Airalo (eSIM)'),
        (r'HULU', 'Hulu'),
        (r'SOLSTICE', 'Solstice (Dental)'),
        (r'Patreon', 'Patreon'),
        (r'KULA COMMUNITY', 'Kula Community'),
        (r'SPOTIFY', 'Spotify'),
        (r'HOSTMYAPPL', 'HostMyAppl'),
        (r'WI DFI', 'WI DFI (State Filing)'),
        (r'WWW\.BRAVE\.COM', 'Brave.com'),
        (r'PURCHASE INTEREST CHARGE', 'Interest Charge'),
        (r'ANNUAL MEMBERSHIP FEE', 'Annual Membership Fee'),
        (r'STATEMENT CREDIT', 'Statement Credit'),
        (r'Payment Thank You|AUTOMATIC PAYMENT', 'CC Payment'),
        (r'CLOUDFLARE', 'Cloudflare'),
        (r'WEBSHARE', 'Webshare Proxy'),
        (r'INVIDEO', 'InVideo'),
        (r'SUPERMEMORY', 'Supermemory'),
        (r'al\.Nord\*VPN', 'NordVPN'),
        (r'MYFICO', 'MyFICO'),
        (r'CURSOR', 'Cursor (AI IDE)'),
        (r'HIGGSFIELD', 'Higgsfield'),
        (r'APPLE\.COM/BILL|APPLE COM BILL', 'Apple'),
        (r'DESCRIPT', 'Descript'),
        (r'FS \*dataforseo', 'DataForSEO'),
        (r'META WAVE', 'Meta Wave Solutions'),
        (r'GM\* RAPIDURLINDEXER', 'RapidURL Indexer'),
        (r'TRAVELINGMAILBOX', 'Traveling Mailbox'),
        (r'ETA-IL\s+ELETRONIC', 'Electronic Travel Auth (Israel)'),
        (r'Online Transfer from SAV', 'Transfer from Savings'),
    ]
    
    for pattern, name in patterns:
        if re.search(pattern, desc, re.IGNORECASE):
            return name
    
    # Fallback: try to extract the first meaningful part
    desc_clean = re.sub(r'\s+', ' ', desc).strip()
    if len(desc_clean) > 50:
        desc_clean = desc_clean[:50] + '...'
    return desc_clean

def categorize_biz_4991(txn):
    """Categorize Business 4991 transactions"""
    desc = txn['description'].upper()
    amount = txn['amount']
    
    # Income
    if 'STRIPE' in desc and amount > 0:
        return 'Income', 'Client Revenue (Stripe)'
    if 'ZELLE PAYMENT FROM' in desc.upper() and amount > 0:
        return 'Income', 'Client Revenue (Zelle)'
    if 'CREDIT STRONG' in desc and amount > 0:
        return 'Income', 'Credit Strong Payment'
    if 'REAL TIME PAYMENT CREDIT' in desc and 'STRIPE' in desc:
        return 'Income', 'Client Revenue (Stripe RTP)'
    
    # Transfers (NOT expenses)
    if 'ONLINE TRANSFER TO CHK' in desc and '0068' in desc:
        return 'Transfer', 'Biz → Personal'
    if 'ONLINE TRANSFER TO  CHK' in desc and '0068' in desc:
        return 'Transfer', 'Biz → Personal'
    if 'ONLINE TRANSFER FROM CHK' in desc and '0068' in desc:
        return 'Transfer', 'Personal → Biz'
    if 'ONLINE TRANSFER FROM  CHK' in desc and '0068' in desc:
        return 'Transfer', 'Personal → Biz'
    if 'ONLINE TRANSFER FROM SAV' in desc:
        return 'Transfer', 'Savings → Biz'
    if 'ZELLE PAYMENT TO' in desc.upper():
        return 'Transfer', 'Zelle Out'
    
    # CC Payments
    if 'PAYMENT TO CHASE CARD' in desc and '0678' in desc:
        return 'CC Payment', 'Payment to Biz CC 0678'
    if 'PAYMENT TO CHASE CARD' in desc and '4252' in desc:
        return 'CC Payment', 'Payment to Sapphire 4252'
    if 'CHASE CREDIT CRD' in desc and 'AUTOPAY' in desc:
        return 'CC Payment', 'Biz CC Autopay'
    
    # SaaS & Tools
    if 'GOHIGHLEVEL' in desc or 'HIGHLEVEL' in desc:
        if 'AGENCY' in desc:
            return 'Expense', '📱 SaaS (GoHighLevel Agency)'
        return 'Expense', '📱 SaaS (GoHighLevel)'
    if '10WEB' in desc:
        return 'Expense', '📱 SaaS (10web.io)'
    if 'GOOGLE' in desc and 'WORKSPACE' in desc:
        return 'Expense', '📱 SaaS (Google Workspace)'
    if 'GOOGLE' in desc and 'CLOUD' in desc:
        return 'Expense', '📱 SaaS (Google Cloud)'
    if 'GOOGLE' in desc and ('ADS' in desc or 'ADS' in desc):
        return 'Expense', '📣 Marketing (Google Ads)'
    if 'GOOGLE' in desc and 'ONE' in desc:
        return 'Expense', '📱 SaaS (Google One)'
    if 'CHATGPT' in desc or 'OPENAI' in desc:
        return 'Expense', '📱 SaaS (OpenAI/ChatGPT)'
    if 'CLAUDE' in desc or 'ANTHROPIC' in desc:
        return 'Expense', '📱 SaaS (Claude AI)'
    if 'LEMLIST' in desc:
        return 'Expense', '📱 SaaS (Lemlist)'
    if 'INSTANTLY' in desc:
        return 'Expense', '📱 SaaS (Instantly)'
    if 'LOVABLE' in desc:
        return 'Expense', '📱 SaaS (Lovable)'
    if 'EXA' in desc and 'AI' in desc:
        return 'Expense', '📱 SaaS (Exa.ai)'
    if 'CURSOR' in desc:
        return 'Expense', '📱 SaaS (Cursor)'
    if 'HIGGSFIELD' in desc:
        return 'Expense', '📱 SaaS (Higgsfield)'
    if 'DESCRIPT' in desc:
        return 'Expense', '📱 SaaS (Descript)'
    if 'DATAFORSEO' in desc:
        return 'Expense', '📱 SaaS (DataForSEO)'
    if 'INVIDEO' in desc:
        return 'Expense', '📱 SaaS (InVideo)'
    if 'SUPERMEMORY' in desc:
        return 'Expense', '📱 SaaS (Supermemory)'
    if 'CLOUDFLARE' in desc:
        return 'Expense', '📱 SaaS (Cloudflare)'
    if 'WEBSHARE' in desc:
        return 'Expense', '📱 SaaS (Webshare Proxy)'
    if 'NORDVPN' in desc or 'NORD*VPN' in desc:
        return 'Expense', '📱 SaaS (NordVPN)'
    if 'APPLE' in desc:
        return 'Expense', '📱 SaaS (Apple)'
    if 'RAPIDURLINDEXER' in desc:
        return 'Expense', '📱 SaaS (RapidURL Indexer)'
    if 'MYFICO' in desc:
        return 'Expense', '📱 SaaS (MyFICO)'
    if 'META WAVE' in desc:
        return 'Expense', '📱 SaaS (Meta Wave)'
    
    # Marketing / Ads
    if 'FACEBK' in desc or 'FACEBOOK' in desc or ('META' in desc and 'WAVE' not in desc):
        return 'Expense', '📣 Marketing (Meta Ads)'
    
    # Operations
    if 'TMOBILE' in desc or 'T-MOBILE' in desc:
        return 'Expense', '🏢 Operations (T-Mobile)'
    if 'NAMECHEAP' in desc or 'NAME-CHEAP' in desc:
        return 'Expense', '🏢 Operations (Domains)'
    if 'TRAVELINGMAILBOX' in desc:
        return 'Expense', '🏢 Operations (Mailbox)'
    if 'ETA-IL' in desc:
        return 'Expense', '🏢 Operations (Travel Auth)'
    if 'MONTHLY SERVICE FEE' in desc:
        return 'Expense', '🏢 Operations (Bank Fee)'
    if 'STOP PAYMENT FEE' in desc:
        return 'Expense', '🏢 Operations (Bank Fee)'
    if 'NON-CHASE ATM FEE' in desc:
        return 'Expense', '🏢 Operations (ATM Fee)'
    if 'NON-CHASE ATM WITHDRAW' in desc:
        return 'Expense', '🏢 Operations (ATM Withdrawal)'
    if 'FOREIGN EXCHANGE' in desc:
        return 'Expense', '🏢 Operations (FX Fee)'
    
    # Insurance
    if 'SAFETYWING' in desc:
        return 'Expense', '🛡️ Insurance (SafetyWing)'
    
    # Debt
    if 'AFFIRM' in desc:
        return 'Expense', '💳 Debt (Affirm)'
    if 'CREDIT STRONG' in desc and amount < 0:
        return 'Expense', '💳 Debt (Credit Strong)'
    if 'SELF LENDER' in desc:
        return 'Expense', '💳 Debt (Self Lender)'
    
    # Wise (living expenses transfer)
    if 'WISE' in desc:
        return 'Expense', '🏢 Operations (Wise Transfer)'
    
    return 'Uncategorized', 'Other'

def categorize_personal_0068(txn):
    """Categorize Personal 0068 transactions"""
    desc = txn['description'].upper()
    amount = txn['amount']
    
    # Transfers
    if 'ONLINE TRANSFER FROM CHK' in desc and '4991' in desc:
        return 'Transfer', 'Biz → Personal'
    if 'ONLINE TRANSFER FROM  CHK' in desc and '4991' in desc:
        return 'Transfer', 'Biz → Personal'
    if 'ONLINE TRANSFER TO CHK' in desc and '4991' in desc:
        return 'Transfer', 'Personal → Biz'
    if 'ONLINE TRANSFER TO  SAV' in desc and '7036' in desc:
        return 'Transfer', 'Personal → Savings'
    if 'ONLINE TRANSFER FROM SAV' in desc and '7036' in desc:
        return 'Transfer', 'Savings → Personal'
    if 'ONLINE TRANSFER FROM  SAV' in desc:
        return 'Transfer', 'Savings → Personal'
    if 'ODP TRANSFER FROM SAVINGS' in desc:
        return 'Transfer', 'ODP from Savings'
    if 'TOT ODP' in desc:
        return 'Transfer', 'Overdraft Protection'
    
    # Investments
    if 'ROBINHOOD' in desc and 'DEBITS' in desc:
        return 'Expense', '📈 Investments (Robinhood)'
    if 'REAL TIME TRANSFER' in desc and 'ROBINHOOD' in desc:
        return 'Income', 'Robinhood Withdrawal'
    if 'ACORNS INVEST' in desc and 'TRANSFER' in desc and amount < 0:
        return 'Expense', '📈 Investments (Acorns)'
    if 'ACORNS ROUND-UPS' in desc:
        return 'Expense', '📈 Investments (Acorns Round-Ups)'
    if 'SUBSCRIPTION' in desc and 'ACORNS' in desc:
        return 'Expense', '📈 Investments (Acorns Fee)'
    if 'ACORNS INVEST' in desc and amount > 0:
        return 'Income', 'Acorns Return'
    
    # ATM & Fees
    if 'NON-CHASE ATM WITHDRAW' in desc:
        return 'Expense', '🏧 ATM Withdrawal'
    if 'NON-CHASE ATM FEE' in desc:
        return 'Expense', '🏧 ATM Fee'
    if 'FOREIGN EXCHANGE' in desc:
        return 'Expense', '🏧 FX Fee'
    
    # CC Payments
    if 'CHASE CREDIT CRD AUTOPAY' in desc:
        return 'CC Payment', 'Sapphire CC Autopay'
    
    # Student Loan
    if 'DEPT EDUCATION' in desc or 'STUDENT LN' in desc:
        return 'Expense', '🎓 Student Loan'
    
    # Travel
    if 'IBERIA' in desc:
        return 'Expense', '✈️ Travel (Flight)'
    if 'LATAM AIRLIN' in desc:
        return 'Expense', '✈️ Travel (Flight)'
    if 'AIRALO' in desc:
        return 'Expense', '✈️ Travel (eSIM)'
    
    # Subscriptions
    if 'HULU' in desc:
        return 'Expense', '📺 Subscriptions (Hulu)'
    if 'SOLSTICE' in desc:
        return 'Expense', '📺 Subscriptions (Dental)'
    if 'PATREON' in desc:
        return 'Expense', '📺 Subscriptions (Patreon)'
    
    # Living/Local
    if 'KULA COMMUNITY' in desc:
        return 'Expense', '🏠 Living/Local'
    
    return 'Uncategorized', 'Other'

def categorize_biz_cc_0678(txn):
    """Categorize Biz CC 0678 transactions"""
    desc = txn['description'].upper()
    amount = txn['amount']
    cc_type = txn.get('cc_type', '').upper()
    
    if cc_type == 'PAYMENT' or 'PAYMENT' in desc:
        return 'CC Payment', 'CC Payment Received'
    if 'STATEMENT CREDIT' in desc:
        return 'CC Payment', 'Statement Credit'
    if 'INTEREST CHARGE' in desc:
        return 'Expense', '💰 CC Interest'
    
    if 'FACEBK' in desc or 'FACEBOOK' in desc:
        return 'Expense', '📣 Marketing (Meta Ads)'
    if 'SPOTIFY' in desc:
        return 'Expense', '📱 SaaS (Spotify)'
    if 'GOOGLE' in desc and 'WORKSPACE' in desc:
        return 'Expense', '📱 SaaS (Google Workspace)'
    if 'HOSTMYAPPL' in desc:
        return 'Expense', '📱 SaaS (HostMyAppl)'
    if 'WI DFI' in desc:
        return 'Expense', '🏢 Operations (State Filing)'
    if 'BRAVE' in desc:
        return 'Expense', '📱 SaaS (Brave)'
    if 'NAME-?CHEAP' in desc or 'NAMECHEAP' in desc:
        return 'Expense', '🏢 Operations (Domains)'
    
    return 'Uncategorized', 'Other'

def categorize_sapphire_4252(txn):
    """Categorize Sapphire 4252 transactions"""
    desc = txn['description'].upper()
    amount = txn['amount']
    cc_type = txn.get('cc_type', '').upper()
    
    if cc_type == 'PAYMENT' or 'PAYMENT' in desc:
        return 'CC Payment', 'CC Payment Received'
    if 'STATEMENT CREDIT' in desc:
        return 'CC Payment', 'Statement Credit'
    if 'INTEREST CHARGE' in desc:
        return 'Expense', '💰 CC Interest'
    if 'ANNUAL MEMBERSHIP FEE' in desc:
        return 'Expense', '💳 CC Fee'
    
    if 'FACEBK' in desc or 'FACEBOOK' in desc:
        return 'Expense', '📣 Marketing (Meta Ads) ⚠️ Personal Card!'
    if 'LATAM AIRLIN' in desc:
        return 'Expense', '✈️ Travel (Flight)'
    
    return 'Uncategorized', 'Other'

# Apply categorization
for txn in business_4991_jan:
    txn['cat_type'], txn['category'] = categorize_biz_4991(txn)
    txn['vendor'] = clean_vendor(txn['description'])

for txn in personal_0068_jan:
    txn['cat_type'], txn['category'] = categorize_personal_0068(txn)
    txn['vendor'] = clean_vendor(txn['description'])

for txn in biz_cc_0678_jan:
    txn['cat_type'], txn['category'] = categorize_biz_cc_0678(txn)
    txn['vendor'] = clean_vendor(txn['description'])

for txn in sapphire_4252_jan:
    txn['cat_type'], txn['category'] = categorize_sapphire_4252(txn)
    txn['vendor'] = clean_vendor(txn['description'])

# ── Build Dashboard Data ──────────────────────────────────────────────────────
print("\nBuilding dashboard data...")

# SECTION A: Income Summary
stripe_income = []
zelle_income = []
other_income = []

for txn in business_4991_jan:
    if txn['cat_type'] == 'Income':
        if 'Stripe' in txn['category']:
            stripe_income.append(txn)
        elif 'Zelle' in txn['category']:
            zelle_income.append(txn)
        else:
            other_income.append(txn)

total_stripe = sum(t['amount'] for t in stripe_income)
total_zelle = sum(t['amount'] for t in zelle_income)
total_other_income = sum(t['amount'] for t in other_income)
total_biz_income = total_stripe + total_zelle + total_other_income

print(f"  Stripe Income: ${total_stripe:,.2f}")
print(f"  Zelle Income: ${total_zelle:,.2f}")
print(f"  Other Income: ${total_other_income:,.2f}")
print(f"  Total Biz Income: ${total_biz_income:,.2f}")

# SECTION B: Business Expenses
biz_expenses = defaultdict(list)
for txn in business_4991_jan:
    if txn['cat_type'] == 'Expense':
        biz_expenses[txn['category']].append(txn)

# Also add CC expenses that are business
for txn in biz_cc_0678_jan:
    if txn['cat_type'] == 'Expense':
        biz_expenses[txn['category']].append(txn)

# Meta Ads on Sapphire (should be biz expense)
for txn in sapphire_4252_jan:
    if 'Meta Ads' in txn.get('category', ''):
        biz_expenses[txn['category']].append(txn)

# Group into main categories
saas_tools = {}
marketing_ads = {}
operations = {}
insurance = {}
debt_payments = {}
cc_interest = {}
cc_fees = {}

for cat, txns in biz_expenses.items():
    total = sum(t['amount'] for t in txns)
    if '📱 SaaS' in cat:
        saas_tools[cat] = (txns, total)
    elif '📣 Marketing' in cat:
        marketing_ads[cat] = (txns, total)
    elif '🏢 Operations' in cat:
        operations[cat] = (txns, total)
    elif '🛡️ Insurance' in cat:
        insurance[cat] = (txns, total)
    elif '💳 Debt' in cat or '💳 CC Fee' in cat:
        debt_payments[cat] = (txns, total)
    elif '💰 CC Interest' in cat:
        cc_interest[cat] = (txns, total)

total_saas = sum(v[1] for v in saas_tools.values())
total_marketing = sum(v[1] for v in marketing_ads.values())
total_operations = sum(v[1] for v in operations.values())
total_insurance = sum(v[1] for v in insurance.values())
total_debt = sum(v[1] for v in debt_payments.values())
total_cc_interest_biz = sum(v[1] for v in cc_interest.values())

total_biz_expenses = total_saas + total_marketing + total_operations + total_insurance + total_debt + total_cc_interest_biz

# SECTION C: Personal Expenses
personal_expenses = defaultdict(list)
for txn in personal_0068_jan:
    if txn['cat_type'] == 'Expense':
        personal_expenses[txn['category']].append(txn)

# Sapphire personal expenses
for txn in sapphire_4252_jan:
    if txn['cat_type'] == 'Expense' and 'Meta' not in txn.get('category', ''):
        personal_expenses[txn['category']].append(txn)

atm_cash = {}
investments = {}
travel = {}
subscriptions = {}
student_loan = {}
personal_cc_interest = {}
personal_cc_fee = {}
living = {}

for cat, txns in personal_expenses.items():
    total = sum(t['amount'] for t in txns)
    if '🏧' in cat:
        atm_cash[cat] = (txns, total)
    elif '📈' in cat:
        investments[cat] = (txns, total)
    elif '✈️' in cat:
        travel[cat] = (txns, total)
    elif '📺' in cat:
        subscriptions[cat] = (txns, total)
    elif '🎓' in cat:
        student_loan[cat] = (txns, total)
    elif '💰 CC Interest' in cat:
        personal_cc_interest[cat] = (txns, total)
    elif '💳 CC Fee' in cat:
        personal_cc_fee[cat] = (txns, total)
    elif '🏠' in cat:
        living[cat] = (txns, total)

total_atm = sum(v[1] for v in atm_cash.values())
total_investments = sum(v[1] for v in investments.values())
total_travel = sum(v[1] for v in travel.values())
total_subs = sum(v[1] for v in subscriptions.values())
total_student = sum(v[1] for v in student_loan.values())
total_personal_cc_interest = sum(v[1] for v in personal_cc_interest.values())
total_personal_cc_fee = sum(v[1] for v in personal_cc_fee.values())
total_living = sum(v[1] for v in living.values())

# CC Payments from personal
personal_cc_payments = sum(t['amount'] for t in personal_0068_jan if t['cat_type'] == 'CC Payment')

total_personal_expenses = (total_atm + total_investments + total_travel + total_subs + 
                          total_student + total_personal_cc_interest + total_personal_cc_fee +
                          total_living + personal_cc_payments)

# Meta Ads across ALL cards
meta_ads_all = []
for txn in business_4991_jan:
    if '📣 Marketing (Meta Ads)' == txn.get('category', ''):
        meta_ads_all.append(txn)
for txn in biz_cc_0678_jan:
    if 'Meta Ads' in txn.get('category', ''):
        meta_ads_all.append(txn)
for txn in sapphire_4252_jan:
    if 'Meta Ads' in txn.get('category', ''):
        meta_ads_all.append(txn)

total_meta_ads = sum(t['amount'] for t in meta_ads_all)

# Transfers
transfers_biz_to_personal = []
transfers_personal_to_biz = []
transfers_savings = []
transfers_other = []

for txn in business_4991_jan:
    if txn['cat_type'] == 'Transfer':
        if 'Biz → Personal' in txn['category']:
            transfers_biz_to_personal.append(txn)
        elif 'Personal → Biz' in txn['category']:
            transfers_personal_to_biz.append(txn)
        else:
            transfers_other.append(txn)

for txn in personal_0068_jan:
    if txn['cat_type'] == 'Transfer':
        if 'Biz → Personal' in txn['category']:
            transfers_biz_to_personal.append(txn)
        elif 'Personal → Biz' in txn['category']:
            transfers_personal_to_biz.append(txn)
        elif 'Savings' in txn['category'] or 'ODP' in txn['category'] or 'Overdraft' in txn['category']:
            transfers_savings.append(txn)

# Only count outflows from biz account for accurate transfer totals
total_biz_to_personal = abs(sum(t['amount'] for t in transfers_biz_to_personal if t['amount'] < 0))
total_personal_to_biz = abs(sum(t['amount'] for t in transfers_personal_to_biz if t['amount'] < 0))
total_savings_out = abs(sum(t['amount'] for t in transfers_savings if t['amount'] < 0))
total_savings_in = sum(t['amount'] for t in transfers_savings if t['amount'] > 0)

# Business CC payments from biz checking
biz_cc_payments = sum(t['amount'] for t in business_4991_jan if t['cat_type'] == 'CC Payment')

# Key Metrics
biz_profit = total_biz_income + total_biz_expenses  # expenses are negative
profit_margin = (biz_profit / total_biz_income * 100) if total_biz_income else 0
daily_burn = abs(total_biz_expenses) / 31

# ATM + FX fees
atm_fees = sum(t['amount'] for t in personal_0068_jan if '🏧 ATM Fee' in t.get('category', '') or '🏧 FX Fee' in t.get('category', ''))
# Also include biz account ATM/FX fees
biz_atm_fees = sum(t['amount'] for t in business_4991_jan if 'ATM Fee' in t.get('category', '') or 'FX Fee' in t.get('category', '') or 'ATM Withdrawal' in t.get('category', ''))

# Total CC Interest across all cards
all_cc_interest = total_cc_interest_biz + total_personal_cc_interest

print(f"\n  Total Biz Expenses: ${total_biz_expenses:,.2f}")
print(f"  Business Profit: ${biz_profit:,.2f}")
print(f"  Profit Margin: {profit_margin:.1f}%")
print(f"  Total Meta Ads (ALL cards): ${total_meta_ads:,.2f}")
print(f"  Total CC Interest (all): ${all_cc_interest:,.2f}")

# ── Build Google Sheet ────────────────────────────────────────────────────────
print("\nCreating Google Sheet...")

# Color helpers (RGB 0-1 float)
def rgb(hex_color):
    h = hex_color.lstrip('#')
    return {
        "red": int(h[0:2], 16) / 255,
        "green": int(h[2:4], 16) / 255,
        "blue": int(h[4:6], 16) / 255,
    }

NAVY = rgb("#1B2A4A")
MED_BLUE = rgb("#2D5F8A")
WHITE = rgb("#FFFFFF")
LIGHT_GREEN = rgb("#E8F5E9")
LIGHT_RED = rgb("#FFEBEE")
LIGHT_GRAY = rgb("#F5F5F5")
ALT_ROW = rgb("#F8F9FA")
TOTAL_BG = rgb("#E3F2FD")
RED_TEXT = rgb("#D32F2F")
GREEN_TEXT = rgb("#2E7D32")
DARK_TEXT = rgb("#1A1A1A")
BORDER_GRAY = rgb("#E0E0E0")

# Sheet IDs
DASH_ID = 0
BIZ_ID = 1
PERS_ID = 2
CC_ID = 3
SAPH_ID = 4
RAW_ID = 5

spreadsheet_body = {
    "properties": {
        "title": "January 2026 — KuriosBrand Financial Overview",
        "locale": "en_US",
        "defaultFormat": {
            "textFormat": {"fontFamily": "Inter", "fontSize": 10}
        }
    },
    "sheets": [
        {"properties": {"sheetId": DASH_ID, "title": "📊 Dashboard", "gridProperties": {"frozenRowCount": 1, "columnCount": 8}}},
        {"properties": {"sheetId": BIZ_ID, "title": "💼 Business 4991", "gridProperties": {"frozenRowCount": 1, "columnCount": 6}}},
        {"properties": {"sheetId": PERS_ID, "title": "👤 Personal 0068", "gridProperties": {"frozenRowCount": 1, "columnCount": 6}}},
        {"properties": {"sheetId": CC_ID, "title": "💳 Biz CC 0678", "gridProperties": {"frozenRowCount": 1, "columnCount": 6}}},
        {"properties": {"sheetId": SAPH_ID, "title": "💎 Sapphire 4252", "gridProperties": {"frozenRowCount": 1, "columnCount": 6}}},
        {"properties": {"sheetId": RAW_ID, "title": "📦 Raw Data", "gridProperties": {"frozenRowCount": 1, "columnCount": 8}}},
    ]
}

r = requests.post(
    "https://sheets.googleapis.com/v4/spreadsheets",
    headers=HEADERS,
    json=spreadsheet_body
)
r.raise_for_status()
sheet = r.json()
SPREADSHEET_ID = sheet["spreadsheetId"]
SPREADSHEET_URL = sheet["spreadsheetUrl"]
print(f"  Created: {SPREADSHEET_URL}")

# Save ID
with open("/home/ec2-user/clawd/data/jan-2026-sheet-id.txt", "w") as f:
    f.write(SPREADSHEET_ID)

# ── Helper: write values ──────────────────────────────────────────────────────
def batch_write(ranges_data):
    """Write multiple ranges at once"""
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [{"range": r, "values": v} for r, v in ranges_data]
    }
    r = requests.post(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values:batchUpdate",
        headers=HEADERS,
        json=body
    )
    r.raise_for_status()
    return r.json()

def batch_format(requests_list):
    """Apply formatting"""
    body = {"requests": requests_list}
    r = requests.post(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate",
        headers=HEADERS,
        json=body
    )
    r.raise_for_status()
    return r.json()

# ── Build Dashboard Data ──────────────────────────────────────────────────────
print("  Building dashboard tab...")

dashboard_rows = []

# Title
dashboard_rows.append(["January 2026 — KuriosBrand Financial Overview", "", "", "", "", "", "", ""])
dashboard_rows.append([""])

# ── SECTION A: Income Summary ──
dashboard_rows.append(["💰 SECTION A: INCOME SUMMARY", "", "", "", "", "", "", ""])
dashboard_rows.append(["Source", "Vendor / Client", "Date", "Amount", "", "", "", ""])

# Stripe income itemized
for txn in sorted(stripe_income, key=lambda t: t['date']):
    dashboard_rows.append(["Stripe", txn['vendor'], txn['date_str'], txn['amount']])

dashboard_rows.append(["", "", "Stripe Subtotal", total_stripe])

# Zelle income
for txn in sorted(zelle_income, key=lambda t: t['date']):
    dashboard_rows.append(["Zelle", txn['vendor'], txn['date_str'], txn['amount']])

dashboard_rows.append(["", "", "Zelle Subtotal", total_zelle])

# Other income
if other_income:
    for txn in sorted(other_income, key=lambda t: t['date']):
        dashboard_rows.append(["Other", txn['vendor'], txn['date_str'], txn['amount']])
    dashboard_rows.append(["", "", "Other Subtotal", total_other_income])

dashboard_rows.append(["", "", "TOTAL BUSINESS INCOME", total_biz_income])
dashboard_rows.append([""])

# ── SECTION B: Business Expenses ──
dashboard_rows.append(["📊 SECTION B: BUSINESS EXPENSES", "", "", "", "", "", "", ""])
dashboard_rows.append(["Category", "Vendor", "Count", "Total", "", "", "", ""])

# SaaS & Tools
dashboard_rows.append(["📱 SaaS & Tools", "", "", "", "", "", "", ""])
for cat in sorted(saas_tools.keys()):
    txns, total = saas_tools[cat]
    # Extract tool name from category
    name = cat.replace('📱 SaaS (', '').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "SaaS Subtotal", total_saas])

# Marketing
dashboard_rows.append(["📣 Marketing / Ads", "", "", "", "", "", "", ""])
for cat in sorted(marketing_ads.keys()):
    txns, total = marketing_ads[cat]
    name = cat.replace('📣 Marketing (', '').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "Marketing Subtotal", total_marketing])

# Operations
dashboard_rows.append(["🏢 Operations", "", "", "", "", "", "", ""])
for cat in sorted(operations.keys()):
    txns, total = operations[cat]
    name = cat.replace('🏢 Operations (', '').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "Operations Subtotal", total_operations])

# Insurance
dashboard_rows.append(["🛡️ Insurance", "", "", "", "", "", "", ""])
for cat in sorted(insurance.keys()):
    txns, total = insurance[cat]
    name = cat.replace('🛡️ Insurance (', '').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "Insurance Subtotal", total_insurance])

# Debt Payments
dashboard_rows.append(["💳 Debt Payments", "", "", "", "", "", "", ""])
for cat in sorted(debt_payments.keys()):
    txns, total = debt_payments[cat]
    name = cat.replace('💳 Debt (', '').replace('💳 CC Fee', 'CC Fee').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "Debt Subtotal", total_debt])

# CC Interest
if cc_interest:
    dashboard_rows.append(["💰 CC Interest (Business)", "", "", "", "", "", "", ""])
    for cat in sorted(cc_interest.keys()):
        txns, total = cc_interest[cat]
        dashboard_rows.append(["", "Biz CC 0678 Interest", len(txns), total])
    dashboard_rows.append(["", "", "CC Interest Subtotal", total_cc_interest_biz])

dashboard_rows.append(["", "", "TOTAL BUSINESS EXPENSES", total_biz_expenses])
dashboard_rows.append([""])

# ── SECTION C: Personal Expenses ──
dashboard_rows.append(["👤 SECTION C: PERSONAL EXPENSES", "", "", "", "", "", "", ""])
dashboard_rows.append(["Category", "Detail", "Count", "Total", "", "", "", ""])

# ATM/Cash
dashboard_rows.append(["🏧 ATM / Cash / FX Fees", "", "", "", "", "", "", ""])
for cat in sorted(atm_cash.keys()):
    txns, total = atm_cash[cat]
    name = cat.replace('🏧 ', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "ATM/Cash Subtotal", total_atm])

# Investments
dashboard_rows.append(["📈 Investments", "", "", "", "", "", "", ""])
for cat in sorted(investments.keys()):
    txns, total = investments[cat]
    name = cat.replace('📈 Investments (', '').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "Investment Subtotal", total_investments])

# Travel
if travel:
    dashboard_rows.append(["✈️ Travel", "", "", "", "", "", "", ""])
    for cat in sorted(travel.keys()):
        txns, total = travel[cat]
        name = cat.replace('✈️ Travel (', '').replace(')', '')
        dashboard_rows.append(["", name, len(txns), total])
    dashboard_rows.append(["", "", "Travel Subtotal", total_travel])

# Subscriptions
dashboard_rows.append(["📺 Subscriptions", "", "", "", "", "", "", ""])
for cat in sorted(subscriptions.keys()):
    txns, total = subscriptions[cat]
    name = cat.replace('📺 Subscriptions (', '').replace(')', '')
    dashboard_rows.append(["", name, len(txns), total])
dashboard_rows.append(["", "", "Subscriptions Subtotal", total_subs])

# Student Loan
if student_loan:
    dashboard_rows.append(["🎓 Student Loan", "", "", "", "", "", "", ""])
    for cat in sorted(student_loan.keys()):
        txns, total = student_loan[cat]
        dashboard_rows.append(["", "Dept of Education", len(txns), total])
    dashboard_rows.append(["", "", "Student Loan Subtotal", total_student])

# CC Payments (Personal)
if personal_cc_payments:
    dashboard_rows.append(["💳 CC Payments", "", "", "", "", "", "", ""])
    cc_pay_txns = [t for t in personal_0068_jan if t['cat_type'] == 'CC Payment']
    for txn in cc_pay_txns:
        dashboard_rows.append(["", txn['vendor'], txn['date_str'], txn['amount']])
    dashboard_rows.append(["", "", "CC Payment Subtotal", personal_cc_payments])

# Personal CC Interest
if personal_cc_interest:
    dashboard_rows.append(["💰 CC Interest (Personal)", "", "", "", "", "", "", ""])
    for cat in sorted(personal_cc_interest.keys()):
        txns, total = personal_cc_interest[cat]
        dashboard_rows.append(["", "Sapphire 4252 Interest", len(txns), total])
    dashboard_rows.append(["", "", "Personal CC Interest Subtotal", total_personal_cc_interest])

# CC Fees
if personal_cc_fee:
    dashboard_rows.append(["💳 CC Fees", "", "", "", "", "", "", ""])
    for cat in sorted(personal_cc_fee.keys()):
        txns, total = personal_cc_fee[cat]
        dashboard_rows.append(["", "Sapphire Annual Fee", len(txns), total])
    dashboard_rows.append(["", "", "CC Fee Subtotal", total_personal_cc_fee])

# Living
if living:
    dashboard_rows.append(["🏠 Living / Local", "", "", "", "", "", "", ""])
    for cat in sorted(living.keys()):
        txns, total = living[cat]
        dashboard_rows.append(["", cat.replace('🏠 ', ''), len(txns), total])
    dashboard_rows.append(["", "", "Living Subtotal", total_living])

dashboard_rows.append([""])

# ── SECTION D: Key Metrics ──
dashboard_rows.append(["📈 SECTION D: KEY METRICS", "", "", "", "", "", "", ""])
dashboard_rows.append(["Metric", "", "", "Value", "", "", "", ""])
dashboard_rows.append(["Business Income", "", "", total_biz_income])
dashboard_rows.append(["Business Expenses", "", "", total_biz_expenses])
dashboard_rows.append(["Business Profit", "", "", biz_profit])
dashboard_rows.append(["Profit Margin", "", "", f"{profit_margin:.1f}%"])
dashboard_rows.append([""])
dashboard_rows.append(["⭐ Total Meta Ads Spend (ALL CARDS)", "", "", total_meta_ads])
dashboard_rows.append(["  → Business 4991", "", "", sum(t['amount'] for t in business_4991_jan if '📣 Marketing (Meta Ads)' == t.get('category', ''))])
dashboard_rows.append(["  → Biz CC 0678", "", "", sum(t['amount'] for t in biz_cc_0678_jan if 'Meta Ads' in t.get('category', ''))])
dashboard_rows.append(["  → Sapphire 4252 ⚠️", "", "", sum(t['amount'] for t in sapphire_4252_jan if 'Meta Ads' in t.get('category', ''))])
dashboard_rows.append([""])
dashboard_rows.append(["Daily Burn Rate (Biz Expenses)", "", "", round(daily_burn, 2)])
dashboard_rows.append(["ATM + FX Fees Total (Personal)", "", "", atm_fees])
dashboard_rows.append(["ATM + FX Fees Total (Business)", "", "", biz_atm_fees])
dashboard_rows.append(["Investment Total (Robinhood + Acorns)", "", "", total_investments])
dashboard_rows.append(["CC Interest Total (All Cards)", "", "", all_cc_interest])
dashboard_rows.append([""])

# ── SECTION E: Money Flow ──
dashboard_rows.append(["🔄 SECTION E: MONEY FLOW", "", "", "", "", "", "", ""])
dashboard_rows.append(["Flow", "", "Count", "Total", "", "", "", ""])
dashboard_rows.append(["Biz 4991 → Personal 0068", "", len([t for t in transfers_biz_to_personal if t['amount'] < 0]), f"-${total_biz_to_personal:,.2f}"])
dashboard_rows.append(["Personal 0068 → Biz 4991", "", len([t for t in transfers_personal_to_biz if t['amount'] < 0]), f"-${total_personal_to_biz:,.2f}"])
dashboard_rows.append(["Personal → Savings 7036", "", len([t for t in transfers_savings if t['amount'] < 0]), f"-${total_savings_out:,.2f}"])
dashboard_rows.append(["Savings 7036 → Personal", "", len([t for t in transfers_savings if t['amount'] > 0]), f"${total_savings_in:,.2f}"])

# CC Payments from biz checking
biz_cc_pay_txns = [t for t in business_4991_jan if t['cat_type'] == 'CC Payment']
dashboard_rows.append(["Biz CC Payments from 4991", "", len(biz_cc_pay_txns), biz_cc_payments])
# Zelle out
zelle_out = [t for t in business_4991_jan if t['cat_type'] == 'Transfer' and 'Zelle Out' in t.get('category', '')]
if zelle_out:
    dashboard_rows.append(["Zelle Outbound", "", len(zelle_out), sum(t['amount'] for t in zelle_out)])
dashboard_rows.append([""])

# ── SECTION F: Action Items ──
dashboard_rows.append(["📝 SECTION F: ACTION ITEMS", "", "", "", "", "", "", ""])
dashboard_rows.append(["#", "Item", "Status", "Notes", "", "", "", ""])
dashboard_rows.append(["1", "Meta Ads on Sapphire 4252 — move to business card", "⚠️", f"${abs(sum(t['amount'] for t in sapphire_4252_jan if 'Meta Ads' in t.get('category', ''))):,.2f} on personal card"])
dashboard_rows.append(["2", "Review ATM withdrawal frequency — reduce fees", "", f"${abs(atm_fees):,.2f} in ATM/FX fees this month"])
dashboard_rows.append(["3", "Investment vs CC debt review", "", f"${abs(total_investments):,.2f} invested while carrying CC debt"])
dashboard_rows.append(["4", "", "", ""])
dashboard_rows.append(["5", "", "", ""])
dashboard_rows.append(["6", "", "", ""])

# ── Write Dashboard ───────────────────────────────────────────────────────────
print("  Writing dashboard data...")

# ── Build Transaction Tabs ────────────────────────────────────────────────────
def build_txn_tab(txns, tab_name):
    """Build sorted transaction data for a tab"""
    rows = [["Date", "Vendor", "Category", "Amount", "Balance", "Notes"]]
    for txn in sorted(txns, key=lambda t: t['date']):
        notes = ""
        if 'Meta Ads' in txn.get('category', '') and 'Personal' in txn.get('account', ''):
            notes = "⚠️ Should be on biz card"
        rows.append([
            txn['date_str'],
            txn['vendor'],
            txn.get('category', txn.get('cat_type', '')),
            txn['amount'],
            txn.get('balance', '') if txn.get('balance') is not None else '',
            notes
        ])
    return rows

biz_rows = build_txn_tab(business_4991_jan, "Business 4991")
personal_rows = build_txn_tab(personal_0068_jan, "Personal 0068")
cc_rows = build_txn_tab(biz_cc_0678_jan, "Biz CC 0678")
sapphire_rows = build_txn_tab(sapphire_4252_jan, "Sapphire 4252")

# ── Raw Data Tab ──────────────────────────────────────────────────────────────
raw_rows = [["Account", "Date", "Description", "Vendor", "Category", "Amount", "Balance", "Type"]]

for txn in sorted(personal_0068 + business_4991 + biz_cc_0678 + sapphire_4252, key=lambda t: t['date']):
    raw_rows.append([
        txn['account'],
        txn['date_str'],
        txn['description'][:100],
        txn.get('vendor', ''),
        txn.get('category', ''),
        txn['amount'],
        txn.get('balance', '') if txn.get('balance') is not None else '',
        txn.get('txn_type', txn.get('cc_type', ''))
    ])

# ── Write All Data ────────────────────────────────────────────────────────────
print("  Writing all tab data...")

batch_write([
    ("'📊 Dashboard'!A1", dashboard_rows),
    ("'💼 Business 4991'!A1", biz_rows),
    ("'👤 Personal 0068'!A1", personal_rows),
    ("'💳 Biz CC 0678'!A1", cc_rows),
    ("'💎 Sapphire 4252'!A1", sapphire_rows),
    ("'📦 Raw Data'!A1", raw_rows),
])

# ── Formatting ────────────────────────────────────────────────────────────────
print("  Applying formatting...")

def cell_format(sheet_id, start_row, end_row, start_col, end_col, bg=None, fg=None, bold=False, font_size=None, h_align=None, num_format=None):
    """Build a repeatCell request"""
    fmt = {"textFormat": {}}
    if bg:
        fmt["backgroundColor"] = bg
    if fg:
        fmt["textFormat"]["foregroundColor"] = fg
    if bold:
        fmt["textFormat"]["bold"] = True
    if font_size:
        fmt["textFormat"]["fontSize"] = font_size
    if h_align:
        fmt["horizontalAlignment"] = h_align
    if num_format:
        fmt["numberFormat"] = num_format
    
    fields = []
    if bg: fields.append("userEnteredFormat.backgroundColor")
    if fg or bold or font_size: fields.append("userEnteredFormat.textFormat")
    if h_align: fields.append("userEnteredFormat.horizontalAlignment")
    if num_format: fields.append("userEnteredFormat.numberFormat")
    
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "cell": {"userEnteredFormat": fmt},
            "fields": ",".join(fields)
        }
    }

def col_width(sheet_id, col, width):
    return {
        "updateDimensionProperties": {
            "range": {"sheetId": sheet_id, "dimension": "COLUMNS", "startIndex": col, "endIndex": col + 1},
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    }

def merge_cells(sheet_id, start_row, end_row, start_col, end_col):
    return {
        "mergeCells": {
            "range": {"sheetId": sheet_id, "startRowIndex": start_row, "endRowIndex": end_row, "startColumnIndex": start_col, "endColumnIndex": end_col},
            "mergeType": "MERGE_ALL"
        }
    }

def border_range(sheet_id, start_row, end_row, start_col, end_col, style="SOLID", color=None):
    if not color:
        color = BORDER_GRAY
    border = {"style": style, "color": color}
    return {
        "updateBorders": {
            "range": {"sheetId": sheet_id, "startRowIndex": start_row, "endRowIndex": end_row, "startColumnIndex": start_col, "endColumnIndex": end_col},
            "top": border, "bottom": border, "left": border, "right": border,
            "innerHorizontal": border, "innerVertical": border
        }
    }

format_requests = []

# ── Dashboard Formatting ─────────────────────────────────────────────────────
# Title row
format_requests.append(merge_cells(DASH_ID, 0, 1, 0, 8))
format_requests.append(cell_format(DASH_ID, 0, 1, 0, 8, bg=NAVY, fg=WHITE, bold=True, font_size=16))

# Find section header rows
section_rows = []
subtotal_rows = []
total_rows = []

for i, row in enumerate(dashboard_rows):
    if not row or not row[0]:
        continue
    text = str(row[0])
    if text.startswith(('💰 SECTION', '📊 SECTION', '👤 SECTION', '📈 SECTION', '🔄 SECTION', '📝 SECTION')):
        section_rows.append(i)
    elif len(row) > 2 and isinstance(row[2], str) and 'Subtotal' in str(row[2]):
        subtotal_rows.append(i)
    elif len(row) > 2 and isinstance(row[2], str) and 'TOTAL' in str(row[2]):
        total_rows.append(i)

# Section headers: merge and navy background
for r in section_rows:
    format_requests.append(merge_cells(DASH_ID, r, r + 1, 0, 8))
    format_requests.append(cell_format(DASH_ID, r, r + 1, 0, 8, bg=MED_BLUE, fg=WHITE, bold=True, font_size=12))

# Sub-headers (Source, Category, Metric rows right after section)
for r in section_rows:
    if r + 1 < len(dashboard_rows) and dashboard_rows[r + 1] and dashboard_rows[r + 1][0] in ('Source', 'Category', 'Metric', 'Flow', '#'):
        format_requests.append(cell_format(DASH_ID, r + 1, r + 2, 0, 8, bg=NAVY, fg=WHITE, bold=True, font_size=10))

# Subtotal rows
for r in subtotal_rows:
    format_requests.append(cell_format(DASH_ID, r, r + 1, 0, 8, bg=ALT_ROW, bold=True))

# Total rows
for r in total_rows:
    format_requests.append(cell_format(DASH_ID, r, r + 1, 0, 8, bg=TOTAL_BG, bold=True, font_size=11))

# Key metric highlight rows
for i, row in enumerate(dashboard_rows):
    if row and len(row) > 0:
        text = str(row[0])
        if text.startswith('⭐'):
            format_requests.append(cell_format(DASH_ID, i, i + 1, 0, 8, bg=rgb("#FFF3E0"), bold=True, font_size=11))
        if text == 'Business Profit':
            format_requests.append(cell_format(DASH_ID, i, i + 1, 0, 8, bg=LIGHT_GREEN, bold=True, font_size=11))
        if text == 'Profit Margin':
            format_requests.append(cell_format(DASH_ID, i, i + 1, 0, 8, bg=LIGHT_GREEN, bold=True))

# Category sub-headers (📱, 📣, etc.)
for i, row in enumerate(dashboard_rows):
    if row and len(row) > 0:
        text = str(row[0])
        if text and text[0] in '📱📣🏢🛡💳💰🏧📈✈📺🎓🏠' and 'SECTION' not in text:
            format_requests.append(cell_format(DASH_ID, i, i + 1, 0, 8, bg=rgb("#ECEFF1"), bold=True))

# Dashboard column widths
format_requests.append(col_width(DASH_ID, 0, 280))
format_requests.append(col_width(DASH_ID, 1, 250))
format_requests.append(col_width(DASH_ID, 2, 200))
format_requests.append(col_width(DASH_ID, 3, 150))
format_requests.append(col_width(DASH_ID, 4, 80))
format_requests.append(col_width(DASH_ID, 5, 80))
format_requests.append(col_width(DASH_ID, 6, 80))
format_requests.append(col_width(DASH_ID, 7, 80))

# Amount column (D) currency format on dashboard
format_requests.append(cell_format(DASH_ID, 0, len(dashboard_rows), 3, 4, 
    num_format={"type": "CURRENCY", "pattern": "$#,##0.00;($#,##0.00)"},
    h_align="RIGHT"))

# ── Transaction Tab Formatting ────────────────────────────────────────────────
for sheet_id, rows, tab_name in [
    (BIZ_ID, biz_rows, "Business 4991"),
    (PERS_ID, personal_rows, "Personal 0068"),
    (CC_ID, cc_rows, "Biz CC 0678"),
    (SAPH_ID, sapphire_rows, "Sapphire 4252"),
]:
    # Header row
    format_requests.append(cell_format(sheet_id, 0, 1, 0, 6, bg=NAVY, fg=WHITE, bold=True, font_size=11))
    
    # Column widths
    format_requests.append(col_width(sheet_id, 0, 110))  # Date
    format_requests.append(col_width(sheet_id, 1, 250))  # Vendor
    format_requests.append(col_width(sheet_id, 2, 280))  # Category
    format_requests.append(col_width(sheet_id, 3, 130))  # Amount
    format_requests.append(col_width(sheet_id, 4, 130))  # Balance
    format_requests.append(col_width(sheet_id, 5, 250))  # Notes
    
    # Amount column currency format
    format_requests.append(cell_format(sheet_id, 0, len(rows), 3, 4,
        num_format={"type": "CURRENCY", "pattern": "$#,##0.00;($#,##0.00)"},
        h_align="RIGHT"))
    
    # Balance column currency format
    format_requests.append(cell_format(sheet_id, 0, len(rows), 4, 5,
        num_format={"type": "CURRENCY", "pattern": "$#,##0.00"},
        h_align="RIGHT"))
    
    # Color-code rows by type
    for i in range(1, len(rows)):
        row = rows[i]
        cat = str(row[2]) if len(row) > 2 else ''
        amount = row[3] if len(row) > 3 else 0
        
        if 'Income' in cat or 'Revenue' in cat:
            format_requests.append(cell_format(sheet_id, i, i + 1, 0, 6, bg=LIGHT_GREEN))
        elif 'Transfer' in cat or 'CC Payment' in cat:
            format_requests.append(cell_format(sheet_id, i, i + 1, 0, 6, bg=LIGHT_GRAY))
        elif isinstance(amount, (int, float)) and amount < 0:
            # Alternate white and light gray for expense rows
            if i % 2 == 0:
                format_requests.append(cell_format(sheet_id, i, i + 1, 0, 6, bg=ALT_ROW))
    
    # Red text for negative amounts
    format_requests.append({
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": len(rows), "startColumnIndex": 3, "endColumnIndex": 4}],
                "booleanRule": {
                    "condition": {"type": "NUMBER_LESS", "values": [{"userEnteredValue": "0"}]},
                    "format": {"textFormat": {"foregroundColor": RED_TEXT}}
                }
            },
            "index": 0
        }
    })
    
    # Green text for positive amounts
    format_requests.append({
        "addConditionalFormatRule": {
            "rule": {
                "ranges": [{"sheetId": sheet_id, "startRowIndex": 1, "endRowIndex": len(rows), "startColumnIndex": 3, "endColumnIndex": 4}],
                "booleanRule": {
                    "condition": {"type": "NUMBER_GREATER", "values": [{"userEnteredValue": "0"}]},
                    "format": {"textFormat": {"foregroundColor": GREEN_TEXT}}
                }
            },
            "index": 0
        }
    })
    
    # Light borders
    format_requests.append(border_range(sheet_id, 0, len(rows), 0, 6))

# ── Raw Data Tab Formatting ──────────────────────────────────────────────────
format_requests.append(cell_format(RAW_ID, 0, 1, 0, 8, bg=NAVY, fg=WHITE, bold=True))
format_requests.append(col_width(RAW_ID, 0, 130))
format_requests.append(col_width(RAW_ID, 1, 100))
format_requests.append(col_width(RAW_ID, 2, 350))
format_requests.append(col_width(RAW_ID, 3, 200))
format_requests.append(col_width(RAW_ID, 4, 250))
format_requests.append(col_width(RAW_ID, 5, 120))
format_requests.append(col_width(RAW_ID, 6, 120))
format_requests.append(col_width(RAW_ID, 7, 120))

# Currency format for amount and balance in raw data
format_requests.append(cell_format(RAW_ID, 0, len(raw_rows), 5, 6,
    num_format={"type": "CURRENCY", "pattern": "$#,##0.00;($#,##0.00)"},
    h_align="RIGHT"))
format_requests.append(cell_format(RAW_ID, 0, len(raw_rows), 6, 7,
    num_format={"type": "CURRENCY", "pattern": "$#,##0.00"},
    h_align="RIGHT"))

# Alternating rows for raw data
for i in range(1, min(len(raw_rows), 400)):  # limit to avoid too many requests
    if i % 2 == 0:
        format_requests.append(cell_format(RAW_ID, i, i + 1, 0, 8, bg=ALT_ROW))

# Dashboard borders
format_requests.append(border_range(DASH_ID, 0, len(dashboard_rows), 0, 4))

# ── Apply all formatting ─────────────────────────────────────────────────────
# Split into chunks to avoid API limits
CHUNK = 500
for i in range(0, len(format_requests), CHUNK):
    chunk = format_requests[i:i+CHUNK]
    print(f"    Applying format batch {i//CHUNK + 1} ({len(chunk)} requests)...")
    batch_format(chunk)

# ── Share with mark@kuriosbrand.com ──────────────────────────────────────────
print("  Sharing with mark@kuriosbrand.com...")

share_body = {
    "role": "writer",
    "type": "user",
    "emailAddress": "mark@kuriosbrand.com"
}
r = requests.post(
    f"https://www.googleapis.com/drive/v3/files/{SPREADSHEET_ID}/permissions",
    headers=HEADERS,
    json=share_body,
    params={"sendNotificationEmail": "false"}
)
r.raise_for_status()

print(f"\n✅ COMPLETE!")
print(f"📊 Spreadsheet URL: {SPREADSHEET_URL}")
print(f"📁 Sheet ID saved to: /home/ec2-user/clawd/data/jan-2026-sheet-id.txt")
print(f"\n── Summary ──")
print(f"  Business Income:  ${total_biz_income:,.2f}")
print(f"  Business Expenses: ${total_biz_expenses:,.2f}")
print(f"  Business Profit:  ${biz_profit:,.2f} ({profit_margin:.1f}% margin)")
print(f"  Meta Ads Total:   ${total_meta_ads:,.2f}")
print(f"  CC Interest Total: ${all_cc_interest:,.2f}")
print(f"  Personal Expenses: ${total_personal_expenses:,.2f}")
print(f"  Shared with: mark@kuriosbrand.com (editor)")
