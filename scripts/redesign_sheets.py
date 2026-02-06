#!/usr/bin/env python3
"""Redesign August & September 2025 Accounting Sheets to match January 2026 format."""

import json
import requests
import time

# ── Auth ──────────────────────────────────────────────────────────────────────
def refresh_token():
    with open('/home/ec2-user/.config/gcal-pro/token.json') as f:
        creds = json.load(f)
    resp = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token'
    })
    return resp.json()['access_token']

TOKEN = refresh_token()
HEADERS = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}

def sheets_get(spreadsheet_id, range_str):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{requests.utils.quote(range_str)}'
    r = requests.get(url, headers=HEADERS)
    return r.json().get('values', [])

def sheets_update(spreadsheet_id, range_str, values):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{requests.utils.quote(range_str)}?valueInputOption=USER_ENTERED'
    body = {'values': values}
    r = requests.put(url, headers=HEADERS, json=body)
    return r.json()

def sheets_batch_update(spreadsheet_id, requests_list):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}:batchUpdate'
    body = {'requests': requests_list}
    r = requests.post(url, headers=HEADERS, json=body)
    if r.status_code != 200:
        print(f"ERROR: {r.status_code} {r.text[:500]}")
    return r.json()

def get_sheet_metadata(spreadsheet_id):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}?includeGridData=false'
    r = requests.get(url, headers=HEADERS)
    return r.json()

# ── Color helpers ─────────────────────────────────────────────────────────────
def rgb(hex_str):
    h = hex_str.lstrip('#')
    return {'red': int(h[0:2],16)/255, 'green': int(h[2:4],16)/255, 'blue': int(h[4:6],16)/255}

NAVY = rgb('#1B2A4A')
WHITE = rgb('#FFFFFF')
LIGHT_BLUE = rgb('#E8EDF3')
LIGHT_GREEN = rgb('#E8F5E9')
LIGHT_RED = rgb('#FFEBEE')
LIGHT_YELLOW = rgb('#FFF8E1')
LIGHT_GRAY = rgb('#F5F5F5')
LIGHT_PURPLE = rgb('#F3E5F5')
MEDIUM_GRAY = rgb('#EEEEEE')

def cell_format(bg=None, fg=None, bold=False, size=10, halign='LEFT', number_fmt=None, borders=False):
    fmt = {
        'textFormat': {'bold': bold, 'fontSize': size}
    }
    if fg:
        fmt['textFormat']['foregroundColorStyle'] = {'rgbColor': fg}
    if bg:
        fmt['backgroundColorStyle'] = {'rgbColor': bg}
    if halign:
        fmt['horizontalAlignment'] = halign
    if number_fmt:
        fmt['numberFormat'] = number_fmt
    return fmt

def format_range(sheet_id, start_row, end_row, start_col, end_col, fmt):
    return {
        'repeatCell': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'cell': {'userEnteredFormat': fmt},
            'fields': 'userEnteredFormat'
        }
    }

def merge_cells(sheet_id, start_row, end_row, start_col, end_col):
    return {
        'mergeCells': {
            'range': {
                'sheetId': sheet_id,
                'startRowIndex': start_row,
                'endRowIndex': end_row,
                'startColumnIndex': start_col,
                'endColumnIndex': end_col
            },
            'mergeType': 'MERGE_ALL'
        }
    }

def set_col_width(sheet_id, col, width):
    return {
        'updateDimensionProperties': {
            'range': {'sheetId': sheet_id, 'dimension': 'COLUMNS', 'startIndex': col, 'endIndex': col+1},
            'properties': {'pixelSize': width},
            'fields': 'pixelSize'
        }
    }

def freeze_rows(sheet_id, count):
    return {
        'updateSheetProperties': {
            'properties': {'sheetId': sheet_id, 'gridProperties': {'frozenRowCount': count}},
            'fields': 'gridProperties.frozenRowCount'
        }
    }

def alternating_colors(sheet_id, start_row, end_row, start_col, end_col):
    return {
        'addBanding': {
            'bandedRange': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                    'startColumnIndex': start_col,
                    'endColumnIndex': end_col
                },
                'rowProperties': {
                    'headerColorStyle': {'rgbColor': NAVY},
                    'firstBandColorStyle': {'rgbColor': WHITE},
                    'secondBandColorStyle': {'rgbColor': LIGHT_GRAY}
                }
            }
        }
    }

CURRENCY_FMT = {'type': 'CURRENCY', 'pattern': '"$"#,##0.00;("$"#,##0.00)'}
PERCENT_FMT = {'type': 'PERCENT', 'pattern': '0.0%'}

# ── August 2025 Data ──────────────────────────────────────────────────────────
AUG_INCOME = [
    ['Stripe', 'Stripe', '08/05/2025', '$230.55'],
    ['Stripe', 'Stripe', '08/06/2025', '$337.80'],
    ['Stripe', 'Stripe', '08/07/2025', '$711.02'],
    ['Stripe', 'Stripe', '08/12/2025', '$572.72'],
    ['Stripe', 'Stripe', '08/14/2025', '$706.52'],
    ['Stripe', 'Stripe', '08/18/2025', '$354.54'],
    ['Stripe', 'Stripe', '08/19/2025', '$582.00'],
    ['Stripe', 'Stripe', '08/21/2025', '$708.39'],
    ['Stripe', 'Stripe', '08/25/2025', '$354.54'],
    ['Stripe', 'Stripe', '08/26/2025', '$582.00'],
    ['Stripe', 'Stripe', '08/28/2025', '$708.39'],
    ['', '', 'Stripe Subtotal', '$5,848.47'],
    ['Zelle', 'ACI Enterprise (Zelle)', '08/12/2025', '$1,000.00'],
    ['Zelle', 'ACI Enterprise (Zelle)', '08/26/2025', '$1,000.00'],
    ['', '', 'Zelle Subtotal', '$2,000.00'],
    ['', '', 'TOTAL BUSINESS INCOME', '$7,848.47'],
]

AUG_BIZ_EXPENSES = [
    # SaaS & Tools
    ['📱 SaaS & Tools'],
    ['', 'GoHighLevel (Agency + Inc)', '3', '($497.00)'],
    ['', '10web.io', '1', '($136.00)'],
    ['', 'localrank.so', '1', '($174.30)'],
    ['', 'Google Ads (3 campaigns)', '3', '($340.86)'],
    ['', 'Google G Suite', '1', '($32.35)'],
    ['', 'Cobrand', '1', '($85.00)'],
    ['', 'Claude AI (Anthropic)', '1', '($20.00)'],
    ['', 'ChatGPT (OpenAI)', '1', '($20.00)'],
    ['', 'Flowith', '1', '($19.90)'],
    ['', 'Google One', '1', '($19.99)'],
    ['', 'TradingView', '1', '($16.95)'],
    ['', 'X Corp (Premium)', '1', '($40.00)'],
    ['', 'Canva', '1', '($15.00)'],
    ['', 'Spotify', '1', '($12.59)'],
    ['', 'Hyonix (Hosting)', '1', '($12.00)'],
    ['', 'Apple Subscriptions', '2', '($30.98)'],
    ['', 'Meta Wave Solutions (Toolzbuy)', '1', '($10.50)'],
    ['', 'Ideogram AI', '1', '($8.00)'],
    ['', '', 'SaaS/Tools Subtotal', '($1,521.42)'],
    # Marketing
    ['📣 Marketing / Ads'],
    ['', 'Facebook/Meta Ads (4991)', '1', '($4.09)'],
    ['', '', 'Marketing Subtotal', '($4.09)'],
    # Operations
    ['🏢 Operations'],
    ['', 'Triwest (Health Insurance)', '1', '($404.39)'],
    ['', 'Regus (Coworking)', '1', '($99.00)'],
    ['', 'Boost Mobile', '1', '($76.62)'],
    ['', 'Spectrum (Internet)', '1', '($70.00)'],
    ['', 'T-Mobile', '1', '($55.36)'],
    ['', 'Zelle to Ross', '1', '($25.00)'],
    ['', 'PayPal (IoT Solution)', '1', '($21.88)'],
    ['', 'Chase Monthly Service Fee', '1', '($15.00)'],
    ['', 'Venmo', '1', '($6.00)'],
    ['', '', 'Operations Subtotal', '($773.25)'],
    # Debt
    ['💳 Debt Payments'],
    ['', 'Affirm (Mattress)', '1', '($179.65)'],
    ['', 'Credit Strong', '1', '($90.00)'],
    ['', 'Self Lender', '1', '($48.00)'],
    ['', '', 'Debt Subtotal', '($317.65)'],
    # Fees
    ['💰 Business Fees & Interest'],
    ['', 'Biz CC 0678 Interest', '1', '($43.67)'],
    ['', '', 'Fees/Interest Subtotal', '($43.67)'],
    ['', '', 'TOTAL BUSINESS EXPENSES', '($2,660.08)'],
]

AUG_PERSONAL = [
    ['🏧 ATM / Cash / Weed / Fees'],
    ['', 'ATM Withdrawals (Milwaukee & SD)', '7', '($482.48)'],
    ['', 'ATM Fees', '7', '($21.00)'],
    ['', 'Smoke Shops & Weed', '4', '($66.86)'],
    ['', 'Venmo (misc)', '5', '($98.00)'],
    ['', '', 'ATM/Cash Subtotal', '($668.34)'],
    ['📈 Investments'],
    ['', 'Robinhood (recurring)', '29', '($725.00)'],
    ['', 'Acorns Invest', '23', '($118.00)'],
    ['', 'Acorns Round-Ups', '9', '($106.46)'],
    ['', 'Acorns Subscription', '1', '($3.00)'],
    ['', '', 'Investment Subtotal', '($952.46)'],
    ['🏠 Housing & Travel (San Diego Trip)'],
    ['', 'Beach Bungalow Hostel (0068)', '2', '($748.43)'],
    ['', 'Beach Bungalow Hostel (4252)', '4', '($208.53)'],
    ['', 'ITH Hostels (0068)', '2', '($46.12)'],
    ['', 'ITH Hostel (4252)', '0', 'incl. in 4252 below'],
    ['', 'Mission Bay Hotel', '1', '($224.37)'],
    ['', 'Hostelworld (4252)', '1', '($13.51)'],
    ['', 'Turo Car Rental (0068)', '1', '($67.45)'],
    ['', 'Turo Car Rental (4252)', '3', '($550.62)'],
    ['', 'Southwest Airlines (0068)', '1', '($166.00)'],
    ['', 'Southwest Airlines (4252)', '1', '($588.36)'],
    ['', 'Uber/Lyft (0068)', '6', '($209.33)'],
    ['', 'Uber (4252)', '2', '($43.89)'],
    ['', 'Lime Rides', '2', '($28.97)'],
    ['', 'Couchsurfing', '1', '($60.00)'],
    ['', 'Gas', '3', '($157.65)'],
    ['', 'Wisconsin Rent (Zelle)', '1', '($550.00)'],
    ['', '', 'Housing/Travel Subtotal', '($3,662.23)'],
    ['🍔 Food & Dining'],
    ['', 'Restaurants & Bars (SD)', '~35', '($958.24)'],
    ['', 'Groceries (Ralphs, Vons, Walmart)', '~12', '($252.48)'],
    ['', 'Coffee shops', '~8', '($106.12)'],
    ['', 'Ice Cream (Oceans)', '4', '($45.23)'],
    ['', 'Milwaukee Food', '4', '($135.96)'],
    ['', '', 'Food/Dining Subtotal', '($1,498.03)'],
    ['📺 Subscriptions & Bills'],
    ['', 'We Energies (Utilities)', '1', '($165.05)'],
    ['', 'Hulu', '1', '($32.36)'],
    ['', 'Netflix', '1', '($19.05)'],
    ['', 'Dental Insurance (Solstice)', '1', '($8.13)'],
    ['', '', 'Subscriptions Subtotal', '($224.59)'],
    ['🎓 Student Loan'],
    ['', 'Dept of Education', '1', '($106.34)'],
    ['', '', 'Student Loan Subtotal', '($106.34)'],
    ['💳 CC Payments'],
    ['', 'Chase Sapphire Autopay', '1', '($218.00)'],
    ['', '', 'CC Payment Subtotal', '($218.00)'],
    ['💰 CC Interest (Personal)'],
    ['', 'Sapphire 4252 Interest', '1', '($159.67)'],
    ['', '', 'Personal CC Subtotal', '($159.67)'],
    ['🛍️ Shopping & Misc'],
    ['', 'Target', '1', '($48.88)'],
    ['', 'Amazon (Earbuds)', '1', '($31.20)'],
    ['', 'CVS (Travel Supplies)', '3', '($112.83)'],
    ['', 'Apple Cash', '2', '($57.00)'],
    ['', 'PayPal (misc)', '2', '($76.07)'],
    ['', 'Mission Surf (4252)', '1', '($99.74)'],
    ['', 'Other Misc', '3', '($44.88)'],
    ['', '', 'Shopping/Misc Subtotal', '($470.60)'],
]

AUG_METRICS = [
    ['Metric', '', '', 'Value'],
    ['Business Income', '', '', '$7,848.47'],
    ['Business Expenses', '', '', '($2,660.08)'],
    ['Business Profit (before personal)', '', '', '$5,188.39'],
    ['Profit Margin', '', '', '66.1%'],
    [''],
    ['Total SaaS/Tools', '', '', '($1,521.42)'],
    ['Total Operations', '', '', '($773.25)'],
    ['CC Interest (All Cards)', '', '', '($203.34)'],
    ['Total Investments (Robinhood + Acorns)', '', '', '($952.46)'],
    ['San Diego Trip Total (Housing+Transport+Food)', '', '', '~($4,500)'],
    ['ATM Withdrawals', '', '', '($482.48)'],
    ['Student Loan', '', '', '($106.34)'],
    ['Subscriptions (Personal)', '', '', '($224.59)'],
]

AUG_MONEY_FLOW = [
    ['Flow', '', 'Count', 'Total'],
    ['Biz 4991 → Personal 0068', '', '24', '$6,930.00'],
    ['Biz 4991 → Tax Account', '', '3', '$700.00'],
    [''],
    ['Personal 0068 → Savings 7036', '', '8', '$385.00'],
    ['Savings 7036 → Personal 0068', '', '3', '$600.00'],
    [''],
    ['Personal 0068 → CC 4252 (Autopay)', '', '1', '$218.00'],
    ['Check Deposit', '', '1', '$50.00'],
]

AUG_DEBT = [
    ['Account', 'Balance', 'Limit', 'Utilization', 'APR', 'Status'],
    ['Student Loans', '$9,046.32', '', '', '', 'Active'],
    ['CC Discover Personal', '$6,068.68', '$6,250', '97%', '19.99%', '⚠️ Near Max'],
    ['CC Chase Sapphire', '$9,085.44', '$9,300', '98%', '21.99%', '⚠️ Near Max'],
    ['CC Chase Ink (Biz)', '$3,859.59', '$5,500', '70%', '16.99%', 'Active'],
    ['TOTAL CC DEBT', '$19,013.71', '', '', '', ''],
    ['TOTAL ALL DEBT', '$28,060.03', '', '', '', ''],
]

AUG_BALANCES = [
    ['Account', '', 'Start of Month', 'End of Month'],
    ['Business Checking 4991', '', '$2,319.91', '$913.94'],
    ['Personal Checking 0068', '', '$332.07', '$1,003.23*'],
    ['* Approx based on last transactions'],
]

AUG_ASSETS = [
    ['Category', '', '', 'Value'],
    ['Rank & Rent Business Assets', '', '', '$150,000.00'],
    ['Cash (Checking Accounts)', '', '', '$3,696.23'],
    ['Stocks & Options', '', '', '$1,150.00'],
    ['Bitcoin', '', '', '$1,614.00'],
    ['Solana', '', '', '$3,101.00'],
    ['Dogecoin', '', '', '$245.00'],
    [''],
    ['Liquid Assets', '', '', '$9,806.23'],
    ['Business Equity', '', '', '$150,000.00'],
    ['Total Assets', '', '', '$159,806.23'],
    ['Total Liabilities', '', '', '($28,060.03)'],
    ['Net Worth', '', '', '$131,746.20'],
]

# ── September 2025 Data ───────────────────────────────────────────────────────
SEPT_INCOME = [
    ['Stripe', 'Stripe', '09/03/2025', '$575.35'],
    ['Stripe', 'Stripe', '09/09/2025', '$236.70'],
    ['Stripe', 'Stripe', '09/10/2025', '$347.20'],
    ['Stripe', 'Stripe', '09/11/2025', '$335.35'],
    ['Stripe', 'Stripe', '09/16/2025', '$572.72'],
    ['Stripe', 'Stripe', '09/17/2025', '$361.95'],
    ['Stripe', 'Stripe', '09/22/2025', '$188.00'],
    ['Stripe', 'Stripe', '09/23/2025', '$242.45'],
    ['Stripe', 'Stripe', '09/24/2025', '$337.80'],
    ['Stripe', 'Stripe', '09/26/2025', '$359.32'],
    ['Stripe', 'Stripe', '09/30/2025', '$577.80'],
    ['', '', 'Stripe Subtotal', '$4,134.64'],
    ['Zelle', 'ACI Enterprise (Zelle)', '09/08/2025', '$1,000.00'],
    ['Zelle', 'ACI Enterprise (Zelle)', '09/24/2025', '$1,000.00'],
    ['Zelle', 'David Monter Tolentino (Zelle)', '09/08/2025', '$375.00'],
    ['', '', 'Zelle Subtotal', '$2,375.00'],
    ['', '', 'TOTAL BUSINESS INCOME', '$6,509.64'],
]

SEPT_BIZ_EXPENSES = [
    ['📱 SaaS & Tools'],
    ['', 'GoHighLevel (Agency + Inc)', '3', '($507.00)'],
    ['', '10web.io', '1', '($136.00)'],
    ['', 'localrank.so', '1', '($174.30)'],
    ['', 'Apple Subscriptions', '3', '($139.10)'],
    ['', 'Cobrand', '1', '($85.00)'],
    ['', 'Spectrum (Internet)', '1', '($70.00)'],
    ['', 'Google Workspace', '1', '($33.60)'],
    ['', 'ChatGPT (OpenAI)', '1', '($20.00)'],
    ['', 'Google One', '1', '($19.99)'],
    ['', 'Flowith', '1', '($19.90)'],
    ['', 'TradingView', '1', '($16.95)'],
    ['', 'Canva', '1', '($15.00)'],
    ['', 'Spotify', '1', '($12.59)'],
    ['', 'CashApp (Reviews)', '1', '($10.00)'],
    ['', 'Ideogram AI', '1', '($8.00)'],
    ['', '', 'SaaS/Tools Subtotal', '($1,267.43)'],
    # Operations
    ['🏢 Operations'],
    ['', 'Regus (Coworking)', '1', '($99.00)'],
    ['', 'SafetyWing (Health Insurance)', '1', '($66.28)'],
    ['', 'T-Mobile', '1', '($55.36)'],
    ['', 'Chase Monthly Service Fee', '1', '($15.00)'],
    ['', 'Zelle to Ross', '1', '($12.50)'],
    ['', '', 'Operations Subtotal', '($248.14)'],
    # Debt
    ['💳 Debt Payments'],
    ['', 'Affirm (Mattress)', '1', '($179.65)'],
    ['', 'Credit Strong', '1', '($90.00)'],
    ['', 'Self Lender', '1', '($48.00)'],
    ['', 'Chase CC 0678 Payment', '1', '($76.00)'],
    ['', '', 'Debt Subtotal', '($393.65)'],
    # Fees
    ['💰 Business Fees & Interest'],
    ['', 'Biz CC 0678 Interest', '1', '($53.25)'],
    ['', '', 'Fees/Interest Subtotal', '($53.25)'],
    ['', '', 'TOTAL BUSINESS EXPENSES', '($1,962.47)'],
]

SEPT_PERSONAL = [
    ['🏧 ATM / Cash / FX Fees'],
    ['', 'ATM Withdrawals (Colombia)', '3', '($627.01)'],
    ['', 'ATM Fees', '3', '($13.00)'],
    ['', 'Foreign Exchange Fee', '1', '($1.93)'],
    ['', '', 'ATM/Cash Subtotal', '($641.94)'],
    ['📈 Investments'],
    ['', 'Robinhood (recurring)', '29', '($828.00)'],
    ['', 'Robinhood (lump payment)', '1', '($300.00)'],
    ['', 'Acorns Invest', '32', '($160.00)'],
    ['', 'Acorns Round-Ups', '8', '($54.02)'],
    ['', 'Acorns Subscription', '1', '($3.00)'],
    ['', '', 'Investment Subtotal', '($1,345.02)'],
    ['✈️ Travel'],
    ['', 'Colombia Rent (Coliving.com)', '1', '($747.90)'],
    ['', 'Southwest Airlines', '1', '($469.18)'],
    ['', 'Southwest Excess Bag', '1', '($35.00)'],
    ['', 'United Airlines', '1', '($370.75)'],
    ['', 'Travel Guard Insurance', '1', '($28.25)'],
    ['', 'Wise (Personal Spending)', '2', '($334.75)'],
    ['', 'Hostels (Hostelworld)', '2', '($29.74)'],
    ['', 'Masaya Medellín (Hostel)', '1', '($64.66)'],
    ['', 'Onward Ticket', '1', '($16.00)'],
    ['', 'Airalo (eSIM)', '2', '($34.30)'],
    ['', '', 'Travel Subtotal', '($2,130.53)'],
    ['🏠 Housing'],
    ['', 'Wisconsin Rent (Zelle to Patrick)', '1', '($550.00)'],
    ['', '', 'Housing Subtotal', '($550.00)'],
    ['🍔 Food & Dining'],
    ['', 'Restaurants (SF + Colombia)', '3', '($77.76)'],
    ['', 'iStore @ SFO', '1', '($54.68)'],
    ['', 'Shopping (Target)', '1', '($74.96)'],
    ['', 'Auntie Anne\'s (MKE)', '1', '($9.73)'],
    ['', 'MKE Pizzeria Piccola', '1', '($21.11)'],
    ['', 'Banzai Bowls', '1', '($11.00)'],
    ['', '', 'Food/Shopping Subtotal', '($249.24)'],
    ['📺 Subscriptions'],
    ['', 'Slate Digital (Music Plugin)', '1', '($160.77)'],
    ['', 'Dental Insurance (Solstice)', '1', '($8.13)'],
    ['', '', 'Subscriptions Subtotal', '($168.90)'],
    ['🎓 Student Loan'],
    ['', 'Dept of Education', '1', '($106.34)'],
    ['', '', 'Student Loan Subtotal', '($106.34)'],
    ['💳 CC Payments (Personal)'],
    ['', 'Chase Sapphire Autopay', '1', '($250.00)'],
    ['', 'Discover Card Payment', '1', '($122.00)'],
    ['', '', 'CC Payment Subtotal', '($372.00)'],
    ['💰 CC Interest (Personal)'],
    ['', 'Sapphire 4252 Interest', '1', '($172.42)'],
    ['', 'Discover Interest', '1', '($101.80)'],
    ['', '', 'Personal CC Subtotal', '($274.22)'],
    ['💸 Donations & Misc'],
    ['', 'GoFundMe Donations', '2', '($345.50)'],
    ['', 'Apple Cash', '3', '($110.00)'],
    ['', 'PayPal', '1', '($28.35)'],
    ['', '', 'Misc Subtotal', '($483.85)'],
]

SEPT_METRICS = [
    ['Metric', '', '', 'Value'],
    ['Business Income', '', '', '$6,509.64'],
    ['Business Expenses', '', '', '($1,962.47)'],
    ['Business Profit (before personal)', '', '', '$4,547.17'],
    ['Profit Margin', '', '', '69.9%'],
    [''],
    ['⭐ Profit excl. Debt Payments', '', '', '$4,940.82'],
    ['Profit Margin excl. Debt', '', '', '75.9%'],
    [''],
    ['Total SaaS/Tools', '', '', '($1,267.43)'],
    ['Total Operations', '', '', '($248.14)'],
    ['CC Interest Total (All Cards)', '', '', '($327.47)'],
    ['Total Investments (Robinhood + Acorns)', '', '', '($1,345.02)'],
    ['Travel Spend', '', '', '($2,130.53)'],
    ['ATM Withdrawals (Colombia)', '', '', '($627.01)'],
    ['Student Loan', '', '', '($106.34)'],
    ['Subscriptions', '', '', '($168.90)'],
]

SEPT_MONEY_FLOW = [
    ['Flow', '', 'Count', 'Total'],
    ['Biz 4991 → Personal 0068', '', '17', '$5,887.00'],
    ['Biz 4991 → Wise (Personal)', '', '1', '$300.51'],
    ['Personal 0068 → Biz 4991', '', '1', '$300.00'],
    ['Savings 7036 → Biz 4991', '', '2', '$400.00'],
    ['Tax Acct (Wells Fargo) → Biz 4991', '', '1', '$950.00'],
    [''],
    ['Personal 0068 → Savings 7036', '', '11', '$1,035.00'],
    ['Savings 7036 → Personal 0068', '', '2', '$566.07'],
]

SEPT_DEBT = [
    ['Account', 'Balance', 'Limit', 'Utilization', 'APR', 'Status'],
    ['Student Loans', '$8,978.06', '', '', '', 'Active'],
    ['CC Discover Personal', '$5,926.48', '$6,250', '95%', '19.99%', '⚠️ Near Max'],
    ['CC Chase Sapphire', '$9,007.86', '$9,300', '97%', '21.99%', '⚠️ Near Max'],
    ['CC Chase Ink (Biz)', '$4,400.93', '$5,500', '80%', '16.99%', 'Active'],
    ['TOTAL CC DEBT', '$19,335.27', '', '', '', ''],
    ['TOTAL ALL DEBT', '$28,313.33', '', '', '', ''],
]

SEPT_BALANCES = [
    ['Account', '', 'Start of Month', 'End of Month'],
    ['Business Checking 4991', '', '$913.94', '$1,384.82'],
    ['Personal Checking 0068', '', '$468.96', '$203.23'],
]

SEPT_ASSETS = [
    ['Category', '', '', 'Value'],
    ['Rank & Rent Business Assets', '', '', '$150,000.00'],
    ['Cash (Checking Accounts)', '', '', '$1,807.43'],
    ['Stocks & Options', '', '', '$1,852.00'],
    ['Bitcoin', '', '', '$2,000.00'],
    ['Solana', '', '', '$500.00'],
    ['Dogecoin', '', '', '$260.00'],
    ['XRP', '', '', '$95.00'],
    ['CreditBuilder Accounts', '', '', '$700.00'],
    [''],
    ['Liquid Assets', '', '', '$7,214.43'],
    ['Business Equity', '', '', '$150,000.00'],
    ['Total Assets', '', '', '$157,214.43'],
    ['Total Liabilities', '', '', '($28,313.33)'],
    ['Net Worth', '', '', '$128,901.10'],
]

# ── Transaction Cleaning ──────────────────────────────────────────────────────
VENDOR_MAP = {
    'APPLE.COM/BILL': 'Apple',
    'BOOST MOBILE': 'Boost Mobile',
    'CLAUDE.AI': 'Claude AI (Anthropic)',
    'COBRAND.COM': 'Cobrand',
    'FACEBK': 'Facebook/Meta Ads',
    'FLOWITH.IO': 'Flowith',
    'HIGHLEVEL AGENCY': 'GoHighLevel (Agency)',
    'HIGHLEVEL INC': 'GoHighLevel Inc',
    'META WAVE': 'Meta Wave Solutions',
    'MONTHLY SERVICE FEE': 'Chase Service Fee',
    'AFFIRM': 'Affirm (Mattress)',
    'Credit Strong': 'Credit Strong',
    'SELF LENDER': 'Self Lender',
    'STRIPE': 'Stripe Deposit',
    'TRIWEST': 'Triwest (Health Insurance)',
    'VENMO': 'Venmo',
    'PAYPAL': 'PayPal',
    'TMOBILE': 'T-Mobile',
    'TradingView': 'TradingView',
    'X CORP': 'X Corp (Premium)',
    'Zelle payment from ACI': 'Zelle — ACI Enterprise',
    'Zelle payment from David': 'Zelle — David Monter Tolentino',
    'Zelle payment to ROSS': 'Zelle to Ross',
    'Zelle payment to Patrick': 'Rent — Patrick (Zelle)',
    'ROBINHOOD': 'Robinhood Investing',
    'Acorns Invest': 'Acorns Invest',
    'Acorns Round': 'Acorns Round-Ups',
    'Subscription     Acorns': 'Acorns Subscription',
    'SAFETYWING': 'SafetyWing (Insurance)',
    'CHASE CREDIT CRD': 'Chase CC Autopay',
    'DEPT EDUCATION': 'Student Loan',
    'DISCOVER': 'Discover CC Payment',
    'HULU': 'Hulu',
    'Netflix': 'Netflix',
    'SOLSTICE': 'Dental Insurance (Solstice)',
    'BEACH BUNGALOW': 'Beach Bungalow Hostel',
    'ITH HOSTELS': 'ITH Hostels',
    'MISSION BAY': 'Mission Bay Hotel',
    'TURO': 'Turo Car Rental',
    'SOUTHWES': 'Southwest Airlines',
    'UBER': 'Uber',
    'UBR*': 'Uber',
    'LIME': 'Lime Rides',
    'COUCHSURFING': 'Couchsurfing',
    'CVS': 'CVS Pharmacy',
    'RALPHS': 'Ralphs (Groceries)',
    'VONS': 'Vons (Groceries)',
    'WAL WAL-MART': 'Walmart',
    'WE ENERGIES': 'We Energies (Utilities)',
    'TARGET': 'Target',
    'Amazon': 'Amazon',
    'APPLE CASH': 'Apple Cash',
    'WOODSTOCKS': 'Woodstocks Pizza',
    'NON-CHASE ATM FEE': 'ATM Fee',
    'NON-CHASE ATM WITHDRAW': 'ATM Withdrawal',
    'Online Transfer to  CHK': 'Transfer → Personal 0068',
    'Online Transfer to CHK': 'Transfer → Personal 0068',
    'Online Transfer from  CHK': 'Transfer ← Business 4991',
    'Online Transfer from CHK': 'Transfer ← Business 4991',
    'Online Transfer to  SAV': 'Transfer → Savings 7036',
    'Online Transfer to SAV': 'Transfer → Savings 7036',
    'Online Transfer from SAV': 'Transfer ← Savings 7036',
    'Online Transfer from  SAV': 'Transfer ← Savings 7036',
    'Online Realtime Transfer to Taxes': 'Transfer → Tax Account',
    'ODP TRANSFER': 'OD Transfer ← Savings',
    'Online RealTime payment to Robinhood': 'Robinhood (Lump Transfer)',
    'CASH APP': 'CashApp',
    'GOOGLE *Google One': 'Google One',
    'GOOGLE *GSUITE': 'Google Workspace',
    'GOOGLE *ADS': 'Google Ads',
    'OPENAI *CHATGPT': 'ChatGPT (OpenAI)',
    'IDEOGRAM': 'Ideogram AI',
    'CANVA': 'Canva',
    '10WEB': '10web.io',
    'LOCALRANK': 'localrank.so',
    'SPOTIFY': 'Spotify',
    'Spectrum': 'Spectrum (Internet)',
    'Regus': 'Regus (Coworking)',
    'PURCHASE INTEREST': 'Interest Charge',
    'AUTOMATIC PAYMENT': 'CC Payment Received',
    'HYONIX': 'Hyonix (Hosting)',
    'COLIVING': 'Colombia Coliving Rent',
    'AIRALO': 'Airalo (eSIM)',
    'GoFundMe': 'GoFundMe Donation',
    'ISTORE': 'iStore @ SFO',
    'MASAYA': 'Masaya Medellín (Hostel)',
    'HOSTELWORLD': 'Hostelworld',
    'ONWARD TICKET': 'Onward Ticket',
    'UNITED': 'United Airlines',
    'TRAVEL GUARD': 'Travel Guard Insurance',
    'Wise': 'Wise Transfer',
    'SWA*EXCS': 'Southwest Excess Bag',
    'SLATE DIGITAL': 'Slate Digital (Music)',
    'KITAVA': 'Kitava (SF Restaurant)',
    'SQ *MERCHANDISING': 'SQ Merchandising (SF)',
    'BANZAI': 'Banzai Bowls',
    'MISSION SURF': 'Mission Surf',
    'WELLS FARGO': 'Wells Fargo (Tax Acct Transfer)',
}

CATEGORY_MAP = {
    'Apple': '📱 SaaS',
    'Boost Mobile': '🏢 Operations',
    'Claude AI': '📱 SaaS',
    'Cobrand': '📱 SaaS',
    'Facebook/Meta Ads': '📣 Marketing',
    'Flowith': '📱 SaaS',
    'GoHighLevel': '📱 SaaS',
    'Meta Wave': '📱 SaaS',
    'Chase Service Fee': '🏢 Operations',
    'Affirm': '💳 Debt Payment',
    'Credit Strong': '💳 Debt Payment',
    'Self Lender': '💳 Debt Payment',
    'Stripe': '💰 Income',
    'Triwest': '🏢 Operations',
    'Venmo': '🛍️ Misc',
    'PayPal': '🛍️ Misc',
    'T-Mobile': '🏢 Operations',
    'TradingView': '📱 SaaS',
    'X Corp': '📱 SaaS',
    'Zelle — ACI': '💰 Income',
    'Zelle — David': '💰 Income',
    'Zelle to Ross': '🏢 Operations',
    'Rent': '🏠 Housing',
    'Robinhood': '📈 Investing',
    'Acorns': '📈 Investing',
    'SafetyWing': '🏢 Operations',
    'Chase CC': '💳 CC Payment',
    'Student Loan': '🎓 Student Loan',
    'Discover CC': '💳 CC Payment',
    'Hulu': '📺 Subscription',
    'Netflix': '📺 Subscription',
    'Dental': '📺 Subscription',
    'Beach Bungalow': '✈️ Travel',
    'ITH': '✈️ Travel',
    'Mission Bay': '✈️ Travel',
    'Turo': '✈️ Travel',
    'Southwest': '✈️ Travel',
    'Uber': '🚗 Transport',
    'Lime': '🚗 Transport',
    'Couchsurfing': '✈️ Travel',
    'CVS': '🛍️ Shopping',
    'Ralphs': '🛒 Groceries',
    'Vons': '🛒 Groceries',
    'Walmart': '🛒 Groceries',
    'We Energies': '🏠 Utilities',
    'Target': '🛍️ Shopping',
    'Amazon': '🛍️ Shopping',
    'Apple Cash': '💸 Personal',
    'ATM Fee': '🏧 ATM Fee',
    'ATM Withdrawal': '🏧 ATM Cash',
    'Transfer': '🔄 Transfer',
    'OD Transfer': '🔄 Transfer',
    'Google One': '📱 SaaS',
    'Google Workspace': '📱 SaaS',
    'Google Ads': '📣 Marketing',
    'ChatGPT': '📱 SaaS',
    'Ideogram': '📱 SaaS',
    'Canva': '📱 SaaS',
    '10web': '📱 SaaS',
    'localrank': '📱 SaaS',
    'Spotify': '📱 SaaS',
    'Spectrum': '📱 SaaS',
    'Regus': '🏢 Operations',
    'Interest': '💰 Interest',
    'CC Payment': '💳 CC Payment',
    'Hyonix': '📱 SaaS',
    'Colombia': '🏠 Housing',
    'Airalo': '✈️ Travel',
    'GoFundMe': '💸 Donation',
    'iStore': '🛍️ Shopping',
    'Masaya': '✈️ Travel',
    'Hostelworld': '✈️ Travel',
    'Onward': '✈️ Travel',
    'United': '✈️ Travel',
    'Travel Guard': '✈️ Travel',
    'Wise': '🔄 Transfer',
    'Excess Bag': '✈️ Travel',
    'Slate Digital': '📺 Subscription',
    'Kitava': '🍔 Dining',
    'Banzai': '🍔 Dining',
    'Mission Surf': '🛍️ Shopping',
    'Wells Fargo': '🔄 Transfer',
    'CashApp': '🏢 Operations',
    'Smoke Shop': '🏧 ATM Cash',
}

def clean_vendor(desc):
    """Map raw bank description to clean vendor name."""
    for key, name in VENDOR_MAP.items():
        if key.upper() in desc.upper():
            return name
    # For restaurants and other places - clean up TST*, SQ* prefixes
    if desc.startswith('TST*') or desc.startswith('SQ *'):
        parts = desc.split(' ')
        # Get the restaurant name
        name = desc.replace('TST* ', '').replace('TST*', '').replace('SQ *', '')
        # Take first few words before the city
        words = name.split()
        clean_parts = []
        for w in words:
            if w in ('SAN', 'San', 'MILWAUKEE', 'Milwaukee', 'Las', 'LAS', 'CA', 'WI', 'NV', 'TX'):
                break
            clean_parts.append(w.title())
        return ' '.join(clean_parts) if clean_parts else name[:30]
    # For other descriptions, just clean up
    desc_clean = desc.split('  ')[0][:40].strip()
    return desc_clean

def get_category(vendor_name):
    """Map vendor name to expense category."""
    for key, cat in CATEGORY_MAP.items():
        if key.lower() in vendor_name.lower():
            return cat
    if any(x in vendor_name.lower() for x in ['restaurant', 'pizza', 'coffee', 'cafe', 'bar', 'beach club', 'grill', 'sushi', 'taco', 'eggies', 'cane', 'ice cream', 'breakfast']):
        return '🍔 Dining'
    if any(x in vendor_name.lower() for x in ['smoke', '7-eleven', 'gas', 'shell', 'bp#']):
        return '🏧 ATM Cash'
    return '🛍️ Other'

def clean_transactions(raw_rows, is_cc=False):
    """Clean raw transaction data into standardized format."""
    cleaned = []
    for row in raw_rows:
        if len(row) < 4:
            continue
        if is_cc:
            # CC format: Card, Trans Date, Post Date, Description, Category, Type, Amount
            if row[0] in ('Card', 'Transaction Date'):
                continue
            date = row[1] if len(row) > 1 else row[0]
            desc = row[3] if len(row) > 3 else row[2]
            amount = row[6] if len(row) > 6 else (row[5] if len(row) > 5 else '')
            balance = ''
        else:
            # Checking format: Details, Posting Date, Description, Amount, Type, Balance
            if row[0] == 'Details':
                continue
            date = row[1] if len(row) > 1 else ''
            desc = row[2] if len(row) > 2 else ''
            amount = row[3] if len(row) > 3 else ''
            balance = row[5] if len(row) > 5 else ''

        vendor = clean_vendor(desc)
        category = get_category(vendor)
        
        cleaned.append([date, vendor, category, amount, balance, ''])
    
    return cleaned

# ── Build Dashboard ───────────────────────────────────────────────────────────
def build_dashboard_data(month, year, income, biz_exp, personal, metrics, money_flow, debt, balances, assets, action_items=None):
    """Build the complete dashboard data array."""
    rows = []
    
    # Title
    rows.append([f'{month} {year} — KuriosBrand Financial Overview'])
    rows.append([])
    
    # Section A: Income
    rows.append(['💰 SECTION A: INCOME SUMMARY'])
    rows.append(['Source', 'Vendor / Client', 'Date', 'Amount'])
    for r in income:
        rows.append(r)
    rows.append([])
    
    # Section B: Business Expenses
    rows.append(['📊 SECTION B: BUSINESS EXPENSES'])
    rows.append(['Category', 'Vendor', 'Count', 'Total'])
    for r in biz_exp:
        rows.append(r)
    rows.append([])
    
    # Section C: Personal Expenses
    rows.append(['👤 SECTION C: PERSONAL EXPENSES'])
    rows.append(['Category', 'Detail', 'Count', 'Total'])
    for r in personal:
        rows.append(r)
    rows.append([])
    
    # Section D: Key Metrics
    rows.append(['📈 SECTION D: KEY METRICS'])
    for r in metrics:
        rows.append(r)
    rows.append([])
    
    # Section E: Money Flow
    rows.append(['🔄 SECTION E: MONEY FLOW'])
    for r in money_flow:
        rows.append(r)
    rows.append([])
    
    # Section F: Debt Tracking
    rows.append(['🏦 SECTION F: DEBT TRACKING'])
    for r in debt:
        rows.append(r)
    rows.append([])
    
    # Section G: Account Balances
    rows.append(['💰 SECTION G: ACCOUNT BALANCES'])
    for r in balances:
        rows.append(r)
    rows.append([])
    
    # Section H: Assets & Net Worth
    rows.append(['🏆 SECTION H: ASSETS & NET WORTH'])
    for r in assets:
        rows.append(r)
    rows.append([])
    
    # Section I: Action Items (if provided)
    if action_items:
        rows.append(['📝 SECTION I: ACTION ITEMS'])
        rows.append(['#', 'Item', 'Status', 'Notes'])
        for r in action_items:
            rows.append(r)
    
    return rows

# ── Apply Formatting ──────────────────────────────────────────────────────────
def build_dashboard_formatting(sheet_id, rows):
    """Build formatting requests for the dashboard."""
    reqs = []
    
    # Column widths
    widths = [180, 280, 120, 140]
    for i, w in enumerate(widths):
        reqs.append(set_col_width(sheet_id, i, w))
    
    # Freeze first row
    reqs.append(freeze_rows(sheet_id, 1))
    
    # Title row - big bold navy
    reqs.append(format_range(sheet_id, 0, 1, 0, 4, 
        cell_format(bg=NAVY, fg=WHITE, bold=True, size=14, halign='LEFT')))
    reqs.append(merge_cells(sheet_id, 0, 1, 0, 4))
    
    # Find section headers and format them
    for i, row in enumerate(rows):
        if not row:
            continue
        text = str(row[0]) if row else ''
        
        # Section headers (💰 SECTION A, 📊 SECTION B, etc.)
        if 'SECTION' in text:
            reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                cell_format(bg=NAVY, fg=WHITE, bold=True, size=11)))
            reqs.append(merge_cells(sheet_id, i, i+1, 0, 4))
        
        # Sub-headers (Source/Vendor/Date/Amount, Category/Detail/Count/Total)
        elif text in ('Source', 'Category', 'Metric', 'Flow', 'Account', '#'):
            reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                cell_format(bg=rgb('#2C3E6B'), fg=WHITE, bold=True, size=10)))
        
        # Category sub-headers (📱 SaaS, 📣 Marketing, etc.)
        elif text.startswith(('📱', '📣', '🏢', '💳', '💰', '🏧', '📈', '✈️', '🏠', '🍔', '📺', '🎓', '💸', '🛍️', '⭐')):
            reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                cell_format(bg=rgb('#E8EDF3'), bold=True, size=10)))
        
        # Subtotals and totals
        elif len(row) > 2 and row[2] and ('Subtotal' in str(row[2]) or 'TOTAL' in str(row[2])):
            if 'TOTAL' in str(row[2]):
                reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                    cell_format(bg=rgb('#1B2A4A'), fg=WHITE, bold=True, size=10)))
            else:
                reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                    cell_format(bg=rgb('#D5DDE8'), bold=True, size=10)))
        
        # Net Worth highlight
        elif len(row) > 2 and 'Net Worth' in str(row[0]):
            reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                cell_format(bg=rgb('#1B5E20'), fg=WHITE, bold=True, size=11)))
        
        # Profit highlight
        elif len(row) > 2 and ('Profit' in str(row[0]) and 'Margin' not in str(row[0])):
            reqs.append(format_range(sheet_id, i, i+1, 0, 4,
                cell_format(bg=LIGHT_GREEN, bold=True, size=10)))
    
    return reqs

def build_txn_formatting(sheet_id, row_count):
    """Build formatting for transaction tabs."""
    reqs = []
    
    # Column widths: Date, Vendor, Category, Amount, Balance, Notes
    widths = [100, 260, 140, 100, 100, 200]
    for i, w in enumerate(widths):
        reqs.append(set_col_width(sheet_id, i, w))
    
    # Header row
    reqs.append(format_range(sheet_id, 0, 1, 0, 6,
        cell_format(bg=NAVY, fg=WHITE, bold=True, size=10, halign='CENTER')))
    
    # Freeze header
    reqs.append(freeze_rows(sheet_id, 1))
    
    # Alternating rows
    if row_count > 2:
        reqs.append(alternating_colors(sheet_id, 0, min(row_count, 500), 0, 6))
    
    # Currency format for Amount column (col 3)
    reqs.append(format_range(sheet_id, 1, row_count, 3, 4,
        {'numberFormat': CURRENCY_FMT, 'horizontalAlignment': 'RIGHT'}))
    
    # Currency format for Balance column (col 4)
    reqs.append(format_range(sheet_id, 1, row_count, 4, 5,
        {'numberFormat': CURRENCY_FMT, 'horizontalAlignment': 'RIGHT'}))
    
    return reqs

# ── Main Processing ───────────────────────────────────────────────────────────
def process_sheet(spreadsheet_id, month, year, income, biz_exp, personal, metrics, 
                  money_flow, debt, balances, assets, action_items,
                  txn_tabs_config):
    """Process a single spreadsheet: create dashboard, clean transactions, format."""
    
    print(f"\n{'='*60}")
    print(f"Processing {month} {year} — {spreadsheet_id}")
    print(f"{'='*60}")
    
    # Get current metadata
    meta = get_sheet_metadata(spreadsheet_id)
    existing_tabs = {s['properties']['title']: s['properties']['sheetId'] for s in meta['sheets']}
    print(f"Existing tabs: {list(existing_tabs.keys())}")
    
    format_reqs = []
    
    # Step 1: Create Dashboard tab (or clear if exists)
    dashboard_title = '📊 Dashboard'
    if dashboard_title in existing_tabs:
        dashboard_id = existing_tabs[dashboard_title]
        # Clear it
        sheets_update(spreadsheet_id, f"'{dashboard_title}'!A1:Z500", 
                      [[''] * 26] * 500)
    else:
        # Create new tab
        dashboard_id = 999999
        result = sheets_batch_update(spreadsheet_id, [{
            'addSheet': {
                'properties': {
                    'title': dashboard_title,
                    'sheetId': dashboard_id,
                    'index': 0,
                    'gridProperties': {'rowCount': 500, 'columnCount': 8}
                }
            }
        }])
        if 'replies' in result:
            dashboard_id = result['replies'][0]['addSheet']['properties']['sheetId']
        print(f"Created Dashboard tab (id={dashboard_id})")
    
    # Step 2: Build and write dashboard data
    dashboard_data = build_dashboard_data(month, year, income, biz_exp, personal,
                                          metrics, money_flow, debt, balances, assets, action_items)
    
    print(f"Writing {len(dashboard_data)} rows to Dashboard...")
    sheets_update(spreadsheet_id, f"'{dashboard_title}'!A1:H{len(dashboard_data)}", dashboard_data)
    
    # Step 3: Format dashboard
    print("Formatting Dashboard...")
    dash_fmt = build_dashboard_formatting(dashboard_id, dashboard_data)
    if dash_fmt:
        sheets_batch_update(spreadsheet_id, dash_fmt)
    
    # Step 4: Process transaction tabs
    for tab_config in txn_tabs_config:
        old_name = tab_config['old_name']
        new_name = tab_config['new_name']
        is_cc = tab_config.get('is_cc', False)
        
        if old_name not in existing_tabs:
            print(f"  Tab '{old_name}' not found, skipping")
            continue
        
        tab_id = existing_tabs[old_name]
        print(f"  Processing: {old_name} → {new_name}")
        
        # Read raw data
        raw_data = sheets_get(spreadsheet_id, f"'{old_name}'!A1:Z300")
        if not raw_data:
            print(f"  No data in {old_name}")
            continue
        
        # Clean transactions
        cleaned = clean_transactions(raw_data, is_cc=is_cc)
        if not cleaned:
            print(f"  No transactions cleaned for {old_name}")
            continue
        
        # Create new cleaned tab
        clean_tab_title = new_name
        clean_tab_id = tab_id + 10000
        
        if clean_tab_title in existing_tabs:
            clean_tab_id = existing_tabs[clean_tab_title]
            sheets_update(spreadsheet_id, f"'{clean_tab_title}'!A1:F500", [[''] * 6] * 500)
        else:
            result = sheets_batch_update(spreadsheet_id, [{
                'addSheet': {
                    'properties': {
                        'title': clean_tab_title,
                        'sheetId': clean_tab_id,
                        'gridProperties': {'rowCount': 500, 'columnCount': 6}
                    }
                }
            }])
            if 'replies' in result:
                clean_tab_id = result['replies'][0]['addSheet']['properties']['sheetId']
        
        # Write header + data
        header = ['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']
        all_rows = [header] + cleaned
        sheets_update(spreadsheet_id, f"'{clean_tab_title}'!A1:F{len(all_rows)}", all_rows)
        
        # Format
        txn_fmt = build_txn_formatting(clean_tab_id, len(all_rows))
        if txn_fmt:
            sheets_batch_update(spreadsheet_id, txn_fmt)
        
        print(f"    Wrote {len(cleaned)} cleaned transactions")
    
    # Step 5: Rename old Overview to preserve it
    old_overview_name = 'Overview'
    if old_overview_name in existing_tabs:
        overview_id = existing_tabs[old_overview_name]
        try:
            sheets_batch_update(spreadsheet_id, [{
                'updateSheetProperties': {
                    'properties': {
                        'sheetId': overview_id,
                        'title': '📦 Original Overview',
                        'hidden': False
                    },
                    'fields': 'title'
                }
            }])
            print("Renamed old Overview → 📦 Original Overview")
        except:
            print("Could not rename Overview tab")
    
    # Step 6: Move Dashboard to first position
    try:
        sheets_batch_update(spreadsheet_id, [{
            'updateSheetProperties': {
                'properties': {
                    'sheetId': dashboard_id,
                    'index': 0
                },
                'fields': 'index'
            }
        }])
    except:
        pass
    
    print(f"\n✅ {month} {year} complete!")
    print(f"   URL: https://docs.google.com/spreadsheets/d/{spreadsheet_id}")

# ── Execute ───────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # AUGUST 2025
    AUG_ID = '1WnP2z0_4sE19-Ln7QTvm6lLfWqywTxmS1ef7HOZ9YeI'
    AUG_ACTIONS = [
        ['1', 'Boost Mobile cancelled — verify no future charges', '✅', 'Confirmed cancelled'],
        ['2', 'Claude AI cancelled — verify', '✅', 'Confirmed cancelled'],
        ['3', 'CC debt hit 97-98% utilization', '⚠️', 'Discover $6,068 / Sapphire $9,085'],
        ['4', 'San Diego trip cost ~$4,500 total', '📝', 'Travel + food + lodging + transport'],
        ['5', 'Google Ads cancelled mid-month', '✅', '$340 spent before cancellation'],
        ['6', 'Triwest health insurance — $404/mo', '📝', 'Replaced by SafetyWing in Sept ($66/mo)'],
        ['7', 'HighLevel still $497/mo — find ways to reduce', '⚠️', 'Largest SaaS expense'],
        ['8', 'Pre-tax profit was actually strong at 66%', '📝', 'Despite travel month'],
    ]
    
    process_sheet(
        AUG_ID, 'August', '2025',
        AUG_INCOME, AUG_BIZ_EXPENSES, AUG_PERSONAL,
        AUG_METRICS, AUG_MONEY_FLOW, AUG_DEBT, AUG_BALANCES, AUG_ASSETS,
        AUG_ACTIONS,
        txn_tabs_config=[
            {'old_name': 'Biz 4991 Transactions', 'new_name': '💼 Business 4991', 'is_cc': False},
            {'old_name': 'Biz Credit Card transactions', 'new_name': '💳 Biz CC 0678', 'is_cc': True},
            {'old_name': 'Personal Checking 0068', 'new_name': '👤 Personal 0068', 'is_cc': False},
            {'old_name': 'Personal Sapphire Card 4252', 'new_name': '💎 Sapphire 4252', 'is_cc': True},
        ]
    )
    
    time.sleep(2)  # Rate limiting
    
    # SEPTEMBER 2025
    SEPT_ID = '1IuZIUjz4R0umPP3ihciMySq_NgrtO4lxB18hhbtLaSM'
    SEPT_ACTIONS = [
        ['1', 'Cobrand cancelled — verify no future charges', '✅', 'Last charge Sept'],
        ['2', 'Flowith cancelled', '✅', 'Last charge Sept'],
        ['3', 'Spectrum cancelled', '✅', 'Last charge Sept'],
        ['4', 'Ideogram AI — cancel ($8/mo)', '⚠️', 'Low value'],
        ['5', 'CC debt still 80-97% utilization', '⚠️', 'Total CC: $19,335'],
        ['6', 'Switched from Triwest ($404) to SafetyWing ($66)', '✅', 'Saving $338/mo'],
        ['7', 'HighLevel still $507/mo — find ways to reduce', '⚠️', 'Consider downgrade'],
        ['8', 'localrank.so $174/mo — evaluate ROI', '🔍', 'Cancelled later'],
        ['9', 'Investing $1,345/mo while carrying $19k CC debt at 17-22% APR', '⚠️', 'Interest > returns'],
        ['10', 'Strong 70% profit margin despite travel', '📝', 'Income declining from peak'],
    ]
    
    process_sheet(
        SEPT_ID, 'September', '2025',
        SEPT_INCOME, SEPT_BIZ_EXPENSES, SEPT_PERSONAL,
        SEPT_METRICS, SEPT_MONEY_FLOW, SEPT_DEBT, SEPT_BALANCES, SEPT_ASSETS,
        SEPT_ACTIONS,
        txn_tabs_config=[
            {'old_name': 'Chase4991_Activity_20251016', 'new_name': '💼 Business 4991', 'is_cc': False},
            {'old_name': 'Chase0678_Activity20250901_20250930_20251016', 'new_name': '💳 Biz CC 0678', 'is_cc': True},
            {'old_name': 'Chase0068_Activity_20251016', 'new_name': '👤 Personal 0068', 'is_cc': False},
            {'old_name': 'Chase4252_Activity20250901_20250930_20251016', 'new_name': '💎 Sapphire 4252', 'is_cc': True},
        ]
    )
    
    print("\n" + "="*60)
    print("ALL DONE!")
    print("="*60)
    print(f"August:    https://docs.google.com/spreadsheets/d/{AUG_ID}")
    print(f"September: https://docs.google.com/spreadsheets/d/{SEPT_ID}")
