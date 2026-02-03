#!/usr/bin/env python3
"""
Monthly financial report generator for Ledger financial agent.
Combines all analyses into a comprehensive monthly report.
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

# Import other modules
from sheets_reader import read_transactions, save_transactions, get_sheet_id
from analyzer import analyze_transactions, generate_summary, save_analysis
from subscriptions import get_known_subscriptions, analyze_subscription_health, find_cancellation_candidates
from burn_rate import calculate_averages, calculate_runway, generate_recommendations, load_summaries
from debt_tracker import load_debt_data, analyze_debt, avalanche_strategy, project_payoff


def generate_monthly_report(month: str, refresh_data: bool = False) -> dict:
    """Generate a comprehensive monthly report."""
    
    report = {
        "month": month,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "sections": {}
    }
    
    data_dir = Path(__file__).parent.parent / "data" / "processed"
    
    # 1. Load or refresh transaction data
    print(f"📊 Generating report for {month}...")
    
    analyzed_file = data_dir / f"analyzed_{month}.json"
    
    if refresh_data or not analyzed_file.exists():
        print("   Refreshing transaction data...")
        try:
            transactions = read_transactions(month)
            save_transactions(transactions, month)
            
            # Re-load and analyze
            from analyzer import load_transactions
            transactions = load_transactions(month)
            analyzed = analyze_transactions(transactions)
            summary = generate_summary(analyzed, month)
            save_analysis(analyzed, summary, month)
        except Exception as e:
            print(f"   ⚠ Could not refresh data: {e}")
            return {"error": str(e)}
    else:
        print("   Using cached transaction data...")
        with open(analyzed_file) as f:
            data = json.load(f)
            analyzed = data.get("transactions", [])
        
        summary_file = data_dir / f"summary_{month}.json"
        if summary_file.exists():
            with open(summary_file) as f:
                summary = json.load(f)
        else:
            summary = generate_summary(analyzed, month)
    
    report["sections"]["summary"] = summary
    
    # 2. Subscription analysis
    print("   Analyzing subscriptions...")
    known_subs = get_known_subscriptions(analyzed)
    sub_health = analyze_subscription_health(known_subs)
    cancellation_candidates = find_cancellation_candidates(known_subs)
    
    report["sections"]["subscriptions"] = {
        "health": sub_health,
        "cancellation_candidates": cancellation_candidates
    }
    
    # 3. Burn rate (if we have multiple months)
    print("   Calculating burn rate...")
    summaries = load_summaries()
    if len(summaries) > 1:
        averages = calculate_averages(summaries, min(3, len(summaries)))
        runway = calculate_runway(averages)
        recommendations = generate_recommendations(averages)
        
        report["sections"]["burn_rate"] = {
            "averages": averages,
            "runway": runway,
            "recommendations": recommendations
        }
    else:
        report["sections"]["burn_rate"] = {
            "note": "Need at least 2 months of data for trend analysis"
        }
    
    # 4. Debt analysis
    print("   Analyzing debt...")
    debt_data = load_debt_data()
    if debt_data.get("accounts"):
        debt_analysis = analyze_debt(debt_data["accounts"])
        strategy = avalanche_strategy(debt_analysis)
        projection = project_payoff(debt_analysis, strategy)
        
        report["sections"]["debt"] = {
            "analysis": debt_analysis,
            "strategy": strategy,
            "projection": projection
        }
    else:
        report["sections"]["debt"] = {
            "note": "No debt accounts configured"
        }
    
    # 5. Highlights and alerts
    print("   Generating highlights...")
    highlights = generate_highlights(report)
    report["highlights"] = highlights
    
    return report


def generate_highlights(report: dict) -> dict:
    """Generate key highlights and alerts from the report."""
    highlights = {
        "good": [],
        "warnings": [],
        "actions": []
    }
    
    summary = report["sections"].get("summary", {})
    
    # Income/expense highlights
    if summary.get("net", 0) > 0:
        highlights["good"].append(f"Profitable month: +${summary['net']:,.2f}")
    else:
        highlights["warnings"].append(f"Net loss this month: ${summary['net']:,.2f}")
    
    if summary.get("savings_rate", 0) >= 20:
        highlights["good"].append(f"Strong savings rate: {summary['savings_rate']}%")
    
    # Subscription highlights
    subs = report["sections"].get("subscriptions", {})
    if subs.get("cancellation_candidates"):
        highlights["actions"].append(
            f"{len(subs['cancellation_candidates'])} subscriptions to review for cancellation"
        )
    
    # Flagged transactions
    flagged = summary.get("flagged_count", 0)
    if flagged > 0:
        highlights["actions"].append(f"{flagged} transactions flagged for review")
    
    # Debt highlights
    debt = report["sections"].get("debt", {})
    if debt.get("analysis"):
        utilization = debt["analysis"].get("overall_utilization", 0)
        if utilization > 50:
            highlights["warnings"].append(f"High credit utilization: {utilization}%")
        elif utilization < 30:
            highlights["good"].append(f"Healthy credit utilization: {utilization}%")
    
    # Burn rate warnings
    burn = report["sections"].get("burn_rate", {})
    if burn.get("recommendations"):
        high_priority = [r for r in burn["recommendations"] if r["priority"] == "high"]
        for rec in high_priority:
            highlights["warnings"].append(rec["issue"])
    
    return highlights


def save_report(report: dict, month: str):
    """Save the report to a file."""
    output_dir = Path(__file__).parent.parent / "data" / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"report_{month}.json"
    
    with open(output_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"✓ Saved report to {output_file}")
    return output_file


def print_report(report: dict):
    """Print a formatted report."""
    print("\n" + "=" * 70)
    print(f"📊 MONTHLY FINANCIAL REPORT: {report['month']}")
    print(f"   Generated: {report['generated_at']}")
    print("=" * 70)
    
    # Highlights
    highlights = report.get("highlights", {})
    
    if highlights.get("good"):
        print("\n✅ GOOD NEWS:")
        for item in highlights["good"]:
            print(f"   • {item}")
    
    if highlights.get("warnings"):
        print("\n⚠️ WARNINGS:")
        for item in highlights["warnings"]:
            print(f"   • {item}")
    
    if highlights.get("actions"):
        print("\n📋 ACTION ITEMS:")
        for item in highlights["actions"]:
            print(f"   • {item}")
    
    # Summary section
    summary = report["sections"].get("summary", {})
    print("\n" + "-" * 70)
    print("💰 INCOME & EXPENSES")
    print("-" * 70)
    print(f"   Income: ${summary.get('income', {}).get('total', 0):,.2f}")
    print(f"   Expenses: ${summary.get('expenses', {}).get('total', 0):,.2f}")
    print(f"   Net: ${summary.get('net', 0):,.2f}")
    print(f"   Savings rate: {summary.get('savings_rate', 0)}%")
    
    # Subscriptions
    subs = report["sections"].get("subscriptions", {})
    health = subs.get("health", {})
    if health:
        print("\n" + "-" * 70)
        print("📦 SUBSCRIPTIONS")
        print("-" * 70)
        print(f"   Active: {health.get('total_active', 0)}")
        print(f"   Monthly cost: ${health.get('monthly_burn', 0):,.2f}")
        print(f"   Annual cost: ${health.get('annual_cost', 0):,.2f}")
    
    # Debt
    debt = report["sections"].get("debt", {})
    if debt.get("analysis"):
        analysis = debt["analysis"]
        print("\n" + "-" * 70)
        print("💳 DEBT")
        print("-" * 70)
        print(f"   Total balance: ${analysis['total_balance']:,.2f}")
        print(f"   Utilization: {analysis['overall_utilization']}%")
        if debt.get("projection", {}).get("debt_free_date"):
            print(f"   Projected debt-free: {debt['projection']['debt_free_date']}")
    
    # Burn rate
    burn = report["sections"].get("burn_rate", {})
    if burn.get("averages"):
        print("\n" + "-" * 70)
        print("🔥 BURN RATE (3-month average)")
        print("-" * 70)
        avg = burn["averages"]["average"]
        print(f"   Avg income: ${avg['income']:,.2f}")
        print(f"   Avg expenses: ${avg['expenses']:,.2f}")
        print(f"   Avg net: ${avg['net']:,.2f}")
    
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive monthly financial report")
    parser.add_argument("--month", required=True, help="Month to report on (YYYY-MM format)")
    parser.add_argument("--refresh", action="store_true", help="Refresh data from Google Sheets")
    parser.add_argument("--json", action="store_true", help="Output as JSON only")
    parser.add_argument("--no-save", action="store_true", help="Don't save report to file")
    
    args = parser.parse_args()
    
    report = generate_monthly_report(args.month, args.refresh)
    
    if "error" in report:
        print(f"❌ Error generating report: {report['error']}")
        return
    
    if not args.no_save:
        save_report(report, args.month)
    
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
