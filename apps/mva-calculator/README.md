# MVA Calculator

Motor Vehicle Accident Lead Pricing & ROI Calculator for Kurios.

## Features

- **State-based Pricing**: Different prices for NC, NY/AZ/UT, TX/PA/NM, CA, and default averages
- **Three Offer Types**: Guaranteed Leads, Live Transfers, Signed Cases
- **Kurios Profitability**: Shows cost, profit, and margin calculations
- **Client ROI Projection**: Expected signed cases and firm revenue based on sign rates
- **Formula Transparency**: Expandable section showing all calculations
- **Embeddable Widget**: Can be embedded in any webpage

## Pricing Data

| State(s) | Lead | Transfer | Case |
|----------|------|----------|------|
| NC | $252 | $1,400 | $3,010 |
| NY/AZ/UT | $315 | $1,715 | $3,640 |
| TX/PA/NM | $378 | $2,030 | $4,270 |
| CA | $673 | $3,504 | $7,218 |
| Default | Avg | Avg | Avg |

## Sign Rate Assumptions

- Leads → Signed Cases: 10%
- Live Transfers → Signed Cases: 50%
- Signed Cases: 100% (already signed)

## ROI Assumptions

- Average Settlement: $30,000
- Contingency Fee: 33%
- Firm Revenue per Case: $10,000

## Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build standalone app
npm run build

# Build embeddable widget
npm run build:widget

# Build both
npm run build:all
```

## Widget Embedding

```html
<!-- Include CSS and JS -->
<link rel="stylesheet" href="mva-widget.css">
<script src="mva-widget.umd.js"></script>

<!-- Container -->
<div id="mva-calculator"></div>

<!-- Initialize -->
<script>
  MVACalculatorWidget.default.init('#mva-calculator', {
    embedded: true
  });
</script>
```

## Analytics

The calculator includes analytics hooks. Set up `window.mvaAnalytics.track(eventName, data)` to receive:

- `calculation_updated`: When any calculation changes
- `offer_type_changed`: When offer type is changed
- `state_changed`: When state is selected

## Build Output

- `dist/` - Standalone app (deploy as static site)
- `dist-widget/` - Embeddable widget files
  - `mva-widget.css` - Styles
  - `mva-widget.umd.js` - UMD bundle
  - `mva-widget.es.js` - ES module bundle
