#!/usr/bin/env python3
"""
Build KuriosBrand LLC — Financial Statements (All Time) Google Sheet.
CPA-ready, professional formatting, no emojis.
"""

import csv
import json
import requests
import sys
import os
from datetime import datetime
from collections import defaultdict
import re
import time

# ─── Config ───
TOKEN_PATH = os.path.expanduser("~/.config/gcal-pro/token.json")
FOLDER_ID = "1XlNibgutZc0eVrI6tkgexTA3RusGepwX"
SHEET_TITLE = "KuriosBrand LLC — Financial Statements (All Time)"
CSV_DIR = "/home/ec2-user/clawd/data/chase-exports"

# ─── OAuth ───
def refresh_token():
    with open(TOKEN_PATH) as f:
        t = json.load(f)
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": t["client_id"],
        "client_secret": t["client_secret"],
        "refresh_token": t["refresh_token"],
        "grant_type": "refresh_token"
    })
    r.raise_for_status()
    return r.json()["access_token"]

# ─── CSV Parsing ───
def parse_business_csv(path):
    """Parse 4991 business checking CSV"""
    txns = []
    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amt = float(row['Amount'].replace(',',''))
                date = datetime.strptime(row['Posting Date'].strip(), '%m/%d/%Y')
                txns.append({
                    'date': date,
                    'month': date.strftime('%Y-%m'),
                    'description': row['Description'].strip(),
                    'amount': amt,
                    'type': row['Type'].strip(),
                    'detail': row['Details'].strip(),
                    'source': '4991'
                })
            except (ValueError, KeyError) as e:
                continue
    return txns

def parse_cc_csv(path, card_id):
    """Parse credit card CSV (0678 or 4252)"""
    txns = []
    with open(path, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                amt = float(row['Amount'].replace(',',''))
                date = datetime.strptime(row['Post Date'].strip(), '%m/%d/%Y')
                txns.append({
                    'date': date,
                    'month': date.strftime('%Y-%m'),
                    'description': row['Description'].strip(),
                    'amount': amt,
                    'type': row.get('Type','').strip(),
                    'category': row.get('Category','').strip(),
                    'detail': 'DEBIT' if amt < 0 else 'CREDIT',
                    'source': card_id
                })
            except (ValueError, KeyError):
                continue
    return txns

# ─── Transaction Classification ───
def classify_transaction(txn):
    """Classify a transaction into GL account categories.
    Returns (gl_code, category_name, is_revenue, is_cogs, is_opex, is_transfer)
    """
    desc = txn['description'].upper()
    raw_desc = txn['description']
    amt = txn['amount']
    typ = txn.get('type', '').upper()
    source = txn['source']
    
    # Skip transfers between own accounts
    if 'ACCT_XFER' in typ or ('ONLINE TRANSFER' in desc and ('CHK' in desc or 'SAV' in desc)):
        return ('7000', "Owner's Draws / Transfers", False, False, False, True)
    
    # CC Payments - skip (just debt movement)
    if 'PAYMENT' in typ or 'PAYMENT THANK YOU' in desc or 'AUTOMATIC PAYMENT' in desc:
        return (None, 'CC Payment', False, False, False, True)
    if 'LOAN_PMT' in typ or 'Payment to Chase card' in raw_desc:
        return (None, 'CC Payment', False, False, False, True)
    
    # FIRST: Stripe Capital Loan disbursement (NOT revenue!) - must check before general Stripe
    if 'STRIPE' in desc and amt >= 4000 and amt <= 4300:
        return ('2200', 'Stripe Capital Loan', False, False, False, True)
    
    # Affirm payments via Stripe ACH (NOT revenue - these are loan debits)
    if 'AFFIRM' in desc:
        if amt < 0:
            return ('6110', 'Loan Repayment', False, False, True, False)
        else:
            return (None, 'Affirm Refund', False, False, False, True)
    
    # Credit Strong payments received (not revenue - loan related)
    if 'CREDIT STRONG' in desc and amt > 0:
        return (None, 'Credit Strong Received', False, False, False, True)
    
    # Statement credits (not revenue)
    if 'STATEMENT CREDIT' in desc:
        return (None, 'Statement Credit', False, False, False, True)
    
    # Revenue: Stripe deposits (normal business revenue)
    if 'STRIPE' in desc and amt > 0:
        return ('4000', 'Service Revenue', True, False, False, False)
    
    # Revenue: Real Time Payment from Stripe
    if 'REAL TIME PAYMENT' in desc and 'STRIPE' in desc and amt > 0:
        return ('4000', 'Service Revenue', True, False, False, False)
    
    # Revenue: Zelle payments received (business) - include ALL Zelle to business account
    if source == '4991' and amt > 0:
        if 'ZELLE' in desc or 'PARTNERFI_TO_CHASE' in typ or 'QUICKPAY_CREDIT' in typ:
            return ('4000', 'Service Revenue', True, False, False, False)
    
    # Wells Fargo transfer (not revenue)
    if 'WELLS FARGO' in desc and amt > 0:
        return (None, 'Transfer', False, False, False, True)
    
    # ODP Transfer from savings (not revenue)
    if 'ODP TRANSFER' in desc and amt > 0:
        return (None, 'Transfer', False, False, False, True)
    
    # COGS: Meta/Facebook ads (on both 4991 and 0678)
    if ('FACEBK' in desc or 'FACEBOOK' in desc) and amt < 0:
        return ('5000', 'Advertising - Meta/Facebook', False, True, False, False)
    
    # COGS: Google Ads (but NOT Google Workspace, Google One, Google Cloud)
    if 'GOOGLE' in desc and 'ADS' in desc and amt < 0:
        return ('5010', 'Advertising - Google Ads', False, True, False, False)
    
    # OpEx: SaaS & Software
    saas_keywords = ['CHATGPT', 'OPENAI', 'CLAUDE', 'ANTHROPIC', 'LOVABLE', 'CURSOR',
                     'FLOWITH', 'APIFY', 'PERPLEXITY', 'DESCRIPT', 'CANVA',
                     'INVIDEO', 'HIGGSFIELD', 'IDEOGRAM', 'SUPERMEMORY',
                     '10WEB', 'UNBOUNCE', 'INSTANTLY', 'LEMLIST', 'REVID',
                     'SIGNALS', 'TRADINGVIEW', 'MYFICO', 'COBRAND',
                     'SERPEMPIRE', 'INDEXSY', 'BRAVE.COM', 'WEBSHARE',
                     'HOSTMYAPPL', 'DATAFORSEO', 'EXA.AI', 'RAPIDURLINDEXER',
                     'GUMROAD', 'MUSIXMATCH', 'NUROAUDIO', 'SWEETWATER',
                     'PATREON', 'ELECTIVE']
    for kw in saas_keywords:
        if kw in desc and amt < 0:
            return ('6000', 'SaaS & Software', False, False, True, False)
    
    # OpEx: HighLevel
    if 'HIGHLEVEL' in desc or 'GOHIGHLEVEL' in desc:
        if amt < 0:
            return ('6000', 'SaaS & Software', False, False, True, False)
    
    # OpEx: SEO Services
    if 'LOCALRANK' in desc and amt < 0:
        return ('6010', 'SEO Services & Tools', False, False, True, False)
    if 'SEMRUSH' in desc and amt < 0:
        return ('6010', 'SEO Services & Tools', False, False, True, False)
    
    # OpEx: Google Workspace / One / Cloud (NOT ads)
    if 'GOOGLE' in desc and amt < 0:
        if 'WORKSPACE' in desc or 'GSUITE' in desc or 'CLOUD' in desc or 'GOOGLE ONE' in desc or 'Google One' in raw_desc:
            return ('6000', 'SaaS & Software', False, False, True, False)
    
    # Skool (education)
    if 'SKOOL' in desc and amt < 0:
        return ('6140', 'Education & Training', False, False, True, False)
    
    # OpEx: Hosting & Domains  
    if 'NAMECHEAP' in desc or 'NAME-CHEAP' in desc:
        if amt < 0:
            return ('6130', 'Domains & Hosting', False, False, True, False)
    if 'CLOUDFLARE' in desc and amt < 0:
        return ('6130', 'Domains & Hosting', False, False, True, False)
    if 'HOSTINGER' in desc and amt < 0:
        return ('6130', 'Domains & Hosting', False, False, True, False)
    if 'HYONIX' in desc and amt < 0:
        return ('6130', 'Domains & Hosting', False, False, True, False)
    
    # OpEx: Coworking/Office
    if 'REGUS' in desc and amt < 0:
        return ('6020', 'Office & Coworking', False, False, True, False)
    if 'ANYTIME MAILBOX' in desc or 'TRAVELINGMAILBOX' in desc:
        if amt < 0:
            return ('6020', 'Office & Coworking', False, False, True, False)
    
    # OpEx: Telecom
    if 'TMOBILE' in desc or 'T-MOBILE' in desc:
        if amt < 0:
            return ('6030', 'Telecommunications', False, False, True, False)
    if 'SPECTRUM' in desc and amt < 0:
        return ('6040', 'Internet Service', False, False, True, False)
    if 'BOOST MOBILE' in desc and amt < 0:
        return ('6030', 'Telecommunications', False, False, True, False)
    if 'AIRALO' in desc and amt < 0:
        return ('6030', 'Telecommunications', False, False, True, False)
    
    # OpEx: Insurance
    if 'SAFETYWING' in desc or 'TRIWEST' in desc or 'TRICARE' in desc:
        if amt < 0:
            return ('6080', 'Insurance', False, False, True, False)
    
    # OpEx: Bank Fees
    if 'SERVICE FEE' in desc or 'STOP PAYMENT FEE' in desc:
        return ('6060', 'Bank Fees & Interest', False, False, True, False)
    if 'FEE_TRANSACTION' in typ and amt < 0:
        return ('6060', 'Bank Fees & Interest', False, False, True, False)
    if 'PURCHASE INTEREST' in desc or 'INTEREST CHARGE' in desc:
        return ('6070', 'CC Interest', False, False, True, False)
    if 'ANNUAL MEMBERSHIP FEE' in desc:
        return ('6060', 'Bank Fees & Interest', False, False, True, False)
    if 'FOREIGN EXCHANGE' in desc or 'FOREIGN TRANSACTION' in desc:
        return ('6060', 'Bank Fees & Interest', False, False, True, False)
    
    # OpEx: Apple services
    if 'APPLE' in desc and amt < 0:
        return ('6000', 'SaaS & Software', False, False, True, False)
    
    # OpEx: Professional services
    if 'HARBOR COMPLIANCE' in desc and amt < 0:
        return ('6050', 'Professional Services', False, False, True, False)
    if 'WI DFI' in desc and amt < 0:
        return ('6050', 'Professional Services', False, False, True, False)
    
    # OpEx: Travel (Business)
    if 'SAFETYWING' not in desc and ('NordVPN' in desc.lower() or 'NORD*VPN' in desc):
        if amt < 0:
            return ('6000', 'SaaS & Software', False, False, True, False)
    
    # OpEx: Contractors
    if 'WISE' in desc and 'KURIOSBRAND' in desc:
        if amt < 0:
            return ('6120', 'Contractor Labor', False, False, True, False)
    if 'ONLINEJOBSPH' in desc and amt < 0:
        return ('6120', 'Contractor Labor', False, False, True, False)
    if 'PAYPAL' in desc and 'IOTSOLUTION' in desc and amt < 0:
        return ('6120', 'Contractor Labor', False, False, True, False)
    
    # Loan payments
    if 'AFFIRM' in desc and amt < 0:
        return ('6110', 'Loan Repayment', False, False, True, False)
    if 'SELF LENDER' in desc and amt < 0:
        return ('6110', 'Loan Repayment', False, False, True, False)
    if 'CREDIT STRONG' in desc and amt < 0:
        return ('6110', 'Loan Repayment', False, False, True, False)
    
    # X Corp
    if 'X CORP' in desc and amt < 0:
        return ('6000', 'SaaS & Software', False, False, True, False)
    
    # Spotify
    if 'SPOTIFY' in desc and amt < 0:
        return ('6000', 'SaaS & Software', False, False, True, False)
    
    # META WAVE
    if 'META WAVE' in desc and amt < 0:
        return ('6000', 'SaaS & Software', False, False, True, False)
    
    # ATM withdrawals from business account
    if 'ATM' in desc and source == '4991' and amt < 0:
        return ('7000', "Owner's Draws / Transfers", False, False, False, True)
    
    # Zelle payments out
    if ('CHASE_TO_PARTNERFI' in typ or 'QUICKPAY_DEBIT' in typ) and amt < 0:
        return ('6150', 'Miscellaneous', False, False, True, False)
    
    # Chase CC autopay from checking
    if 'CHASE CREDIT CRD' in desc and amt < 0:
        return (None, 'CC Payment', False, False, False, True)
    
    # Catch remaining debits
    if amt < 0 and source in ['4991', '0678']:
        return ('6150', 'Miscellaneous', False, False, True, False)
    
    # Catch remaining credits
    if amt > 0:
        return (None, 'Other Income', False, False, False, True)
    
    return (None, 'Unclassified', False, False, False, True)


def process_all_transactions():
    """Process all CSVs and return classified transactions."""
    biz_txns = parse_business_csv(f"{CSV_DIR}/business-4991-alltime.csv")
    cc_txns = parse_cc_csv(f"{CSV_DIR}/bizcc-0678-alltime.csv", '0678')
    
    all_txns = []
    
    for txn in biz_txns:
        gl, cat, is_rev, is_cogs, is_opex, is_xfer = classify_transaction(txn)
        txn['gl_code'] = gl
        txn['category'] = cat
        txn['is_revenue'] = is_rev
        txn['is_cogs'] = is_cogs
        txn['is_opex'] = is_opex
        txn['is_transfer'] = is_xfer
        all_txns.append(txn)
    
    for txn in cc_txns:
        gl, cat, is_rev, is_cogs, is_opex, is_xfer = classify_transaction(txn)
        txn['gl_code'] = gl
        txn['category'] = cat
        txn['is_revenue'] = is_rev
        txn['is_cogs'] = is_cogs
        txn['is_opex'] = is_opex
        txn['is_transfer'] = is_xfer
        all_txns.append(txn)
    
    return all_txns


def build_monthly_financials(all_txns):
    """Aggregate transactions into monthly financial data."""
    months_data = defaultdict(lambda: {
        'revenue': defaultdict(float),
        'cogs': defaultdict(float),
        'opex': defaultdict(float),
        'total_revenue': 0,
        'total_cogs': 0,
        'total_opex': 0,
        'net_income': 0
    })
    
    for txn in all_txns:
        m = txn['month']
        cat = txn['category']
        amt = txn['amount']
        
        if txn['is_revenue']:
            months_data[m]['revenue'][cat] += amt
            months_data[m]['total_revenue'] += amt
        elif txn['is_cogs']:
            months_data[m]['cogs'][cat] += abs(amt)
            months_data[m]['total_cogs'] += abs(amt)
        elif txn['is_opex']:
            months_data[m]['opex'][cat] += abs(amt)
            months_data[m]['total_opex'] += abs(amt)
    
    for m in months_data:
        d = months_data[m]
        d['net_income'] = d['total_revenue'] - d['total_cogs'] - d['total_opex']
    
    return months_data


# ─── Google Sheets API ───
def sheets_api(token, method, url, json_data=None):
    """Make Sheets API request."""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    if method == 'POST':
        r = requests.post(url, headers=headers, json=json_data)
    elif method == 'PUT':
        r = requests.put(url, headers=headers, json=json_data)
    elif method == 'GET':
        r = requests.get(url, headers=headers)
    else:
        r = requests.request(method, url, headers=headers, json=json_data)
    if r.status_code >= 400:
        print(f"API Error {r.status_code}: {r.text[:500]}")
    r.raise_for_status()
    return r.json()


def create_spreadsheet(token):
    """Create the spreadsheet with all tabs."""
    body = {
        "properties": {
            "title": SHEET_TITLE,
            "locale": "en_US",
            "defaultFormat": {
                "textFormat": {"fontFamily": "Arial", "fontSize": 10}
            }
        },
        "sheets": [
            {"properties": {"title": "Summary", "sheetId": 0, "index": 0}},
            {"properties": {"title": "Chart of Accounts", "sheetId": 1, "index": 1}},
            {"properties": {"title": "Income Statement 2024", "sheetId": 7, "index": 2}},
            {"properties": {"title": "Income Statement 2025", "sheetId": 2, "index": 3}},
            {"properties": {"title": "Income Statement 2026", "sheetId": 3, "index": 4}},
            {"properties": {"title": "Schedule C Summary", "sheetId": 4, "index": 5}},
            {"properties": {"title": "Balance Sheet", "sheetId": 5, "index": 6}},
            {"properties": {"title": "Bank Reconciliation", "sheetId": 6, "index": 7}},
        ]
    }
    
    result = sheets_api(token, 'POST', 'https://sheets.googleapis.com/v4/spreadsheets', body)
    sid = result['spreadsheetId']
    
    # Move to folder
    requests.patch(
        f"https://www.googleapis.com/drive/v3/files/{sid}?addParents={FOLDER_ID}",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    return sid


def batch_update(token, spreadsheet_id, requests_list):
    """Send batchUpdate to Sheets API."""
    if not requests_list:
        return
    # Split into chunks of 500 to avoid API limits
    chunk_size = 500
    for i in range(0, len(requests_list), chunk_size):
        chunk = requests_list[i:i+chunk_size]
        body = {"requests": chunk}
        sheets_api(token, 'POST',
                   f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate',
                   body)
        if i + chunk_size < len(requests_list):
            time.sleep(1)


def update_values(token, spreadsheet_id, range_str, values):
    """Update cell values."""
    body = {
        "range": range_str,
        "majorDimension": "ROWS",
        "values": values
    }
    sheets_api(token, 'PUT',
               f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_str}?valueInputOption=USER_ENTERED',
               body)


# ─── Color/Format Helpers ───
def rgb(r, g, b):
    return {"red": r/255, "green": g/255, "blue": b/255}

DARK_GRAY = rgb(51, 51, 51)  # #333333
WHITE = rgb(255, 255, 255)
LIGHT_GRAY = rgb(243, 243, 243)
LIGHT_BLUE = rgb(232, 237, 245)

def header_format():
    return {
        "backgroundColor": DARK_GRAY,
        "textFormat": {"bold": True, "foregroundColor": WHITE, "fontFamily": "Arial", "fontSize": 10}
    }

def subheader_format():
    return {
        "backgroundColor": LIGHT_GRAY,
        "textFormat": {"bold": True, "fontFamily": "Arial", "fontSize": 10}
    }

def total_format():
    return {
        "backgroundColor": LIGHT_BLUE,
        "textFormat": {"bold": True, "fontFamily": "Arial", "fontSize": 10}
    }

def format_row(sheet_id, row, start_col, end_col, fmt):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row,
                "endRowIndex": row + 1,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "cell": {"userEnteredFormat": fmt},
            "fields": "userEnteredFormat"
        }
    }

def format_range_currency(sheet_id, start_row, end_row, start_col, end_col):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "CURRENCY",
                        "pattern": "$#,##0.00;($#,##0.00)"
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    }

def format_range_pct(sheet_id, start_row, end_row, start_col, end_col):
    return {
        "repeatCell": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": start_row,
                "endRowIndex": end_row,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "cell": {
                "userEnteredFormat": {
                    "numberFormat": {
                        "type": "PERCENT",
                        "pattern": "0.0%"
                    }
                }
            },
            "fields": "userEnteredFormat.numberFormat"
        }
    }

def col_width(sheet_id, col, width):
    return {
        "updateDimensionProperties": {
            "range": {
                "sheetId": sheet_id,
                "dimension": "COLUMNS",
                "startIndex": col,
                "endIndex": col + 1
            },
            "properties": {"pixelSize": width},
            "fields": "pixelSize"
        }
    }

def border_bottom(sheet_id, row, start_col, end_col, style="SOLID"):
    return {
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row,
                "endRowIndex": row + 1,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "bottom": {"style": style, "width": 1, "color": rgb(0,0,0)}
        }
    }

def double_border_bottom(sheet_id, row, start_col, end_col):
    return {
        "updateBorders": {
            "range": {
                "sheetId": sheet_id,
                "startRowIndex": row,
                "endRowIndex": row + 1,
                "startColumnIndex": start_col,
                "endColumnIndex": end_col
            },
            "bottom": {"style": "DOUBLE", "width": 1, "color": rgb(0,0,0)}
        }
    }


# ─── TAB BUILDERS ───

def build_summary_tab(token, sid):
    """Tab 1: Summary"""
    values = [
        ["KuriosBrand LLC — Financial Statements"],
        [""],
        ["Entity Information"],
        ["Entity Name", "KuriosBrand LLC"],
        ["EIN", "To be provided"],
        ["Entity Type", "Single-Member LLC (Schedule C)"],
        ["Owner / Managing Member", "Mark Gundrum"],
        ["Fiscal Year", "Calendar Year (January - December)"],
        ["Accounting Method", "Cash Basis"],
        ["Industry", "Digital Marketing / Lead Generation"],
        ["Business Address", "361 Falls Rd, Grafton, WI"],
        [""],
        ["Accounting Period Covered", "June 2025 - Present"],
        ["Data Source", "Chase Bank Exports (CSV), Stripe API"],
        ["Prepared By", "KuriosBrand Internal Accounting"],
        [""],
        ["Bank Accounts & Financial Institutions"],
        ["Account", "Institution", "Account Number (Last 4)", "Type", "Purpose"],
        ["Business Checking", "Chase", "4991", "Checking", "Primary operating account"],
        ["Business Credit Card", "Chase Ink", "0678", "Credit Card", "Business expenses"],
        ["Personal Checking", "Chase", "0068", "Checking", "Owner personal account"],
        ["Personal Credit Card", "Chase Sapphire", "4252", "Credit Card", "Owner personal CC"],
        ["Payment Processor", "Stripe", "N/A", "Processor", "Client payment processing"],
        ["Tax Savings", "Wells Fargo", "3485", "Savings", "Tax set-aside account"],
        [""],
        ["Notes"],
        ["1. All figures are reported on a cash basis."],
        ["2. Revenue is recognized when deposited to the business checking account."],
        ["3. Personal accounts (0068, 4252) are tracked for owner's draw calculations only."],
        ["4. Stripe deposits include processing fees deducted at source."],
        ["5. Stripe Capital loan of $4,200 disbursed January 23, 2026 (total repayment: $5,035)."],
    ]
    
    update_values(token, sid, "'Summary'!A1", values)
    
    fmt_requests = [
        format_row(0, 0, 0, 6, {"textFormat": {"bold": True, "fontSize": 14, "fontFamily": "Arial"}}),
        format_row(0, 2, 0, 6, header_format()),
        format_row(0, 16, 0, 6, header_format()),
        format_row(0, 17, 0, 6, subheader_format()),
        format_row(0, 25, 0, 6, header_format()),
        col_width(0, 0, 220),
        col_width(0, 1, 200),
        col_width(0, 2, 180),
        col_width(0, 3, 120),
        col_width(0, 4, 250),
    ]
    batch_update(token, sid, fmt_requests)


def build_chart_of_accounts(token, sid):
    """Tab 2: Chart of Accounts"""
    values = [
        ["Chart of Accounts — KuriosBrand LLC"],
        [""],
        ["Account #", "Account Name", "Account Type", "Normal Balance", "Description"],
        ["", "ASSETS", "", "", ""],
        ["1000", "Cash - Business Checking (4991)", "Asset", "Debit", "Primary operating account"],
        ["1010", "Cash - Personal Checking (0068)", "Asset", "Debit", "Owner personal checking"],
        ["1020", "Cash - Savings (7036)", "Asset", "Debit", "Chase savings account"],
        ["1030", "Cash - Tax Account (Wells Fargo)", "Asset", "Debit", "Tax set-aside"],
        ["1100", "Accounts Receivable", "Asset", "Debit", "Outstanding client invoices"],
        ["1200", "Stripe Pending", "Asset", "Debit", "Pending Stripe settlements"],
        ["1300", "Investments - Robinhood", "Asset", "Debit", "Stock investments"],
        ["1310", "Investments - Acorns", "Asset", "Debit", "Micro-investments"],
        ["1320", "Investments - Crypto", "Asset", "Debit", "Cryptocurrency holdings"],
        ["1400", "Business Equity (R&R Assets)", "Asset", "Debit", "Rank & rent website assets"],
        [""],
        ["", "LIABILITIES", "", "", ""],
        ["2000", "Credit Card - Ink Business (0678)", "Liability", "Credit", "Business credit card"],
        ["2010", "Credit Card - Sapphire (4252)", "Liability", "Credit", "Personal credit card"],
        ["2020", "Credit Card - Discover (6820)", "Liability", "Credit", "Personal credit card"],
        ["2100", "Student Loans", "Liability", "Credit", "Federal student loans"],
        ["2200", "Stripe Capital Loan", "Liability", "Credit", "Stripe Capital ($4,200 disbursed 01/23/2026)"],
        [""],
        ["", "EQUITY", "", "", ""],
        ["3000", "Owner's Equity", "Equity", "Credit", "Initial and additional capital contributions"],
        ["3100", "Owner's Draws", "Equity", "Debit", "Distributions to owner"],
        ["3200", "Retained Earnings", "Equity", "Credit", "Accumulated net income"],
        [""],
        ["", "REVENUE", "", "", ""],
        ["4000", "Service Revenue - MVA Lead Gen", "Revenue", "Credit", "Motor vehicle accident lead generation"],
        ["4010", "Service Revenue - Rank & Rent", "Revenue", "Credit", "Rank and rent website revenue"],
        ["4020", "Service Revenue - SEO / Projects", "Revenue", "Credit", "SEO consulting and project work"],
        ["4100", "Stripe Processing Fees (contra)", "Revenue", "Debit", "Stripe fees deducted at source"],
        [""],
        ["", "COST OF GOODS SOLD", "", "", ""],
        ["5000", "Advertising - Meta/Facebook", "COGS", "Debit", "Facebook/Meta ad spend"],
        ["5010", "Advertising - Google Ads", "COGS", "Debit", "Google advertising spend"],
        ["5020", "Lead Generation Tools", "COGS", "Debit", "Direct lead gen tool costs"],
        [""],
        ["", "OPERATING EXPENSES", "", "", ""],
        ["6000", "SaaS & Software", "Expense", "Debit", "Software subscriptions"],
        ["6010", "SEO Services & Tools", "Expense", "Debit", "SEO tools and services"],
        ["6020", "Office & Coworking", "Expense", "Debit", "Coworking, virtual mailbox"],
        ["6030", "Telecommunications", "Expense", "Debit", "Phone, mobile service"],
        ["6040", "Internet Service", "Expense", "Debit", "Internet provider"],
        ["6050", "Professional Services", "Expense", "Debit", "Legal, compliance, accounting"],
        ["6060", "Bank Fees & Interest", "Expense", "Debit", "Bank and processing fees"],
        ["6070", "Credit Card Interest (Business)", "Expense", "Debit", "CC interest charges"],
        ["6080", "Insurance", "Expense", "Debit", "Health, travel, business insurance"],
        ["6090", "Travel (Business)", "Expense", "Debit", "Business travel expenses"],
        ["6100", "Meals (Business, 50%)", "Expense", "Debit", "Business meals (50% deductible)"],
        ["6110", "Loan Repayment", "Expense", "Debit", "Affirm, Self Lender, Credit Strong"],
        ["6120", "Contractor Labor", "Expense", "Debit", "Freelancers, VAs (via Wise, PayPal)"],
        ["6130", "Domains & Hosting", "Expense", "Debit", "Domain registration, web hosting"],
        ["6140", "Education & Training", "Expense", "Debit", "Courses, Skool, training"],
        ["6150", "Miscellaneous", "Expense", "Debit", "Other business expenses"],
        [""],
        ["", "PERSONAL (Not on Schedule C)", "", "", ""],
        ["7000", "Owner's Draws / Transfers", "N/A", "Debit", "Transfers to personal accounts"],
        ["7100", "Personal Living Expenses", "N/A", "Debit", "Personal spending"],
        ["7200", "Personal Investments", "N/A", "Debit", "Robinhood, Acorns, Crypto"],
        ["7300", "Personal Debt Payments", "N/A", "Debit", "Student loans, personal CC"],
    ]
    
    update_values(token, sid, "'Chart of Accounts'!A1", values)
    
    # Format header rows
    section_rows = [3, 15, 22, 27, 33, 37, 55]
    fmt_requests = [
        format_row(1, 0, 0, 5, {"textFormat": {"bold": True, "fontSize": 14, "fontFamily": "Arial"}}),
        format_row(1, 2, 0, 5, header_format()),
        col_width(1, 0, 100),
        col_width(1, 1, 320),
        col_width(1, 2, 100),
        col_width(1, 3, 110),
        col_width(1, 4, 350),
    ]
    for r in section_rows:
        fmt_requests.append(format_row(1, r, 0, 5, subheader_format()))
    
    batch_update(token, sid, fmt_requests)


def build_income_statement(token, sid, months_data, year, sheet_id):
    """Build Income Statement tab for a given year."""
    if year == 2024:
        month_cols = [f'2024-{m:02d}' for m in range(1, 13)]
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        tab_name = 'Income Statement 2024'
    elif year == 2025:
        month_cols = [f'2025-{m:02d}' for m in range(1, 13)]
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        tab_name = 'Income Statement 2025'
    else:
        month_cols = [f'2026-{m:02d}' for m in range(1, 13)]
        month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        tab_name = 'Income Statement 2026'
    
    # Collect all unique category names across months
    rev_cats = set()
    cogs_cats = set()
    opex_cats = set()
    for m in month_cols:
        if m in months_data:
            rev_cats.update(months_data[m]['revenue'].keys())
            cogs_cats.update(months_data[m]['cogs'].keys())
            opex_cats.update(months_data[m]['opex'].keys())
    
    rev_cats = sorted(rev_cats) if rev_cats else ['Service Revenue']
    cogs_cats = sorted(cogs_cats) if cogs_cats else ['Advertising - Meta/Facebook', 'Advertising - Google Ads']
    opex_cats_sorted = [
        'SaaS & Software', 'SEO Services & Tools', 'Office & Coworking',
        'Telecommunications', 'Internet Service', 'Insurance',
        'Bank Fees & Interest', 'CC Interest', 'Professional Services',
        'Contractor Labor', 'Domains & Hosting', 'Loan Repayment',
        'Miscellaneous'
    ]
    opex_cats_final = [c for c in opex_cats_sorted if c in opex_cats]
    remaining = [c for c in opex_cats if c not in opex_cats_final]
    opex_cats_final.extend(sorted(remaining))
    
    # Build data rows
    rows = []
    row_idx = 0
    
    # Title
    rows.append([f"KuriosBrand LLC — Income Statement ({year})"])
    row_idx += 1
    rows.append(["For the Year Ended December 31, " + str(year)])
    row_idx += 1
    rows.append([""])
    row_idx += 1
    
    # Header row
    header = [""] + month_labels + ["TOTAL"]
    rows.append(header)
    header_row = row_idx
    row_idx += 1
    
    # REVENUE section
    rows.append(["REVENUE"] + [""] * (len(month_labels) + 1))
    rev_section_row = row_idx
    row_idx += 1
    
    rev_detail_start = row_idx
    for cat in rev_cats:
        row = [f"  {cat}"]
        total = 0
        for m in month_cols:
            val = months_data.get(m, {}).get('revenue', {}).get(cat, 0)
            row.append(val)
            total += val
        row.append(total)
        rows.append(row)
        row_idx += 1
    rev_detail_end = row_idx
    
    # Total Revenue
    row = ["TOTAL REVENUE"]
    rev_total = 0
    for m in month_cols:
        val = months_data.get(m, {}).get('total_revenue', 0)
        row.append(val)
        rev_total += val
    row.append(rev_total)
    rows.append(row)
    total_rev_row = row_idx
    row_idx += 1
    
    rows.append([""])
    row_idx += 1
    
    # COGS section
    rows.append(["COST OF REVENUE"] + [""] * (len(month_labels) + 1))
    cogs_section_row = row_idx
    row_idx += 1
    
    cogs_detail_start = row_idx
    for cat in sorted(cogs_cats):
        row = [f"  {cat}"]
        total = 0
        for m in month_cols:
            val = months_data.get(m, {}).get('cogs', {}).get(cat, 0)
            if val > 0:
                val = -val  # Show as negative
            row.append(val)
            total += val
        row.append(total)
        rows.append(row)
        row_idx += 1
    cogs_detail_end = row_idx
    
    # Total COGS
    row = ["TOTAL COST OF REVENUE"]
    cogs_total = 0
    for m in month_cols:
        val = months_data.get(m, {}).get('total_cogs', 0)
        row.append(-val)
        cogs_total -= val
    row.append(cogs_total)
    rows.append(row)
    total_cogs_row = row_idx
    row_idx += 1
    
    rows.append([""])
    row_idx += 1
    
    # GROSS PROFIT
    row = ["GROSS PROFIT"]
    gp_total = 0
    for m in month_cols:
        rev = months_data.get(m, {}).get('total_revenue', 0)
        cogs = months_data.get(m, {}).get('total_cogs', 0)
        gp = rev - cogs
        row.append(gp)
        gp_total += gp
    row.append(gp_total)
    rows.append(row)
    gross_profit_row = row_idx
    row_idx += 1
    
    # Gross Margin %
    row = ["  Gross Margin %"]
    for m in month_cols:
        rev = months_data.get(m, {}).get('total_revenue', 0)
        cogs = months_data.get(m, {}).get('total_cogs', 0)
        gp = rev - cogs
        row.append(gp / rev if rev > 0 else 0)
    row.append(gp_total / rev_total if rev_total > 0 else 0)
    rows.append(row)
    gm_row = row_idx
    row_idx += 1
    
    rows.append([""])
    row_idx += 1
    
    # OPERATING EXPENSES
    rows.append(["OPERATING EXPENSES"] + [""] * (len(month_labels) + 1))
    opex_section_row = row_idx
    row_idx += 1
    
    opex_detail_start = row_idx
    for cat in opex_cats_final:
        row = [f"  {cat}"]
        total = 0
        for m in month_cols:
            val = months_data.get(m, {}).get('opex', {}).get(cat, 0)
            if val > 0:
                val = -val
            row.append(val)
            total += val
        row.append(total)
        rows.append(row)
        row_idx += 1
    opex_detail_end = row_idx
    
    # Total OpEx
    row = ["TOTAL OPERATING EXPENSES"]
    opex_total = 0
    for m in month_cols:
        val = months_data.get(m, {}).get('total_opex', 0)
        row.append(-val)
        opex_total -= val
    row.append(opex_total)
    rows.append(row)
    total_opex_row = row_idx
    row_idx += 1
    
    rows.append([""])
    row_idx += 1
    
    # NET INCOME
    row = ["NET INCOME"]
    ni_total = 0
    for m in month_cols:
        d = months_data.get(m, {})
        ni = d.get('total_revenue', 0) - d.get('total_cogs', 0) - d.get('total_opex', 0)
        row.append(ni)
        ni_total += ni
    row.append(ni_total)
    rows.append(row)
    net_income_row = row_idx
    row_idx += 1
    
    # Net Margin %
    row = ["  Net Margin %"]
    for m in month_cols:
        d = months_data.get(m, {})
        ni = d.get('total_revenue', 0) - d.get('total_cogs', 0) - d.get('total_opex', 0)
        rev = d.get('total_revenue', 0)
        row.append(ni / rev if rev > 0 else 0)
    row.append(ni_total / rev_total if rev_total > 0 else 0)
    rows.append(row)
    nm_row = row_idx
    row_idx += 1
    
    # Write values
    update_values(token, sid, f"'{tab_name}'!A1", rows)
    
    # Formatting
    num_cols = len(month_labels) + 2  # label + months + total
    fmt = [
        format_row(sheet_id, 0, 0, num_cols, {"textFormat": {"bold": True, "fontSize": 14, "fontFamily": "Arial"}}),
        format_row(sheet_id, 1, 0, num_cols, {"textFormat": {"italic": True, "fontSize": 10, "fontFamily": "Arial"}}),
        format_row(sheet_id, header_row, 0, num_cols, header_format()),
        format_row(sheet_id, rev_section_row, 0, num_cols, subheader_format()),
        format_row(sheet_id, total_rev_row, 0, num_cols, {"textFormat": {"bold": True, "fontFamily": "Arial"}}),
        border_bottom(sheet_id, total_rev_row, 1, num_cols),
        format_row(sheet_id, cogs_section_row, 0, num_cols, subheader_format()),
        format_row(sheet_id, total_cogs_row, 0, num_cols, {"textFormat": {"bold": True, "fontFamily": "Arial"}}),
        border_bottom(sheet_id, total_cogs_row, 1, num_cols),
        format_row(sheet_id, gross_profit_row, 0, num_cols, total_format()),
        double_border_bottom(sheet_id, gross_profit_row, 1, num_cols),
        format_row(sheet_id, opex_section_row, 0, num_cols, subheader_format()),
        format_row(sheet_id, total_opex_row, 0, num_cols, {"textFormat": {"bold": True, "fontFamily": "Arial"}}),
        border_bottom(sheet_id, total_opex_row, 1, num_cols),
        format_row(sheet_id, net_income_row, 0, num_cols, total_format()),
        double_border_bottom(sheet_id, net_income_row, 1, num_cols),
        # Currency formatting for data columns
        format_range_currency(sheet_id, rev_detail_start, opex_detail_end + 5, 1, num_cols),
        # Override percent rows
        format_range_pct(sheet_id, gm_row, gm_row + 1, 1, num_cols),
        format_range_pct(sheet_id, nm_row, nm_row + 1, 1, num_cols),
        col_width(sheet_id, 0, 280),
    ]
    for i in range(1, num_cols):
        fmt.append(col_width(sheet_id, i, 120))
    
    batch_update(token, sid, fmt)


def build_schedule_c(token, sid, months_data):
    """Tab 5: Schedule C Summary"""
    # Aggregate by year
    def year_totals(year_str):
        totals = defaultdict(float)
        for m, d in months_data.items():
            if m.startswith(year_str):
                for cat, amt in d['cogs'].items():
                    totals[cat] += amt
                for cat, amt in d['opex'].items():
                    totals[cat] += amt
        return totals
    
    t2024 = year_totals('2024')
    t2025 = year_totals('2025')
    t2026 = year_totals('2026')
    
    # Map to Schedule C lines
    rows = [
        ["KuriosBrand LLC — Schedule C Summary"],
        ["IRS Schedule C — Profit or Loss From Business"],
        [""],
        ["Line", "Category", "2024 Total", "2025 Total", "2026 YTD", "GL Accounts", "Notes"],
        ["", "INCOME", "", "", "", "", ""],
    ]
    
    # Calculate total revenue
    rev_2024 = sum(d.get('total_revenue', 0) for m, d in months_data.items() if m.startswith('2024'))
    rev_2025 = sum(d.get('total_revenue', 0) for m, d in months_data.items() if m.startswith('2025'))
    rev_2026 = sum(d.get('total_revenue', 0) for m, d in months_data.items() if m.startswith('2026'))
    
    rows.append(["1", "Gross receipts or sales", rev_2024, rev_2025, rev_2026, "4000-4020", "Stripe deposits + Zelle payments"])
    rows.append(["7", "Gross income", rev_2024, rev_2025, rev_2026, "", "Line 1 (no returns/COGS adjustment here)"])
    rows.append(["", "", "", "", "", "", ""])
    rows.append(["", "EXPENSES", "", "", "", "", ""])
    
    # Line 8: Advertising
    ad_cats = ['Advertising - Meta/Facebook', 'Advertising - Google Ads']
    ad_2024 = sum(t2024.get(c, 0) for c in ad_cats)
    ad_2025 = sum(t2025.get(c, 0) for c in ad_cats)
    ad_2026 = sum(t2026.get(c, 0) for c in ad_cats)
    rows.append(["8", "Advertising", ad_2024, ad_2025, ad_2026, "5000, 5010", "Meta Ads, Google Ads"])
    
    # Line 11: Contract labor
    cl_2024 = t2024.get('Contractor Labor', 0)
    cl_2025 = t2025.get('Contractor Labor', 0)
    cl_2026 = t2026.get('Contractor Labor', 0)
    rows.append(["11", "Contract labor", cl_2024, cl_2025, cl_2026, "6120", "Freelancers, VAs (via Wise, PayPal)"])
    
    # Line 15: Insurance
    ins_2024 = t2024.get('Insurance', 0)
    ins_2025 = t2025.get('Insurance', 0)
    ins_2026 = t2026.get('Insurance', 0)
    rows.append(["15", "Insurance (other than health)", ins_2024, ins_2025, ins_2026, "6080", "SafetyWing, Triwest/Tricare"])
    
    # Line 17: Legal & professional
    pro_2024 = t2024.get('Professional Services', 0)
    pro_2025 = t2025.get('Professional Services', 0)
    pro_2026 = t2026.get('Professional Services', 0)
    rows.append(["17", "Legal and professional services", pro_2024, pro_2025, pro_2026, "6050", "Harbor Compliance, WI DFI"])
    
    # Line 18: Office expense
    off_cats = ['Office & Coworking']
    off_2024 = sum(t2024.get(c, 0) for c in off_cats)
    off_2025 = sum(t2025.get(c, 0) for c in off_cats)
    off_2026 = sum(t2026.get(c, 0) for c in off_cats)
    rows.append(["18", "Office expense", off_2024, off_2025, off_2026, "6020", "Regus coworking, virtual mailbox"])
    
    # Line 25: Utilities
    util_cats = ['Telecommunications', 'Internet Service']
    util_2024 = sum(t2024.get(c, 0) for c in util_cats)
    util_2025 = sum(t2025.get(c, 0) for c in util_cats)
    util_2026 = sum(t2026.get(c, 0) for c in util_cats)
    rows.append(["25", "Utilities", util_2024, util_2025, util_2026, "6030, 6040", "T-Mobile, Spectrum, Airalo"])
    
    # Line 27: Other expenses
    other_cats = ['SaaS & Software', 'SEO Services & Tools', 'Bank Fees & Interest', 
                  'CC Interest', 'Domains & Hosting', 'Loan Repayment', 'Education & Training', 'Miscellaneous']
    
    rows.append(["27a", "Other expenses (see list)", "", "", "", "", ""])
    
    total_other_2024 = 0
    total_other_2025 = 0
    total_other_2026 = 0
    for cat in other_cats:
        v24 = t2024.get(cat, 0)
        v25 = t2025.get(cat, 0)
        v26 = t2026.get(cat, 0)
        if v24 > 0 or v25 > 0 or v26 > 0:
            rows.append(["", f"  {cat}", v24, v25, v26, "", ""])
            total_other_2024 += v24
            total_other_2025 += v25
            total_other_2026 += v26
    
    rows.append(["", "  Total Other Expenses", total_other_2024, total_other_2025, total_other_2026, "6000-6150", ""])
    rows.append(["", "", "", "", "", "", ""])
    
    # Total expenses
    total_exp_2024 = ad_2024 + cl_2024 + ins_2024 + pro_2024 + off_2024 + util_2024 + total_other_2024
    total_exp_2025 = ad_2025 + cl_2025 + ins_2025 + pro_2025 + off_2025 + util_2025 + total_other_2025
    total_exp_2026 = ad_2026 + cl_2026 + ins_2026 + pro_2026 + off_2026 + util_2026 + total_other_2026
    rows.append(["28", "TOTAL EXPENSES", total_exp_2024, total_exp_2025, total_exp_2026, "", ""])
    rows.append(["", "", "", "", "", "", ""])
    rows.append(["31", "NET PROFIT (LOSS)", rev_2024 - total_exp_2024, rev_2025 - total_exp_2025, rev_2026 - total_exp_2026, "", "Line 7 minus Line 28"])
    
    update_values(token, sid, "'Schedule C Summary'!A1", rows)
    
    num_rows = len(rows)
    fmt = [
        format_row(4, 0, 0, 7, {"textFormat": {"bold": True, "fontSize": 14, "fontFamily": "Arial"}}),
        format_row(4, 1, 0, 7, {"textFormat": {"italic": True, "fontSize": 10, "fontFamily": "Arial"}}),
        format_row(4, 3, 0, 7, header_format()),
        format_row(4, 4, 0, 7, subheader_format()),
        format_row(4, 8, 0, 7, subheader_format()),
        format_range_currency(4, 5, num_rows, 2, 5),
        col_width(4, 0, 60),
        col_width(4, 1, 300),
        col_width(4, 2, 130),
        col_width(4, 3, 130),
        col_width(4, 4, 130),
        col_width(4, 5, 100),
        col_width(4, 6, 280),
    ]
    
    # Bold total rows
    for i, row in enumerate(rows):
        if row[0] in ['28', '31'] or (len(row) > 1 and 'TOTAL' in str(row[1]).upper()):
            fmt.append(format_row(4, i, 0, 7, total_format()))
            fmt.append(double_border_bottom(4, i, 2, 5))
    
    batch_update(token, sid, fmt)


def build_balance_sheet(token, sid, months_data, all_txns):
    """Tab 6: Balance Sheet (simplified)"""
    # Get sorted months
    active_months = sorted([m for m in months_data.keys() if months_data[m]['total_revenue'] > 0 or months_data[m]['total_cogs'] > 0 or months_data[m]['total_opex'] > 0])
    
    if not active_months:
        active_months = ['2025-06']
    
    month_labels = []
    for m in active_months:
        dt = datetime.strptime(m, '%Y-%m')
        month_labels.append(dt.strftime('%b %Y'))
    
    rows = [
        ["KuriosBrand LLC — Balance Sheet"],
        ["Monthly Snapshots (Cash Basis)"],
        [""],
        [""] + month_labels,
        [""],
        ["ASSETS"],
        ["  Current Assets"],
    ]
    
    # We don't have actual balance data from CSVs (only transaction data)
    # So we'll calculate cumulative P&L as retained earnings proxy
    cumulative_ni = 0
    ni_by_month = []
    for m in active_months:
        d = months_data.get(m, {})
        ni = d.get('total_revenue', 0) - d.get('total_cogs', 0) - d.get('total_opex', 0)
        cumulative_ni += ni
        ni_by_month.append(cumulative_ni)
    
    # Business checking balance from CSV (end of month balances)
    # Extract from transactions - last balance of each month from 4991
    biz_balances = {}
    for txn in all_txns:
        if txn['source'] == '4991':
            m = txn['month']
            # The CSV has balance column but it's in our parsed data
            # We'll use the known values
    
    rows.append(["    Cash - Business Checking (4991)"] + ["See bank reconciliation"] * len(active_months))
    rows.append(["    Stripe Pending"] + ["--"] * len(active_months))
    rows.append(["  Total Current Assets"] + ["--"] * len(active_months))
    rows.append([""])
    rows.append(["  Note: Detailed asset balances require manual input of statement balances."])
    rows.append(["  This section tracks cumulative profitability from operations."])
    rows.append([""])
    rows.append(["EQUITY"])
    rows.append(["  Retained Earnings (Cumulative Net Income)"] + [round(ni, 2) for ni in ni_by_month])
    
    # Monthly net income row
    monthly_ni = []
    for m in active_months:
        d = months_data.get(m, {})
        ni = d.get('total_revenue', 0) - d.get('total_cogs', 0) - d.get('total_opex', 0)
        monthly_ni.append(round(ni, 2))
    
    rows.append(["  Net Income (Current Month)"] + monthly_ni)
    rows.append([""])
    rows.append(["Note: Full balance sheet requires bank statement ending balances,"])
    rows.append(["investment account values, and liability balances from each creditor."])
    rows.append(["Contact accountant to complete with year-end statement data."])
    
    update_values(token, sid, "'Balance Sheet'!A1", rows)
    
    num_cols = len(active_months) + 1
    fmt = [
        format_row(5, 0, 0, num_cols, {"textFormat": {"bold": True, "fontSize": 14, "fontFamily": "Arial"}}),
        format_row(5, 1, 0, num_cols, {"textFormat": {"italic": True, "fontSize": 10, "fontFamily": "Arial"}}),
        format_row(5, 3, 0, num_cols, header_format()),
        format_row(5, 5, 0, num_cols, subheader_format()),
        format_row(5, 15, 0, num_cols, subheader_format()),
        format_range_currency(5, 16, 18, 1, num_cols),
        col_width(5, 0, 350),
    ]
    for i in range(1, num_cols):
        fmt.append(col_width(5, i, 120))
    
    batch_update(token, sid, fmt)


def build_bank_reconciliation(token, sid, months_data):
    """Tab 7: Bank Reconciliation"""
    # Use verified monthly totals from the task spec
    verified = {
        '2025-06': {'revenue': 9023, 'expenses': 4253, 'profit': 4769},
        '2025-07': {'revenue': 12688, 'expenses': 3851, 'profit': 5737},
        '2025-08': {'revenue': 7848, 'expenses': 2660, 'profit': 5188},
        '2025-09': {'revenue': 6510, 'expenses': 1962, 'profit': 4547},
        '2025-11': {'revenue': 5071, 'expenses': 2035, 'profit': 3036},
        '2025-12': {'revenue': 6326, 'expenses': 3611, 'profit': 2715},
        '2026-01': {'revenue': 9322, 'expenses': 9609, 'profit': -287},
    }
    
    rows = [
        ["KuriosBrand LLC — Bank Reconciliation"],
        ["Comparison: Computed vs. Verified Totals"],
        [""],
        ["Month", "Verified Revenue", "Computed Revenue", "Rev. Difference",
         "Verified Expenses", "Computed Expenses", "Exp. Difference",
         "Verified Profit", "Computed Profit", "Profit Difference", "Status"],
    ]
    
    for m in sorted(verified.keys()):
        v = verified[m]
        d = months_data.get(m, {})
        comp_rev = round(d.get('total_revenue', 0), 2)
        comp_exp = round(d.get('total_cogs', 0) + d.get('total_opex', 0), 2)
        comp_profit = round(comp_rev - comp_exp, 2)
        
        rev_diff = round(comp_rev - v['revenue'], 2)
        exp_diff = round(comp_exp - v['expenses'], 2)
        profit_diff = round(comp_profit - v['profit'], 2)
        
        status = "OK" if abs(profit_diff) < 50 else "REVIEW"
        
        dt = datetime.strptime(m, '%Y-%m')
        label = dt.strftime('%b %Y')
        
        rows.append([label, v['revenue'], comp_rev, rev_diff,
                     v['expenses'], comp_exp, exp_diff,
                     v['profit'], comp_profit, profit_diff, status])
    
    rows.append([""])
    rows.append(["Notes:"])
    rows.append(["1. 'Verified' totals are from the monthly financial review."])
    rows.append(["2. Differences may arise from transaction classification timing or CC vs checking allocation."])
    rows.append(["3. October 2025 has no verified data (transition month)."])
    rows.append(["4. Small differences are expected due to rounding and transaction date cutoffs."])
    
    update_values(token, sid, "'Bank Reconciliation'!A1", rows)
    
    num_data_rows = len(verified) + 4
    fmt = [
        format_row(6, 0, 0, 11, {"textFormat": {"bold": True, "fontSize": 14, "fontFamily": "Arial"}}),
        format_row(6, 1, 0, 11, {"textFormat": {"italic": True, "fontSize": 10, "fontFamily": "Arial"}}),
        format_row(6, 3, 0, 11, header_format()),
        format_range_currency(6, 4, num_data_rows + 1, 1, 10),
        col_width(6, 0, 100),
    ]
    for i in range(1, 11):
        fmt.append(col_width(6, i, 130))
    
    batch_update(token, sid, fmt)


# ─── MAIN ───
def main():
    print("Refreshing OAuth token...")
    token = refresh_token()
    print("Token refreshed.")
    
    # Delete old sheet if exists
    old_id_path = "/home/ec2-user/clawd/data/accountant-view-sheet-id.txt"
    if os.path.exists(old_id_path):
        with open(old_id_path) as f:
            old_id = f.read().strip()
        if old_id:
            try:
                requests.delete(
                    f"https://www.googleapis.com/drive/v3/files/{old_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                print(f"Deleted old sheet: {old_id}")
            except:
                pass
    
    print("Parsing CSV files...")
    all_txns = process_all_transactions()
    print(f"Total transactions parsed: {len(all_txns)}")
    
    print("Classifying and aggregating transactions...")
    months_data = build_monthly_financials(all_txns)
    
    # Print summary for verification
    for m in sorted(months_data.keys()):
        d = months_data[m]
        if d['total_revenue'] > 0 or d['total_cogs'] > 0 or d['total_opex'] > 0:
            print(f"  {m}: Revenue=${d['total_revenue']:,.2f} COGS=${d['total_cogs']:,.2f} OpEx=${d['total_opex']:,.2f} Net=${d['net_income']:,.2f}")
    
    print("\nCreating Google Sheet...")
    sid = create_spreadsheet(token)
    print(f"Sheet created: {sid}")
    
    print("Building Summary tab...")
    build_summary_tab(token, sid)
    
    print("Building Chart of Accounts tab...")
    build_chart_of_accounts(token, sid)
    
    print("Building Income Statement 2024...")
    build_income_statement(token, sid, months_data, 2024, 7)
    
    print("Building Income Statement 2025...")
    build_income_statement(token, sid, months_data, 2025, 2)
    
    print("Building Income Statement 2026...")
    build_income_statement(token, sid, months_data, 2026, 3)
    
    print("Building Schedule C Summary...")
    build_schedule_c(token, sid, months_data)
    
    print("Building Balance Sheet...")
    build_balance_sheet(token, sid, months_data, all_txns)
    
    print("Building Bank Reconciliation...")
    build_bank_reconciliation(token, sid, months_data)
    
    # Freeze header rows on IS tabs
    freeze_requests = []
    for sheet_id in [7, 2, 3]:
        freeze_requests.append({
            "updateSheetProperties": {
                "properties": {
                    "sheetId": sheet_id,
                    "gridProperties": {"frozenRowCount": 4}
                },
                "fields": "gridProperties.frozenRowCount"
            }
        })
    # Freeze on summary
    freeze_requests.append({
        "updateSheetProperties": {
            "properties": {
                "sheetId": 0,
                "gridProperties": {"frozenRowCount": 1}
            },
            "fields": "gridProperties.frozenRowCount"
        }
    })
    batch_update(token, sid, freeze_requests)
    
    sheet_url = f"https://docs.google.com/spreadsheets/d/{sid}"
    print(f"\nDone! Sheet URL: {sheet_url}")
    
    # Save sheet ID
    with open("/home/ec2-user/clawd/data/accountant-view-sheet-id.txt", "w") as f:
        f.write(sid)
    
    # Write build report
    report = f"""# Accountant View Build Report

## Sheet Details
- **Title:** {SHEET_TITLE}
- **Sheet ID:** {sid}
- **URL:** {sheet_url}
- **Folder:** KuriosBrand Accounting ({FOLDER_ID})
- **Built:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Tabs Created
1. **Summary** - Entity info, accounting methods, bank accounts
2. **Chart of Accounts** - Full GL numbering (1000-7300)
3. **Income Statement 2025** - P&L Jun-Dec 2025 by month
4. **Income Statement 2026** - P&L Jan-Feb 2026 by month
5. **Schedule C Summary** - IRS Schedule C expense mapping
6. **Balance Sheet** - Cumulative profitability tracking
7. **Bank Reconciliation** - Computed vs verified totals

## Transaction Summary
- **Total transactions processed:** {len(all_txns)}
- **Business checking (4991):** {len([t for t in all_txns if t['source']=='4991'])} txns
- **Business CC (0678):** {len([t for t in all_txns if t['source']=='0678'])} txns

## Monthly Financial Summary
| Month | Revenue | COGS | OpEx | Net Income |
|-------|---------|------|------|------------|
"""
    for m in sorted(months_data.keys()):
        d = months_data[m]
        if d['total_revenue'] > 0 or d['total_cogs'] > 0 or d['total_opex'] > 0:
            report += f"| {m} | ${d['total_revenue']:,.2f} | ${d['total_cogs']:,.2f} | ${d['total_opex']:,.2f} | ${d['net_income']:,.2f} |\n"
    
    report += """
## Formatting
- Professional, CPA-ready formatting (no emojis)
- Headers: Bold, dark gray (#333333) background, white text
- Currency: Standard accounting format with parentheses for negatives
- Subtotals: Single underline; Totals: Double underline
- Font: Arial 10pt throughout

## Notes for Accountant
1. All figures are cash basis
2. Revenue = Stripe deposits + Zelle business payments to 4991
3. COGS = Meta/Facebook ads + Google Ads
4. OpEx categories mapped to Chart of Accounts GL codes
5. Personal accounts (0068, 4252) excluded from P&L
6. Owner's draws tracked as transfers between accounts
7. Stripe Capital loan ($4,200 on 01/23/2026) tracked as liability
8. Balance Sheet requires manual input of bank statement ending balances
"""
    
    with open("/home/ec2-user/clawd/data/accountant-view-build-report.md", "w") as f:
        f.write(report)
    
    print("Report written to /home/ec2-user/clawd/data/accountant-view-build-report.md")
    return sid, sheet_url


if __name__ == "__main__":
    sid, url = main()
