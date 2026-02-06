#!/usr/bin/env python3
"""
Comprehensive audit of all 8 KuriosBrand monthly accounting sheets.
READ-ONLY — does not modify any sheets.
"""

import requests
import csv
import json
import sys
from datetime import datetime
from collections import defaultdict

# ─── AUTH ───────────────────────────────────────────────────────────────
def get_token():
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '838433184423-1sd6hs0m7m7mrvm63f1sct2ovjhs88ut.apps.googleusercontent.com',
        'client_secret': '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',
        'refresh_token': '1//05PmAu-vBTVrWCgYIARAAGAUSNwF-L9Irl-dM7iPoS4XocG_eO32bhNSfNYM0rfwGMKBi-KwJYCpzpAlXYINO04lXIWVAAHmh0qw',
        'grant_type': 'refresh_token'
    })
    return r.json()['access_token']

TOKEN = get_token()
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

# ─── SHEET IDS ──────────────────────────────────────────────────────────
SHEETS = {
    'June 2025': '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg',
    'July 2025': '1fl1VT93SkVjBLV2bss8RN4m45yv5dzC-ATI8JczfVR8',
    'August 2025': '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI',
    'September 2025': '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM',
    'October 2025': '1g403GZFVxpF2Siys_1Kpk_sTnOZZEb0-Xibfmiz16dA',
    'November 2025': '1DmOeIoWJ-K6P4vST4-Sdbf35cZqiuej7AjS0facCsA0',
    'December 2025': '1sGg3SHDLKAmDz0V79MvF-ZVCHcaxjCYMTDV-fZlLWOo',
    'January 2026': '1EMYwVZVoAGUMAlM-G2C1NunZ_RZOvDmgJxdBaKqUriE'
}

# ─── EXPECTED TAB SPEC ──────────────────────────────────────────────────
EXPECTED_TABS = [
    {'name': '📊 Dashboard', 'color_hex': None},       # white/default
    {'name': '💰 Profit First', 'color_hex': '#34A853'},
    {'name': '🎯 Pareto Analysis', 'color_hex': '#FF6D01'},
    {'name': '💼 Business 4991', 'color_hex': '#1B2A4A'},
    {'name': '👤 Personal 0068', 'color_hex': '#1B2A4A'},
    {'name': '💳 Biz CC 0678', 'color_hex': '#1B2A4A'},
    {'name': '💎 Sapphire 4252', 'color_hex': '#1B2A4A'},
    {'name': '📦 Raw Data', 'color_hex': '#999999'},
]

# Colors as RGB fractions
def hex_to_rgb(h):
    h = h.lstrip('#')
    return {'red': int(h[0:2],16)/255.0, 'green': int(h[2:4],16)/255.0, 'blue': int(h[4:6],16)/255.0}

NAVY = hex_to_rgb('#1B2A4A')
GRAY_BG = hex_to_rgb('#F3F3F3')
BLUE_TINT = hex_to_rgb('#E8EDF5')
GREEN_TAB = hex_to_rgb('#34A853')
ORANGE_TAB = hex_to_rgb('#FF6D01')
NAVY_TAB = hex_to_rgb('#1B2A4A')
GRAY_TAB = hex_to_rgb('#999999')

# ─── CSV DATA ───────────────────────────────────────────────────────────
CSV_FILES = {
    'Business 4991': 'data/chase-exports/business-4991-alltime.csv',
    'Personal 0068': 'data/chase-exports/personal-0068-alltime.csv',
    'Biz CC 0678': 'data/chase-exports/bizcc-0678-alltime.csv',
    'Sapphire 4252': 'data/chase-exports/sapphire-4252-alltime.csv',
}

MONTHS = {
    'June 2025': (datetime(2025,6,1), datetime(2025,6,30)),
    'July 2025': (datetime(2025,7,1), datetime(2025,7,31)),
    'August 2025': (datetime(2025,8,1), datetime(2025,8,31)),
    'September 2025': (datetime(2025,9,1), datetime(2025,9,30)),
    'October 2025': (datetime(2025,10,1), datetime(2025,10,31)),
    'November 2025': (datetime(2025,11,1), datetime(2025,11,30)),
    'December 2025': (datetime(2025,12,1), datetime(2025,12,31)),
    'January 2026': (datetime(2026,1,1), datetime(2026,1,31)),
}

def load_csv_data():
    """Load all CSV data, grouped by month and account."""
    data = {}
    for acct_name, fpath in CSV_FILES.items():
        with open(fpath, 'r') as f:
            reader = csv.DictReader(f)
            cols = reader.fieldnames
            date_col = 'Posting Date' if 'Posting Date' in cols else 'Transaction Date'
            for row in reader:
                try:
                    d = datetime.strptime(row[date_col].strip(), '%m/%d/%Y')
                    amt = float(row['Amount'].strip()) if row['Amount'].strip() else 0
                    desc = row.get('Description', '').strip()
                    for mname, (start, end) in MONTHS.items():
                        if start <= d <= end:
                            key = (mname, acct_name)
                            if key not in data:
                                data[key] = []
                            data[key].append({
                                'date': d,
                                'description': desc,
                                'amount': amt,
                                'balance': row.get('Balance', '').strip(),
                            })
                            break
                except Exception as e:
                    pass
    return data

# ─── API HELPERS ────────────────────────────────────────────────────────
def get_spreadsheet(sheet_id):
    """Get full spreadsheet metadata + formatting."""
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}'
    params = {'includeGridData': 'true'}
    r = requests.get(url, headers=HEADERS, params=params)
    if r.status_code != 200:
        print(f"ERROR fetching {sheet_id}: {r.status_code} {r.text[:200]}")
        return None
    return r.json()

def color_matches(actual, expected, tolerance=0.05):
    """Check if a color dict matches expected RGB (with tolerance for rounding)."""
    if actual is None and expected is None:
        return True
    if actual is None or expected is None:
        return False
    for c in ['red', 'green', 'blue']:
        a = actual.get(c, 0)
        e = expected.get(c, 0)
        if abs(a - e) > tolerance:
            return False
    return True

def get_cell_value(cell):
    """Extract the display or raw value from a cell."""
    if not cell:
        return None
    ev = cell.get('effectiveValue', {})
    if 'stringValue' in ev:
        return ev['stringValue']
    if 'numberValue' in ev:
        return ev['numberValue']
    if 'formulaValue' in ev:
        return ev['formulaValue']
    if 'boolValue' in ev:
        return ev['boolValue']
    fv = cell.get('formattedValue', '')
    return fv if fv else None

def get_cell_formatted(cell):
    """Get the formatted display value."""
    if not cell:
        return ''
    return cell.get('formattedValue', '')

# ─── AUDIT FUNCTIONS ────────────────────────────────────────────────────

class AuditResult:
    def __init__(self, month):
        self.month = month
        self.issues = []
        self.design_score = 0
        self.design_max = 0
        self.template_score = 0
        self.template_max = 0
        self.math_score = 0
        self.math_max = 0
    
    def check(self, category, name, passed, detail=''):
        """Record a check. category = 'design', 'template', or 'math'"""
        if category == 'design':
            self.design_max += 1
            if passed:
                self.design_score += 1
        elif category == 'template':
            self.template_max += 1
            if passed:
                self.template_score += 1
        elif category == 'math':
            self.math_max += 1
            if passed:
                self.math_score += 1
        
        if not passed:
            self.issues.append({
                'category': category,
                'check': name,
                'detail': detail,
            })
    
    def summary(self):
        total = self.design_score + self.template_score + self.math_score
        total_max = self.design_max + self.template_max + self.math_max
        return {
            'month': self.month,
            'design': f'{self.design_score}/{self.design_max}',
            'template': f'{self.template_score}/{self.template_max}',
            'math': f'{self.math_score}/{self.math_max}',
            'total': f'{total}/{total_max}',
            'issues': self.issues,
        }


def audit_sheet(month, sheet_id, csv_data, ss_data):
    """Run full audit on one sheet."""
    ar = AuditResult(month)
    
    if ss_data is None:
        ar.check('design', 'Sheet accessible', False, f'Could not fetch sheet {sheet_id}')
        return ar
    
    # ════════════════════════════════════════════════════════════════════
    # A. VISUAL DESIGN CHECKS
    # ════════════════════════════════════════════════════════════════════
    
    sheets = ss_data.get('sheets', [])
    props = ss_data.get('properties', {})
    
    # 1. Spreadsheet title
    expected_title = f'{month} — KuriosBrand Financial Overview'
    actual_title = props.get('title', '')
    ar.check('template', 'Spreadsheet title', 
             actual_title == expected_title,
             f'Expected: "{expected_title}", Got: "{actual_title}"')
    
    # 2. Tab count
    ar.check('design', 'Tab count = 8', len(sheets) == 8,
             f'Found {len(sheets)} tabs, expected 8')
    
    # 3. Tab names and order
    tab_map = {}
    for i, sheet in enumerate(sheets):
        sp = sheet.get('properties', {})
        tab_name = sp.get('title', '')
        tab_map[tab_name] = i
        
        if i < len(EXPECTED_TABS):
            expected_name = EXPECTED_TABS[i]['name']
            ar.check('design', f'Tab {i+1} name', 
                     tab_name == expected_name,
                     f'Tab {i+1}: Expected "{expected_name}", Got "{tab_name}"')
            
            # Tab color
            tab_color = sp.get('tabColorStyle', {}).get('rgbColor', sp.get('tabColor', None))
            expected_hex = EXPECTED_TABS[i]['color_hex']
            if expected_hex is None:
                # Dashboard should be white/default (no color or white)
                is_white = tab_color is None or color_matches(tab_color, {'red': 1, 'green': 1, 'blue': 1})
                is_default = tab_color is None or (tab_color.get('red', 0) == 0 and tab_color.get('green', 0) == 0 and tab_color.get('blue', 0) == 0 and len(tab_color) == 0)
                ar.check('design', f'Tab {i+1} color (white/default)',
                         tab_color is None or is_white or len(tab_color) == 0,
                         f'Dashboard tab should be white/default, got {tab_color}')
            else:
                expected_rgb = hex_to_rgb(expected_hex)
                ar.check('design', f'Tab {i+1} color ({expected_hex})',
                         color_matches(tab_color, expected_rgb),
                         f'Expected ~{expected_hex}, got {tab_color}')
    
    # 4. Check Dashboard formatting
    dashboard_sheet = sheets[0] if sheets else None
    if dashboard_sheet and 'data' in dashboard_sheet:
        grid_data = dashboard_sheet['data'][0]
        rows = grid_data.get('rowData', [])
        
        # Check for section headers (navy bg, white text)
        section_header_count = 0
        has_navy_headers = True
        for ri, row in enumerate(rows):
            cells = row.get('values', [])
            if not cells:
                continue
            cell0 = cells[0] if cells else {}
            bg = cell0.get('effectiveFormat', {}).get('backgroundColor', {})
            
            # Detect section header: navy background
            if color_matches(bg, NAVY, tolerance=0.08):
                section_header_count += 1
                # Check text color is white
                tc = cell0.get('effectiveFormat', {}).get('textFormat', {}).get('foregroundColor', {})
                if not color_matches(tc, {'red': 1, 'green': 1, 'blue': 1}, tolerance=0.1):
                    has_navy_headers = False
                    ar.check('design', f'Dashboard row {ri+1} header text white',
                             False, f'Navy header text not white: {tc}')
                
                # Check font size (should be 14pt for section headers)
                fs = cell0.get('effectiveFormat', {}).get('textFormat', {}).get('fontSize', 10)
                # Only flag if clearly wrong
                if fs < 11:
                    ar.check('design', f'Dashboard row {ri+1} header font size',
                             False, f'Section header font size: {fs}pt, expected >=11pt')
        
        ar.check('design', 'Dashboard has section headers (navy bg)',
                 section_header_count >= 4,
                 f'Found {section_header_count} navy section headers, expected at least 4 (A-D minimum)')
        
        # Check for font (Arial)
        sample_font = None
        for ri, row in enumerate(rows[:20]):
            cells = row.get('values', [])
            for cell in cells:
                ff = cell.get('effectiveFormat', {}).get('textFormat', {}).get('fontFamily', '')
                if ff:
                    sample_font = ff
                    break
            if sample_font:
                break
        ar.check('design', 'Dashboard font family',
                 sample_font and 'arial' in sample_font.lower(),
                 f'Expected Arial, found: {sample_font}')
        
        # Check totals row formatting (blue tint background)
        has_totals_formatting = False
        for ri, row in enumerate(rows):
            cells = row.get('values', [])
            for cell in cells:
                fv = get_cell_formatted(cell)
                if fv and ('TOTAL' in str(fv).upper() and 'SUBTOTAL' not in str(fv).upper()):
                    bg = cell.get('effectiveFormat', {}).get('backgroundColor', {})
                    if color_matches(bg, BLUE_TINT, tolerance=0.15):
                        has_totals_formatting = True
                    break
        ar.check('design', 'Dashboard total rows have blue tint bg',
                 has_totals_formatting,
                 'No total rows found with #E8EDF5 background')
        
        # Check currency formatting
        has_currency = False
        for ri, row in enumerate(rows):
            cells = row.get('values', [])
            for cell in cells:
                nf = cell.get('effectiveFormat', {}).get('numberFormat', {})
                if nf.get('type') == 'CURRENCY' or (nf.get('pattern', '') and '$' in nf.get('pattern', '')):
                    has_currency = True
                    break
            if has_currency:
                break
        ar.check('design', 'Dashboard has currency formatting',
                 has_currency, 'No currency-formatted cells found')
    
    # 5. Check transaction tab formatting
    txn_tab_names = ['💼 Business 4991', '👤 Personal 0068', '💳 Biz CC 0678', '💎 Sapphire 4252']
    for tname in txn_tab_names:
        tab_idx = None
        for i, s in enumerate(sheets):
            if s.get('properties', {}).get('title', '') == tname:
                tab_idx = i
                break
        
        if tab_idx is None:
            ar.check('design', f'{tname} tab exists', False, 'Tab not found')
            continue
        
        tsheet = sheets[tab_idx]
        tprops = tsheet.get('properties', {})
        
        # Check frozen rows
        grid_props = tprops.get('gridProperties', {})
        frozen = grid_props.get('frozenRowCount', 0)
        ar.check('design', f'{tname} frozen row 1', frozen >= 1,
                 f'Frozen rows: {frozen}, expected >= 1')
        
        # Check header formatting
        if 'data' in tsheet:
            tgrid = tsheet['data'][0]
            trows = tgrid.get('rowData', [])
            if trows:
                hrow = trows[0]
                hcells = hrow.get('values', [])
                if hcells:
                    hcell = hcells[0]
                    hbg = hcell.get('effectiveFormat', {}).get('backgroundColor', {})
                    ar.check('design', f'{tname} header navy bg',
                             color_matches(hbg, NAVY, tolerance=0.08),
                             f'Header bg: {hbg}, expected navy')
                    
                    htc = hcell.get('effectiveFormat', {}).get('textFormat', {})
                    hfc = htc.get('foregroundColor', htc.get('foregroundColorStyle', {}).get('rgbColor', {}))
                    ar.check('design', f'{tname} header white text',
                             color_matches(hfc, {'red': 1, 'green': 1, 'blue': 1}, tolerance=0.1),
                             f'Header text color: {hfc}')
                    
                    hbold = htc.get('bold', False)
                    ar.check('design', f'{tname} header bold', hbold,
                             f'Header bold: {hbold}')
            
            # Check column widths
            col_metadata = tgrid.get('columnMetadata', [])
            expected_widths = [110, 250, 250, 130, 130, 250]
            for ci, ew in enumerate(expected_widths):
                if ci < len(col_metadata):
                    aw = col_metadata[ci].get('pixelSize', 0)
                    ar.check('design', f'{tname} col {ci+1} width',
                             abs(aw - ew) <= 15,
                             f'Col {ci+1} width: {aw}px, expected {ew}px')
            
            # Check header names
            if trows:
                hrow = trows[0]
                hcells = hrow.get('values', [])
                expected_headers = ['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']
                for hi, eh in enumerate(expected_headers):
                    if hi < len(hcells):
                        hv = get_cell_formatted(hcells[hi])
                        ar.check('template', f'{tname} header {hi+1}',
                                 eh.lower() in str(hv).lower(),
                                 f'Header {hi+1}: Expected "{eh}", Got "{hv}"')
    
    # 6. Check Profit First tab
    pf_idx = None
    for i, s in enumerate(sheets):
        if 'Profit First' in s.get('properties', {}).get('title', ''):
            pf_idx = i
            break
    
    ar.check('template', 'Profit First tab exists', pf_idx is not None)
    
    if pf_idx is not None and 'data' in sheets[pf_idx]:
        pf_grid = sheets[pf_idx]['data'][0]
        pf_rows = pf_grid.get('rowData', [])
        
        # Check for key Profit First elements
        has_revenue = False
        has_profit = False
        has_owner = False
        has_tax = False
        has_opex = False
        
        for row in pf_rows:
            cells = row.get('values', [])
            for cell in cells:
                fv = str(get_cell_formatted(cell)).lower()
                if 'revenue' in fv or 'income' in fv:
                    has_revenue = True
                if 'profit' in fv and 'owner' not in fv:
                    has_profit = True
                if 'owner' in fv:
                    has_owner = True
                if 'tax' in fv:
                    has_tax = True
                if 'opex' in fv or 'operating' in fv:
                    has_opex = True
        
        ar.check('template', 'Profit First has Revenue row', has_revenue)
        ar.check('template', 'Profit First has Profit row', has_profit)
        ar.check('template', 'Profit First has Owner Comp row', has_owner)
        ar.check('template', 'Profit First has Tax row', has_tax)
        ar.check('template', 'Profit First has OpEx row', has_opex)
        
        # Check for navy headers in Profit First
        pf_navy_count = 0
        for row in pf_rows:
            cells = row.get('values', [])
            if cells:
                bg = cells[0].get('effectiveFormat', {}).get('backgroundColor', {})
                if color_matches(bg, NAVY, tolerance=0.08):
                    pf_navy_count += 1
        ar.check('design', 'Profit First has navy section headers',
                 pf_navy_count >= 1, f'Found {pf_navy_count} navy headers')
    
    # 7. Check Pareto tab
    pareto_idx = None
    for i, s in enumerate(sheets):
        if 'Pareto' in s.get('properties', {}).get('title', ''):
            pareto_idx = i
            break
    
    ar.check('template', 'Pareto tab exists', pareto_idx is not None)
    
    if pareto_idx is not None and 'data' in sheets[pareto_idx]:
        pa_grid = sheets[pareto_idx]['data'][0]
        pa_rows = pa_grid.get('rowData', [])
        
        # Check it has data rows
        data_row_count = 0
        has_cumulative = False
        for row in pa_rows:
            cells = row.get('values', [])
            for cell in cells:
                fv = str(get_cell_formatted(cell)).lower()
                if 'cumul' in fv or 'cum' in fv:
                    has_cumulative = True
            if len(cells) >= 3:
                data_row_count += 1
        
        ar.check('template', 'Pareto has data rows', data_row_count >= 3,
                 f'Found {data_row_count} rows with 3+ cols')
        ar.check('template', 'Pareto has cumulative column', has_cumulative,
                 'No cumulative % column found in headers')
    
    # 8. Check Raw Data tab
    raw_idx = None
    for i, s in enumerate(sheets):
        if 'Raw Data' in s.get('properties', {}).get('title', ''):
            raw_idx = i
            break
    
    ar.check('template', 'Raw Data tab exists', raw_idx is not None)
    
    # 9. Dashboard section checks
    if dashboard_sheet and 'data' in dashboard_sheet:
        grid_data = dashboard_sheet['data'][0]
        rows = grid_data.get('rowData', [])
        
        all_text = ''
        for row in rows:
            cells = row.get('values', [])
            for cell in cells:
                fv = get_cell_formatted(cell)
                if fv:
                    all_text += fv + ' '
        
        at_lower = all_text.lower()
        
        # Section A: Income
        ar.check('template', 'Dashboard has Income section',
                 'income' in at_lower, 'No "income" found in dashboard')
        
        # Business lines
        ar.check('template', 'Dashboard has MVA business line',
                 'mva' in at_lower or 'motor vehicle' in at_lower or '🚗' in all_text,
                 'No MVA business line found')
        
        # Section B: Business Expenses
        ar.check('template', 'Dashboard has Business Expenses section',
                 'business expense' in at_lower or 'biz expense' in at_lower or ('business' in at_lower and 'expense' in at_lower),
                 'No business expenses section found')
        
        # Section C: Personal
        ar.check('template', 'Dashboard has Personal section',
                 'personal' in at_lower,
                 'No personal section found')
        
        # Section D: Key Metrics or Summary
        ar.check('template', 'Dashboard has metrics/summary',
                 'metric' in at_lower or 'summary' in at_lower or 'profit margin' in at_lower or 'net profit' in at_lower,
                 'No metrics/summary section found')
        
        # Section categories
        ar.check('template', 'Dashboard has SaaS category',
                 'saas' in at_lower or '📱' in all_text,
                 'No SaaS category found')
        ar.check('template', 'Dashboard has Marketing category',
                 'marketing' in at_lower or 'ads' in at_lower or '📣' in all_text,
                 'No Marketing category found')
    
    # ════════════════════════════════════════════════════════════════════
    # C. MATH ACCURACY CHECKS
    # ════════════════════════════════════════════════════════════════════
    
    # Map tab names to CSV account names
    tab_to_csv = {
        '💼 Business 4991': 'Business 4991',
        '👤 Personal 0068': 'Personal 0068',
        '💳 Biz CC 0678': 'Biz CC 0678',
        '💎 Sapphire 4252': 'Sapphire 4252',
    }
    
    for tname, csv_acct in tab_to_csv.items():
        csv_key = (month, csv_acct)
        csv_txns = csv_data.get(csv_key, [])
        csv_count = len(csv_txns)
        csv_total = sum(t['amount'] for t in csv_txns)
        
        # Find tab
        tab_idx = None
        for i, s in enumerate(sheets):
            if s.get('properties', {}).get('title', '') == tname:
                tab_idx = i
                break
        
        if tab_idx is None:
            ar.check('math', f'{tname} exists for math check', False, 'Tab missing')
            continue
        
        if 'data' not in sheets[tab_idx]:
            ar.check('math', f'{tname} has data', False, 'No grid data')
            continue
        
        tgrid = sheets[tab_idx]['data'][0]
        trows = tgrid.get('rowData', [])
        
        # Count data rows (skip header)
        sheet_amounts = []
        sheet_dates = []
        for ri in range(1, len(trows)):
            cells = trows[ri].get('values', [])
            if len(cells) < 4:
                continue
            
            # Get amount from column D (index 3)
            amt_cell = cells[3] if len(cells) > 3 else {}
            amt_val = amt_cell.get('effectiveValue', {}).get('numberValue', None)
            
            # Get date from column A (index 0)
            date_cell = cells[0] if cells else {}
            date_val = get_cell_formatted(date_cell)
            
            # Skip empty rows
            if amt_val is None and not date_val:
                continue
            
            if amt_val is not None:
                sheet_amounts.append(amt_val)
            if date_val:
                sheet_dates.append(date_val)
        
        sheet_count = len(sheet_amounts)
        sheet_total = sum(sheet_amounts) if sheet_amounts else 0
        
        # Transaction count comparison
        count_diff = abs(sheet_count - csv_count)
        ar.check('math', f'{tname} transaction count ({csv_count} expected)',
                 count_diff <= 2,
                 f'Sheet has {sheet_count} rows, CSV has {csv_count} ({count_diff} difference)')
        
        # Total amount comparison
        total_diff = abs(sheet_total - csv_total)
        ar.check('math', f'{tname} total amount (${csv_total:,.2f} expected)',
                 total_diff < 5.00,
                 f'Sheet total: ${sheet_total:,.2f}, CSV total: ${csv_total:,.2f} (diff: ${total_diff:,.2f})')
        
        # Spot-check: compare individual transactions
        # Sort CSV by amount for easier matching
        csv_sorted = sorted(csv_txns, key=lambda x: abs(x['amount']), reverse=True)
        sheet_amounts_set = set(round(a, 2) for a in sheet_amounts)
        
        spot_checks = min(10, len(csv_sorted))
        matches = 0
        misses = []
        for t in csv_sorted[:spot_checks]:
            csv_amt = round(t['amount'], 2)
            if csv_amt in sheet_amounts_set:
                matches += 1
            else:
                misses.append(f"${csv_amt:,.2f} ({t['description'][:40]})")
        
        ar.check('math', f'{tname} spot-check ({spot_checks} largest txns)',
                 matches >= spot_checks * 0.7,
                 f'{matches}/{spot_checks} matched. Missing: {"; ".join(misses[:5])}')
    
    # Check Profit First math
    if pf_idx is not None and 'data' in sheets[pf_idx]:
        pf_grid = sheets[pf_idx]['data'][0]
        pf_rows = pf_grid.get('rowData', [])
        
        # Try to find revenue and allocation values
        revenue_val = None
        alloc_vals = {}
        
        for row in pf_rows:
            cells = row.get('values', [])
            for ci, cell in enumerate(cells):
                fv = str(get_cell_formatted(cell)).lower()
                if ('revenue' in fv or 'total income' in fv) and ci == 0:
                    # Look for numeric value in adjacent cells
                    for adj in range(1, min(6, len(cells))):
                        nv = cells[adj].get('effectiveValue', {}).get('numberValue', None)
                        if nv and abs(nv) > 10:
                            revenue_val = nv
                            break
                
                for bucket, pct in [('profit', 0.05), ('owner', 0.50), ('tax', 0.15), ('opex', 0.30)]:
                    if bucket in fv and ci == 0:
                        for adj in range(1, min(6, len(cells))):
                            nv = cells[adj].get('effectiveValue', {}).get('numberValue', None)
                            if nv is not None:
                                alloc_vals[bucket] = nv
                                break
        
        if revenue_val:
            ar.check('math', 'Profit First revenue found', True,
                     f'Revenue: ${revenue_val:,.2f}')
            
            # Check allocations
            for bucket, pct in [('profit', 0.05), ('owner', 0.50), ('tax', 0.15), ('opex', 0.30)]:
                expected_alloc = revenue_val * pct
                actual_alloc = alloc_vals.get(bucket)
                if actual_alloc is not None:
                    diff = abs(actual_alloc - expected_alloc)
                    ar.check('math', f'Profit First {bucket} allocation',
                             diff < abs(expected_alloc) * 0.1 + 1,
                             f'Expected ${expected_alloc:,.2f} ({pct*100}% of ${revenue_val:,.2f}), got ${actual_alloc:,.2f}')
        else:
            ar.check('math', 'Profit First revenue found', False,
                     'Could not find revenue value in Profit First tab')
    
    # Check Pareto cumulative %
    if pareto_idx is not None and 'data' in sheets[pareto_idx]:
        pa_grid = sheets[pareto_idx]['data'][0]
        pa_rows = pa_grid.get('rowData', [])
        
        # Find the cumulative % column
        cum_pct_values = []
        pct_col = None
        
        # Find header row to locate cumulative % column
        if pa_rows:
            hcells = pa_rows[0].get('values', [])
            for ci, cell in enumerate(hcells):
                fv = str(get_cell_formatted(cell)).lower()
                if 'cum' in fv and '%' in fv:
                    pct_col = ci
                    break
                if 'cum' in fv:
                    pct_col = ci
                    break
        
        if pct_col is not None:
            for ri in range(1, len(pa_rows)):
                cells = pa_rows[ri].get('values', [])
                if pct_col < len(cells):
                    nv = cells[pct_col].get('effectiveValue', {}).get('numberValue', None)
                    if nv is not None:
                        cum_pct_values.append(nv)
            
            if cum_pct_values:
                last_pct = cum_pct_values[-1]
                # Should end near 100% (1.0)
                ar.check('math', 'Pareto cumulative reaches ~100%',
                         abs(last_pct - 1.0) < 0.02 or abs(last_pct - 100) < 2,
                         f'Last cumulative %: {last_pct} (expected ~1.0 or ~100%)')
                
                # Check monotonically increasing
                is_monotonic = all(cum_pct_values[i] <= cum_pct_values[i+1] + 0.001 
                                  for i in range(len(cum_pct_values)-1))
                ar.check('math', 'Pareto cumulative is monotonically increasing',
                         is_monotonic, 'Cumulative % not always increasing')
            else:
                ar.check('math', 'Pareto has cumulative values', False, 'No numeric values found')
        else:
            ar.check('math', 'Pareto cumulative % column found', False,
                     'Could not identify cumulative % column')
    
    return ar


# ─── MAIN ───────────────────────────────────────────────────────────────
def main():
    print("Loading CSV data...")
    csv_data = load_csv_data()
    
    all_results = []
    
    for month, sheet_id in SHEETS.items():
        print(f"\n{'='*60}")
        print(f"AUDITING: {month} ({sheet_id})")
        print(f"{'='*60}")
        
        ss_data = get_spreadsheet(sheet_id)
        if ss_data:
            print(f"  Title: {ss_data.get('properties', {}).get('title', 'N/A')}")
            print(f"  Tabs: {len(ss_data.get('sheets', []))}")
        
        result = audit_sheet(month, sheet_id, csv_data, ss_data)
        all_results.append(result)
        
        s = result.summary()
        print(f"  Design: {s['design']}")
        print(f"  Template: {s['template']}")
        print(f"  Math: {s['math']}")
        print(f"  Issues: {len(s['issues'])}")
        for issue in s['issues']:
            print(f"    ❌ [{issue['category']}] {issue['check']}: {issue['detail'][:100]}")
    
    # ─── Generate Report ────────────────────────────────────────────────
    print("\n\n" + "="*80)
    print("GENERATING FINAL REPORT")
    print("="*80)
    
    # Compute global scores
    total_design = sum(r.design_score for r in all_results)
    total_design_max = sum(r.design_max for r in all_results)
    total_template = sum(r.template_score for r in all_results)
    total_template_max = sum(r.template_max for r in all_results)
    total_math = sum(r.math_score for r in all_results)
    total_math_max = sum(r.math_max for r in all_results)
    
    total_score = total_design + total_template + total_math
    total_max = total_design_max + total_template_max + total_math_max
    
    # Normalize to 1000 points
    if total_max > 0:
        design_norm = round(333 * total_design / total_design_max) if total_design_max > 0 else 0
        template_norm = round(333 * total_template / total_template_max) if total_template_max > 0 else 0
        math_norm = round(334 * total_math / total_math_max) if total_math_max > 0 else 0
        final_score = design_norm + template_norm + math_norm
    else:
        final_score = 0
        design_norm = template_norm = math_norm = 0
    
    # Count issues
    all_issues = []
    for r in all_results:
        for issue in r.issues:
            issue['month'] = r.month
            all_issues.append(issue)
    
    design_issues = [i for i in all_issues if i['category'] == 'design']
    template_issues = [i for i in all_issues if i['category'] == 'template']
    math_issues = [i for i in all_issues if i['category'] == 'math']
    
    pass_fail = "✅ PASS" if final_score >= 800 else ("⚠️ CONDITIONAL PASS" if final_score >= 600 else "❌ FAIL")
    
    report = f"""# 📋 Final Comprehensive Audit Report — KuriosBrand Accounting Sheets

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Auditor:** Sierra (Automated)
**Scope:** All 8 monthly sheets (June 2025 – January 2026)
**Mode:** READ-ONLY verification (no changes made)

---

## 🏆 OVERALL SCORE: {final_score} / 1000

| Category | Score | Raw | Issues |
|----------|-------|-----|--------|
| 🎨 Visual Design | {design_norm}/333 | {total_design}/{total_design_max} | {len(design_issues)} |
| 📋 Template Accuracy | {template_norm}/333 | {total_template}/{total_template_max} | {len(template_issues)} |
| 🔢 Math Accuracy | {math_norm}/334 | {total_math}/{total_math_max} | {len(math_issues)} |
| **TOTAL** | **{final_score}/1000** | **{total_score}/{total_max}** | **{len(all_issues)}** |

### Assessment: {pass_fail}

---

## 📊 Per-Sheet Scores

| Month | Design | Template | Math | Total | Issues |
|-------|--------|----------|------|-------|--------|
"""
    
    for r in all_results:
        s = r.summary()
        sheet_total = r.design_score + r.template_score + r.math_score
        sheet_max = r.design_max + r.template_max + r.math_max
        pct = round(100 * sheet_total / sheet_max) if sheet_max > 0 else 0
        report += f"| {r.month} | {s['design']} | {s['template']} | {s['math']} | {sheet_total}/{sheet_max} ({pct}%) | {len(s['issues'])} |\n"
    
    report += f"""
---

## 🎨 A. VISUAL DESIGN ISSUES ({len(design_issues)} found)

"""
    if not design_issues:
        report += "✅ No visual design issues found!\n\n"
    else:
        for month_name in SHEETS:
            month_issues = [i for i in design_issues if i['month'] == month_name]
            if month_issues:
                report += f"### {month_name}\n"
                for i in month_issues:
                    report += f"- ❌ **{i['check']}**: {i['detail']}\n"
                report += "\n"
    
    report += f"""---

## 📋 B. TEMPLATE ACCURACY ISSUES ({len(template_issues)} found)

"""
    if not template_issues:
        report += "✅ No template accuracy issues found!\n\n"
    else:
        for month_name in SHEETS:
            month_issues = [i for i in template_issues if i['month'] == month_name]
            if month_issues:
                report += f"### {month_name}\n"
                for i in month_issues:
                    report += f"- ❌ **{i['check']}**: {i['detail']}\n"
                report += "\n"
    
    report += f"""---

## 🔢 C. MATH ACCURACY ISSUES ({len(math_issues)} found)

"""
    if not math_issues:
        report += "✅ No math accuracy issues found!\n\n"
    else:
        for month_name in SHEETS:
            month_issues = [i for i in math_issues if i['month'] == month_name]
            if month_issues:
                report += f"### {month_name}\n"
                for i in month_issues:
                    report += f"- ❌ **{i['check']}**: {i['detail']}\n"
                report += "\n"
    
    report += """---

## 🔧 Issues Fixed During Audit

**NONE** — This was a READ-ONLY audit pass. No changes were made.

---

## 📝 Remaining Issues Needing Manual Attention

"""
    
    # Categorize severity
    critical = [i for i in all_issues if 'missing' in i['detail'].lower() or 'not found' in i['detail'].lower() or 'total' in i['check'].lower()]
    important = [i for i in all_issues if i not in critical and ('count' in i['check'].lower() or 'amount' in i['check'].lower())]
    minor = [i for i in all_issues if i not in critical and i not in important]
    
    report += f"### 🔴 Critical ({len(critical)})\n"
    for i in critical:
        report += f"- [{i['month']}] {i['check']}: {i['detail']}\n"
    
    report += f"\n### 🟡 Important ({len(important)})\n"
    for i in important:
        report += f"- [{i['month']}] {i['check']}: {i['detail']}\n"
    
    report += f"\n### 🟢 Minor ({len(minor)})\n"
    for i in minor:
        report += f"- [{i['month']}] {i['check']}: {i['detail']}\n"
    
    report += f"""
---

## 📈 Summary

- **Total checks performed:** {total_max}
- **Total checks passed:** {total_score}
- **Total checks failed:** {total_max - total_score}
- **Pass rate:** {round(100*total_score/total_max) if total_max > 0 else 0}%
- **Final score (normalized):** {final_score}/1000

### Conclusion

{pass_fail}

{'The sheets are in good overall shape with mostly formatting and minor structural issues.' if final_score >= 700 else 'Significant issues remain that need attention before these sheets can be considered production-ready.'}

---
*Report generated automatically by Sierra audit system*
"""
    
    # Write report
    with open('data/final-audit-report.md', 'w') as f:
        f.write(report)
    
    print(f"\nReport written to data/final-audit-report.md")
    print(f"FINAL SCORE: {final_score}/1000 — {pass_fail}")
    
    # Also dump raw JSON for potential further analysis
    raw_output = {
        'score': final_score,
        'design': design_norm,
        'template': template_norm,
        'math': math_norm,
        'issues': all_issues,
        'per_sheet': [r.summary() for r in all_results]
    }
    with open('data/final-audit-raw.json', 'w') as f:
        json.dump(raw_output, f, indent=2, default=str)

if __name__ == '__main__':
    main()
