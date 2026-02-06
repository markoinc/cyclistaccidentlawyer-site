#!/usr/bin/env python3
"""
Detailed investigation of discrepancies found in initial audit.
Identifies specific missing/extra transactions.
"""
import csv
import json
import requests
import sys
from datetime import datetime, date
from io import StringIO
import urllib.parse

def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

def read_sheet_tab(token, sheet_id, tab_name, range_spec='A1:Z5000'):
    encoded_tab = urllib.parse.quote(tab_name, safe='')
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{encoded_tab}!{range_spec}'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers, params={'valueRenderOption': 'UNFORMATTED_VALUE'})
    if r.status_code != 200:
        r = requests.get(url, headers=headers, params={'valueRenderOption': 'FORMATTED_VALUE'})
    if r.status_code != 200:
        return None
    return r.json().get('values', [])

def get_sheet_tabs(token, sheet_id):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}'
    headers = {'Authorization': f'Bearer {token}'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []
    return [s['properties']['title'] for s in r.json().get('sheets', [])]

def parse_checking_csv(filepath):
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                posting_date = datetime.strptime(row['Posting Date'].strip(), '%m/%d/%Y').date()
                amount = float(row['Amount'].strip().replace(',', ''))
                balance_str = row.get('Balance', '').strip().replace(',', '')
                balance = float(balance_str) if balance_str else None
                txns.append({
                    'date': posting_date,
                    'description': row['Description'].strip().strip('"'),
                    'amount': amount,
                    'balance': balance,
                    'type': row.get('Type', '').strip(),
                })
            except (ValueError, KeyError):
                pass
    return txns

def parse_cc_csv(filepath):
    txns = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    reader = csv.reader(StringIO(content))
    header = next(reader)
    header = [h.strip() for h in header]
    has_card = header[0].lower() == 'card'
    
    if has_card:
        date_idx, post_date_idx, desc_idx, cat_idx, type_idx, amount_idx = 1, 2, 3, 4, 5, 6
    else:
        date_idx, post_date_idx, desc_idx, cat_idx, type_idx, amount_idx = 0, 1, 2, 3, 4, 5
    
    for row in reader:
        if not row or len(row) < amount_idx + 1:
            continue
        try:
            txn_date = datetime.strptime(row[date_idx].strip(), '%m/%d/%Y').date()
            post_date = datetime.strptime(row[post_date_idx].strip(), '%m/%d/%Y').date()
            amount = float(row[amount_idx].strip().replace(',', ''))
            txns.append({
                'date': txn_date,
                'post_date': post_date,
                'description': row[desc_idx].strip(),
                'amount': amount,
                'category': row[cat_idx].strip(),
                'type': row[type_idx].strip(),
            })
        except (ValueError, IndexError):
            pass
    return txns

def parse_amount(val):
    if val is None or val == '' or val == '-':
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace('$', '').replace(',', '').replace('(', '-').replace(')', '').strip()
    if not s or s == '-':
        return 0.0
    try:
        return float(s)
    except ValueError:
        return None

def excel_serial_to_date(serial):
    """Convert Excel serial date to Python date."""
    if isinstance(serial, (int, float)) and serial > 40000:
        from datetime import timedelta
        return date(1899, 12, 30) + timedelta(days=int(serial))
    return None

def find_tab(tabs, patterns):
    for pattern in patterns:
        for tab in tabs:
            clean_p = pattern.replace('💼', '').replace('👤', '').replace('💳', '').replace('💎', '').replace('📊', '').strip().lower()
            clean_t = tab.replace('💼', '').replace('👤', '').replace('💳', '').replace('💎', '').replace('📊', '').strip().lower()
            if clean_p in clean_t or clean_t in clean_p:
                return tab
    return None

token = get_token()
print("Token obtained.\n")

# ===== INVESTIGATION 1: June 2025 - Biz CC 0678 (1 missing txn, $17.16) =====
print("=" * 60)
print("INVESTIGATION 1: June 2025 - Biz CC 0678")
print("  Missing: 1 txn, $17.16 in debits")
print("=" * 60)

cc_txns = parse_cc_csv('/home/ec2-user/clawd/data/chase-exports/bizcc-0678-alltime.csv')
june_cc = [t for t in cc_txns if date(2025, 6, 1) <= t['post_date'] <= date(2025, 6, 30)]
print(f"\nCSV transactions ({len(june_cc)}):")
for t in sorted(june_cc, key=lambda x: x['post_date']):
    print(f"  {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:60]}")

sheet_id = '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg'
tabs = get_sheet_tabs(token, sheet_id)
cc_tab = find_tab(tabs, ['Biz CC 0678', '💳 Biz CC 0678', '💳'])
if cc_tab:
    values = read_sheet_tab(token, sheet_id, cc_tab)
    if values:
        header = values[0]
        print(f"\nSheet header: {header}")
        print(f"Sheet transactions ({len(values)-1}):")
        
        # Find amount column
        amt_col = None
        for i, h in enumerate(header):
            if 'amount' in str(h).lower():
                amt_col = i
        
        sheet_amounts = []
        for row in values[1:]:
            if len(row) > amt_col:
                amt = parse_amount(row[amt_col])
                desc = row[3] if len(row) > 3 else ''
                dt = row[1] if len(row) > 1 else ''
                print(f"  {dt}  {amt:>10.2f}  {desc}")
                sheet_amounts.append(amt)
        
        # Find missing
        csv_amounts = sorted([t['amount'] for t in june_cc])
        sheet_amounts_sorted = sorted(sheet_amounts)
        print(f"\nCSV amounts sorted: {csv_amounts}")
        print(f"Sheet amounts sorted: {sheet_amounts_sorted}")
        
        # Find which CSV txns are not in sheet
        csv_amts_copy = [t['amount'] for t in june_cc]
        sheet_amts_copy = list(sheet_amounts)
        
        missing_from_sheet = []
        for t in june_cc:
            if t['amount'] in sheet_amts_copy:
                sheet_amts_copy.remove(t['amount'])
            else:
                missing_from_sheet.append(t)
        
        print(f"\nMissing from sheet:")
        for t in missing_from_sheet:
            print(f"  {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:60]}  (type: {t['type']})")

# ===== INVESTIGATION 2: July 2025 - Personal 0068 (27 missing txns) =====
print("\n" + "=" * 60)
print("INVESTIGATION 2: July 2025 - Personal 0068")
print("  Missing: 27 txns, $1,724.51 debits, $1,176.36 credits")
print("=" * 60)

pers_txns = parse_checking_csv('/home/ec2-user/clawd/data/chase-exports/personal-0068-alltime.csv')
july_pers = [t for t in pers_txns if date(2025, 7, 1) <= t['date'] <= date(2025, 7, 31)]
print(f"\nCSV transactions: {len(july_pers)}")

sheet_id = '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8'
tabs = get_sheet_tabs(token, sheet_id)
pers_tab = find_tab(tabs, ['Personal 0068', '👤 Personal 0068', '👤'])
if pers_tab:
    values = read_sheet_tab(token, sheet_id, pers_tab)
    if values:
        header = values[0]
        print(f"Sheet header: {header}")
        
        amt_col = None
        desc_col = None
        date_col = None
        for i, h in enumerate(header):
            hl = str(h).lower()
            if 'amount' in hl:
                amt_col = i
            if 'description' in hl or 'desc' in hl:
                desc_col = i
            if 'date' in hl and date_col is None:
                date_col = i
        
        sheet_txns = []
        for row in values[1:]:
            if len(row) > amt_col:
                amt = parse_amount(row[amt_col])
                if amt is not None and amt != 0:
                    desc = str(row[desc_col]) if desc_col and len(row) > desc_col else ''
                    dt = row[date_col] if date_col and len(row) > date_col else ''
                    sheet_txns.append({'date': dt, 'description': desc, 'amount': amt})
        
        print(f"Sheet transactions: {len(sheet_txns)}")
        print(f"Difference: {len(july_pers) - len(sheet_txns)} transactions missing from sheet")
        
        # Match by amount to find what's missing
        csv_list = [(t['date'], t['amount'], t['description'][:50]) for t in sorted(july_pers, key=lambda x: (x['date'], x['amount']))]
        sheet_list = [(t['date'], t['amount'], t['description'][:50]) for t in sheet_txns]
        
        # Build amount frequency maps
        from collections import Counter
        csv_amounts = Counter([round(t['amount'], 2) for t in july_pers])
        sheet_amounts = Counter([round(t['amount'], 2) for t in sheet_txns])
        
        missing_amounts = csv_amounts - sheet_amounts
        extra_amounts = sheet_amounts - csv_amounts
        
        print(f"\nAmounts in CSV but not in sheet (missing):")
        for amt, count in sorted(missing_amounts.items()):
            matching = [t for t in july_pers if round(t['amount'], 2) == amt]
            for m in matching[:count]:
                print(f"  {m['date']}  {m['amount']:>10.2f}  {m['description'][:60]}")
        
        missing_sum_debits = sum(amt * count for amt, count in missing_amounts.items() if amt < 0)
        missing_sum_credits = sum(amt * count for amt, count in missing_amounts.items() if amt > 0)
        print(f"\nMissing debits total: ${missing_sum_debits:,.2f}")
        print(f"Missing credits total: ${missing_sum_credits:,.2f}")
        
        if extra_amounts:
            print(f"\nAmounts in sheet but not in CSV (extra):")
            for amt, count in sorted(extra_amounts.items()):
                matching = [t for t in sheet_txns if round(t['amount'], 2) == amt]
                for m in matching[:count]:
                    print(f"  {m['date']}  {m['amount']:>10.2f}  {m['description'][:60]}")

# ===== INVESTIGATION 3: August 2025 - Sapphire 4252 (7 missing txns) =====
print("\n" + "=" * 60)
print("INVESTIGATION 3: August 2025 - Sapphire 4252")
print("  Missing: 7 txns, $767.18 in debits")
print("=" * 60)

sap_txns = parse_cc_csv('/home/ec2-user/clawd/data/chase-exports/sapphire-4252-alltime.csv')
aug_sap = [t for t in sap_txns if date(2025, 8, 1) <= t['post_date'] <= date(2025, 8, 31)]
print(f"\nCSV transactions by post_date ({len(aug_sap)}):")
for t in sorted(aug_sap, key=lambda x: x['post_date']):
    print(f"  txn: {t['date']}  post: {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:50]}  cat: {t['category']}")

# Also check by transaction date
aug_sap_txndate = [t for t in sap_txns if date(2025, 8, 1) <= t['date'] <= date(2025, 8, 31)]
print(f"\nCSV transactions by txn_date ({len(aug_sap_txndate)}):")
for t in sorted(aug_sap_txndate, key=lambda x: x['date']):
    print(f"  txn: {t['date']}  post: {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:50]}  cat: {t['category']}")

sheet_id = '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI'
tabs = get_sheet_tabs(token, sheet_id)
sap_tab = find_tab(tabs, ['Sapphire 4252', '💎 Sapphire 4252', '💎'])
if sap_tab:
    values = read_sheet_tab(token, sheet_id, sap_tab)
    if values:
        header = values[0]
        print(f"\nSheet header: {header}")
        print(f"Sheet rows: {len(values)-1}")
        for row in values[1:]:
            print(f"  {row}")

# ===== INVESTIGATION 4: September 2025 - Sapphire 4252 (0 txns in sheet) =====
print("\n" + "=" * 60)
print("INVESTIGATION 4: September 2025 - Sapphire 4252")
print("  Missing: 2 txns (entire tab empty)")
print("=" * 60)

sep_sap = [t for t in sap_txns if date(2025, 9, 1) <= t['post_date'] <= date(2025, 9, 30)]
print(f"\nCSV transactions by post_date ({len(sep_sap)}):")
for t in sorted(sep_sap, key=lambda x: x['post_date']):
    print(f"  txn: {t['date']}  post: {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:50]}")

sep_sap_txn = [t for t in sap_txns if date(2025, 9, 1) <= t['date'] <= date(2025, 9, 30)]
print(f"\nCSV transactions by txn_date ({len(sep_sap_txn)}):")
for t in sorted(sep_sap_txn, key=lambda x: x['date']):
    print(f"  txn: {t['date']}  post: {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:50]}")

sheet_id = '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM'
tabs = get_sheet_tabs(token, sheet_id)
sap_tab = find_tab(tabs, ['Sapphire 4252', '💎 Sapphire 4252', '💎'])
if sap_tab:
    values = read_sheet_tab(token, sheet_id, sap_tab)
    if values:
        header = values[0]
        print(f"\nSheet header: {header}")
        print(f"Sheet rows: {len(values)-1}")
        for row in values[1:]:
            print(f"  {row}")
    else:
        print("\nSheet tab is empty!")

# ===== INVESTIGATION 5: January 2026 - Biz CC 0678 (2 extra txns) =====
print("\n" + "=" * 60)
print("INVESTIGATION 5: January 2026 - Biz CC 0678")
print("  Extra: 2 txns, $805.31 extra debits")
print("=" * 60)

jan_cc = [t for t in cc_txns if date(2026, 1, 1) <= t['post_date'] <= date(2026, 1, 31)]
print(f"\nCSV transactions by post_date ({len(jan_cc)}):")
for t in sorted(jan_cc, key=lambda x: x['post_date']):
    print(f"  txn: {t['date']}  post: {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:50]}  type:{t['type']}")

jan_cc_txn = [t for t in cc_txns if date(2026, 1, 1) <= t['date'] <= date(2026, 1, 31)]
print(f"\nCSV transactions by txn_date ({len(jan_cc_txn)}):")
for t in sorted(jan_cc_txn, key=lambda x: x['date']):
    print(f"  txn: {t['date']}  post: {t['post_date']}  {t['amount']:>10.2f}  {t['description'][:50]}  type:{t['type']}")

sheet_id = '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE'
tabs = get_sheet_tabs(token, sheet_id)
cc_tab = find_tab(tabs, ['Biz CC 0678', '💳 Biz CC 0678', '💳'])
if cc_tab:
    values = read_sheet_tab(token, sheet_id, cc_tab)
    if values:
        header = values[0]
        print(f"\nSheet header: {header}")
        
        amt_col = None
        for i, h in enumerate(header):
            if 'amount' in str(h).lower():
                amt_col = i
        
        print(f"Sheet transactions ({len(values)-1}):")
        sheet_cc_txns = []
        for row in values[1:]:
            if len(row) > amt_col:
                amt = parse_amount(row[amt_col])
                dt = row[1] if len(row) > 1 else ''
                desc = row[3] if len(row) > 3 else ''
                print(f"  {dt}  {amt:>10.2f}  {desc}")
                sheet_cc_txns.append({'date': dt, 'amount': amt, 'description': str(desc)})
        
        # Compare
        csv_amounts = Counter([round(t['amount'], 2) for t in jan_cc])
        sheet_amounts = Counter([round(t['amount'], 2) for t in sheet_cc_txns])
        
        extra = sheet_amounts - csv_amounts
        missing = csv_amounts - sheet_amounts
        
        print(f"\nExtra in sheet (not in CSV by post_date):")
        for amt, count in sorted(extra.items()):
            matching = [t for t in sheet_cc_txns if round(t['amount'], 2) == amt]
            for m in matching[:count]:
                print(f"  {m['date']}  {m['amount']:>10.2f}  {m['description'][:60]}")
        
        if missing:
            print(f"\nMissing from sheet:")
            for amt, count in sorted(missing.items()):
                matching = [t for t in jan_cc if round(t['amount'], 2) == amt]
                for m in matching[:count]:
                    print(f"  {m['post_date']}  {m['amount']:>10.2f}  {m['description'][:60]}")

# ===== BALANCE VERIFICATION CLARIFICATION =====
print("\n" + "=" * 60)
print("BALANCE VERIFICATION ANALYSIS")
print("=" * 60)

# The balance column in sheets shows running balance (opening + cumulative sum)
# NOT prev_row_balance + current_amount, because same-day txns can be reordered
# Check if opening + sum(amounts) = closing for each account

for month_name, sheet_id_val, start, end in [
    ('June 2025', '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg', date(2025, 6, 1), date(2025, 6, 30)),
    ('January 2026', '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE', date(2026, 1, 1), date(2026, 1, 31)),
]:
    print(f"\n--- {month_name} Balance Check ---")
    tabs = get_sheet_tabs(token, sheet_id_val)
    
    for acct_name, tab_patterns in [('Business 4991', ['Business 4991', '💼']), ('Personal 0068', ['Personal 0068', '👤'])]:
        tab = find_tab(tabs, tab_patterns)
        if tab:
            values = read_sheet_tab(token, sheet_id_val, tab)
            if values:
                header = values[0]
                amt_col = bal_col = None
                for i, h in enumerate(header):
                    hl = str(h).lower()
                    if 'amount' in hl: amt_col = i
                    if 'balance' in hl: bal_col = i
                
                if amt_col is not None and bal_col is not None:
                    amounts = []
                    first_balance = last_balance = None
                    for row in values[1:]:
                        if len(row) > max(amt_col, bal_col):
                            amt = parse_amount(row[amt_col])
                            bal = parse_amount(row[bal_col])
                            if amt is not None:
                                amounts.append(amt)
                            if bal is not None:
                                if first_balance is None:
                                    first_balance = bal
                                last_balance = bal
                    
                    sum_amounts = round(sum(amounts), 2)
                    print(f"  {acct_name}:")
                    print(f"    First balance (row 2): ${first_balance:,.2f}" if first_balance else "    First balance: N/A")
                    print(f"    Last balance (last row): ${last_balance:,.2f}" if last_balance else "    Last balance: N/A")
                    print(f"    Sum of amounts: ${sum_amounts:,.2f}")
                    print(f"    Count: {len(amounts)}")
                    
                    # Check: does opening_balance = first_balance - first_amount?
                    if values and len(values) > 1:
                        first_amt = parse_amount(values[1][amt_col]) if len(values[1]) > amt_col else None
                        if first_balance is not None and first_amt is not None:
                            opening = round(first_balance - first_amt, 2)
                            expected_closing = round(opening + sum_amounts, 2)
                            print(f"    Implied opening (first_bal - first_amt): ${opening:,.2f}")
                            print(f"    Expected closing (opening + sum): ${expected_closing:,.2f}")
                            if last_balance is not None:
                                if abs(expected_closing - last_balance) < 0.01:
                                    print(f"    ✅ Closing balance matches!")
                                else:
                                    print(f"    ❌ Closing balance mismatch! Expected ${expected_closing:,.2f}, got ${last_balance:,.2f}")
                                    print(f"       Difference: ${last_balance - expected_closing:+,.2f}")

# ===== DASHBOARD DEEP DIVE =====
print("\n" + "=" * 60)
print("DASHBOARD ANALYSIS FOR EACH MONTH")
print("=" * 60)

for month_name, sheet_id_val in [
    ('June 2025', '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg'),
    ('July 2025', '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8'),
    ('October 2025', '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA'),
    ('January 2026', '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE'),
]:
    print(f"\n--- {month_name} Dashboard ---")
    tabs = get_sheet_tabs(token, sheet_id_val)
    dash_tab = find_tab(tabs, ['Dashboard', '📊'])
    if dash_tab:
        values = read_sheet_tab(token, sheet_id_val, dash_tab, 'A1:H50')
        if values:
            for i, row in enumerate(values[:40]):
                print(f"  Row {i+1}: {row}")

print("\n\nDone with investigations.")
