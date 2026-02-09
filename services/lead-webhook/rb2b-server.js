const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = 9100;
const LOG_DIR = path.join(__dirname, 'logs');
const SLACK_CHANNEL = 'C0A7RNYC6CF'; // #rb2b-notifications

// Load credentials
let SLACK_BOT_TOKEN;
try {
  SLACK_BOT_TOKEN = fs.readFileSync(path.join(require('os').homedir(), '.config/slack/bot_token'), 'utf8').trim();
} catch(e) {
  SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN || '';
}

let BETTERCONTACT_API_KEY;
try {
  const creds = JSON.parse(fs.readFileSync(path.join(require('os').homedir(), '.config/bettercontact/credentials.json'), 'utf8'));
  BETTERCONTACT_API_KEY = creds.api_key;
} catch(e) {
  BETTERCONTACT_API_KEY = process.env.BETTERCONTACT_API_KEY || '';
}

const MAX_BODY_SIZE = 512 * 1024;
if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });

// =============================================================================
// RB2B PAYLOAD NORMALIZATION
// Convert RB2B format to our internal format
// =============================================================================

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
    industry: payload['Industry'] || '',
    employeeCount: payload['Employee Count'] || '',
    estimatedRevenue: payload['Estimate Revenue'] || '',
    city: payload['City'] || '',
    state: payload['State'] || '',
    zipcode: payload['Zipcode'] || '',
    seenAt: payload['Seen At'] || '',
    referrer: payload['Referrer'] || '',
    capturedUrl: payload['Captured URL'] || '',
    tags: payload['Tags'] || '',
    // For repeat visitors
    visitHistory: payload['Visit History'] || null,
    // Original payload for logging
    _raw: payload
  };
}

// =============================================================================
// WEBSITE VERIFICATION - Check if it's a law firm
// =============================================================================

const LAW_FIRM_INDICATORS = {
  // Strong indicators (in page content)
  strongKeywords: [
    'personal injury', 'car accident attorney', 'truck accident', 'motorcycle accident',
    'slip and fall', 'wrongful death', 'medical malpractice', 'workers compensation',
    'injury lawyer', 'injury attorney', 'accident lawyer', 'accident attorney',
    'law firm', 'attorneys at law', 'legal services', 'free consultation',
    'case evaluation', 'no fee unless we win', 'contingency fee',
    'practice areas', 'our attorneys', 'attorney profiles', 'meet our lawyers'
  ],
  // Moderate indicators
  moderateKeywords: [
    'attorney', 'lawyer', 'legal', 'law office', 'esquire', 'esq.',
    'litigation', 'trial attorney', 'courtroom', 'verdict', 'settlement',
    'bar association', 'admitted to practice'
  ],
  // Domain patterns that indicate law firms
  domainPatterns: [
    /law\.com$/i, /legal\.com$/i, /attorney/i, /lawyer/i,
    /lawfirm/i, /lawoffice/i, /esq/i, /legal/i
  ],
  // Title patterns for decision makers (broadened per Marko 2026-02-06)
  decisionMakerTitles: [
    // Partners & Principals
    'partner', 'managing partner', 'founding partner', 'senior partner', 'junior partner',
    'owner', 'founder', 'co-founder', 'principal', 'of counsel', 'shareholder',
    // C-Suite & Directors
    'ceo', 'president', 'chief executive', 'managing director', 'executive director',
    'coo', 'cfo', 'general counsel',
    'marketing director', 'cmo', 'chief marketing', 'director of marketing',
    'vp', 'vice president', 'head of', 'director of',
    // Attorneys (all levels)
    'attorney', 'lawyer', 'associate attorney', 'senior associate', 'staff attorney',
    'trial attorney', 'litigator', 'counsel',
    // Business Development & Intake
    'business development', 'intake director', 'intake manager', 'intake coordinator',
    'case manager', 'client relations',
    // Admin with authority
    'office manager', 'legal secretary', 'executive secretary', 'legal administrator',
    'firm administrator', 'operations manager'
  ],
  // Titles to exclude (only truly non-decision-makers)
  excludeTitles: [
    'paralegal', 'legal assistant', 'receptionist',
    'intern', 'clerk', 'student', 'extern'
  ]
};

async function fetchWebsite(url, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const protocol = urlObj.protocol === 'https:' ? https : http;
    
    const req = protocol.get(url, { 
      timeout,
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; KuriosBot/1.0; +https://kuriosbrand.com)'
      }
    }, (res) => {
      // Follow redirects
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        fetchWebsite(res.headers.location, timeout).then(resolve).catch(reject);
        return;
      }
      
      let body = '';
      res.on('data', chunk => {
        body += chunk;
        if (body.length > 500000) { // Max 500KB
          res.destroy();
          resolve(body);
        }
      });
      res.on('end', () => resolve(body));
    });
    
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('timeout'));
    });
    req.on('error', reject);
  });
}

async function verifyLawFirm(data) {
  const result = {
    isLawFirm: false,
    isDecisionMaker: false,
    confidence: 0,
    reasons: [],
    websiteChecked: false
  };

  const title = (data.jobTitle || '').toLowerCase();
  const industry = (data.industry || '').toLowerCase();
  const company = (data.companyName || '').toLowerCase();
  const website = data.website || '';

  // 1. Check Industry field (quick win)
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

  // 3. Check title for legal role (case-insensitive comparison)
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

  // 4. Check for excluded titles (case-insensitive)
  if (LAW_FIRM_INDICATORS.excludeTitles.some(t => title.includes(t.toLowerCase()))) {
    result.confidence -= 30;
    result.reasons.push(`Non-decision maker title: "${data.jobTitle}"`);
  }

  // 5. Check website domain patterns
  if (website) {
    try {
      const domain = new URL(website.startsWith('http') ? website : `https://${website}`).hostname;
      if (LAW_FIRM_INDICATORS.domainPatterns.some(p => p.test(domain))) {
        result.confidence += 20;
        result.reasons.push(`Domain suggests law firm: ${domain}`);
      }
    } catch(e) {}
  }

  // 6. Scrape website if we're not confident enough
  if (result.confidence < 60 && website) {
    try {
      const fullUrl = website.startsWith('http') ? website : `https://${website}`;
      console.log(`[VERIFY] Fetching website: ${fullUrl}`);
      
      const html = await fetchWebsite(fullUrl);
      result.websiteChecked = true;
      
      const lowerHtml = html.toLowerCase();
      
      // Check for strong indicators
      const strongMatches = LAW_FIRM_INDICATORS.strongKeywords.filter(kw => lowerHtml.includes(kw));
      if (strongMatches.length >= 2) {
        result.confidence += 40;
        result.reasons.push(`Website has law firm content: ${strongMatches.slice(0, 3).join(', ')}`);
      } else if (strongMatches.length === 1) {
        result.confidence += 20;
        result.reasons.push(`Website mentions: ${strongMatches[0]}`);
      }
      
      // Check for moderate indicators
      const moderateMatches = LAW_FIRM_INDICATORS.moderateKeywords.filter(kw => lowerHtml.includes(kw));
      if (moderateMatches.length >= 3) {
        result.confidence += 20;
        result.reasons.push(`Website legal terms: ${moderateMatches.slice(0, 3).join(', ')}`);
      }
      
    } catch(err) {
      result.reasons.push(`Website check failed: ${err.message}`);
    }
  }

  // Final determination
  result.isLawFirm = result.confidence >= 50;
  
  // Must be decision maker for final qualification
  if (!result.isDecisionMaker && result.isLawFirm) {
    // Check if title suggests any decision-making capacity
    const hasSomeAuthority = title.includes('director') || title.includes('manager') ||
      title.includes('head') || title.includes('chief') || title.includes('vp') ||
      title.includes('president') || title.includes('owner');
    
    if (!hasSomeAuthority) {
      result.reasons.push(`Not a decision maker - may not have authority`);
    } else {
      result.isDecisionMaker = true;
    }
  }

  return result;
}

// =============================================================================
// BETTERCONTACT ENRICHMENT
// =============================================================================

async function enrichWithBetterContact(data) {
  if (!BETTERCONTACT_API_KEY) {
    console.log('[ENRICH] No BetterContact API key, skipping enrichment');
    return null;
  }

  const enrichRequest = {
    data: [{
      first_name: data.firstName,
      last_name: data.lastName,
      company: data.companyName,
      company_domain: data.website ? new URL(data.website.startsWith('http') ? data.website : `https://${data.website}`).hostname : '',
      linkedin_url: data.linkedinUrl
    }],
    enrich_email_address: true,
    enrich_phone_number: true
  };

  console.log(`[ENRICH] Calling BetterContact for ${data.fullName}...`);

  return new Promise((resolve, reject) => {
    const postData = JSON.stringify(enrichRequest);
    
    const req = https.request({
      hostname: 'app.bettercontact.rocks',
      path: '/api/v2/async',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': BETTERCONTACT_API_KEY,
        'Content-Length': Buffer.byteLength(postData)
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.success && result.id) {
            console.log(`[ENRICH] Request queued: ${result.id}`);
            // Now poll for results
            pollEnrichmentResults(result.id, resolve, reject);
          } else {
            console.log(`[ENRICH] API response: ${body}`);
            resolve(null);
          }
        } catch(e) {
          console.log(`[ENRICH] Parse error: ${body}`);
          resolve(null);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('[ENRICH] Request error:', err.message);
      resolve(null);
    });
    
    req.write(postData);
    req.end();
  });
}

function pollEnrichmentResults(requestId, resolve, reject, attempts = 0) {
  const maxAttempts = 36; // 3 minutes with 5-second intervals
  
  if (attempts >= maxAttempts) {
    console.log(`[ENRICH] Timeout waiting for results: ${requestId}`);
    resolve(null);
    return;
  }

  setTimeout(() => {
    https.get({
      hostname: 'app.bettercontact.rocks',
      path: `/api/v2/async/${requestId}`,
      headers: { 'X-API-Key': BETTERCONTACT_API_KEY }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          
          if (result.status === 'terminated' && result.data && result.data.length > 0) {
            const enriched = result.data[0];
            console.log(`[ENRICH] ✅ Got results: email=${enriched.contact_email_address || 'N/A'}, phone=${enriched.contact_phone_number || 'N/A'}`);
            resolve({
              email: enriched.contact_email_address,
              emailStatus: enriched.contact_email_address_status,
              phone: enriched.contact_phone_number,
              provider: enriched.email_provider
            });
          } else if (result.status === 'processing' || result.status === 'pending') {
            console.log(`[ENRICH] Still processing (attempt ${attempts + 1}/${maxAttempts})...`);
            pollEnrichmentResults(requestId, resolve, reject, attempts + 1);
          } else {
            console.log(`[ENRICH] Unexpected status: ${result.status}`);
            resolve(null);
          }
        } catch(e) {
          console.log(`[ENRICH] Poll parse error: ${body}`);
          pollEnrichmentResults(requestId, resolve, reject, attempts + 1);
        }
      });
    }).on('error', (err) => {
      console.error('[ENRICH] Poll error:', err.message);
      pollEnrichmentResults(requestId, resolve, reject, attempts + 1);
    });
  }, 5000); // Poll every 5 seconds
}

// =============================================================================
// SLACK MESSAGE FORMATTING
// =============================================================================

function formatSlackMessage(data, verification, enrichment) {
  const name = data.fullName || 'Unknown';
  const title = data.jobTitle || 'N/A';
  const company = data.companyName || 'N/A';
  const location = [data.city, data.state].filter(Boolean).join(', ') || 'N/A';
  
  // Use enriched data if available, fall back to RB2B data
  const email = enrichment?.email || data.businessEmail || 'N/A';
  const phone = enrichment?.phone || 'N/A';
  const emailStatus = enrichment?.emailStatus ? ` (${enrichment.emailStatus})` : '';
  
  const blocks = [
    {
      type: 'header',
      text: {
        type: 'plain_text',
        text: `🎯 QUALIFIED LAW FIRM LEAD`,
        emoji: true
      }
    },
    {
      type: 'section',
      fields: [
        { type: 'mrkdwn', text: `*👤 Name:*\n${name}` },
        { type: 'mrkdwn', text: `*💼 Title:*\n${title}` },
        { type: 'mrkdwn', text: `*🏢 Company:*\n${company}` },
        { type: 'mrkdwn', text: `*🏭 Industry:*\n${data.industry || 'N/A'}` }
      ]
    },
    {
      type: 'section',
      fields: [
        { type: 'mrkdwn', text: `*📧 Email:*\n${email}${emailStatus}` },
        { type: 'mrkdwn', text: `*📱 Phone:*\n${phone}` },
        { type: 'mrkdwn', text: `*📍 Location:*\n${location}` },
        { type: 'mrkdwn', text: `*👥 Size:*\n${data.employeeCount || 'N/A'}` }
      ]
    }
  ];

  // Website & LinkedIn
  const links = [];
  if (data.website) links.push(`<${data.website}|🌐 Website>`);
  if (data.linkedinUrl) links.push(`<${data.linkedinUrl}|🔗 LinkedIn>`);
  
  if (links.length > 0) {
    blocks.push({
      type: 'section',
      text: { type: 'mrkdwn', text: `*Links:* ${links.join(' • ')}` }
    });
  }

  // Visitor behavior
  const behaviorParts = [];
  if (data.capturedUrl) behaviorParts.push(`Page: ${data.capturedUrl}`);
  if (data.referrer) behaviorParts.push(`From: ${data.referrer}`);
  if (data.tags) behaviorParts.push(`Tags: ${data.tags}`);
  
  if (behaviorParts.length > 0) {
    blocks.push({
      type: 'section',
      text: { type: 'mrkdwn', text: `*📊 Visit:* ${behaviorParts.join(' • ')}` }
    });
  }

  // Verification details
  blocks.push({
    type: 'context',
    elements: [
      { type: 'mrkdwn', text: `*Verification (${verification.confidence}% confidence):* ${verification.reasons.join(' · ')}` }
    ]
  });

  // Enrichment source
  if (enrichment) {
    blocks.push({
      type: 'context',
      elements: [
        { type: 'mrkdwn', text: `*Enriched via:* BetterContact${enrichment.provider ? ` (${enrichment.provider})` : ''}` }
      ]
    });
  }

  return { blocks };
}

// =============================================================================
// SLACK DELIVERY
// =============================================================================

async function sendToSlack(payload, channelId = SLACK_CHANNEL) {
  if (!SLACK_BOT_TOKEN) {
    console.log('[SLACK] No bot token, skipping');
    return;
  }

  const postData = JSON.stringify({
    channel: channelId,
    blocks: payload.blocks,
    text: 'New qualified law firm lead'
  });

  return new Promise((resolve) => {
    const req = https.request({
      hostname: 'slack.com',
      path: '/api/chat.postMessage',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SLACK_BOT_TOKEN}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(body);
          if (result.ok) {
            console.log(`[SLACK] ✅ Posted to ${channelId}`);
          } else {
            console.error(`[SLACK] ❌ Error: ${result.error}`);
          }
          resolve(result);
        } catch(e) {
          resolve(body);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('[SLACK] Error:', err.message);
      resolve(null);
    });
    
    req.write(postData);
    req.end();
  });
}

// =============================================================================
// HTTP SERVER
// =============================================================================

const server = http.createServer(async (req, res) => {
  const clientIp = req.headers['x-forwarded-for']?.split(',')[0]?.trim() || req.socket.remoteAddress;

  console.log(`[REQUEST] ${req.method} ${req.url} from ${clientIp}`);

  // Health check
  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'rb2b-webhook', version: '1.0' }));
    return;
  }

  // RB2B Webhook endpoint
  if (req.method === 'POST' && (req.url === '/rb2b/webhook' || req.url === '/rb2b' || req.url === '/webhook')) {
    let body = '';
    
    req.on('data', chunk => {
      if (body.length < MAX_BODY_SIZE) body += chunk;
    });

    req.on('end', async () => {
      const timestamp = new Date().toISOString();
      
      try {
        const payload = JSON.parse(body);
        
        // Log raw payload
        const rawLog = path.join(LOG_DIR, `rb2b-raw-${new Date().toISOString().slice(0, 10)}.jsonl`);
        fs.appendFileSync(rawLog, JSON.stringify({ timestamp, payload }) + '\n');

        // Normalize RB2B payload
        const data = normalizeRB2BPayload(payload);
        
        console.log(`[RB2B] Visitor: ${data.fullName} | ${data.jobTitle} @ ${data.companyName} | Industry: ${data.industry}`);

        // Skip test payloads
        if (data.firstName === 'RB2B' && data.lastName === 'Test Payload') {
          console.log('[RB2B] ✓ Test payload received successfully');
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ received: true, test: true }));
          return;
        }

        // STEP 1: Verify this is a law firm + decision maker
        const verification = await verifyLawFirm(data);
        
        console.log(`[VERIFY] ${data.fullName}: isLawFirm=${verification.isLawFirm}, isDecisionMaker=${verification.isDecisionMaker}, confidence=${verification.confidence}`);
        console.log(`[VERIFY] Reasons: ${verification.reasons.join(' | ')}`);

        // Log all visitors
        const allLog = path.join(LOG_DIR, `rb2b-all-${new Date().toISOString().slice(0, 10)}.jsonl`);
        fs.appendFileSync(allLog, JSON.stringify({
          timestamp, ...data,
          verification: {
            isLawFirm: verification.isLawFirm,
            isDecisionMaker: verification.isDecisionMaker,
            confidence: verification.confidence,
            reasons: verification.reasons
          }
        }) + '\n');

        // Not qualified - respond and exit
        if (!verification.isLawFirm || !verification.isDecisionMaker) {
          console.log(`[RB2B] ❌ Not qualified: ${data.fullName} - ${verification.reasons.join(', ')}`);
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ 
            received: true, 
            qualified: false, 
            reason: !verification.isLawFirm ? 'not_law_firm' : 'not_decision_maker'
          }));
          return;
        }

        // QUALIFIED! 
        console.log(`[RB2B] ✅ QUALIFIED: ${data.fullName} @ ${data.companyName}`);

        // STEP 2: Enrich with BetterContact
        let enrichment = null;
        if (!data.businessEmail || data.businessEmail === 'N/A') {
          enrichment = await enrichWithBetterContact(data);
        } else {
          console.log(`[ENRICH] Already have email: ${data.businessEmail}, skipping enrichment`);
          enrichment = { email: data.businessEmail };
        }

        // STEP 3: Post to Slack
        const slackMsg = formatSlackMessage(data, verification, enrichment);
        await sendToSlack(slackMsg);

        // Log qualified lead
        const qualifiedLog = path.join(LOG_DIR, 'rb2b-qualified.jsonl');
        fs.appendFileSync(qualifiedLog, JSON.stringify({
          timestamp, ...data,
          verification,
          enrichment
        }) + '\n');

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ 
          received: true, 
          qualified: true,
          confidence: verification.confidence,
          enriched: !!enrichment
        }));

      } catch (err) {
        console.error('[ERROR]', err.message, err.stack);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ received: true, error: err.message }));
      }
    });
    return;
  }

  // 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'not_found' }));
});

server.listen(PORT, () => {
  console.log(`[RB2B Webhook] Running on port ${PORT}`);
  console.log(`[RB2B Webhook] Endpoint: POST /rb2b/webhook`);
  console.log(`[RB2B Webhook] Health: GET /health`);
  console.log(`[RB2B Webhook] BetterContact: ${BETTERCONTACT_API_KEY ? 'configured' : 'NOT configured'}`);
  console.log(`[RB2B Webhook] Slack: ${SLACK_BOT_TOKEN ? 'configured' : 'NOT configured'}`);
});
