#!/usr/bin/env python3
"""Cross-verify KuriosBrand monthly accounting sheets against Chase CSV exports."""

import csv
import json
import requests
from datetime import datetime
from collections import defaultdict
from io import StringIO
import re
import sys

# ─── OAuth Token Refresh ───
def get_access_token():
    with open('/home/ec2-user/.config/gcal-pro/token.json') as f:
        creds = json.load(f)
    resp = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token',
    })
    resp.raise_for_status()
    return resp.json()['access_token']

# ─── CSV Parsing ───
def parse_checking_csv(filepath):
    """Parse checking account CSV (Details,Posting Date,Description,Amount,Type,Balance,Check or Slip #)"""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row['Posting Date'].strip(), '%m/%d/%Y')
                amount = float(row['Amount'].strip())
                txns.append({
                    'date': date,
                    'description': row['Description'].strip().strip('"'),
                    'amount': amount,
                    'type': row.get('Type', '').strip(),
                    'details': row.get('Details', '').strip(),
                })
            except (ValueError, KeyError) as e:
                pass  # Skip malformed rows
    return txns

def parse_cc_csv(filepath):
    """Parse credit card CSV (Card,Transaction Date,Post Date,Description,Category,Type,Amount)"""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row['Transaction Date'].strip(), '%m/%d/%Y')
                post_date = datetime.strptime(row['Post Date'].strip(), '%m/%d/%Y')
                amount = float(row['Amount'].strip())
                txns.append({
                    'date': date,
                    'post_date': post_date,
                    'description': row['Description'].strip(),
                    'amount': amount,
                    'category': row.get('Category', '').strip(),
                    'type': row.get('Type', '').strip(),
                })
            except (ValueError, KeyError) as e:
                pass
    return txns

def parse_sapphire_csv(filepath):
    """Parse Sapphire CSV (Transaction Date,Post Date,Description,Category,Type,Amount,Memo) - no Card column"""
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                date = datetime.strptime(row['Transaction Date'].strip(), '%m/%d/%Y')
                post_date = datetime.strptime(row['Post Date'].strip(), '%m/%d/%Y')
                amount = float(row['Amount'].strip())
                txns.append({
                    'date': date,
                    'post_date': post_date,
                    'description': row['Description'].strip(),
                    'amount': amount,
                    'category': row.get('Category', '').strip(),
                    'type': row.get('Type', '').strip(),
                })
            except (ValueError, KeyError) as e:
                pass
    return txns

# ─── Month Filtering ───
def filter_by_month(txns, year, month, date_field='date'):
    """Filter transactions to a specific year/month."""
    return [t for t in txns if t[date_field].year == year and t[date_field].month == month]

# ─── Google Sheets Reading ───
def read_sheet(token, spreadsheet_id, range_name):
    """Read a range from a Google Sheet."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_name}'
    resp = requests.get(url, headers={'Authorization': f'Bearer {token}'}, params={'valueRenderOption': 'UNFORMATTED_VALUE'})
    if resp.status_code == 200:
        return resp.json().get('values', [])
    else:
        return None

def get_sheet_tabs(token, spreadsheet_id):
    """Get all tab names from a spreadsheet."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}'
    resp = requests.get(url, headers={'Authorization': f'Bearer {token}'}, params={'fields': 'sheets.properties.title'})
    if resp.status_code == 200:
        return [s['properties']['title'] for s in resp.json().get('sheets', [])]
    return []

def read_sheet_tab_data(token, spreadsheet_id, tab_name):
    """Read all data from a specific tab."""
    # URL-encode the tab name for the range
    encoded_tab = tab_name.replace("'", "''")
    range_name = f"'{encoded_tab}'!A1:Z1000"
    return read_sheet(token, spreadsheet_id, range_name)

# ─── Sheet Transaction Parsing ───
def parse_sheet_transactions(rows):
    """Parse transactions from a sheet tab. Returns list of dicts with date, description, amount."""
    if not rows or len(rows) < 2:
        return []
    
    headers = [str(h).lower().strip() for h in rows[0]]
    txns = []
    
    for row in rows[1:]:
        if not row or all(str(c).strip() == '' for c in row):
            continue
        
        # Pad row to match headers
        while len(row) < len(headers):
            row.append('')
        
        record = {}
        for i, h in enumerate(headers):
            record[h] = row[i] if i < len(row) else ''
        
        # Try to extract date, description, amount
        txn = {'raw': record}
        
        # Find date field
        for key in ['date', 'posting date', 'transaction date', 'post date']:
            if key in record and record[key]:
                txn['date_raw'] = record[key]
                break
        
        # Find description
        for key in ['description', 'desc', 'memo', 'vendor', 'name']:
            if key in record and record[key]:
                txn['description'] = str(record[key]).strip()
                break
        
        # Find amount
        for key in ['amount', 'total', 'debit', 'credit']:
            if key in record and record[key] != '':
                try:
                    val = str(record[key]).replace('$', '').replace(',', '').strip()
                    if val and val != '-':
                        txn['amount'] = float(val)
                        break
                except (ValueError, TypeError):
                    pass
        
        if 'amount' in txn or 'description' in txn:
            txns.append(txn)
    
    return txns

# ─── Dashboard Reading ───
def parse_dashboard(rows):
    """Parse dashboard data from the Dashboard tab."""
    if not rows:
        return {}
    
    result = {}
    for row in rows:
        if not row:
            continue
        key = str(row[0]).strip().lower() if row else ''
        vals = [str(c).strip() for c in row[1:]] if len(row) > 1 else []
        result[key] = vals
    
    return {'raw': rows}

# ─── Main Logic ───
def main():
    print("Starting cross-verification...", flush=True)
    
    # Get token
    print("Refreshing OAuth token...", flush=True)
    token = get_access_token()
    print("Token obtained.", flush=True)
    
    # Parse all CSVs
    print("Parsing CSV files...", flush=True)
    biz_txns = parse_checking_csv('/home/ec2-user/clawd/data/chase-exports/business-4991-alltime.csv')
    personal_txns = parse_checking_csv('/home/ec2-user/clawd/data/chase-exports/personal-0068-alltime.csv')
    bizcc_txns = parse_cc_csv('/home/ec2-user/clawd/data/chase-exports/bizcc-0678-alltime.csv')
    sapphire_txns = parse_sapphire_csv('/home/ec2-user/clawd/data/chase-exports/sapphire-4252-alltime.csv')
    
    print(f"Loaded: Biz={len(biz_txns)}, Personal={len(personal_txns)}, BizCC={len(bizcc_txns)}, Sapphire={len(sapphire_txns)}", flush=True)
    
    # Monthly sheets
    sheets = {
        'June 2025': {'id': '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg', 'year': 2025, 'month': 6, 'note': 'transaction tabs empty'},
        'July 2025': {'id': '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8', 'year': 2025, 'month': 7},
        'August 2025': {'id': '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI', 'year': 2025, 'month': 8},
        'September 2025': {'id': '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM', 'year': 2025, 'month': 9},
        'November 2025': {'id': '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0', 'year': 2025, 'month': 11},
        'December 2025': {'id': '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo', 'year': 2025, 'month': 12},
        'January 2026': {'id': '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE', 'year': 2026, 'month': 1},
    }
    
    # Tab name patterns to match
    tab_patterns = {
        'business': ['💼 Business 4991', 'Business 4991', '💼Business 4991', 'Business'],
        'personal': ['👤 Personal 0068', 'Personal 0068', '👤Personal 0068', 'Personal'],
        'bizcc': ['💳 Biz CC 0678', 'Biz CC 0678', '💳Biz CC 0678', 'Biz CC'],
        'sapphire': ['💎 Sapphire 4252', 'Sapphire 4252', '💎Sapphire 4252', 'Sapphire'],
        'dashboard': ['📊 Dashboard', 'Dashboard', '📊Dashboard'],
    }
    
    def find_tab(tab_list, patterns):
        """Find matching tab from list."""
        for pattern in patterns:
            for tab in tab_list:
                if pattern.lower() in tab.lower() or tab.lower() in pattern.lower():
                    return tab
        return None
    
    # Collect all results
    results = {}
    all_sheet_data = {}
    
    for month_name, info in sheets.items():
        print(f"\n{'='*60}", flush=True)
        print(f"Processing {month_name}...", flush=True)
        sid = info['id']
        year = info['year']
        month = info['month']
        
        # Get CSV data for this month
        csv_biz = filter_by_month(biz_txns, year, month)
        csv_personal = filter_by_month(personal_txns, year, month)
        csv_bizcc = filter_by_month(bizcc_txns, year, month)
        csv_sapphire = filter_by_month(sapphire_txns, year, month)
        
        print(f"  CSV counts: Biz={len(csv_biz)}, Personal={len(csv_personal)}, BizCC={len(csv_bizcc)}, Sapphire={len(csv_sapphire)}", flush=True)
        
        # Get sheet tabs
        tabs = get_sheet_tabs(token, sid)
        print(f"  Sheet tabs: {tabs}", flush=True)
        
        month_result = {
            'csv': {
                'business': {'count': len(csv_biz), 'sum': sum(t['amount'] for t in csv_biz), 'txns': csv_biz},
                'personal': {'count': len(csv_personal), 'sum': sum(t['amount'] for t in csv_personal), 'txns': csv_personal},
                'bizcc': {'count': len(csv_bizcc), 'sum': sum(t['amount'] for t in csv_bizcc), 'txns': csv_bizcc},
                'sapphire': {'count': len(csv_sapphire), 'sum': sum(t['amount'] for t in csv_sapphire), 'txns': csv_sapphire},
            },
            'sheet': {},
            'tabs': tabs,
        }
        
        # Read each matching tab
        for acct_key, patterns in tab_patterns.items():
            tab_name = find_tab(tabs, patterns)
            if tab_name:
                print(f"  Reading tab: {tab_name}", flush=True)
                data = read_sheet_tab_data(token, sid, tab_name)
                if data:
                    if acct_key == 'dashboard':
                        month_result['dashboard_raw'] = data
                    else:
                        parsed = parse_sheet_transactions(data)
                        month_result['sheet'][acct_key] = {
                            'count': len(parsed),
                            'sum': sum(t.get('amount', 0) for t in parsed),
                            'txns': parsed,
                            'raw_headers': data[0] if data else [],
                            'raw_rows': len(data) - 1 if data else 0,
                        }
                        print(f"    → {len(parsed)} transactions parsed (sum: {sum(t.get('amount', 0) for t in parsed):.2f})", flush=True)
                else:
                    month_result['sheet'][acct_key] = {'count': 0, 'sum': 0, 'txns': [], 'raw_headers': [], 'raw_rows': 0}
                    print(f"    → No data", flush=True)
            else:
                month_result['sheet'][acct_key] = {'count': 0, 'sum': 0, 'txns': [], 'note': 'tab not found'}
                print(f"  Tab not found for {acct_key}", flush=True)
        
        results[month_name] = month_result
    
    # ─── October 2025 (no sheet) ───
    print(f"\n{'='*60}", flush=True)
    print("Analyzing October 2025 (no sheet exists)...", flush=True)
    oct_biz = filter_by_month(biz_txns, 2025, 10)
    oct_personal = filter_by_month(personal_txns, 2025, 10)
    oct_bizcc = filter_by_month(bizcc_txns, 2025, 10)
    oct_sapphire = filter_by_month(sapphire_txns, 2025, 10)
    october_data = {
        'business': {'count': len(oct_biz), 'sum': sum(t['amount'] for t in oct_biz), 'txns': oct_biz},
        'personal': {'count': len(oct_personal), 'sum': sum(t['amount'] for t in oct_personal), 'txns': oct_personal},
        'bizcc': {'count': len(oct_bizcc), 'sum': sum(t['amount'] for t in oct_bizcc), 'txns': oct_bizcc},
        'sapphire': {'count': len(oct_sapphire), 'sum': sum(t['amount'] for t in oct_sapphire), 'txns': oct_sapphire},
    }
    print(f"  October CSV counts: Biz={len(oct_biz)}, Personal={len(oct_personal)}, BizCC={len(oct_bizcc)}, Sapphire={len(oct_sapphire)}", flush=True)
    
    # ─── Pre-June 2025 data ───
    print(f"\n{'='*60}", flush=True)
    print("Analyzing pre-June 2025 data...", flush=True)
    pre_june = defaultdict(lambda: defaultdict(list))
    for t in biz_txns:
        if t['date'] < datetime(2025, 6, 1):
            key = t['date'].strftime('%Y-%m')
            pre_june[key]['business'].append(t)
    for t in personal_txns:
        if t['date'] < datetime(2025, 6, 1):
            key = t['date'].strftime('%Y-%m')
            pre_june[key]['personal'].append(t)
    for t in bizcc_txns:
        if t['date'] < datetime(2025, 6, 1):
            key = t['date'].strftime('%Y-%m')
            pre_june[key]['bizcc'].append(t)
    for t in sapphire_txns:
        if t['date'] < datetime(2025, 6, 1):
            key = t['date'].strftime('%Y-%m')
            pre_june[key]['sapphire'].append(t)
    
    print("Pre-June 2025 months with data:", flush=True)
    for ym in sorted(pre_june.keys()):
        counts = {k: len(v) for k, v in pre_june[ym].items()}
        print(f"  {ym}: {counts}", flush=True)
    
    # ─── Generate Reports ───
    print(f"\n{'='*60}", flush=True)
    print("Generating reports...", flush=True)
    
    # Identify ambiguous transactions
    ambiguous_vendors = []
    zelle_unclear = []
    suspicious_dupes = []
    
    # Check for Zelle across all transactions
    for t in biz_txns + personal_txns:
        desc = t['description'].upper()
        if 'ZELLE' in desc:
            # Try to extract recipient/sender
            zelle_unclear.append({
                'date': t['date'].strftime('%m/%d/%Y'),
                'amount': t['amount'],
                'description': t['description'][:120],
                'account': 'Business 4991' if t in biz_txns else 'Personal 0068',
            })
    
    # Check for potential duplicates (same amount, same day, same description)
    for name, txn_list in [('Business 4991', biz_txns), ('Personal 0068', personal_txns)]:
        by_key = defaultdict(list)
        for t in txn_list:
            key = (t['date'].strftime('%Y-%m-%d'), t['amount'])
            by_key[key].append(t)
        for key, group in by_key.items():
            if len(group) > 1:
                descs = [t['description'][:60] for t in group]
                # Check if descriptions are similar
                if len(set(descs)) < len(descs):
                    suspicious_dupes.append({
                        'account': name,
                        'date': key[0],
                        'amount': key[1],
                        'count': len(group),
                        'descriptions': descs,
                    })
    
    for name, txn_list in [('Biz CC 0678', bizcc_txns), ('Sapphire 4252', sapphire_txns)]:
        by_key = defaultdict(list)
        for t in txn_list:
            key = (t['date'].strftime('%Y-%m-%d'), t['amount'])
            by_key[key].append(t)
        for key, group in by_key.items():
            if len(group) > 1:
                descs = [t['description'][:60] for t in group]
                if len(set(descs)) < len(descs):
                    suspicious_dupes.append({
                        'account': name,
                        'date': key[0],
                        'amount': key[1],
                        'count': len(group),
                        'descriptions': descs,
                    })
    
    # ─── Write Cross-Verification Report ───
    report = []
    report.append("# Cross-Verification Report: KuriosBrand Monthly Sheets vs Chase CSVs")
    report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    report.append(f"\n**CSV Sources:**")
    report.append(f"- Business 4991: {len(biz_txns)} total transactions")
    report.append(f"- Personal 0068: {len(personal_txns)} total transactions")
    report.append(f"- Biz CC 0678: {len(bizcc_txns)} total transactions")
    report.append(f"- Sapphire 4252: {len(sapphire_txns)} total transactions")
    
    # Date ranges
    if biz_txns:
        dates = sorted([t['date'] for t in biz_txns])
        report.append(f"\n**Date Range in CSVs:** {dates[0].strftime('%m/%d/%Y')} – {dates[-1].strftime('%m/%d/%Y')}")
    
    report.append("\n---\n")
    
    # Per-month sections
    for month_name, info in sheets.items():
        r = results[month_name]
        report.append(f"## {month_name}")
        report.append(f"\n**Sheet ID:** `{info['id']}`")
        report.append(f"**Tabs found:** {', '.join(r['tabs'])}")
        
        if info.get('note'):
            report.append(f"\n⚠️ **Note:** {info['note']}")
        
        report.append(f"\n### Transaction Count Comparison")
        report.append(f"\n| Account | CSV Count | Sheet Count | Match? |")
        report.append(f"|---------|-----------|-------------|--------|")
        
        for acct_key, acct_name in [('business', '💼 Business 4991'), ('personal', '👤 Personal 0068'), ('bizcc', '💳 Biz CC 0678'), ('sapphire', '💎 Sapphire 4252')]:
            csv_count = r['csv'][acct_key]['count']
            sheet_count = r['sheet'].get(acct_key, {}).get('count', 0)
            sheet_raw = r['sheet'].get(acct_key, {}).get('raw_rows', 0)
            match = '✅' if csv_count == sheet_count else ('⚠️' if abs(csv_count - sheet_count) <= 3 else '❌')
            note = r['sheet'].get(acct_key, {}).get('note', '')
            if note:
                report.append(f"| {acct_name} | {csv_count} | {sheet_count} ({note}) | {match} |")
            else:
                report.append(f"| {acct_name} | {csv_count} | {sheet_count} (raw rows: {sheet_raw}) | {match} |")
        
        report.append(f"\n### Amount Comparison")
        report.append(f"\n| Account | CSV Sum | Sheet Sum | Difference |")
        report.append(f"|---------|---------|-----------|------------|")
        
        for acct_key, acct_name in [('business', '💼 Business 4991'), ('personal', '👤 Personal 0068'), ('bizcc', '💳 Biz CC 0678'), ('sapphire', '💎 Sapphire 4252')]:
            csv_sum = r['csv'][acct_key]['sum']
            sheet_sum = r['sheet'].get(acct_key, {}).get('sum', 0)
            diff = csv_sum - sheet_sum
            flag = '' if abs(diff) < 1 else ' ⚠️'
            report.append(f"| {acct_name} | ${csv_sum:,.2f} | ${sheet_sum:,.2f} | ${diff:,.2f}{flag} |")
        
        # Detailed transaction comparison for non-empty months
        if month_name != 'June 2025':
            for acct_key, acct_name in [('business', '💼 Business 4991'), ('personal', '👤 Personal 0068'), ('bizcc', '💳 Biz CC 0678'), ('sapphire', '💎 Sapphire 4252')]:
                csv_txns_month = r['csv'][acct_key]['txns']
                sheet_txns_month = r['sheet'].get(acct_key, {}).get('txns', [])
                
                if csv_txns_month and not sheet_txns_month:
                    report.append(f"\n#### {acct_name}: ❌ Sheet tab empty/missing — {len(csv_txns_month)} CSV transactions unaccounted for")
                    # List top 10 by absolute amount
                    sorted_txns = sorted(csv_txns_month, key=lambda x: abs(x['amount']), reverse=True)[:10]
                    report.append(f"\nTop transactions by amount:")
                    for t in sorted_txns:
                        report.append(f"- {t['date'].strftime('%m/%d')} | ${t['amount']:,.2f} | {t['description'][:80]}")
                
                elif csv_txns_month and sheet_txns_month:
                    csv_amounts = sorted([t['amount'] for t in csv_txns_month])
                    sheet_amounts = sorted([t.get('amount', 0) for t in sheet_txns_month])
                    
                    if csv_amounts != sheet_amounts:
                        # Find amounts in CSV not in sheet
                        csv_amount_counts = defaultdict(int)
                        sheet_amount_counts = defaultdict(int)
                        for a in csv_amounts:
                            csv_amount_counts[a] += 1
                        for a in sheet_amounts:
                            sheet_amount_counts[a] += 1
                        
                        missing_from_sheet = []
                        for amt, cnt in csv_amount_counts.items():
                            diff_cnt = cnt - sheet_amount_counts.get(amt, 0)
                            if diff_cnt > 0:
                                matching = [t for t in csv_txns_month if t['amount'] == amt][:diff_cnt]
                                missing_from_sheet.extend(matching)
                        
                        extra_in_sheet = []
                        for amt, cnt in sheet_amount_counts.items():
                            diff_cnt = cnt - csv_amount_counts.get(amt, 0)
                            if diff_cnt > 0:
                                matching = [t for t in sheet_txns_month if t.get('amount') == amt][:diff_cnt]
                                extra_in_sheet.extend(matching)
                        
                        if missing_from_sheet:
                            report.append(f"\n#### {acct_name}: Missing from Sheet ({len(missing_from_sheet)} txns)")
                            for t in sorted(missing_from_sheet, key=lambda x: abs(x['amount']), reverse=True)[:15]:
                                report.append(f"- {t['date'].strftime('%m/%d')} | ${t['amount']:,.2f} | {t['description'][:80]}")
                        
                        if extra_in_sheet:
                            report.append(f"\n#### {acct_name}: Extra in Sheet ({len(extra_in_sheet)} txns)")
                            for t in extra_in_sheet[:15]:
                                desc = t.get('description', str(t.get('raw', {}))[:80])
                                report.append(f"- ${t.get('amount', 0):,.2f} | {desc[:80]}")
        
        # Dashboard analysis
        if r.get('dashboard_raw'):
            report.append(f"\n### Dashboard Data")
            dash = r['dashboard_raw']
            for row in dash[:20]:  # First 20 rows
                report.append(f"  {' | '.join(str(c) for c in row)}")
        
        report.append(f"\n---\n")
    
    # ─── October 2025 Section ───
    report.append("## October 2025 (NO MONTHLY SHEET)")
    report.append("\n⚠️ **No accounting sheet exists for October 2025.** Below are all transactions from the Chase CSVs.\n")
    
    for acct_key, acct_name in [('business', '💼 Business 4991'), ('personal', '👤 Personal 0068'), ('bizcc', '💳 Biz CC 0678'), ('sapphire', '💎 Sapphire 4252')]:
        data = october_data[acct_key]
        report.append(f"### {acct_name}: {data['count']} transactions (sum: ${data['sum']:,.2f})")
        
        if data['txns']:
            # Group by income/expense
            income = [t for t in data['txns'] if t['amount'] > 0]
            expenses = [t for t in data['txns'] if t['amount'] < 0]
            
            if income:
                report.append(f"\n**Income ({len(income)} txns, ${sum(t['amount'] for t in income):,.2f}):**")
                for t in sorted(income, key=lambda x: x['amount'], reverse=True)[:15]:
                    report.append(f"- {t['date'].strftime('%m/%d')} | ${t['amount']:,.2f} | {t['description'][:80]}")
            
            if expenses:
                report.append(f"\n**Expenses ({len(expenses)} txns, ${sum(t['amount'] for t in expenses):,.2f}):**")
                for t in sorted(expenses, key=lambda x: x['amount'])[:15]:
                    report.append(f"- {t['date'].strftime('%m/%d')} | ${t['amount']:,.2f} | {t['description'][:80]}")
        report.append("")
    
    report.append("---\n")
    
    # ─── Pre-June 2025 Section ───
    report.append("## Pre-June 2025 Transaction Summary")
    report.append("\nThese months have transactions in the CSVs but no monthly accounting sheets.\n")
    
    report.append("| Month | Business 4991 | Personal 0068 | Biz CC 0678 | Sapphire 4252 |")
    report.append("|-------|---------------|---------------|-------------|---------------|")
    
    for ym in sorted(pre_june.keys()):
        biz_c = len(pre_june[ym].get('business', []))
        per_c = len(pre_june[ym].get('personal', []))
        bcc_c = len(pre_june[ym].get('bizcc', []))
        sap_c = len(pre_june[ym].get('sapphire', []))
        biz_s = sum(t['amount'] for t in pre_june[ym].get('business', []))
        per_s = sum(t['amount'] for t in pre_june[ym].get('personal', []))
        bcc_s = sum(t['amount'] for t in pre_june[ym].get('bizcc', []))
        sap_s = sum(t['amount'] for t in pre_june[ym].get('sapphire', []))
        report.append(f"| {ym} | {biz_c} txns (${biz_s:,.2f}) | {per_c} txns (${per_s:,.2f}) | {bcc_c} txns (${bcc_s:,.2f}) | {sap_c} txns (${sap_s:,.2f}) |")
    
    report.append("\n---\n")
    
    # ─── Zelle Analysis ───
    report.append("## Zelle Transactions (All Time)")
    report.append("\nThese Zelle payments need business line clarification (MVA/R&R/SEO):\n")
    
    zelle_in_range = [z for z in zelle_unclear if True]  # All of them
    for z in sorted(zelle_in_range, key=lambda x: x['date'], reverse=True)[:50]:
        report.append(f"- {z['date']} | {z['account']} | ${z['amount']:,.2f} | {z['description']}")
    
    if len(zelle_unclear) > 50:
        report.append(f"\n... and {len(zelle_unclear) - 50} more Zelle transactions")
    
    report.append(f"\n**Total Zelle transactions:** {len(zelle_unclear)}")
    report.append("\n---\n")
    
    # ─── Suspicious Duplicates ───
    report.append("## Potential Duplicate Transactions")
    report.append("\nSame date + same amount + similar description:\n")
    
    if suspicious_dupes:
        for d in suspicious_dupes[:30]:
            report.append(f"- **{d['account']}** | {d['date']} | ${d['amount']:,.2f} × {d['count']} | {d['descriptions'][0]}")
    else:
        report.append("No suspicious duplicates found.")
    
    report.append("\n---\n")
    
    # ─── Ambiguous Transactions ───
    report.append("## Ambiguous / Hard-to-Categorize Transactions")
    report.append("\nTransactions with unclear business purpose or vendor names:\n")
    
    ambiguous_patterns = ['VENMO', 'CASH APP', 'PAYPAL', 'ATM', 'TRANSFER', 'ONLINE PAYMENT', 'WITHDRAWAL']
    for name, txn_list in [('Business 4991', biz_txns), ('Personal 0068', personal_txns)]:
        for t in txn_list:
            desc_upper = t['description'].upper()
            if any(p in desc_upper for p in ambiguous_patterns):
                if abs(t['amount']) > 50:  # Only flag material ones
                    ambiguous_vendors.append({
                        'account': name,
                        'date': t['date'].strftime('%m/%d/%Y'),
                        'amount': t['amount'],
                        'description': t['description'][:100],
                    })
    
    # Show recent ones (Jun 2025+)
    recent_ambiguous = [a for a in ambiguous_vendors if datetime.strptime(a['date'], '%m/%d/%Y') >= datetime(2025, 6, 1)]
    for a in sorted(recent_ambiguous, key=lambda x: abs(x['amount']), reverse=True)[:40]:
        report.append(f"- {a['date']} | {a['account']} | ${a['amount']:,.2f} | {a['description']}")
    
    report.append(f"\n**Total ambiguous (Jun 2025+):** {len(recent_ambiguous)}")
    
    # Write report
    with open('/home/ec2-user/clawd/data/cross-verification-report.md', 'w') as f:
        f.write('\n'.join(report))
    print(f"\nReport written: /home/ec2-user/clawd/data/cross-verification-report.md", flush=True)
    
    # ─── Questions for Marko ───
    questions = []
    questions.append("# Questions for Marko — Accounting Clarifications Needed")
    questions.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
    questions.append("\nPlease answer each question briefly. For classification, just write the answer next to the question.\n")
    
    q_num = 1
    
    # Missing month
    questions.append("## Missing Data")
    questions.append(f"\n{q_num}. **October 2025** — There's no monthly accounting sheet for October. The CSVs show {october_data['business']['count']} business, {october_data['personal']['count']} personal, {october_data['bizcc']['count']} biz CC, and {october_data['sapphire']['count']} Sapphire transactions. Should we create an October sheet, or were these intentionally skipped?")
    q_num += 1
    
    questions.append(f"\n{q_num}. **June 2025** — The monthly sheet exists but the transaction tabs appear empty (only Dashboard has data). Should we backfill the transaction tabs from the CSVs?")
    q_num += 1
    
    questions.append(f"\n{q_num}. **Pre-June 2025 data** — The CSVs go back to Feb 2024. Do we need accounting sheets for any months before June 2025, or is June 2025 the official start?")
    q_num += 1
    
    # Zelle clarifications
    questions.append("\n## Zelle Payment Classification")
    questions.append("\nFor each recurring Zelle payment, which business line should it be assigned to? (MVA / R&R / SEO / Personal / Other)\n")
    
    # Group Zelle by unique description patterns
    zelle_patterns = defaultdict(list)
    for z in zelle_unclear:
        # Extract name from description
        desc = z['description']
        zelle_patterns[desc[:60]].append(z)
    
    for pattern, txns in sorted(zelle_patterns.items(), key=lambda x: abs(sum(t['amount'] for t in x[1])), reverse=True)[:20]:
        total = sum(t['amount'] for t in txns)
        questions.append(f"{q_num}. **{pattern}** — {len(txns)} payments totaling ${total:,.2f}. Business line?")
        q_num += 1
    
    # Discrepancy questions
    questions.append("\n## Transaction Discrepancies")
    
    for month_name, r in results.items():
        for acct_key, acct_name in [('business', 'Business 4991'), ('personal', 'Personal 0068'), ('bizcc', 'Biz CC 0678'), ('sapphire', 'Sapphire 4252')]:
            csv_count = r['csv'][acct_key]['count']
            sheet_count = r['sheet'].get(acct_key, {}).get('count', 0)
            if csv_count != sheet_count and csv_count > 0 and sheet_count > 0:
                diff = csv_count - sheet_count
                questions.append(f"\n{q_num}. **{month_name} — {acct_name}:** CSV has {csv_count} transactions but sheet has {sheet_count} ({diff:+d}). Is this expected? Were some transactions intentionally excluded?")
                q_num += 1
    
    # Business vs Personal
    questions.append("\n## Business vs Personal Classification")
    questions.append("\nThese transactions are on the business account but might be personal (or vice versa):\n")
    
    personal_on_biz = []
    for t in biz_txns:
        desc = t['description'].upper()
        if any(p in desc for p in ['NETFLIX', 'SPOTIFY', 'HULU', 'DOORDASH', 'UBER EATS', 'GRUBHUB', 'AMAZON PRIME', 'DISNEY', 'HBO']):
            if t['date'] >= datetime(2025, 6, 1):
                personal_on_biz.append(t)
    
    for t in personal_on_biz[:10]:
        questions.append(f"{q_num}. {t['date'].strftime('%m/%d/%Y')} | Business 4991 | ${t['amount']:,.2f} | {t['description'][:80]} — Business or personal?")
        q_num += 1
    
    # Large unclear transactions
    questions.append("\n## Large Transactions Needing Clarification")
    questions.append("\nThese large transactions need a clear category/business line:\n")
    
    large_unclear = []
    for t in biz_txns:
        if abs(t['amount']) > 500 and t['date'] >= datetime(2025, 6, 1):
            desc = t['description'].upper()
            if 'ZELLE' in desc or 'TRANSFER' in desc or 'CHECK' in desc:
                large_unclear.append(('Business 4991', t))
    
    for acct, t in sorted(large_unclear, key=lambda x: abs(x[1]['amount']), reverse=True)[:15]:
        questions.append(f"{q_num}. {t['date'].strftime('%m/%d/%Y')} | {acct} | ${t['amount']:,.2f} | {t['description'][:80]} — What is this for?")
        q_num += 1
    
    questions.append(f"\n---\n**Total questions:** {q_num - 1}")
    
    with open('/home/ec2-user/clawd/data/questions-for-marko.md', 'w') as f:
        f.write('\n'.join(questions))
    print(f"Questions written: /home/ec2-user/clawd/data/questions-for-marko.md", flush=True)
    
    # ─── Summary Statistics ───
    print(f"\n{'='*60}", flush=True)
    print("SUMMARY", flush=True)
    print(f"{'='*60}", flush=True)
    
    for month_name in sheets:
        r = results[month_name]
        total_csv = sum(r['csv'][k]['count'] for k in ['business', 'personal', 'bizcc', 'sapphire'])
        total_sheet = sum(r['sheet'].get(k, {}).get('count', 0) for k in ['business', 'personal', 'bizcc', 'sapphire'])
        match = '✅' if total_csv == total_sheet else '❌'
        print(f"  {month_name}: CSV={total_csv}, Sheet={total_sheet} {match}", flush=True)
    
    print(f"\n  October 2025: {sum(october_data[k]['count'] for k in october_data)} CSV transactions (NO SHEET)", flush=True)
    print(f"  Questions for Marko: {q_num - 1}", flush=True)
    print(f"\nDone!", flush=True)

if __name__ == '__main__':
    main()
