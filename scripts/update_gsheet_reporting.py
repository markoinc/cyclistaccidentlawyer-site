#!/usr/bin/env python3
"""Add reporting requirements to Kurios Performance Stats sheet"""
import json
import os
import requests

TOKEN_PATH = os.path.expanduser("~/.config/gcal-pro/token.json")
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
    
    if refresh_resp.status_code == 200:
        return refresh_resp.json()["access_token"]
    return token_data["token"]

def add_reporting_requirements():
    token = get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Add a new sheet for Guarantee Requirements
    add_sheet_resp = requests.post(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}:batchUpdate",
        headers=headers,
        json={
            "requests": [{
                "addSheet": {
                    "properties": {
                        "title": "Guarantee Requirements",
                        "index": 1
                    }
                }
            }]
        }
    )
    
    # Reporting requirements data
    reporting_data = [
        ["🔒 GUARANTEE QUALIFICATION REQUIREMENTS"],
        [""],
        ["To qualify for guarantee fulfillment, clients MUST adhere to ALL of the following:"],
        [""],
        ["📊 LEAD REPORTING (Required within 24 hours of lead delivery)"],
        ["Requirement", "Details", "Deadline"],
        ["Lead Status Update", "Mark each lead as: Contacted / No Answer / Bad Number / Not Interested / Qualified / Signed", "Within 24 hours"],
        ["Contact Attempts", "Minimum 5 contact attempts before marking as 'No Answer'", "Within 48 hours"],
        ["Call Recording/Notes", "Provide call notes or recording for disputed leads", "Upon request"],
        [""],
        ["📞 LIVE TRANSFER REPORTING (Required same day)"],
        ["Requirement", "Details", "Deadline"],
        ["Transfer Outcome", "Mark as: Signed / Not Qualified / No Show / Call Dropped / Other", "Same day"],
        ["Reason for Rejection", "If not signed, provide specific reason (not enough damages, liability issue, SOL, etc.)", "Same day"],
        ["Duration Tracking", "Confirm call lasted minimum 2 minutes for valid transfer", "Same day"],
        [""],
        ["📁 CASE REPORTING (Required within 72 hours)"],
        ["Requirement", "Details", "Deadline"],
        ["Retainer Status", "Confirm signed retainer received", "Within 72 hours"],
        ["Case Value Estimate", "Provide estimated case value range", "Within 7 days"],
        ["Case Type Classification", "Categorize: Auto/Truck/Motorcycle/Pedestrian/Other", "Within 72 hours"],
        [""],
        ["⚠️ DISQUALIFYING ACTIONS (Voids Guarantee)"],
        ["Action", "Consequence"],
        ["Failure to update lead status within 24 hours", "Lead excluded from guarantee calculation"],
        ["Less than 5 contact attempts on 'No Answer' leads", "Lead excluded from guarantee calculation"],
        ["No call notes/recording when disputed", "Dispute resolved in Kurios favor"],
        ["Failure to report transfer outcome same day", "Transfer excluded from guarantee"],
        ["Retainer not confirmed within 72 hours", "Case excluded from guarantee"],
        ["Sharing leads with other firms", "Immediate contract termination, no refunds"],
        ["Reselling or redistributing leads", "Immediate contract termination, legal action"],
        [""],
        ["✅ GUARANTEE TIERS"],
        ["Product", "Guarantee", "Conditions"],
        ["Leads", "Replacement or credit for bad leads", "Must follow all lead reporting requirements"],
        ["Live Transfers", "Replacement for no-shows or drops", "Must confirm within same day"],
        ["Cases", "Performance guarantee based on agreed cost-per-case", "Must follow all reporting, 90-day evaluation period"],
        [""],
        ["📅 REPORTING SCHEDULE"],
        ["Report Type", "Frequency", "Due"],
        ["Lead Status Updates", "Daily", "End of business day"],
        ["Weekly Performance Summary", "Weekly", "Monday by 12pm"],
        ["Monthly Reconciliation", "Monthly", "5th of following month"],
        [""],
        ["🚨 NON-COMPLIANCE ESCALATION"],
        ["Strike", "Action"],
        ["1st Offense", "Written warning, 24-hour grace period to update"],
        ["2nd Offense", "Affected leads/transfers excluded from guarantee"],
        ["3rd Offense", "Guarantee suspended for 30 days"],
        ["4th Offense", "Guarantee permanently revoked, contract review"],
        [""],
        ["By accepting leads/transfers/cases, client agrees to all reporting requirements above."],
    ]
    
    # Update the new sheet with data
    update_resp = requests.put(
        f"https://sheets.googleapis.com/v4/spreadsheets/{SPREADSHEET_ID}/values/'Guarantee Requirements'!A1?valueInputOption=RAW",
        headers=headers,
        json={"values": reporting_data}
    )
    
    if update_resp.status_code == 200:
        print("✅ Added Guarantee Requirements sheet!")
        print(f"📊 https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=1")
    else:
        print(f"Failed: {update_resp.text}")

if __name__ == "__main__":
    add_reporting_requirements()
