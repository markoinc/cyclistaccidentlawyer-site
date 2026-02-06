#!/usr/bin/env python3
"""
MATH ACCURACY AUDIT: Verify every monthly KuriosBrand accounting sheet
against the all-time transaction CSVs.
"""
import csv
import json
import requests
import sys
from datetime import datetime, date
from collections import defaultdict
from io import StringIO

# ===== CONFIG =====
CSV_FILES = {
    'biz_4991': '/home/ec2-user/clawd/data/chase-exports/business-4991-alltime.csv',
    'personal_0068': '/home/ec2-user/clawd/data/chase-exports/personal-0068-alltime.csv',
    'bizcc_0678': '/home/ec2-user/clawd/data/chase-exports/bizcc-0678-alltime.csv',
    'sapphire_4252': '/home/ec2-user/clawd/data/chase-exports/sapphire-4252-alltime.csv',
}

MONTHS = [
    ('June 2025', '2025-06', date(2025, 6, 1), date(2025, 6, 30)),
    ('July 2025', '2025-07', date(2025, 7, 1), date(2025, 7, 31)),
    ('August 2025', '2025-08', date(2025, 8, 1), date(2025, 8, 31)),
    ('September 2025', '2025-09', date(2025, 9, 1), date(2025, 9, 30)),
    ('October 2025', '2025-10', date(2025, 10, 1), date(2025, 10, 31)),
    ('November 2025', '2025-11', date(2025, 11, 1), date(2025, 11, 30)),
    ('December 2025', '2025-12', date(2025, 12, 1), date(2025, 12, 31)),
    ('January 2026', '2026-01', date(2026, 1, 1), date(2026, 1, 31)),
]

SHEET_IDS = {
    'June 2025': '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg',
    'July 2025': '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8',
    'August 2025': '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI',
    'September 2025': '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM',
    'October 2025': '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA',
    'November 2025': '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0',
    'December 2025': '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo',
    'January 2026': '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE',
}

# Tab name patterns to search for in each sheet
TAB_PATTERNS = {
    'biz_4991': ['Business 4991', '💼 Business 4991', 'Business', '💼'],
    'personal_0068': ['Personal 0068', '👤 Personal 0068', 'Personal', '👤'],
    'bizcc_0678': ['Biz CC 0678', '💳 Biz CC 0678', 'Biz CC', '💳'],
    'sapphire_4252': ['Sapphire 4252', '💎 Sapphire 4252', 'Sapphire', '💎'],
    'dashboard': ['Dashboard', '📊 Dashboard', '📊'],
}

def get_token():
    """Get OAuth2 access token."""
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

def parse_checking_csv(filepath):
    """Parse checking account CSV. Returns list of dicts with parsed dates and amounts."""
    transactions = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                posting_date = datetime.strptime(row['Posting Date'].strip(), '%m/%d/%Y').date()
                amount = float(row['Amount'].strip().replace(',', ''))
                balance_str = row.get('Balance', '').strip().replace(',', '')
                balance = float(balance_str) if balance_str else None
                transactions.append({
                    'date': posting_date,
                    'description': row['Description'].strip().strip('"'),
                    'amount': amount,
                    'balance': balance,
                    'type': row.get('Type', '').strip(),
                    'details': row.get('Details', '').strip(),
                })
            except (ValueError, KeyError) as e:
                print(f"  Warning: Skipping row in {filepath}: {e} — row: {dict(row)}", file=sys.stderr)
    return transactions

def parse_cc_csv(filepath):
    """Parse credit card CSV. Returns list of dicts."""
    transactions = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    reader = csv.reader(StringIO(content))
    header = next(reader)
    header = [h.strip() for h in header]
    
    # Detect if there's a Card column
    has_card = header[0].lower() == 'card'
    
    if has_card:
        # Card, Transaction Date, Post Date, Description, Category, Type, Amount, Memo
        date_idx = 1
        post_date_idx = 2
        desc_idx = 3
        cat_idx = 4
        type_idx = 5
        amount_idx = 6
    else:
        # Transaction Date, Post Date, Description, Category, Type, Amount, Memo
        date_idx = 0
        post_date_idx = 1
        desc_idx = 2
        cat_idx = 3
        type_idx = 4
        amount_idx = 5
    
    for row in reader:
        if not row or len(row) < amount_idx + 1:
            continue
        try:
            txn_date = datetime.strptime(row[date_idx].strip(), '%m/%d/%Y').date()
            post_date = datetime.strptime(row[post_date_idx].strip(), '%m/%d/%Y').date()
            amount = float(row[amount_idx].strip().replace(',', ''))
            transactions.append({
                'date': txn_date,
                'post_date': post_date,
                'description': row[desc_idx].strip(),
                'amount': amount,
                'category': row[cat_idx].strip() if cat_idx < len(row) else '',
                'type': row[type_idx].strip() if type_idx < len(row) else '',
            })
        except (ValueError, IndexError) as e:
            print(f"  Warning: Skipping row in {filepath}: {e}", file=sys.stderr)
    return transactions

def filter_by_month(transactions, start_date, end_date, use_post_date=False):
    """Filter transactions to those within date range."""
    if use_post_date:
        return [t for t in transactions if start_date <= t.get('post_date', t['date']) <= end_date]
    return [t for t in transactions if start_date <= t['date'] <= end_date]

def calc_stats(transactions, is_checking=True):
    """Calculate stats from filtered transactions."""
    count = len(transactions)
    debits = sum(t['amount'] for t in transactions if t['amount'] < 0)
    credits = sum(t['amount'] for t in transactions if t['amount'] > 0)
    net = sum(t['amount'] for t in transactions)
    
    result = {
        'count': count,
        'debits': round(debits, 2),
        'credits': round(credits, 2),
        'net': round(net, 2),
    }
    
    if is_checking and transactions:
        # Sort by date, then look for balances
        # The CSV is newest-first, so we need to handle that
        sorted_txns = sorted(transactions, key=lambda t: t['date'])
        balances = [t for t in sorted_txns if t.get('balance') is not None]
        if balances:
            result['opening_balance'] = balances[0]['balance']
            result['closing_balance'] = balances[-1]['balance']
    
    return result

def get_sheet_tabs(token, sheet_id):
    """Get list of tab names in a sheet."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"  Error getting sheet metadata: {r.status_code} {r.text[:200]}", file=sys.stderr)
        return []
    data = r.json()
    return [s['properties']['title'] for s in data.get('sheets', [])]

def read_sheet_tab(token, sheet_id, tab_name, range_spec='A1:Z1000'):
    """Read all data from a sheet tab."""
    import urllib.parse
    encoded_tab = urllib.parse.quote(tab_name, safe='')
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_tab}!{range_spec}'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers, params={'valueRenderOption': 'UNFORMATTED_VALUE'})
    if r.status_code != 200:
        # Try with formatted value
        r = requests.get(url, headers=headers, params={'valueRenderOption': 'FORMATTED_VALUE'})
        if r.status_code != 200:
            print(f"  Error reading tab '{tab_name}': {r.status_code} {r.text[:200]}", file=sys.stderr)
            return None
    data = r.json()
    return data.get('values', [])

def find_tab(tabs, patterns):
    """Find the matching tab name from a list of patterns."""
    for pattern in patterns:
        for tab in tabs:
            if pattern.lower() in tab.lower() or tab.lower() in pattern.lower():
                return tab
    # Try partial match
    for tab in tabs:
        for pattern in patterns:
            clean_pattern = pattern.replace('💼', '').replace('👤', '').replace('💳', '').replace('💎', '').replace('📊', '').strip()
            clean_tab = tab.replace('💼', '').replace('👤', '').replace('💳', '').replace('💎', '').replace('📊', '').strip()
            if clean_pattern.lower() in clean_tab.lower() or clean_tab.lower() in clean_pattern.lower():
                return tab
    return None

def parse_amount(val):
    """Parse a money value from sheet."""
    if val is None or val == '' or val == '-':
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip()
    s = s.replace('$', '').replace(',', '').replace('(', '-').replace(')', '').strip()
    if not s or s == '-':
        return 0.0
    try:
        return float(s)
    except ValueError:
        return None

def analyze_sheet_tab(values, is_checking=True):
    """Analyze a transaction tab from the sheet."""
    if not values or len(values) < 2:
        return {'count': 0, 'debits': 0, 'credits': 0, 'net': 0, 'raw_header': [], 'raw_rows': []}
    
    header = values[0]
    rows = values[1:]
    
    # Find the amount column
    amount_col = None
    balance_col = None
    date_col = None
    desc_col = None
    
    for i, h in enumerate(header):
        hl = str(h).lower().strip()
        if 'amount' in hl:
            amount_col = i
        if 'balance' in hl:
            balance_col = i
        if 'date' in hl and date_col is None:
            date_col = i
        if 'description' in hl or 'desc' in hl:
            desc_col = i
    
    if amount_col is None:
        # Try to find it by position or other means
        print(f"  Warning: Could not find 'Amount' column. Header: {header}", file=sys.stderr)
        return {'count': 0, 'debits': 0, 'credits': 0, 'net': 0, 'raw_header': header, 'raw_rows': rows, 'error': 'no_amount_col'}
    
    count = 0
    debits = 0
    credits = 0
    parsed_rows = []
    balance_errors = []
    
    for row_idx, row in enumerate(rows):
        if len(row) <= amount_col:
            continue
        amt = parse_amount(row[amount_col])
        if amt is None:
            continue
        if amt == 0 and not any(str(cell).strip() for cell in row if cell):
            continue  # Skip empty rows
        
        count += 1
        if amt < 0:
            debits += amt
        else:
            credits += amt
        
        # Get balance if checking
        balance = None
        if is_checking and balance_col is not None and len(row) > balance_col:
            balance = parse_amount(row[balance_col])
        
        desc = row[desc_col] if desc_col is not None and len(row) > desc_col else ''
        date_val = row[date_col] if date_col is not None and len(row) > date_col else ''
        
        parsed_rows.append({
            'date': date_val,
            'description': desc,
            'amount': amt,
            'balance': balance,
            'row_num': row_idx + 2,  # 1-indexed + header
        })
    
    # Verify running balance for checking accounts
    if is_checking and balance_col is not None and parsed_rows:
        for i in range(1, len(parsed_rows)):
            prev = parsed_rows[i-1]
            curr = parsed_rows[i]
            if prev['balance'] is not None and curr['balance'] is not None and curr['amount'] is not None:
                expected = round(prev['balance'] + curr['amount'], 2)
                actual = curr['balance']
                if abs(expected - actual) > 0.005:
                    balance_errors.append({
                        'row': curr['row_num'],
                        'date': curr['date'],
                        'description': curr['description'],
                        'prev_balance': prev['balance'],
                        'amount': curr['amount'],
                        'expected_balance': expected,
                        'actual_balance': actual,
                        'difference': round(actual - expected, 2),
                    })
    
    return {
        'count': count,
        'debits': round(debits, 2),
        'credits': round(credits, 2),
        'net': round(debits + credits, 2),
        'raw_header': header,
        'raw_rows': rows,
        'parsed_rows': parsed_rows,
        'balance_errors': balance_errors,
        'amount_col': amount_col,
        'balance_col': balance_col,
    }

def analyze_dashboard(values):
    """Parse dashboard tab to find key metrics."""
    result = {}
    if not values:
        return result
    
    for row_idx, row in enumerate(values):
        for col_idx, cell in enumerate(row):
            cell_str = str(cell).lower().strip()
            # Look for key labels and get adjacent values
            if 'total income' in cell_str or 'income' == cell_str:
                if col_idx + 1 < len(row):
                    result['total_income'] = parse_amount(row[col_idx + 1])
                elif row_idx + 1 < len(values) and len(values[row_idx + 1]) > col_idx:
                    result['total_income'] = parse_amount(values[row_idx + 1][col_idx])
            if 'total business' in cell_str or 'business expense' in cell_str:
                if col_idx + 1 < len(row):
                    result['total_biz_expenses'] = parse_amount(row[col_idx + 1])
                elif row_idx + 1 < len(values) and len(values[row_idx + 1]) > col_idx:
                    result['total_biz_expenses'] = parse_amount(values[row_idx + 1][col_idx])
            if 'total personal' in cell_str or 'personal expense' in cell_str:
                if col_idx + 1 < len(row):
                    result['total_personal_expenses'] = parse_amount(row[col_idx + 1])
                elif row_idx + 1 < len(values) and len(values[row_idx + 1]) > col_idx:
                    result['total_personal_expenses'] = parse_amount(values[row_idx + 1][col_idx])
            if 'net' in cell_str and ('cash' in cell_str or 'flow' in cell_str or 'income' in cell_str):
                if col_idx + 1 < len(row):
                    result['net_cash_flow'] = parse_amount(row[col_idx + 1])
            if 'opening' in cell_str and 'balance' in cell_str:
                if col_idx + 1 < len(row):
                    result['opening_balance'] = parse_amount(row[col_idx + 1])
            if 'closing' in cell_str and 'balance' in cell_str:
                if col_idx + 1 < len(row):
                    result['closing_balance'] = parse_amount(row[col_idx + 1])
    
    # Also dump entire dashboard for inspection
    result['raw'] = values
    return result

# ===== MAIN AUDIT =====
def main():
    print("=" * 60)
    print("MATH ACCURACY AUDIT — KuriosBrand Accounting Sheets")
    print("=" * 60)
    
    # Step 1: Parse all CSVs
    print("\n[1/4] Parsing CSV files...")
    all_txns = {}
    
    all_txns['biz_4991'] = parse_checking_csv(CSV_FILES['biz_4991'])
    print(f"  Business 4991: {len(all_txns['biz_4991'])} total transactions")
    
    all_txns['personal_0068'] = parse_checking_csv(CSV_FILES['personal_0068'])
    print(f"  Personal 0068: {len(all_txns['personal_0068'])} total transactions")
    
    all_txns['bizcc_0678'] = parse_cc_csv(CSV_FILES['bizcc_0678'])
    print(f"  Biz CC 0678: {len(all_txns['bizcc_0678'])} total transactions")
    
    all_txns['sapphire_4252'] = parse_cc_csv(CSV_FILES['sapphire_4252'])
    print(f"  Sapphire 4252: {len(all_txns['sapphire_4252'])} total transactions")
    
    # Step 2: Get OAuth token
    print("\n[2/4] Getting OAuth token...")
    token = get_token()
    print(f"  Token obtained: {token[:20]}...")
    
    # Step 3: Process each month
    print("\n[3/4] Processing each month...")
    
    all_results = {}
    
    for month_name, month_key, start_date, end_date in MONTHS:
        print(f"\n{'=' * 50}")
        print(f"  MONTH: {month_name}")
        print(f"{'=' * 50}")
        
        month_result = {
            'csv_stats': {},
            'sheet_stats': {},
            'dashboard': {},
            'comparisons': [],
            'discrepancies': [],
            'balance_errors': {},
        }
        
        # Filter CSVs for this month
        for acct_key in ['biz_4991', 'personal_0068', 'bizcc_0678', 'sapphire_4252']:
            is_checking = acct_key in ['biz_4991', 'personal_0068']
            # For credit cards, use post_date for monthly filtering
            use_post = not is_checking
            filtered = filter_by_month(all_txns[acct_key], start_date, end_date, use_post_date=use_post)
            stats = calc_stats(filtered, is_checking=is_checking)
            month_result['csv_stats'][acct_key] = stats
            print(f"  CSV {acct_key}: {stats['count']} txns, debits={stats['debits']}, credits={stats['credits']}, net={stats['net']}")
        
        # Read Google Sheet
        sheet_id = SHEET_IDS[month_name]
        tabs = get_sheet_tabs(token, sheet_id)
        print(f"  Sheet tabs: {tabs}")
        
        for acct_key in ['biz_4991', 'personal_0068', 'bizcc_0678', 'sapphire_4252']:
            is_checking = acct_key in ['biz_4991', 'personal_0068']
            tab_name = find_tab(tabs, TAB_PATTERNS[acct_key])
            if tab_name:
                print(f"  Reading tab: '{tab_name}'")
                values = read_sheet_tab(token, sheet_id, tab_name)
                if values:
                    sheet_stats = analyze_sheet_tab(values, is_checking=is_checking)
                    month_result['sheet_stats'][acct_key] = sheet_stats
                    print(f"  Sheet {acct_key}: {sheet_stats['count']} txns, debits={sheet_stats['debits']}, credits={sheet_stats['credits']}")
                    if sheet_stats.get('balance_errors'):
                        month_result['balance_errors'][acct_key] = sheet_stats['balance_errors']
                        print(f"  ⚠️  {len(sheet_stats['balance_errors'])} balance errors found!")
                else:
                    month_result['sheet_stats'][acct_key] = None
                    print(f"  WARNING: No data in tab '{tab_name}'")
            else:
                month_result['sheet_stats'][acct_key] = None
                print(f"  WARNING: No tab found for {acct_key}")
        
        # Read Dashboard
        dashboard_tab = find_tab(tabs, TAB_PATTERNS['dashboard'])
        if dashboard_tab:
            print(f"  Reading dashboard: '{dashboard_tab}'")
            dash_values = read_sheet_tab(token, sheet_id, dashboard_tab)
            if dash_values:
                month_result['dashboard'] = analyze_dashboard(dash_values)
                print(f"  Dashboard metrics: {json.dumps({k:v for k,v in month_result['dashboard'].items() if k != 'raw'}, default=str)}")
        
        # Compare
        for acct_key in ['biz_4991', 'personal_0068', 'bizcc_0678', 'sapphire_4252']:
            csv_stats = month_result['csv_stats'].get(acct_key, {})
            sheet_stats = month_result['sheet_stats'].get(acct_key)
            
            if sheet_stats is None:
                month_result['comparisons'].append({
                    'account': acct_key,
                    'check': 'tab_exists',
                    'csv_value': 'N/A',
                    'sheet_value': 'MISSING',
                    'match': False,
                    'difference': 'Tab not found',
                })
                continue
            
            # Transaction count
            csv_count = csv_stats.get('count', 0)
            sheet_count = sheet_stats.get('count', 0)
            count_match = csv_count == sheet_count
            month_result['comparisons'].append({
                'account': acct_key,
                'check': 'txn_count',
                'csv_value': csv_count,
                'sheet_value': sheet_count,
                'match': count_match,
                'difference': sheet_count - csv_count,
            })
            if not count_match:
                month_result['discrepancies'].append({
                    'account': acct_key,
                    'check': 'txn_count',
                    'csv_value': csv_count,
                    'sheet_value': sheet_count,
                    'difference': sheet_count - csv_count,
                })
            
            # Total debits
            csv_debits = csv_stats.get('debits', 0)
            sheet_debits = sheet_stats.get('debits', 0)
            debits_match = abs(csv_debits - sheet_debits) < 0.01
            month_result['comparisons'].append({
                'account': acct_key,
                'check': 'total_debits',
                'csv_value': csv_debits,
                'sheet_value': sheet_debits,
                'match': debits_match,
                'difference': round(sheet_debits - csv_debits, 2),
            })
            if not debits_match:
                month_result['discrepancies'].append({
                    'account': acct_key,
                    'check': 'total_debits',
                    'csv_value': csv_debits,
                    'sheet_value': sheet_debits,
                    'difference': round(sheet_debits - csv_debits, 2),
                })
            
            # Total credits
            csv_credits = csv_stats.get('credits', 0)
            sheet_credits = sheet_stats.get('credits', 0)
            credits_match = abs(csv_credits - sheet_credits) < 0.01
            month_result['comparisons'].append({
                'account': acct_key,
                'check': 'total_credits',
                'csv_value': csv_credits,
                'sheet_value': sheet_credits,
                'match': credits_match,
                'difference': round(sheet_credits - csv_credits, 2),
            })
            if not credits_match:
                month_result['discrepancies'].append({
                    'account': acct_key,
                    'check': 'total_credits',
                    'csv_value': csv_credits,
                    'sheet_value': sheet_credits,
                    'difference': round(sheet_credits - csv_credits, 2),
                })
            
            # Net flow
            csv_net = csv_stats.get('net', 0)
            sheet_net = sheet_stats.get('net', 0)
            net_match = abs(csv_net - sheet_net) < 0.01
            month_result['comparisons'].append({
                'account': acct_key,
                'check': 'net_flow',
                'csv_value': csv_net,
                'sheet_value': sheet_net,
                'match': net_match,
                'difference': round(sheet_net - csv_net, 2),
            })
            if not net_match:
                month_result['discrepancies'].append({
                    'account': acct_key,
                    'check': 'net_flow',
                    'csv_value': csv_net,
                    'sheet_value': sheet_net,
                    'difference': round(sheet_net - csv_net, 2),
                })
        
        all_results[month_name] = month_result
    
    # Step 4: Identify cross-account transfers
    print("\n\n[4/4] Cross-account transfer reconciliation...")
    transfer_mismatches = []
    
    for month_name, month_key, start_date, end_date in MONTHS:
        # Find transfers in biz_4991 to personal_0068
        biz_filtered = filter_by_month(all_txns['biz_4991'], start_date, end_date)
        pers_filtered = filter_by_month(all_txns['personal_0068'], start_date, end_date)
        
        biz_to_pers = [t for t in biz_filtered if '0068' in t['description'] and t['amount'] < 0]
        pers_from_biz = [t for t in pers_filtered if '4991' in t['description'] and t['amount'] > 0]
        
        biz_to_pers_total = sum(t['amount'] for t in biz_to_pers)
        pers_from_biz_total = sum(t['amount'] for t in pers_from_biz)
        
        if abs(biz_to_pers_total + pers_from_biz_total) > 0.01:
            transfer_mismatches.append({
                'month': month_name,
                'type': 'biz_to_personal',
                'biz_side': biz_to_pers_total,
                'personal_side': pers_from_biz_total,
                'difference': round(biz_to_pers_total + pers_from_biz_total, 2),
            })
        
        # CC payments from checking
        biz_cc_payments = [t for t in biz_filtered if '0678' in t['description'] and t['amount'] < 0]
        cc_payments_received = [t for t in filter_by_month(all_txns['bizcc_0678'], start_date, end_date, use_post_date=True) if t['type'].lower() == 'payment']
        
        biz_cc_total = sum(t['amount'] for t in biz_cc_payments)
        cc_received_total = sum(t['amount'] for t in cc_payments_received)
        
        if abs(biz_cc_total + cc_received_total) > 0.01:
            transfer_mismatches.append({
                'month': month_name,
                'type': 'biz_to_cc_0678',
                'biz_side': biz_cc_total,
                'cc_side': cc_received_total,
                'difference': round(biz_cc_total + cc_received_total, 2),
            })
        
        # Sapphire payments
        sapphire_payments_checking = [t for t in biz_filtered if '4252' in t['description'] and t['amount'] < 0]
        sapphire_payments_received = [t for t in filter_by_month(all_txns['sapphire_4252'], start_date, end_date, use_post_date=True) if t['type'].lower() == 'payment']
        
        sap_check_total = sum(t['amount'] for t in sapphire_payments_checking)
        sap_received_total = sum(t['amount'] for t in sapphire_payments_received)
        
        if abs(sap_check_total + sap_received_total) > 0.01:
            transfer_mismatches.append({
                'month': month_name,
                'type': 'biz_to_sapphire',
                'checking_side': sap_check_total,
                'sapphire_side': sap_received_total,
                'difference': round(sap_check_total + sap_received_total, 2),
            })
    
    # ===== GENERATE REPORT =====
    print("\n\nGenerating report...")
    
    report = []
    report.append("# Math Accuracy Audit — KuriosBrand Accounting Sheets")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    report.append(f"\n**Scope:** June 2025 through January 2026 (8 months)")
    report.append(f"\n**Source of Truth:** Chase CSV exports (all-time)")
    
    # Executive Summary
    total_checks = 0
    total_passes = 0
    total_fails = 0
    months_with_errors = []
    total_discrepancy_dollars = 0
    
    for month_name in [m[0] for m in MONTHS]:
        mr = all_results.get(month_name, {})
        month_has_error = False
        for comp in mr.get('comparisons', []):
            total_checks += 1
            if comp['match']:
                total_passes += 1
            else:
                total_fails += 1
                month_has_error = True
                if isinstance(comp.get('difference'), (int, float)):
                    total_discrepancy_dollars += abs(comp['difference'])
        if month_has_error:
            months_with_errors.append(month_name)
    
    report.append("\n---\n")
    report.append("## 1. Executive Summary\n")
    report.append(f"| Metric | Value |")
    report.append(f"|--------|-------|")
    report.append(f"| Total checks performed | {total_checks} |")
    report.append(f"| Checks passed | {total_passes} ✅ |")
    report.append(f"| Checks failed | {total_fails} ❌ |")
    report.append(f"| Accuracy rate | {total_passes/max(total_checks,1)*100:.1f}% |")
    report.append(f"| Months with zero errors | {8 - len(months_with_errors)} of 8 |")
    report.append(f"| Months with errors | {len(months_with_errors)} of 8 |")
    if months_with_errors:
        report.append(f"| Error months | {', '.join(months_with_errors)} |")
    report.append(f"| Total discrepancy (absolute $) | ${total_discrepancy_dollars:,.2f} |")
    
    # Per-Month Detail
    report.append("\n---\n")
    report.append("## 2. Per-Month Detail\n")
    
    ACCT_NAMES = {
        'biz_4991': '💼 Business 4991',
        'personal_0068': '👤 Personal 0068',
        'bizcc_0678': '💳 Biz CC 0678',
        'sapphire_4252': '💎 Sapphire 4252',
    }
    
    for month_name, month_key, start_date, end_date in MONTHS:
        mr = all_results.get(month_name, {})
        report.append(f"\n### {month_name}\n")
        report.append(f"| Check | CSV Truth | Sheet Value | Match? | Difference |")
        report.append(f"|-------|-----------|-------------|--------|------------|")
        
        for comp in mr.get('comparisons', []):
            acct = ACCT_NAMES.get(comp['account'], comp['account'])
            check = comp['check']
            csv_val = comp['csv_value']
            sheet_val = comp['sheet_value']
            match_icon = '✅' if comp['match'] else '❌'
            diff = comp['difference']
            
            # Format values
            if check in ['total_debits', 'total_credits', 'net_flow']:
                csv_str = f"${csv_val:,.2f}" if isinstance(csv_val, (int, float)) else str(csv_val)
                sheet_str = f"${sheet_val:,.2f}" if isinstance(sheet_val, (int, float)) else str(sheet_val)
                diff_str = f"${diff:+,.2f}" if isinstance(diff, (int, float)) else str(diff)
            else:
                csv_str = str(csv_val)
                sheet_str = str(sheet_val)
                diff_str = f"{diff:+d}" if isinstance(diff, int) else str(diff)
            
            report.append(f"| {acct} {check} | {csv_str} | {sheet_str} | {match_icon} | {diff_str} |")
        
        # Dashboard info
        dash = mr.get('dashboard', {})
        if dash and any(k for k in dash if k != 'raw'):
            report.append(f"\n**Dashboard Metrics Found:**")
            for k, v in dash.items():
                if k != 'raw' and v is not None:
                    report.append(f"- {k}: ${v:,.2f}" if isinstance(v, (int, float)) else f"- {k}: {v}")
    
    # Discrepancy Log
    report.append("\n---\n")
    report.append("## 3. Discrepancy Log\n")
    
    all_discrepancies = []
    for month_name in [m[0] for m in MONTHS]:
        mr = all_results.get(month_name, {})
        for d in mr.get('discrepancies', []):
            d['month'] = month_name
            all_discrepancies.append(d)
    
    if not all_discrepancies:
        report.append("**No discrepancies found! All sheets match CSV data perfectly.** 🎉")
    else:
        report.append(f"**{len(all_discrepancies)} discrepancies found:**\n")
        
        # Sort by absolute dollar difference
        all_discrepancies.sort(key=lambda d: abs(d.get('difference', 0)) if isinstance(d.get('difference'), (int, float)) else 0, reverse=True)
        
        for i, d in enumerate(all_discrepancies, 1):
            report.append(f"### Discrepancy #{i}")
            report.append(f"- **Month:** {d['month']}")
            report.append(f"- **Account:** {ACCT_NAMES.get(d['account'], d['account'])}")
            report.append(f"- **Check:** {d['check']}")
            csv_val = d['csv_value']
            sheet_val = d['sheet_value']
            diff = d['difference']
            if d['check'] in ['total_debits', 'total_credits', 'net_flow']:
                report.append(f"- **CSV (Expected):** ${csv_val:,.2f}")
                report.append(f"- **Sheet (Actual):** ${sheet_val:,.2f}")
                report.append(f"- **Difference:** ${diff:+,.2f}")
            else:
                report.append(f"- **CSV (Expected):** {csv_val}")
                report.append(f"- **Sheet (Actual):** {sheet_val}")
                report.append(f"- **Difference:** {diff}")
            report.append("")
    
    # Running Balance Verification
    report.append("\n---\n")
    report.append("## 4. Running Balance Verification\n")
    
    total_balance_errors = 0
    for month_name in [m[0] for m in MONTHS]:
        mr = all_results.get(month_name, {})
        be = mr.get('balance_errors', {})
        if be:
            for acct_key, errors in be.items():
                total_balance_errors += len(errors)
                report.append(f"\n### {month_name} — {ACCT_NAMES.get(acct_key, acct_key)}")
                report.append(f"**{len(errors)} balance errors found:**\n")
                report.append(f"| Row | Date | Description | Prev Balance | Amount | Expected | Actual | Diff |")
                report.append(f"|-----|------|-------------|--------------|--------|----------|--------|------|")
                for e in errors:
                    report.append(f"| {e['row']} | {e['date']} | {str(e['description'])[:30]} | ${e['prev_balance']:,.2f} | ${e['amount']:,.2f} | ${e['expected_balance']:,.2f} | ${e['actual_balance']:,.2f} | ${e['difference']:+,.2f} |")
    
    if total_balance_errors == 0:
        report.append("**All running balances verified correctly across all checking account tabs.** ✅")
    else:
        report.append(f"\n**Total balance formula errors found: {total_balance_errors}**")
    
    # Cross-Account Transfer Reconciliation
    report.append("\n---\n")
    report.append("## 5. Cross-Account Transfer Reconciliation\n")
    
    if not transfer_mismatches:
        report.append("**All cross-account transfers reconcile correctly.** ✅")
    else:
        report.append(f"**{len(transfer_mismatches)} transfer mismatches found:**\n")
        for tm in transfer_mismatches:
            report.append(f"- **{tm['month']}** — {tm['type']}: difference of ${tm['difference']:+,.2f}")
            for k, v in tm.items():
                if k not in ['month', 'type', 'difference']:
                    report.append(f"  - {k}: ${v:,.2f}" if isinstance(v, (int, float)) else f"  - {k}: {v}")
    
    # Priority Fix List
    report.append("\n---\n")
    report.append("## 6. Priority Fix List\n")
    
    if not all_discrepancies:
        report.append("**No fixes needed — all sheets are accurate!** 🎉")
    else:
        report.append("Ranked by absolute dollar amount of discrepancy:\n")
        report.append(f"| Priority | Month | Account | Check | Difference |")
        report.append(f"|----------|-------|---------|-------|------------|")
        for i, d in enumerate(all_discrepancies, 1):
            diff = d.get('difference', 0)
            if isinstance(diff, (int, float)):
                diff_str = f"${abs(diff):,.2f}"
            else:
                diff_str = str(diff)
            report.append(f"| {i} | {d['month']} | {ACCT_NAMES.get(d['account'], d['account'])} | {d['check']} | {diff_str} |")
    
    # Write report
    report_text = '\n'.join(report)
    with open('/home/ec2-user/clawd/data/math-accuracy-audit.md', 'w') as f:
        f.write(report_text)
    
    print(f"\n✅ Report written to /home/ec2-user/clawd/data/math-accuracy-audit.md")
    print(f"   Total checks: {total_checks}")
    print(f"   Passed: {total_passes}")
    print(f"   Failed: {total_fails}")
    print(f"   Accuracy: {total_passes/max(total_checks,1)*100:.1f}%")
    
    # Also dump raw data for debugging
    debug_data = {
        'all_results_summary': {},
    }
    for month_name in [m[0] for m in MONTHS]:
        mr = all_results.get(month_name, {})
        debug_data['all_results_summary'][month_name] = {
            'csv_stats': mr.get('csv_stats', {}),
            'sheet_stats_summary': {
                k: {kk: vv for kk, vv in (v or {}).items() if kk not in ['raw_header', 'raw_rows', 'parsed_rows']}
                for k, v in mr.get('sheet_stats', {}).items()
            },
            'comparisons': mr.get('comparisons', []),
            'discrepancy_count': len(mr.get('discrepancies', [])),
            'dashboard_keys': [k for k in mr.get('dashboard', {}).keys() if k != 'raw'],
        }
    
    with open('/home/ec2-user/clawd/data/math-accuracy-audit-debug.json', 'w') as f:
        json.dump(debug_data, f, indent=2, default=str)
    
    print(f"   Debug data: /home/ec2-user/clawd/data/math-accuracy-audit-debug.json")
    
    # Print summary of dashboard raw data for each month
    print("\n\n===== DASHBOARD RAW DATA DUMP =====")
    for month_name in [m[0] for m in MONTHS]:
        mr = all_results.get(month_name, {})
        dash = mr.get('dashboard', {})
        raw = dash.get('raw', [])
        if raw:
            print(f"\n--- {month_name} Dashboard ---")
            for row in raw[:30]:  # First 30 rows
                print(f"  {row}")

if __name__ == '__main__':
    main()
