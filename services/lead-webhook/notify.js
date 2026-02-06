#!/usr/bin/env node
/**
 * RB2B Qualified Lead Notifier
 * Watches the qualified-leads log and sends notifications via Slack channel
 * Run this alongside the webhook server
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const QUALIFIED_LOG = path.join(__dirname, 'logs', 'qualified-leads.jsonl');
const SLACK_CHANNEL = 'C0ACS689MT4'; // #mark-sierra - change to rb2b channel when created
let lastSize = 0;

try {
  if (fs.existsSync(QUALIFIED_LOG)) {
    lastSize = fs.statSync(QUALIFIED_LOG).size;
  }
} catch {}

console.log('[Notifier] Watching for qualified leads...');

fs.watchFile(QUALIFIED_LOG, { interval: 5000 }, (curr, prev) => {
  if (curr.size <= lastSize) return;
  
  try {
    const content = fs.readFileSync(QUALIFIED_LOG, 'utf8');
    const lines = content.trim().split('\n');
    const newLines = lines.slice(-5); // Get last few lines
    
    for (const line of newLines) {
      try {
        const data = JSON.parse(line);
        if (new Date(data.timestamp) > new Date(Date.now() - 60000)) {
          // Less than 60 seconds old — notify
          const msg = `🔥 *Qualified RB2B Visitor!*\n` +
            `*${data['First Name']} ${data['Last Name']}*\n` +
            `${data['Title'] || 'N/A'} @ ${data['Company Name'] || 'N/A'}\n` +
            `📧 ${data['Business Email'] || 'N/A'}\n` +
            `🔗 ${data['LinkedIn URL'] || 'N/A'}\n` +
            `📍 ${data['City'] || ''}, ${data['State'] || ''}\n` +
            `🏢 ${data['Employee Count'] || 'N/A'} employees | ${data['Estimate Revenue'] || 'N/A'}\n` +
            `📄 Visited: ${data['Captured URL'] || 'N/A'}\n` +
            `⭐ Score: ${data.score} | ${(data.reasons || []).join(' • ')}`;
          
          console.log(`[Notifier] Sending alert for ${data['First Name']} ${data['Last Name']}`);
          console.log(msg);
        }
      } catch {}
    }
    
    lastSize = curr.size;
  } catch (err) {
    console.error('[Notifier] Error:', err.message);
  }
});
