/**
 * Fast Qualification Logic Test - 1000 cases
 * Tests ONLY the qualification logic (no BetterContact, no Slack)
 */

const http = require('http');

// Temporarily start a test server that skips enrichment
const TEST_PORT = 9101;

// =============================================================================
// COPY OF QUALIFICATION LOGIC (for direct testing)
// =============================================================================

const LAW_FIRM_INDICATORS = {
  strongKeywords: [
    'personal injury', 'car accident attorney', 'truck accident', 'motorcycle accident',
    'slip and fall', 'wrongful death', 'medical malpractice', 'workers compensation',
    'injury lawyer', 'injury attorney', 'accident lawyer', 'accident attorney',
    'law firm', 'attorneys at law', 'legal services', 'free consultation',
    'case evaluation', 'no fee unless we win', 'contingency fee',
    'practice areas', 'our attorneys', 'attorney profiles', 'meet our lawyers'
  ],
  moderateKeywords: [
    'attorney', 'lawyer', 'legal', 'law office', 'esquire', 'esq.',
    'litigation', 'trial attorney', 'courtroom', 'verdict', 'settlement',
    'bar association', 'admitted to practice'
  ],
  domainPatterns: [
    /law\.com$/i, /legal\.com$/i, /attorney/i, /lawyer/i,
    /lawfirm/i, /lawoffice/i, /esq/i, /legal/i
  ],
  decisionMakerTitles: [
    'partner', 'managing partner', 'founding partner', 'senior partner',
    'owner', 'founder', 'principal', 'of counsel',
    'ceo', 'president', 'chief executive', 'managing director', 'executive director',
    'marketing director', 'cmo', 'chief marketing', 'director of marketing',
    'vp', 'vice president', 'head of', 'director of',
    'business development', 'intake director', 'intake manager'
  ],
  excludeTitles: [
    'paralegal', 'legal assistant', 'secretary', 'receptionist',
    'associate attorney', 'associate', 'intern', 'clerk', 'student'
  ]
};

function verifyLawFirmSync(data) {
  const result = {
    isLawFirm: false,
    isDecisionMaker: false,
    confidence: 0,
    reasons: []
  };

  const title = (data.jobTitle || '').toLowerCase();
  const industry = (data.industry || '').toLowerCase();
  const company = (data.companyName || '').toLowerCase();
  const website = data.website || '';

  // 1. Check Industry field
  if (industry.includes('legal') || industry.includes('law')) {
    result.confidence += 40;
    result.reasons.push(`Industry: "${data.industry}"`);
  }

  // 2. Check company name for law firm patterns
  if (company.includes('law') || company.includes('legal') || 
      company.includes('attorney') || company.includes('lawyer') ||
      company.includes('& associates') || company.includes('llp') ||
      company.includes('pllc') || /\b(pc|pa|plc)\b/i.test(company)) {
    result.confidence += 30;
    result.reasons.push(`Company name suggests law firm`);
  }

  // 3. Check title for decision maker
  if (LAW_FIRM_INDICATORS.decisionMakerTitles.some(t => title.includes(t.toLowerCase()))) {
    result.isDecisionMaker = true;
    result.confidence += 20;
    result.reasons.push(`Decision maker title: "${data.jobTitle}"`);
  }
  
  // Check for attorney/lawyer in title
  if (title.includes('attorney') || title.includes('lawyer') || title.includes('partner')) {
    result.confidence += 15;
    result.reasons.push(`Legal professional title`);
  }

  // 4. Check for excluded titles
  if (LAW_FIRM_INDICATORS.excludeTitles.some(t => title.includes(t.toLowerCase()))) {
    result.confidence -= 30;
    result.reasons.push(`Non-decision maker title: "${data.jobTitle}"`);
  }

  // 5. Check website domain
  if (website) {
    try {
      const domain = new URL(website.startsWith('http') ? website : `https://${website}`).hostname;
      if (LAW_FIRM_INDICATORS.domainPatterns.some(p => p.test(domain))) {
        result.confidence += 20;
        result.reasons.push(`Domain suggests law firm: ${domain}`);
      }
    } catch(e) {}
  }

  // Final determination
  result.isLawFirm = result.confidence >= 50;
  
  // Decision maker check
  if (!result.isDecisionMaker && result.isLawFirm) {
    const hasSomeAuthority = title.includes('director') || title.includes('manager') ||
      title.includes('head') || title.includes('chief') || title.includes('vp') ||
      title.includes('president') || title.includes('owner');
    
    if (hasSomeAuthority) {
      result.isDecisionMaker = true;
    }
  }

  return result;
}

function normalizeRB2BPayload(payload) {
  return {
    firstName: payload['First Name'] || '',
    lastName: payload['Last Name'] || '',
    fullName: `${payload['First Name'] || ''} ${payload['Last Name'] || ''}`.trim(),
    jobTitle: payload['Title'] || '',
    companyName: payload['Company Name'] || '',
    businessEmail: payload['Business Email'] || '',
    website: payload['Website'] || '',
    linkedinUrl: payload['LinkedIn URL'] || '',
    industry: payload['Industry'] || ''
  };
}

// =============================================================================
// TEST DATA GENERATORS (same as before but simplified)
// =============================================================================

const LAW_FIRM_NAMES = [
  'Smith & Associates', 'Johnson Law Firm', 'Williams Legal Group',
  'Davis & Partners LLP', 'Miller Law Offices', 'Taylor Law Group PLLC',
  'Morgan & Morgan', 'Cellino & Barnes', 'Jacoby & Meyers',
  'Personal Injury Law Center', 'Accident Attorneys of Texas',
  'MVA Legal Group', 'Car Accident Lawyers LLC'
];

const NON_LAW_FIRMS = [
  'Google', 'Microsoft', 'Amazon', 'Acme Corporation',
  'Bank of America', 'State Farm', 'McKinsey & Company',
  'Digital Marketing Agency', 'SEO Experts LLC'
];

const DECISION_MAKER_TITLES = [
  'Managing Partner', 'Senior Partner', 'Founding Partner', 'Partner',
  'Owner', 'Founder', 'CEO', 'Marketing Director', 'CMO'
];

const NON_DECISION_TITLES = [
  'Associate Attorney', 'Legal Assistant', 'Paralegal',
  'Intern', 'Receptionist', 'Software Engineer'
];

const LEGAL_INDUSTRIES = ['Legal Services', 'Law Practice', 'Legal'];
const NON_LEGAL_INDUSTRIES = ['Technology', 'Insurance', 'Marketing & Advertising', 'Consulting'];

function randomFrom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomName() {
  const firstNames = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia'];
  return { firstName: randomFrom(firstNames), lastName: randomFrom(lastNames) };
}

function generateTestCases(count) {
  const cases = [];
  
  // 30% - Clear law firm decision makers (should qualify)
  for (let i = 0; i < count * 0.30; i++) {
    const name = randomName();
    cases.push({
      category: 'law_firm_decision_maker',
      expectedQualified: true,
      payload: {
        'First Name': name.firstName, 'Last Name': name.lastName,
        'Title': randomFrom(DECISION_MAKER_TITLES),
        'Company Name': randomFrom(LAW_FIRM_NAMES),
        'Industry': randomFrom(LEGAL_INDUSTRIES)
      }
    });
  }
  
  // 20% - Law firm non-decision makers (should NOT qualify)
  for (let i = 0; i < count * 0.20; i++) {
    const name = randomName();
    cases.push({
      category: 'law_firm_non_decision_maker',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName, 'Last Name': name.lastName,
        'Title': randomFrom(NON_DECISION_TITLES),
        'Company Name': randomFrom(LAW_FIRM_NAMES),
        'Industry': randomFrom(LEGAL_INDUSTRIES)
      }
    });
  }
  
  // 30% - Non-law company (should NOT qualify)
  for (let i = 0; i < count * 0.30; i++) {
    const name = randomName();
    cases.push({
      category: 'non_law_company',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName, 'Last Name': name.lastName,
        'Title': randomFrom(DECISION_MAKER_TITLES),
        'Company Name': randomFrom(NON_LAW_FIRMS),
        'Industry': randomFrom(NON_LEGAL_INDUSTRIES)
      }
    });
  }
  
  // 10% - Edge cases: Attorney at non-law company (should NOT qualify)
  for (let i = 0; i < count * 0.10; i++) {
    const name = randomName();
    cases.push({
      category: 'edge_attorney_non_law',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName, 'Last Name': name.lastName,
        'Title': 'Staff Attorney',
        'Company Name': 'State Farm Insurance',
        'Industry': 'Insurance'
      }
    });
  }
  
  // 10% - Minimal data (should NOT qualify without enough info)
  for (let i = 0; i < count * 0.10; i++) {
    const name = randomName();
    cases.push({
      category: 'minimal_data',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName, 'Last Name': name.lastName
      }
    });
  }
  
  return cases;
}

// =============================================================================
// RUN TESTS
// =============================================================================

async function runAllTests(count = 1000) {
  console.log(`\n🧪 FAST QUALIFICATION TEST - ${count} CASES\n`);
  console.log('='.repeat(60));
  
  const testCases = generateTestCases(count);
  const results = [];
  const startTime = Date.now();
  
  for (const tc of testCases) {
    const data = normalizeRB2BPayload(tc.payload);
    const verification = verifyLawFirmSync(data);
    
    const qualified = verification.isLawFirm && verification.isDecisionMaker;
    const match = qualified === tc.expectedQualified;
    
    results.push({
      category: tc.category,
      expected: tc.expectedQualified,
      actual: qualified,
      confidence: verification.confidence,
      match,
      payload: tc.payload,
      reasons: verification.reasons
    });
  }
  
  const duration = (Date.now() - startTime) / 1000;
  console.log(`✅ Completed in ${duration.toFixed(2)}s (${(count/duration).toFixed(0)} tests/sec)\n`);
  
  // Analysis
  console.log('='.repeat(60));
  console.log('📊 RESULTS BY CATEGORY\n');
  
  const categories = {};
  for (const r of results) {
    if (!categories[r.category]) {
      categories[r.category] = { total: 0, matches: 0, falsePositives: [], falseNegatives: [] };
    }
    categories[r.category].total++;
    if (r.match) {
      categories[r.category].matches++;
    } else if (r.actual === true && r.expected === false) {
      categories[r.category].falsePositives.push(r);
    } else if (r.actual === false && r.expected === true) {
      categories[r.category].falseNegatives.push(r);
    }
  }
  
  for (const [cat, data] of Object.entries(categories)) {
    const accuracy = ((data.matches / data.total) * 100).toFixed(1);
    const status = data.matches === data.total ? '✅' : '⚠️';
    console.log(`${status} ${cat}: ${data.matches}/${data.total} (${accuracy}%)`);
    if (data.falsePositives.length > 0) {
      console.log(`   ❌ False Positives: ${data.falsePositives.length}`);
    }
    if (data.falseNegatives.length > 0) {
      console.log(`   ❌ False Negatives: ${data.falseNegatives.length}`);
    }
  }
  
  // Overall stats
  const totalMatches = results.filter(r => r.match).length;
  const totalFP = results.filter(r => r.actual === true && r.expected === false).length;
  const totalFN = results.filter(r => r.actual === false && r.expected === true).length;
  
  console.log('\n' + '='.repeat(60));
  console.log('📈 OVERALL METRICS\n');
  console.log(`  Total Tests:      ${count}`);
  console.log(`  Correct:          ${totalMatches} (${((totalMatches/count)*100).toFixed(1)}%)`);
  console.log(`  False Positives:  ${totalFP} (letting non-lawyers through)`);
  console.log(`  False Negatives:  ${totalFN} (missing real lawyers)`);
  
  // Show examples of failures
  if (totalFP > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('🚨 FALSE POSITIVE EXAMPLES:\n');
    const fpExamples = results.filter(r => r.actual === true && r.expected === false).slice(0, 5);
    for (const ex of fpExamples) {
      console.log(`  • ${ex.payload['First Name']} ${ex.payload['Last Name']}`);
      console.log(`    Title: ${ex.payload['Title']}`);
      console.log(`    Company: ${ex.payload['Company Name']}`);
      console.log(`    Industry: ${ex.payload['Industry']}`);
      console.log(`    Confidence: ${ex.confidence}`);
      console.log(`    Reasons: ${ex.reasons.join(' | ')}`);
      console.log('');
    }
  }
  
  if (totalFN > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('🚨 FALSE NEGATIVE EXAMPLES:\n');
    const fnExamples = results.filter(r => r.actual === false && r.expected === true).slice(0, 5);
    for (const ex of fnExamples) {
      console.log(`  • ${ex.payload['First Name']} ${ex.payload['Last Name']}`);
      console.log(`    Title: ${ex.payload['Title']}`);
      console.log(`    Company: ${ex.payload['Company Name']}`);
      console.log(`    Industry: ${ex.payload['Industry']}`);
      console.log(`    Confidence: ${ex.confidence}`);
      console.log(`    Reasons: ${ex.reasons.join(' | ')}`);
      console.log('');
    }
  }
  
  // Save results
  const fs = require('fs');
  const reportPath = `/home/ec2-user/clawd/services/lead-webhook/qualification-test-results.json`;
  fs.writeFileSync(reportPath, JSON.stringify({
    summary: {
      total: count,
      correct: totalMatches,
      accuracy: ((totalMatches/count)*100).toFixed(1) + '%',
      falsePositives: totalFP,
      falseNegatives: totalFN
    },
    categories,
    failures: {
      falsePositives: results.filter(r => r.actual === true && r.expected === false),
      falseNegatives: results.filter(r => r.actual === false && r.expected === true)
    }
  }, null, 2));
  
  console.log(`\n📁 Results saved to: ${reportPath}`);
  
  return { totalMatches, totalFP, totalFN, count, categories };
}

runAllTests(1000);
