#!/usr/bin/env python3
"""
Transaction analyzer for Ledger financial agent.
Categorizes transactions and identifies patterns.
"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)


def load_transactions(month: str) -> list[dict]:
    """Load transactions from processed data file."""
    data_file = Path(__file__).parent.parent / "data" / "processed" / f"transactions_{month}.json"
    
    if not data_file.exists():
        raise FileNotFoundError(f"No transaction data for {month}. Run sheets_reader.py first.")
    
    with open(data_file) as f:
        data = json.load(f)
    
    return data.get("transactions", [])


def categorize_transaction(tx: dict) -> dict:
    """Categorize a single transaction based on patterns."""
    description = tx["description"].upper()
    amount = tx["amount"]
    
    # Check for income
    for pattern in CONFIG["categories"]["income"]["patterns"]:
        if re.search(pattern, description):
            tx["category"] = "income"
            tx["tax_category"] = "business"
            
            # Subcategorize income
            for subcat, subpatterns in CONFIG["categories"]["income"]["subcategories"].items():
                for sp in subpatterns:
                    if re.search(sp, description):
                        tx["subcategory"] = subcat
                        break
            return tx
    
    # Check for known subscriptions
    for sub_id, sub_info in CONFIG["categories"]["subscriptions"]["known"].items():
        if re.search(sub_info["pattern"], description):
            tx["category"] = "subscription"
            tx["subcategory"] = sub_info.get("subcategory", "other")
            tx["tax_category"] = sub_info.get("category", "unknown")
            tx["subscription_id"] = sub_id
            tx["is_recurring"] = True
            return tx
    
    # Check for transfers (exclude from expenses)
    for pattern in CONFIG["categories"]["transfers"]["patterns"]:
        if re.search(pattern, description):
            tx["category"] = "transfer"
            tx["tax_category"] = "none"
            return tx
    
    # Check for food
    for pattern in CONFIG["categories"]["food"]["patterns"]:
        if re.search(pattern, description):
            tx["category"] = "food"
            tx["tax_category"] = "personal"
            return tx
    
    # Check for utilities
    for pattern in CONFIG["categories"]["utilities"]["patterns"]:
        if re.search(pattern, description):
            tx["category"] = "utilities"
            tx["tax_category"] = "mixed"
            return tx
    
    # Check for travel
    for pattern in CONFIG["categories"]["travel"]["patterns"]:
        if re.search(pattern, description):
            tx["category"] = "travel"
            tx["tax_category"] = "mixed"
            return tx
    
    # Default
    tx["category"] = "other"
    tx["tax_category"] = "unknown"
    return tx


def flag_transaction(tx: dict) -> dict:
    """Add flags for notable transactions."""
    flags = []
    amount = abs(tx["amount"])
    
    # Large expense
    if amount >= CONFIG["thresholds"]["large_expense"] and tx.get("category") != "income":
        flags.append("large_expense")
    
    # Check annotation for action items
    annotation = tx.get("annotation", "").lower()
    for keyword in CONFIG["annotations"]["action_keywords"]:
        if keyword in annotation:
            flags.append(f"annotation:{keyword}")
    
    if flags:
        tx["flags"] = flags
    
    return tx


def analyze_transactions(transactions: list[dict]) -> list[dict]:
    """Analyze and categorize all transactions."""
    analyzed = []
    
    for tx in transactions:
        tx = categorize_transaction(tx.copy())
        tx = flag_transaction(tx)
        analyzed.append(tx)
    
    return analyzed


def generate_summary(transactions: list[dict], month: str) -> dict:
    """Generate a summary of analyzed transactions."""
    income_total = sum(t["amount"] for t in transactions if t.get("category") == "income")
    
    expense_txs = [t for t in transactions if t.get("category") not in ["income", "transfer", None]]
    expenses_total = abs(sum(t["amount"] for t in expense_txs))
    
    subscription_total = abs(sum(t["amount"] for t in transactions if t.get("category") == "subscription"))
    
    # Breakdown by category
    by_category = {}
    for tx in transactions:
        cat = tx.get("category", "uncategorized")
        by_category[cat] = by_category.get(cat, 0) + abs(tx["amount"])
    
    # Tax breakdown
    by_tax = {}
    for tx in expense_txs:
        tax_cat = tx.get("tax_category", "unknown")
        by_tax[tax_cat] = by_tax.get(tax_cat, 0) + abs(tx["amount"])
    
    # Flagged transactions
    flagged = [t for t in transactions if t.get("flags")]
    
    return {
        "month": month,
        "transaction_count": len(transactions),
        "income": {
            "total": income_total,
            "sources": len([t for t in transactions if t.get("category") == "income"])
        },
        "expenses": {
            "total": expenses_total,
            "subscriptions": subscription_total,
            "one_time": expenses_total - subscription_total
        },
        "net": income_total - expenses_total,
        "savings_rate": round((income_total - expenses_total) / income_total * 100, 1) if income_total > 0 else 0,
        "by_category": by_category,
        "by_tax_category": by_tax,
        "flagged_count": len(flagged),
        "flagged_transactions": [
            {"description": t["description"][:50], "amount": t["amount"], "flags": t["flags"]}
            for t in flagged
        ]
    }


def save_analysis(transactions: list[dict], summary: dict, month: str):
    """Save analyzed data to files."""
    output_dir = Path(__file__).parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save analyzed transactions
    tx_file = output_dir / f"analyzed_{month}.json"
    with open(tx_file, "w") as f:
        json.dump({
            "month": month,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "transactions": transactions
        }, f, indent=2)
    
    # Save summary
    summary_file = output_dir / f"summary_{month}.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"✓ Saved analyzed transactions to {tx_file}")
    print(f"✓ Saved summary to {summary_file}")


def print_summary(summary: dict):
    """Print a formatted summary."""
    print("\n" + "=" * 60)
    print(f"📊 FINANCIAL SUMMARY: {summary['month']}")
    print("=" * 60)
    
    print(f"\n💰 INCOME: ${summary['income']['total']:,.2f}")
    print(f"   ({summary['income']['sources']} income transactions)")
    
    print(f"\n💸 EXPENSES: ${summary['expenses']['total']:,.2f}")
    print(f"   Subscriptions: ${summary['expenses']['subscriptions']:,.2f}")
    print(f"   One-time: ${summary['expenses']['one_time']:,.2f}")
    
    print(f"\n📈 NET: ${summary['net']:,.2f}")
    print(f"   Savings rate: {summary['savings_rate']}%")
    
    print("\n📂 BY CATEGORY:")
    for cat, amount in sorted(summary["by_category"].items(), key=lambda x: -x[1]):
        print(f"   {cat}: ${amount:,.2f}")
    
    print("\n🏷️ TAX CATEGORIES:")
    for cat, amount in sorted(summary["by_tax_category"].items(), key=lambda x: -x[1]):
        print(f"   {cat}: ${amount:,.2f}")
    
    if summary["flagged_count"] > 0:
        print(f"\n⚠️ FLAGGED TRANSACTIONS: {summary['flagged_count']}")
        for tx in summary["flagged_transactions"][:5]:
            print(f"   {tx['description']}: ${tx['amount']:,.2f} [{', '.join(tx['flags'])}]")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Analyze and categorize transactions")
    parser.add_argument("--month", required=True, help="Month to analyze (YYYY-MM format)")
    parser.add_argument("--no-save", action="store_true", help="Don't save output files")
    parser.add_argument("--json", action="store_true", help="Output summary as JSON")
    
    args = parser.parse_args()
    
    print(f"🔍 Analyzing transactions for {args.month}...")
    
    transactions = load_transactions(args.month)
    print(f"   Loaded {len(transactions)} transactions")
    
    analyzed = analyze_transactions(transactions)
    summary = generate_summary(analyzed, args.month)
    
    if not args.no_save:
        save_analysis(analyzed, summary, args.month)
    
    if args.json:
        print(json.dumps(summary, indent=2))
    else:
        print_summary(summary)


if __name__ == "__main__":
    main()
