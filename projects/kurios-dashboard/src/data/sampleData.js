// Kurios Dashboard - Marko's Real Data
// Goal: $9.6M exit by end of 2026, then retire to music

export const GOAL = {
  total: 9600000,
  deadline: '2026-12-31',
  margin: 0.30, // Kurios's 30% margin
  currentYear: 2024,
};

// Real Prospects Pipeline
export const initialDeals = [
  { 
    id: 'd1', 
    name: 'Scott Barney', 
    company: 'VA Beach Firm',
    value: 75000, 
    kuriosMargin: 22500,
    stage: 'qualified', 
    contact: 'Scott Barney', 
    state: 'VA', 
    createdAt: '2024-01-20',
    probability: 70,
    priority: 'high',
    notes: 'Burned $250k with other vendors. HIGH PRIORITY - ready to spend.',
    nextAction: 'Follow up call',
    lastContact: '2024-01-28'
  },
  { 
    id: 'd2', 
    name: 'Ross Robin', 
    company: 'New PI Firm',
    value: 40000, 
    kuriosMargin: 12000,
    stage: 'qualified', 
    contact: 'Ross Robin', 
    state: 'FL', 
    createdAt: '2024-01-22',
    probability: 65,
    priority: 'high',
    notes: 'New PI firm, hungry for cases. HIGH PRIORITY.',
    nextAction: 'Send proposal',
    lastContact: '2024-01-27'
  },
  { 
    id: 'd3', 
    name: 'Jalal Abdallah', 
    company: 'Multi-State Practice',
    value: 50000, 
    kuriosMargin: 15000,
    stage: 'negotiation', 
    contact: 'Jalal Abdallah', 
    state: 'TX', 
    createdAt: '2024-01-15',
    probability: 85,
    priority: 'high',
    notes: '$50k multi-state campaign. VERBAL COMMIT.',
    nextAction: 'Send contract',
    lastContact: '2024-01-26'
  },
  { 
    id: 'd4', 
    name: 'Omeed H.', 
    company: 'CA Practice',
    value: 50000, 
    kuriosMargin: 15000,
    stage: 'proposal', 
    contact: 'Omeed H.', 
    state: 'CA', 
    createdAt: '2024-01-18',
    probability: 55,
    priority: 'medium',
    notes: '$50k campaign interest. California market.',
    nextAction: 'Proposal review call',
    lastContact: '2024-01-25'
  },
  { 
    id: 'd5', 
    name: 'Rich Hyde', 
    company: 'Trial Tribe',
    value: 35000, 
    kuriosMargin: 10500,
    stage: 'qualified', 
    contact: 'Rich Hyde', 
    state: 'TX', 
    createdAt: '2024-01-20',
    probability: 50,
    priority: 'medium',
    notes: 'Wants reliable vendor. Had bad experiences before.',
    nextAction: 'Case study presentation',
    lastContact: '2024-01-24'
  },
  { 
    id: 'd6', 
    name: 'Lucas Naccarati', 
    company: 'Muniz Kim Law',
    value: 60000, 
    kuriosMargin: 18000,
    stage: 'lead', 
    contact: 'Lucas Naccarati', 
    state: 'FL', 
    createdAt: '2024-01-23',
    probability: 35,
    priority: 'medium',
    notes: 'Looking for scalable acquisition. Big potential.',
    nextAction: 'Discovery call',
    lastContact: '2024-01-23'
  },
  { 
    id: 'd7', 
    name: 'Dagmawi G.', 
    company: 'DG Firm',
    value: 15000, 
    kuriosMargin: 4500,
    stage: 'lead', 
    contact: 'Dagmawi G.', 
    state: 'GA', 
    createdAt: '2024-01-25',
    probability: 40,
    priority: 'low',
    notes: 'Wants small test first. Good entry point.',
    nextAction: 'Intro call',
    lastContact: '2024-01-25'
  },
  { 
    id: 'd8', 
    name: 'Daniel Ramirez', 
    company: 'Dallas/Houston Practice',
    value: 45000, 
    kuriosMargin: 13500,
    stage: 'qualified', 
    contact: 'Daniel Ramirez', 
    state: 'TX', 
    createdAt: '2024-01-19',
    probability: 55,
    priority: 'medium',
    notes: 'Dallas→Houston expansion. Spanish markets focus.',
    nextAction: 'Market analysis presentation',
    lastContact: '2024-01-26'
  },
  { 
    id: 'd9', 
    name: 'Josh Sweeney', 
    company: 'Shane Smith Law',
    value: 30000, 
    kuriosMargin: 9000,
    stage: 'lead', 
    contact: 'Josh Sweeney', 
    state: 'TX', 
    createdAt: '2024-01-24',
    probability: 30,
    priority: 'low',
    notes: 'YouTube/TikTok interest. Social media angle.',
    nextAction: 'Content strategy call',
    lastContact: '2024-01-24'
  },
  { 
    id: 'd10', 
    name: 'Michael Shirts', 
    company: 'BS Injury Law',
    value: 55000, 
    kuriosMargin: 16500,
    stage: 'qualified', 
    contact: 'Michael Shirts', 
    state: 'NV', 
    createdAt: '2024-01-17',
    probability: 50,
    priority: 'medium',
    notes: 'Vegas market. Good conversion rates there.',
    nextAction: 'Proposal call',
    lastContact: '2024-01-22'
  },
  { 
    id: 'd11', 
    name: 'Michael Schulz', 
    company: 'RMD Law',
    value: 40000, 
    kuriosMargin: 12000,
    stage: 'lead', 
    contact: 'Michael Schulz', 
    state: 'CA', 
    createdAt: '2024-01-21',
    probability: 25,
    priority: 'medium',
    notes: 'Follow up 02/10. Set reminder.',
    nextAction: 'Follow up Feb 10',
    lastContact: '2024-01-21'
  },
  { 
    id: 'd12', 
    name: 'Joan Suh', 
    company: 'Suh & Associates',
    value: 35000, 
    kuriosMargin: 10500,
    stage: 'qualified', 
    contact: 'Joan Suh', 
    state: 'CA', 
    createdAt: '2024-01-26',
    probability: 60,
    priority: 'high',
    notes: 'Call scheduled. Ready to move.',
    nextAction: 'Scheduled call',
    lastContact: '2024-01-28'
  },
  // CLOSED DEAL
  { 
    id: 'd13', 
    name: 'Jason E.', 
    company: 'Jason E. Law',
    value: 31750, 
    kuriosMargin: 9525,
    stage: 'closed', 
    contact: 'Jason E.', 
    state: 'TX', 
    createdAt: '2024-01-10',
    probability: 100,
    priority: 'closed',
    notes: 'FIRST CLOSED DEAL! $31,750 total, $9,525 margin.',
    nextAction: 'Deliver results',
    lastContact: '2024-01-15'
  },
];

export const pipelineStages = [
  { id: 'lead', name: 'Lead', color: '#6366f1' },
  { id: 'qualified', name: 'Qualified', color: '#8b5cf6' },
  { id: 'proposal', name: 'Proposal', color: '#3366FF' },
  { id: 'negotiation', name: 'Negotiation', color: '#f59e0b' },
  { id: 'closed', name: 'Closed Won', color: '#00E676' },
];

// Real Client Data by State (from Google Sheet)
export const initialClients = [
  // Texas - 3 clients
  { id: 'c1', name: 'TX Client 1', state: 'TX', revenue: 2000, caseValue: '$1,700-2,000/case', conversion: 15, industry: 'MVA', status: 'active', startDate: '2023-10-15', casesPerMonth: 12, notes: 'Consistent performer' },
  { id: 'c2', name: 'TX Client 2', state: 'TX', revenue: 1800, caseValue: '$1,800/case', conversion: 14, industry: 'MVA', status: 'active', startDate: '2023-11-01', casesPerMonth: 10, notes: 'Growing account' },
  { id: 'c3', name: 'TX Client 3', state: 'TX', revenue: 1700, caseValue: '$1,700/case', conversion: 16, industry: 'MVA', status: 'active', startDate: '2023-12-01', casesPerMonth: 8, notes: 'New but solid' },
  // Florida - Strong market
  { id: 'c4', name: 'FL Client 1', state: 'FL', revenue: 2000, caseValue: '$1,200-2,000/case', conversion: 25, industry: 'MVA', status: 'active', startDate: '2023-09-01', casesPerMonth: 35, notes: '30+ cases/mo consistently' },
  { id: 'c5', name: 'FL Client 2', state: 'FL', revenue: 1500, caseValue: '$1,500/case', conversion: 22, industry: 'MVA', status: 'active', startDate: '2023-10-15', casesPerMonth: 28, notes: 'Scaling up' },
  // California - Highest costs but $4M+ spend
  { id: 'c6', name: 'CA Client 1', state: 'CA', revenue: 4500, caseValue: '$3,500-4,500/case', conversion: 12, industry: 'MVA', status: 'active', startDate: '2023-06-01', casesPerMonth: 20, notes: '$4M+ total spend capacity' },
  { id: 'c7', name: 'CA Client 2', state: 'CA', revenue: 3800, caseValue: '$3,800/case', conversion: 10, industry: 'MVA', status: 'active', startDate: '2023-08-01', casesPerMonth: 15, notes: 'Premium market' },
  // Georgia - Strong conversion
  { id: 'c8', name: 'GA Client 1', state: 'GA', revenue: 1800, caseValue: '$1,800/case', conversion: 20, industry: 'MVA', status: 'active', startDate: '2023-09-15', casesPerMonth: 18, notes: '15-25% conversion' },
  { id: 'c9', name: 'GA Client 2', state: 'GA', revenue: 1600, caseValue: '$1,600/case', conversion: 25, industry: 'MVA', status: 'active', startDate: '2023-11-01', casesPerMonth: 14, notes: 'Strong market' },
  // Nevada
  { id: 'c10', name: 'NV Client 1', state: 'NV', revenue: 2200, caseValue: '$2,200/case', conversion: 18, industry: 'MVA', status: 'active', startDate: '2023-10-01', casesPerMonth: 12, notes: 'Vegas market solid' },
  // Arizona
  { id: 'c11', name: 'AZ Client 1', state: 'AZ', revenue: 1900, caseValue: '$1,900/case', conversion: 16, industry: 'MVA', status: 'active', startDate: '2023-11-15', casesPerMonth: 10, notes: 'Growing' },
  // New York
  { id: 'c12', name: 'NY Client 1', state: 'NY', revenue: 3200, caseValue: '$3,200/case', conversion: 14, industry: 'MVA', status: 'active', startDate: '2023-07-01', casesPerMonth: 16, notes: 'High value market' },
  // Others
  { id: 'c13', name: 'CO Client 1', state: 'CO', revenue: 1700, caseValue: '$1,700/case', conversion: 17, industry: 'MVA', status: 'active', startDate: '2023-10-01', casesPerMonth: 8, notes: 'Steady' },
  { id: 'c14', name: 'VA Client 1', state: 'VA', revenue: 1800, caseValue: '$1,800/case', conversion: 15, industry: 'MVA', status: 'active', startDate: '2023-12-01', casesPerMonth: 6, notes: 'New market' },
];

// Partners & Key Contacts
export const initialContacts = [
  // Partners
  { id: 'ct1', name: 'Patrick', email: 'patrick@inquiredesquire.com', phone: '', company: 'Inquired Esquire', role: 'Partner - Intake', type: 'partner', notes: 'Handles intake. Patrick Pipeline deals.' },
  { id: 'ct2', name: 'Max', email: 'max@casesondemand.com', phone: '', company: 'Cases on Demand', role: 'Partner', type: 'partner', notes: 'Cases on Demand partnership.' },
  { id: 'ct3', name: 'Jeremy', email: 'jeremy@casesondemand.com', phone: '', company: 'Cases on Demand', role: 'Partner', type: 'partner', notes: 'Cases on Demand partnership.' },
  // Prospects (quick access)
  { id: 'ct4', name: 'Scott Barney', email: '', phone: '', company: 'VA Beach Firm', role: 'Owner', type: 'prospect', notes: 'HIGH PRIORITY - Burned $250k elsewhere' },
  { id: 'ct5', name: 'Ross Robin', email: '', phone: '', company: 'New PI Firm', role: 'Owner', type: 'prospect', notes: 'HIGH PRIORITY - New firm, hungry' },
  { id: 'ct6', name: 'Jalal Abdallah', email: '', phone: '', company: 'Multi-State', role: 'Owner', type: 'prospect', notes: 'VERBAL COMMIT - $50k multi-state' },
  { id: 'ct7', name: 'Joan Suh', email: '', phone: '', company: 'Suh & Associates', role: 'Owner', type: 'prospect', notes: 'Call scheduled - ready to move' },
  // Client contacts
  { id: 'ct8', name: 'Jason E.', email: '', phone: '', company: 'Jason E. Law', role: 'Owner', type: 'client', notes: 'FIRST CLOSED DEAL - $31,750' },
];

// Projects
export const initialProjects = [
  { 
    id: 'p1', 
    name: 'MVA Lead Gen System', 
    status: 'in_progress', 
    progress: 75,
    dueDate: '2024-02-15',
    description: 'Build automated MVA lead generation for PI lawyers',
    client: 'Kurios/Cases on Demand',
    tasks: [
      { id: 't1', name: 'Landing page templates', completed: true },
      { id: 't2', name: 'Google Ads campaigns', completed: true },
      { id: 't3', name: 'Lead routing to Patrick', completed: true },
      { id: 't4', name: 'CRM integration', completed: false },
      { id: 't5', name: 'Reporting dashboard', completed: false },
    ]
  },
  { 
    id: 'p2', 
    name: 'State Expansion - Q1', 
    status: 'in_progress', 
    progress: 40,
    dueDate: '2024-03-31',
    description: 'Expand to 5 new states this quarter',
    client: 'Internal',
    tasks: [
      { id: 't6', name: 'Virginia market research', completed: true },
      { id: 't7', name: 'Nevada setup', completed: true },
      { id: 't8', name: 'New York campaigns', completed: false },
      { id: 't9', name: 'Arizona expansion', completed: false },
      { id: 't10', name: 'Colorado optimization', completed: false },
    ]
  },
  { 
    id: 'p3', 
    name: 'Sales Process Optimization', 
    status: 'in_progress', 
    progress: 60,
    dueDate: '2024-02-28',
    description: 'Get to 2-3 calls/day at <$100-150/call',
    client: 'Internal',
    tasks: [
      { id: 't11', name: 'Call booking automation', completed: true },
      { id: 't12', name: 'Lead qualification criteria', completed: true },
      { id: 't13', name: 'Sales script optimization', completed: true },
      { id: 't14', name: 'Cost per call tracking', completed: false },
      { id: 't15', name: 'A/B test outreach', completed: false },
    ]
  },
];

// Ideas Backlog
export const initialIdeas = [
  { id: 'i1', title: 'YouTube/TikTok Content', description: 'Authority content for PI lawyers. Josh Sweeney interested.', priority: 'high', status: 'backlog', votes: 5, createdAt: '2024-01-20' },
  { id: 'i2', title: 'Spanish Market Campaigns', description: 'Daniel Ramirez interested. Houston Spanish-speaking market.', priority: 'high', status: 'in_review', votes: 7, createdAt: '2024-01-18' },
  { id: 'i3', title: 'White Label for Partners', description: 'Let partners resell under their brand.', priority: 'medium', status: 'backlog', votes: 4, createdAt: '2024-01-15' },
  { id: 'i4', title: 'Case Study Library', description: 'Build authority with documented wins.', priority: 'high', status: 'approved', votes: 8, createdAt: '2024-01-10' },
  { id: 'i5', title: 'Retargeting Sequences', description: 'Follow up with unconverted leads.', priority: 'medium', status: 'backlog', votes: 3, createdAt: '2024-01-08' },
];

// Call tracking data
export const callData = {
  today: 2,
  thisWeek: 8,
  target: { daily: 3, weekly: 15 },
  avgCostPerCall: 125,
  targetCostPerCall: 150,
  conversionRate: 25, // % of calls that close
};

// Revenue tracking (Kurios 30% margin)
export const revenueData = [
  { month: 'Jan', deals: 31750, margin: 9525, calls: 12, closedDeals: 1 },
  { month: 'Feb', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Mar', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Apr', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'May', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Jun', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Jul', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Aug', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Sep', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Oct', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Nov', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
  { month: 'Dec', deals: 0, margin: 0, calls: 0, closedDeals: 0 },
];

// State performance data
export const stateData = [
  { state: 'TX', clients: 3, avgCaseValue: 1833, conversion: 15, casesPerMonth: 30, totalSpend: 55000 },
  { state: 'FL', clients: 2, avgCaseValue: 1750, conversion: 24, casesPerMonth: 63, totalSpend: 110000 },
  { state: 'CA', clients: 2, avgCaseValue: 4150, conversion: 11, casesPerMonth: 35, totalSpend: 145000 },
  { state: 'GA', clients: 2, avgCaseValue: 1700, conversion: 23, casesPerMonth: 32, totalSpend: 54000 },
  { state: 'NV', clients: 1, avgCaseValue: 2200, conversion: 18, casesPerMonth: 12, totalSpend: 26000 },
  { state: 'AZ', clients: 1, avgCaseValue: 1900, conversion: 16, casesPerMonth: 10, totalSpend: 19000 },
  { state: 'NY', clients: 1, avgCaseValue: 3200, conversion: 14, casesPerMonth: 16, totalSpend: 51000 },
  { state: 'CO', clients: 1, avgCaseValue: 1700, conversion: 17, casesPerMonth: 8, totalSpend: 14000 },
  { state: 'VA', clients: 1, avgCaseValue: 1800, conversion: 15, casesPerMonth: 6, totalSpend: 11000 },
];

// Milestones to $9.6M
export const milestones = [
  { amount: 100000, label: '$100K', achieved: false },
  { amount: 500000, label: '$500K', achieved: false },
  { amount: 1000000, label: '$1M', achieved: false },
  { amount: 2500000, label: '$2.5M', achieved: false },
  { amount: 5000000, label: '$5M', achieved: false },
  { amount: 7500000, label: '$7.5M', achieved: false },
  { amount: 9600000, label: '$9.6M 🎵', achieved: false },
];

// Activity feed
export const activityFeed = [
  { id: 'a1', type: 'deal', message: 'Jason E. CLOSED - First deal! $31,750', timestamp: '2024-01-15T14:30:00Z', icon: 'check-circle' },
  { id: 'a2', type: 'call', message: 'Call with Joan Suh scheduled', timestamp: '2024-01-28T12:15:00Z', icon: 'phone' },
  { id: 'a3', type: 'deal', message: 'Jalal Abdallah verbal commit - $50k', timestamp: '2024-01-26T10:00:00Z', icon: 'trending-up' },
  { id: 'a4', type: 'lead', message: 'New lead: Lucas Naccarati (Muniz Kim)', timestamp: '2024-01-23T16:45:00Z', icon: 'plus' },
  { id: 'a5', type: 'call', message: 'Scott Barney follow-up needed', timestamp: '2024-01-28T14:20:00Z', icon: 'alert-circle' },
];

// Settings with dark mode default
export const settings = {
  profile: {
    name: 'Marko',
    email: 'mark@kuriosbrand.com',
    role: 'Founder',
    stageName: 'Marko Inc',
    avatar: null,
  },
  notifications: {
    email: false,
    push: true,
    dealUpdates: true,
    callReminders: true,
  },
  integrations: {
    googleCalendar: true,
    slack: false,
    patrick: true, // Patrick pipeline integration
  },
  appearance: {
    darkMode: true, // DEFAULT DARK MODE for night work
    compactMode: true,
    sidebarCollapsed: false,
  },
};
