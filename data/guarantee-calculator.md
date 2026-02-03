# Guarantee Calculator Logic

## Inputs
- **Offer Type:** Leads | Live Transfers | Signed Cases
- **State:** CA, TX, FL, GA, PA, NC, NY, etc.
- **Budget:** $15k - $100k+

## State Cost Data (Our Costs)
| State | Lead Cost | Transfer Cost | Case Cost | Conversion |
|-------|-----------|---------------|-----------|------------|
| CA | $350 | $450 | $3,500 | 10% |
| TX | $250 | $350 | $2,000 | 15% |
| FL | $250 | $350 | $2,200 | 12% |
| GA | $275 | $375 | $2,000 | 15% |
| PA | $300 | $400 | $2,000 | 15% |
| NC | $200 | $300 | $1,500 | 15% |
| NY | $250 | $350 | $2,000 | 15% |
| MI | $200 | $300 | $1,500 | 15% |
| National | $125 | $225 | $1,200 | 15% |

## Calculation Formulas

### LEADS
```
Guaranteed Leads = Budget / Lead Cost
Our Cost = Lead Cost per lead
Our Margin = Client Pays - Our Cost
Break-even Leads = Budget / Our Cost
"In Trouble" Number = Break-even Leads - (Margin Buffer)
```

### LIVE TRANSFERS
```
Leads Generated = Budget × 0.7 / Lead Cost  (70% to media, 30% margin)
Expected Transfers = Leads × 0.35 (35% transfer rate)
Guaranteed Transfers = Expected Transfers × 0.85 (15% safety buffer)
Transfer Cost = Lead Cost + $100
"In Trouble" Number = (Budget × 0.7) / Transfer Cost
```

### SIGNED CASES
```
Leads Generated = Budget × 0.7 / Lead Cost
Expected Cases = Leads × Conversion Rate
Guaranteed Cases = Expected Cases × 0.85 (15% safety buffer)
Case Cost = Lead Cost / Conversion + $350
"In Trouble" Number = (Budget × 0.7) / Case Cost
```

## Guarantee Tiers

### $30k Budget (Minimum for Guarantees)
| State | Leads | Transfers | Cases |
|-------|-------|-----------|-------|
| CA | 60-75 | 18-22 | 5-7 |
| TX | 85-100 | 28-35 | 9-12 |
| FL | 85-100 | 25-32 | 8-10 |
| NC/MI | 105-125 | 35-42 | 12-15 |

### $50k Budget
| State | Leads | Transfers | Cases |
|-------|-------|-----------|-------|
| CA | 100-120 | 30-38 | 10-12 |
| TX | 140-170 | 45-55 | 17-22 |
| FL | 140-170 | 42-52 | 15-19 |
| NC/MI | 175-210 | 55-68 | 22-28 |

### $100k Budget
| State | Leads | Transfers | Cases |
|-------|-------|-----------|-------|
| CA | 200-250 | 65-80 | 20-25 |
| TX | 280-350 | 95-115 | 35-45 |
| FL | 280-350 | 85-105 | 30-38 |
| NC/MI | 350-450 | 115-140 | 45-55 |

## "In Trouble" Thresholds (When to Worry)

The "in trouble" number is when delivered results fall below break-even considering our profit margin is used to make up the difference.

### Formula:
```
Max Replacement Budget = Expected Margin
Replacement Units = Max Replacement Budget / Unit Cost
In Trouble Threshold = Guaranteed - Replacement Units
```

### Example ($30k TX Campaign - Signed Cases):
- Budget: $30,000
- Our margin: 30% = $9,000
- Expected cases: 12
- Guaranteed: 10
- Case cost to us: $2,000
- Max replacement: $9,000 / $2,000 = 4.5 cases
- **In Trouble if under: 10 - 4.5 = 5.5 cases**

If we deliver less than 6 cases, we're losing money even after using our profit to replace.

## Pricing to Client (30% Margin)

| Our Cost | Client Pays | Our Margin |
|----------|-------------|------------|
| $200/lead | $260-285/lead | $60-85 |
| $300/transfer | $390-420/transfer | $90-120 |
| $2,000/case | $2,600-2,800/case | $600-800 |

## Small Budget (<$30k) - No Guarantees
- Sell leads only at marked-up price
- Outsourced intake sold separately:
  - $200 per live transfer
  - $450 per signed case
  - Minimum: batch of 5 up front ($1,000 or $2,250)
