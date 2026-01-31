const https = require('https');

const NOTION_KEY = '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';
const DATABASE_ID = '2f89371d-3030-8126-a67c-c73ee64fa034';

const data = require('./ghl-docs-workflows.json');

// Category mapping
const categoryMap = {
  'Workflows & Automations': 'Workflows',
  'Pipeline & CRM Setup': 'CRM',
  'Calendar & Booking': 'Calendar',
  'SMS & Email Sequences': 'Communications',
  'Forms & Landing Pages': 'Forms',
  'Documents & Contracts': 'Integrations'
};

// Determine sales flow relevance from salesFlowApplication text
function getSalesFlowRelevance(text) {
  const lower = (text || '').toLowerCase();
  if (lower.includes('lead capture') || lower.includes('form submitted') || lower.includes('lead gen')) return 'Lead Capture';
  if (lower.includes('book') || lower.includes('appointment') || lower.includes('calendar') || lower.includes('schedule')) return 'Booking';
  if (lower.includes('follow-up') || lower.includes('follow up') || lower.includes('drip') || lower.includes('sequence') || lower.includes('nurture')) return 'Nurture';
  if (lower.includes('close') || lower.includes('won') || lower.includes('contract') || lower.includes('signed') || lower.includes('proposal')) return 'Closing';
  if (lower.includes('report') || lower.includes('stats') || lower.includes('track')) return 'Reporting';
  if (lower.includes('reminder') || lower.includes('sms') || lower.includes('email')) return 'Follow-up';
  return 'Nurture'; // default
}

// Determine priority
function getPriority(title, category) {
  const lower = title.toLowerCase();
  // Core workflow/automation docs get High priority
  if (category === 'Workflows' || lower.includes('introduction') || lower.includes('getting started') || 
      lower.includes('trigger') || lower.includes('action') || lower.includes('pipeline')) {
    return 'High';
  }
  return 'Medium';
}

function createNotionPage(doc, categoryName) {
  return new Promise((resolve, reject) => {
    const category = categoryMap[categoryName] || 'Workflows';
    const salesFlow = getSalesFlowRelevance(doc.salesFlowApplication);
    const priority = getPriority(doc.title, category);
    
    // Key Features - join concepts into rich text
    const keyFeatures = (doc.keyConceptsFeatures || []).join('\n• ');
    
    const body = JSON.stringify({
      parent: { database_id: DATABASE_ID },
      properties: {
        'Name': {
          title: [{ text: { content: doc.title } }]
        },
        'Category': {
          select: { name: category }
        },
        'URL': {
          url: doc.url
        },
        'Key Features': {
          rich_text: [{ text: { content: keyFeatures.slice(0, 2000) } }]
        },
        'Sales Flow Relevance': {
          select: { name: salesFlow }
        },
        'Priority': {
          select: { name: priority }
        },
        'Status': {
          select: { name: 'To Review' }
        }
      }
    });

    const options = {
      hostname: 'api.notion.com',
      port: 443,
      path: '/v1/pages',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${NOTION_KEY}`,
        'Content-Type': 'application/json',
        'Notion-Version': '2022-06-28'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200 || res.statusCode === 201) {
          resolve({ success: true, title: doc.title });
        } else {
          reject({ success: false, title: doc.title, error: data, status: res.statusCode });
        }
      });
    });

    req.on('error', (e) => reject({ success: false, title: doc.title, error: e.message }));
    req.write(body);
    req.end();
  });
}

async function importAll() {
  const results = { success: 0, failed: 0, errors: [] };
  
  for (const category of data.categories) {
    for (const doc of category.docs) {
      try {
        await createNotionPage(doc, category.name);
        results.success++;
        console.log(`✓ Created: ${doc.title}`);
        // Small delay to avoid rate limits
        await new Promise(r => setTimeout(r, 350));
      } catch (err) {
        results.failed++;
        results.errors.push(err);
        console.log(`✗ Failed: ${doc.title} - ${err.error || err}`);
      }
    }
  }
  
  console.log(`\n=== Import Complete ===`);
  console.log(`Created: ${results.success} pages`);
  console.log(`Failed: ${results.failed} pages`);
  if (results.errors.length > 0) {
    console.log('Errors:', JSON.stringify(results.errors, null, 2));
  }
}

importAll();
