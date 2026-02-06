const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');

const PORT = 9100;
const LOG_DIR = path.join(__dirname, 'logs');
const SLACK_CHANNEL = 'C0A7RNYC6CF'; // #leadpipe-notifications

// Load Slack bot token
let SLACK_BOT_TOKEN;
try {
  SLACK_BOT_TOKEN = fs.readFileSync(path.join(require('os').homedir(), '.config/slack/bot_token'), 'utf8').trim();
} catch(e) {
  SLACK_BOT_TOKEN = process.env.SLACK_BOT_TOKEN || '';
}

// Load Leadpipe webhook secret
let WEBHOOK_SECRET;
try {
  const creds = JSON.parse(fs.readFileSync(path.join(require('os').homedir(), '.config/leadpipe/credentials.json'), 'utf8'));
  WEBHOOK_SECRET = creds.webhook_secret;
} catch(e) {
  WEBHOOK_SECRET = process.env.WEBHOOK_SECRET || 'T5v9hc5rP64wwhNE0FKsUNYj2p3l-FfH';
}
const MAX_BODY_SIZE = 512 * 1024; // 512KB max payload

// Ensure log directory exists
if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });

// --- Rate Limiting ---
const rateLimiter = {
  requests: new Map(), // ip -> { count, resetAt }
  failedAuth: new Map(), // ip -> { count, resetAt }
  
  check(ip, type = 'requests') {
    const map = type === 'auth' ? this.failedAuth : this.requests;
    const limit = type === 'auth' ? 10 : 120; // 10 failed auth/min, 120 req/min
    const now = Date.now();
    const entry = map.get(ip);
    
    if (!entry || now > entry.resetAt) {
      map.set(ip, { count: 1, resetAt: now + 60000 });
      return true;
    }
    
    entry.count++;
    if (entry.count > limit) return false;
    return true;
  },
  
  // Cleanup old entries every 5 min
  cleanup() {
    const now = Date.now();
    for (const [ip, entry] of this.requests) {
      if (now > entry.resetAt) this.requests.delete(ip);
    }
    for (const [ip, entry] of this.failedAuth) {
      if (now > entry.resetAt) this.failedAuth.delete(ip);
    }
  }
};

setInterval(() => rateLimiter.cleanup(), 300000);

// --- Sanitize strings for log safety ---
function sanitize(str) {
  if (typeof str !== 'string') return String(str || '');
  // Strip HTML tags and control characters
  return str.replace(/<[^>]*>/g, '').replace(/[\x00-\x08\x0B\x0C\x0E-\x1F]/g, '').slice(0, 500);
}

// =============================================================================
// ICP SCORING - Kurios MVA Lead Gen
// Target: Law firms, personal injury attorneys, managing partners
// =============================================================================

const ICP_KEYWORDS = {
  // Legal professional titles (highest value)
  legalTitles: [
    'managing partner', 'founding partner', 'named partner', 'senior partner',
    'partner', 'attorney', 'lawyer', 'trial lawyer', 'litigator',
    'of counsel', 'counsel', 'associate attorney', 'staff attorney',
    'general counsel', 'legal director'
  ],
  // Legal support staff (moderate value)
  legalStaff: [
    'paralegal', 'legal assistant', 'legal secretary', 'intake manager',
    'intake coordinator', 'intake specialist', 'case manager', 'legal nurse',
    'office manager', 'legal administrator', 'law clerk', 'legal intern'
  ],
  // General decision maker titles
  decisionMakers: [
    'ceo', 'president', 'owner', 'founder', 'co-founder', 'principal',
    'managing director', 'executive director', 'vice president', 'vp',
    'director', 'head of', 'chief'
  ],
  // Legal industry keywords
  legalIndustry: [
    'law firm', 'legal services', 'legal', 'law practice', 'law office',
    'attorney', 'lawyer', 'litigation', 'trial', 'judicial', 'law'
  ],
  // Personal injury / MVA specific (bonus points)
  piKeywords: [
    'personal injury', 'injury', 'mva', 'motor vehicle accident', 'accident',
    'tort', 'plaintiff', 'negligence', 'wrongful death', 'slip and fall',
    'medical malpractice', 'workers comp', 'workers compensation',
    'catastrophic injury', 'brain injury', 'spinal cord', 'car accident',
    'truck accident', 'motorcycle accident', 'pedestrian accident'
  ],
  // Adjacent industries
  adjacentIndustry: ['insurance', 'healthcare', 'medical', 'chiropractic',
                     'rehabilitation', 'claims'],
  // Excluded titles
  excludeTitles: ['student', 'intern', 'retired', 'professor', 'teacher',
                  'researcher', 'academic', 'unemployed'],
  // Competitor/vendor signals (penalty)
  competitors: ['seo agency', 'seo', 'marketing agency', 'lead generation', 'lead gen',
                'leadgen', 'digital marketing', 'advertising agency', 'web design agency',
                'saas', 'marketing software', 'crm vendor', 'backlink', 'ppc agency',
                'digital agency', 'growth agency', 'web agency']
};

function scoreVisitor(data) {
  let score = 0;
  const reasons = [];

  const title = sanitize(data.jobTitle || '').toLowerCase();
  const industry = sanitize(data.industry || '').toLowerCase();
  const company = sanitize(data.companyName || '').toLowerCase();
  const department = sanitize(data.department || '').toLowerCase();
  const seniority = sanitize(data.seniority || '').toLowerCase();
  const landingPage = sanitize(data.landingPage || '').toLowerCase();
  const visitedPages = (Array.isArray(data.visitedPages) ? data.visitedPages : [])
    .map(p => sanitize(p).toLowerCase());
  const allPages = [landingPage, ...visitedPages].filter(Boolean);

  // Helper: word-boundary-aware keyword match to avoid "partnership" matching "partner"
  function wordMatch(text, keyword) {
    return new RegExp('\\b' + keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'i').test(text);
  }

  // =============================================
  // 1. TITLE SCORING (max ~40)
  // =============================================
  let titleMatched = false;

  // Legal professional titles (highest value: 35-40 pts)
  for (const kw of ICP_KEYWORDS.legalTitles) {
    if (wordMatch(title, kw)) {
      const pts = kw.includes('partner') ? 40 : 35;
      score += pts;
      reasons.push(`Legal title: "${data.jobTitle}" (+${pts})`);
      titleMatched = true;
      break;
    }
  }

  // Legal staff (moderate value: 12 pts)
  if (!titleMatched) {
    for (const kw of ICP_KEYWORDS.legalStaff) {
      if (wordMatch(title, kw)) {
        score += 12;
        reasons.push(`Legal staff: "${data.jobTitle}" (+12)`);
        titleMatched = true;
        break;
      }
    }
  }

  // General decision makers (some value: 10 pts)
  if (!titleMatched) {
    for (const kw of ICP_KEYWORDS.decisionMakers) {
      if (title.includes(kw)) {
        score += 10;
        reasons.push(`Decision maker: "${data.jobTitle}" (+10)`);
        titleMatched = true;
        break;
      }
    }
  }

  // Excluded titles penalty
  for (const kw of ICP_KEYWORDS.excludeTitles) {
    if (title.includes(kw)) {
      score -= 50;
      reasons.push(`Excluded title: "${data.jobTitle}" (-50)`);
      break;
    }
  }

  // =============================================
  // 2. SENIORITY BONUS (max 8)
  // =============================================
  if (seniority) {
    const seniorityMap = {
      'c-level': 8, 'c-suite': 8, 'owner': 8, 'founder': 8,
      'vp': 6, 'vice president': 6,
      'director': 5,
      'manager': 3, 'senior': 2
    };
    for (const [level, pts] of Object.entries(seniorityMap)) {
      if (seniority.includes(level)) {
        score += pts;
        reasons.push(`Seniority: ${data.seniority} (+${pts})`);
        break;
      }
    }
  }

  // =============================================
  // 3. INDUSTRY / COMPANY (max 35)
  // =============================================
  const industryCompanyText = `${industry} ${company} ${department}`;
  let industryMatched = false;

  // Legal industry (25 pts)
  for (const kw of ICP_KEYWORDS.legalIndustry) {
    if (industryCompanyText.includes(kw)) {
      score += 25;
      reasons.push(`Legal industry/company (+25)`);
      industryMatched = true;
      break;
    }
  }

  // Personal injury / MVA specialty bonus (10 pts)
  for (const kw of ICP_KEYWORDS.piKeywords) {
    if (industryCompanyText.includes(kw) || title.includes(kw)) {
      score += 10;
      reasons.push(`PI/MVA specialty (+10)`);
      break;
    }
  }

  // Adjacent industries (5 pts, only if no legal match)
  if (!industryMatched) {
    for (const kw of ICP_KEYWORDS.adjacentIndustry) {
      if (industryCompanyText.includes(kw)) {
        score += 5;
        reasons.push(`Adjacent industry: ${data.industry || data.companyName} (+5)`);
        break;
      }
    }
  }

  // Competitor/vendor penalty (-20 pts)
  for (const kw of ICP_KEYWORDS.competitors) {
    if (industryCompanyText.includes(kw) || title.includes(kw)) {
      score -= 20;
      reasons.push(`Competitor/vendor signal (-20)`);
      break;
    }
  }

  // =============================================
  // 4. LEADPIPE INTENT SCORE (max 12)
  // =============================================
  const intentLevel = sanitize(data.intentScore || '').toLowerCase();
  const intentScores = { 'high': 12, 'medium': 6, 'low': 2 };
  if (intentScores[intentLevel]) {
    score += intentScores[intentLevel];
    reasons.push(`Intent: ${data.intentScore} (+${intentScores[intentLevel]})`);
  }

  // =============================================
  // 5. BEHAVIORAL SIGNALS (max 10)
  // =============================================
  let behavioralPts = 0;
  const pricingViews = Number(data.pricingPageViews) || 0;
  const demoViews = Number(data.demoPageViews) || 0;
  const checkoutViews = Number(data.checkoutPageViews) || 0;
  const sessions = Number(data.sessions) || 0;
  const pageviews = Number(data.pageviews) || 0;

  if (pricingViews > 0) behavioralPts += Math.min(pricingViews * 2, 4);
  if (demoViews > 0) behavioralPts += Math.min(demoViews * 2, 4);
  if (checkoutViews > 0) behavioralPts += Math.min(checkoutViews * 3, 6);
  if (sessions >= 3) behavioralPts += 3;
  if (pageviews >= 10) behavioralPts += 2;

  behavioralPts = Math.min(behavioralPts, 10);
  if (behavioralPts > 0) {
    score += behavioralPts;
    reasons.push(`Behavioral: ${sessions}s/${pageviews}pv, pricing:${pricingViews} demo:${demoViews} checkout:${checkoutViews} (+${behavioralPts})`);
  }

  // High-intent page bonus (5 pts)
  const highIntentPage = allPages.some(p =>
    p.includes('pricing') || p.includes('contact') || p.includes('demo') ||
    p.includes('schedule') || p.includes('book') || p.includes('start') ||
    p.includes('get-started') || p.includes('consultation') || p.includes('free-trial')
  );
  if (highIntentPage) {
    score += 5;
    reasons.push(`High-intent page visited (+5)`);
  }

  // =============================================
  // 6. CONTACT QUALITY (max 8)
  // =============================================
  const businessEmail = (Array.isArray(data.businessEmails) && data.businessEmails[0]) || '';
  const freeEmailDomains = ['gmail', 'yahoo', 'hotmail', 'outlook', 'aol', 'icloud', 'protonmail'];
  if (businessEmail && !freeEmailDomains.some(d => businessEmail.toLowerCase().includes(d))) {
    score += 4;
    reasons.push(`Business email (+4)`);
  }
  if (data.linkedinUrl) {
    score += 2;
    reasons.push(`LinkedIn profile (+2)`);
  }
  if (Array.isArray(data.phones) && data.phones.length > 0) {
    score += 2;
    reasons.push(`Phone available (+2)`);
  }

  // =============================================
  // 7. COMPANY FIT (max 6)
  // =============================================
  const empCount = Number(data.companyEmployeeCount) || 0;
  if (empCount === 1) {
    score += 3;
    reasons.push(`Solo practitioner (+3)`);
  } else if (empCount >= 2 && empCount <= 100) {
    score += 4;
    reasons.push(`Company size ${empCount} — law firm sweet spot (+4)`);
  } else if (empCount > 100 && empCount <= 500) {
    score += 2;
    reasons.push(`Mid-size company ${empCount} (+2)`);
  } else if (empCount > 500) {
    score += 1;
    reasons.push(`Large company ${empCount} (+1)`);
  }

  const revenue = Number(data.companyTotalRevenue) || 0;
  if (revenue >= 500000 && revenue <= 50000000) {
    score += 2;
    reasons.push(`Revenue fit ($${(revenue / 1000000).toFixed(1)}M) (+2)`);
  }

  // =============================================
  // 8. UTM / TRAFFIC SOURCE (max 4)
  // =============================================
  const utmMedium = sanitize(data.utmMedium || '').toLowerCase();
  const referrer = sanitize(data.referrer || '').toLowerCase();

  if (['cpc', 'ppc', 'paid', 'paidsearch', 'paid_search'].includes(utmMedium)) {
    score += 4;
    reasons.push(`Paid traffic (+4)`);
  } else if (referrer.includes('google') || referrer.includes('bing') || referrer.includes('yahoo')) {
    score += 2;
    reasons.push(`Search traffic (+2)`);
  }

  // =============================================
  // 9. LOCATION BONUS (max 3)
  // =============================================
  const state = sanitize(data.state || '').toLowerCase();
  if (state === 'texas' || state === 'tx') {
    score += 3;
    reasons.push(`Texas location (+3)`);
  }

  // =============================================
  // QUALIFICATION THRESHOLD: 50
  // =============================================
  return { score, reasons, qualified: score >= 50 };
}

// =============================================================================
// SLACK MESSAGE FORMATTING (Leadpipe fields)
// =============================================================================

function formatSlackMessage(data, scoreResult) {
  const fireEmoji = scoreResult.score >= 80 ? '🔥🔥🔥' :
                    scoreResult.score >= 60 ? '🔥🔥' : '🔥';
  const intentEmoji = { 'high': '🔴', 'medium': '🟡', 'low': '🟢' };
  const intentIcon = intentEmoji[(data.intentScore || '').toLowerCase()] || '⚪';

  const name = [data.firstName, data.lastName].filter(Boolean).map(s => sanitize(s)).join(' ') || 'Unknown';
  const email = sanitize((Array.isArray(data.businessEmails) && data.businessEmails[0]) || data.email || 'N/A');
  const phone = (Array.isArray(data.phones) && data.phones[0]) ? sanitize(data.phones[0]) : 'N/A';
  const title = sanitize(data.jobTitle || 'N/A');
  const company = sanitize(data.companyName || 'N/A');
  const industryStr = sanitize(data.industry || 'N/A');
  const location = [data.city, data.state].filter(Boolean).map(s => sanitize(s)).join(', ') || 'N/A';
  const empCount = data.companyEmployeeCount ? `${data.companyEmployeeCount} employees` : 'N/A';
  const revenue = data.companyTotalRevenue
    ? `$${(Number(data.companyTotalRevenue) / 1000000).toFixed(1)}M`
    : 'N/A';

  const blocks = [
    {
      type: 'header',
      text: {
        type: 'plain_text',
        text: `${fireEmoji} Qualified Lead — Score: ${scoreResult.score}`,
        emoji: true
      }
    },
    {
      type: 'section',
      fields: [
        { type: 'mrkdwn', text: `*👤 Name:*\n${name}` },
        { type: 'mrkdwn', text: `*💼 Title:*\n${title}` },
        { type: 'mrkdwn', text: `*🏢 Company:*\n${company}` },
        { type: 'mrkdwn', text: `*🏭 Industry:*\n${industryStr}` },
        { type: 'mrkdwn', text: `*📧 Email:*\n${email}` },
        { type: 'mrkdwn', text: `*📱 Phone:*\n${phone}` },
        { type: 'mrkdwn', text: `*📍 Location:*\n${location}` },
        { type: 'mrkdwn', text: `*👥 Size:*\n${empCount}` }
      ]
    },
    {
      type: 'section',
      fields: [
        { type: 'mrkdwn', text: `*${intentIcon} Intent:*\n${sanitize(data.intentScore || 'N/A')} | ${data.sessions || 0} sessions, ${data.pageviews || 0} pageviews` },
        { type: 'mrkdwn', text: `*💰 Revenue:*\n${revenue}` }
      ]
    }
  ];

  // Behavioral signals section
  const behaviorParts = [];
  if (data.pricingPageViews) behaviorParts.push(`Pricing: ${data.pricingPageViews}x`);
  if (data.demoPageViews) behaviorParts.push(`Demo: ${data.demoPageViews}x`);
  if (data.checkoutPageViews) behaviorParts.push(`Checkout: ${data.checkoutPageViews}x`);
  if (data.landingPage) behaviorParts.push(`Landing: ${sanitize(data.landingPage)}`);

  if (behaviorParts.length > 0) {
    blocks.push({
      type: 'section',
      text: { type: 'mrkdwn', text: `*📊 Behavior:* ${behaviorParts.join(' • ')}` }
    });
  }

  // UTM / Referrer
  const trafficParts = [];
  if (data.utmSource) trafficParts.push(`Source: ${sanitize(data.utmSource)}`);
  if (data.utmMedium) trafficParts.push(`Medium: ${sanitize(data.utmMedium)}`);
  if (data.utmCampaign) trafficParts.push(`Campaign: ${sanitize(data.utmCampaign)}`);
  if (data.referrer) trafficParts.push(`Referrer: ${sanitize(data.referrer).slice(0, 80)}`);

  if (trafficParts.length > 0) {
    blocks.push({
      type: 'section',
      text: { type: 'mrkdwn', text: `*🔍 Traffic:* ${trafficParts.join(' • ')}` }
    });
  }

  // Score breakdown
  blocks.push({
    type: 'context',
    elements: [
      { type: 'mrkdwn', text: `*Score Breakdown:* ${scoreResult.reasons.join(' · ')}` }
    ]
  });

  // LinkedIn button
  if (data.linkedinUrl) {
    blocks.push({
      type: 'actions',
      elements: [
        {
          type: 'button',
          text: { type: 'plain_text', text: '🔗 LinkedIn Profile', emoji: true },
          url: sanitize(data.linkedinUrl),
          action_id: 'linkedin_profile'
        }
      ]
    });
  }

  return { blocks };
}

// =============================================================================
// SLACK DELIVERY (via Bot Token + chat.postMessage)
// =============================================================================

async function sendToSlack(payload, channelId = SLACK_CHANNEL) {
  if (!SLACK_BOT_TOKEN) {
    console.log('[SLACK] No bot token configured, skipping notification');
    return;
  }

  try {
    const postData = JSON.stringify({
      channel: channelId,
      blocks: payload.blocks,
      text: payload.text || 'New qualified lead'
    });

    const options = {
      hostname: 'slack.com',
      path: '/api/chat.postMessage',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${SLACK_BOT_TOKEN}`,
        'Content-Length': Buffer.byteLength(postData)
      }
    };

    return new Promise((resolve, reject) => {
      const req = https.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            const result = JSON.parse(body);
            if (result.ok) {
              console.log(`[SLACK] ✅ Posted to ${channelId}: ${res.statusCode}`);
            } else {
              console.error(`[SLACK] ❌ Error: ${result.error}`);
            }
            resolve(result);
          } catch(e) {
            console.log(`[SLACK] Response: ${body}`);
            resolve(body);
          }
        });
      });
      req.on('error', (err) => {
        console.error('[SLACK] Request error:', err.message);
        reject(err);
      });
      req.write(postData);
      req.end();
    });
  } catch (err) {
    console.error('[SLACK] Error:', err.message);
  }
}

// =============================================================================
// HTTP SERVER
// =============================================================================

const server = http.createServer(async (req, res) => {
  const clientIp = req.headers['x-forwarded-for']?.split(',')[0]?.trim() ||
                   req.headers['x-real-ip'] ||
                   req.socket.remoteAddress;

  // Debug: log ALL incoming requests
  console.log(`[REQUEST] ${req.method} ${req.url} from ${clientIp} | Headers: ${JSON.stringify(req.headers)}`);

  // Rate limit check (exempt localhost for testing/health checks)
  const isLocalhost = clientIp === '127.0.0.1' || clientIp === '::1' || clientIp === '::ffff:127.0.0.1';
  if (!isLocalhost && !rateLimiter.check(clientIp)) {
    res.writeHead(429, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'rate_limited' }));
    return;
  }

  // Health check
  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'lead-webhook', version: 'leadpipe-v2' }));
    return;
  }

  // Webhook endpoint
  const parsedUrl = new URL(req.url, `http://${req.headers.host}`);
  const urlPath = parsedUrl.pathname;
  const urlKey = parsedUrl.searchParams.get('key');

  if (req.method === 'POST' && (urlPath === '/webhook' || urlPath === '/rb2b' || urlPath === '/rb2b/webhook' || urlPath === '/leadpipe')) {
    // Verify auth - support multiple methods
    const authHeader = req.headers['authorization'] || '';
    const bearerToken = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : '';

    const isAuthValid =
      urlKey === WEBHOOK_SECRET ||                     // query param
      bearerToken === WEBHOOK_SECRET ||                // bearer token
      req.headers['x-webhook-event'] ||                // Leadpipe header present
      req.headers['webhook-id'] ||                     // Svix header
      req.headers['webhook-signature'];                // Svix signature

    if (!isAuthValid) {
      rateLimiter.check(clientIp, 'auth');
      if (!rateLimiter.check(clientIp, 'auth')) {
        res.writeHead(429, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'too_many_auth_failures' }));
        return;
      }
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: 'unauthorized' }));
      return;
    }

    let body = '';
    let bodySize = 0;

    req.on('data', chunk => {
      bodySize += chunk.length;
      if (bodySize > MAX_BODY_SIZE) {
        res.writeHead(413, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'payload_too_large' }));
        req.destroy();
        return;
      }
      body += chunk;
    });

    req.on('end', async () => {
      if (bodySize > MAX_BODY_SIZE) return;

      try {
        const payload = JSON.parse(body);

        // Reject non-object payloads
        if (typeof payload !== 'object' || payload === null || Array.isArray(payload)) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'invalid_payload' }));
          return;
        }

        const timestamp = new Date().toISOString();

        // Extract visitor data from Leadpipe format: { event, data: {...} }
        // Falls back to top-level if no .data wrapper (backwards compat)
        const data = payload.data || payload;
        const eventType = payload.event || 'unknown';

        // Log raw payload for debugging
        const rawLogFile = path.join(LOG_DIR, `raw-${new Date().toISOString().slice(0, 10)}.jsonl`);
        fs.appendFileSync(rawLogFile, JSON.stringify({ timestamp, event: eventType, payload }) + '\n');

        // Log ALL visitors to file
        const logFile = path.join(LOG_DIR, `visitors-${new Date().toISOString().slice(0, 10)}.jsonl`);
        fs.appendFileSync(logFile, JSON.stringify({ timestamp, event: eventType, ...data }) + '\n');

        // Score the visitor
        const scoreResult = scoreVisitor(data);

        console.log(`[VISITOR] ${timestamp} | ${sanitize(data.firstName || '')} ${sanitize(data.lastName || '')} | ${sanitize(data.jobTitle || 'N/A')} @ ${sanitize(data.companyName || 'N/A')} | Intent: ${sanitize(data.intentScore || 'N/A')} | Score: ${scoreResult.score} | Qualified: ${scoreResult.qualified}`);

        // Log to all-visitors file
        const allLog = path.join(LOG_DIR, 'all-visitors.jsonl');
        fs.appendFileSync(allLog, JSON.stringify({
          timestamp, event: eventType,
          score: scoreResult.score, qualified: scoreResult.qualified,
          name: `${data.firstName || ''} ${data.lastName || ''}`.trim(),
          jobTitle: data.jobTitle, companyName: data.companyName,
          industry: data.industry, intentScore: data.intentScore,
          ...data
        }) + '\n');

        // If qualified, log and alert
        if (scoreResult.qualified) {
          const qualifiedLog = path.join(LOG_DIR, 'qualified-leads.jsonl');
          fs.appendFileSync(qualifiedLog, JSON.stringify({
            timestamp, event: eventType,
            score: scoreResult.score, reasons: scoreResult.reasons,
            name: `${data.firstName || ''} ${data.lastName || ''}`.trim(),
            jobTitle: data.jobTitle, companyName: data.companyName,
            industry: data.industry, intentScore: data.intentScore,
            email: data.email, phones: data.phones, linkedinUrl: data.linkedinUrl,
            ...data
          }) + '\n');

          console.log(`[QUALIFIED] 🔥 ${sanitize(data.firstName || '')} ${sanitize(data.lastName || '')} — ${sanitize(data.jobTitle || 'N/A')} @ ${sanitize(data.companyName || 'N/A')} | Score: ${scoreResult.score} | Reasons: ${scoreResult.reasons.join(', ')}`);

          // Send Slack notification
          if (SLACK_BOT_TOKEN) {
            const slackMsg = formatSlackMessage(data, scoreResult);
            sendToSlack(slackMsg).catch(err =>
              console.error('[SLACK] Failed:', err.message)
            );
          }
        }

        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
          received: true,
          score: scoreResult.score,
          qualified: scoreResult.qualified
        }));
      } catch (err) {
        console.error('[ERROR]', err.message);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ received: true, error: 'parse_error' }));
      }
    });
    return;
  }

  // 404 for everything else
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: 'not_found' }));
});

// Server timeout for slow clients
server.timeout = 30000;
server.keepAliveTimeout = 5000;

server.listen(PORT, () => {
  console.log(`[Webhook Server] Leadpipe v2 — Running on port ${PORT}`);
  console.log(`[Webhook Server] Endpoints: POST /webhook, /leadpipe, /rb2b/webhook`);
  console.log(`[Webhook Server] Health: GET /health`);
  console.log(`[Webhook Server] ICP: Law firms, PI attorneys, managing partners`);
  console.log(`[Webhook Server] Qualification threshold: 50 points`);
  console.log(`[Webhook Server] Max payload: ${MAX_BODY_SIZE / 1024}KB`);
  console.log(`[Webhook Server] Rate limit: 120 req/min, 10 failed auth/min`);
});
