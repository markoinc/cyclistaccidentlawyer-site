#!/usr/bin/env node
/**
 * Funnel Test Script - cases.kuriosbrand.com
 * Tests the full flow from /qualify to calendar booking
 * Handles SPA (React Router) navigation properly
 */

const puppeteer = require('puppeteer');

const BASE_URL = 'https://cases.kuriosbrand.com';
const VIEWPORT_POSITIONS = [
  { width: 375, height: 667, name: 'iPhone SE' },
  { width: 390, height: 844, name: 'iPhone 12' },
  { width: 414, height: 896, name: 'iPhone 11 Pro Max' },
  { width: 360, height: 640, name: 'Android Small' },
  { width: 412, height: 915, name: 'Android Large' },
  { width: 768, height: 1024, name: 'iPad' },
  { width: 1024, height: 768, name: 'iPad Landscape' },
  { width: 1280, height: 720, name: 'Desktop HD' },
  { width: 1920, height: 1080, name: 'Desktop FHD' },
  { width: 2560, height: 1440, name: 'Desktop 2K' },
];

const SCROLL_POSITIONS = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000];

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function waitForUrlChange(page, initialUrl, timeout = 10000) {
  const startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    const currentUrl = page.url();
    if (currentUrl !== initialUrl) {
      return currentUrl;
    }
    await delay(100);
  }
  throw new Error(`URL did not change from ${initialUrl} within ${timeout}ms`);
}

async function testFunnel(browser, viewport, scrollPosition, testId) {
  const page = await browser.newPage();
  const results = {
    testId,
    viewport: viewport.name,
    scrollPosition,
    steps: [],
    success: true,
    error: null,
  };

  try {
    await page.setViewport({ width: viewport.width, height: viewport.height });

    // Step 1: Load /qualify page
    const startTime = Date.now();
    await page.goto(`${BASE_URL}/qualify`, { waitUntil: 'networkidle2', timeout: 30000 });
    results.steps.push({
      step: 'load_qualify',
      success: true,
      timeMs: Date.now() - startTime,
    });

    // Step 2: Scroll to position
    await page.evaluate((pos) => window.scrollTo(0, pos), scrollPosition);
    await delay(100);
    results.steps.push({ step: 'scroll', success: true, position: scrollPosition });

    // Step 3: Find and click checkbox
    const checkboxSelector = '#certification';
    await page.waitForSelector(checkboxSelector, { timeout: 5000 });
    await page.click(checkboxSelector);
    await delay(200); // Wait for state update
    results.steps.push({ step: 'click_checkbox', success: true });

    // Step 4: Verify checkbox is checked
    const isChecked = await page.evaluate(() => {
      const checkbox = document.querySelector('#certification');
      return checkbox?.getAttribute('data-state') === 'checked' || checkbox?.checked;
    });
    results.steps.push({ step: 'verify_checkbox', success: isChecked });

    // Step 5: Click "Book My Call" button
    const initialUrl = page.url();
    const buttonClicked = await page.evaluate(() => {
      const buttons = document.querySelectorAll('button');
      for (const btn of buttons) {
        if (btn.textContent.includes('Book My Call') && !btn.disabled) {
          btn.click();
          return true;
        }
      }
      return false;
    });
    
    if (!buttonClicked) {
      throw new Error('Could not find or click Book My Call button');
    }
    results.steps.push({ step: 'click_button', success: true });

    // Step 6: Wait for SPA navigation (URL change)
    const newUrl = await waitForUrlChange(page, initialUrl, 10000);
    
    if (newUrl.includes('test-batch-calendar')) {
      results.steps.push({ step: 'navigate_calendar', success: true, url: newUrl });
    } else {
      results.steps.push({ step: 'navigate_calendar', success: false, url: newUrl });
      results.success = false;
    }

    // Step 7: Wait for page to settle after navigation
    await delay(500);

    // Step 8: Check if calendar iframe loads
    await page.waitForSelector('iframe[src*="leadconnectorhq"]', { timeout: 15000 });
    results.steps.push({ step: 'calendar_iframe_present', success: true });

    // Step 9: Verify iframe src
    const iframeSrc = await page.evaluate(() => {
      const iframe = document.querySelector('iframe[src*="leadconnectorhq"]');
      return iframe?.src || null;
    });
    
    if (iframeSrc && iframeSrc.includes('leadconnectorhq')) {
      results.steps.push({ step: 'calendar_src_valid', success: true, src: iframeSrc });
    } else {
      results.steps.push({ step: 'calendar_src_valid', success: false });
      results.success = false;
    }

  } catch (error) {
    results.success = false;
    results.error = error.message;
    results.steps.push({ step: 'error', success: false, message: error.message });
  } finally {
    await page.close();
  }

  return results;
}

async function runTests() {
  console.log('🚀 Starting Funnel Tests...\n');
  console.log(`Testing ${VIEWPORT_POSITIONS.length} viewports × ${SCROLL_POSITIONS.length} scroll positions`);
  console.log(`Total test combinations: ${VIEWPORT_POSITIONS.length * SCROLL_POSITIONS.length}\n`);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const allResults = [];
  let testId = 0;
  let passed = 0;
  let failed = 0;

  // Run tests for each viewport and scroll position
  for (const viewport of VIEWPORT_POSITIONS) {
    for (const scrollPos of SCROLL_POSITIONS) {
      testId++;
      process.stdout.write(`\rRunning test ${testId}/${VIEWPORT_POSITIONS.length * SCROLL_POSITIONS.length}...`);
      
      const result = await testFunnel(browser, viewport, scrollPos, testId);
      allResults.push(result);
      
      if (result.success) {
        passed++;
      } else {
        failed++;
        console.log(`\n❌ FAILED: ${viewport.name} @ scroll ${scrollPos}`);
        console.log(`   Error: ${result.error || 'Unknown'}`);
      }
    }
  }

  await browser.close();

  // Summary
  console.log('\n\n📊 TEST SUMMARY');
  console.log('═'.repeat(50));
  console.log(`Total Tests: ${allResults.length}`);
  console.log(`✅ Passed: ${passed}`);
  console.log(`❌ Failed: ${failed}`);
  console.log(`Success Rate: ${((passed / allResults.length) * 100).toFixed(1)}%`);

  // Group failures by error type
  if (failed > 0) {
    console.log('\n🔴 FAILURE BREAKDOWN:');
    const errors = {};
    allResults.filter(r => !r.success).forEach(r => {
      const err = r.error || 'Unknown';
      errors[err] = (errors[err] || 0) + 1;
    });
    Object.entries(errors).forEach(([err, count]) => {
      console.log(`   ${count}x: ${err}`);
    });
  }

  // Performance stats
  const loadTimes = allResults
    .map(r => r.steps.find(s => s.step === 'load_qualify')?.timeMs)
    .filter(Boolean);
  
  if (loadTimes.length > 0) {
    const avgLoad = loadTimes.reduce((a, b) => a + b, 0) / loadTimes.length;
    const maxLoad = Math.max(...loadTimes);
    const minLoad = Math.min(...loadTimes);
    
    console.log('\n⚡ PERFORMANCE:');
    console.log(`   Avg page load: ${avgLoad.toFixed(0)}ms`);
    console.log(`   Min page load: ${minLoad}ms`);
    console.log(`   Max page load: ${maxLoad}ms`);
  }

  // Check step success rates
  console.log('\n📍 STEP SUCCESS RATES:');
  const stepStats = {};
  allResults.forEach(r => {
    r.steps.forEach(s => {
      if (!stepStats[s.step]) stepStats[s.step] = { total: 0, success: 0 };
      stepStats[s.step].total++;
      if (s.success) stepStats[s.step].success++;
    });
  });
  Object.entries(stepStats).forEach(([step, stats]) => {
    const rate = ((stats.success / stats.total) * 100).toFixed(1);
    const icon = stats.success === stats.total ? '✅' : '⚠️';
    console.log(`   ${icon} ${step}: ${stats.success}/${stats.total} (${rate}%)`);
  });

  // Return exit code
  process.exit(failed > 0 ? 1 : 0);
}

runTests().catch(console.error);
