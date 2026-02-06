/**
 * RB2B Webhook Stress Test - 1000 Visitors
 * Tests qualification logic with diverse scenarios
 */

const https = require('https');
const http = require('http');

const WEBHOOK_URL = 'http://localhost:9100/rb2b/webhook';

// =============================================================================
// TEST DATA GENERATORS
// =============================================================================

// Real law firm patterns
const LAW_FIRM_NAMES = [
  'Smith & Associates', 'Johnson Law Firm', 'Williams Legal Group',
  'Davis & Partners LLP', 'Miller Law Offices', 'Wilson Legal Services',
  'Brown & Brown Attorneys', 'Taylor Law Group PLLC', 'Anderson Legal',
  'Thomas & Associates PC', 'Martinez Law Firm', 'Robinson Legal Group',
  'Clark & Clark LLP', 'Lewis Law Offices', 'Lee & Associates',
  'Walker Legal Services', 'Hall Law Firm', 'Allen & Partners',
  'Young Legal Group', 'King Law Offices PLLC', 'Morgan & Morgan',
  'Cellino & Barnes', 'Jacoby & Meyers', 'Sokolove Law',
  'Ben Crump Law', 'Joye Law Firm', 'Beasley Allen'
];

const PI_LAW_FIRM_NAMES = [
  'Personal Injury Law Center', 'Accident Attorneys of Texas',
  'MVA Legal Group', 'Car Accident Lawyers LLC', 'Injury Justice Law Firm',
  'Texas Injury Attorneys', 'Dallas Accident Law', 'Houston PI Lawyers',
  'Slip & Fall Legal Center', 'Wrongful Death Attorneys',
  'Medical Malpractice Law Group', 'Truck Accident Legal Team'
];

// Non-law firm companies
const NON_LAW_FIRMS = [
  'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta',
  'Acme Corporation', 'Best Buy', 'Target', 'Walmart', 'Home Depot',
  'Bank of America', 'Chase', 'Wells Fargo', 'Citibank',
  'Blue Cross Blue Shield', 'United Healthcare', 'Aetna',
  'State Farm', 'Allstate', 'Progressive', 'GEICO',
  'McKinsey & Company', 'Deloitte', 'PwC', 'KPMG',
  'Salesforce', 'HubSpot', 'Zendesk', 'Freshworks',
  'Digital Marketing Agency', 'SEO Experts LLC', 'Lead Gen Solutions'
];

// Ambiguous companies (could be law firms or not)
const AMBIGUOUS_COMPANIES = [
  'Smith Consulting', 'Johnson & Partners', 'Davis Group',
  'Legal Solutions Inc', 'Justice Services', 'Claims Processing LLC',
  'Settlement Services', 'Case Management Co', 'Court Reporters Inc',
  'Paralegal Services', 'Document Review LLC', 'E-Discovery Solutions'
];

// Decision maker titles
const DECISION_MAKER_TITLES = [
  'Managing Partner', 'Senior Partner', 'Founding Partner', 'Name Partner',
  'Partner', 'Owner', 'Founder', 'Co-Founder', 'Principal',
  'CEO', 'President', 'Managing Director', 'Executive Director',
  'Chief Marketing Officer', 'CMO', 'VP of Marketing', 'Marketing Director',
  'Director of Business Development', 'Head of Growth', 'Chief Revenue Officer'
];

// Legal professional titles (qualified)
const LEGAL_TITLES = [
  'Attorney', 'Lawyer', 'Trial Attorney', 'Litigator',
  'Personal Injury Attorney', 'PI Lawyer', 'Accident Attorney',
  'Of Counsel', 'Senior Counsel', 'General Counsel'
];

// Non-decision maker titles (not qualified)
const NON_DECISION_TITLES = [
  'Associate Attorney', 'Junior Associate', 'Legal Assistant', 'Paralegal',
  'Legal Secretary', 'Receptionist', 'Intern', 'Law Clerk',
  'Document Reviewer', 'Legal Researcher', 'Case Manager',
  'Software Engineer', 'Marketing Coordinator', 'Sales Rep',
  'Accountant', 'HR Manager', 'Office Manager', 'Administrative Assistant'
];

// Industries
const LEGAL_INDUSTRIES = [
  'Legal Services', 'Law Practice', 'Legal', 'Law Firms',
  'Legal Services & Law Firms', 'Litigation', 'Trial Law'
];

const NON_LEGAL_INDUSTRIES = [
  'Technology', 'Software', 'Internet Technology & Services',
  'Financial Services', 'Banking', 'Insurance',
  'Healthcare', 'Medical', 'Pharmaceuticals',
  'Retail', 'E-commerce', 'Consumer Goods',
  'Marketing & Advertising', 'Digital Marketing', 'SEO Services',
  'Consulting', 'Management Consulting', 'Business Services',
  'Real Estate', 'Construction', 'Manufacturing'
];

// Law firm websites (real)
const LAW_FIRM_WEBSITES = [
  'https://www.forthepeople.com', 'https://www.cellinolaw.com',
  'https://www.jacobymeyers.com', 'https://www.bencrump.com',
  'https://www.joyelawfirm.com', 'https://www.beasleyallen.com',
  'https://www.morganandmorgan.com', 'https://www.sokolovelaw.com'
];

// Non-law firm websites
const NON_LAW_WEBSITES = [
  'https://www.google.com', 'https://www.microsoft.com',
  'https://www.salesforce.com', 'https://www.hubspot.com',
  'https://www.digitalmarketingagency.com', 'https://www.seocompany.com'
];

// US States
const STATES = ['Texas', 'California', 'Florida', 'New York', 'Illinois', 'Pennsylvania', 'Ohio', 'Georgia', 'North Carolina', 'Michigan'];
const CITIES = {
  'Texas': ['Dallas', 'Houston', 'Austin', 'San Antonio'],
  'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
  'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville'],
  'New York': ['New York', 'Buffalo', 'Albany', 'Rochester'],
  'Illinois': ['Chicago', 'Springfield', 'Naperville'],
  'Pennsylvania': ['Philadelphia', 'Pittsburgh', 'Allentown'],
  'Ohio': ['Columbus', 'Cleveland', 'Cincinnati'],
  'Georgia': ['Atlanta', 'Savannah', 'Augusta'],
  'North Carolina': ['Charlotte', 'Raleigh', 'Durham'],
  'Michigan': ['Detroit', 'Grand Rapids', 'Ann Arbor']
};

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function randomFrom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function randomName() {
  const firstNames = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'Robert', 'Jennifer', 'William', 'Lisa', 'James', 'Maria', 'Richard', 'Susan', 'Thomas', 'Nancy', 'Charles', 'Karen', 'Daniel', 'Betty'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin'];
  return { firstName: randomFrom(firstNames), lastName: randomFrom(lastNames) };
}

// =============================================================================
// TEST CASE GENERATORS
// =============================================================================

function generateTestCases(count) {
  const cases = [];
  
  // Distribution:
  // 20% - Clear law firm decision makers (should qualify)
  // 15% - PI/MVA specific law firms (should qualify)  
  // 10% - Lawyers at law firms but NOT decision makers (should NOT qualify)
  // 15% - Non-law companies with decision maker titles (should NOT qualify)
  // 15% - Ambiguous companies (tests website scraping)
  // 10% - Marketing/SEO agencies (should NOT qualify - competitors)
  // 10% - Edge cases and weird data
  // 5% - Empty/minimal data
  
  const distribution = {
    lawFirmDecisionMaker: Math.floor(count * 0.20),
    piLawFirm: Math.floor(count * 0.15),
    lawFirmNonDecisionMaker: Math.floor(count * 0.10),
    nonLawDecisionMaker: Math.floor(count * 0.15),
    ambiguous: Math.floor(count * 0.15),
    competitor: Math.floor(count * 0.10),
    edgeCase: Math.floor(count * 0.10),
    minimal: Math.floor(count * 0.05)
  };
  
  // Law firm decision makers (SHOULD QUALIFY)
  for (let i = 0; i < distribution.lawFirmDecisionMaker; i++) {
    const name = randomName();
    const state = randomFrom(STATES);
    cases.push({
      category: 'law_firm_decision_maker',
      expectedQualified: true,
      payload: {
        'First Name': name.firstName,
        'Last Name': name.lastName,
        'Title': randomFrom(DECISION_MAKER_TITLES),
        'Company Name': randomFrom(LAW_FIRM_NAMES),
        'Industry': randomFrom(LEGAL_INDUSTRIES),
        'Website': randomFrom(LAW_FIRM_WEBSITES),
        'LinkedIn URL': `https://linkedin.com/in/${name.firstName.toLowerCase()}${name.lastName.toLowerCase()}`,
        'State': state,
        'City': randomFrom(CITIES[state] || ['Unknown']),
        'Employee Count': randomFrom(['1-10', '11-50', '51-200']),
        'Captured URL': 'https://kuriosbrand.com/pricing'
      }
    });
  }
  
  // PI/MVA specific law firms (SHOULD QUALIFY)
  for (let i = 0; i < distribution.piLawFirm; i++) {
    const name = randomName();
    const state = randomFrom(STATES);
    cases.push({
      category: 'pi_law_firm',
      expectedQualified: true,
      payload: {
        'First Name': name.firstName,
        'Last Name': name.lastName,
        'Title': randomFrom([...DECISION_MAKER_TITLES, ...LEGAL_TITLES]),
        'Company Name': randomFrom(PI_LAW_FIRM_NAMES),
        'Industry': randomFrom(LEGAL_INDUSTRIES),
        'Website': randomFrom(LAW_FIRM_WEBSITES),
        'State': state,
        'City': randomFrom(CITIES[state] || ['Unknown']),
        'Employee Count': randomFrom(['1-10', '11-50']),
        'Captured URL': 'https://kuriosbrand.com'
      }
    });
  }
  
  // Law firm non-decision makers (SHOULD NOT QUALIFY)
  for (let i = 0; i < distribution.lawFirmNonDecisionMaker; i++) {
    const name = randomName();
    cases.push({
      category: 'law_firm_non_decision_maker',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName,
        'Last Name': name.lastName,
        'Title': randomFrom(NON_DECISION_TITLES),
        'Company Name': randomFrom(LAW_FIRM_NAMES),
        'Industry': randomFrom(LEGAL_INDUSTRIES),
        'Website': randomFrom(LAW_FIRM_WEBSITES),
        'State': randomFrom(STATES),
        'Employee Count': randomFrom(['11-50', '51-200', '201-500'])
      }
    });
  }
  
  // Non-law company decision makers (SHOULD NOT QUALIFY)
  for (let i = 0; i < distribution.nonLawDecisionMaker; i++) {
    const name = randomName();
    cases.push({
      category: 'non_law_decision_maker',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName,
        'Last Name': name.lastName,
        'Title': randomFrom(DECISION_MAKER_TITLES),
        'Company Name': randomFrom(NON_LAW_FIRMS),
        'Industry': randomFrom(NON_LEGAL_INDUSTRIES),
        'Website': randomFrom(NON_LAW_WEBSITES),
        'State': randomFrom(STATES),
        'Employee Count': randomFrom(['51-200', '201-500', '501-1000', '1001-5000'])
      }
    });
  }
  
  // Ambiguous companies (tests website scraping - mixed expected results)
  for (let i = 0; i < distribution.ambiguous; i++) {
    const name = randomName();
    const isActuallyLawFirm = Math.random() > 0.5;
    cases.push({
      category: 'ambiguous',
      expectedQualified: isActuallyLawFirm ? 'maybe' : false,
      payload: {
        'First Name': name.firstName,
        'Last Name': name.lastName,
        'Title': randomFrom(DECISION_MAKER_TITLES),
        'Company Name': randomFrom(AMBIGUOUS_COMPANIES),
        'Industry': '', // No industry to force website check
        'Website': isActuallyLawFirm ? randomFrom(LAW_FIRM_WEBSITES) : randomFrom(NON_LAW_WEBSITES),
        'State': randomFrom(STATES)
      }
    });
  }
  
  // Marketing/SEO competitors (SHOULD NOT QUALIFY)
  for (let i = 0; i < distribution.competitor; i++) {
    const name = randomName();
    cases.push({
      category: 'competitor',
      expectedQualified: false,
      payload: {
        'First Name': name.firstName,
        'Last Name': name.lastName,
        'Title': randomFrom(['CEO', 'Founder', 'Marketing Director', 'SEO Specialist']),
        'Company Name': randomFrom(['Digital Marketing Agency', 'SEO Experts', 'Lead Gen Solutions', 'Growth Hackers Inc', 'PPC Masters']),
        'Industry': randomFrom(['Marketing & Advertising', 'Digital Marketing', 'SEO Services']),
        'Website': 'https://www.digitalagency.com',
        'State': randomFrom(STATES)
      }
    });
  }
  
  // Edge cases
  for (let i = 0; i < distribution.edgeCase; i++) {
    const name = randomName();
    const edgeType = i % 5;
    
    switch (edgeType) {
      case 0: // Attorney title but at insurance company
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
        break;
      case 1: // Partner title but at consulting firm
        cases.push({
          category: 'edge_partner_consulting',
          expectedQualified: false,
          payload: {
            'First Name': name.firstName, 'Last Name': name.lastName,
            'Title': 'Partner',
            'Company Name': 'McKinsey & Company',
            'Industry': 'Management Consulting'
          }
        });
        break;
      case 2: // Legal title with typos
        cases.push({
          category: 'edge_typos',
          expectedQualified: true,
          payload: {
            'First Name': name.firstName, 'Last Name': name.lastName,
            'Title': 'Managng Partnr',
            'Company Name': 'Smith Law Offces',
            'Industry': 'Legl Services'
          }
        });
        break;
      case 3: // Foreign/international law firm
        cases.push({
          category: 'edge_international',
          expectedQualified: true,
          payload: {
            'First Name': name.firstName, 'Last Name': name.lastName,
            'Title': 'Senior Partner',
            'Company Name': 'Baker McKenzie LLP',
            'Industry': 'Legal Services',
            'State': ''
          }
        });
        break;
      case 4: // Solo practitioner
        cases.push({
          category: 'edge_solo',
          expectedQualified: true,
          payload: {
            'First Name': name.firstName, 'Last Name': name.lastName,
            'Title': 'Attorney at Law',
            'Company Name': `Law Office of ${name.firstName} ${name.lastName}`,
            'Industry': 'Legal Services',
            'Employee Count': '1'
          }
        });
        break;
    }
  }
  
  // Minimal data cases
  for (let i = 0; i < distribution.minimal; i++) {
    const name = randomName();
    const minimalType = i % 3;
    
    switch (minimalType) {
      case 0: // Only name
        cases.push({
          category: 'minimal_name_only',
          expectedQualified: false,
          payload: {
            'First Name': name.firstName,
            'Last Name': name.lastName
          }
        });
        break;
      case 1: // Name + company only
        cases.push({
          category: 'minimal_name_company',
          expectedQualified: 'maybe',
          payload: {
            'First Name': name.firstName,
            'Last Name': name.lastName,
            'Company Name': randomFrom(LAW_FIRM_NAMES)
          }
        });
        break;
      case 2: // Empty payload
        cases.push({
          category: 'minimal_empty',
          expectedQualified: false,
          payload: {}
        });
        break;
    }
  }
  
  return cases;
}

// =============================================================================
// RUN TESTS
// =============================================================================

async function runTest(testCase, index) {
  return new Promise((resolve) => {
    const postData = JSON.stringify(testCase.payload);
    
    const req = http.request({
      hostname: 'localhost',
      port: 9100,
      path: '/rb2b/webhook',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData)
      },
      timeout: 15000 // 15 second timeout for website scraping
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          resolve({
            index,
            category: testCase.category,
            expected: testCase.expectedQualified,
            actual: result.qualified,
            confidence: result.confidence,
            match: testCase.expectedQualified === 'maybe' || result.qualified === testCase.expectedQualified,
            payload: testCase.payload,
            result
          });
        } catch(e) {
          resolve({
            index, category: testCase.category,
            expected: testCase.expectedQualified,
            actual: 'error',
            error: e.message,
            match: false
          });
        }
      });
    });
    
    req.on('error', (err) => {
      resolve({
        index, category: testCase.category,
        expected: testCase.expectedQualified,
        actual: 'error',
        error: err.message,
        match: false
      });
    });
    
    req.on('timeout', () => {
      req.destroy();
      resolve({
        index, category: testCase.category,
        expected: testCase.expectedQualified,
        actual: 'timeout',
        match: false
      });
    });
    
    req.write(postData);
    req.end();
  });
}

async function runAllTests(count = 1000, batchSize = 10) {
  console.log(`\n🧪 RB2B WEBHOOK STRESS TEST - ${count} CASES\n`);
  console.log('='.repeat(60));
  
  const testCases = generateTestCases(count);
  const results = [];
  const startTime = Date.now();
  
  // Run in batches to avoid overwhelming the server
  for (let i = 0; i < testCases.length; i += batchSize) {
    const batch = testCases.slice(i, i + batchSize);
    const batchResults = await Promise.all(
      batch.map((tc, j) => runTest(tc, i + j))
    );
    results.push(...batchResults);
    
    // Progress
    const pct = Math.round((results.length / count) * 100);
    process.stdout.write(`\r  Progress: ${results.length}/${count} (${pct}%) `);
    
    // Small delay between batches
    await new Promise(r => setTimeout(r, 100));
  }
  
  const duration = (Date.now() - startTime) / 1000;
  console.log(`\n\n✅ Completed in ${duration.toFixed(1)}s\n`);
  
  // ==========================================================================
  // ANALYSIS
  // ==========================================================================
  
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
  const totalErrors = results.filter(r => r.actual === 'error' || r.actual === 'timeout').length;
  
  console.log('\n' + '='.repeat(60));
  console.log('📈 OVERALL METRICS\n');
  console.log(`  Total Tests:      ${count}`);
  console.log(`  Correct:          ${totalMatches} (${((totalMatches/count)*100).toFixed(1)}%)`);
  console.log(`  False Positives:  ${totalFP} (letting non-lawyers through)`);
  console.log(`  False Negatives:  ${totalFN} (missing real lawyers)`);
  console.log(`  Errors/Timeouts:  ${totalErrors}`);
  console.log(`  Throughput:       ${(count/duration).toFixed(1)} tests/sec`);
  
  // Show examples of failures
  if (totalFP > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('🚨 FALSE POSITIVE EXAMPLES (non-lawyers that got through):\n');
    const fpExamples = results.filter(r => r.actual === true && r.expected === false).slice(0, 5);
    for (const ex of fpExamples) {
      console.log(`  • ${ex.payload['First Name']} ${ex.payload['Last Name']}`);
      console.log(`    Title: ${ex.payload['Title']}`);
      console.log(`    Company: ${ex.payload['Company Name']}`);
      console.log(`    Industry: ${ex.payload['Industry']}`);
      console.log(`    Confidence: ${ex.confidence}`);
      console.log('');
    }
  }
  
  if (totalFN > 0) {
    console.log('\n' + '='.repeat(60));
    console.log('🚨 FALSE NEGATIVE EXAMPLES (real lawyers that were missed):\n');
    const fnExamples = results.filter(r => r.actual === false && r.expected === true).slice(0, 5);
    for (const ex of fnExamples) {
      console.log(`  • ${ex.payload['First Name']} ${ex.payload['Last Name']}`);
      console.log(`    Title: ${ex.payload['Title']}`);
      console.log(`    Company: ${ex.payload['Company Name']}`);
      console.log(`    Industry: ${ex.payload['Industry']}`);
      console.log(`    Result: ${JSON.stringify(ex.result)}`);
      console.log('');
    }
  }
  
  // Save full results
  const fs = require('fs');
  const reportPath = `/home/ec2-user/clawd/services/lead-webhook/stress-test-results-${Date.now()}.json`;
  fs.writeFileSync(reportPath, JSON.stringify({
    summary: {
      total: count,
      correct: totalMatches,
      falsePositives: totalFP,
      falseNegatives: totalFN,
      errors: totalErrors,
      accuracy: ((totalMatches/count)*100).toFixed(1) + '%',
      duration: duration.toFixed(1) + 's'
    },
    categories,
    failures: {
      falsePositives: results.filter(r => r.actual === true && r.expected === false),
      falseNegatives: results.filter(r => r.actual === false && r.expected === true)
    },
    allResults: results
  }, null, 2));
  
  console.log(`\n📁 Full results saved to: ${reportPath}`);
  
  return { categories, totalMatches, totalFP, totalFN, totalErrors, count };
}

// Run the tests
runAllTests(1000, 20);
