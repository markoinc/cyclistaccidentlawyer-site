#!/usr/bin/env python3
"""
Burn rate and profitability calculator for Ledger financial agent.
Calculates monthly income vs expenses and projects runway.
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


def load_summaries() -> dict:
    """Load all monthly summaries."""
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    summaries = {}
    
    for file in sorted(data_dir.glob("summary_*.json")):
        with open(file) as f:
            data = json.load(f)
            month = data.get("month")
            if month:
                summaries[month] = data
    
    return summaries


def calculate_averages(summaries: dict, months: int = 3) -> dict:
    """Calculate average income/expenses over recent months."""
    sorted_months = sorted(summaries.keys(), reverse=True)[:months]
    
    if not sorted_months:
        return {"error": "No data available"}
    
    incomes = [summaries[m]["income"]["total"] for m in sorted_months]
    expenses = [summaries[m]["expenses"]["total"] for m in sorted_months]
    subscription_costs = [summaries[m]["expenses"]["subscriptions"] for m in sorted_months]
    
    avg_income = sum(incomes) / len(incomes)
    avg_expenses = sum(expenses) / len(expenses)
    avg_subscriptions = sum(subscription_costs) / len(subscription_costs)
    
    return {
        "period_months": len(sorted_months),
        "months_analyzed": sorted_months,
        "average": {
            "income": round(avg_income, 2),
            "expenses": round(avg_expenses, 2),
            "subscriptions": round(avg_subscriptions, 2),
            "net": round(avg_income - avg_expenses, 2),
            "savings_rate": round((avg_income - avg_expenses) / avg_income * 100, 1) if avg_income > 0 else 0
        },
        "monthly_data": {
            m: {
                "income": summaries[m]["income"]["total"],
                "expenses": summaries[m]["expenses"]["total"],
                "net": summaries[m]["net"]
            }
            for m in sorted_months
        },
        "trend": {
            "income": calculate_trend(incomes),
            "expenses": calculate_trend(expenses)
        }
    }


def calculate_trend(values: list) -> str:
    """Determine if values are trending up, down, or stable."""
    if len(values) < 2:
        return "insufficient_data"
    
    # Compare first half to second half
    mid = len(values) // 2
    first_half = sum(values[:mid]) / max(mid, 1)
    second_half = sum(values[mid:]) / max(len(values) - mid, 1)
    
    change = (second_half - first_half) / first_half * 100 if first_half > 0 else 0
    
    if change > 10:
        return "increasing"
    elif change < -10:
        return "decreasing"
    else:
        return "stable"


def calculate_runway(averages: dict, current_cash: float = 0) -> dict:
    """Calculate runway based on burn rate."""
    monthly_net = averages["average"]["net"]
    
    if monthly_net >= 0:
        return {
            "status": "profitable",
            "monthly_net": monthly_net,
            "message": "Business is profitable, no runway concern"
        }
    
    burn_rate = abs(monthly_net)
    
    if current_cash > 0:
        months_remaining = current_cash / burn_rate
        return {
            "status": "burning",
            "monthly_burn": burn_rate,
            "current_cash": current_cash,
            "months_remaining": round(months_remaining, 1),
            "runway_date": calculate_future_date(months_remaining)
        }
    
    return {
        "status": "burning",
        "monthly_burn": burn_rate,
        "message": "Provide current_cash to calculate runway"
    }


def calculate_future_date(months: float) -> str:
    """Calculate a date N months in the future."""
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    future = datetime.now() + relativedelta(months=int(months))
    return future.strftime("%Y-%m")


def generate_recommendations(averages: dict, subscriptions_path: Optional[Path] = None) -> list:
    """Generate actionable recommendations based on financial data."""
    recommendations = []
    
    avg = averages["average"]
    
    # Profitability check
    if avg["net"] < 0:
        recommendations.append({
            "priority": "high",
            "category": "profitability",
            "issue": f"Negative monthly net: ${avg['net']:,.2f}",
            "action": "Reduce expenses or increase income to become profitable"
        })
    elif avg["savings_rate"] < 20:
        recommendations.append({
            "priority": "medium",
            "category": "savings",
            "issue": f"Low savings rate: {avg['savings_rate']}%",
            "action": "Target 20-30% savings rate for financial health"
        })
    
    # Subscription burden
    subscription_ratio = avg["subscriptions"] / avg["expenses"] * 100 if avg["expenses"] > 0 else 0
    if subscription_ratio > 40:
        recommendations.append({
            "priority": "medium",
            "category": "subscriptions",
            "issue": f"Subscriptions are {subscription_ratio:.1f}% of expenses",
            "action": "Review subscriptions for consolidation opportunities"
        })
    
    # Load subscription candidates if available
    if subscriptions_path and subscriptions_path.exists():
        with open(subscriptions_path) as f:
            sub_data = json.load(f)
            if "health" in sub_data:
                annual = sub_data["health"].get("annual_cost", 0)
                if annual > 3000:
                    recommendations.append({
                        "priority": "low",
                        "category": "subscriptions",
                        "issue": f"Annual subscription cost: ${annual:,.2f}",
                        "action": "Consider annual billing for discounts on key services"
                    })
    
    # Trend warnings
    if averages["trend"]["expenses"] == "increasing":
        recommendations.append({
            "priority": "medium",
            "category": "expenses",
            "issue": "Expenses are trending upward",
            "action": "Review recent expense increases"
        })
    
    if averages["trend"]["income"] == "decreasing":
        recommendations.append({
            "priority": "high",
            "category": "income",
            "issue": "Income is trending downward",
            "action": "Focus on revenue-generating activities"
        })
    
    return recommendations


def print_report(averages: dict, runway: dict, recommendations: list):
    """Print burn rate report."""
    print("\n" + "=" * 60)
    print("🔥 BURN RATE ANALYSIS")
    print("=" * 60)
    
    print(f"\n📅 PERIOD: {averages['period_months']} months")
    print(f"   Months analyzed: {', '.join(averages['months_analyzed'])}")
    
    avg = averages["average"]
    print(f"\n💰 AVERAGES:")
    print(f"   Income: ${avg['income']:,.2f}/month")
    print(f"   Expenses: ${avg['expenses']:,.2f}/month")
    print(f"   Subscriptions: ${avg['subscriptions']:,.2f}/month")
    print(f"   Net: ${avg['net']:,.2f}/month")
    print(f"   Savings rate: {avg['savings_rate']}%")
    
    print(f"\n📈 TRENDS:")
    print(f"   Income: {averages['trend']['income']}")
    print(f"   Expenses: {averages['trend']['expenses']}")
    
    print(f"\n🚀 RUNWAY:")
    if runway["status"] == "profitable":
        print(f"   ✓ {runway['message']}")
        print(f"   Monthly profit: ${runway['monthly_net']:,.2f}")
    else:
        print(f"   ⚠ Monthly burn: ${runway['monthly_burn']:,.2f}")
        if "months_remaining" in runway:
            print(f"   Cash remaining: ${runway['current_cash']:,.2f}")
            print(f"   Runway: {runway['months_remaining']} months")
            print(f"   Zero date: ~{runway['runway_date']}")
    
    if recommendations:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in sorted(recommendations, key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x["priority"], 3)):
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(rec["priority"], "⚪")
            print(f"   {priority_icon} [{rec['category']}] {rec['issue']}")
            print(f"      → {rec['action']}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Calculate burn rate and profitability")
    parser.add_argument("--months", type=int, default=3, help="Number of months to analyze")
    parser.add_argument("--cash", type=float, help="Current cash on hand for runway calc")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    print("📊 Calculating burn rate...")
    
    summaries = load_summaries()
    
    if not summaries:
        print("❌ No monthly summaries found. Run analyzer.py first.")
        return
    
    print(f"   Found {len(summaries)} months of data")
    
    averages = calculate_averages(summaries, args.months)
    runway = calculate_runway(averages, args.cash or 0)
    
    sub_path = Path(__file__).parent.parent / "data" / "processed" / "subscriptions.json"
    recommendations = generate_recommendations(averages, sub_path)
    
    if args.json:
        print(json.dumps({
            "averages": averages,
            "runway": runway,
            "recommendations": recommendations
        }, indent=2))
    else:
        print_report(averages, runway, recommendations)


if __name__ == "__main__":
    main()
