#!/usr/bin/env python3
"""
Debt tracking and paydown strategy for Ledger financial agent.
Monitors credit utilization and suggests paydown strategies.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# Load config
CONFIG_PATH = Path(__file__).parent.parent / "config.json"
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)


def load_debt_data() -> dict:
    """Load current debt data from config or saved file."""
    data_file = Path(__file__).parent.parent / "data" / "processed" / "debt.json"
    
    if data_file.exists():
        with open(data_file) as f:
            return json.load(f)
    
    # Return structure from config
    return {
        "accounts": CONFIG.get("debt", {}).get("cards", {}),
        "target_utilization": CONFIG.get("debt", {}).get("target_utilization", 30)
    }


def calculate_utilization(balance: float, limit: float) -> float:
    """Calculate utilization percentage."""
    if limit <= 0:
        return 0
    return round(balance / limit * 100, 1)


def analyze_debt(accounts: dict) -> dict:
    """Analyze overall debt position."""
    total_balance = 0
    total_limit = 0
    account_details = []
    
    for acc_id, acc in accounts.items():
        balance = acc.get("balance", 0)
        limit = acc.get("limit", 0)
        apr = acc.get("apr", 0)
        
        total_balance += balance
        total_limit += limit
        
        utilization = calculate_utilization(balance, limit)
        monthly_interest = balance * (apr / 100 / 12)
        
        account_details.append({
            "id": acc_id,
            "name": acc.get("name", acc_id.replace("_", " ").title()),
            "balance": balance,
            "limit": limit,
            "utilization": utilization,
            "apr": apr,
            "monthly_interest": round(monthly_interest, 2),
            "minimum_payment": acc.get("minimum_payment", 0),
            "status": "high" if utilization > 50 else "medium" if utilization > 30 else "good"
        })
    
    overall_utilization = calculate_utilization(total_balance, total_limit)
    
    return {
        "total_balance": total_balance,
        "total_limit": total_limit,
        "overall_utilization": overall_utilization,
        "accounts": sorted(account_details, key=lambda x: x["apr"], reverse=True),
        "monthly_interest_total": sum(a["monthly_interest"] for a in account_details),
        "status": "high" if overall_utilization > 50 else "medium" if overall_utilization > 30 else "good"
    }


def avalanche_strategy(analysis: dict, extra_payment: float = 0) -> list:
    """
    Avalanche strategy: Pay minimums on all, extra to highest APR.
    Most mathematically efficient - minimizes total interest paid.
    """
    strategy = []
    remaining_extra = extra_payment
    
    # Sort by APR descending
    accounts = sorted(analysis["accounts"], key=lambda x: x["apr"], reverse=True)
    
    for acc in accounts:
        minimum = acc["minimum_payment"]
        payment = minimum
        
        if remaining_extra > 0:
            # Add extra payment to highest APR account
            payment += remaining_extra
            remaining_extra = 0
        
        strategy.append({
            "account": acc["name"],
            "balance": acc["balance"],
            "apr": acc["apr"],
            "minimum": minimum,
            "recommended_payment": payment,
            "reason": "highest APR" if payment > minimum else "minimum"
        })
    
    return strategy


def snowball_strategy(analysis: dict, extra_payment: float = 0) -> list:
    """
    Snowball strategy: Pay minimums on all, extra to lowest balance.
    Psychologically motivating - quick wins from paying off small debts.
    """
    strategy = []
    remaining_extra = extra_payment
    
    # Sort by balance ascending
    accounts = sorted(analysis["accounts"], key=lambda x: x["balance"])
    
    for acc in accounts:
        minimum = acc["minimum_payment"]
        payment = minimum
        
        if remaining_extra > 0:
            # Add extra payment to lowest balance account
            payment += remaining_extra
            remaining_extra = 0
        
        strategy.append({
            "account": acc["name"],
            "balance": acc["balance"],
            "apr": acc["apr"],
            "minimum": minimum,
            "recommended_payment": payment,
            "reason": "lowest balance" if payment > minimum else "minimum"
        })
    
    return strategy


def calculate_payoff_time(balance: float, apr: float, payment: float) -> Optional[int]:
    """Calculate months to pay off a balance."""
    if payment <= 0:
        return None
    
    if apr == 0:
        return int(balance / payment) + 1
    
    monthly_rate = apr / 100 / 12
    
    if payment <= balance * monthly_rate:
        return None  # Payment doesn't cover interest
    
    # Formula: n = -log(1 - (r * P / M)) / log(1 + r)
    import math
    try:
        months = -math.log(1 - (monthly_rate * balance / payment)) / math.log(1 + monthly_rate)
        return int(months) + 1
    except (ValueError, ZeroDivisionError):
        return None


def project_payoff(analysis: dict, strategy: list) -> dict:
    """Project when debt will be paid off."""
    projections = []
    
    for acc in analysis["accounts"]:
        strat_item = next((s for s in strategy if s["account"] == acc["name"]), None)
        payment = strat_item["recommended_payment"] if strat_item else acc["minimum_payment"]
        
        months = calculate_payoff_time(acc["balance"], acc["apr"], payment)
        
        projections.append({
            "account": acc["name"],
            "balance": acc["balance"],
            "payment": payment,
            "months_to_payoff": months,
            "payoff_date": calculate_future_date(months) if months else None
        })
    
    # Total payoff (when all are paid)
    max_months = max((p["months_to_payoff"] or 0) for p in projections)
    
    return {
        "projections": projections,
        "total_months": max_months,
        "debt_free_date": calculate_future_date(max_months) if max_months else None
    }


def calculate_future_date(months: int) -> str:
    """Calculate date N months in future."""
    from dateutil.relativedelta import relativedelta
    future = datetime.now() + relativedelta(months=months)
    return future.strftime("%Y-%m")


def calculate_interest_savings(analysis: dict, extra_monthly: float) -> dict:
    """Calculate interest savings from extra payments."""
    total_interest_without = 0
    total_interest_with = 0
    
    for acc in analysis["accounts"]:
        balance = acc["balance"]
        apr = acc["apr"]
        minimum = acc["minimum_payment"]
        
        # Interest with minimum payments only
        months_min = calculate_payoff_time(balance, apr, minimum)
        if months_min:
            total_interest_without += (minimum * months_min) - balance
        
        # Interest with extra payment (avalanche - goes to highest APR first)
        payment = minimum + extra_monthly
        months_extra = calculate_payoff_time(balance, apr, payment)
        if months_extra:
            total_interest_with += (payment * months_extra) - balance
    
    return {
        "extra_monthly_payment": extra_monthly,
        "interest_minimum_only": round(total_interest_without, 2),
        "interest_with_extra": round(total_interest_with, 2),
        "savings": round(total_interest_without - total_interest_with, 2)
    }


def update_balances(accounts: dict, updates: dict) -> dict:
    """Update account balances."""
    for acc_id, new_balance in updates.items():
        if acc_id in accounts:
            accounts[acc_id]["balance"] = new_balance
            
            # Add to history
            if "history" not in accounts[acc_id]:
                accounts[acc_id]["history"] = []
            
            accounts[acc_id]["history"].append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "balance": new_balance
            })
    
    return accounts


def save_debt_data(data: dict):
    """Save debt data to file."""
    output_dir = Path(__file__).parent.parent / "data" / "processed"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "debt.json"
    
    data["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"✓ Saved debt data to {output_file}")


def print_report(analysis: dict, strategy: list, projection: dict, savings: Optional[dict] = None):
    """Print debt report."""
    print("\n" + "=" * 60)
    print("💳 DEBT ANALYSIS")
    print("=" * 60)
    
    status_icon = {"good": "🟢", "medium": "🟡", "high": "🔴"}.get(analysis["status"], "⚪")
    print(f"\n📊 OVERVIEW: {status_icon} {analysis['status'].upper()}")
    print(f"   Total balance: ${analysis['total_balance']:,.2f}")
    print(f"   Total limit: ${analysis['total_limit']:,.2f}")
    print(f"   Overall utilization: {analysis['overall_utilization']}%")
    print(f"   Monthly interest: ${analysis['monthly_interest_total']:,.2f}")
    
    print(f"\n💳 ACCOUNTS:")
    for acc in analysis["accounts"]:
        status_icon = {"good": "🟢", "medium": "🟡", "high": "🔴"}.get(acc["status"], "⚪")
        print(f"   {status_icon} {acc['name']}")
        print(f"      Balance: ${acc['balance']:,.2f} / ${acc['limit']:,.2f} ({acc['utilization']}%)")
        print(f"      APR: {acc['apr']}% | Monthly interest: ${acc['monthly_interest']}")
    
    print(f"\n📋 PAYMENT STRATEGY:")
    for item in strategy:
        extra = " ⭐" if item["recommended_payment"] > item["minimum"] else ""
        print(f"   {item['account']}: ${item['recommended_payment']:,.2f}{extra}")
        print(f"      (Minimum: ${item['minimum']}) - {item['reason']}")
    
    print(f"\n📅 PAYOFF PROJECTION:")
    for proj in projection["projections"]:
        if proj["months_to_payoff"]:
            print(f"   {proj['account']}: {proj['months_to_payoff']} months (by {proj['payoff_date']})")
        else:
            print(f"   {proj['account']}: ⚠ Payment doesn't cover interest")
    
    if projection["debt_free_date"]:
        print(f"\n   🎯 Debt-free by: {projection['debt_free_date']}")
    
    if savings:
        print(f"\n💡 INTEREST SAVINGS (with ${savings['extra_monthly_payment']}/mo extra):")
        print(f"   Interest (minimum only): ${savings['interest_minimum_only']:,.2f}")
        print(f"   Interest (with extra): ${savings['interest_with_extra']:,.2f}")
        print(f"   Savings: ${savings['savings']:,.2f}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Track debt and suggest paydown strategies")
    parser.add_argument("--strategy", choices=["avalanche", "snowball"], default="avalanche",
                       help="Paydown strategy (default: avalanche)")
    parser.add_argument("--extra", type=float, default=0, help="Extra monthly payment available")
    parser.add_argument("--update", type=str, help='Update balances: {"card_id": balance, ...}')
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    print("💳 Analyzing debt...")
    
    debt_data = load_debt_data()
    accounts = debt_data.get("accounts", {})
    
    if args.update:
        updates = json.loads(args.update)
        accounts = update_balances(accounts, updates)
        debt_data["accounts"] = accounts
        save_debt_data(debt_data)
    
    analysis = analyze_debt(accounts)
    
    if args.strategy == "avalanche":
        strategy = avalanche_strategy(analysis, args.extra)
    else:
        strategy = snowball_strategy(analysis, args.extra)
    
    projection = project_payoff(analysis, strategy)
    
    savings = None
    if args.extra > 0:
        savings = calculate_interest_savings(analysis, args.extra)
    
    if args.json:
        print(json.dumps({
            "analysis": analysis,
            "strategy": strategy,
            "projection": projection,
            "savings": savings
        }, indent=2))
    else:
        print_report(analysis, strategy, projection, savings)


if __name__ == "__main__":
    main()
