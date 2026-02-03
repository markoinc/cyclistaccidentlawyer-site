#!/usr/bin/env python3
"""Add guaranteed quantities columns for $30k budget"""
import json
import requests

TOKEN_PATH = "/home/ec2-user/.config/gcal-pro/token.json"
SPREADSHEET_ID = "1Ka5HMSXoxsffYX3W-jlNURMkFiNuA7FcptM4tkx6h7c"

def get_access_token():
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    refresh_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": token_data["client_id"],
        "client_secret": token_data["client_secret"],
        "refresh_token": token_data["refresh_token"],
        "grant_type": "refresh_token"
    })
    return refresh_resp.json()["access_token"]

def calc_guaranteed(budget, price_str):
    """Calculate guaranteed quantity from price string like '$315-$441' or '$315'"""
    # Use the higher price (conservative) for guarantee
    price_str = price_str.replace("$", "").replace(",", "")
    if "-" in price_str:
        prices = price_str.split("-")
        price = float(prices[1])  # Use higher price
    else:
        price = float(price_str)
    return int(budget / price)

budget = 30000

# Updated data with guaranteed columns
data = [
    ["State", "# Clients", "COD Lead Cost", "Our Lead Cost (-10%)", "Sell Lead (+40%)", "Guaranteed Leads @$30k", "Our Transfer Cost", "Sell Transfer (+40%)", "Guaranteed Transfers @$30k", "Our Case Cost", "Sell Case (+40%)", "Guaranteed Cases @$30k", "Client Stories & Results"],
    ["California CA", "4+", "$250-$350", "$225-$315", "$315-$441", calc_guaranteed(budget, "$441"), "$1,225-$1,675", "$1,715-$2,345", calc_guaranteed(budget, "$2,345"), "$2,800-$3,700", "$3,920-$5,180", calc_guaranteed(budget, "$5,180"), "Client since 1st year. Over $4M spent. $250k/month spend. 40+ cases. 6-10% conversion. $3000-4000 avg case cost."],
    ["Texas TX", "3", "$250-$300", "$225-$270", "$315-$378", calc_guaranteed(budget, "$378"), "$1,225-$1,450", "$1,715-$2,030", calc_guaranteed(budget, "$2,030"), "$2,800-$3,250", "$3,920-$4,550", calc_guaranteed(budget, "$4,550"), "$2,000 avg case cost. 4+ year client. 20+ cases. ~15% conversion. 600+ cases through case signing company."],
    ["Louisiana LA", "2", "$250-$300", "$225-$270", "$315-$378", calc_guaranteed(budget, "$378"), "$1,225-$1,450", "$1,715-$2,030", calc_guaranteed(budget, "$2,030"), "$2,800-$3,250", "$3,920-$4,550", calc_guaranteed(budget, "$4,550"), "Since March 2021. <$2k cost/case. Signs 40+ cases/month. 30+ cases total."],
    ["Florida FL", "1", "$250-$300", "$225-$270", "$315-$378", calc_guaranteed(budget, "$378"), "$1,225-$1,450", "$1,715-$2,030", calc_guaranteed(budget, "$2,030"), "$2,800-$3,250", "$3,920-$4,550", calc_guaranteed(budget, "$4,550"), "$2k avg CPC. $1200 avg case cost. Since early 2020. 60+ cases. 5% conversion."],
    ["WA/OR/UT/ID", "2", "$250-$300", "$225-$270", "$315-$378", calc_guaranteed(budget, "$378"), "$1,225-$1,450", "$1,715-$2,030", calc_guaranteed(budget, "$2,030"), "$2,800-$3,250", "$3,920-$4,550", calc_guaranteed(budget, "$4,550"), "$2500 avg CPC. Since 2020. Over $1.5M spend. 10-15% conversion."],
    ["New Mexico NM", "2", "$200", "$180", "$252", calc_guaranteed(budget, "$252"), "$1,000", "$1,400", calc_guaranteed(budget, "$1,400"), "$2,350", "$3,290", calc_guaranteed(budget, "$3,290"), "$2k avg case cost. 10% conversion. Since June 2020. LOTS OF TRUCKING CASES - 4x more likely fatality = HIGH VALUE."],
    ["GA/VA/OH/SC", "4", "$200-$350", "$180-$315", "$252-$441", calc_guaranteed(budget, "$441"), "$1,000-$1,850", "$1,400-$2,590", calc_guaranteed(budget, "$2,590"), "$2,350-$4,050", "$3,290-$5,670", calc_guaranteed(budget, "$5,670"), "Favorite client (Maria's bday 3/2021). $1500 or less CPC. 100+ cases signed. 15-25% conversion. $1M+ spend."],
    ["Pennsylvania PA", "2", "$200", "$180", "$252", calc_guaranteed(budget, "$252"), "$1,000", "$1,400", calc_guaranteed(budget, "$1,400"), "$2,350", "$3,290", calc_guaranteed(budget, "$3,290"), "$1500 w/aggressive intake. Since 2023. 15-20% conversion. Philadelphia area. TIP: Not competitive - speak with confidence."],
    ["NC/GA/SC", "3", "$200", "$180", "$252", calc_guaranteed(budget, "$252"), "$1,000", "$1,400", calc_guaranteed(budget, "$1,400"), "$2,350", "$3,290", calc_guaranteed(budget, "$3,290"), "Since May 2020. <$1500/case. 15% conversion."],
    ["New York NY", "3", "$250", "$225", "$315", calc_guaranteed(budget, "$315"), "$1,225", "$1,715", calc_guaranteed(budget, "$1,715"), "$2,800", "$3,920", calc_guaranteed(budget, "$3,920"), "$250/lead. <$2k/case. Expanding fast, partnering w/firms. $1500-2k/case. 15% conversion."],
    ["NATIONAL Client 1", "1", "$200", "$180", "$252", calc_guaranteed(budget, "$252"), "$1,000", "$1,400", calc_guaranteed(budget, "$1,400"), "$2,350", "$3,290", calc_guaranteed(budget, "$3,290"), "Dark firm. $1500 avg cost/case. $2k avg CPC."],
    ["NATIONAL Client 2", "1", "$200-$300", "$180-$270", "$252-$378", calc_guaranteed(budget, "$378"), "$1,000-$1,600", "$1,400-$2,240", calc_guaranteed(budget, "$2,240"), "$2,350-$3,550", "$3,290-$4,970", calc_guaranteed(budget, "$4,970"), "NY/GA/SC/TN/TX. All 50 states. Multi 7-figure annual spend."],
]

token = get_access_token()
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Clear and update the first sheet
update_resp = requests.put(
    f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/'Pricing by State'!A1:M20?valueInputOption=RAW",
    headers=headers,
    json={"values": data}
)

if update_resp.status_code == 200:
    print("✅ Added guaranteed quantity columns for $30k budget!")
    print(f"📊 https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
else:
    print(f"Failed: {update_resp.status_code} - {update_resp.text}")
