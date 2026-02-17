#!/usr/bin/env python3
"""
Scrape Notion pages using Playwright with proper waiting.
"""

import asyncio
import sys
import json
from playwright.async_api import async_playwright

async def scrape_notion_page(url, timeout=30000):
    """Scrape a single Notion page."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle", timeout=timeout)
            
            # Wait for content to load
            await page.wait_for_selector('[data-block-id]', timeout=15000)
            await asyncio.sleep(2)  # Extra wait for dynamic content
            
            # Extract all text content
            content = await page.evaluate('''() => {
                // Get the main content area
                const main = document.querySelector('[class*="notion-page-content"]') || 
                             document.querySelector('main') || 
                             document.body;
                
                // Extract text from all blocks
                const blocks = main.querySelectorAll('[data-block-id]');
                let text = [];
                blocks.forEach(block => {
                    const textContent = block.innerText.trim();
                    if (textContent) {
                        text.push(textContent);
                    }
                });
                
                return {
                    title: document.querySelector('h1')?.innerText || '',
                    text: text.join('\\n\\n'),
                    html: main.innerHTML.substring(0, 50000)
                };
            }''')
            
            return content
            
        except Exception as e:
            print(f"Error scraping {url}: {e}", file=sys.stderr)
            return None
        finally:
            await browser.close()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_notion_playwright.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    result = await scrape_notion_page(url)
    
    if result:
        print(json.dumps(result, indent=2))
    else:
        print("Failed to scrape page")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
