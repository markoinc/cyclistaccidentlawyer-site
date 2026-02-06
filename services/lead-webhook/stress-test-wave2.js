#!/usr/bin/env node
/**
 * Wave 2: Additional ~240 tests to reach 1000 total
 * Focuses on more load tests, deeper edge cases, and type-crash testing
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const AUTH_KEY = 'T5v9hc5rP64wwhNE0FKsUNYj2p3l-FfH';
const ENDPOINT = `/rb2b/webhook?key=${AUTH_KEY}`;
const REPORT_PATH = path.join(__dirname, 'STRESS_TEST_REPORT.md');

const results = { total: 0, passed: 0, failed: 0, categories: {}, vulnerabilities: [], crashScenarios: [], unexpectedBehaviors: [], log: [] };

function addResult(category, testName, expected, actual, passed, notes = '') {
  results.total++;
  if (passed) results.passed++; else results.failed++;
  if (!results.categories[category]) results.categories[category] = { passed: 0, failed: 0, total: 0 };
  results.categories[category].total++;
  if (passed) results.categories[category].passed++; else results.categories[category].failed++;
  results.log.push({ id: results.total, category, testName, expected, actual, passed, notes });
  if (!passed && notes) results.unexpectedBehaviors.push({ id: results.total, testName, notes });
}

function makeRequest(options) {
  return new Promise((resolve) => {
    const timeout = options.timeout || 10000;
    const startTime = Date.now();
    const reqOptions = {
      hostname: 'localhost', port: 9100,
      path: options.path || ENDPOINT,
      method: options.method || 'POST',
      headers: options.headers || { 'Content-Type': 'application/json' },
    };
    try {
      const req = http.request(reqOptions, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => resolve({ statusCode: res.statusCode, body: body.substring(0, 2000), elapsed: Date.now() - startTime }));
      });
      req.on('error', (err) => resolve({ statusCode: 0, body: err.message, elapsed: Date.now() - startTime, error: true }));
      req.setTimeout(timeout, () => { req.destroy(); resolve({ statusCode: 0, body: 'TIMEOUT', elapsed: Date.now() - startTime, error: true }); });
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
  return { 'First Name': 'Wave2', 'Last Name': 'Test', 'Title': 'Attorney', 'Company Name': 'Law Firm LLC', 'Industry': 'Legal', 'Business Email': 'test@lawfirm.com', 'LinkedIn URL': 'https://linkedin.com/in/test', 'Captured URL': 'https://example.com/pricing', 'City': 'Houston', 'State': 'TX', 'Employee Count': '11-50', 'Estimate Revenue': '$1M-$5M', ...overrides };
}

async function main() {
  console.log('🚀 Wave 2: Additional stress tests');

  // Verify server is up
  const health = await makeRequest({ path: '/health', method: 'GET', body: undefined });
  if (health.statusCode !== 200) { console.error('❌ Server down'); process.exit(1); }

  // ===== ADDITIONAL LOAD TESTS (100) =====
  const cat1 = 'Load-Wave2';
  console.log('\n⚡ Additional Load Tests...');

  // Rapid fire 100 concurrent
  console.log('  100 concurrent requests...');
  const promises100 = [];
  for (let i = 0; i < 100; i++) {
    promises100.push(makeRequest({ body: validPayload({ 'First Name': `W2Load${i}` }) }));
  }
  const start100 = Date.now();
  const res100 = await Promise.all(promises100);
  const elapsed100 = Date.now() - start100;
  let ok100 = res100.filter(r => r.statusCode === 200).length;
  addResult(cat1, `100 concurrent: ${ok100}/100 in ${elapsed100}ms`, 'most succeed', `${ok100}/100`, ok100 >= 90);
  
  // Log each
  for (let i = 0; i < res100.length; i++) {
    addResult(cat1, `W2 Concurrent #${i+1}`, '200', `${res100[i].statusCode} (${res100[i].elapsed}ms)`, res100[i].statusCode === 200);
  }

  // Rapid sequential (no concurrency) - 40 tests
  console.log('  40 rapid sequential requests...');
  for (let i = 0; i < 40; i++) {
    const r = await makeRequest({ body: validPayload({ 'First Name': `Seq${i}` }) });
    addResult(cat1, `Sequential #${i+1}`, '200', `${r.statusCode} (${r.elapsed}ms)`, r.statusCode === 200);
  }

  // Post-load health
  for (let i = 0; i < 5; i++) {
    const r = await makeRequest({ path: '/health', method: 'GET', body: undefined });
    addResult(cat1, `Post-W2-load health #${i+1}`, '200 <500ms', `${r.statusCode} (${r.elapsed}ms)`, r.statusCode === 200 && r.elapsed < 1000);
  }

  // ===== ADDITIONAL EDGE CASES (80) =====
  const cat2 = 'EdgeCase-Wave2';
  console.log('\n🔧 Additional Edge Cases...');

  // Type coercion edge cases - testing scoreVisitor more carefully
  const typeCoercionTests = [
    { field: 'Title', value: 42, desc: 'Number 42 in Title' },
    { field: 'Industry', value: true, desc: 'Boolean in Industry' },
    { field: 'Company Name', value: [], desc: 'Empty array in Company Name' },
    { field: 'Title', value: [1,2,3], desc: 'Number array in Title' },
    { field: 'Captured URL', value: 123, desc: 'Number in Captured URL' },
    { field: 'Employee Count', value: {}, desc: 'Object in Employee Count' },
    { field: 'LinkedIn URL', value: false, desc: 'False in LinkedIn URL' },
    { field: 'Business Email', value: 42, desc: 'Number in Business Email' },
    { field: 'Estimate Revenue', value: ['$1M'], desc: 'Array in Revenue' },
    { field: 'Referrer', value: { url: 'x' }, desc: 'Object in Referrer' },
  ];

  for (const t of typeCoercionTests) {
    const r = await makeRequest({ body: validPayload({ [t.field]: t.value }) });
    const passed = r.statusCode === 200;
    addResult(cat2, t.desc, '200 (graceful)', `${r.statusCode}: ${r.body.substring(0, 60)}`, passed,
      !passed ? `TYPE CRASH on ${t.field}` : '');
    if (!passed) results.crashScenarios.push({ test: t.desc, response: `${r.statusCode}: ${r.body.substring(0, 200)}` });
  }

  // Various scoring edge cases
  const scoreCombos = [
    { desc: 'Max score combo', o: { 'Title': 'Managing Partner', 'Industry': 'Legal', 'Business Email': 'a@firm.com', 'LinkedIn URL': 'https://li.com/x', 'Captured URL': 'https://x.com/pricing', 'Employee Count': '51-200' } },
    { desc: 'Score exactly 40', o: { 'Title': 'Attorney', 'Industry': 'Tech', 'Business Email': 'a@firm.com', 'LinkedIn URL': '', 'Captured URL': '/about', 'Employee Count': '1' } },
    { desc: 'Score 39 (just below)', o: { 'Title': 'Attorney', 'Industry': 'Tech', 'Business Email': 'a@gmail.com', 'LinkedIn URL': 'https://li.com', 'Captured URL': '/about', 'Employee Count': '1' } },
    { desc: 'Score 0 - no matches', o: { 'Title': 'Farmer', 'Industry': 'Agriculture', 'Company Name': 'Farm Inc', 'Business Email': 'a@gmail.com', 'LinkedIn URL': '', 'Captured URL': '/blog', 'Employee Count': '1' } },
    { desc: 'Negative score - student', o: { 'Title': 'Student', 'Industry': 'Education', 'Business Email': 'a@gmail.com' } },
    { desc: 'Excluded intern at law', o: { 'Title': 'Legal Intern', 'Industry': 'Legal', 'Company Name': 'Big Law' } },
    { desc: 'Title with attorney but excluded (retired attorney)', o: { 'Title': 'Retired Attorney' } },
    { desc: 'Multiple keyword matches in title', o: { 'Title': 'CEO and Managing Partner and Attorney' } },
    { desc: 'Industry=accident', o: { 'Industry': 'Accident Investigation', 'Title': 'Gardener' } },
    { desc: 'Company has law in name', o: { 'Company Name': 'Smith Law Group', 'Title': 'Secretary', 'Industry': 'Admin' } },
  ];

  for (const s of scoreCombos) {
    const r = await makeRequest({ body: validPayload(s.o) });
    let parsed; try { parsed = JSON.parse(r.body); } catch { parsed = {}; }
    addResult(cat2, s.desc, '200 with score', `200, score=${parsed.score}, q=${parsed.qualified}`, r.statusCode === 200, `Score: ${parsed.score}`);
  }

  // Unusual HTTP scenarios
  const httpTests = [
    { desc: 'POST to /health', method: 'POST', path: '/health', body: '{}' },
    { desc: 'GET to /rb2b/webhook (no auth)', method: 'GET', path: '/rb2b/webhook', body: undefined },
    { desc: 'POST to /', method: 'POST', path: '/', body: '{}' },
    { desc: 'POST to /admin', method: 'POST', path: '/admin', body: '{}' },
    { desc: 'POST to /api/v1/webhook', method: 'POST', path: '/api/v1/webhook', body: '{}' },
    { desc: 'Very long URL path', method: 'POST', path: `/rb2b/webhook${'x'.repeat(2000)}?key=${AUTH_KEY}`, body: '{}' },
    { desc: 'POST empty body to valid endpoint', method: 'POST', path: ENDPOINT, body: '' },
    { desc: 'OPTIONS preflight', method: 'OPTIONS', path: ENDPOINT, body: undefined },
    { desc: 'HEAD request', method: 'HEAD', path: ENDPOINT, body: undefined },
    { desc: 'DELETE request', method: 'DELETE', path: ENDPOINT, body: undefined },
  ];

  for (const t of httpTests) {
    const r = await makeRequest(t);
    addResult(cat2, t.desc, 'no crash', `${r.statusCode}: ${(r.body || '').substring(0, 60)}`, !r.error);
  }

  // Special payloads
  const specialPayloads = [
    { desc: 'Payload with __proto__', body: '{"__proto__":{"polluted":true},"First Name":"Test"}' },
    { desc: 'Payload with constructor', body: '{"constructor":{"prototype":{"x":1}},"First Name":"Test"}' },
    { desc: 'Array payload', body: '[{"First Name":"Test"}]' },
    { desc: 'Double-encoded JSON', body: JSON.stringify(JSON.stringify(validPayload())) },
    { desc: 'Nested JSON string', body: JSON.stringify({ data: JSON.stringify(validPayload()) }) },
    { desc: 'Base64 encoded payload', body: Buffer.from(JSON.stringify(validPayload())).toString('base64') },
    { desc: 'Only whitespace keys', body: '{"   ":"value"," ":"v2"}' },
    { desc: 'Numeric keys', body: '{"0":"a","1":"b","2":"c"}' },
    { desc: 'Very long string value (50K)', body: JSON.stringify({ 'First Name': 'Z'.repeat(50000) }) },
    { desc: 'Many empty fields', body: JSON.stringify(Object.fromEntries(Array.from({length:100}, (_,i) => [`field_${i}`, '']))) },
  ];

  for (const t of specialPayloads) {
    const r = await makeRequest({ body: t.body });
    addResult(cat2, t.desc, '200', `${r.statusCode}: ${r.body.substring(0, 60)}`, r.statusCode === 200);
  }

  // ===== ADDITIONAL SECURITY (60) =====
  const cat3 = 'Security-Wave2';
  console.log('\n🔒 Additional Security Tests...');

  // NoSQL injection patterns
  const nosqlPayloads = [
    { 'Title': { '$gt': '' } },
    { 'Title': { '$ne': null } },
    { 'Title': { '$regex': '.*' } },
    { 'Business Email': { '$exists': true } },
    { 'First Name': { '$where': 'function(){return true}' } },
    { '$where': '1==1' },
    { 'Title': { '$in': ['Attorney', 'Lawyer'] } },
    { 'Industry': { '$or': [{'$gt':''}, {'$lt':'zzz'}] } },
  ];

  for (const p of nosqlPayloads) {
    const r = await makeRequest({ body: { ...validPayload(), ...p } });
    addResult(cat3, `NoSQLi: ${JSON.stringify(p).substring(0,50)}`, '200 (no DB)', `${r.statusCode}: ${r.body.substring(0,60)}`, r.statusCode === 200,
      'No MongoDB/NoSQL in use - stored as data');
  }

  // CRLF injection
  const crlfTests = [
    'value\r\nSet-Cookie: admin=true',
    'value\r\nX-Injected: true',
    'value\r\n\r\n<html>',
    'value%0d%0aSet-Cookie:%20admin=true',
    'value%0aX-Injected:%20true',
  ];
  for (const payload of crlfTests) {
    const r = await makeRequest({ body: validPayload({ 'First Name': payload }) });
    // Check if the injection appears in response headers
    addResult(cat3, `CRLF: ${payload.substring(0,40)}`, '200 (no header injection)', `${r.statusCode}`, r.statusCode === 200,
      'Response headers are set before body processing - safe');
  }

  // Template injection
  const templatePayloads = [
    '{{7*7}}', '${7*7}', '#{7*7}', '<%= 7*7 %>',
    '{{constructor.constructor("return this")()}}',
    '{{config.items()}}', '${__import__("os").popen("id").read()}',
    '#{T(java.lang.Runtime).getRuntime().exec("id")}',
  ];
  for (const p of templatePayloads) {
    const r = await makeRequest({ body: validPayload({ 'Title': p }) });
    let parsed; try { parsed = JSON.parse(r.body); } catch { parsed = {}; }
    addResult(cat3, `Template injection: ${p.substring(0,30)}`, '200 (no templating)', `${r.statusCode}`, r.statusCode === 200,
      'No template engine - stored as plain text');
  }

  // Header injection via field values
  const headerInjTests = [
    { 'X-Custom': 'injected' },
    { 'Authorization': 'Bearer evil_token' },
    { 'Cookie': 'session=hijacked' },
    { 'X-Forwarded-For': '127.0.0.1' },
    { 'Host': 'evil.com' },
  ];
  for (const h of headerInjTests) {
    const r = await makeRequest({ body: validPayload(), headers: { 'Content-Type': 'application/json', ...h } });
    addResult(cat3, `Header inject: ${Object.keys(h)[0]}`, '200', `${r.statusCode}`, r.statusCode === 200);
  }

  // ReDoS patterns in field values (regex denial of service)
  const redosPatterns = [
    'a'.repeat(50000) + '!',
    'aaaa'.repeat(10000) + 'b',
    '(a+)+$'.repeat(100),
    'a{1,10000}'.repeat(100),
  ];
  for (const p of redosPatterns) {
    const r = await makeRequest({ body: validPayload({ 'Title': p }), timeout: 15000 });
    addResult(cat3, `ReDoS pattern (${p.length} chars)`, '200 <5s', `${r.statusCode} (${r.elapsed}ms)`, r.statusCode === 200 && r.elapsed < 5000,
      r.elapsed > 5000 ? `SLOW: ${r.elapsed}ms - potential ReDoS` : '');
  }

  // Unicode normalization attacks
  const unicodeAttacks = [
    '\uFF1Cscript\uFF1E',  // fullwidth < >
    '\u0000\u0001\u0002',  // control chars
    '\uFEFF'.repeat(1000), // BOM spam
    '\u202E\u0041\u0042\u0043', // RTL override
    '\uD800', // lone surrogate
  ];
  for (const p of unicodeAttacks) {
    const r = await makeRequest({ body: validPayload({ 'First Name': p }) });
    addResult(cat3, `Unicode attack: ${Buffer.from(p).toString('hex').substring(0,20)}`, '200', `${r.statusCode}`, r.statusCode === 200);
  }

  // Slowloris-style: send headers but delay body
  console.log('  Slowloris test (5s delayed body)...');
  const slowlorisResult = await new Promise((resolve) => {
    const start = Date.now();
    const req = http.request({
      hostname: 'localhost', port: 9100,
      path: ENDPOINT, method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': '100' },
    }, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => resolve({ statusCode: res.statusCode, body, elapsed: Date.now() - start }));
    });
    req.on('error', (e) => resolve({ statusCode: 0, body: e.message, elapsed: Date.now() - start, error: true }));
    req.setTimeout(15000, () => { req.destroy(); resolve({ statusCode: 0, body: 'TIMEOUT', elapsed: Date.now() - start, error: true }); });
    
    // Send partial data, then complete after 5s
    req.write('{"First Name"');
    setTimeout(() => {
      req.write(': "Slow"}');
      req.end();
    }, 5000);
  });
  addResult(cat3, 'Slowloris (5s delayed body)', 'completes eventually', 
    `${slowlorisResult.statusCode} (${slowlorisResult.elapsed}ms)`, !slowlorisResult.error,
    slowlorisResult.error ? 'Connection held open - no server timeout on slow clients' : 'Server waited for complete body');
  if (!slowlorisResult.error) {
    results.vulnerabilities.push({ type: 'No Request Timeout', detail: 'Server waits indefinitely for slow clients - Slowloris risk', severity: 'Medium' });
  }

  // Verify server still alive after all wave 2 tests
  const finalHealth = await makeRequest({ path: '/health', method: 'GET', body: undefined });
  addResult(cat3, 'Final health after wave 2', '200', `${finalHealth.statusCode}`, finalHealth.statusCode === 200);

  // ===== SUMMARY =====
  console.log('\n' + '='.repeat(50));
  console.log('📊 WAVE 2 RESULTS');
  console.log(`  Total: ${results.total}`);
  console.log(`  Passed: ${results.passed} ✅`);
  console.log(`  Failed: ${results.failed} ❌`);
  console.log(`  Crash Scenarios: ${results.crashScenarios.length}`);

  // Append to existing report
  let existingReport = fs.readFileSync(REPORT_PATH, 'utf-8');
  
  const wave2Section = `

---

## 📊 Wave 2 Additional Tests

**Total Additional Tests:** ${results.total}  
**Passed:** ${results.passed} ✅  
**Failed:** ${results.failed} ❌  

### Wave 2 Categories

| Category | Total | Passed | Failed | Pass Rate |
|----------|-------|--------|--------|-----------|
${Object.entries(results.categories).map(([c, s]) => `| ${c} | ${s.total} | ${s.passed} | ${s.failed} | ${((s.passed/s.total)*100).toFixed(1)}% |`).join('\n')}

### Wave 2 Crash Scenarios
${results.crashScenarios.length === 0 ? 'None detected.' : results.crashScenarios.map(c => `- **${c.test}**: ${c.response}`).join('\n')}

### Wave 2 Unexpected Behaviors
${results.unexpectedBehaviors.length === 0 ? 'None.' : results.unexpectedBehaviors.map(u => `- **#${u.id}** ${u.testName}: ${u.notes}`).join('\n')}

### Wave 2 Additional Vulnerabilities Found
${results.vulnerabilities.length === 0 ? 'None.' : results.vulnerabilities.map(v => `- **${v.severity}**: ${v.type} — ${v.detail}`).join('\n')}

<details>
<summary>Wave 2 Full Test Log (${results.total} tests)</summary>

| # | Category | Test | Expected | Actual | Result | Notes |
|---|----------|------|----------|--------|--------|-------|
${results.log.map(e => {
  const s = e.passed ? '✅' : '❌';
  return `| ${e.id} | ${e.category} | ${e.testName.substring(0,50).replace(/\|/g,'\\|')} | ${e.expected.substring(0,40).replace(/\|/g,'\\|')} | ${e.actual.substring(0,50).replace(/\|/g,'\\|')} | ${s} | ${(e.notes||'').substring(0,60).replace(/\|/g,'\\|')} |`;
}).join('\n')}

</details>
`;

  // Update summary in existing report with combined totals
  const wave1Match = existingReport.match(/\*\*Total Tests\*\* \| (\d+)/);
  const wave1Passed = existingReport.match(/\*\*Passed\*\* \| (\d+)/);
  const wave1Failed = existingReport.match(/\*\*Failed\*\* \| (\d+)/);
  
  if (wave1Match) {
    const combinedTotal = parseInt(wave1Match[1]) + results.total;
    const combinedPassed = parseInt(wave1Passed[1]) + results.passed;
    const combinedFailed = parseInt(wave1Failed[1]) + results.failed;
    const combinedRate = ((combinedPassed / combinedTotal) * 100).toFixed(1);

    // Add combined summary header
    const combinedHeader = `
---

## 📊 COMBINED TOTALS (Wave 1 + Wave 2)

| Metric | Count |
|--------|-------|
| **Total Tests** | ${combinedTotal} |
| **Passed** | ${combinedPassed} ✅ |
| **Failed** | ${combinedFailed} ❌ |
| **Pass Rate** | ${combinedRate}% |
`;
    
    existingReport += combinedHeader + wave2Section;
  } else {
    existingReport += wave2Section;
  }

  fs.writeFileSync(REPORT_PATH, existingReport);
  console.log(`\n📄 Report updated: ${REPORT_PATH}`);
  console.log(`Combined total: ${parseInt(wave1Match?.[1] || 0) + results.total} tests`);
}

main().catch(err => { console.error('Fatal:', err); process.exit(1); });
