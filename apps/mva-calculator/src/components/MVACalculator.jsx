import { useState, useEffect, useCallback } from 'react';

// Pricing data from Kurios Performance Sheet
const PRICING = {
  NC: { lead: 252, transfer: 1400, case: 3010 },
  NY: { lead: 315, transfer: 1715, case: 3640 },
  AZ: { lead: 315, transfer: 1715, case: 3640 },
  UT: { lead: 315, transfer: 1715, case: 3640 },
  TX: { lead: 378, transfer: 2030, case: 4270 },
  PA: { lead: 378, transfer: 2030, case: 4270 },
  NM: { lead: 378, transfer: 2030, case: 4270 },
  CA: { lead: 673, transfer: 3504, case: 7218 },
};

// Our costs (sell price / 1.4 for 30% margin)
const OUR_COSTS = {
  NC: { lead: 180, transfer: 1000, case: 2150 },
  NY: { lead: 225, transfer: 1225, case: 2600 },
  AZ: { lead: 225, transfer: 1225, case: 2600 },
  UT: { lead: 225, transfer: 1225, case: 2600 },
  TX: { lead: 270, transfer: 1450, case: 3050 },
  PA: { lead: 270, transfer: 1450, case: 3050 },
  NM: { lead: 270, transfer: 1450, case: 3050 },
  CA: { lead: 481, transfer: 2503, case: 5156 },
};

// Calculate averages for unmapped states
const calcAverage = (data, key) => {
  const values = Object.values(data).map(v => v[key]);
  return Math.round(values.reduce((a, b) => a + b, 0) / values.length);
};

const DEFAULT_PRICING = {
  lead: calcAverage(PRICING, 'lead'),
  transfer: calcAverage(PRICING, 'transfer'),
  case: calcAverage(PRICING, 'case'),
};

const DEFAULT_COSTS = {
  lead: calcAverage(OUR_COSTS, 'lead'),
  transfer: calcAverage(OUR_COSTS, 'transfer'),
  case: calcAverage(OUR_COSTS, 'case'),
};

// All US states
const ALL_STATES = [
  { code: 'DEFAULT', name: 'Average (All States)' },
  { code: 'AL', name: 'Alabama' },
  { code: 'AK', name: 'Alaska' },
  { code: 'AZ', name: 'Arizona' },
  { code: 'AR', name: 'Arkansas' },
  { code: 'CA', name: 'California' },
  { code: 'CO', name: 'Colorado' },
  { code: 'CT', name: 'Connecticut' },
  { code: 'DE', name: 'Delaware' },
  { code: 'FL', name: 'Florida' },
  { code: 'GA', name: 'Georgia' },
  { code: 'HI', name: 'Hawaii' },
  { code: 'ID', name: 'Idaho' },
  { code: 'IL', name: 'Illinois' },
  { code: 'IN', name: 'Indiana' },
  { code: 'IA', name: 'Iowa' },
  { code: 'KS', name: 'Kansas' },
  { code: 'KY', name: 'Kentucky' },
  { code: 'LA', name: 'Louisiana' },
  { code: 'ME', name: 'Maine' },
  { code: 'MD', name: 'Maryland' },
  { code: 'MA', name: 'Massachusetts' },
  { code: 'MI', name: 'Michigan' },
  { code: 'MN', name: 'Minnesota' },
  { code: 'MS', name: 'Mississippi' },
  { code: 'MO', name: 'Missouri' },
  { code: 'MT', name: 'Montana' },
  { code: 'NE', name: 'Nebraska' },
  { code: 'NV', name: 'Nevada' },
  { code: 'NH', name: 'New Hampshire' },
  { code: 'NJ', name: 'New Jersey' },
  { code: 'NM', name: 'New Mexico' },
  { code: 'NY', name: 'New York' },
  { code: 'NC', name: 'North Carolina' },
  { code: 'ND', name: 'North Dakota' },
  { code: 'OH', name: 'Ohio' },
  { code: 'OK', name: 'Oklahoma' },
  { code: 'OR', name: 'Oregon' },
  { code: 'PA', name: 'Pennsylvania' },
  { code: 'RI', name: 'Rhode Island' },
  { code: 'SC', name: 'South Carolina' },
  { code: 'SD', name: 'South Dakota' },
  { code: 'TN', name: 'Tennessee' },
  { code: 'TX', name: 'Texas' },
  { code: 'UT', name: 'Utah' },
  { code: 'VT', name: 'Vermont' },
  { code: 'VA', name: 'Virginia' },
  { code: 'WA', name: 'Washington' },
  { code: 'WV', name: 'West Virginia' },
  { code: 'WI', name: 'Wisconsin' },
  { code: 'WY', name: 'Wyoming' },
];

// ROI Constants
const AVG_SETTLEMENT = 30000;
const CONTINGENCY_RATE = 0.33;
const FIRM_REVENUE_PER_CASE = AVG_SETTLEMENT * CONTINGENCY_RATE; // $10,000

const SIGN_RATES = {
  lead: 0.10,      // 10% of leads become signed cases
  transfer: 0.50,  // 50% of transfers become signed cases
  case: 1.0,       // 100% (already signed)
};

// Analytics tracking hook (placeholder for future implementation)
const trackEvent = (eventName, data) => {
  // Will be implemented when analytics is added
  if (window.mvaAnalytics && typeof window.mvaAnalytics.track === 'function') {
    window.mvaAnalytics.track(eventName, data);
  }
  console.log('[MVA Analytics]', eventName, data);
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

const formatNumber = (num, decimals = 1) => {
  if (Number.isInteger(num)) return num.toString();
  return num.toFixed(decimals);
};

export default function MVACalculator({ embedded = false }) {
  const [offerType, setOfferType] = useState('lead');
  const [state, setState] = useState('CA');
  const [budget, setBudget] = useState(10000);
  const [showFormulas, setShowFormulas] = useState(false);

  const getPricing = useCallback((stateCode) => {
    return PRICING[stateCode] || DEFAULT_PRICING;
  }, []);

  const getCosts = useCallback((stateCode) => {
    return OUR_COSTS[stateCode] || DEFAULT_COSTS;
  }, []);

  // Get current prices
  const currentPricing = getPricing(state);
  const currentCosts = getCosts(state);
  const sellPrice = currentPricing[offerType];
  const ourCost = currentCosts[offerType];
  
  // Calculate guaranteed quantity
  const guaranteedQty = budget / sellPrice;
  const signRate = SIGN_RATES[offerType];
  const expectedSignedCases = guaranteedQty * signRate;
  const expectedRevenue = expectedSignedCases * FIRM_REVENUE_PER_CASE;
  const totalCost = guaranteedQty * ourCost;
  const profit = budget - totalCost;
  const margin = budget > 0 ? ((profit / budget) * 100) : 0;
  const clientROI = budget > 0 ? (((expectedRevenue - budget) / budget) * 100) : 0;

  // Track calculation changes
  useEffect(() => {
    trackEvent('calculation_updated', {
      offerType,
      state,
      budget,
      guaranteedQty,
      expectedRevenue,
    });
  }, [offerType, state, budget, guaranteedQty, expectedRevenue]);

  const offerLabels = {
    lead: 'Guaranteed Leads',
    transfer: 'Live Transfers',
    case: 'Signed Cases',
  };

  const containerClass = embedded 
    ? 'mva-widget p-4' 
    : 'min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4 md:p-8';

  return (
    <div className={containerClass}>
      <div className={`max-w-4xl mx-auto ${!embedded && 'pt-8'}`}>
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">
            MVA Calculator
          </h1>
          <p className="text-blue-200 text-lg">
            Motor Vehicle Accident Lead Pricing & ROI Calculator
          </p>
        </div>

        {/* Main Calculator Card */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 md:p-8 border border-white/20 shadow-2xl">
          {/* Input Section */}
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {/* Offer Type */}
            <div>
              <label className="block text-blue-200 text-sm font-medium mb-2">
                Offer Type
              </label>
              <select
                value={offerType}
                onChange={(e) => {
                  setOfferType(e.target.value);
                  trackEvent('offer_type_changed', { offerType: e.target.value });
                }}
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none cursor-pointer"
              >
                <option value="lead" className="bg-slate-800">Guaranteed Leads</option>
                <option value="transfer" className="bg-slate-800">Live Transfers</option>
                <option value="case" className="bg-slate-800">Signed Cases</option>
              </select>
            </div>

            {/* State */}
            <div>
              <label className="block text-blue-200 text-sm font-medium mb-2">
                State
              </label>
              <select
                value={state}
                onChange={(e) => {
                  setState(e.target.value);
                  trackEvent('state_changed', { state: e.target.value });
                }}
                className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent appearance-none cursor-pointer"
              >
                {ALL_STATES.map(s => (
                  <option key={s.code} value={s.code} className="bg-slate-800">
                    {s.name} {PRICING[s.code] ? '' : '(Avg)'}
                  </option>
                ))}
              </select>
            </div>

            {/* Budget */}
            <div>
              <label className="block text-blue-200 text-sm font-medium mb-2">
                Budget
              </label>
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-white/60">$</span>
                <input
                  type="number"
                  value={budget}
                  onChange={(e) => setBudget(Math.max(0, parseFloat(e.target.value) || 0))}
                  className="w-full bg-white/10 border border-white/20 rounded-lg pl-8 pr-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  min="0"
                  step="100"
                />
              </div>
            </div>
          </div>

          {/* Results Grid */}
          <div className="grid md:grid-cols-2 gap-6 mb-8">
            {/* Guaranteed Delivery Card */}
            <div className="bg-gradient-to-br from-blue-600/30 to-blue-800/30 rounded-xl p-6 border border-blue-400/30">
              <h3 className="text-blue-200 text-sm font-medium uppercase tracking-wide mb-4">
                Client Gets (Guaranteed)
              </h3>
              <div className="flex items-end justify-between">
                <div>
                  <p className="text-5xl font-bold text-white">
                    {formatNumber(guaranteedQty)}
                  </p>
                  <p className="text-blue-200 mt-1">{offerLabels[offerType]}</p>
                </div>
                <div className="text-right">
                  <p className="text-lg text-blue-200">@ {formatCurrency(sellPrice)} each</p>
                </div>
              </div>
            </div>

            {/* Kurios Margin Card */}
            <div className="bg-gradient-to-br from-emerald-600/30 to-emerald-800/30 rounded-xl p-6 border border-emerald-400/30">
              <h3 className="text-emerald-200 text-sm font-medium uppercase tracking-wide mb-4">
                Kurios Profitability
              </h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-emerald-200">Revenue:</span>
                  <span className="text-white font-semibold">{formatCurrency(budget)}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-emerald-200">Our Cost:</span>
                  <span className="text-white font-semibold">-{formatCurrency(totalCost)}</span>
                </div>
                <div className="border-t border-emerald-400/30 pt-2 flex justify-between items-center">
                  <span className="text-emerald-200">Profit:</span>
                  <span className={`text-2xl font-bold ${profit >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                    {formatCurrency(profit)}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-emerald-200">Margin:</span>
                  <span className={`font-semibold ${margin >= 30 ? 'text-emerald-400' : 'text-yellow-400'}`}>
                    {margin.toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Client ROI Section */}
          <div className="bg-gradient-to-br from-purple-600/30 to-purple-800/30 rounded-xl p-6 border border-purple-400/30 mb-8">
            <h3 className="text-purple-200 text-sm font-medium uppercase tracking-wide mb-4">
              Client ROI Projection
            </h3>
            <div className="grid md:grid-cols-4 gap-4">
              <div className="text-center">
                <p className="text-3xl font-bold text-white">{formatNumber(guaranteedQty)}</p>
                <p className="text-purple-200 text-sm">{offerLabels[offerType]}</p>
              </div>
              <div className="text-center flex items-center justify-center">
                <div>
                  <p className="text-purple-200">×</p>
                  <p className="text-white font-semibold">{(signRate * 100).toFixed(0)}% sign rate</p>
                </div>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-white">{formatNumber(expectedSignedCases)}</p>
                <p className="text-purple-200 text-sm">Signed Cases</p>
              </div>
              <div className="text-center">
                <p className="text-3xl font-bold text-emerald-400">{formatCurrency(expectedRevenue)}</p>
                <p className="text-purple-200 text-sm">Firm Revenue</p>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-purple-400/30 flex flex-wrap justify-between items-center gap-4">
              <div className="text-purple-200 text-sm">
                Based on {formatCurrency(AVG_SETTLEMENT)} avg settlement × {(CONTINGENCY_RATE * 100).toFixed(0)}% contingency = {formatCurrency(FIRM_REVENUE_PER_CASE)}/case
              </div>
              <div className="text-right">
                <span className="text-purple-200 mr-2">Client ROI:</span>
                <span className={`text-2xl font-bold ${clientROI >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                  {clientROI.toFixed(0)}%
                </span>
              </div>
            </div>
          </div>

          {/* Formula Toggle */}
          <button
            onClick={() => setShowFormulas(!showFormulas)}
            className="w-full text-center text-blue-300 hover:text-blue-100 text-sm py-2 transition-colors"
          >
            {showFormulas ? '▼ Hide Formulas' : '▶ Show Formulas & Pricing Breakdown'}
          </button>

          {/* Formulas Section */}
          {showFormulas && (
            <div className="mt-6 space-y-6">
              {/* Pricing Table */}
              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-600/30">
                <h4 className="text-white font-semibold mb-4">State Pricing Reference</h4>
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-slate-400 border-b border-slate-600">
                        <th className="text-left py-2 px-3">State</th>
                        <th className="text-right py-2 px-3">Lead</th>
                        <th className="text-right py-2 px-3">Transfer</th>
                        <th className="text-right py-2 px-3">Case</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(PRICING).map(([code, prices]) => (
                        <tr key={code} className={`border-b border-slate-700/50 ${state === code ? 'bg-blue-600/20' : ''}`}>
                          <td className="py-2 px-3 text-white font-medium">{code}</td>
                          <td className="py-2 px-3 text-right text-slate-300">{formatCurrency(prices.lead)}</td>
                          <td className="py-2 px-3 text-right text-slate-300">{formatCurrency(prices.transfer)}</td>
                          <td className="py-2 px-3 text-right text-slate-300">{formatCurrency(prices.case)}</td>
                        </tr>
                      ))}
                      <tr className="border-b border-slate-700/50 bg-slate-700/30">
                        <td className="py-2 px-3 text-white font-medium">Default (Avg)</td>
                        <td className="py-2 px-3 text-right text-slate-300">{formatCurrency(DEFAULT_PRICING.lead)}</td>
                        <td className="py-2 px-3 text-right text-slate-300">{formatCurrency(DEFAULT_PRICING.transfer)}</td>
                        <td className="py-2 px-3 text-right text-slate-300">{formatCurrency(DEFAULT_PRICING.case)}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Formulas */}
              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-600/30">
                <h4 className="text-white font-semibold mb-4">Calculation Formulas</h4>
                <div className="space-y-4 font-mono text-sm">
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 mb-1">Guaranteed Quantity:</p>
                    <p className="text-blue-300">
                      {formatCurrency(budget)} ÷ {formatCurrency(sellPrice)} = <span className="text-white font-bold">{formatNumber(guaranteedQty, 2)} {offerLabels[offerType]}</span>
                    </p>
                  </div>
                  
                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 mb-1">Our Cost (Break-even threshold @ 30% margin):</p>
                    <p className="text-emerald-300">
                      {formatCurrency(sellPrice)} ÷ 1.4 = <span className="text-white font-bold">{formatCurrency(ourCost)}/unit</span>
                    </p>
                    <p className="text-slate-400 mt-2 text-xs">
                      If we pay more than {formatCurrency(ourCost)} per {offerType}, we lose money.
                    </p>
                  </div>

                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 mb-1">Expected Signed Cases:</p>
                    <p className="text-purple-300">
                      {formatNumber(guaranteedQty, 2)} × {(signRate * 100)}% sign rate = <span className="text-white font-bold">{formatNumber(expectedSignedCases, 2)} cases</span>
                    </p>
                  </div>

                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 mb-1">Client Revenue:</p>
                    <p className="text-purple-300">
                      {formatNumber(expectedSignedCases, 2)} cases × {formatCurrency(FIRM_REVENUE_PER_CASE)} = <span className="text-white font-bold">{formatCurrency(expectedRevenue)}</span>
                    </p>
                    <p className="text-slate-400 mt-2 text-xs">
                      Based on {formatCurrency(AVG_SETTLEMENT)} avg settlement × {(CONTINGENCY_RATE * 100)}% contingency
                    </p>
                  </div>

                  <div className="bg-slate-900/50 rounded-lg p-4">
                    <p className="text-slate-400 mb-1">Client ROI:</p>
                    <p className="text-emerald-300">
                      ({formatCurrency(expectedRevenue)} - {formatCurrency(budget)}) ÷ {formatCurrency(budget)} × 100 = <span className="text-white font-bold">{clientROI.toFixed(1)}%</span>
                    </p>
                  </div>
                </div>
              </div>

              {/* Sign Rate Assumptions */}
              <div className="bg-slate-800/50 rounded-xl p-6 border border-slate-600/30">
                <h4 className="text-white font-semibold mb-4">Sign Rate Assumptions</h4>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="text-center p-4 bg-slate-900/50 rounded-lg">
                    <p className="text-2xl font-bold text-white">10%</p>
                    <p className="text-slate-400 text-sm">Leads → Signed Cases</p>
                  </div>
                  <div className="text-center p-4 bg-slate-900/50 rounded-lg">
                    <p className="text-2xl font-bold text-white">50%</p>
                    <p className="text-slate-400 text-sm">Transfers → Signed Cases</p>
                  </div>
                  <div className="text-center p-4 bg-slate-900/50 rounded-lg">
                    <p className="text-2xl font-bold text-white">100%</p>
                    <p className="text-slate-400 text-sm">Cases (already signed)</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        {!embedded && (
          <div className="text-center mt-8 text-slate-400 text-sm">
            <p>Kurios MVA Calculator • Pricing as of 2024</p>
          </div>
        )}
      </div>
    </div>
  );
}
