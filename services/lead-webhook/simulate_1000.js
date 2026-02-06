#!/usr/bin/env node
/**
 * Lead Webhook Simulation — 1000 Realistic Visitors
 * Generates Leadpipe-format payloads with realistic distributions:
 *   15% lawyers/attorneys (ICP)
 *   10% law firm staff
 *   20% other professionals who might buy leads
 *   15% competitors/vendors
 *   40% random/irrelevant visitors
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const WEBHOOK_URL = 'http://localhost:9100/webhook';
const REPORT_PATH = path.join(__dirname, 'SIMULATION_REPORT.md');
const CONCURRENCY = 20; // parallel requests

// ============================================================
// DATA POOLS
// ============================================================

const FIRST_NAMES = ['James','John','Robert','Michael','David','William','Richard','Joseph','Thomas','Charles',
  'Christopher','Daniel','Matthew','Anthony','Mark','Donald','Steven','Paul','Andrew','Joshua',
  'Mary','Patricia','Jennifer','Linda','Barbara','Elizabeth','Susan','Jessica','Sarah','Karen',
  'Lisa','Nancy','Betty','Margaret','Sandra','Ashley','Dorothy','Kimberly','Emily','Donna',
  'Carlos','Maria','Juan','Miguel','Sofia','Isabella','Alejandro','Diego','Valentina','Camila',
  'Raj','Priya','Amit','Sunita','Deepak','Anita','Ravi','Kavita','Sanjay','Neha'];

const LAST_NAMES = ['Smith','Johnson','Williams','Brown','Jones','Garcia','Miller','Davis','Rodriguez','Martinez',
  'Hernandez','Lopez','Gonzalez','Wilson','Anderson','Thomas','Taylor','Moore','Jackson','Martin',
  'Lee','Perez','Thompson','White','Harris','Sanchez','Clark','Ramirez','Lewis','Robinson',
  'Walker','Young','Allen','King','Wright','Scott','Torres','Nguyen','Hill','Flores',
  'Green','Adams','Nelson','Baker','Hall','Rivera','Campbell','Mitchell','Carter','Roberts',
  'Patel','Shah','Kim','Park','Chen','Wang','Li','Zhang','Singh','Kumar'];

const STATES = ['Texas','California','Florida','New York','Pennsylvania','Illinois','Ohio','Georgia',
  'North Carolina','Michigan','New Jersey','Virginia','Washington','Arizona','Massachusetts',
  'Tennessee','Indiana','Missouri','Maryland','Wisconsin','Colorado','Minnesota','South Carolina',
  'Alabama','Louisiana','Kentucky','Oregon','Oklahoma','Connecticut','Utah','Iowa','Nevada',
  'Arkansas','Mississippi','Kansas','New Mexico','Nebraska','Idaho','West Virginia','Hawaii'];

const CITIES = {
  'Texas': ['Houston','Dallas','Austin','San Antonio','Fort Worth','El Paso','Arlington','Corpus Christi','Plano','Lubbock'],
  'California': ['Los Angeles','San Francisco','San Diego','San Jose','Sacramento','Oakland','Fresno','Long Beach'],
  'Florida': ['Miami','Orlando','Tampa','Jacksonville','Fort Lauderdale','St. Petersburg','Tallahassee'],
  'New York': ['New York City','Buffalo','Rochester','Albany','Syracuse','Yonkers'],
  'default': ['Springfield','Portland','Charlotte','Nashville','Denver','Phoenix','Seattle','Boston','Chicago','Detroit']
};

function randomCity(state) {
  const pool = CITIES[state] || CITIES['default'];
  return pool[Math.floor(Math.random() * pool.length)];
}

// ============================================================
// VISITOR CATEGORY GENERATORS
// ============================================================

function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }
function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function maybe(pct) { return Math.random() < pct; }

function makeDomain(company) {
  return company.toLowerCase().replace(/[^a-z0-9]+/g, '').slice(0, 20) + '.com';
}

function baseVisitor() {
  const firstName = pick(FIRST_NAMES);
  const lastName = pick(LAST_NAMES);
  const state = pick(STATES);
  return {
    firstName,
    lastName,
    fullName: `${firstName} ${lastName}`,
    ageRange: pick(['25-34','35-44','45-54','55-64']),
    gender: pick(['Male','Female']),
    city: randomCity(state),
    state,
    country: 'United States',
    sessions: rand(1, 15),
    pageviews: rand(1, 60),
    pricingPageViews: 0,
    demoPageViews: 0,
    checkoutPageViews: 0,
  };
}

// ----- 1. LAWYERS / ATTORNEYS (ICP) — 15% -----
function generateLawyer() {
  const v = baseVisitor();
  const lawFirmNames = [
    `${v.lastName} & Associates`, `${v.lastName} Law Group`, `${v.lastName} Legal`,
    `${v.lastName} & Partners`, `The ${v.lastName} Firm`, `${v.lastName} Law Offices`,
    `${v.lastName}, ${pick(LAST_NAMES)} & ${pick(LAST_NAMES)}`,
    `${v.lastName} Personal Injury Law`, `${v.lastName} Trial Attorneys`,
    `${v.lastName} & ${pick(LAST_NAMES)} Injury Lawyers`
  ];
  const titles = [
    'Managing Partner', 'Senior Partner', 'Founding Partner', 'Partner',
    'Attorney', 'Trial Lawyer', 'Personal Injury Attorney',
    'Associate Attorney', 'Of Counsel', 'General Counsel',
    'Senior Associate', 'Attorney at Law', 'Litigation Partner'
  ];
  const industries = [
    'Legal Services', 'Law Practice', 'Law Firm', 'Legal',
    'Personal Injury Law', 'Litigation', 'Trial Law'
  ];
  const seniorities = ['Owner', 'C-Level', 'VP', 'Director', 'Senior', 'Manager', ''];

  const company = pick(lawFirmNames);
  const domain = makeDomain(company);
  const email = `${v.firstName.toLowerCase()}.${v.lastName.toLowerCase()}@${domain}`;

  v.jobTitle = pick(titles);
  v.companyName = company;
  v.companyDomain = domain;
  v.companyEmployeeCount = rand(1, 80);
  v.companySize = v.companyEmployeeCount <= 10 ? '1-10' : v.companyEmployeeCount <= 50 ? '11-50' : '51-200';
  v.companyTotalRevenue = rand(500000, 30000000);
  v.industry = pick(industries);
  v.department = pick(['Legal', 'Management', 'Executive']);
  v.seniority = pick(seniorities);
  v.email = email;
  v.emails = [email];
  v.businessEmails = [email];
  v.personalEmails = maybe(0.5) ? [`${v.firstName.toLowerCase()}${rand(1,99)}@gmail.com`] : [];
  v.phones = maybe(0.7) ? [`+1${rand(200,999)}${rand(1000000,9999999)}`] : [];
  v.linkedinUrl = maybe(0.6) ? `https://linkedin.com/in/${v.firstName.toLowerCase()}${v.lastName.toLowerCase()}${rand(1,999)}` : undefined;
  v.intentScore = pick(['high', 'high', 'medium', 'medium', 'low']);
  v.pricingPageViews = maybe(0.5) ? rand(1, 5) : 0;
  v.demoPageViews = maybe(0.3) ? rand(1, 3) : 0;
  v.checkoutPageViews = maybe(0.1) ? rand(1, 2) : 0;
  v.sessions = rand(2, 12);
  v.pageviews = rand(5, 50);

  const pages = ['https://kuriosbrand.com/', 'https://kuriosbrand.com/about'];
  if (v.pricingPageViews > 0) pages.push('https://kuriosbrand.com/pricing');
  if (v.demoPageViews > 0) pages.push('https://kuriosbrand.com/demo');
  v.landingPage = pick(pages);
  v.visitedPages = pages;
  v.referrer = pick(['https://www.google.com/search?q=mva+lead+generation',
    'https://www.google.com/search?q=personal+injury+leads',
    'https://www.bing.com/', '', 'https://www.google.com/']);
  v.utmSource = maybe(0.4) ? 'google' : undefined;
  v.utmMedium = v.utmSource ? pick(['cpc', 'organic']) : undefined;
  v.utmCampaign = v.utmMedium === 'cpc' ? 'pi-attorneys-2024' : undefined;

  // Some Texas lawyers (higher ICP match)
  if (maybe(0.3)) {
    v.state = 'Texas';
    v.city = randomCity('Texas');
  }

  return { category: 'lawyer', expected: 'qualified', visitor: v };
}

// ----- 2. LAW FIRM STAFF — 10% -----
function generateLawStaff() {
  const v = baseVisitor();
  const company = `${pick(LAST_NAMES)} & ${pick(LAST_NAMES)} Law`;
  const domain = makeDomain(company);
  const email = `${v.firstName.toLowerCase()}.${v.lastName.toLowerCase()}@${domain}`;

  const titles = [
    'Paralegal', 'Legal Assistant', 'Intake Manager', 'Intake Coordinator',
    'Office Manager', 'Legal Secretary', 'Case Manager', 'Legal Administrator',
    'Intake Specialist', 'Law Clerk', 'Legal Nurse Consultant'
  ];

  v.jobTitle = pick(titles);
  v.companyName = company;
  v.companyDomain = domain;
  v.companyEmployeeCount = rand(3, 50);
  v.companyTotalRevenue = rand(500000, 10000000);
  v.industry = pick(['Legal Services', 'Law Practice', 'Legal']);
  v.department = pick(['Legal', 'Administration', 'Operations']);
  v.seniority = pick(['Manager', 'Senior', '']);
  v.email = email;
  v.emails = [email];
  v.businessEmails = [email];
  v.personalEmails = [`${v.firstName.toLowerCase()}@gmail.com`];
  v.phones = maybe(0.5) ? [`+1${rand(200,999)}${rand(1000000,9999999)}`] : [];
  v.linkedinUrl = maybe(0.4) ? `https://linkedin.com/in/${v.firstName.toLowerCase()}${v.lastName.toLowerCase()}` : undefined;
  v.intentScore = pick(['medium', 'medium', 'low', 'high']);
  v.pricingPageViews = maybe(0.3) ? rand(1, 3) : 0;
  v.demoPageViews = maybe(0.2) ? rand(1, 2) : 0;
  v.sessions = rand(1, 6);
  v.pageviews = rand(2, 20);

  v.landingPage = pick(['https://kuriosbrand.com/', 'https://kuriosbrand.com/pricing', 'https://kuriosbrand.com/blog']);
  v.visitedPages = [v.landingPage];
  v.referrer = pick(['https://www.google.com/', '', 'https://www.bing.com/']);

  return { category: 'law_staff', expected: 'borderline', visitor: v };
}

// ----- 3. OTHER PROFESSIONALS — 20% -----
function generateOtherPro() {
  const v = baseVisitor();
  const companies = [
    'Allstate Insurance', 'State Farm', 'Progressive Corp', 'GEICO',
    'Blue Cross Health', 'Kaiser Permanente', 'Mayo Clinic', 'Cleveland Clinic',
    'Chiropractor Plus', 'SpineHealth Associates', 'Claims Pro Inc',
    'Regional Medical Center', 'ABC Insurance Brokers', 'HealthFirst Network',
    'Metro Auto Body', 'Quick Claims Adjusting', 'MedPay Solutions',
    'Recovery & Rehab Center', 'First National Bank', 'Acme Industries',
    'Global Logistics Inc', 'Summit Financial Group', 'Horizon Healthcare',
    'Pacific Coast Chiropractic', 'Austin Auto Group'
  ];
  const titles = [
    'CEO', 'President', 'Owner', 'Director of Operations', 'VP of Sales',
    'Managing Director', 'Business Development Manager', 'Account Executive',
    'Claims Adjuster', 'Insurance Agent', 'Healthcare Administrator',
    'Practice Manager', 'Operations Manager', 'General Manager',
    'Regional Director', 'Chiropractor', 'Director of Marketing',
    'Sales Manager', 'Branch Manager', 'Executive Director'
  ];
  const industries = [
    'Insurance', 'Healthcare', 'Medical', 'Chiropractic', 'Financial Services',
    'Automotive', 'Real Estate', 'Consulting', 'Manufacturing',
    'Construction', 'Retail', 'Transportation', 'Banking'
  ];

  const company = pick(companies);
  const domain = makeDomain(company);
  const email = `${v.firstName.toLowerCase()}.${v.lastName.toLowerCase()}@${domain}`;

  v.jobTitle = pick(titles);
  v.companyName = company;
  v.companyDomain = domain;
  v.companyEmployeeCount = rand(10, 5000);
  v.companyTotalRevenue = rand(1000000, 500000000);
  v.industry = pick(industries);
  v.department = pick(['Sales', 'Operations', 'Executive', 'Marketing', 'Claims']);
  v.seniority = pick(['C-Level', 'VP', 'Director', 'Manager', 'Senior', '']);
  v.email = email;
  v.emails = [email];
  v.businessEmails = [email];
  v.phones = maybe(0.4) ? [`+1${rand(200,999)}${rand(1000000,9999999)}`] : [];
  v.linkedinUrl = maybe(0.5) ? `https://linkedin.com/in/${v.firstName.toLowerCase()}${v.lastName.toLowerCase()}` : undefined;
  v.intentScore = pick(['high', 'medium', 'medium', 'low', 'low']);
  v.pricingPageViews = maybe(0.2) ? rand(1, 3) : 0;
  v.demoPageViews = maybe(0.1) ? rand(1, 2) : 0;
  v.sessions = rand(1, 5);
  v.pageviews = rand(1, 15);

  v.landingPage = pick(['https://kuriosbrand.com/', 'https://kuriosbrand.com/about', 'https://kuriosbrand.com/blog', 'https://kuriosbrand.com/pricing']);
  v.visitedPages = [v.landingPage];
  v.referrer = pick(['https://www.google.com/', '', 'https://www.linkedin.com/', 'https://www.bing.com/']);

  return { category: 'other_pro', expected: 'unqualified', visitor: v };
}

// ----- 4. COMPETITORS / VENDORS — 15% -----
function generateCompetitor() {
  const v = baseVisitor();
  const companies = [
    'LeadBolt Agency', 'Growth Marketing Co', 'Digital Leads Pro', 'RankFirst SEO',
    'SEO Wizards LLC', 'PPC Masters Agency', 'WebDev Solutions', 'Lead Gen Experts',
    'Marketing Force Inc', 'AdVantage Digital', 'ConvertPro SaaS', 'LeadPipe Inc',
    'RB2B Analytics', 'Clearbit Data', 'ZoomInfo Corp', 'Apollo.io',
    'HubSpot', 'Salesforce', 'Click Funnels', 'Social Media Agency Plus',
    'PageRank Digital', 'Backlink Builders', 'Content Marketing Co',
    'Funnel Hackers LLC', 'CRM Solutions Inc'
  ];
  const titles = [
    'CEO', 'Founder', 'Co-Founder', 'Head of Marketing', 'VP of Sales',
    'SEO Specialist', 'Digital Marketing Manager', 'Growth Hacker',
    'Account Executive', 'Business Development Rep', 'Sales Manager',
    'Marketing Director', 'Content Strategist', 'PPC Manager',
    'Lead Generation Specialist', 'Partnership Manager', 'SDR', 'BDR'
  ];
  const industries = [
    'Marketing & Advertising', 'Digital Marketing', 'SaaS', 'Marketing Agency',
    'Software', 'Technology', 'Information Technology', 'Advertising',
    'Lead Generation', 'SEO Agency', 'Web Design Agency'
  ];

  const company = pick(companies);
  const domain = makeDomain(company);
  const email = `${v.firstName.toLowerCase()}@${domain}`;

  v.jobTitle = pick(titles);
  v.companyName = company;
  v.companyDomain = domain;
  v.companyEmployeeCount = rand(5, 200);
  v.companyTotalRevenue = rand(500000, 20000000);
  v.industry = pick(industries);
  v.department = pick(['Marketing', 'Sales', 'Executive', 'Business Development']);
  v.seniority = pick(['C-Level', 'VP', 'Director', 'Manager', '']);
  v.email = email;
  v.emails = [email];
  v.businessEmails = [email];
  v.phones = maybe(0.3) ? [`+1${rand(200,999)}${rand(1000000,9999999)}`] : [];
  v.linkedinUrl = maybe(0.7) ? `https://linkedin.com/in/${v.firstName.toLowerCase()}${v.lastName.toLowerCase()}` : undefined;
  v.intentScore = pick(['high', 'medium', 'low']);
  v.pricingPageViews = maybe(0.4) ? rand(1, 5) : 0;
  v.demoPageViews = maybe(0.2) ? rand(1, 3) : 0;
  v.sessions = rand(1, 10);
  v.pageviews = rand(2, 30);

  v.landingPage = pick(['https://kuriosbrand.com/', 'https://kuriosbrand.com/pricing', 'https://kuriosbrand.com/about', 'https://kuriosbrand.com/blog']);
  v.visitedPages = [v.landingPage];
  v.referrer = pick(['https://www.google.com/', '', 'https://www.linkedin.com/', 'direct']);

  return { category: 'competitor', expected: 'unqualified', visitor: v };
}

// ----- 5. RANDOM / IRRELEVANT — 40% -----
function generateRandom() {
  const v = baseVisitor();
  const companies = [
    'University of Texas', 'Stanford University', 'McDonald\'s', 'Walmart',
    'Target', 'Home Depot', 'Best Buy', 'Starbucks', 'Amazon',
    '', 'Self-Employed', 'Freelancer', 'N/A', 'Uber', 'Lyft',
    'DoorDash', 'Local Restaurant', 'Small Business', 'Family Farm',
    'Construction Co', 'Plumbing Plus', 'Electric Solutions', 'Hair Salon',
    'Fitness Center', 'Pet Store', 'Coffee Shop', 'Food Truck',
    'Auto Repair Shop', 'Landscaping LLC', 'Cleaning Services'
  ];
  const titles = [
    '', 'Student', 'Intern', 'Retired', 'Unemployed', 'Cashier',
    'Teacher', 'Professor', 'Nurse', 'Driver', 'Engineer',
    'Software Developer', 'Data Analyst', 'Designer', 'Writer',
    'Photographer', 'Chef', 'Mechanic', 'Electrician', 'Plumber',
    'Real Estate Agent', 'Accountant', 'HR Manager', 'Receptionist',
    'Barista', 'Server', 'Bartender', 'Fitness Trainer', 'Therapist',
    'Social Worker', 'Researcher', 'Lab Technician', 'Pharmacist'
  ];
  const industries = [
    'Education', 'Retail', 'Food & Beverage', 'Transportation',
    'Technology', 'Entertainment', 'Hospitality', 'Agriculture',
    'Construction', 'Manufacturing', 'Arts', '', 'Other',
    'Government', 'Non-Profit', 'Religious', 'Military'
  ];

  const company = pick(companies);
  const usePersonalEmail = maybe(0.7);
  const emailProvider = pick(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com', 'icloud.com']);
  const email = usePersonalEmail
    ? `${v.firstName.toLowerCase()}${v.lastName.toLowerCase()}${rand(1,999)}@${emailProvider}`
    : `${v.firstName.toLowerCase()}@${makeDomain(company || 'example')}`;

  v.jobTitle = pick(titles);
  v.companyName = company;
  v.companyDomain = company ? makeDomain(company) : '';
  v.companyEmployeeCount = maybe(0.5) ? rand(1, 50000) : 0;
  v.companyTotalRevenue = maybe(0.3) ? rand(10000, 100000000) : 0;
  v.industry = pick(industries);
  v.department = pick(['', 'Operations', 'Sales', 'IT', 'HR', 'Finance']);
  v.seniority = pick(['', '', '', 'Manager', 'Senior']);
  v.email = email;
  v.emails = [email];
  v.businessEmails = usePersonalEmail ? [] : [email];
  v.personalEmails = usePersonalEmail ? [email] : [];
  v.phones = maybe(0.2) ? [`+1${rand(200,999)}${rand(1000000,9999999)}`] : [];
  v.linkedinUrl = maybe(0.2) ? `https://linkedin.com/in/${v.firstName.toLowerCase()}${v.lastName.toLowerCase()}` : undefined;
  v.intentScore = pick(['low', 'low', 'low', 'medium']);
  v.pricingPageViews = maybe(0.1) ? 1 : 0;
  v.demoPageViews = 0;
  v.checkoutPageViews = 0;
  v.sessions = rand(1, 3);
  v.pageviews = rand(1, 8);

  v.landingPage = pick(['https://kuriosbrand.com/', 'https://kuriosbrand.com/blog', 'https://kuriosbrand.com/about']);
  v.visitedPages = [v.landingPage];
  v.referrer = pick(['', 'https://www.google.com/', 'https://www.facebook.com/', 'https://twitter.com/', 'https://www.reddit.com/']);

  return { category: 'random', expected: 'unqualified', visitor: v };
}

// ============================================================
// GENERATE ALL VISITORS
// ============================================================

function generateVisitors(count) {
  const visitors = [];
  const distribution = { lawyer: 0.15, law_staff: 0.10, other_pro: 0.20, competitor: 0.15, random: 0.40 };

  for (let i = 0; i < count; i++) {
    const r = Math.random();
    if (r < distribution.lawyer) {
      visitors.push(generateLawyer());
    } else if (r < distribution.lawyer + distribution.law_staff) {
      visitors.push(generateLawStaff());
    } else if (r < distribution.lawyer + distribution.law_staff + distribution.other_pro) {
      visitors.push(generateOtherPro());
    } else if (r < distribution.lawyer + distribution.law_staff + distribution.other_pro + distribution.competitor) {
      visitors.push(generateCompetitor());
    } else {
      visitors.push(generateRandom());
    }
  }
  return visitors;
}

// ============================================================
// SEND TO WEBHOOK
// ============================================================

function sendWebhook(visitorData) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      event: 'visitor.identified',
      data: visitorData
    });

    const url = new URL(WEBHOOK_URL);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-webhook-event': 'visitor.identified',
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = http.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          resolve({ error: 'parse_error', raw: body });
        }
      });
    });

    req.on('error', (err) => resolve({ error: err.message }));
    req.setTimeout(5000, () => {
      req.destroy();
      resolve({ error: 'timeout' });
    });

    req.write(payload);
    req.end();
  });
}

// ============================================================
// RUN SIMULATION
// ============================================================

async function runSimulation() {
  console.log('🚀 Generating 1000 visitor payloads...');
  const visitors = generateVisitors(1000);

  // Count distribution
  const dist = {};
  for (const v of visitors) {
    dist[v.category] = (dist[v.category] || 0) + 1;
  }
  console.log('📊 Distribution:', JSON.stringify(dist));
  console.log('📡 Sending to webhook...\n');

  const results = [];
  const errors = [];
  let completed = 0;

  // Send in batches for concurrency control
  for (let i = 0; i < visitors.length; i += CONCURRENCY) {
    const batch = visitors.slice(i, i + CONCURRENCY);
    const batchResults = await Promise.all(
      batch.map(async (v, idx) => {
        const globalIdx = i + idx;
        try {
          const response = await sendWebhook(v.visitor);
          completed++;
          if (completed % 100 === 0) {
            process.stdout.write(`  Processed ${completed}/1000\n`);
          }
          return {
            index: globalIdx,
            category: v.category,
            expected: v.expected,
            name: `${v.visitor.firstName} ${v.visitor.lastName}`,
            jobTitle: v.visitor.jobTitle,
            companyName: v.visitor.companyName,
            industry: v.visitor.industry,
            intentScore: v.visitor.intentScore,
            seniority: v.visitor.seniority,
            score: response.score,
            qualified: response.qualified,
            error: response.error || null
          };
        } catch (err) {
          errors.push({ index: globalIdx, category: v.category, error: err.message });
          return {
            index: globalIdx,
            category: v.category,
            expected: v.expected,
            name: `${v.visitor.firstName} ${v.visitor.lastName}`,
            jobTitle: v.visitor.jobTitle,
            companyName: v.visitor.companyName,
            industry: v.visitor.industry,
            score: null,
            qualified: null,
            error: err.message
          };
        }
      })
    );
    results.push(...batchResults);
  }

  console.log(`\n✅ All ${results.length} requests completed (${errors.length} errors)\n`);
  return { visitors, results, errors, dist };
}

// ============================================================
// GENERATE REPORT
// ============================================================

function generateReport({ visitors, results, errors, dist }) {
  const validResults = results.filter(r => r.score !== null && r.score !== undefined);

  // Overall stats
  const qualified = validResults.filter(r => r.qualified);
  const unqualified = validResults.filter(r => !r.qualified);

  // By category
  const byCategory = {};
  for (const r of validResults) {
    if (!byCategory[r.category]) {
      byCategory[r.category] = { total: 0, qualified: 0, scores: [], items: [] };
    }
    byCategory[r.category].total++;
    if (r.qualified) byCategory[r.category].qualified++;
    byCategory[r.category].scores.push(r.score);
    byCategory[r.category].items.push(r);
  }

  // Score distribution histogram
  const buckets = {};
  for (const r of validResults) {
    const bucket = Math.floor(r.score / 10) * 10;
    const key = r.score < 0 ? 'negative' : `${bucket}-${bucket + 9}`;
    buckets[key] = (buckets[key] || 0) + 1;
  }

  // False positives: scored qualified but shouldn't be (random, competitor)
  const falsePositives = validResults.filter(r =>
    r.qualified && (r.category === 'random' || r.category === 'competitor')
  );

  // False negatives: scored unqualified but should be (lawyer)
  const falseNegatives = validResults.filter(r =>
    !r.qualified && r.category === 'lawyer'
  );

  // Top 10 highest
  const top10 = [...validResults].sort((a, b) => b.score - a.score).slice(0, 10);

  // Bottom 10 closest to qualifying (score 35-49)
  const borderline = [...validResults]
    .filter(r => r.score >= 35 && r.score < 50)
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

  // Category stats
  function catStats(cat) {
    const c = byCategory[cat];
    if (!c) return { avg: 0, min: 0, max: 0, median: 0, qualRate: '0%' };
    const sorted = [...c.scores].sort((a, b) => a - b);
    return {
      total: c.total,
      qualified: c.qualified,
      qualRate: `${((c.qualified / c.total) * 100).toFixed(1)}%`,
      avg: (c.scores.reduce((a, b) => a + b, 0) / c.scores.length).toFixed(1),
      min: sorted[0],
      max: sorted[sorted.length - 1],
      median: sorted[Math.floor(sorted.length / 2)]
    };
  }

  // Build markdown report
  let md = `# Lead Webhook Simulation Report
> Generated: ${new Date().toISOString()}
> Total visitors: ${results.length} | Errors: ${errors.length}

## Summary

| Metric | Value |
|--------|-------|
| Total Processed | ${validResults.length} |
| **Qualified** | **${qualified.length}** (${((qualified.length / validResults.length) * 100).toFixed(1)}%) |
| Unqualified | ${unqualified.length} (${((unqualified.length / validResults.length) * 100).toFixed(1)}%) |
| False Positives | ${falsePositives.length} |
| False Negatives | ${falseNegatives.length} |
| Errors | ${errors.length} |

## Distribution Generated

| Category | Count | % |
|----------|-------|---|
| Lawyers/Attorneys (ICP) | ${dist.lawyer || 0} | ${(((dist.lawyer || 0) / results.length) * 100).toFixed(1)}% |
| Law Firm Staff | ${dist.law_staff || 0} | ${(((dist.law_staff || 0) / results.length) * 100).toFixed(1)}% |
| Other Professionals | ${dist.other_pro || 0} | ${(((dist.other_pro || 0) / results.length) * 100).toFixed(1)}% |
| Competitors/Vendors | ${dist.competitor || 0} | ${(((dist.competitor || 0) / results.length) * 100).toFixed(1)}% |
| Random/Irrelevant | ${dist.random || 0} | ${(((dist.random || 0) / results.length) * 100).toFixed(1)}% |

## Qualification by Category

| Category | Total | Qualified | Rate | Avg Score | Min | Max | Median |
|----------|-------|-----------|------|-----------|-----|-----|--------|
`;

  for (const cat of ['lawyer', 'law_staff', 'other_pro', 'competitor', 'random']) {
    const s = catStats(cat);
    if (s.total) {
      md += `| ${cat} | ${s.total} | ${s.qualified} | ${s.qualRate} | ${s.avg} | ${s.min} | ${s.max} | ${s.median} |\n`;
    }
  }

  // Score histogram
  md += `\n## Score Distribution\n\n`;
  md += `| Score Range | Count | Bar |\n|-------------|-------|-----|\n`;
  const sortedBuckets = Object.entries(buckets).sort((a, b) => {
    if (a[0] === 'negative') return -1;
    if (b[0] === 'negative') return 1;
    return parseInt(a[0]) - parseInt(b[0]);
  });
  const maxBucket = Math.max(...Object.values(buckets));
  for (const [range, count] of sortedBuckets) {
    const bar = '█'.repeat(Math.ceil((count / maxBucket) * 30));
    md += `| ${range} | ${count} | ${bar} |\n`;
  }

  // False positives
  md += `\n## False Positives (${falsePositives.length})\n`;
  md += `> Visitors scored as qualified but should NOT be (competitors/random)\n\n`;
  if (falsePositives.length === 0) {
    md += `✅ No false positives!\n`;
  } else {
    md += `| Name | Title | Company | Industry | Score | Category |\n|------|-------|---------|----------|-------|----------|\n`;
    for (const fp of falsePositives.slice(0, 20)) {
      md += `| ${fp.name} | ${fp.jobTitle || 'N/A'} | ${fp.companyName || 'N/A'} | ${fp.industry || 'N/A'} | ${fp.score} | ${fp.category} |\n`;
    }
    if (falsePositives.length > 20) md += `\n... and ${falsePositives.length - 20} more\n`;
  }

  // False negatives
  md += `\n## False Negatives (${falseNegatives.length})\n`;
  md += `> Lawyers who scored below qualification threshold (50)\n\n`;
  if (falseNegatives.length === 0) {
    md += `✅ No false negatives!\n`;
  } else {
    md += `| Name | Title | Company | Industry | Intent | Score |\n|------|-------|---------|----------|--------|-------|\n`;
    for (const fn of falseNegatives.slice(0, 20)) {
      md += `| ${fn.name} | ${fn.jobTitle || 'N/A'} | ${fn.companyName || 'N/A'} | ${fn.industry || 'N/A'} | ${fn.intentScore || 'N/A'} | ${fn.score} |\n`;
    }
    if (falseNegatives.length > 20) md += `\n... and ${falseNegatives.length - 20} more\n`;
  }

  // Top 10
  md += `\n## Top 10 Highest Scored Visitors\n\n`;
  md += `| # | Name | Title | Company | Industry | Intent | Score | Category |\n|---|------|-------|---------|----------|--------|-------|----------|\n`;
  for (let i = 0; i < top10.length; i++) {
    const t = top10[i];
    md += `| ${i + 1} | ${t.name} | ${t.jobTitle || 'N/A'} | ${t.companyName || 'N/A'} | ${t.industry || 'N/A'} | ${t.intentScore || 'N/A'} | **${t.score}** | ${t.category} |\n`;
  }

  // Borderline (close to qualifying)
  md += `\n## Borderline Visitors (Score 35-49)\n`;
  md += `> These almost qualified but didn't make the cut\n\n`;
  if (borderline.length === 0) {
    md += `No visitors in the 35-49 range.\n`;
  } else {
    md += `| Name | Title | Company | Industry | Intent | Score | Category |\n|------|-------|---------|----------|--------|-------|----------|\n`;
    for (const b of borderline) {
      md += `| ${b.name} | ${b.jobTitle || 'N/A'} | ${b.companyName || 'N/A'} | ${b.industry || 'N/A'} | ${b.intentScore || 'N/A'} | ${b.score} | ${b.category} |\n`;
    }
  }

  // Errors
  if (errors.length > 0) {
    md += `\n## Errors (${errors.length})\n\n`;
    md += `| Index | Category | Error |\n|-------|----------|-------|\n`;
    for (const e of errors.slice(0, 20)) {
      md += `| ${e.index} | ${e.category} | ${e.error} |\n`;
    }
  }

  md += `\n---\n*Simulation complete. Qualification threshold: 50 points.*\n`;

  return md;
}

// ============================================================
// MAIN
// ============================================================

(async () => {
  try {
    // Verify server is up
    const healthCheck = await new Promise((resolve) => {
      http.get('http://localhost:9100/health', (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => resolve(JSON.parse(body)));
      }).on('error', () => resolve({ error: 'Server not reachable' }));
    });

    if (healthCheck.error) {
      console.error('❌ Server not running! Start it first: pm2 restart lead-webhook');
      process.exit(1);
    }
    console.log('✅ Server is up:', JSON.stringify(healthCheck));

    const simData = await runSimulation();
    const report = generateReport(simData);

    fs.writeFileSync(REPORT_PATH, report);
    console.log(`\n📄 Report saved to: ${REPORT_PATH}`);

    // Print summary
    const valid = simData.results.filter(r => r.score != null);
    const qual = valid.filter(r => r.qualified);
    const fp = valid.filter(r => r.qualified && (r.category === 'random' || r.category === 'competitor'));
    const fn = valid.filter(r => !r.qualified && r.category === 'lawyer');

    console.log('\n════════════════════════════════════════');
    console.log('  SIMULATION SUMMARY');
    console.log('════════════════════════════════════════');
    console.log(`  Total:           ${valid.length}`);
    console.log(`  Qualified:       ${qual.length} (${((qual.length / valid.length) * 100).toFixed(1)}%)`);
    console.log(`  False Positives: ${fp.length}`);
    console.log(`  False Negatives: ${fn.length}`);
    console.log('════════════════════════════════════════\n');

  } catch (err) {
    console.error('❌ Simulation failed:', err);
    process.exit(1);
  }
})();
