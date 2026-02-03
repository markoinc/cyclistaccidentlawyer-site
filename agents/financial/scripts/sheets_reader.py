#!/usr/bin/env python3
"""
Google Sheets reader for Ledger financial agent.
Reads transaction data from Marko's monthly finance sheets.
"""

import argparse
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional
import requests

from auth import get_headers

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

SHEETS_API = "https://sheets.googleapis.com/v4/spreadsheets"


def get_sheet_id(month: str) -> str:
    """Get sheet ID for a given month (YYYY-MM format)."""
    if month in CONFIG["sheets"]:
        return CONFIG["sheets"][month]
    raise ValueError(f"No sheet ID configured for {month}. Available: {list(CONFIG['sheets'].keys())}")


def read_sheet_metadata(sheet_id: str) -> dict:
    """Get sheet metadata including tab names."""
    url = f"{SHEETS_API}/{sheet_id}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json()


def list_tabs(sheet_id: str) -> list[str]:
    """List all tabs in a sheet."""
    metadata = read_sheet_metadata(sheet_id)
    return [sheet["properties"]["title"] for sheet in metadata.get("sheets", [])]


def read_range(sheet_id: str, range_name: str) -> list[list]:
    """Read a range from a sheet."""
    url = f"{SHEETS_API}/{sheet_id}/values/{range_name}"
    response = requests.get(url, headers=get_headers())
    response.raise_for_status()
    return response.json().get("values", [])


def parse_transaction_row(row: list, headers: list, sheet_id: str, tab: str, row_num: int) -> Optional[dict]:
    """Parse a single transaction row into a structured dict."""
    if not row or len(row) < 3:
        return None
    
    # Create a dict from headers and values
    data = {}
    for i, header in enumerate(headers):
        data[header.lower().strip()] = row[i] if i < len(row) else ""
    
    # Extract standard fields
    date_str = data.get("date", data.get("transaction date", ""))
    description = data.get("description", data.get("memo", ""))
    amount_str = data.get("amount", "0")
    tx_type = data.get("type", "")
    balance_str = data.get("balance", "")
    annotation = data.get("annotation", data.get("notes", data.get("annotations", "")))
    
    if not date_str or not description:
        return None
    
    # Parse date
    try:
        for fmt in ["%m/%d/%Y", "%Y-%m-%d", "%m-%d-%Y", "%d/%m/%Y"]:
            try:
                date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue
        else:
            return None
    except Exception:
        return None
    
    # Parse amount
    try:
        amount = float(str(amount_str).replace(",", "").replace("$", "").strip() or "0")
    except ValueError:
        amount = 0.0
    
    # Parse balance
    try:
        balance = float(str(balance_str).replace(",", "").replace("$", "").strip() or "0")
    except ValueError:
        balance = None
    
    # Generate unique ID
    id_string = f"{date.isoformat()}|{description}|{amount}"
    tx_id = hashlib.md5(id_string.encode()).hexdigest()[:12]
    
    return {
        "id": tx_id,
        "date": date.strftime("%Y-%m-%d"),
        "description": description,
        "amount": amount,
        "type": tx_type.lower() if tx_type else ("debit" if amount < 0 else "credit"),
        "balance": balance,
        "annotation": annotation,
        "source": {
            "sheet_id": sheet_id,
            "tab": tab,
            "row": row_num
        }
    }


def read_transactions(month: str, tab: Optional[str] = None) -> list[dict]:
    """Read all transactions for a month."""
    sheet_id = get_sheet_id(month)
    tabs = list_tabs(sheet_id)
    
    print(f"📊 Reading sheet for {month}")
    print(f"   Found tabs: {tabs}")
    
    all_transactions = []
    
    # Determine which tabs to read
    tabs_to_read = [tab] if tab else [t for t in tabs if t.lower() != "overview"]
    
    for tab_name in tabs_to_read:
        if tab_name not in tabs:
            print(f"   ⚠ Tab '{tab_name}' not found, skipping")
            continue
        
        print(f"   Reading tab: {tab_name}")
        
        # Read the full tab
        data = read_range(sheet_id, f"'{tab_name}'!A:Z")
        
        if not data or len(data) < 2:
            print(f"   ⚠ No data in {tab_name}")
            continue
        
        headers = data[0]
        print(f"   Headers: {headers}")
        
        for i, row in enumerate(data[1:], start=2):
            tx = parse_transaction_row(row, headers, sheet_id, tab_name, i)
            if tx:
                all_transactions.append(tx)
        
        print(f"   ✓ Found {len([t for t in all_transactions if t['source']['tab'] == tab_name])} transactions")
    
    return all_transactions


def read_overview(month: str) -> dict:
    """Read the Overview tab for summary data."""
    sheet_id = get_sheet_id(month)
    tabs = list_tabs(sheet_id)
    
    # Find overview tab (case-insensitive)
    overview_tab = None
    for tab in tabs:
        if tab.lower() == "overview":
            overview_tab = tab
            break
    
    if not overview_tab:
        return {"error": "No overview tab found"}
    
    data = read_range(sheet_id, f"'{overview_tab}'!A:Z")
    
    # Parse overview data (structure varies, return raw for now)
    return {
        "tab": overview_tab,
        "data": data
    }


def save_transactions(transactions: list[dict], month: str):
    """Save transactions to a JSON file."""
    output_dir = Path(__file__).parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"transactions_{month}.json"
    
    with open(output_file, "w") as f:
        json.dump({
            "month": month,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "count": len(transactions),
            "transactions": transactions
        }, f, indent=2)
    
    print(f"\n✓ Saved {len(transactions)} transactions to {output_file}")
    return output_file


def main():
    parser = argparse.ArgumentParser(description="Read financial data from Google Sheets")
    parser.add_argument("--month", required=True, help="Month to read (YYYY-MM format)")
    parser.add_argument("--tab", help="Specific tab to read (optional)")
    parser.add_argument("--overview", action="store_true", help="Read overview tab only")
    parser.add_argument("--list-tabs", action="store_true", help="List available tabs")
    parser.add_argument("--dry-run", action="store_true", help="Don't save output")
    
    args = parser.parse_args()
    
    if args.list_tabs:
        sheet_id = get_sheet_id(args.month)
        tabs = list_tabs(sheet_id)
        print(f"Tabs in {args.month} sheet:")
        for tab in tabs:
            print(f"  - {tab}")
        return
    
    if args.overview:
        overview = read_overview(args.month)
        print(json.dumps(overview, indent=2))
        return
    
    transactions = read_transactions(args.month, args.tab)
    
    if not args.dry_run:
        save_transactions(transactions, args.month)
    else:
        print(f"\nDry run: would save {len(transactions)} transactions")
        if transactions:
            print("\nSample transaction:")
            print(json.dumps(transactions[0], indent=2))


if __name__ == "__main__":
    main()
