#!/usr/bin/env python3
"""
Subscription detector and manager for Ledger financial agent.
Identifies recurring charges and tracks subscription status.
"""

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import re

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)


def load_all_transactions() -> list[dict]:
    """Load transactions from all available months."""
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    all_transactions = []
    
    for file in sorted(data_dir.glob("analyzed_*.json")):
        with open(file) as f:
            data = json.load(f)
            all_transactions.extend(data.get("transactions", []))
    
    return sorted(all_transactions, key=lambda x: x["date"])


def detect_recurring_charges(transactions: list[dict]) -> dict:
    """Detect potential recurring charges not in known subscriptions."""
    # Group transactions by normalized description
    by_description = defaultdict(list)
    
    for tx in transactions:
        if tx.get("category") in ["income", "transfer"]:
            continue
        
        # Normalize description (remove dates, numbers, etc.)
        desc = tx["description"].upper()
        desc = re.sub(r'\d{2}/\d{2}', '', desc)  # Remove dates
        desc = re.sub(r'#\d+', '', desc)  # Remove order numbers
        desc = re.sub(r'\s+', ' ', desc).strip()
        
        by_description[desc].append(tx)
    
    # Find recurring patterns
    recurring = {}
    thresholds = CONFIG["thresholds"]["subscription_detection"]
    
    for desc, txs in by_description.items():
        if len(txs) < thresholds["min_occurrences"]:
            continue
        
        # Check if amounts are consistent
        amounts = [abs(tx["amount"]) for tx in txs]
        avg_amount = sum(amounts) / len(amounts)
        variance = max(abs(a - avg_amount) / avg_amount * 100 for a in amounts) if avg_amount > 0 else 100
        
        if variance > thresholds["amount_variance_percent"]:
            continue
        
        # Check if timing is consistent (monthly-ish)
        dates = sorted([datetime.strptime(tx["date"], "%Y-%m-%d") for tx in txs])
        if len(dates) < 2:
            continue
        
        intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
        avg_interval = sum(intervals) / len(intervals)
        
        if not (thresholds["days_between_min"] <= avg_interval <= thresholds["days_between_max"]):
            continue
        
        # This looks like a subscription!
        recurring[desc] = {
            "name": desc[:50],
            "pattern": desc,
            "amount": round(avg_amount, 2),
            "frequency": "monthly" if 25 <= avg_interval <= 35 else "other",
            "occurrences": len(txs),
            "first_seen": min(tx["date"] for tx in txs),
            "last_seen": max(tx["date"] for tx in txs),
            "dates": [tx["date"] for tx in txs],
            "status": "detected",
            "is_known": False
        }
    
    return recurring


def get_known_subscriptions(transactions: list[dict]) -> dict:
    """Get status of known subscriptions from transactions."""
    known = {}
    
    for sub_id, sub_info in CONFIG["categories"]["subscriptions"]["known"].items():
        pattern = sub_info["pattern"]
        
        matching_txs = [
            tx for tx in transactions 
            if re.search(pattern, tx["description"].upper())
        ]
        
        if not matching_txs:
            known[sub_id] = {
                "name": sub_id.replace("_", " ").title(),
                "pattern": pattern,
                "amount": sub_info.get("expected"),
                "status": "not_found",
                "category": sub_info.get("category", "unknown"),
                "subcategory": sub_info.get("subcategory", "other"),
                "is_known": True
            }
            continue
        
        amounts = [abs(tx["amount"]) for tx in matching_txs]
        dates = [tx["date"] for tx in matching_txs]
        
        # Check for cancellation annotations
        cancelled = any(
            "cancelled" in tx.get("annotation", "").lower() 
            for tx in matching_txs
        )
        
        known[sub_id] = {
            "name": sub_id.replace("_", " ").title(),
            "pattern": pattern,
            "amount": round(sum(amounts) / len(amounts), 2),
            "expected_amount": sub_info.get("expected"),
            "actual_amounts": amounts,
            "frequency": "monthly",
            "occurrences": len(matching_txs),
            "first_seen": min(dates),
            "last_seen": max(dates),
            "dates": dates,
            "status": "cancelled" if cancelled else "active",
            "category": sub_info.get("category", "unknown"),
            "subcategory": sub_info.get("subcategory", "other"),
            "is_known": True,
            "total_spent": sum(amounts)
        }
    
    return known


def analyze_subscription_health(subscriptions: dict) -> dict:
    """Analyze subscription portfolio health."""
    active = [s for s in subscriptions.values() if s.get("status") == "active"]
    cancelled = [s for s in subscriptions.values() if s.get("status") == "cancelled"]
    
    # Calculate monthly burn from subscriptions
    monthly_burn = sum(s.get("amount", 0) for s in active)
    
    # Categorize by business vs personal
    business = [s for s in active if s.get("category") == "business"]
    personal = [s for s in active if s.get("category") == "personal"]
    mixed = [s for s in active if s.get("category") == "mixed"]
    
    business_cost = sum(s.get("amount", 0) for s in business)
    personal_cost = sum(s.get("amount", 0) for s in personal)
    
    return {
        "total_active": len(active),
        "total_cancelled": len(cancelled),
        "monthly_burn": round(monthly_burn, 2),
        "annual_cost": round(monthly_burn * 12, 2),
        "business": {
            "count": len(business),
            "monthly": round(business_cost, 2),
            "annual": round(business_cost * 12, 2)
        },
        "personal": {
            "count": len(personal),
            "monthly": round(personal_cost, 2),
            "annual": round(personal_cost * 12, 2)
        },
        "top_expenses": sorted(
            active, 
            key=lambda x: x.get("amount", 0), 
            reverse=True
        )[:5]
    }


def find_cancellation_candidates(subscriptions: dict) -> list[dict]:
    """Find subscriptions that might be worth cancelling."""
    candidates = []
    
    for sub_id, sub in subscriptions.items():
        if sub.get("status") != "active":
            continue
        
        reasons = []
        
        # Check for price increases
        if sub.get("expected_amount") and sub.get("amount"):
            if sub["amount"] > sub["expected_amount"] * 1.1:
                reasons.append(f"Price increased from ${sub['expected_amount']} to ${sub['amount']}")
        
        # Personal entertainment subscriptions
        if sub.get("category") == "personal" and sub.get("subcategory") == "entertainment":
            reasons.append("Entertainment expense - review if still used")
        
        # High-cost subscriptions
        if sub.get("amount", 0) > 50:
            reasons.append(f"High cost: ${sub['amount']}/month")
        
        if reasons:
            candidates.append({
                "id": sub_id,
                "name": sub.get("name"),
                "amount": sub.get("amount"),
                "category": sub.get("category"),
                "reasons": reasons
            })
    
    return candidates


def save_subscriptions(subscriptions: dict, health: dict):
    """Save subscription data."""
    output_dir = Path(__file__).parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "subscriptions.json"
    
    with open(output_file, "w") as f:
        json.dump({
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "subscriptions": subscriptions,
            "health": health
        }, f, indent=2)
    
    print(f"✓ Saved subscription data to {output_file}")


def print_report(subscriptions: dict, health: dict, candidates: list):
    """Print subscription report."""
    print("\n" + "=" * 60)
    print("📦 SUBSCRIPTION REPORT")
    print("=" * 60)
    
    print(f"\n📊 SUMMARY:")
    print(f"   Active subscriptions: {health['total_active']}")
    print(f"   Monthly burn: ${health['monthly_burn']:,.2f}")
    print(f"   Annual cost: ${health['annual_cost']:,.2f}")
    
    print(f"\n💼 BUSINESS:")
    print(f"   {health['business']['count']} subscriptions")
    print(f"   ${health['business']['monthly']:,.2f}/month (${health['business']['annual']:,.2f}/year)")
    
    print(f"\n🎮 PERSONAL:")
    print(f"   {health['personal']['count']} subscriptions")
    print(f"   ${health['personal']['monthly']:,.2f}/month (${health['personal']['annual']:,.2f}/year)")
    
    print(f"\n💰 TOP EXPENSES:")
    for sub in health["top_expenses"]:
        status_icon = "✓" if sub["status"] == "active" else "✗"
        print(f"   {status_icon} {sub['name']}: ${sub.get('amount', 0):,.2f}/month")
    
    if candidates:
        print(f"\n⚠️ CANCELLATION CANDIDATES:")
        for c in candidates:
            print(f"   {c['name']}: ${c['amount']:,.2f}/month")
            for reason in c["reasons"]:
                print(f"      → {reason}")
    
    print("\n📋 ALL SUBSCRIPTIONS:")
    for sub_id, sub in sorted(subscriptions.items(), key=lambda x: x[1].get("amount", 0), reverse=True):
        status = sub.get("status", "unknown")
        icon = {"active": "✓", "cancelled": "✗", "not_found": "?", "detected": "🔍"}.get(status, "•")
        amount = sub.get("amount", 0)
        cat = sub.get("category", "")
        print(f"   {icon} {sub['name']}: ${amount:,.2f} [{cat}] ({status})")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Detect and manage subscriptions")
    parser.add_argument("--detect", action="store_true", help="Detect recurring charges")
    parser.add_argument("--known-only", action="store_true", help="Only show known subscriptions")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-save", action="store_true", help="Don't save output")
    
    args = parser.parse_args()
    
    print("🔍 Analyzing subscriptions...")
    
    transactions = load_all_transactions()
    print(f"   Loaded {len(transactions)} transactions")
    
    # Get known subscriptions
    known = get_known_subscriptions(transactions)
    
    # Detect unknown recurring charges
    detected = {}
    if args.detect and not args.known_only:
        detected = detect_recurring_charges(transactions)
        # Filter out already known ones
        detected = {k: v for k, v in detected.items() 
                   if not any(re.search(sub["pattern"], k) 
                             for sub in CONFIG["categories"]["subscriptions"]["known"].values())}
    
    # Combine
    all_subs = {**known, **detected}
    
    # Analyze health
    health = analyze_subscription_health(all_subs)
    
    # Find cancellation candidates
    candidates = find_cancellation_candidates(all_subs)
    
    if not args.no_save:
        save_subscriptions(all_subs, health)
    
    if args.json:
        print(json.dumps({"subscriptions": all_subs, "health": health, "candidates": candidates}, indent=2))
    else:
        print_report(all_subs, health, candidates)


if __name__ == "__main__":
    main()
