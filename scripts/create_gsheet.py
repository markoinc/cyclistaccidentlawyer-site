#!/usr/bin/env python3
"""Create a Google Sheet with Kurios Performance Stats"""
import json
import os
import requests

TOKEN_PATH = os.path.expanduser("~/.config/gcal-pro/token.json")
KURIOS_FOLDER_ID = "1igaRyFYqMF0rAKR3rVcRWa747j9hroUQ"

def get_access_token():
    with open(TOKEN_PATH) as f:
        token_data = json.load(f)
    
    refresh_resp = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": token_data["client_id"],
        "client_secret": token_data["client_secret"],
        "refresh_token": token_data["refresh_token"],
        "grant_type": "refresh_token"
    })
    
    if refresh_resp.status_code == 200:
        new_token = refresh_resp.json()["access_token"]
        token_data["token"] = new_token
        with open(TOKEN_PATH, "w") as f:
            json.dump(token_data, f, indent=2)
        return new_token
    return token_data["token"]

def create_sheet():
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Create spreadsheet
    create_resp = requests.post(
        "https://sheets.googleapis.com/v4/spreadsheets",
        headers=headers,
        json={
            "properties": {"title": "Kurios Performance Stats & Pricing"},
            "sheets": [{"properties": {"title": "Pricing by State"}}]
        }
    )
    
    if create_resp.status_code != 200:
        print(f"Failed to create sheet: {create_resp.text}")
        return None
    
    sheet_data = create_resp.json()
    spreadsheet_id = sheet_data["spreadsheetId"]
    print(f"Created spreadsheet: {spreadsheet_id}")
    
    # Data rows - all values, no formulas
    data = [
        ["State", "# Clients", "COD Lead Cost", "Our Lead Cost (-10%)", "Sell Lead (+40% w/guarantee)", "Our Transfer Cost (Lead×5+$100)", "Sell Transfer (+40%)", "Our Case Cost (Transfer×2+$350)", "Sell Case (+40%)", "Client Stories & Results"],
        ["California CA", "4+", "$250-$350", "$225-$315", "$315-$441", "$1,225-$1,675", "$1,715-$2,345", "$2,800-$3,700", "$3,920-$5,180", "Client since 1st year. Over $4M spent. $250k/month spend. 40+ cases. 6-10% conversion. $3000-4000 avg case cost."],
        ["Texas TX", "3", "$250-$300", "$225-$270", "$315-$378", "$1,225-$1,450", "$1,715-$2,030", "$2,800-$3,250", "$3,920-$4,550", "$2,000 avg case cost. 4+ year client. 20+ cases. ~15% conversion. 600+ cases through case signing company."],
        ["Louisiana LA", "2", "$250-$300", "$225-$270", "$315-$378", "$1,225-$1,450", "$1,715-$2,030", "$2,800-$3,250", "$3,920-$4,550", "Since March 2021. <$2k cost/case. Signs 40+ cases/month. 30+ cases total."],
        ["Florida FL", "1", "$250-$300", "$225-$270", "$315-$378", "$1,225-$1,450", "$1,715-$2,030", "$2,800-$3,250", "$3,920-$4,550", "$2k avg CPC. $1200 avg case cost. Since early 2020. 60+ cases. 5% conversion."],
        ["WA/OR/UT/ID", "2", "$250-$300", "$225-$270", "$315-$378", "$1,225-$1,450", "$1,715-$2,030", "$2,800-$3,250", "$3,920-$4,550", "$2500 avg CPC. Since 2020. Over $1.5M spend. 10-15% conversion."],
        ["New Mexico NM", "2", "$200", "$180", "$252", "$1,000", "$1,400", "$2,350", "$3,290", "$2k avg case cost. 10% conversion. Since June 2020. LOTS OF TRUCKING CASES - 4x more likely fatality = HIGH VALUE."],
        ["GA/VA/OH/SC", "4", "$200-$350", "$180-$315", "$252-$441", "$1,000-$1,850", "$1,400-$2,590", "$2,350-$4,050", "$3,290-$5,670", "Favorite client (Maria's bday 3/2021). $1500 or less CPC. 100+ cases signed. 15-25% conversion. $1M+ spend."],
        ["Pennsylvania PA", "2", "$200", "$180", "$252", "$1,000", "$1,400", "$2,350", "$3,290", "$1500 w/aggressive intake. Since 2023. 15-20% conversion. Philadelphia area. TIP: Not competitive - speak with confidence."],
        ["NC/GA/SC", "3", "$200", "$180", "$252", "$1,000", "$1,400", "$2,350", "$3,290", "Since May 2020. <$1500/case. 15% conversion."],
        ["New York NY", "3", "$250", "$225", "$315", "$1,225", "$1,715", "$2,800", "$3,920", "$250/lead. <$2k/case. Expanding fast, partnering w/firms. $1500-2k/case. 15% conversion."],
        ["NATIONAL Client 1", "1", "$200", "$180", "$252", "$1,000", "$1,400", "$2,350", "$3,290", "Dark firm. $1500 avg cost/case. $2k avg CPC."],
        ["NATIONAL Client 2", "1", "$200-$300", "$180-$270", "$252-$378", "$1,000-$1,600", "$1,400-$2,240", "$2,350-$3,550", "$3,290-$4,970", "NY/GA/SC/TN/TX. All 50 states. Multi 7-figure annual spend."],
        ["", "", "", "", "", "", "", "", "", ""],
        ["PRICING FORMULAS", "", "", "", "", "", "", "", "", ""],
        ["Our Lead Cost", "=", "COD Lead Cost - 10%", "", "", "", "", "", "", ""],
        ["Sell Lead", "=", "Our Lead Cost + 40%", "", "", "", "", "", "", ""],
        ["Our Transfer Cost", "=", "(Our Lead Cost × 5) + $100", "", "", "", "", "", "", ""],
        ["Sell Transfer", "=", "Our Transfer Cost + 40%", "", "", "", "", "", "", ""],
        ["Our Case Cost", "=", "(Our Transfer Cost × 2) + $350", "", "", "", "", "", "", ""],
        ["Sell Case", "=", "Our Case Cost + 40%", "", "", "", "", "", "", ""],
    ]
    
    # Update with data
    update_resp = requests.put(
        f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/A1?valueInputOption=RAW",
        headers=headers,
        json={"values": data}
    )
    
    if update_resp.status_code != 200:
        print(f"Failed to add data: {update_resp.text}")
        return None
    
    # Move to Kurios folder
    drive_headers = {"Authorization": f"Bearer {token}"}
    
    # Get current parents
    file_resp = requests.get(
        f"https://www.googleapis.com/drive/v3/files/{spreadsheet_id}?fields=parents",
        headers=drive_headers
    )
    current_parents = file_resp.json().get("parents", [])
    
    # Move to Kurios folder
    move_resp = requests.patch(
        f"https://www.googleapis.com/drive/v3/files/{spreadsheet_id}?addParents={KURIOS_FOLDER_ID}&removeParents={','.join(current_parents)}",
        headers=drive_headers
    )
    
    print(f"✅ Google Sheet created!")
    print(f"📊 https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")
    return spreadsheet_id

if __name__ == "__main__":
    create_sheet()
