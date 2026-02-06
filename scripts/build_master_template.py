#!/usr/bin/env python3
"""
Build KuriosBrand Master Template Google Sheet.
Complete with all 8 tabs, formatting, data validation, and placeholder data.
"""

import json
import requests as req
import sys
import time

# ─── Configuration ───────────────────────────────────────────
TOKEN_PATH = '/home/ec2-user/.config/gcal-pro/token.json'
FOLDER_ID = '1XlNibgutZc0eVrI6tkgexTA3RusGepwX'
SHEET_TITLE = '📋 MASTER TEMPLATE — KuriosBrand Monthly Accounting'
OUTPUT_PATH = '/home/ec2-user/clawd/data/master-template-sheet-id.txt'

# ─── Colors (RGB 0-1 for Sheets API) ────────────────────────
C = {
    'navy':       {'red': 27/255, 'green': 42/255, 'blue': 74/255},
    'white':      {'red': 1.0, 'green': 1.0, 'blue': 1.0},
    'light_gray': {'red': 243/255, 'green': 243/255, 'blue': 243/255},
    'totals_bg':  {'red': 232/255, 'green': 237/255, 'blue': 245/255},
    'green_tab':  {'red': 52/255, 'green': 168/255, 'blue': 83/255},
    'orange_tab': {'red': 1.0, 'green': 109/255, 'blue': 1/255},
    'gray_tab':   {'red': 153/255, 'green': 153/255, 'blue': 153/255},
    'red_text':   {'red': 204/255, 'green': 0, 'blue': 0},
    'dk_green':   {'red': 0, 'green': 97/255, 'blue': 0},
    'black':      {'red': 0, 'green': 0, 'blue': 0},
    'green_bg':   {'red': 183/255, 'green': 225/255, 'blue': 183/255},
    'yellow_bg':  {'red': 255/255, 'green': 242/255, 'blue': 179/255},
    'red_bg':     {'red': 244/255, 'green': 199/255, 'blue': 195/255},
    'orange_bg':  {'red': 255/255, 'green': 229/255, 'blue': 194/255},
    'gray_bg':    {'red': 230/255, 'green': 230/255, 'blue': 230/255},
}

# Sheet IDs
SID = {
    'dashboard': 0, 'profit_first': 1, 'pareto': 2, 'biz_4991': 3,
    'personal_0068': 4, 'biz_cc_0678': 5, 'sapphire_4252': 6, 'raw_data': 7,
}

TAB_NAMES = [
    '📊 Dashboard', '💰 Profit First', '🎯 Pareto Analysis',
    '💼 Business 4991', '👤 Personal 0068', '💳 Biz CC 0678',
    '💎 Sapphire 4252', '📦 Raw Data',
]

BASE = 'https://sheets.googleapis.com/v4/spreadsheets'

# ─── Token Management ────────────────────────────────────────
def refresh_token():
    with open(TOKEN_PATH) as f:
        tok = json.load(f)
    resp = req.post('https://oauth2.googleapis.com/token', data={
        'client_id': tok['client_id'],
        'client_secret': tok['client_secret'],
        'refresh_token': tok['refresh_token'],
        'grant_type': 'refresh_token',
    })
    resp.raise_for_status()
    data = resp.json()
    tok['token'] = data['access_token']
    with open(TOKEN_PATH, 'w') as f:
        json.dump(tok, f)
    print(f"✅ Token refreshed")
    return data['access_token']

def headers(token):
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

# ─── Helper: format request builders ─────────────────────────
def cell_fmt(sheet_id, row, col, end_row, end_col, bg=None, fg=None, bold=False, font_size=10, halign=None, number_fmt=None, italic=False):
    """Build a repeatCell request."""
    cell = {'userEnteredFormat': {}}
    fmt = cell['userEnteredFormat']
    fields = []
    
    if bg:
        fmt['backgroundColor'] = C[bg]
        fields.append('userEnteredFormat.backgroundColor')
    if fg or bold or font_size != 10 or italic:
        fmt['textFormat'] = {}
        if fg:
            fmt['textFormat']['foregroundColor'] = C[fg]
            fields.append('userEnteredFormat.textFormat.foregroundColor')
        if bold:
            fmt['textFormat']['bold'] = True
            fields.append('userEnteredFormat.textFormat.bold')
        if italic:
            fmt['textFormat']['italic'] = True
            fields.append('userEnteredFormat.textFormat.italic')
        if font_size != 10:
            fmt['textFormat']['fontSize'] = font_size
            fields.append('userEnteredFormat.textFormat.fontSize')
        fmt['textFormat']['fontFamily'] = 'Arial'
        fields.append('userEnteredFormat.textFormat.fontFamily')
    if halign:
        fmt['horizontalAlignment'] = halign
        fields.append('userEnteredFormat.horizontalAlignment')
    if number_fmt:
        fmt['numberFormat'] = {'type': 'NUMBER', 'pattern': number_fmt}
        fields.append('userEnteredFormat.numberFormat')
    
    return {
        'repeatCell': {
            'range': {'sheetId': sheet_id, 'startRowIndex': row, 'endRowIndex': end_row, 'startColumnIndex': col, 'endColumnIndex': end_col},
            'cell': cell,
            'fields': ','.join(fields),
        }
    }

def col_width(sheet_id, col, width):
    return {
        'updateDimensionProperties': {
            'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col + 1},
            'properties': {'pixelSize': width},
            'fields': 'pixelSize',
        }
    }

def row_height(sheet_id, row, height):
    return {
        'updateDimensionProperties': {
            'range': {'sheetId': sheet_id, 'dimension': 'ROWS', 'startIndex': row, 'endIndex': row + 1},
            'properties': {'pixelSize': height},
            'fields': 'pixelSize',
        }
    }

def merge_cells(sheet_id, row, col, end_row, end_col):
    return {
        'mergeCells': {
            'range': {'sheetId': sheet_id, 'startRowIndex': row, 'endRowIndex': end_row, 'startColumnIndex': col, 'endColumnIndex': end_col},
            'mergeType': 'MERGE_ALL',
        }
    }

def freeze_rows(sheet_id, count):
    return {
        'updateSheetProperties': {
            'properties': {'sheetId': sheet_id, 'gridProperties': {'frozenRowCount': count}},
            'fields': 'gridProperties.frozenRowCount',
        }
    }

def data_validation(sheet_id, row, end_row, col, values):
    return {
        'setDataValidation': {
            'range': {'sheetId': sheet_id, 'startRowIndex': row, 'endRowIndex': end_row, 'startColumnIndex': col, 'endColumnIndex': col + 1},
            'rule': {
                'condition': {
                    'type': 'ONE_OF_LIST',
                    'values': [{'userEnteredValue': v} for v in values],
                },
                'showCustomUi': True,
                'strict': False,
            }
        }
    }

# ─── Create Spreadsheet ──────────────────────────────────────
def create_spreadsheet(token):
    tab_colors = [
        None, C['green_tab'], C['orange_tab'], C['navy'], C['navy'], C['navy'], C['navy'], C['gray_tab'],
    ]
    
    sheets = []
    for i, (name, sid_key) in enumerate(zip(TAB_NAMES, SID.keys())):
        props = {
            'sheetId': SID[sid_key],
            'title': name,
            'gridProperties': {'frozenRowCount': 1, 'rowCount': 200, 'columnCount': 10},
        }
        if tab_colors[i]:
            props['tabColor'] = tab_colors[i]
        sheets.append({'properties': props})
    
    body = {'properties': {'title': SHEET_TITLE}, 'sheets': sheets}
    
    resp = req.post(BASE, headers=headers(token), json=body)
    resp.raise_for_status()
    sid = resp.json()['spreadsheetId']
    print(f"✅ Spreadsheet created: {sid}")
    return sid

# ─── Build Dashboard Data ────────────────────────────────────
def build_dashboard_data():
    """Returns (rows, row_types) where row_types maps row_index to type."""
    rows = []
    types = {}  # row_idx -> 'section_header' | 'col_header' | 'subtotal' | 'total' | 'data' | 'blank'
    
    def add(row, rtype='data'):
        types[len(rows)] = rtype
        rows.append(row)
    
    # ── SECTION A: INCOME SUMMARY ──
    add(['💰 SECTION A: INCOME SUMMARY', '', '', '', ''], 'section_header')
    add(['Source', 'Method', 'Amount', '% of Total', 'Notes'], 'col_header')
    add(['Client A — MVA Retainer', 'Stripe', '$5,000.00', '50.0%', 'Monthly retainer'])
    add(['Client B — SEO Services', 'Stripe', '$2,500.00', '25.0%', 'Monthly retainer'])
    add(['Client C — One-Time Project', 'Zelle', '$2,500.00', '25.0%', 'Website build'])
    add(['TOTAL INCOME', '', '$10,000.00', '100.0%', ''], 'total')
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION B: BUSINESS EXPENSES ──
    add(['📊 SECTION B: BUSINESS EXPENSES', '', '', '', ''], 'section_header')
    add(['Category', 'Vendor', 'Amount', 'Recurring?', 'Notes'], 'col_header')
    add(['📱 SaaS & Tools', 'HighLevel', '-$497.00', 'Monthly', 'CRM + funnels'])
    add(['📱 SaaS & Tools', 'ChatGPT Plus', '-$20.00', 'Monthly', 'AI assistant'])
    add(['📱 SaaS & Tools', 'Namecheap', '-$45.99', 'Annual', 'Domains'])
    add(['SUBTOTAL: 📱 SaaS & Tools', '', '-$562.99', '', ''], 'subtotal')
    add(['📣 Marketing / Ads', 'Meta Ads', '-$3,500.00', 'Variable', 'MVA campaigns'])
    add(['📣 Marketing / Ads', 'Google Ads', '-$500.00', 'Variable', 'Local services'])
    add(['SUBTOTAL: 📣 Marketing / Ads', '', '-$4,000.00', '', ''], 'subtotal')
    add(['🏢 Operations', 'Zoom Pro', '-$15.99', 'Monthly', 'Video calls'])
    add(['🏢 Operations', 'Virtual Mailbox', '-$29.00', 'Monthly', 'Business address'])
    add(['SUBTOTAL: 🏢 Operations', '', '-$44.99', '', ''], 'subtotal')
    add(['💳 Debt Payments (Business)', 'Stripe Capital', '-$330.00', 'Auto', '20% of deposits'])
    add(['SUBTOTAL: 💳 Debt Payments', '', '-$330.00', '', ''], 'subtotal')
    add(['💰 Business Fees & Interest', 'Chase', '-$15.00', '', 'Service fee'])
    add(['SUBTOTAL: 💰 Fees & Interest', '', '-$15.00', '', ''], 'subtotal')
    add(['🏧 Business ATM / Cash', 'Chase ATM', '-$200.00', '', 'Cash withdrawal'])
    add(['SUBTOTAL: 🏧 ATM / Cash', '', '-$200.00', '', ''], 'subtotal')
    add(['TOTAL BUSINESS EXPENSES', '', '-$5,152.98', '', ''], 'total')
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION C: PERSONAL EXPENSES ──
    add(['👤 SECTION C: PERSONAL EXPENSES', '', '', '', ''], 'section_header')
    add(['Category', 'Vendor', 'Amount', 'Recurring?', 'Notes'], 'col_header')
    add(['📈 Investments', 'Robinhood', '-$150.00', 'Daily', 'Stock purchases'])
    add(['📈 Investments', 'Acorns', '-$50.00', 'Daily', 'Roundups + recurring'])
    add(['SUBTOTAL: 📈 Investments', '', '-$200.00', '', ''], 'subtotal')
    add(['🏠 Living / Local', 'Rent', '-$1,200.00', 'Monthly', 'Apartment'])
    add(['🏠 Living / Local', 'Electric / Water', '-$150.00', 'Monthly', 'Utilities'])
    add(['SUBTOTAL: 🏠 Living / Local', '', '-$1,350.00', '', ''], 'subtotal')
    add(['🍔 Food & Dining', 'Grocery Stores', '-$400.00', 'Weekly', 'HEB / Walmart'])
    add(['🍔 Food & Dining', 'Restaurants', '-$200.00', 'Variable', 'Eating out'])
    add(['SUBTOTAL: 🍔 Food & Dining', '', '-$600.00', '', ''], 'subtotal')
    add(['📺 Subscriptions', 'YouTube Premium', '-$13.99', 'Monthly', ''])
    add(['📺 Subscriptions', 'Spotify', '-$10.99', 'Monthly', ''])
    add(['SUBTOTAL: 📺 Subscriptions', '', '-$24.98', '', ''], 'subtotal')
    add(['✈️ Travel', 'Gas Stations', '-$200.00', 'Variable', 'Monthly gas'])
    add(['SUBTOTAL: ✈️ Travel', '', '-$200.00', '', ''], 'subtotal')
    add(['🛍️ Shopping & Misc', 'Amazon', '-$150.00', 'Variable', 'Various'])
    add(['SUBTOTAL: 🛍️ Shopping & Misc', '', '-$150.00', '', ''], 'subtotal')
    add(['💳 CC Payments', 'Sapphire Payment', '-$500.00', 'Monthly', 'Statement payment'])
    add(['SUBTOTAL: 💳 CC Payments', '', '-$500.00', '', ''], 'subtotal')
    add(['💰 CC Interest & Fees', 'Sapphire Interest', '-$45.00', 'Monthly', ''])
    add(['SUBTOTAL: 💰 CC Interest & Fees', '', '-$45.00', '', ''], 'subtotal')
    add(['🏧 ATM / Cash / FX', 'Chase ATM', '-$100.00', '', 'Cash withdrawal'])
    add(['SUBTOTAL: 🏧 ATM / Cash / FX', '', '-$100.00', '', ''], 'subtotal')
    add(['TOTAL PERSONAL EXPENSES', '', '-$3,169.98', '', ''], 'total')
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION D: KEY METRICS ──
    add(['📈 SECTION D: KEY METRICS', '', '', '', ''], 'section_header')
    add(['Metric', 'Value', 'Target', 'Status', ''], 'col_header')
    add(['Total Revenue', '$10,000.00', '', '', ''])
    add(['Total Business Expenses', '-$5,152.98', '', '', ''])
    add(['Business Profit', '$4,847.02', '', '', ''])
    add(['Profit Margin', '48.5%', '50%+', '🟡', ''])
    add(['Meta Ad Spend', '-$3,500.00', '', '', ''])
    add(['Cost Per Call', '$175.00', '<$150', '🔴', ''])
    add(['Revenue Per Client', '$3,333.33', '', '', ''])
    add(['MoM Revenue Change', '+12.5%', '', '🟢', ''])
    add(['Burn Rate', '$8,322.96/mo', '', '', ''])
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION E: MONEY FLOW ──
    add(['🔄 SECTION E: MONEY FLOW', '', '', '', ''], 'section_header')
    add(['Flow', 'From', 'To', 'Amount', 'Notes'], 'col_header')
    add(['Business → Personal', '4991', '0068', '$3,000.00', "Owner's draw"])
    add(['Business → Tax', '4991', 'Wells Fargo', '$500.00', 'Tax set-aside'])
    add(['Personal → Investments', '0068', 'Robinhood', '$150.00', 'Daily buys'])
    add(['Personal → Investments', '0068', 'Acorns', '$50.00', 'Daily + roundups'])
    add(['Personal → Savings', '0068', '7036', '$200.00', 'Auto-saves'])
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION F: DEBT TRACKING (7 cols) ──
    add(['🏦 SECTION F: DEBT TRACKING', '', '', '', '', '', ''], 'section_header')
    add(['Account', 'Balance', 'Limit', 'Utilization', 'Min Payment', 'Actual Payment', 'Notes'], 'col_header')
    add(['Student Loans', '$28,500.00', '—', '—', '$350.00', '$350.00', ''])
    add(['Discover 6820', '$4,200.00', '$6,300.00', '66.7%', '$105.00', '$200.00', ''])
    add(['Sapphire 4252', '$5,800.00', '$9,300.00', '62.4%', '$145.00', '$500.00', ''])
    add(['Ink 0678', '$3,200.00', '$5,500.00', '58.2%', '$80.00', '$250.00', ''])
    add(['Stripe Loan', '$4,705.00', '—', '—', '20% of deps', '$330.00', ''])
    add(['TOTAL DEBT', '$46,405.00', '', '', '', '$1,630.00', ''], 'total')
    add(['', '', '', '', '', '', ''], 'blank')
    add(['', '', '', '', '', '', ''], 'blank')
    
    # ── SECTION G: ACCOUNT BALANCES ──
    add(['💰 SECTION G: ACCOUNT BALANCES', '', '', '', ''], 'section_header')
    add(['Account', 'Opening', 'Closing', 'Change', 'Notes'], 'col_header')
    add(['Chase Biz 4991', '$8,500.00', '$6,847.02', '-$1,652.98', ''])
    add(['Chase Personal 0068', '$3,200.00', '$2,530.02', '-$669.98', ''])
    add(['Chase Savings 7036', '$1,500.00', '$1,700.00', '+$200.00', ''])
    add(['Wells Fargo Tax', '$2,000.00', '$2,500.00', '+$500.00', ''])
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION H: ASSETS & NET WORTH ──
    add(['💎 SECTION H: ASSETS & NET WORTH', '', '', '', ''], 'section_header')
    add(['Asset', 'Value', 'Change', 'Notes', ''], 'col_header')
    add(['Business Equity', '$150,000.00', '—', 'Rank & rent portfolio', ''])
    add(['Robinhood', '$4,500.00', '+$350.00', 'Stocks', ''])
    add(['Acorns', '$2,800.00', '+$175.00', 'Index funds', ''])
    add(['Bitcoin', '$3,200.00', '+$400.00', '0.03 BTC', ''])
    add(['Solana', '$1,500.00', '-$200.00', '10 SOL', ''])
    add(['Cash (all accounts)', '$13,577.04', '', 'Sum of Section G', ''])
    add(['TOTAL ASSETS', '$175,577.04', '', '', ''], 'total')
    add(['TOTAL LIABILITIES', '-$46,405.00', '', 'From Section F', ''], 'total')
    add(['NET WORTH', '$129,172.04', '+$2,150.00', '', ''], 'total')
    add(['', '', '', '', ''], 'blank')
    add(['', '', '', '', ''], 'blank')
    
    # ── SECTION I: ACTION ITEMS ──
    add(['📝 SECTION I: ACTION ITEMS', '', '', '', ''], 'section_header')
    add(['Priority', 'Action', 'Status', 'Due', 'Notes'], 'col_header')
    add(['🔴 HIGH', 'Reduce Meta Ad spend or improve ROAS', '⬜', '', 'Currently 35% of revenue'])
    add(['🔴 HIGH', 'Pay down Discover card', '⬜', '', 'Highest utilization at 66.7%'])
    add(['🟡 MED', 'Cancel unused SaaS subscriptions', '⬜', '', 'Audit all tools'])
    add(['🟡 MED', 'Increase owner pay to 50% target', '⬜', '', 'Currently at 30%'])
    add(['🟢 LOW', 'Set up Discover auto-pay', '⬜', '', 'Avoid late fees'])
    add(['🟢 LOW', 'Review tax set-aside percentage', '⬜', '', 'May need to increase to 15%'])
    
    return rows, types

def build_profit_first_data():
    return [
        ['💰 PROFIT FIRST ALLOCATION', '', '', '', '', ''],
        ['Bucket', 'Target %', 'Current %', 'Target Amount', 'Actual Amount', 'Gap'],
        ['Revenue (TAPs)', '100%', '100%', '$10,000.00', '$10,000.00', '—'],
        ['Profit', '5%', '3.0%', '$500.00', '$300.00', '-$200.00'],
        ["Owner's Comp", '50%', '30.0%', '$5,000.00', '$3,000.00', '-$2,000.00'],
        ['Tax', '15%', '5.0%', '$1,500.00', '$500.00', '-$1,000.00'],
        ['OpEx', '30%', '51.5%', '$3,000.00', '$5,152.98', '+$2,152.98'],
        ['', '', '', '', '', ''],
        ['ANALYSIS & NOTES:', '', '', '', '', ''],
        ['• OpEx is significantly over target — reduce SaaS and/or Ad spend', '', '', '', '', ''],
        ["• Owner's comp below target — business reinvesting too heavily", '', '', '', '', ''],
        ['• Tax set-aside needs to increase from 5% to 15%', '', '', '', '', ''],
        ['• Profit allocation should be prioritized — pay yourself first', '', '', '', '', ''],
    ]

def build_pareto_data():
    return [
        ['🎯 PARETO ANALYSIS — TOP EXPENSES', '', '', '', '', ''],
        ['Rank', 'Expense', 'Amount', 'Cumulative', 'Cum %', 'Category'],
        ['1', 'Meta Ads', '$3,500.00', '$3,500.00', '42.1%', '📣 Marketing'],
        ['2', 'Rent', '$1,200.00', '$4,700.00', '56.5%', '🏠 Living'],
        ['3', 'Google Ads', '$500.00', '$5,200.00', '62.5%', '📣 Marketing'],
        ['4', 'Sapphire Payment', '$500.00', '$5,700.00', '68.6%', '💳 CC Payment'],
        ['5', 'HighLevel', '$497.00', '$6,197.00', '74.5%', '📱 SaaS'],
        ['6', 'Grocery Stores', '$400.00', '$6,597.00', '79.3%', '🍔 Food'],
        ['7', 'Stripe Capital', '$330.00', '$6,927.00', '83.3%', '💳 Debt'],
        ['8', 'Restaurants', '$200.00', '$7,127.00', '85.7%', '🍔 Food'],
        ['9', 'ATM Cash (Biz)', '$200.00', '$7,327.00', '88.1%', '🏧 ATM'],
        ['10', 'Gas Stations', '$200.00', '$7,527.00', '90.5%', '✈️ Travel'],
        ['11', 'Robinhood', '$150.00', '$7,677.00', '92.3%', '📈 Investment'],
        ['12', 'Amazon', '$150.00', '$7,827.00', '94.1%', '🛍️ Shopping'],
        ['13', 'Electric / Water', '$150.00', '$7,977.00', '95.9%', '🏠 Living'],
        ['14', 'ATM Cash (Personal)', '$100.00', '$8,077.00', '97.1%', '🏧 ATM'],
        ['15', 'Acorns', '$50.00', '$8,127.00', '97.7%', '📈 Investment'],
        ['16', 'Namecheap', '$45.99', '$8,172.99', '98.3%', '📱 SaaS'],
        ['17', 'Sapphire Interest', '$45.00', '$8,217.99', '98.8%', '💰 Fees'],
        ['18', 'Virtual Mailbox', '$29.00', '$8,246.99', '99.2%', '🏢 Operations'],
        ['19', 'ChatGPT Plus', '$20.00', '$8,266.99', '99.4%', '📱 SaaS'],
        ['20', 'Zoom Pro', '$15.99', '$8,282.98', '99.6%', '🏢 Operations'],
        ['21', 'Chase Service Fee', '$15.00', '$8,297.98', '99.8%', '💰 Fees'],
        ['22', 'YouTube Premium', '$13.99', '$8,311.97', '100.0%', '📺 Subs'],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['80% LINE: Top 6 expenses account for 79.3% of all spending', '', '', '', '', ''],
        ['➡️ Focus cost reduction efforts on Meta Ads, Rent, Google Ads, and SaaS', '', '', '', '', ''],
    ]

def build_transaction_data(tab_type):
    """Build transaction data. tab_type: 'biz_4991', 'personal_0068', 'biz_cc_0678', 'sapphire_4252'"""
    header = ['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']
    
    if tab_type == 'biz_4991':
        return [header,
            ['01/02/2026', 'Stripe Deposit', '💵 Revenue', '$5,000.00', '$13,500.00', 'Client A retainer'],
            ['01/03/2026', 'Stripe Deposit', '💵 Revenue', '$2,500.00', '$16,000.00', 'Client B retainer'],
            ['01/05/2026', 'Zelle — Client C', '💵 Revenue', '$2,500.00', '$18,500.00', 'Website project'],
            ['01/05/2026', 'Meta Ads', '📣 Marketing / Ads', '-$3,500.00', '$15,000.00', 'MVA campaigns'],
            ['01/06/2026', 'HighLevel', '📱 SaaS & Tools', '-$497.00', '$14,503.00', 'CRM monthly'],
            ['01/06/2026', 'Google Ads', '📣 Marketing / Ads', '-$500.00', '$14,003.00', 'Local services'],
            ['01/07/2026', 'Transfer to Personal', '🔄 Transfer', '-$3,000.00', '$11,003.00', "Owner's draw"],
            ['01/08/2026', 'Namecheap', '📱 SaaS & Tools', '-$45.99', '$10,957.01', 'Domain renewals'],
            ['01/10/2026', 'ChatGPT Plus', '📱 SaaS & Tools', '-$20.00', '$10,937.01', 'AI tools'],
            ['01/10/2026', 'Zoom Pro', '🏢 Operations', '-$15.99', '$10,921.02', 'Video calls'],
            ['01/12/2026', 'Virtual Mailbox', '🏢 Operations', '-$29.00', '$10,892.02', 'Business address'],
            ['01/15/2026', 'Stripe Capital', '💳 Debt Payment', '-$330.00', '$10,562.02', 'Auto-deduction'],
            ['01/15/2026', 'Transfer to Tax', '🔄 Transfer', '-$500.00', '$10,062.02', 'Tax set-aside'],
            ['01/20/2026', 'Chase ATM', '🏧 ATM / Cash', '-$200.00', '$9,862.02', 'Cash withdrawal'],
            ['01/25/2026', 'Chase', '💰 Fees & Interest', '-$15.00', '$9,847.02', 'Service fee'],
        ]
    elif tab_type == 'personal_0068':
        return [header,
            ['01/01/2026', 'Rent', '🏠 Living / Local', '-$1,200.00', '$2,000.00', 'January rent'],
            ['01/02/2026', 'Robinhood', '📈 Investment', '-$150.00', '$3,050.00', 'Stock purchases'],
            ['01/02/2026', 'Acorns', '📈 Investment', '-$50.00', '$3,000.00', 'Roundups'],
            ['01/05/2026', 'Electric Co', '🏠 Living / Local', '-$100.00', '$5,900.00', 'Electricity'],
            ['01/05/2026', 'Water Utility', '🏠 Living / Local', '-$50.00', '$5,850.00', 'Water bill'],
            ['01/06/2026', 'YouTube Premium', '📺 Subscription', '-$13.99', '$5,836.01', ''],
            ['01/06/2026', 'Spotify', '📺 Subscription', '-$10.99', '$5,825.02', ''],
            ['01/07/2026', 'Transfer from Business', '💵 Income', '$3,000.00', '$6,200.00', "Owner's draw"],
            ['01/08/2026', 'HEB Grocery', '🍔 Food & Dining', '-$250.00', '$5,950.00', 'Groceries'],
            ['01/08/2026', 'Amazon', '🛍️ Shopping & Misc', '-$75.00', '$5,875.00', 'Office supplies'],
            ['01/10/2026', 'Restaurant', '🍔 Food & Dining', '-$75.00', '$5,800.00', 'Dinner'],
            ['01/12/2026', 'Gas Station', '✈️ Travel', '-$60.00', '$5,740.00', 'Gas'],
            ['01/15/2026', 'HEB Grocery', '🍔 Food & Dining', '-$150.00', '$5,590.00', 'Groceries'],
            ['01/15/2026', 'Transfer to Savings', '🔄 Transfer', '-$200.00', '$5,390.00', 'Auto-save'],
            ['01/18/2026', 'Amazon', '🛍️ Shopping & Misc', '-$75.00', '$5,315.00', 'Household'],
            ['01/20/2026', 'Restaurant', '🍔 Food & Dining', '-$125.00', '$5,190.00', 'Lunch + dinner'],
            ['01/20/2026', 'Chase ATM', '🏧 ATM / Cash / FX', '-$100.00', '$5,090.00', 'Cash'],
            ['01/22/2026', 'Gas Station', '✈️ Travel', '-$55.00', '$5,035.00', 'Gas'],
            ['01/25/2026', 'Sapphire Payment', '💳 CC Payment', '-$500.00', '$4,535.00', 'Statement payment'],
            ['01/25/2026', 'Sapphire Interest', '💰 Interest & Fees', '-$45.00', '$4,490.00', ''],
            ['01/28/2026', 'Gas Station', '✈️ Travel', '-$85.00', '$4,405.00', 'Gas'],
        ]
    elif tab_type == 'biz_cc_0678':
        return [header,
            ['01/03/2026', 'Namecheap', '📱 SaaS & Tools', '-$45.99', '$3,245.99', 'Domain renewals'],
            ['01/05/2026', 'Canva Pro', '📱 SaaS & Tools', '-$12.99', '$3,258.98', 'Design tools'],
            ['01/08/2026', 'Office Depot', '🏢 Operations', '-$89.00', '$3,347.98', 'Printer supplies'],
            ['01/10/2026', 'Uber (business)', '🏢 Operations', '-$35.00', '$3,382.98', 'Client meeting'],
            ['01/15/2026', 'Statement Payment', '💳 Debt Payment', '$250.00', '$2,950.00', 'Payment received'],
            ['01/18/2026', 'Meta Ads (overflow)', '📣 Marketing / Ads', '-$200.00', '$3,150.00', 'Additional spend'],
            ['01/20/2026', 'Ink Interest', '💰 Fees & Interest', '-$42.00', '$3,192.00', 'Monthly interest'],
            ['01/25/2026', 'Staples', '🏢 Operations', '-$28.00', '$3,220.00', 'Office supplies'],
        ]
    elif tab_type == 'sapphire_4252':
        return [header,
            ['01/02/2026', 'Uber Eats', '🍔 Food & Dining', '-$45.00', '$5,845.00', '3x points'],
            ['01/05/2026', 'Southwest Airlines', '✈️ Travel', '-$350.00', '$6,195.00', 'Austin → LA flight'],
            ['01/08/2026', 'Hotel Tonight', '✈️ Travel', '-$189.00', '$6,384.00', '2-night stay'],
            ['01/10/2026', 'Lyft', '✈️ Travel', '-$28.00', '$6,412.00', 'Airport ride'],
            ['01/12/2026', 'Target', '🛍️ Shopping & Misc', '-$67.00', '$6,479.00', 'Household items'],
            ['01/15/2026', 'Netflix', '📺 Subscription', '-$15.49', '$6,494.49', ''],
            ['01/15/2026', 'iCloud', '📺 Subscription', '-$2.99', '$6,497.48', ''],
            ['01/20/2026', 'Whole Foods', '🍔 Food & Dining', '-$95.00', '$6,592.48', 'Groceries'],
            ['01/22/2026', 'Statement Payment', '💳 CC Payment', '$500.00', '$5,300.00', 'Payment received'],
            ['01/25/2026', 'Sapphire Interest', '💰 Interest & Fees', '-$48.00', '$5,348.00', 'Monthly interest'],
            ['01/28/2026', 'Amazon', '🛍️ Shopping & Misc', '-$52.00', '$5,400.00', 'Electronics'],
        ]

def build_raw_data():
    return [
        ['=== CHASE BUSINESS 4991 ===', '', '', '', '', ''],
        ['(Raw CSV data will be pasted here during monthly processing)', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['=== CHASE PERSONAL 0068 ===', '', '', '', '', ''],
        ['(Raw CSV data will be pasted here during monthly processing)', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['=== CHASE INK CC 0678 ===', '', '', '', '', ''],
        ['(Raw CSV data will be pasted here during monthly processing)', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['', '', '', '', '', ''],
        ['=== CHASE SAPPHIRE 4252 ===', '', '', '', '', ''],
        ['(Raw CSV data will be pasted here during monthly processing)', '', '', '', '', ''],
    ]

# ─── Populate All Data ───────────────────────────────────────
def populate_data(token, spreadsheet_id):
    dashboard_rows, _ = build_dashboard_data()
    
    value_data = [
        {'range': f"'{TAB_NAMES[0]}'!A1", 'values': dashboard_rows},
        {'range': f"'{TAB_NAMES[1]}'!A1", 'values': build_profit_first_data()},
        {'range': f"'{TAB_NAMES[2]}'!A1", 'values': build_pareto_data()},
        {'range': f"'{TAB_NAMES[3]}'!A1", 'values': build_transaction_data('biz_4991')},
        {'range': f"'{TAB_NAMES[4]}'!A1", 'values': build_transaction_data('personal_0068')},
        {'range': f"'{TAB_NAMES[5]}'!A1", 'values': build_transaction_data('biz_cc_0678')},
        {'range': f"'{TAB_NAMES[6]}'!A1", 'values': build_transaction_data('sapphire_4252')},
        {'range': f"'{TAB_NAMES[7]}'!A1", 'values': build_raw_data()},
    ]
    
    resp = req.post(
        f'{BASE}/{spreadsheet_id}/values:batchUpdate',
        headers=headers(token),
        json={'valueInputOption': 'USER_ENTERED', 'data': value_data},
    )
    resp.raise_for_status()
    print(f"✅ All data populated")

# ─── Format Everything ────────────────────────────────────────
def format_spreadsheet(token, spreadsheet_id):
    reqs = []
    _, dash_types = build_dashboard_data()
    
    # ══════════════════════════════════════════════════════════
    # DASHBOARD FORMATTING
    # ══════════════════════════════════════════════════════════
    sid = SID['dashboard']
    
    # Set default font for whole sheet
    reqs.append(cell_fmt(sid, 0, 0, 200, 10, font_size=10, fg='black'))
    
    # Column widths for dashboard (wider columns for multi-col layout)
    dash_widths = [250, 200, 150, 130, 250, 130, 150]
    for i, w in enumerate(dash_widths):
        reqs.append(col_width(sid, i, w))
    
    # Unfreeze dashboard (no frozen row - section headers serve as context)
    # Actually spec says freeze row 1 on all tabs. But dashboard row 1 is a section header.
    # Let's keep frozen row 1 as set during creation.
    
    # Apply formatting based on row types
    for row_idx, rtype in dash_types.items():
        if rtype == 'section_header':
            # Determine how many columns this section header spans
            ncols = 7  # max columns (Section F has 7)
            reqs.append(cell_fmt(sid, row_idx, 0, row_idx + 1, ncols, bg='navy', fg='white', bold=True, font_size=14))
            reqs.append(merge_cells(sid, row_idx, 0, row_idx + 1, ncols))
            reqs.append(row_height(sid, row_idx, 36))
        elif rtype == 'col_header':
            ncols = 7
            reqs.append(cell_fmt(sid, row_idx, 0, row_idx + 1, ncols, bg='light_gray', fg='black', bold=True, font_size=11, halign='CENTER'))
            reqs.append(row_height(sid, row_idx, 28))
        elif rtype == 'subtotal':
            reqs.append(cell_fmt(sid, row_idx, 0, row_idx + 1, 7, bg='light_gray', bold=True, font_size=10))
        elif rtype == 'total':
            reqs.append(cell_fmt(sid, row_idx, 0, row_idx + 1, 7, bg='totals_bg', bold=True, font_size=11))
    
    # Currency formatting for Amount columns on dashboard (col C = index 2 for sections A-E, col B for F-H)
    # This is approximate - apply currency format to columns that have $ values
    # Col C (index 2) for most sections, col B (index 1) for some
    # Actually let's just format broadly - currency columns
    for row_idx, rtype in dash_types.items():
        if rtype in ('data', 'subtotal', 'total'):
            # Format column C (Amount) as currency  
            reqs.append(cell_fmt(sid, row_idx, 2, row_idx + 1, 3, number_fmt='$#,##0.00;[Red]($#,##0.00)'))
    
    # ══════════════════════════════════════════════════════════
    # PROFIT FIRST FORMATTING
    # ══════════════════════════════════════════════════════════
    sid = SID['profit_first']
    pf_widths = [200, 120, 120, 160, 160, 160]
    for i, w in enumerate(pf_widths):
        reqs.append(col_width(sid, i, w))
    
    # Title row
    reqs.append(cell_fmt(sid, 0, 0, 1, 6, bg='navy', fg='white', bold=True, font_size=14))
    reqs.append(merge_cells(sid, 0, 0, 1, 6))
    reqs.append(row_height(sid, 0, 36))
    
    # Column headers
    reqs.append(cell_fmt(sid, 1, 0, 2, 6, bg='navy', fg='white', bold=True, font_size=11, halign='CENTER'))
    reqs.append(row_height(sid, 1, 30))
    
    # Data rows
    reqs.append(cell_fmt(sid, 2, 0, 7, 6, font_size=10))
    
    # Currency columns D, E, F (indices 3, 4, 5)
    reqs.append(cell_fmt(sid, 2, 3, 7, 6, number_fmt='$#,##0.00;[Red]($#,##0.00)'))
    
    # Revenue row - totals style
    reqs.append(cell_fmt(sid, 2, 0, 3, 6, bg='totals_bg', bold=True))
    
    # OpEx row - highlight as over target (red bg)
    reqs.append(cell_fmt(sid, 6, 0, 7, 6, bg='red_bg', bold=True))
    
    # Off-target rows
    reqs.append(cell_fmt(sid, 3, 0, 4, 6, bg='yellow_bg'))  # Profit - close to target
    reqs.append(cell_fmt(sid, 4, 0, 5, 6, bg='red_bg'))      # Owner's Comp - far off
    reqs.append(cell_fmt(sid, 5, 0, 6, 6, bg='red_bg'))      # Tax - far off
    
    # Notes section
    reqs.append(cell_fmt(sid, 8, 0, 9, 6, bold=True, font_size=11))
    reqs.append(cell_fmt(sid, 9, 0, 13, 6, font_size=10, italic=True))
    
    # ══════════════════════════════════════════════════════════
    # PARETO ANALYSIS FORMATTING
    # ══════════════════════════════════════════════════════════
    sid = SID['pareto']
    pareto_widths = [60, 200, 130, 130, 100, 180]
    for i, w in enumerate(pareto_widths):
        reqs.append(col_width(sid, i, w))
    
    # Title row
    reqs.append(cell_fmt(sid, 0, 0, 1, 6, bg='navy', fg='white', bold=True, font_size=14))
    reqs.append(merge_cells(sid, 0, 0, 1, 6))
    reqs.append(row_height(sid, 0, 36))
    
    # Column headers
    reqs.append(cell_fmt(sid, 1, 0, 2, 6, bg='navy', fg='white', bold=True, font_size=11, halign='CENTER'))
    reqs.append(row_height(sid, 1, 30))
    
    # Data rows
    reqs.append(cell_fmt(sid, 2, 0, 24, 6, font_size=10))
    
    # Currency columns (Amount=2, Cumulative=3)
    reqs.append(cell_fmt(sid, 2, 2, 24, 4, number_fmt='$#,##0.00'))
    
    # Rank column center
    reqs.append(cell_fmt(sid, 2, 0, 24, 1, halign='CENTER'))
    
    # Items above 80% line (rows 2-7, indices 2-8) - orange bg
    reqs.append(cell_fmt(sid, 2, 0, 8, 6, bg='orange_bg'))
    
    # Items below 80% line - gray bg
    reqs.append(cell_fmt(sid, 8, 0, 24, 6, bg='gray_bg'))
    
    # 80% line note rows
    reqs.append(cell_fmt(sid, 26, 0, 28, 6, bold=True, font_size=11, italic=True))
    
    # ══════════════════════════════════════════════════════════
    # TRANSACTION TABS FORMATTING (4 tabs)
    # ══════════════════════════════════════════════════════════
    txn_tabs = [
        (SID['biz_4991'], 16),
        (SID['personal_0068'], 22),
        (SID['biz_cc_0678'], 9),
        (SID['sapphire_4252'], 12),
    ]
    txn_widths = [110, 250, 250, 130, 130, 250]
    
    for sid, data_rows in txn_tabs:
        # Column widths
        for i, w in enumerate(txn_widths):
            reqs.append(col_width(sid, i, w))
        
        # Header row - navy bg, white text, bold 11pt
        reqs.append(cell_fmt(sid, 0, 0, 1, 6, bg='navy', fg='white', bold=True, font_size=11, halign='CENTER'))
        reqs.append(row_height(sid, 0, 30))
        
        # Data font
        reqs.append(cell_fmt(sid, 1, 0, data_rows, 6, font_size=10))
        
        # Date column format
        reqs.append(cell_fmt(sid, 1, 0, data_rows, 1, number_fmt='MM/DD/YYYY'))
        
        # Amount column (D = index 3)
        reqs.append(cell_fmt(sid, 1, 3, data_rows, 4, number_fmt='$#,##0.00;[Red]($#,##0.00)', halign='RIGHT'))
        
        # Balance column (E = index 4)
        reqs.append(cell_fmt(sid, 1, 4, data_rows, 5, number_fmt='$#,##0.00', halign='RIGHT'))
    
    # ══════════════════════════════════════════════════════════
    # RAW DATA TAB FORMATTING
    # ══════════════════════════════════════════════════════════
    sid = SID['raw_data']
    # Section label rows
    for row in [0, 5, 10, 15]:
        reqs.append(cell_fmt(sid, row, 0, row + 1, 6, bg='navy', fg='white', bold=True, font_size=12))
        reqs.append(merge_cells(sid, row, 0, row + 1, 6))
        reqs.append(row_height(sid, row, 32))
    
    # Placeholder text rows
    for row in [1, 6, 11, 16]:
        reqs.append(cell_fmt(sid, row, 0, row + 1, 6, font_size=10, italic=True, fg='gray_tab'))
    
    # Column widths
    raw_widths = [200, 200, 200, 130, 130, 200]
    for i, w in enumerate(raw_widths):
        reqs.append(col_width(sid, i, w))
    
    # ══════════════════════════════════════════════════════════
    # GLOBAL: Set default font for all sheets
    # ══════════════════════════════════════════════════════════
    for sid_val in SID.values():
        reqs.append({
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sid_val,
                    'gridProperties': {'frozenRowCount': 1},
                },
                'fields': 'gridProperties.frozenRowCount',
            }
        })
    
    # Send all formatting requests
    # Split into chunks to avoid hitting size limits
    chunk_size = 100
    for i in range(0, len(reqs), chunk_size):
        chunk = reqs[i:i+chunk_size]
        resp = req.post(
            f'{BASE}/{spreadsheet_id}:batchUpdate',
            headers=headers(token),
            json={'requests': chunk},
        )
        if resp.status_code != 200:
            print(f"⚠️  Format batch {i//chunk_size + 1} error: {resp.status_code}")
            print(resp.text[:500])
        else:
            print(f"✅ Format batch {i//chunk_size + 1} applied ({len(chunk)} requests)")
        time.sleep(0.3)

# ─── Data Validation ──────────────────────────────────────────
def add_validations(token, spreadsheet_id):
    biz_categories = [
        '📱 SaaS & Tools', '📣 Marketing / Ads', '🏢 Operations',
        '💳 Debt Payment', '💰 Fees & Interest', '🏧 ATM / Cash',
        '💵 Revenue', '🔄 Transfer',
    ]
    
    personal_categories = [
        '📈 Investment', '🏠 Living / Local', '🍔 Food & Dining',
        '📺 Subscription', '✈️ Travel', '🛍️ Shopping & Misc',
        '💳 CC Payment', '💰 Interest & Fees', '🏧 ATM / Cash / FX',
        '🔄 Transfer', '💵 Income',
    ]
    
    reqs = [
        # Business 4991 - Category column C (index 2), rows 2-100
        data_validation(SID['biz_4991'], 1, 100, 2, biz_categories),
        # Personal 0068
        data_validation(SID['personal_0068'], 1, 100, 2, personal_categories),
        # Biz CC 0678
        data_validation(SID['biz_cc_0678'], 1, 100, 2, biz_categories),
        # Sapphire 4252
        data_validation(SID['sapphire_4252'], 1, 100, 2, personal_categories),
    ]
    
    resp = req.post(
        f'{BASE}/{spreadsheet_id}:batchUpdate',
        headers=headers(token),
        json={'requests': reqs},
    )
    resp.raise_for_status()
    print(f"✅ Data validations added (4 tabs)")

# ─── Move to Folder ───────────────────────────────────────────
def move_to_folder(token, spreadsheet_id, folder_id):
    # First get current parents
    resp = req.get(
        f'https://www.googleapis.com/drive/v3/files/{spreadsheet_id}?fields=parents',
        headers=headers(token),
    )
    resp.raise_for_status()
    current_parents = resp.json().get('parents', [])
    
    # Move to target folder
    remove = ','.join(current_parents) if current_parents else ''
    resp = req.patch(
        f'https://www.googleapis.com/drive/v3/files/{spreadsheet_id}?addParents={folder_id}&removeParents={remove}',
        headers=headers(token),
    )
    resp.raise_for_status()
    print(f"✅ Moved to folder {folder_id}")

# ─── Main ────────────────────────────────────────────────────
def main():
    print("🚀 Building KuriosBrand Master Template...")
    print()
    
    # 1. Refresh token
    token = refresh_token()
    
    # 2. Create spreadsheet
    spreadsheet_id = create_spreadsheet(token)
    
    # 3. Populate data
    populate_data(token, spreadsheet_id)
    
    # 4. Apply formatting
    format_spreadsheet(token, spreadsheet_id)
    
    # 5. Add data validations
    add_validations(token, spreadsheet_id)
    
    # 6. Move to accounting folder
    move_to_folder(token, spreadsheet_id, FOLDER_ID)
    
    # 7. Save sheet ID
    url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit'
    with open(OUTPUT_PATH, 'w') as f:
        f.write(spreadsheet_id)
    
    print()
    print("=" * 60)
    print(f"✅ MASTER TEMPLATE CREATED SUCCESSFULLY")
    print(f"📋 Sheet ID: {spreadsheet_id}")
    print(f"🔗 URL: {url}")
    print(f"💾 ID saved to: {OUTPUT_PATH}")
    print("=" * 60)

if __name__ == '__main__':
    main()
