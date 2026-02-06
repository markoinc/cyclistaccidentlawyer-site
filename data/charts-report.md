# 📈 Charts Report — All Time Financial Overview

**Date:** 2025-07-14  
**Sheet:** [All Time Financial Overview](https://docs.google.com/spreadsheets/d/1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ)

---

## ✅ Summary

Successfully created **8 embedded charts** on a new **📈 Charts** tab plus **6 sparkline mini-charts** on the **🌐 All Time Dashboard** tab.

---

## 📊 Charts Created

### Tab: 📈 Charts (sheetId: 100)
Tab color: Amber/Gold (#FBBC04)

| # | Chart | Type | Data Source | Chart ID |
|---|-------|------|-------------|----------|
| 1 | **Monthly Revenue & Expenses** | Line | Dashboard!A20:C45 (25 months) | 1001341344 |
| 2 | **Monthly Net Profit** | Column (Bar) | Dashboard!A20:D45 | 109132130 |
| 3 | **Revenue by Business Line** | Pie | Dashboard!A13:E15 (3 segments) | 1299974167 |
| 4 | **Expense Breakdown (All Time)** | Donut (Pie w/ hole) | Dashboard!A51:E56 (6 categories) | 806309374 |
| 5 | **Profit Margin Trend** | Line + Dashed Target | Dashboard!A20:E45 + G20:G45 (50% target) | 101762990 |
| 6 | **Debt Payoff Progress** | Multi-Line | Dashboard!A99:G108 (5 debt lines + total) | 993254914 |
| 7 | **Annual Revenue Comparison** | Grouped Column | Charts!M1:P4 (helper data) | 1624785761 |
| 8 | **Net Worth Over Time** | Area | Dashboard!A86:D95 (9 months) | 901736164 |

### Chart Layout (Grid)
```
Row 0:    ┌──────────────── 📈 FINANCIAL CHARTS DASHBOARD ────────────────┐
Row 1:    │  Revenue & Profit Trends                                       │
Row 2-22: │  [Chart 1: Rev & Exp Line]     [Chart 2: Net Profit Bars]     │
Row 23:   │  Revenue & Expense Breakdown                                   │
Row 24-44:│  [Chart 3: Business Pie]       [Chart 4: Expense Donut]       │
Row 45:   │  Margins & Debt Tracking                                       │
Row 46-66:│  [Chart 5: Margin + Target]    [Chart 6: Debt Lines]          │
Row 67:   │  Annual Comparison & Net Worth                                 │
Row 68-88:│  [Chart 7: Annual Bars]        [Chart 8: Net Worth Area]      │
          └────────────────────────────────────────────────────────────────┘
```

---

## ✨ Sparklines Added

| Location | Metric | Formula | Color |
|----------|--------|---------|-------|
| Dashboard!F2 | Header: "Trend" | — | Bold, centered |
| Dashboard!F3 | Total Revenue trend | `SPARKLINE(B21:B45)` | #6366F1 (Indigo) |
| Dashboard!F4 | Total Expenses trend | `SPARKLINE(C21:C45)` | #EF4444 (Red) |
| Dashboard!F5 | Net Profit trend | `SPARKLINE(D21:D45)` | #22C55E (Green) |
| Dashboard!F6 | Profit Margin trend | `SPARKLINE(E21:E45)` | #06B6D4 (Cyan) |
| Dashboard!F86 | Net Worth trend | `SPARKLINE({inline data})` | #22C55E (Green) |
| Dashboard!H99 | Debt Total trend | `SPARKLINE({inline data})` | #8B5CF6 (Purple) |

---

## 🎨 Styling Applied

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Indigo | #6366F1 | Revenue lines, primary series |
| Green | #22C55E | Profit, positive values, net worth |
| Red | #EF4444 | Expenses, losses, negative values |
| Cyan | #06B6D4 | Margins, Discover debt |
| Amber | #F59E0B | 50% target line, Sapphire debt |
| Purple | #8B5CF6 | Student loans, debt trend |

### Chart Formatting
- Title: Arial 14pt Bold
- Axis labels: Arial 10pt
- Legend: Bottom position (line/bar), Right position (pie)
- Line width: 3px (primary), 2px (secondary/debt), 4px (total debt)
- 50% target line: Medium dashed, amber
- Donut hole: 40% (expense chart)
- All charts: ~600×400px

### Tab Formatting
- Title bar: Navy (#1B2A4A) background, White 16pt Bold
- Section labels: Navy text, 11pt Bold
- Background: Light gray (#FAFAFA)

---

## 📝 Helper Data Created

| Location | Purpose | Content |
|----------|---------|---------|
| Charts!M1:P4 | Annual comparison (Chart 7) | Year, Revenue, Expenses, Net Profit for 2024/2025/2026 |
| Dashboard!G20:G45 | 50% target line (Chart 5) | Header + 25 rows of 0.5 |

---

## 📊 Data Ranges Reference

| Section | Header Row | Data Rows | Columns |
|---------|-----------|-----------|---------|
| Monthly Trend | Row 20 | 21–45 (25 months, Feb 2024 – Feb 2026) | A:G |
| Revenue by Business | Row 12 | 13–15 (3 lines) | A:F |
| Expense Categories | Row 50 | 51–56 (6 categories) | A:F |
| Net Worth | Row 86 | 87–95 (9 months, Jun 2025 – Feb 2026) | A:E |
| Debt Tracker | Row 99 | 100–108 (9 months, Jun 2025 – Feb 2026) | A:G |
| Executive Summary | Row 2 | 3–6 (4 metrics) | A:F |

---

## 🔗 Quick Links

- **Sheet:** https://docs.google.com/spreadsheets/d/1v1di5lJT-84iMD7FfnKGFfWanFV-5gyWXWR5mGJuJZQ
- **Charts Tab:** Navigate to "📈 Charts" tab
- **Script:** `/home/ec2-user/clawd/data/create_charts.py`
