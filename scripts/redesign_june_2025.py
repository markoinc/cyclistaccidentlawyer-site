#!/usr/bin/env python3
"""
Redesign June 2025 Accounting Sheet to match January 2026 format.
Phases: 1) Backup & rename, 2) Clean transactions, 3) Dashboard, 4) Format
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime, timedelta

SHEET_ID = '19YSihOlMi1R-2nkZzfwa1dmoidouGl4UakhjdfceBsg'
TOKEN_FILE = '/home/ec2-user/.config/gcal-pro/token.json'

# Tab sheet IDs (from metadata)
TAB_IDS = {
    'Overview': 0,
    'Biz Credit Card transactions': 332554580,
    'Biz 4991 Transactions': 1255858978,
    'Personal Checking 0068': 845500177,
    'Personal Sapphire Card 4252': 1409199514,
}

# Color constants
NAVY = {'red': 0.106, 'green': 0.165, 'blue': 0.290}  # #1B2A4A
WHITE = {'red': 1, 'green': 1, 'blue': 1}
LIGHT_GREEN = {'red': 0.851, 'green': 0.918, 'blue': 0.827}  # #D9EAD3
LIGHT_RED = {'red': 0.957, 'green': 0.800, 'blue': 0.800}  # #F4CCCC
LIGHT_GRAY = {'red': 0.937, 'green': 0.937, 'blue': 0.937}  # #EFEFEF
ALT_WHITE = {'red': 1, 'green': 1, 'blue': 1}
ALT_GRAY = {'red': 0.961, 'green': 0.961, 'blue': 0.961}  # #F5F5F5
SECTION_BG = {'red': 0.231, 'green': 0.318, 'blue': 0.451}  # #3B516F (section headers)
SUBTOTAL_BG = {'red': 0.898, 'green': 0.910, 'blue': 0.933}  # #E5E8EE

def get_token():
    with open(TOKEN_FILE) as f:
        return json.load(f)['token']

def api_call(method, url, body=None):
    token = get_token()
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers)
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {e.read().decode()[:500]}")
        raise

def batch_update(requests):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate'
    return api_call('POST', url, {'requests': requests})

def batch_values(data, input_option='USER_ENTERED'):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values:batchUpdate'
    return api_call('POST', url, {'valueInputOption': input_option, 'data': data})

def clear_range(range_str):
    encoded = urllib.parse.quote(range_str)
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{encoded}:clear'
    return api_call('POST', url, {})

def serial_to_date(serial):
    """Convert serial date to MM/DD/YYYY"""
    if isinstance(serial, (int, float)) and serial > 40000:
        base = datetime(1899, 12, 30)
        dt = base + timedelta(days=int(serial))
        return dt.strftime('%m/%d/%Y')
    return str(serial)

def serial_to_sortable(serial):
    """Convert serial date for sorting"""
    if isinstance(serial, (int, float)) and serial > 40000:
        return int(serial)
    return 0

# ============================================================
# VENDOR & CATEGORY MAPPING
# ============================================================

def categorize_biz_4991(desc, amount, detail_type=''):
    """Categorize Business 4991 transaction. Returns (vendor, category, notes)"""
    d = desc.upper() if desc else ''
    
    # Income
    if 'STRIPE' in d:
        return ('Stripe', '💰 Income (Stripe)', '')
    if 'ZELLE' in d and 'FROM' in d.upper():
        if 'ACI ENTERPRISE' in d:
            return ('ACI Enterprise (Zelle)', '💰 Income (Zelle)', 'Client subscription')
        if 'EDDY OROZCO' in d:
            return ('Eddy Orozco Reyes (Zelle)', '💰 Income (Zelle)', 'Hooked commissions')
        if 'JONATHAN BIBLE' in d:
            return ('Jonathan Bible (Zelle)', '💰 Income (Zelle)', 'Client payment')
        if 'WILLARD' in d:
            return ('Willard Construction (Zelle)', '💰 Income (Zelle)', 'Client payment')
        return ('Zelle Income', '💰 Income (Zelle)', '')
    
    # Zelle outbound
    if 'ZELLE' in d and 'TO' in d.upper() and 'ROSS' in d:
        return ('Ross Yenerich (Zelle)', '🏢 Operations (Contractor)', 'Logo design')
    
    # Transfers
    if 'TRANSFER TO CHK' in d and '0068' in d:
        return ('Transfer to Personal 0068', 'Biz → Personal', '')
    if 'TRANSFER FROM CHK' in d and '0068' in d:
        return ('Transfer from Personal 0068', 'Personal → Biz', '')
    if 'TRANSFER TO TAXES' in d or 'TRANSFER TO TAX' in d.lower():
        return ('Transfer to Tax Account', '🏦 Tax Transfer', '')
    if 'TRANSFER FROM SAV' in d and '7036' in d:
        return ('Transfer from Savings 7036', 'Savings → Biz', '')
    
    # SaaS & Tools
    if 'APPLE.COM/BILL' in d:
        return ('Apple', '📱 SaaS (Apple)', 'recurring')
    if 'BOOST MOBILE' in d:
        return ('Boost Mobile', '📱 SaaS (Boost Mobile)', 'recurring')
    if 'FLOWITH' in d:
        return ('Flowith', '📱 SaaS (Flowith)', 'recurring')
    if 'HIGHLEVEL AGENCY' in d:
        return ('GoHighLevel (Agency)', '📱 SaaS (GoHighLevel)', 'recurring')
    if 'HIGHLEVEL INC' in d:
        return ('GoHighLevel (Inc)', '📱 SaaS (GoHighLevel)', 'recurring')
    if 'MIDJOURNEY' in d:
        return ('Midjourney', '📱 SaaS (Midjourney)', 'cancelled')
    if 'PHOTOAI' in d:
        return ('PhotoAI.com', '📱 SaaS (PhotoAI)', '')
    
    # Marketing
    if 'CASH APP' in d and 'MARCO DIEMER' in d:
        return ('CashApp Reviews (Marco Diemer)', '📣 Marketing (Reviews)', '')
    if 'CASH APP' in d and 'VIVI' in d:
        return ('CashApp Reviews (Vivi)', '📣 Marketing (Reviews)', '')
    if 'DISCOVERABILITY' in d:
        return ('Discoverability (Reviews)', '📣 Marketing (Reviews)', '')
    if 'INDEXSY' in d:
        return ('Indexsy (Guest Posts)', '📣 Marketing (Guest Posts)', '')
    if 'LOCALRANK' in d:
        return ('LocalRank.so (Citations)', '📣 Marketing (Citations)', '')
    if 'SERPEMPIRE' in d or 'NUV*SERP' in d:
        return ('SerpEmpire (CTR)', '📣 Marketing (CTR Manipulation)', 'cancelled')
    
    # Operations
    if 'MONTHLY SERVICE FEE' in d:
        return ('Chase Monthly Service Fee', '🏢 Operations (Bank Fee)', 'recurring')
    if 'TMOBILE' in d or 'T-MOBILE' in d:
        return ('T-Mobile', '🏢 Operations (Phone)', 'recurring')
    if 'OUTSOURCE SHARKS' in d:
        return ('Outsource Sharks (VA)', '🏢 Operations (VA Outsource)', '')
    
    # Debt
    if 'CREDIT STRONG' in d:
        return ('Credit Strong', '💳 Debt (Credit Builder)', 'recurring')
    if 'SELF LENDER' in d:
        return ('Self Lender', '💳 Debt (Credit Builder)', 'recurring')
    if 'PAYMENT TO CHASE CARD' in d and '0678' in d:
        return ('CC Payment to 0678', '💳 CC Payment', '')
    
    # PayPal/International
    if 'CHUI WAH EVELYN' in d or 'NETTIPALVELU' in d or 'VS NETTI' in d:
        vendor = 'PayPal (Nettipalvelu)' if 'NETTI' in d else 'PayPal (Chui Wah Evelyn)'
        return (vendor, '🏢 Operations (Unknown)', 'Investigate')
    
    return (desc[:40] if desc else 'Unknown', '❓ Uncategorized', 'Review')


def categorize_biz_cc(desc, amount):
    """Categorize Business CC 0678 transaction."""
    d = desc.upper() if desc else ''
    
    if '10WEB' in d:
        return ('10web.io', '📱 SaaS (Hosting)', 'recurring')
    if 'AARON ABKE' in d:
        return ('Aaron Abke', '📱 SaaS (Subscription)', 'cancelled')
    if 'CANVA' in d:
        return ('Canva', '📱 SaaS (Design)', 'recurring')
    if 'FACEBK' in d or 'FACEBOOK' in d:
        return ('Meta / Facebook Ads', '📣 Marketing (Meta Ads)', 'cancelled mid-month')
    if 'GOOGLE' in d and 'ONE' in d:
        return ('Google One', '📱 SaaS (Cloud Storage)', 'recurring')
    if 'GOOGLE' in d and 'GSUITE' in d:
        return ('Google Workspace', '📱 SaaS (Email/Business)', 'recurring')
    if 'IDEOGRAM' in d:
        return ('Ideogram AI', '📱 SaaS (AI Image Gen)', 'recurring')
    if 'LOCALRANK' in d:
        return ('LocalRank.so', '📱 SaaS (SEO Tool)', 'recurring')
    if 'NAME-CHEAP' in d or 'NAMECHEAP' in d:
        return ('Namecheap', '🏢 Operations (Domains)', '')
    if 'OPENAI' in d or 'CHATGPT' in d:
        return ('ChatGPT (OpenAI)', '📱 SaaS (AI)', 'recurring')
    if 'PAYMENT' in d and ('THANK' in d or 'MOBILE' in d):
        return ('CC Payment Received', '💳 CC Payment', '')
    if 'REGUS' in d:
        return ('Regus', '🏢 Operations (Coworking)', 'recurring')
    if 'SPECTRUM' in d:
        return ('Spectrum', '🏢 Operations (Internet)', 'recurring')
    if 'SPOTIFY' in d:
        return ('Spotify', '📱 SaaS (Music)', 'recurring')
    
    return (desc[:40] if desc else 'Unknown', '❓ Uncategorized', 'Review')


def categorize_personal_0068(desc, amount):
    """Categorize Personal 0068 transaction."""
    d = desc.upper() if desc else ''
    
    # Transfers
    if 'TRANSFER FROM CHK' in d and '4991' in d:
        return ('Transfer from Biz 4991', 'Biz → Personal', '')
    if 'TRANSFER TO CHK' in d and '4991' in d:
        return ('Transfer to Biz 4991', 'Personal → Biz', '')
    if 'TRANSFER FROM SAV' in d and '7036' in d:
        return ('Transfer from Savings 7036', 'Savings → Personal', '')
    if 'TRANSFER TO SAV' in d and '7036' in d:
        return ('Transfer to Savings 7036', 'Personal → Savings', '')
    if 'ODP TRANSFER FROM SAVINGS' in d:
        return ('Transfer from Savings 7036 (ODP)', 'Savings → Personal', 'Overdraft protection')
    
    # Investments
    if 'ROBINHOOD' in d:
        return ('Robinhood', '📈 Investment (Robinhood)', 'Daily recurring')
    if 'ACORNS ROUND' in d:
        return ('Acorns (Round-Ups)', '📈 Investment (Acorns)', '')
    if 'SUBSCRIPTION ACORNS' in d:
        return ('Acorns (Subscription)', '📈 Investment (Acorns)', '')
    
    # Debt Payments
    if 'CHASE CREDIT CRD AUTOPAY' in d:
        return ('Chase Sapphire CC Payment', '💳 CC Payment', '')
    if 'DEPT EDUCATION' in d or 'STUDENT LN' in d:
        return ('Student Loan Payment', '💳 Debt (Student Loan)', 'recurring')
    if 'DISCOVER E-PAYMENT' in d:
        return ('Discover CC Payment', '💳 CC Payment', '')
    
    # Housing
    if 'ZELLE' in d and 'PATRICK' in d:
        return ('Rent (Patrick Landlord)', '🏠 Housing (Rent)', '')
    if 'WE ENERGIES' in d:
        return ('We Energies', '🏠 Housing (Utilities)', '')
    
    # Food & Groceries
    if 'WHOLEFDS' in d or 'WHOLE FOODS' in d:
        return ('Whole Foods', '🛒 Groceries', '')
    if 'PICK N SAVE' in d:
        return ("Pick 'n Save", '🛒 Groceries', '')
    if 'TRADER JOE' in d:
        return ("Trader Joe's", '🛒 Groceries', '')
    if 'SPARROW HILL' in d:
        return ('Sparrow Hill Farm', '🛒 Groceries (Farm)', '')
    if 'SENDIKS' in d:
        return ("Sendik's", '🛒 Groceries', '')
    if 'COLECTIVO' in d:
        return ('Colectivo Coffee', '☕ Food (Coffee)', '')
    if 'ROCHAMBO' in d:
        return ('Rochambo Coffee', '☕ Food (Coffee)', '')
    if 'STONE CREEK' in d:
        return ('Stone Creek Coffee', '☕ Food (Coffee)', '')
    if 'TROPICAL SMOOTHIE' in d:
        return ('Tropical Smoothie', '🍔 Food (Dining)', '')
    if 'CULVERS' in d:
        return ("Culver's", '🍔 Food (Dining)', '')
    if 'LA MICHOACANA' in d:
        return ('La Michoacana', '🍔 Food (Dining)', '')
    if 'TRINITY THREE' in d:
        return ('Trinity Three Irish Pub', '🍔 Food (Bar)', '')
    if 'TST*BRUNCH' in d:
        return ('Brunch Cedarburg', '🍔 Food (Dining)', '')
    if 'TST*PETES PUB' in d:
        return ("Pete's Pub", '🍔 Food (Bar)', '')
    if 'DINNER DETECTIVE' in d:
        return ('Dinner Detective', '🎮 Entertainment (Dining)', "Magen's Bday")
    
    # Subscriptions
    if 'HULU' in d:
        return ('Hulu', '📺 Subscriptions', 'recurring')
    if 'SOLSTICE' in d:
        return ('Solstice Dental Insurance', '🏥 Insurance (Dental)', 'recurring')
    
    # Shopping
    if 'AMAZON' in d:
        return ('Amazon', '🛒 Shopping', '')
    if 'TARGET' in d:
        return ('Target', '🛒 Shopping', '')
    if 'OLD NAVY' in d:
        return ('Old Navy', '🛒 Shopping (Clothing)', '')
    if 'CLOSET CLASSICS' in d:
        return ('Closet Classics', '🛒 Shopping (Thrift)', '')
    if 'DOWNER HARDWARE' in d:
        return ('Downer Hardware', '🛒 Shopping (Hardware)', '')
    if 'CVS' in d:
        return ('CVS Pharmacy', '🛒 Shopping (Pharmacy)', '')
    if 'STAR SEED' in d or 'ASCENDED' in d:
        return ('Star Seed / Ascended Gifts', '💆 Personal Care (Wellness)', '')
    if 'SALON MAYFAIR' in d:
        return ('Salon Mayfair', '💇 Personal Care', '')
    
    # Transportation
    if 'LIME' in d:
        return ('Lime Scooter', '🚗 Transportation (Scooter)', '')
    if 'BP#' in d or 'EXXON' in d or 'KWIK TRIP' in d:
        name = 'BP Gas' if 'BP#' in d else ('Exxon' if 'EXXON' in d else 'Kwik Trip')
        return (name, '🚗 Transportation (Gas)', '')
    if 'JETZ' in d:
        return ('Jetz Car Wash', '🚗 Transportation (Car Wash)', '')
    if 'DUNES TRAVEL' in d or 'ITR CONCESSION' in d or 'SKYWAY' in d:
        return ('Travel Stop', '🚗 Transportation', '')
    if 'TOLL' in d:
        return ('Tolls', '🚗 Transportation (Tolls)', '')
    
    # ATM
    if 'NON-CHASE ATM FEE' in d:
        return ('ATM Fee', '🏧 ATM Fee', '')
    if 'NON-CHASE ATM WITHDRAW' in d or ('ATM' in d and amount and amount < 0):
        return ('ATM Withdrawal', '🏧 ATM Withdrawal', '')
    
    # Personal
    if 'APPLE CASH' in d:
        return ('Apple Cash (to Magen)', '💝 Personal (Gift)', '')
    if 'GLASSHOUSE' in d:
        return ('The Glasshouse', '🛒 Shopping (Vape)', '')
    if 'A Z VAPE' in d or 'MB SMOKE' in d:
        name = 'A-Z Vape' if 'A Z' in d else 'MB Smoke Shop'
        return (name, '🛒 Shopping (Smoke/Vape)', '')
    if 'NINTENDO' in d:
        return ('Nintendo (Minecraft)', '🎮 Entertainment', '')
    if 'BLUEMOUND BOWL' in d:
        return ('Bluemound Bowl', '🎮 Entertainment (Bowling)', '')
    
    return (desc[:40] if desc else 'Unknown', '❓ Uncategorized', 'Review')


def categorize_sapphire(desc, amount):
    """Categorize Personal Sapphire 4252 transaction."""
    d = desc.upper() if desc else ''
    
    if 'INTEREST' in d:
        return ('Interest Charge', '💰 CC Interest', '')
    if 'PAYMENT' in d:
        return ('CC Payment Received', '💳 CC Payment', '')
    if 'ELITE NORTH SHORE' in d:
        return ('Elite North Shore (Gym)', '🏋️ Health (Gym)', 'recurring — cancel!!')
    
    return (desc[:40] if desc else 'Unknown', '❓ Uncategorized', '')


# ============================================================
# PHASE 1: Create backup, rename tabs
# ============================================================

def phase1_backup_and_rename():
    print("=== PHASE 1: Backup & Rename ===")
    
    # Add Raw Data tab
    requests = [
        {
            'addSheet': {
                'properties': {
                    'title': '📦 Raw Data',
                    'index': 5,
                    'gridProperties': {'rowCount': 200, 'columnCount': 30}
                }
            }
        }
    ]
    result = batch_update(requests)
    raw_sheet_id = result['replies'][0]['addSheet']['properties']['sheetId']
    print(f"  Created '📦 Raw Data' tab (sheetId={raw_sheet_id})")
    
    # Read current Overview data
    token = get_token()
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/Overview?valueRenderOption=FORMATTED_VALUE'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    resp = urllib.request.urlopen(req)
    overview_data = json.loads(resp.read()).get('values', [])
    
    # Write Overview data to Raw Data
    if overview_data:
        header = [['=== ORIGINAL OVERVIEW TAB (June 2025) — Preserved for Reference ===']]
        batch_values([{
            'range': "'📦 Raw Data'!A1",
            'values': header + [['']] + overview_data
        }])
        print(f"  Backed up Overview ({len(overview_data)} rows) to Raw Data tab")
    
    # Rename tabs
    rename_requests = [
        {'updateSheetProperties': {'properties': {'sheetId': 0, 'title': '📊 Dashboard'}, 'fields': 'title'}},
        {'updateSheetProperties': {'properties': {'sheetId': 332554580, 'title': '💳 Biz CC 0678'}, 'fields': 'title'}},
        {'updateSheetProperties': {'properties': {'sheetId': 1255858978, 'title': '💼 Business 4991'}, 'fields': 'title'}},
        {'updateSheetProperties': {'properties': {'sheetId': 845500177, 'title': '👤 Personal 0068'}, 'fields': 'title'}},
        {'updateSheetProperties': {'properties': {'sheetId': 1409199514, 'title': '💎 Sapphire 4252'}, 'fields': 'title'}},
    ]
    
    # Reorder tabs: Dashboard first, then transaction tabs, then Raw Data
    rename_requests += [
        {'updateSheetProperties': {'properties': {'sheetId': 0, 'index': 0}, 'fields': 'index'}},
        {'updateSheetProperties': {'properties': {'sheetId': 1255858978, 'index': 1}, 'fields': 'index'}},
        {'updateSheetProperties': {'properties': {'sheetId': 845500177, 'index': 2}, 'fields': 'index'}},
        {'updateSheetProperties': {'properties': {'sheetId': 332554580, 'index': 3}, 'fields': 'index'}},
        {'updateSheetProperties': {'properties': {'sheetId': 1409199514, 'index': 4}, 'fields': 'index'}},
        {'updateSheetProperties': {'properties': {'sheetId': raw_sheet_id, 'index': 5}, 'fields': 'index'}},
    ]
    
    batch_update(rename_requests)
    print("  Renamed and reordered all tabs")
    
    # Clear all content from the main tabs
    for tab in ['📊 Dashboard', '💼 Business 4991', '👤 Personal 0068', '💳 Biz CC 0678', '💎 Sapphire 4252']:
        try:
            clear_range(f"'{tab}'!A:Z")
        except:
            clear_range(f"'{tab}'!A1:Z1000")
    print("  Cleared all tab content")
    
    return raw_sheet_id


# ============================================================
# PHASE 2: Process and write cleaned transactions
# ============================================================

# Raw data from the spreadsheet (extracted earlier)
BIZ_4991_RAW = [
    ["DEBIT", 45824, "APPLE.COM/BILL 866-712-7753 CA 06/15", -9.99, "DEBIT_CARD", 1661.38],
    ["DEBIT", 45826, "APPLE.COM/BILL 866-712-7753 CA 06/17", -5.24, "DEBIT_CARD", 2573.6],
    ["DEBIT", 45811, "BOOST MOBILE HTTPS://WWW.D CO 06/02", -66.62, "DEBIT_CARD", 3047.43],
    ["DEBIT", 45814, "CASH APP*MARCO DIEMER Oakland CA 06/05", -7, "DEBIT_CARD", 1969.23],
    ["DEBIT", 45817, "CASH APP*MARCO DIEMER Oakland CA 06/06", -7, "DEBIT_CARD", 2316.53],
    ["DEBIT", 45817, "CASH APP*MARCO DIEMER Oakland CA 06/06", -7, "DEBIT_CARD", 2323.53],
    ["DEBIT", 45814, "CASH APP*MARCO DIEMER Oakland CA 06/06", -7, "DEBIT_CARD", 1550.53],
    ["DEBIT", 45817, "CASH APP*MARCO DIEMER Oakland CA 06/07", -7, "DEBIT_CARD", 2289.63],
    ["DEBIT", 45817, "CASH APP*MARCO DIEMER Oakland CA 06/08", -7, "DEBIT_CARD", 2062.63],
    ["DEBIT", 45817, "CASH APP*MARCO DIEMER Oakland CA 06/08", -20, "DEBIT_CARD", 2069.63],
    ["DEBIT", 45818, "CASH APP*MARCO DIEMER Oakland CA 06/09", -7, "DEBIT_CARD", 2262.88],
    ["DEBIT", 45818, "CASH APP*MARCO DIEMER Oakland CA 06/09", -20, "DEBIT_CARD", 2269.88],
    ["DEBIT", 45819, "CASH APP*MARCO DIEMER Oakland CA 06/10", -7, "DEBIT_CARD", 2197.88],
    ["DEBIT", 45819, "CASH APP*MARCO DIEMER Oakland CA 06/10", -10, "DEBIT_CARD", 2204.88],
    ["DEBIT", 45820, "CASH APP*VIVI Oakland CA 06/11", -10, "DEBIT_CARD", 2245.48],
    ["DEBIT", 45820, "DISCOVERABILITY.CO DISCOVERABILI PA 06/11", -89.6, "DEBIT_CARD", 2255.48],
    ["DEBIT", 45821, "DISCOVERABILITY.CO DISCOVERABILI PA 06/12", -89.6, "DEBIT_CARD", 2426.73],
    ["DEBIT", 45821, "DISCOVERABILITY.CO DISCOVERABILI PA 06/12", -89.6, "DEBIT_CARD", 2516.33],
    ["DEBIT", 45826, "DISCOVERABILITY.CO DISCOVERABILI PA 06/17", -89.6, "DEBIT_CARD", 2484],
    ["DEBIT", 45817, "FLOWITH.IO FLOWITH.IO CO 06/07", -19.9, "DEBIT_CARD", 2296.63],
    ["DEBIT", 45832, "FLOWITH.IO FLOWITH.IO CO 06/23", -20, "DEBIT_CARD", 1617.39],
    ["DEBIT", 45814, "HIGHLEVEL AGENCY SUB GOHIGHLEVEL.C TX 06/06", -297, "DEBIT_CARD", 1591.23],
    ["DEBIT", 45814, "HIGHLEVEL INC. GOHIGHLEVEL.C TX 06/05", -100, "DEBIT_CARD", 1976.23],
    ["DEBIT", 45825, "HIGHLEVEL INC. GOHIGHLEVEL.C TX 06/17", -100, "DEBIT_CARD", 2628.84],
    ["DEBIT", 45838, "HIGHLEVEL INC. GOHIGHLEVEL.C TX 06/28", -100, "DEBIT_CARD", 2269.41],
    ["DEBIT", 45814, "INDEXSY RICHMOND BC 06/05", -81, "DEBIT_CARD", 1888.23],
    ["DEBIT", 45813, "INDEXSY RICHMOND BC 06/05", -81, "DEBIT_CARD", 2909.93],
    ["DEBIT", 45832, "INDEXSY RICHMOND BC 06/23", -81, "DEBIT_CARD", 1637.39],
    ["DEBIT", 45826, "LOCALRANK.SO RICHMOND BC 06/17", -350, "DEBIT_CARD", 1784],
    ["DEBIT", 45826, "LOCALRANK.SO RICHMOND BC 06/17", -350, "DEBIT_CARD", 2134],
    ["DEBIT", 45828, "LOCALRANK.SO RICHMOND BC 06/19", -350, "DEBIT_CARD", 2593.14],
    ["DEBIT", 45825, "MIDJOURNEY INC. MIDJOURNEY.CO CA 06/16", -10.79, "DEBIT_CARD", 2728.84],
    ["DEBIT", 45838, "MONTHLY SERVICE FEE", -15, "FEE_TRANSACTION", 1954.41],
    ["DEBIT", 45831, "NUV*SERPEMPIRE LAS PALMAS DE 06/20", -79, "DEBIT_CARD", 2214.14],
    ["DEBIT", 45813, "Online Realtime Transfer to Taxes 3485 transaction#: 25018156040 reference#: 9018156040RX 06/05", -400, "ACCT_XFER", 2109.93],
    ["CREDIT", 45810, "Online Transfer from CHK ...0068 transaction#: 24987735122", 200, "ACCT_XFER", 1987.1],
    ["DEBIT", 45817, "Online Transfer to CHK ...0068 transaction#: 24864779945 06/09", -350, "ACCT_XFER", 1712.63],
    ["DEBIT", 45810, "Online Transfer to CHK ...0068 transaction#: 24983957451 06/02", -100, "ACCT_XFER", 1874.6],
    ["DEBIT", 45811, "Online Transfer to CHK ...0068 transaction#: 24997652343 06/03", -300, "ACCT_XFER", 2747.43],
    ["DEBIT", 45811, "Online Transfer to CHK ...0068 transaction#: 24998944360 06/03", -200, "ACCT_XFER", 2547.43],
    ["DEBIT", 45813, "Online Transfer to CHK ...0068 transaction#: 25018168956 06/05", -100, "ACCT_XFER", 2809.93],
    ["DEBIT", 45814, "Online Transfer to CHK ...0068 transaction#: 25038102461 06/06", -100, "ACCT_XFER", 1450.53],
    ["DEBIT", 45817, "Online Transfer to CHK ...0068 transaction#: 25058860082 06/09", -100, "ACCT_XFER", 2189.63],
    ["DEBIT", 45817, "Online Transfer to CHK ...0068 transaction#: 25059389690 06/09", -100, "ACCT_XFER", 2089.63],
    ["DEBIT", 45831, "Online Transfer to CHK ...0068 transaction#: 25066965786 06/23", -350, "ACCT_XFER", 1741.14],
    ["DEBIT", 45819, "Online Transfer to CHK ...0068 transaction#: 25091715290 06/11", -200, "ACCT_XFER", 1997.88],
    ["DEBIT", 45821, "Online Transfer to CHK ...0068 transaction#: 25116240381 06/13", -100, "ACCT_XFER", 2326.73],
    ["DEBIT", 45821, "Online Transfer to CHK ...0068 transaction#: 25118775938 06/13", -100, "ACCT_XFER", 2226.73],
    ["DEBIT", 45824, "Online Transfer to CHK ...0068 transaction#: 25134253375 06/16", -300, "ACCT_XFER", 1871.37],
    ["DEBIT", 45824, "Online Transfer to CHK ...0068 transaction#: 25137260105 06/16", -200, "ACCT_XFER", 1671.37],
    ["DEBIT", 45825, "Online Transfer to CHK ...0068 transaction#: 25162630164 06/17", -50, "ACCT_XFER", 2578.84],
    ["DEBIT", 45826, "Online Transfer to CHK ...0068 transaction#: 25171868585 06/18", -100, "ACCT_XFER", 1684],
    ["DEBIT", 45826, "Online Transfer to CHK ...0068 transaction#: 25176301526 06/18", -100, "ACCT_XFER", 1584],
    ["DEBIT", 45828, "Online Transfer to CHK ...0068 transaction#: 25198212221 06/20", -300, "ACCT_XFER", 2293.14],
    ["DEBIT", 45831, "Online Transfer to CHK ...0068 transaction#: 25230548055 06/23", -600, "ACCT_XFER", 1141.14],
    ["DEBIT", 45832, "Online Transfer to CHK ...0068 transaction#: 25245750219 06/24", -160, "ACCT_XFER", 1457.39],
    ["DEBIT", 45833, "Online Transfer to CHK ...0068 transaction#: 25250838090 06/25", -200, "ACCT_XFER", 1257.39],
    ["DEBIT", 45833, "Online Transfer to CHK ...0068 transaction#: 25251746150 06/25", -200, "ACCT_XFER", 1057.39],
    ["DEBIT", 45835, "Online Transfer to CHK ...0068 transaction#: 25276252991 06/27", -300, "ACCT_XFER", 2369.41],
    ["DEBIT", 45838, "Online Transfer to CHK ...0068 transaction#: 25297995141 06/30", -100, "ACCT_XFER", 2169.41],
    ["DEBIT", 45838, "Online Transfer to CHK ...0068 transaction#: 25314096811 06/30", -200, "ACCT_XFER", 1969.41],
    ["DEBIT", 45814, "ORIG CO NAME:CHUI WAH EVELYN ORIG ID:770510487C DESC DATE: CO ENTRY DESCR:IAT PAYPALSEC:WEB TRACE#:091000017677393 EED:250606 IND ID:1042678399372 IND NAME:MARK GUNDRUM IATCV TRN: 1577677393TC", -33.7, "MISC_DEBIT", 1557.53],
    ["DEBIT", 45813, "ORIG CO NAME:CHUI WAH EVELYN ORIG ID:770510487C DESC DATE: CO ENTRY DESCR:IAT PAYPALSEC:WEB TRACE#:091000018924341 EED:250605 IND ID:1042662203930 IND NAME:MARK GUNDRUM IATCV TRN: 1568924341TC", -33.7, "MISC_DEBIT", 2076.23],
    ["DEBIT", 45831, "ORIG CO NAME:Credit Strong ORIG ID:5122002794 DESC DATE:062125 CO ENTRY DESCR:CSTR PAYMTSEC:WEB TRACE#:114994031228864 EED:250623 IND ID:2138568 IND NAME:Mark Gundrum TRN: 1741228864TC", -90, "MISC_DEBIT", 2091.14],
    ["DEBIT", 45818, "ORIG CO NAME:SELF LENDER INC ORIG ID:473596202 DESC DATE: CO ENTRY DESCR:PAYMENTS SEC:WEB TRACE#:096001013511460 EED:250610 IND ID:116875136 IND NAME:MARK GUNDRUM TRN: 1613511460TC", -48, "MISC_DEBIT", 2214.88],
    ["CREDIT", 45825, "ORIG CO NAME:STRIPE ORIG ID: 800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:043305133159492 EED:250617 IND ID:ST-V9X2V3I1H1U7 IND NAME:MARK GUNDRUM TRN: 1683159492TC", 177.25, "ACH_CREDIT", 2739.63],
    ["CREDIT", 45813, "ORIG CO NAME:STRIPE ORIG ID: 800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:043305139090534 EED:250605 IND ID:ST-R8F6S0X2R3P0 IND NAME:MARK GUNDRUM TRN: 1569090534TC", 347.2, "ACH_CREDIT", 2990.93],
    ["CREDIT", 45821, "ORIG CO NAME:STRIPE ORIG ID: 800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:043305139208950 EED:250613 IND ID:ST-D9J7A0O3A8J5 IND NAME:MARK GUNDRUM TRN: 1649208950TC", 360.45, "ACH_CREDIT", 2605.93],
    ["CREDIT", 45818, "ORIG CO NAME:STRIPE ORIG ID:1800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:091000012760000 EED:250610 IND ID:ST-H1S5B9X5H9B9 IND NAME:MARK GUNDRUM TRN: 1612760000TC", 577.25, "ACH_CREDIT", 2289.88],
    ["CREDIT", 45828, "ORIG CO NAME:STRIPE ORIG ID:1800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:091000013662225 EED:250620 IND ID:ST-P4R8D6J3Y6C6 IND NAME:MARK GUNDRUM TRN: 1713662225TC", 709.14, "ACH_CREDIT", 2293.14],
    ["CREDIT", 45812, "ORIG CO NAME:STRIPE ORIG ID:1800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:091000018578982 EED:250604 IND ID:ST-M3T1F3J1E7U1 IND NAME:MARK GUNDRUM TRN: 1558578982TC", 96.3, "ACH_CREDIT", 2643.73],
    ["CREDIT", 45832, "ORIG CO NAME:STRIPE ORIG ID:1800948598 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:091000019242260 EED:250624 IND ID:ST-X7A5K0J5N9J6 IND NAME:MARK GUNDRUM TRN: 1759242260TC", 577.25, "ACH_CREDIT", 1718.39],
    ["CREDIT", 45834, "ORIG CO NAME:STRIPE ORIG ID:4270465600 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:111000022812423 EED:250626 IND ID:ST-U5E9B4D2B3N9 IND NAME:MARK GUNDRUM TRN: 1772812423TC", 711.02, "ACH_CREDIT", 1768.41],
    ["CREDIT", 45811, "ORIG CO NAME:STRIPE ORIG ID:4270465600 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:111000028916589 EED:250603 IND ID:ST-Y0W8O4S9F2S3 IND NAME:MARK GUNDRUM TRN: 1548916589TC", 239.45, "ACH_CREDIT", 3114.05],
    ["CREDIT", 45820, "ORIG CO NAME:STRIPE ORIG ID:4270465600 DESC DATE: CO ENTRY DESCR:TRANSFER SEC:CCD TRACE#:111000029593979 EED:250612 IND ID:ST-R8A6Z4S8H5E2 IND NAME:MARK GUNDRUM TRN: 1639593979TC", 347.2, "ACH_CREDIT", 2345.08],
    ["DEBIT", 45831, "ORIG CO NAME:VS NETTIPALVELU ORIG ID:770510487C DESC DATE: CO ENTRY DESCR:IAT PAYPALSEC:WEB TRACE#:091000016335125 EED:250623 IND ID:1042998025519 IND NAME:MARK GUNDRUM IATCV TRN: 1746335125TC", -33, "MISC_DEBIT", 2181.14],
    ["DEBIT", 45824, "OUTSOURCE SHARKS, LL OUTSOURCESHAR DE 06/15", -99, "DEBIT_CARD", 1562.38],
    ["DEBIT", 45813, "Payment to Chase card ending in 0678 06/05", -300, "LOAN_PMT", 2509.93],
    ["DEBIT", 45835, "PHOTOAI.COM SINGAPORE 06/26", -99, "DEBIT_CARD", 2669.41],
    ["DEBIT", 45824, "TMOBILE*AUTO PAY 800-937-8997 WA 06/13", -55.36, "DEBIT_CARD", 2171.37],
    ["CREDIT", 45811, "Zelle payment from ACI ENTERPRISE, LLC WFCT0YWDL6TT", 1000, "PARTNERFI_TO_CHASE", 2874.6],
    ["CREDIT", 45825, "Zelle payment from ACI ENTERPRISE, LLC WFCT0YXS6FQM", 1000, "PARTNERFI_TO_CHASE", 2562.38],
    ["CREDIT", 45817, "Zelle payment from Eddy Orozco Reyes BBT313330046", 880, "PARTNERFI_TO_CHASE", 2330.53],
    ["CREDIT", 45828, "Zelle payment from Eddy Orozco Reyes BBT315328369", 650, "PARTNERFI_TO_CHASE", 2943.14],
    ["CREDIT", 45810, "Zelle payment from JONATHAN BIBLE WFCT0YVZZ88V", 350, "PARTNERFI_TO_CHASE", 1787.1],
    ["CREDIT", 45835, "Zelle payment from WILLARD CONSTRUCTION GROUP LLC BACm5rqwes8p", 1000, "PARTNERFI_TO_CHASE", 2768.41],
    ["DEBIT", 45810, "Zelle payment to ROSS YENERICH JPM99baj11at", -12.5, "CHASE_TO_PARTNERFI", 1974.6],
]

BIZ_CC_RAW = [
    [678, 45809, 45810, "10WEB.IO", "Professional Services", "Sale", -136],
    [678, 45807, 45809, "AARON ABKE", "Merchandise & Inventory", "Sale", -99],
    [678, 45813, 45814, "CANVA* I04538-81050357", "Professional Services", "Sale", -15],
    [678, 45815, 45816, "FACEBK *2JS4QSLXC2", "Professional Services", "Sale", -19.68],
    [678, 45815, 45816, "FACEBK *8EC45RCXC2", "Professional Services", "Sale", -4.8],
    [678, 45810, 45811, "FACEBK *P46HHR4YC2", "Professional Services", "Sale", -48],
    [678, 45825, 45826, "FACEBK *QRZERUUXC2", "Professional Services", "Sale", -53],
    [678, 45815, 45816, "GOOGLE *Google One", "Office & Shipping", "Return", 0.64],
    [678, 45809, 45810, "GOOGLE *GSUITE_kuriosb", "Professional Services", "Sale", -28.8],
    [678, 45813, 45814, "IDEOGRAM AI", "Office & Shipping", "Sale", -20],
    [678, 45823, 45824, "LOCALRANK.SO", "Office & Shipping", "Sale", -174.3],
    [678, 45826, 45827, "NAME-CHEAP.COM* 8EQWUX", "Professional Services", "Sale", -11.46],
    [678, 45826, 45827, "NAME-CHEAP.COM* 92TWTO", "Professional Services", "Sale", -11.46],
    [678, 45819, 45819, "NAME-CHEAP.COM* 9J05GQ", "Professional Services", "Sale", -11.46],
    [678, 45818, 45819, "NAME-CHEAP.COM* EWKE4G", "Professional Services", "Sale", -17.16],
    [678, 45807, 45809, "NAME-CHEAP.COM* LFYNBT", "Professional Services", "Sale", -17.16],
    [678, 45814, 45816, "OPENAI *CHATGPT SUBSCR", "Office & Shipping", "Sale", -20],
    [678, 45813, 45813, "Payment Thank You-Mobile", "", "Payment", 300],
    [678, 45828, 45830, "Regus Management Group BC", "Professional Services", "Sale", -99],
    [678, 45826, 45827, "Spectrum", "Bills & Utilities", "Sale", -60],
    [678, 45831, 45832, "SPOTIFY", "Bills & Utilities", "Sale", -12.59],
]

PERSONAL_0068_RAW = [
    ["DEBIT", 45838, "A Z VAPE AND TOBACCO MILWAUKEE WI 06/27", -11.29, "DEBIT_CARD", 478.12],
    ["DEBIT", 45817, "Acorns Round-Ups Transfer 04WJGQ1 WEB ID: 9000142693", -6.02, "MISC_DEBIT", 441.27],
    ["DEBIT", 45831, "Acorns Round-Ups Transfer 37WCRQ1 WEB ID: 9000142693", -6.28, "MISC_DEBIT", 1248.67],
    ["DEBIT", 45838, "Acorns Round-Ups Transfer 3MJDXQ1 WEB ID: 9000142693", -7.22, "MISC_DEBIT", 219.46],
    ["DEBIT", 45831, "Acorns Round-Ups Transfer 4B55QQ1 WEB ID: 9000142693", -9.72, "MISC_DEBIT", 1254.95],
    ["DEBIT", 45810, "Acorns Round-Ups Transfer 900P9Q1 WEB ID: 9000142693", -5.56, "MISC_DEBIT", 505.36],
    ["DEBIT", 45826, "Acorns Round-Ups Transfer 95MFNQ1 WEB ID: 9000142693", -18.12, "MISC_DEBIT", 286.31],
    ["DEBIT", 45819, "Acorns Round-Ups Transfer B24QHQ1 WEB ID: 9000142693", -6.66, "MISC_DEBIT", 433.51],
    ["DEBIT", 45834, "Acorns Round-Ups Transfer DZWPTQ1 WEB ID: 9000142693", -9.58, "MISC_DEBIT", 118.86],
    ["DEBIT", 45838, "Acorns Round-Ups Transfer PGF0WQ1 WEB ID: 9000142693", -7.3, "MISC_DEBIT", 226.68],
    ["DEBIT", 45817, "Acorns Round-Ups Transfer YNX5FQ1 WEB ID: 9000142693", -11.94, "MISC_DEBIT", 644.83],
    ["DEBIT", 45817, "AMAZON MKTPL*NH9GG1V Amzn.com/bill WA 06/06", -22.64, "DEBIT_CARD", 698.36],
    ["DEBIT", 45812, "Amazon.com*N692220S0 Amzn.com/bill WA 06/04", -115.43, "DEBIT_CARD", 243.09],
    ["DEBIT", 45824, "APPLE CASH SENT MONE 1INFINITELOOP CA 06/15", -100, "DEBIT_CARD", 248.27],
    ["DEBIT", 45838, "APPLE CASH SENT MONE 1INFINITELOOP CA 06/28", -100, "DEBIT_CARD", 513.38],
    ["DEBIT", 45824, "ASCENDED GIFTS MILWAUKEE WI 06/13", -89.76, "DEBIT_CARD", 679.35],
    ["DEBIT", 45824, "BLUEMOUND BOWL BROOKFIELD WI 06/15", -45, "DEBIT_CARD", 203.27],
    ["DEBIT", 45826, "BP#1017900PEWAUKEE BP PEWAUKEE WI 834700 06/18", -37.42, "DEBIT_CARD", 197.89],
    ["DEBIT", 45824, "BP#8513194BP PANTRY 41 MILWAUKEE WI 018365 06/16", -9.09, "DEBIT_CARD", 134.52],
    ["DEBIT", 45813, "BP#8513194BP PANTRY 41# MILWAUKEE WI 06/04", -37.06, "DEBIT_CARD", 210.03],
    ["DEBIT", 45831, "CHASE CREDIT CRD AUTOPAY PPD ID: 4760039224", -218, "ACH_DEBIT", 1264.67],
    ["DEBIT", 45814, "CLOSET CLASSICS MILWAUKEE WI 06/04", -11.71, "DEBIT_CARD", 232.58],
    ["DEBIT", 45821, "CLOSET CLASSICS MILWAUKEE WI 06/11", -10.89, "DEBIT_CARD", 301.62],
    ["DEBIT", 45831, "CLOSET CLASSICS MILWAUKEE WI 06/19", -10.78, "DEBIT_CARD", 1600.25],
    ["DEBIT", 45834, "CLOSET CLASSICS MILWAUKEE WI 06/24", -10.89, "DEBIT_CARD", 183.01],
    ["DEBIT", 45824, "CULVERS OF SHOREWOOD SHOREWOOD WI 06/13", -32.26, "DEBIT_CARD", 557.09],
    ["DEBIT", 45817, "CVS/PHARMACY #08 08767 MILWAUKEE WI 802616 06/08", -18.79, "DEBIT_CARD", 447.29],
    ["DEBIT", 45818, "DEPT EDUCATION STUDENT LN PPD ID: 9102001001", -106.34, "ACH_DEBIT", 306.93],
    ["DEBIT", 45824, "DISCOVER E-PAYMENT 6820 WEB ID: 3510020270", -127, "ACH_DEBIT", 430.09],
    ["DEBIT", 45825, "DOWNER HARDWARE INC. MILWAUKEE WI 06/16", -13.39, "DEBIT_CARD", 171.13],
    ["DEBIT", 45810, "DUNES TRAVEL PLA SAWYER MI 136585 06/02", -30.78, "DEBIT_CARD", 449.58],
    ["DEBIT", 45834, "EXXON GLENDALE ARC GLENDALE WI 06/25", -38.57, "DEBIT_CARD", 144.44],
    ["DEBIT", 45828, "HULU SANTA MONICA CA 356898 06/20", -32.36, "DEBIT_CARD", 314.31],
    ["DEBIT", 45810, "ITR CONCESSION COMPANY ELKHART IN 05/30", -1.8, "DEBIT_CARD", 534.92],
    ["DEBIT", 45810, "ITR CONCESSION COMPANY ELKHART IN 05/30", -4.5, "DEBIT_CARD", 536.72],
    ["DEBIT", 45824, "JETZ 4524 MILWAUKEE WI 865644 06/14", -37.45, "DEBIT_CARD", 376.64],
    ["DEBIT", 45810, "KWIK TRIP 290 OAK CREEK WI 581303 06/02", -6.56, "DEBIT_CARD", 443.02],
    ["DEBIT", 45824, "LA MICHOACANA PREMIUM M MILWAUKEE WI 06/14", -28.37, "DEBIT_CARD", 348.27],
    ["DEBIT", 45838, "LIME*2 RIDES IHF6 LI.ME CA 06/28", -8.05, "DEBIT_CARD", 613.38],
    ["DEBIT", 45810, "LIME*RIDE IHF6 LI.ME CA 06/01", -3.18, "DEBIT_CARD", 549.02],
    ["DEBIT", 45817, "LIME*RIDE IHF6 LI.ME CA 06/07", -4.02, "DEBIT_CARD", 672.77],
    ["DEBIT", 45819, "LIME*RIDE IHF6 LI.ME CA 06/11", -2.76, "DEBIT_CARD", 456.17],
    ["DEBIT", 45831, "LIME*RIDE IHF6 LI.ME CA 06/22", -9.07, "DEBIT_CARD", 1482.67],
    ["DEBIT", 45831, "LIME*RIDE IHF6 LI.ME CA 06/22", -9.07, "DEBIT_CARD", 1491.74],
    ["DEBIT", 45835, "LIME*RIDE IHF6 LI.ME CA 06/27", -14.54, "DEBIT_CARD", 337.43],
    ["DEBIT", 45835, "LIME*RIDE IHF6 LI.ME CA 06/27", -14.12, "DEBIT_CARD", 351.97],
    ["DEBIT", 45828, "MB SMOKE ON MILWAUKEE WI 06/18", -22.37, "DEBIT_CARD", 475.52],
    ["DEBIT", 45831, "Nintendo CA1420711209 800-2553700 WA 06/21", -31.49, "DEBIT_CARD", 1552.5],
    ["DEBIT", 45817, "NON-CHASE ATM FEE-WITH", -3, "FEE_TRANSACTION", 413.27],
    ["DEBIT", 45817, "NON-CHASE ATM WITHDRAW 005820 06/082950 N OA", -83.5, "ATM", 561.33],
    ["CREDIT", 45810, "ODP TRANSFER FROM SAVINGS ...7036", 312.71, "MISC_CREDIT", 452.2],
    ["DEBIT", 45838, "OLD NAVY US 4518 MILWAUKEE WI 657546 06/29", -46.57, "DEBIT_CARD", 233.98],
    ["CREDIT", 45817, "Online Transfer from CHK ...4991 transaction#: 24864779945", 350, "ACCT_XFER", 521],
    ["CREDIT", 45810, "Online Transfer from CHK ...4991 transaction#: 24983957451", 100, "ACCT_XFER", 552.2],
    ["CREDIT", 45811, "Online Transfer from CHK ...4991 transaction#: 24997652343", 300, "ACCT_XFER", 300],
    ["CREDIT", 45811, "Online Transfer from CHK ...4991 transaction#: 24998944360", 200, "ACCT_XFER", 500],
    ["CREDIT", 45813, "Online Transfer from CHK ...4991 transaction#: 25018168956", 100, "ACCT_XFER", 247.09],
    ["CREDIT", 45814, "Online Transfer from CHK ...4991 transaction#: 25038102461", 100, "ACCT_XFER", 244.29],
    ["CREDIT", 45817, "Online Transfer from CHK ...4991 transaction#: 25058860082", 100, "ACCT_XFER", 621],
    ["CREDIT", 45817, "Online Transfer from CHK ...4991 transaction#: 25059389690", 100, "ACCT_XFER", 721],
    ["CREDIT", 45831, "Online Transfer from CHK ...4991 transaction#: 25066965786", 350, "ACCT_XFER", 1211.03],
    ["CREDIT", 45819, "Online Transfer from CHK ...4991 transaction#: 25091715290", 200, "ACCT_XFER", 458.93],
    ["CREDIT", 45821, "Online Transfer from CHK ...4991 transaction#: 25116240381", 100, "ACCT_XFER", 212.51],
    ["CREDIT", 45821, "Online Transfer from CHK ...4991 transaction#: 25118775938", 100, "ACCT_XFER", 312.51],
    ["CREDIT", 45824, "Online Transfer from CHK ...4991 transaction#: 25134253375", 300, "ACCT_XFER", 569.11],
    ["CREDIT", 45824, "Online Transfer from CHK ...4991 transaction#: 25137260105", 200, "ACCT_XFER", 769.11],
    ["CREDIT", 45825, "Online Transfer from CHK ...4991 transaction#: 25162630164", 50, "ACCT_XFER", 184.52],
    ["CREDIT", 45826, "Online Transfer from CHK ...4991 transaction#: 25171868585", 100, "ACCT_XFER", 223.13],
    ["CREDIT", 45826, "Online Transfer from CHK ...4991 transaction#: 25176301526", 100, "ACCT_XFER", 323.13],
    ["CREDIT", 45828, "Online Transfer from CHK ...4991 transaction#: 25198212221", 300, "ACCT_XFER", 497.89],
    ["CREDIT", 45831, "Online Transfer from CHK ...4991 transaction#: 25230548055", 600, "ACCT_XFER", 861.03],
    ["CREDIT", 45832, "Online Transfer from CHK ...4991 transaction#: 25245750219", 160, "ACCT_XFER", 272.25],
    ["CREDIT", 45833, "Online Transfer from CHK ...4991 transaction#: 25250838090", 200, "ACCT_XFER", 424.25],
    ["CREDIT", 45833, "Online Transfer from CHK ...4991 transaction#: 25251746150", 200, "ACCT_XFER", 624.25],
    ["CREDIT", 45835, "Online Transfer from CHK ...4991 transaction#: 25276252991", 300, "ACCT_XFER", 366.09],
    ["CREDIT", 45838, "Online Transfer from CHK ...4991 transaction#: 25297995141", 100, "ACCT_XFER", 621.43],
    ["CREDIT", 45838, "Online Transfer from CHK ...4991 transaction#: 25314096811", 200, "ACCT_XFER", 521.43],
    ["CREDIT", 45831, "Online Transfer from SAV ...7036 transaction#: 25230536861", 300, "ACCT_XFER", 1511.03],
    ["CREDIT", 45831, "Online Transfer from SAV ...7036 transaction#: 25230539758", 100, "ACCT_XFER", 1611.03],
    ["DEBIT", 45810, "Online Transfer to CHK ...4991 transaction#: 24987735122 06/02", -200, "ACCT_XFER", 243.02],
    ["DEBIT", 45810, "Online Transfer to SAV ...7036 transaction#: 24864880323", -25, "ACCT_XFER", 480.36],
    ["DEBIT", 45812, "Online Transfer to SAV ...7036 transaction#: 24915598088", -80, "ACCT_XFER", 147.09],
    ["DEBIT", 45813, "Online Transfer to SAV ...7036 transaction#: 24927847408", -35, "ACCT_XFER", 150.98],
    ["DEBIT", 45817, "Online Transfer to SAV ...7036 transaction#: 24982474301", -25, "ACCT_XFER", 416.27],
    ["DEBIT", 45819, "Online Transfer to SAV ...7036 transaction#: 25007409514", -80, "ACCT_XFER", 353.51],
    ["DEBIT", 45820, "Online Transfer to SAV ...7036 transaction#: 25019474014", -35, "ACCT_XFER", 112.51],
    ["DEBIT", 45824, "Online Transfer to SAV ...7036 transaction#: 25066798727", -25, "ACCT_XFER", 151.15],
    ["DEBIT", 45826, "Online Transfer to SAV ...7036 transaction#: 25100049596", -35, "ACCT_XFER", 235.31],
    ["DEBIT", 45831, "Online Transfer to SAV ...7036 transaction#: 25148073808", -25, "ACCT_XFER", 1223.67],
    ["DEBIT", 45834, "Online Transfer to SAV ...7036 transaction#: 25170689530", -35, "ACCT_XFER", 83.86],
    ["DEBIT", 45833, "Online Transfer to SAV ...7036 transaction#: 25170771916", -80, "ACCT_XFER", 528.25],
    ["DEBIT", 45838, "Online Transfer to SAV ...7036 transaction#: 25226410448", -25, "ACCT_XFER", 194.46],
    ["DEBIT", 45811, "PICK N SAVE #882 1100 MILWAUKEE WI 038996 06/03", -31.86, "DEBIT_CARD", 396.14],
    ["DEBIT", 45810, "PICK N SAVE #882 1100 MILWAUKEE WI 362185 06/02", -5.79, "DEBIT_CARD", 0],
    ["DEBIT", 45824, "PICK N SAVE #882 1100 MILWAUKEE WI 513622 06/15", -27.12, "DEBIT_CARD", 176.15],
    ["DEBIT", 45831, "PICK N SAVE #882 1100 MILWAUKEE WI 838165 06/23", -11.42, "DEBIT_CARD", 112.25],
    ["DEBIT", 45838, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 462.12],
    ["DEBIT", 45835, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 321.43],
    ["DEBIT", 45834, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 128.44],
    ["DEBIT", 45833, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 608.25],
    ["DEBIT", 45832, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 224.25],
    ["DEBIT", 45832, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 240.25],
    ["DEBIT", 45832, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 256.25],
    ["DEBIT", 45831, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 1520.5],
    ["DEBIT", 45831, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 1536.5],
    ["DEBIT", 45828, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 346.67],
    ["DEBIT", 45826, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 270.31],
    ["DEBIT", 45825, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 123.13],
    ["DEBIT", 45825, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 139.13],
    ["DEBIT", 45825, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 155.13],
    ["DEBIT", 45824, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 414.09],
    ["DEBIT", 45821, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 285.62],
    ["DEBIT", 45820, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 147.51],
    ["DEBIT", 45819, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 440.17],
    ["DEBIT", 45818, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 258.93],
    ["DEBIT", 45818, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 274.93],
    ["DEBIT", 45818, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 290.93],
    ["DEBIT", 45817, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 656.77],
    ["DEBIT", 45814, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 216.58],
    ["DEBIT", 45813, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 185.98],
    ["DEBIT", 45812, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -16, "MISC_DEBIT", 227.09],
    ["DEBIT", 45811, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -24, "MISC_DEBIT", 428],
    ["DEBIT", 45811, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -24, "MISC_DEBIT", 452],
    ["DEBIT", 45811, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -24, "MISC_DEBIT", 476],
    ["DEBIT", 45810, "ROBINHOOD DEBITS 912028016 WEB ID: 5326394001", -24, "MISC_DEBIT", 510.92],
    ["DEBIT", 45824, "SENDIKS ON DOWNER LLC MILWAUKEE WI 226412 06/16", -7.54, "DEBIT_CARD", 143.61],
    ["DEBIT", 45810, "SKYWAY CONCESSIONS CHICAGO IL 05/30", -7.8, "DEBIT_CARD", 541.22],
    ["DEBIT", 45831, "SOLSTICE WWW.SOLSTICEB FL 06/20", -16.26, "DEBIT_CARD", 1583.99],
    ["DEBIT", 45812, "SP SPARROW HILL FARM SPARROWHILLFA WI 06/03", -37.62, "DEBIT_CARD", 358.52],
    ["DEBIT", 45838, "SQ *COLECTIVO Milwaukee WI 06/27", -23.97, "DEBIT_CARD", 489.41],
    ["DEBIT", 45813, "SQ *ROCHAMBO COFFEE AND Milwaukee WI 06/04", -8.05, "DEBIT_CARD", 201.98],
    ["DEBIT", 45813, "SQ *ROCHAMBO COFFEE AND Milwaukee WI 06/05", -6.69, "DEBIT_CARD", 144.29],
    ["DEBIT", 45838, "SQ *SALON MAYFAIR THREA Wauwatosa WI 06/29", -36.8, "DEBIT_CARD", 349.41],
    ["DEBIT", 45824, "SQ *STAR SEED WELLNESS Milwaukee WI 06/13", -90, "DEBIT_CARD", 589.35],
    ["DEBIT", 45821, "SQ *STONE CREEK COFFEE Milwaukee WI 06/13", -16.51, "DEBIT_CARD", 269.11],
    ["DEBIT", 45834, "SQ *STONE CREEK COFFEE Milwaukee WI 06/26", -17.77, "DEBIT_CARD", 66.09],
    ["DEBIT", 45838, "SQ *STONE CREEK COFFEE Milwaukee WI 06/30", -9.13, "DEBIT_CARD", 185.33],
    ["DEBIT", 45831, "Subscription Acorns 6G9Z38 WEB ID: 9000142694", -3, "MISC_DEBIT", 1517.5],
    ["DEBIT", 45817, "TARGET STORE T-2877 GLENDALE WI 028010 06/08", -95.25, "DEBIT_CARD", 466.08],
    ["DEBIT", 45833, "TARGET STORE T-2877 GLENDALE WI 062324 06/25", -67.83, "DEBIT_CARD", 366.02],
    ["DEBIT", 45820, "THE DINNER DETECTIVE 866-496-0535 CO 06/11", -190, "DEBIT_CARD", 163.51],
    ["DEBIT", 45817, "THE GLASSHOUSE MILWAUKEE WI 06/05", -21.57, "DEBIT_CARD", 676.79],
    ["DEBIT", 45833, "TRADER JOE S #71 TRADE MILWAUKEE WI 333568 06/25", -94.4, "DEBIT_CARD", 433.85],
    ["DEBIT", 45831, "TRINITY THREE IRISH PUB MILWAUKEE WI 06/22", -16.69, "DEBIT_CARD", 1500.81],
    ["DEBIT", 45826, "TROPICAL SMOOTHIE CAFE GLENDALE WI 06/17", -18.7, "DEBIT_CARD", 304.43],
    ["DEBIT", 45838, "TROPICAL SMOOTHIE CAFE GLENDALE WI 06/28", -19.55, "DEBIT_CARD", 442.57],
    ["DEBIT", 45838, "TST*BRUNCH CEDARBURG Cedarburg WI 06/29", -68.86, "DEBIT_CARD", 280.55],
    ["DEBIT", 45838, "TST*PETES PUB ON BRAD 765-228-6461 WI 06/29", -56.36, "DEBIT_CARD", 386.21],
    ["DEBIT", 45828, "WE ENERGIES PAYMENT 074707564400001 WEB ID: 13904762WE", -112.85, "ACH_DEBIT", 362.67],
    ["DEBIT", 45810, "WHOLEFDS MLW 101 2305 MILWAUKEE WI 030362 06/02", -237.23, "DEBIT_CARD", 5.79],
    ["DEBIT", 45814, "WHOLEFDS MLW 101 2305 MILWAUKEE WI 063280 06/06", -45.58, "DEBIT_CARD", 171],
    ["DEBIT", 45833, "WHOLEFDS MLW 101 2305 MILWAUKEE WI 438437 06/25", -172.12, "DEBIT_CARD", 193.9],
    ["DEBIT", 45828, "WHOLEFDS MLW 101 2305 MILWAUKEE WI 538303 06/20", -53.28, "DEBIT_CARD", 261.03],
    ["DEBIT", 45831, "Zelle payment to Patrick Landlord JPM99bd72yyd", -1100, "CHASE_TO_PARTNERFI", 123.67],
]

SAPPHIRE_RAW = [
    [45831, 45831, "PURCHASE INTEREST CHARGE", "Fees & Adjustments", "Fee", -148.05],
    [45828, 45828, "AUTOMATIC PAYMENT - THANK", "", "Payment", 218],
    [45824, 45825, "ELITE NORTH SHORE LLC", "Health & Wellness", "Sale", -191.36],
]


def process_biz_4991():
    """Process and return cleaned Business 4991 transactions."""
    rows = []
    for raw in BIZ_4991_RAW:
        date_serial = raw[1]
        desc = raw[2]
        amount = raw[3]
        balance = raw[5]
        vendor, category, notes = categorize_biz_4991(desc, amount)
        rows.append([date_serial, vendor, category, amount, balance, notes])
    # Sort by date
    rows.sort(key=lambda r: r[0])
    return rows


def process_biz_cc():
    """Process and return cleaned Biz CC 0678 transactions."""
    rows = []
    for raw in BIZ_CC_RAW:
        date_serial = raw[1]  # Transaction Date
        desc = raw[3]
        amount = raw[6]
        vendor, category, notes = categorize_biz_cc(desc, amount)
        rows.append([date_serial, vendor, category, amount, '', notes])
    rows.sort(key=lambda r: r[0])
    return rows


def process_personal_0068():
    """Process and return cleaned Personal 0068 transactions."""
    rows = []
    for raw in PERSONAL_0068_RAW:
        date_serial = raw[1]
        desc = raw[2]
        amount = raw[3]
        balance = raw[5]
        vendor, category, notes = categorize_personal_0068(desc, amount)
        rows.append([date_serial, vendor, category, amount, balance, notes])
    rows.sort(key=lambda r: r[0])
    return rows


def process_sapphire():
    """Process and return cleaned Sapphire 4252 transactions."""
    rows = []
    for raw in SAPPHIRE_RAW:
        date_serial = raw[0]
        desc = raw[2]
        amount = raw[5]
        vendor, category, notes = categorize_sapphire(desc, amount)
        rows.append([date_serial, vendor, category, amount, '', notes])
    rows.sort(key=lambda r: r[0])
    return rows


def phase2_write_transactions():
    print("=== PHASE 2: Write Cleaned Transactions ===")
    
    header = ['Date', 'Vendor', 'Category', 'Amount', 'Balance', 'Notes']
    
    biz_4991 = process_biz_4991()
    biz_cc = process_biz_cc()
    personal = process_personal_0068()
    sapphire = process_sapphire()
    
    value_data = [
        {
            'range': "'💼 Business 4991'!A1",
            'values': [header] + biz_4991
        },
        {
            'range': "'💳 Biz CC 0678'!A1",
            'values': [header] + biz_cc
        },
        {
            'range': "'👤 Personal 0068'!A1",
            'values': [header] + personal
        },
        {
            'range': "'💎 Sapphire 4252'!A1",
            'values': [header] + sapphire
        },
    ]
    
    batch_values(value_data)
    print(f"  💼 Business 4991: {len(biz_4991)} rows")
    print(f"  💳 Biz CC 0678: {len(biz_cc)} rows")
    print(f"  👤 Personal 0068: {len(personal)} rows")
    print(f"  💎 Sapphire 4252: {len(sapphire)} rows")
    
    return biz_4991, biz_cc, personal, sapphire


# ============================================================
# PHASE 3: Build and write Dashboard
# ============================================================

def build_dashboard(biz_4991, biz_cc, personal, sapphire):
    """Build the dashboard data matching Jan 2026 format."""
    
    # Compute summaries from cleaned data
    # Income from Business 4991
    stripe_income = []
    zelle_income = []
    for row in biz_4991:
        if 'Income (Stripe)' in str(row[2]):
            stripe_income.append(row)
        elif 'Income (Zelle)' in str(row[2]):
            zelle_income.append(row)
    
    stripe_total = sum(r[3] for r in stripe_income)
    zelle_total = sum(r[3] for r in zelle_income)
    total_income = stripe_total + zelle_total
    
    # Business Expenses from 4991 (non-transfer, non-income, non-CC-payment)
    biz_expenses_4991 = {}
    for row in biz_4991:
        cat = str(row[2])
        if 'Income' in cat or '→' in cat or 'Biz' in cat or 'Personal' in cat or 'Savings' in cat or 'Tax' in cat or 'CC Payment' in cat:
            continue
        # Group by high-level category
        if '📱 SaaS' in cat:
            key = '📱 SaaS & Tools'
        elif '📣 Marketing' in cat:
            key = '📣 Marketing'
        elif '🏢 Operations' in cat:
            key = '🏢 Operations'
        elif '💳 Debt' in cat:
            key = '💳 Debt Payments'
        elif '🏦' in cat:
            continue  # Tax transfer handled elsewhere
        else:
            key = '❓ Other'
        
        if key not in biz_expenses_4991:
            biz_expenses_4991[key] = []
        biz_expenses_4991[key].append(row)
    
    # CC expenses
    cc_expenses = {}
    for row in biz_cc:
        cat = str(row[2])
        if 'CC Payment' in cat:
            continue
        if '📱 SaaS' in cat:
            key = '📱 SaaS & Tools'
        elif '📣 Marketing' in cat:
            key = '📣 Marketing'
        elif '🏢 Operations' in cat:
            key = '🏢 Operations'
        else:
            key = '❓ Other'
        if key not in cc_expenses:
            cc_expenses[key] = []
        cc_expenses[key].append(row)
    
    # Merge biz expenses
    all_biz_expenses = {}
    for key in set(list(biz_expenses_4991.keys()) + list(cc_expenses.keys())):
        all_biz_expenses[key] = biz_expenses_4991.get(key, []) + cc_expenses.get(key, [])
    
    # Personal expenses  
    personal_expenses = {}
    personal_transfers = []
    for row in personal:
        cat = str(row[2])
        if '→' in cat or 'Biz' in cat or 'Personal' in cat or 'Savings' in cat:
            personal_transfers.append(row)
            continue
        
        if '📈 Investment' in cat:
            key = '📈 Investments'
        elif '🛒 Groceries' in cat:
            key = '🛒 Groceries'
        elif '🛒 Shopping' in cat:
            key = '🛒 Shopping'
        elif '🍔 Food' in cat or '☕ Food' in cat:
            key = '🍔 Food & Dining'
        elif '🏠 Housing' in cat:
            key = '🏠 Housing'
        elif '🚗 Transportation' in cat:
            key = '🚗 Transportation'
        elif '💳' in cat:
            key = '💳 CC/Debt Payments'
        elif '🏧' in cat:
            key = '🏧 ATM / Cash'
        elif '📺' in cat or '🏥' in cat:
            key = '📺 Subscriptions & Insurance'
        elif '🎮' in cat:
            key = '🎮 Entertainment'
        elif '💝' in cat or '💆' in cat or '💇' in cat:
            key = '💝 Personal / Wellness'
        else:
            key = '❓ Other Personal'
        
        if key not in personal_expenses:
            personal_expenses[key] = []
        personal_expenses[key].append(row)
    
    # Money flow
    biz_to_personal = [r for r in biz_4991 if 'Biz → Personal' in str(r[2])]
    personal_to_biz = [r for r in biz_4991 if 'Personal → Biz' in str(r[2])]
    tax_transfers = [r for r in biz_4991 if 'Tax Transfer' in str(r[2])]
    cc_payments_4991 = [r for r in biz_4991 if 'CC Payment' in str(r[2])]
    
    # Savings flows from personal
    personal_to_savings = [r for r in personal if 'Personal → Savings' in str(r[2])]
    savings_to_personal = [r for r in personal if 'Savings → Personal' in str(r[2])]
    
    # Build dashboard rows
    rows = []
    
    # Title
    rows.append(['June 2025 — KuriosBrand Financial Overview'])
    rows.append([])
    
    # Section A: Income
    rows.append(['💰 SECTION A: INCOME SUMMARY'])
    rows.append(['Source', 'Vendor / Client', 'Date', 'Amount'])
    
    for r in stripe_income:
        rows.append(['Stripe', 'Stripe', serial_to_date(r[0]), r[3]])
    rows.append(['', '', 'Stripe Subtotal', stripe_total])
    
    for r in zelle_income:
        rows.append(['Zelle', r[1], serial_to_date(r[0]), r[3]])
    rows.append(['', '', 'Zelle Subtotal', zelle_total])
    
    rows.append(['', '', 'TOTAL BUSINESS INCOME', total_income])
    rows.append([])
    
    # Section B: Business Expenses
    rows.append(['📊 SECTION B: BUSINESS EXPENSES'])
    rows.append(['Category', 'Vendor', 'Count', 'Total'])
    
    total_biz_exp = 0
    category_order = ['📱 SaaS & Tools', '📣 Marketing', '🏢 Operations', '💳 Debt Payments', '❓ Other']
    
    for cat_key in category_order:
        if cat_key not in all_biz_expenses:
            continue
        items = all_biz_expenses[cat_key]
        rows.append([cat_key])
        
        # Group by vendor within category
        vendor_totals = {}
        for item in items:
            v = item[1]
            if v not in vendor_totals:
                vendor_totals[v] = {'count': 0, 'total': 0}
            vendor_totals[v]['count'] += 1
            vendor_totals[v]['total'] += item[3]
        
        # Sort by absolute total
        sorted_vendors = sorted(vendor_totals.items(), key=lambda x: x[1]['total'])
        cat_total = 0
        for vendor, data in sorted_vendors:
            rows.append(['', vendor, data['count'], data['total']])
            cat_total += data['total']
        
        rows.append(['', '', f'{cat_key} Subtotal', cat_total])
        total_biz_exp += cat_total
    
    rows.append(['', '', 'TOTAL BUSINESS EXPENSES', total_biz_exp])
    rows.append([])
    
    # Section C: Personal Expenses
    rows.append(['👤 SECTION C: PERSONAL EXPENSES'])
    rows.append(['Category', 'Detail', 'Count', 'Total'])
    
    total_personal_exp = 0
    personal_order = ['🏠 Housing', '🛒 Groceries', '🍔 Food & Dining', '📈 Investments', 
                      '🚗 Transportation', '🛒 Shopping', '💳 CC/Debt Payments',
                      '🏧 ATM / Cash', '📺 Subscriptions & Insurance', '🎮 Entertainment', 
                      '💝 Personal / Wellness', '❓ Other Personal']
    
    for cat_key in personal_order:
        if cat_key not in personal_expenses:
            continue
        items = personal_expenses[cat_key]
        rows.append([cat_key])
        
        vendor_totals = {}
        for item in items:
            v = item[1]
            if v not in vendor_totals:
                vendor_totals[v] = {'count': 0, 'total': 0}
            vendor_totals[v]['count'] += 1
            vendor_totals[v]['total'] += item[3]
        
        sorted_vendors = sorted(vendor_totals.items(), key=lambda x: x[1]['total'])
        cat_total = 0
        for vendor, data in sorted_vendors:
            rows.append(['', vendor, data['count'], data['total']])
            cat_total += data['total']
        
        rows.append(['', '', f'{cat_key} Subtotal', cat_total])
        total_personal_exp += cat_total
    
    # Sapphire expenses
    sap_total = 0
    rows.append(['💎 Sapphire 4252'])
    for r in sapphire:
        rows.append(['', r[1], '', r[3]])
        sap_total += r[3]
    rows.append(['', '', 'Sapphire Subtotal', sap_total])
    total_personal_exp += sap_total
    
    rows.append(['', '', 'TOTAL PERSONAL EXPENSES', total_personal_exp])
    rows.append([])
    
    # Section D: Key Metrics
    profit = total_income + total_biz_exp  # biz_exp is negative
    margin = profit / total_income * 100 if total_income else 0
    
    rows.append(['📈 SECTION D: KEY METRICS'])
    rows.append(['Metric', '', '', 'Value'])
    rows.append(['Business Income', '', '', total_income])
    rows.append(['Business Expenses', '', '', total_biz_exp])
    rows.append(['Business Profit (before personal)', '', '', profit])
    rows.append(['Profit Margin', '', '', f'{margin:.1f}%'])
    rows.append([])
    
    # Calculate specific metrics
    saas_total = sum(r[3] for r in all_biz_expenses.get('📱 SaaS & Tools', []))
    marketing_total = sum(r[3] for r in all_biz_expenses.get('📣 Marketing', []))
    
    rows.append(['Total SaaS/Tools', '', '', saas_total])
    rows.append(['Total Marketing/Ads', '', '', marketing_total])
    
    # Investment totals from personal
    inv_items = personal_expenses.get('📈 Investments', [])
    inv_total = sum(r[3] for r in inv_items)
    rows.append(['Total Investments (Robinhood + Acorns)', '', '', inv_total])
    
    rows.append(['Daily Burn Rate (Biz Expenses / 30)', '', '', total_biz_exp / 30])
    rows.append([])
    
    # Section E: Money Flow
    biz_to_personal_total = sum(abs(r[3]) for r in biz_to_personal)
    personal_to_biz_total = sum(abs(r[3]) for r in personal_to_biz)
    tax_total = sum(abs(r[3]) for r in tax_transfers)
    cc_payment_total = sum(abs(r[3]) for r in cc_payments_4991)
    savings_out = sum(abs(r[3]) for r in personal_to_savings)
    savings_in = sum(r[3] for r in savings_to_personal)
    
    rows.append(['🔄 SECTION E: MONEY FLOW'])
    rows.append(['Flow', '', 'Count', 'Total'])
    rows.append(['Biz 4991 → Personal 0068', '', len(biz_to_personal), -biz_to_personal_total])
    rows.append(['Personal 0068 → Biz 4991', '', len(personal_to_biz), personal_to_biz_total])
    rows.append(['Net Flow (4991 → 0068)', '', '', -(biz_to_personal_total - personal_to_biz_total)])
    rows.append([])
    rows.append(['Biz 4991 → Tax Account', '', len(tax_transfers), -tax_total])
    rows.append(['Biz 4991 → CC 0678', '', len(cc_payments_4991), -cc_payment_total])
    rows.append([])
    rows.append(['Personal → Savings 7036', '', len(personal_to_savings), -savings_out])
    rows.append(['Savings 7036 → Personal', '', len(savings_to_personal), savings_in])
    rows.append([])
    
    # Section F: Debt Tracking
    rows.append(['🏦 SECTION F: DEBT TRACKING (June 2025)'])
    rows.append(['Debt', '', 'Balance', 'Monthly Payment'])
    rows.append(['Student Loans', '', 9294.92, 106.34])
    rows.append(['CC Discover Personal', '', 6295.59, 130.00])
    rows.append(['CC Chase Sapphire 4252', '', 7779.21, 218.00])
    rows.append(['CC Chase Ink Biz 0678', '', 3722.19, 300.00])
    rows.append(['TOTAL DEBT', '', 27091.91, 754.34])
    rows.append([])
    
    # Section G: Assets & Net Worth
    rows.append(['💰 SECTION G: ASSETS & NET WORTH'])
    rows.append(['Category', '', '', 'Amount'])
    rows.append(['Rank & Rent Assets', '', '', 150000])
    rows.append(['Cash', '', '', 4200])
    rows.append(['Stocks', '', '', 628])
    rows.append(['Bitcoin', '', '', 1100])
    rows.append(['Solana', '', '', 873])
    rows.append(['Dogecoin', '', '', 100])
    rows.append(['Trumpcoin', '', '', 26])
    rows.append(['Liquid Assets', '', '', 6927])
    rows.append(['Business Equity', '', '', 150000])
    rows.append(['Total Assets', '', '', 156927.46])
    rows.append(['Total Liabilities', '', '', -27091.91])
    rows.append(['NET WORTH', '', '', 129835.55])
    rows.append([])
    
    # Section H: Action Items
    rows.append(['📝 SECTION H: ACTION ITEMS'])
    rows.append(['#', 'Item', 'Status', 'Notes'])
    rows.append([1, 'Start paying off $2k/mo credit card debt', '⚠️', f'Total CC debt: $27,091.91'])
    rows.append([2, 'Cancel Midjourney, CTR Manipulation, Kevin\'s PBN', '✅', 'Marked cancelled in June'])
    rows.append([3, 'Reduce HighLevel cost ($597/mo)', '🔍', 'Largest SaaS expense'])
    rows.append([4, 'Cancel Aaron Abke subscription', '✅', 'Already cancelled'])
    rows.append([5, 'Review LocalRank.so citations spend ($1,050)', '⚠️', '12% of income on citations alone'])
    rows.append([6, 'Track Zelle income by client', '🔍', 'Multiple sources: ACI, Eddy, Jonathan, Willard'])
    rows.append([7, 'Reduce daily Robinhood investment ($496/mo)', '⚠️', 'Investing while carrying 17-22% APR CC debt'])
    
    return rows


def phase3_write_dashboard(biz_4991, biz_cc, personal, sapphire):
    print("=== PHASE 3: Write Dashboard ===")
    
    dashboard_rows = build_dashboard(biz_4991, biz_cc, personal, sapphire)
    
    batch_values([{
        'range': "'📊 Dashboard'!A1",
        'values': dashboard_rows
    }])
    
    print(f"  Dashboard: {len(dashboard_rows)} rows written")
    return len(dashboard_rows)


# ============================================================
# PHASE 4: Apply formatting
# ============================================================

def phase4_format(raw_sheet_id, dash_rows, txn_counts):
    print("=== PHASE 4: Apply Formatting ===")
    
    biz_count, cc_count, personal_count, sap_count = txn_counts
    
    requests = []
    
    # Helper to create cell format request
    def fmt(sheet_id, start_row, end_row, start_col, end_col, bg=None, fg=None, bold=False, ha=None, num_fmt=None):
        cell_fmt = {}
        if bg:
            cell_fmt['backgroundColor'] = bg
        text_fmt = {}
        if fg:
            text_fmt['foregroundColor'] = fg
        if bold:
            text_fmt['bold'] = True
        if text_fmt:
            cell_fmt['textFormat'] = text_fmt
        if ha:
            cell_fmt['horizontalAlignment'] = ha
        if num_fmt:
            cell_fmt['numberFormat'] = num_fmt
        
        fields = []
        if bg: fields.append('userEnteredFormat.backgroundColor')
        if fg or bold: fields.append('userEnteredFormat.textFormat')
        if ha: fields.append('userEnteredFormat.horizontalAlignment')
        if num_fmt: fields.append('userEnteredFormat.numberFormat')
        
        return {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
                    'startRowIndex': start_row,
                    'endRowIndex': end_row,
                    'startColumnIndex': start_col,
                    'endColumnIndex': end_col,
                },
                'cell': {'userEnteredFormat