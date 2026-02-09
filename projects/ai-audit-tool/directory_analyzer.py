#!/usr/bin/env python3
"""
Directory SEO Audit Tool
Comprehensive analysis for directory/listing websites based on Jacky Chou's methodologies

Analyzes 30 categories across 6 sections:

DIRECTORY SEO (200 pts):
- Structure & Architecture (50 pts)
- On-Page SEO (50 pts)
- Content Quality (40 pts)
- Technical SEO (30 pts)
- Authority & Trust (30 pts)

AI VISIBILITY (100 pts):
- AI Crawler Access (10 pts)
- Structured Data Quality (10 pts)
- Content Structure (10 pts)
- E-E-A-T Signals (10 pts)
- Brand Presence (10 pts)
- Content Freshness (10 pts)
- Question-Based Content (10 pts)
- Citations & Sources (10 pts)
- Technical Performance (10 pts)
- AI Platform Presence (10 pts)

Total: 300 points = Combined Directory + AI Score

Usage: python3 directory_analyzer.py https://example-directory.com
"""

import requests
import json
import re
import sys
import base64
from urllib.parse import urlparse, urljoin, parse_qs
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple, Set
from collections import Counter
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import AI visibility checks from enhanced analyzer
try:
    from enhanced_analyzer import EnhancedWebsiteAnalyzer
    AI_ANALYZER_AVAILABLE = True
except ImportError:
    AI_ANALYZER_AVAILABLE = False
    print("Warning: enhanced_analyzer not found. AI visibility checks will be limited.")

# DataForSEO integration
DATAFORSEO_AVAILABLE = False
DATAFORSEO_AUTH = None
try:
    import os
    # Check for DataForSEO credentials
    cred_path = os.path.expanduser('~/.config/dataforseo/credentials.json')
    if os.path.exists(cred_path):
        with open(cred_path) as f:
            creds = json.load(f)
            DATAFORSEO_AUTH = base64.b64encode(
                f"{creds['login']}:{creds['password']}".encode()
            ).decode()
            DATAFORSEO_AVAILABLE = True
except:
    pass


@dataclass
class CategoryScore:
    """Score for a single audit category"""
    name: str
    score: int = 0  # 0-10
    max_score: int = 10
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DirectoryAuditResult:
    """Complete audit result for a directory site"""
    url: str
    directory_name: Optional[str] = None
    directory_type: Optional[str] = None  # e.g., "business", "product", "service"
    
    # Directory SEO Section scores (200 pts total)
    structure_score: int = 0  # /50
    onpage_score: int = 0  # /50
    content_score: int = 0  # /40
    technical_score: int = 0  # /30
    authority_score: int = 0  # /30
    
    # AI Visibility score (100 pts total)
    ai_visibility_score: int = 0  # /100
    
    # Totals
    directory_health_score: int = 0  # /200
    total_score: int = 0  # /300 (directory + AI)
    grade: str = "F"
    
    # Category breakdowns - Directory SEO
    structure_categories: List[CategoryScore] = field(default_factory=list)
    onpage_categories: List[CategoryScore] = field(default_factory=list)
    content_categories: List[CategoryScore] = field(default_factory=list)
    technical_categories: List[CategoryScore] = field(default_factory=list)
    authority_categories: List[CategoryScore] = field(default_factory=list)
    
    # Category breakdowns - AI Visibility
    ai_categories: List[CategoryScore] = field(default_factory=list)
    
    # Actionable insights
    quick_wins: List[str] = field(default_factory=list)
    priority_fixes: List[str] = field(default_factory=list)
    
    # Raw data
    technical_data: Dict[str, Any] = field(default_factory=dict)
    listing_samples: List[Dict] = field(default_factory=list)
    category_analysis: Dict[str, Any] = field(default_factory=dict)


class DirectorySEOAnalyzer:
    """
    Comprehensive Directory SEO Analyzer
    
    Checks 20 categories specific to directory/listing sites:
    - Listing completeness and quality
    - Category taxonomy and structure
    - Location/geo pages
    - Schema markup (LocalBusiness, ItemList, etc.)
    - User-generated content
    - And more...
    """
    
    # Multiple User-Agent options to rotate for bot protection bypass
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.4; rv:125.0) Gecko/20100101 Firefox/125.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    ]
    
    def __init__(self, url: str, max_pages: int = 50):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.parsed_url = urlparse(self.url)
        self.domain = self.parsed_url.netloc.replace('www.', '')
        self.max_pages = max_pages
        self.request_count = 0
        self.last_request_time = 0
        self.rate_limit_delay = 0.3  # Base delay between requests
        
        self.session = requests.Session()
        self._rotate_user_agent()
        self.session.headers.update({
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
    
    def _rotate_user_agent(self):
        """Rotate User-Agent to help avoid bot detection"""
        ua = random.choice(self.USER_AGENTS)
        self.session.headers['User-Agent'] = ua
        
        # Page data
        self.html = None
        self.soup = None
        self.robots_txt = None
        self.sitemap_urls = []
        
        # Discovered pages by type
        self.listing_pages: List[Dict] = []
        self.category_pages: List[Dict] = []
        self.location_pages: List[Dict] = []
        self.other_pages: List[Dict] = []
        
        # Schema data
        self.all_schemas: List[Dict] = []
        
    def fetch_page(self, url: str = None, timeout: int = 15, retries: int = 2) -> Tuple[Optional[str], Optional[BeautifulSoup]]:
        """Fetch a page and return HTML + BeautifulSoup object
        
        Includes:
        - Retry logic with exponential backoff
        - Rate limiting to avoid 429 errors
        - User-Agent rotation on failures
        """
        target_url = url or self.url
        
        # Filter out localhost/internal URLs that shouldn't be fetched
        parsed = urlparse(target_url)
        if parsed.netloc in ['localhost', '127.0.0.1', ''] or parsed.netloc.startswith('localhost:'):
            return None, None
        
        # Rate limiting - ensure minimum delay between requests
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        
        for attempt in range(retries + 1):
            try:
                # Add referer header for internal pages
                headers = {}
                if url and url != self.url:
                    headers['Referer'] = self.url
                
                resp = self.session.get(target_url, timeout=timeout, allow_redirects=True, headers=headers)
                self.last_request_time = time.time()
                self.request_count += 1
                
                # Handle rate limiting
                if resp.status_code == 429:
                    retry_after = int(resp.headers.get('Retry-After', 5))
                    if attempt < retries:
                        wait_time = min(retry_after, 10) * (attempt + 1)
                        print(f"  [!] Rate limited, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        self._rotate_user_agent()
                        self.rate_limit_delay = min(self.rate_limit_delay * 1.5, 2.0)  # Increase delay
                        continue
                    else:
                        print(f"  [!] Rate limited on {target_url[:60]}...")
                        return None, None
                
                # Handle 403 - try with different headers on retry
                if resp.status_code == 403 and attempt < retries:
                    self._rotate_user_agent()
                    time.sleep(1 * (attempt + 1))
                    continue
                
                resp.raise_for_status()
                html = resp.text
                soup = BeautifulSoup(html, 'html.parser')
                
                if url is None:  # Main page
                    self.html = html
                    self.soup = soup
                    
                return html, soup
                
            except requests.exceptions.Timeout:
                if attempt < retries:
                    time.sleep(2 * (attempt + 1))
                    continue
                print(f"  [!] Timeout fetching {target_url[:60]}...")
                return None, None
                
            except requests.exceptions.RequestException as e:
                error_msg = str(e)[:100]
                if attempt < retries and ('403' in error_msg or '429' in error_msg):
                    self._rotate_user_agent()
                    time.sleep(2 * (attempt + 1))
                    continue
                # Only print error on final failure or non-retryable errors
                if url is None or attempt == retries:  # Main page or final attempt
                    print(f"  [!] Error fetching {target_url[:60]}...: {error_msg}")
                return None, None
        
        return None, None
            
    def fetch_robots_txt(self) -> str:
        """Fetch robots.txt"""
        try:
            robots_url = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/robots.txt"
            resp = self.session.get(robots_url, timeout=10)
            if resp.status_code == 200:
                self.robots_txt = resp.text
                return self.robots_txt
        except:
            pass
        return ""
        
    def fetch_sitemap(self) -> List[str]:
        """Fetch and parse sitemap(s)"""
        urls = []
        sitemap_locations = [
            f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/sitemap.xml",
            f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/sitemap_index.xml",
            f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/sitemap-index.xml",
        ]
        
        # Check robots.txt for sitemap
        if self.robots_txt:
            for line in self.robots_txt.split('\n'):
                if line.lower().startswith('sitemap:'):
                    sitemap_locations.insert(0, line.split(':', 1)[1].strip())
                    
        for sitemap_url in sitemap_locations[:3]:
            try:
                resp = self.session.get(sitemap_url, timeout=15)
                if resp.status_code == 200:
                    # Parse XML
                    soup = BeautifulSoup(resp.text, 'lxml-xml')
                    
                    # Check for sitemap index
                    sitemaps = soup.find_all('sitemap')
                    if sitemaps:
                        # It's an index, fetch child sitemaps
                        for sm in sitemaps[:5]:  # Limit to 5 child sitemaps
                            loc = sm.find('loc')
                            if loc:
                                try:
                                    sm_resp = self.session.get(loc.text, timeout=15)
                                    sm_soup = BeautifulSoup(sm_resp.text, 'lxml-xml')
                                    for url_tag in sm_soup.find_all('url'):
                                        loc_tag = url_tag.find('loc')
                                        if loc_tag:
                                            urls.append(loc_tag.text)
                                except:
                                    continue
                    else:
                        # Direct sitemap
                        for url_tag in soup.find_all('url'):
                            loc_tag = url_tag.find('loc')
                            if loc_tag:
                                urls.append(loc_tag.text)
                                
                    if urls:
                        break
            except Exception as e:
                continue
                
        self.sitemap_urls = urls[:500]  # Limit to 500 URLs
        return self.sitemap_urls
        
    def extract_schemas(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract all JSON-LD schema from a page"""
        schemas = []
        for script in soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    schemas.extend(data)
                else:
                    schemas.append(data)
            except:
                pass
        return schemas
        
    def classify_page(self, url: str, soup: BeautifulSoup) -> str:
        """Classify a page as listing, category, location, or other"""
        url_lower = url.lower()
        text = soup.get_text().lower() if soup else ""
        
        # URL patterns - expanded for more directory types
        listing_patterns = [
            '/listing/', '/business/', '/company/', '/profile/', '/place/', 
            '/vendor/', '/provider/', '/shop/', '/store/', '/detail/',
            '/biz/', '/firm/', '/agency/', '/organization/', '/review/',
            '/software/', '/product/', '/app/', '/tool/', '/service-provider/',
            '/attorney/', '/lawyer/', '/doctor/', '/dentist/', '/contractor/',
            '/restaurant/', '/hotel/', '/clinic/'
        ]
        category_patterns = [
            '/category/', '/categories/', '/browse/', '/explore/', 
            '/industry/', '/type/', '/sector/', '/service/', '/services/',
            '/directory/', '/top/', '/best/', '/all-', '/find/',
            '/software-development/', '/web-design/', '/marketing-agencies/',
            '/companies/', '/agencies/', '/firms/'
        ]
        location_patterns = [
            '/location/', '/city/', '/state/', '/region/', '/area/',
            '/near-me/', '/local/', '/geo/', '/in-', '/-in-',
            '/us/', '/uk/', '/ca/', '/au/'  # Country codes
        ]
        
        # Check URL patterns
        for pattern in listing_patterns:
            if pattern in url_lower:
                return 'listing'
                
        for pattern in category_patterns:
            if pattern in url_lower:
                return 'category'
                
        for pattern in location_patterns:
            if pattern in url_lower:
                return 'location'
                
        # Check schemas
        if soup:
            schemas = self.extract_schemas(soup)
            for schema in schemas:
                schema_type = str(schema.get('@type', '')).lower()
                if any(t in schema_type for t in ['localbusiness', 'organization', 'place', 'product', 'softwareapplication', 'professionalservice']):
                    return 'listing'
                if 'itemlist' in schema_type or 'collectionpage' in schema_type or 'searchresultspage' in schema_type:
                    return 'category'
                    
        # Check page content patterns
        if soup:
            # Listings typically have contact info, hours, ratings, etc.
            has_phone = bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
            has_address = bool(re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|blvd|drive|dr|way|lane|ln)', text))
            has_hours = 'hours' in text or 'open' in text or 'monday' in text
            has_rating = bool(re.search(r'\d+(\.\d+)?\s*(star|rating|review|out of)', text))
            has_website_link = bool(soup.find('a', href=re.compile(r'^https?://', re.I), string=re.compile(r'website|visit|site', re.I)))
            
            listing_signals = sum([has_phone, has_address, has_hours, has_rating, has_website_link])
            if listing_signals >= 2:
                return 'listing'
                
            # Category pages have many links, filtering options
            links = soup.find_all('a', href=True)
            filter_words = ['filter', 'sort', 'showing', 'results', 'found', 'matching', 'search']
            if len(links) > 20 and any(w in text for w in filter_words):
                return 'category'
                
            # Check for list-like structures
            list_items = soup.find_all(['li', 'article', 'div'], class_=re.compile(r'result|listing|item|card', re.I))
            if len(list_items) >= 5:
                return 'category'
                
        return 'other'
        
    def discover_pages(self, sample_size: int = 30) -> None:
        """Discover and classify pages from the site"""
        print(f"  Discovering pages...")
        
        discovered_urls = set()
        
        # Add sitemap URLs
        if self.sitemap_urls:
            discovered_urls.update(self.sitemap_urls[:200])
            
        # Crawl homepage for links
        if self.soup:
            for link in self.soup.find_all('a', href=True):
                href = link['href']
                
                # Skip non-HTTP links
                if href.startswith(('javascript:', 'mailto:', 'tel:', '#', 'data:')):
                    continue
                    
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    href = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}{href}"
                elif not href.startswith('http'):
                    # Relative path without leading slash
                    href = urljoin(self.url, href)
                
                # Filter out invalid URLs
                parsed_href = urlparse(href)
                
                # Skip localhost, empty hosts, or external domains
                if parsed_href.netloc in ['localhost', '127.0.0.1', '']:
                    continue
                if parsed_href.netloc.startswith('localhost:'):
                    continue
                if self.domain not in parsed_href.netloc:
                    continue
                    
                if href.startswith('http'):
                    discovered_urls.add(href)
                    
        # Sample pages to analyze
        urls_to_check = list(discovered_urls)[:sample_size]
        
        print(f"  Analyzing {len(urls_to_check)} pages...")
        
        successful_fetches = 0
        failed_fetches = 0
        
        for url in urls_to_check:
            try:
                html, soup = self.fetch_page(url, timeout=10)
                if soup:
                    successful_fetches += 1
                    page_type = self.classify_page(url, soup)
                    page_data = {
                        'url': url,
                        'type': page_type,
                        'title': soup.find('title').get_text() if soup.find('title') else '',
                        'schemas': self.extract_schemas(soup),
                    }
                    
                    if page_type == 'listing':
                        self.listing_pages.append(page_data)
                    elif page_type == 'category':
                        self.category_pages.append(page_data)
                    elif page_type == 'location':
                        self.location_pages.append(page_data)
                    else:
                        self.other_pages.append(page_data)
                        
                    # Collect all schemas
                    self.all_schemas.extend(page_data['schemas'])
                else:
                    failed_fetches += 1
                    
            except Exception as e:
                failed_fetches += 1
                continue
                
        print(f"  Found: {len(self.listing_pages)} listings, {len(self.category_pages)} categories, "
              f"{len(self.location_pages)} locations, {len(self.other_pages)} other pages")
        
        if failed_fetches > successful_fetches and failed_fetches > 5:
            print(f"  ⚠️  Many pages failed to fetch ({failed_fetches}/{len(urls_to_check)}) - site may have bot protection")

    # =========================================================================
    # STRUCTURE & ARCHITECTURE CHECKS (50 points)
    # =========================================================================
    
    def check_listing_completeness(self) -> CategoryScore:
        """Category 1: Listing Completeness (10 pts)
        Do listings have full data (name, description, contact, images, categories)?
        """
        score = CategoryScore(name="Listing Completeness")
        findings = []
        recommendations = []
        points = 0
        details = {'listings_analyzed': 0, 'completeness_scores': []}
        
        if not self.listing_pages:
            findings.append("❌ No listing pages detected")
            recommendations.append("Ensure listing pages are properly structured with /listing/ or similar URL pattern")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        # Analyze sample of listings
        sample_listings = self.listing_pages[:10]
        details['listings_analyzed'] = len(sample_listings)
        
        total_completeness = 0
        
        for listing in sample_listings:
            try:
                html, soup = self.fetch_page(listing['url'], timeout=10)
                if not soup:
                    continue
                    
                text = soup.get_text().lower()
                listing_score = 0
                fields_found = []
                
                # Check for essential fields
                # Name (usually in H1)
                h1 = soup.find('h1')
                if h1 and len(h1.get_text().strip()) > 2:
                    listing_score += 1
                    fields_found.append('name')
                    
                # Description (substantial text content)
                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile(r'content|description', re.I))
                if main_content:
                    desc_text = main_content.get_text()
                    if len(desc_text) > 200:
                        listing_score += 1
                        fields_found.append('description')
                        
                # Phone number
                if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text):
                    listing_score += 1
                    fields_found.append('phone')
                    
                # Address
                if re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd|blvd|drive|dr|way|lane)', text):
                    listing_score += 1
                    fields_found.append('address')
                    
                # Images
                images = soup.find_all('img')
                content_images = [img for img in images if not any(x in str(img.get('src', '')).lower() 
                                for x in ['logo', 'icon', 'sprite', 'pixel', 'tracking'])]
                if len(content_images) >= 1:
                    listing_score += 1
                    fields_found.append('images')
                    
                # Categories/tags
                if soup.find_all('a', class_=re.compile(r'category|tag|badge', re.I)) or \
                   soup.find_all(class_=re.compile(r'category|tag|badge', re.I)):
                    listing_score += 1
                    fields_found.append('categories')
                    
                # Website link
                external_links = [a for a in soup.find_all('a', href=True) 
                                 if a['href'].startswith('http') and self.domain not in a['href']]
                if external_links:
                    listing_score += 1
                    fields_found.append('website')
                    
                # Hours
                if 'hours' in text or 'monday' in text or 'open' in text:
                    listing_score += 1
                    fields_found.append('hours')
                    
                completeness = listing_score / 8 * 100
                total_completeness += completeness
                details['completeness_scores'].append({
                    'url': listing['url'],
                    'score': completeness,
                    'fields': fields_found
                })
                
                time.sleep(0.1)
            except:
                continue
                
        if details['completeness_scores']:
            avg_completeness = total_completeness / len(details['completeness_scores'])
            details['average_completeness'] = f"{avg_completeness:.1f}%"
            
            if avg_completeness >= 80:
                findings.append(f"✅ Excellent listing completeness ({avg_completeness:.0f}% average)")
                points = 10
            elif avg_completeness >= 60:
                findings.append(f"⚠️ Good listing completeness ({avg_completeness:.0f}% average)")
                points = 7
            elif avg_completeness >= 40:
                findings.append(f"⚠️ Moderate listing completeness ({avg_completeness:.0f}% average)")
                points = 5
            else:
                findings.append(f"❌ Poor listing completeness ({avg_completeness:.0f}% average)")
                points = 2
                
            # Common missing fields
            all_fields = set()
            for s in details['completeness_scores']:
                all_fields.update(s['fields'])
            possible_fields = {'name', 'description', 'phone', 'address', 'images', 'categories', 'website', 'hours'}
            missing = possible_fields - all_fields
            
            if missing:
                recommendations.append(f"Add missing fields to listings: {', '.join(missing)}")
        else:
            findings.append("❌ Could not analyze listing completeness")
            points = 0
            
        findings.append(f"Analyzed {len(details['completeness_scores'])} listing pages")
        
        score.score = points
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_category_taxonomy(self) -> CategoryScore:
        """Category 2: Category Taxonomy (10 pts)
        Well-organized hierarchical categories? Breadcrumbs?
        """
        score = CategoryScore(name="Category Taxonomy")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Create organized category pages with breadcrumb navigation"]
            return score
            
        # Check for category navigation
        nav_elements = self.soup.find_all(['nav', 'aside', 'div'], class_=re.compile(r'categ|nav|menu|sidebar', re.I))
        
        category_links = []
        for nav in nav_elements:
            for link in nav.find_all('a', href=True):
                href = link['href'].lower()
                text = link.get_text().strip()
                if any(p in href for p in ['/category/', '/browse/', '/type/', '/service/', '/industry/']):
                    category_links.append({'url': href, 'text': text})
                    
        # Also check the discovered category pages
        if self.category_pages:
            details['category_pages_found'] = len(self.category_pages)
            findings.append(f"✅ {len(self.category_pages)} category pages detected")
            points += 3
        else:
            findings.append("⚠️ Limited category pages detected")
            recommendations.append("Create dedicated category landing pages for each main category")
            
        # Check for hierarchical structure (subcategories)
        has_hierarchy = False
        for page in self.category_pages[:5]:
            url = page['url']
            # Count path segments (more = deeper hierarchy)
            path = urlparse(url).path
            segments = [s for s in path.split('/') if s]
            if len(segments) >= 3:
                has_hierarchy = True
                break
                
        if has_hierarchy:
            findings.append("✅ Hierarchical category structure detected")
            points += 2
        else:
            findings.append("⚠️ Flat category structure")
            recommendations.append("Implement hierarchical categories (e.g., /restaurants/italian/pizza/)")
            
        # Check for breadcrumbs
        breadcrumb_found = False
        breadcrumb_patterns = [
            self.soup.find(class_=re.compile(r'breadcrumb', re.I)),
            self.soup.find('nav', {'aria-label': re.compile(r'breadcrumb', re.I)}),
            self.soup.find(itemtype=re.compile(r'BreadcrumbList', re.I)),
        ]
        
        if any(breadcrumb_patterns):
            findings.append("✅ Breadcrumb navigation present")
            points += 2
            breadcrumb_found = True
            
        # Check for BreadcrumbList schema
        breadcrumb_schema = any('BreadcrumbList' in str(s) for s in self.all_schemas)
        if breadcrumb_schema:
            findings.append("✅ BreadcrumbList schema implemented")
            points += 2
        else:
            recommendations.append("Add BreadcrumbList schema markup")
            if not breadcrumb_found:
                recommendations.append("Add visible breadcrumb navigation")
                
        # Check category count
        unique_categories = set()
        for page in self.category_pages:
            path = urlparse(page['url']).path
            # Extract likely category name from URL
            segments = path.split('/')
            for seg in segments:
                if seg and len(seg) > 2 and seg not in ['category', 'categories', 'browse']:
                    unique_categories.add(seg)
                    
        if len(unique_categories) >= 10:
            findings.append(f"✅ {len(unique_categories)}+ unique category segments")
            points += 1
        elif len(unique_categories) >= 5:
            findings.append(f"⚠️ {len(unique_categories)} unique category segments")
            
        details['unique_categories'] = list(unique_categories)[:20]
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_location_structure(self) -> CategoryScore:
        """Category 3: Location Structure (10 pts)
        City/state/region pages if geo-relevant?
        """
        score = CategoryScore(name="Location Structure")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # Check if directory appears geo-relevant
        geo_relevant = False
        if self.soup:
            text = self.soup.get_text().lower()
            geo_keywords = ['near me', 'local', 'in your area', 'city', 'location', 'find nearby', 'near you']
            if any(kw in text for kw in geo_keywords):
                geo_relevant = True
                
        # Check for location pages
        location_page_count = len(self.location_pages)
        
        # Also detect location patterns in all discovered URLs
        location_urls = []
        all_urls = [p['url'] for p in self.listing_pages + self.category_pages + self.location_pages + self.other_pages]
        
        # US states
        us_states = ['alabama', 'alaska', 'arizona', 'california', 'colorado', 'florida', 
                     'georgia', 'illinois', 'new-york', 'texas', 'washington']
        # Major cities
        major_cities = ['new-york', 'los-angeles', 'chicago', 'houston', 'phoenix', 'philadelphia',
                       'san-antonio', 'san-diego', 'dallas', 'austin', 'seattle', 'denver', 'boston']
        
        for url in all_urls:
            url_lower = url.lower()
            if any(state in url_lower for state in us_states) or \
               any(city in url_lower for city in major_cities):
                location_urls.append(url)
                
        if location_urls:
            location_page_count = max(location_page_count, len(set(location_urls)))
            
        details['location_pages_found'] = location_page_count
        
        if location_page_count >= 10:
            findings.append(f"✅ Excellent location coverage ({location_page_count}+ location pages)")
            points += 5
        elif location_page_count >= 5:
            findings.append(f"⚠️ Good location coverage ({location_page_count} location pages)")
            points += 3
        elif location_page_count > 0:
            findings.append(f"⚠️ Limited location coverage ({location_page_count} location pages)")
            points += 1
        else:
            if geo_relevant:
                findings.append("❌ No location-specific pages detected")
                recommendations.append("Create city/state landing pages (e.g., /restaurants/new-york/)")
            else:
                findings.append("ℹ️ Directory may not be geo-focused")
                points += 5  # Not penalized if not geo-relevant
                
        # Check for location in URL structure
        location_in_urls = any('/city/' in u or '/state/' in u or '/location/' in u 
                              for u in all_urls)
        if location_in_urls:
            findings.append("✅ Location segments in URL structure")
            points += 2
        elif geo_relevant:
            recommendations.append("Use location-based URL structure (/category/city/)")
            
        # Check for LocalBusiness schema with geo
        has_geo_schema = False
        for schema in self.all_schemas:
            if 'geo' in str(schema).lower() or 'addressLocality' in str(schema):
                has_geo_schema = True
                break
                
        if has_geo_schema:
            findings.append("✅ Location data in schema markup")
            points += 2
        elif geo_relevant:
            recommendations.append("Include geo coordinates in LocalBusiness schema")
            
        # Check for location filters/dropdowns
        if self.soup:
            location_filters = self.soup.find_all(['select', 'input'], 
                                                  attrs={'name': re.compile(r'location|city|state|zip', re.I)})
            if location_filters:
                findings.append("✅ Location filter/search available")
                points += 1
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_internal_linking(self) -> CategoryScore:
        """Category 4: Internal Linking (10 pts)
        Cross-links between related listings? Category hubs?
        """
        score = CategoryScore(name="Internal Linking")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Add internal links between related listings and category pages"]
            return score
            
        # Count internal links on homepage
        all_links = self.soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        
        for link in all_links:
            href = link['href']
            if href.startswith('/') or self.domain in href:
                internal_links.append(href)
            elif href.startswith('http'):
                external_links.append(href)
                
        details['homepage_internal_links'] = len(internal_links)
        details['homepage_external_links'] = len(external_links)
        
        if len(internal_links) >= 50:
            findings.append(f"✅ Strong internal linking ({len(internal_links)} internal links on homepage)")
            points += 3
        elif len(internal_links) >= 20:
            findings.append(f"⚠️ Moderate internal linking ({len(internal_links)} internal links)")
            points += 2
        else:
            findings.append(f"❌ Weak internal linking ({len(internal_links)} internal links)")
            recommendations.append("Add more internal links to category and listing pages")
            
        # Check for "related listings" sections
        related_patterns = ['related', 'similar', 'you may also like', 'see also', 'recommended']
        has_related = False
        
        # Check a sample listing page
        for listing in self.listing_pages[:3]:
            try:
                html, soup = self.fetch_page(listing['url'], timeout=8)
                if soup:
                    text = soup.get_text().lower()
                    if any(p in text for p in related_patterns):
                        has_related = True
                        break
                    # Also check for related section by class
                    if soup.find(class_=re.compile(r'related|similar|recommended', re.I)):
                        has_related = True
                        break
            except:
                continue
                
        if has_related:
            findings.append("✅ Related/similar listings sections found")
            points += 3
        else:
            findings.append("⚠️ No related listings sections detected")
            recommendations.append("Add 'Related Listings' or 'Similar Businesses' sections")
            
        # Check for category hub links
        category_link_sections = self.soup.find_all(['section', 'div'], 
                                                     class_=re.compile(r'categor|browse|explore', re.I))
        if category_link_sections:
            findings.append("✅ Category hub/browse sections present")
            points += 2
        else:
            recommendations.append("Add category hub sections linking to main categories")
            
        # Check for footer links to categories
        footer = self.soup.find('footer')
        if footer:
            footer_links = footer.find_all('a', href=True)
            footer_category_links = [l for l in footer_links 
                                    if any(p in l['href'].lower() for p in ['/category/', '/browse/', '/type/'])]
            if len(footer_category_links) >= 5:
                findings.append(f"✅ Footer contains {len(footer_category_links)} category links")
                points += 2
            elif footer_category_links:
                findings.append(f"⚠️ Footer has limited category links ({len(footer_category_links)})")
                points += 1
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_url_structure(self) -> CategoryScore:
        """Category 5: URL Structure (10 pts)
        Clean, logical URLs (/category/subcategory/listing-name)?
        """
        score = CategoryScore(name="URL Structure")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # Analyze URL patterns
        all_urls = [p['url'] for p in self.listing_pages + self.category_pages + self.location_pages]
        
        if not all_urls:
            findings.append("❌ No URLs to analyze")
            recommendations.append("Ensure the site has a clear URL structure with category and listing pages")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        # Check for clean URLs (no query parameters for main pages)
        urls_with_params = [u for u in all_urls if '?' in u]
        clean_url_ratio = (len(all_urls) - len(urls_with_params)) / len(all_urls) * 100
        
        details['clean_url_ratio'] = f"{clean_url_ratio:.0f}%"
        
        if clean_url_ratio >= 90:
            findings.append(f"✅ Clean URLs ({clean_url_ratio:.0f}% without query parameters)")
            points += 3
        elif clean_url_ratio >= 70:
            findings.append(f"⚠️ Mostly clean URLs ({clean_url_ratio:.0f}%)")
            points += 2
        else:
            findings.append(f"❌ Many URLs have query parameters ({clean_url_ratio:.0f}% clean)")
            recommendations.append("Use clean, readable URLs without query parameters")
            
        # Check for readable slugs (no numeric IDs)
        numeric_pattern = r'/\d{5,}/'  # URLs with 5+ digit IDs
        urls_with_ids = [u for u in all_urls if re.search(numeric_pattern, u)]
        
        if not urls_with_ids:
            findings.append("✅ URLs use readable slugs (no numeric IDs)")
            points += 2
        else:
            findings.append(f"⚠️ {len(urls_with_ids)} URLs contain numeric IDs")
            recommendations.append("Replace numeric IDs with descriptive slugs (e.g., /business-name/ not /12345/)")
            points += 1
            
        # Check for logical hierarchy
        hierarchical_urls = 0
        for url in all_urls:
            path = urlparse(url).path
            segments = [s for s in path.split('/') if s]
            if len(segments) >= 2:
                hierarchical_urls += 1
                
        hierarchy_ratio = hierarchical_urls / len(all_urls) * 100 if all_urls else 0
        details['hierarchical_url_ratio'] = f"{hierarchy_ratio:.0f}%"
        
        if hierarchy_ratio >= 80:
            findings.append("✅ Logical URL hierarchy (/category/listing/)")
            points += 3
        elif hierarchy_ratio >= 50:
            findings.append("⚠️ Some hierarchical URL structure")
            points += 2
        else:
            recommendations.append("Use hierarchical URLs: /category/subcategory/listing-name/")
            
        # Check for lowercase and hyphens
        bad_urls = [u for u in all_urls if re.search(r'[A-Z]|_', urlparse(u).path)]
        if not bad_urls:
            findings.append("✅ URLs are lowercase with hyphens")
            points += 2
        else:
            findings.append(f"⚠️ {len(bad_urls)} URLs have uppercase or underscores")
            recommendations.append("Use lowercase letters and hyphens in URLs")
            points += 1
            
        # Sample URL examples
        details['sample_urls'] = all_urls[:5]
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    # =========================================================================
    # ON-PAGE SEO CHECKS (50 points)
    # =========================================================================
    
    def check_title_optimization(self) -> CategoryScore:
        """Category 6: Title Tag Optimization (10 pts)
        Unique, keyword-rich titles per listing/category?
        """
        score = CategoryScore(name="Title Tag Optimization")
        findings = []
        recommendations = []
        points = 0
        details = {'titles_analyzed': [], 'duplicate_titles': False}
        
        # Collect titles from different page types
        pages_to_check = (self.listing_pages[:5] + self.category_pages[:5])[:10]
        titles = []
        
        for page in pages_to_check:
            try:
                html, soup = self.fetch_page(page['url'], timeout=8)
                if soup:
                    title_tag = soup.find('title')
                    if title_tag:
                        title = title_tag.get_text().strip()
                        titles.append({
                            'url': page['url'],
                            'title': title,
                            'length': len(title)
                        })
                time.sleep(0.1)
            except:
                continue
                
        if not titles:
            findings.append("❌ Could not analyze title tags")
            recommendations.append("Ensure each page has a unique, keyword-rich title tag (50-60 characters)")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        details['titles_analyzed'] = titles
        
        # Check for unique titles
        title_texts = [t['title'] for t in titles]
        unique_titles = set(title_texts)
        
        if len(unique_titles) == len(title_texts):
            findings.append(f"✅ All {len(titles)} titles are unique")
            points += 4
        else:
            duplicate_count = len(title_texts) - len(unique_titles)
            findings.append(f"❌ {duplicate_count} duplicate title(s) found")
            details['duplicate_titles'] = True
            recommendations.append("Ensure every page has a unique title tag")
            points += 1
            
        # Check title length (optimal: 50-60 chars)
        optimal_titles = [t for t in titles if 50 <= t['length'] <= 60]
        too_long = [t for t in titles if t['length'] > 60]
        too_short = [t for t in titles if t['length'] < 30]
        
        if len(optimal_titles) >= len(titles) * 0.7:
            findings.append(f"✅ {len(optimal_titles)}/{len(titles)} titles have optimal length (50-60 chars)")
            points += 3
        else:
            if too_long:
                findings.append(f"⚠️ {len(too_long)} titles are too long (>60 chars)")
                recommendations.append("Shorten title tags to 50-60 characters")
            if too_short:
                findings.append(f"⚠️ {len(too_short)} titles are too short (<30 chars)")
                recommendations.append("Expand short titles with relevant keywords")
            points += 1
            
        # Check for keyword presence in titles
        # Look for common directory patterns
        keyword_patterns = ['best', 'top', 'find', 'directory', 'near', 'local', 'review']
        titles_with_keywords = sum(1 for t in titles if any(kw in t['title'].lower() for kw in keyword_patterns))
        
        if titles_with_keywords >= len(titles) * 0.6:
            findings.append("✅ Titles include relevant keywords")
            points += 2
        else:
            recommendations.append("Add search-intent keywords to titles (best, top, find, near me)")
            points += 1
            
        # Check for branding in titles
        brand_in_titles = sum(1 for t in titles if '|' in t['title'] or '-' in t['title'])
        if brand_in_titles >= len(titles) * 0.8:
            findings.append("✅ Consistent branding in titles")
            points += 1
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_meta_descriptions(self) -> CategoryScore:
        """Category 7: Meta Descriptions (10 pts)
        Unique descriptions for each page type?
        """
        score = CategoryScore(name="Meta Descriptions")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        pages_to_check = (self.listing_pages[:5] + self.category_pages[:5])[:10]
        descriptions = []
        
        for page in pages_to_check:
            try:
                html, soup = self.fetch_page(page['url'], timeout=8)
                if soup:
                    meta_desc = soup.find('meta', {'name': 'description'})
                    if meta_desc and meta_desc.get('content'):
                        content = meta_desc['content'].strip()
                        descriptions.append({
                            'url': page['url'],
                            'description': content,
                            'length': len(content)
                        })
                    else:
                        descriptions.append({
                            'url': page['url'],
                            'description': None,
                            'length': 0
                        })
                time.sleep(0.1)
            except:
                continue
                
        if not descriptions:
            findings.append("❌ Could not analyze meta descriptions")
            recommendations.append("Add unique meta descriptions (150-160 characters) to all pages")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        # Check for presence
        pages_with_desc = [d for d in descriptions if d['description']]
        pages_without_desc = [d for d in descriptions if not d['description']]
        
        if len(pages_with_desc) == len(descriptions):
            findings.append(f"✅ All {len(descriptions)} pages have meta descriptions")
            points += 3
        elif len(pages_without_desc) > 0:
            findings.append(f"❌ {len(pages_without_desc)} pages missing meta descriptions")
            recommendations.append("Add unique meta descriptions to all pages")
            points += 1
            
        # Check uniqueness
        if pages_with_desc:
            desc_texts = [d['description'] for d in pages_with_desc]
            unique_descs = set(desc_texts)
            
            if len(unique_descs) == len(desc_texts):
                findings.append("✅ All meta descriptions are unique")
                points += 3
            else:
                duplicate_count = len(desc_texts) - len(unique_descs)
                findings.append(f"⚠️ {duplicate_count} duplicate meta descriptions")
                recommendations.append("Write unique meta descriptions for each page")
                points += 1
                
            # Check length (optimal: 150-160 chars)
            optimal_length = [d for d in pages_with_desc if 150 <= d['length'] <= 160]
            too_short = [d for d in pages_with_desc if d['length'] < 120]
            
            if len(optimal_length) >= len(pages_with_desc) * 0.6:
                findings.append("✅ Meta descriptions have optimal length")
                points += 2
            else:
                if too_short:
                    findings.append(f"⚠️ {len(too_short)} meta descriptions are too short")
                    recommendations.append("Expand meta descriptions to 150-160 characters")
                points += 1
                
            # Check for call-to-action
            cta_patterns = ['find', 'discover', 'explore', 'browse', 'compare', 'read reviews', 'get quotes']
            descs_with_cta = sum(1 for d in pages_with_desc 
                                if any(cta in d['description'].lower() for cta in cta_patterns))
            if descs_with_cta >= len(pages_with_desc) * 0.5:
                findings.append("✅ Meta descriptions include calls-to-action")
                points += 2
            else:
                recommendations.append("Add action-oriented language to meta descriptions")
                
        details['descriptions_analyzed'] = len(descriptions)
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_heading_structure(self) -> CategoryScore:
        """Category 8: Heading Structure (10 pts)
        Proper H1/H2/H3 hierarchy?
        """
        score = CategoryScore(name="Heading Structure")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # Analyze homepage + sample pages
        pages_to_check = [{'url': self.url, 'type': 'homepage'}]
        if self.listing_pages:
            pages_to_check.append(self.listing_pages[0])
        if self.category_pages:
            pages_to_check.append(self.category_pages[0])
            
        heading_analysis = []
        
        for page in pages_to_check:
            try:
                if page['url'] == self.url:
                    soup = self.soup
                else:
                    _, soup = self.fetch_page(page['url'], timeout=8)
                    
                if soup:
                    h1s = soup.find_all('h1')
                    h2s = soup.find_all('h2')
                    h3s = soup.find_all('h3')
                    
                    heading_analysis.append({
                        'url': page['url'],
                        'h1_count': len(h1s),
                        'h2_count': len(h2s),
                        'h3_count': len(h3s),
                        'h1_text': [h.get_text().strip()[:100] for h in h1s]
                    })
            except:
                continue
                
        if not heading_analysis:
            findings.append("❌ Could not analyze heading structure")
            recommendations.append("Use a single H1 tag per page and H2/H3 for content hierarchy")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        details['heading_analysis'] = heading_analysis
        
        # Check H1 usage
        pages_with_single_h1 = sum(1 for h in heading_analysis if h['h1_count'] == 1)
        pages_with_multiple_h1 = sum(1 for h in heading_analysis if h['h1_count'] > 1)
        pages_without_h1 = sum(1 for h in heading_analysis if h['h1_count'] == 0)
        
        if pages_with_single_h1 == len(heading_analysis):
            findings.append("✅ All pages have exactly one H1")
            points += 4
        else:
            if pages_without_h1:
                findings.append(f"❌ {pages_without_h1} page(s) missing H1")
                recommendations.append("Add a single H1 tag to every page")
            if pages_with_multiple_h1:
                findings.append(f"⚠️ {pages_with_multiple_h1} page(s) have multiple H1s")
                recommendations.append("Use only one H1 tag per page")
            points += 1
            
        # Check H2/H3 usage
        pages_with_h2 = sum(1 for h in heading_analysis if h['h2_count'] >= 2)
        pages_with_h3 = sum(1 for h in heading_analysis if h['h3_count'] >= 1)
        
        if pages_with_h2 >= len(heading_analysis) * 0.8:
            findings.append("✅ Good use of H2 tags for content sections")
            points += 3
        else:
            findings.append("⚠️ Limited H2 tag usage")
            recommendations.append("Use H2 tags to break content into logical sections")
            points += 1
            
        if pages_with_h3 >= len(heading_analysis) * 0.5:
            findings.append("✅ H3 tags used for subsections")
            points += 2
        else:
            findings.append("⚠️ Consider adding H3 tags for better hierarchy")
            points += 1
            
        # Check heading text quality
        all_h1_texts = [h for analysis in heading_analysis for h in analysis['h1_text']]
        if all_h1_texts:
            avg_h1_length = sum(len(h) for h in all_h1_texts) / len(all_h1_texts)
            if 20 <= avg_h1_length <= 70:
                findings.append("✅ H1 tags have appropriate length")
                points += 1
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_schema_markup(self) -> CategoryScore:
        """Category 9: Schema Markup (10 pts)
        LocalBusiness, Product, AggregateRating, ItemList, BreadcrumbList?
        """
        score = CategoryScore(name="Schema Markup")
        findings = []
        recommendations = []
        points = 0
        details = {'schemas_found': [], 'schema_types': []}
        
        if not self.all_schemas:
            # Try to collect from main page
            if self.soup:
                self.all_schemas = self.extract_schemas(self.soup)
                
        if not self.all_schemas:
            findings.append("❌ No JSON-LD structured data found")
            recommendations.append("Implement JSON-LD schema markup - critical for SEO")
            recommendations.append("Add LocalBusiness schema for listing pages")
            recommendations.append("Add ItemList schema for category pages")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        # Collect all schema types
        schema_types = []
        for schema in self.all_schemas:
            schema_type = schema.get('@type', 'Unknown')
            if isinstance(schema_type, list):
                schema_types.extend(schema_type)
            else:
                schema_types.append(schema_type)
                
        schema_types = list(set(schema_types))
        details['schema_types'] = schema_types
        
        findings.append(f"Found schema types: {', '.join(schema_types[:5])}")
        
        # Check for directory-critical schemas
        critical_schemas = {
            'LocalBusiness': 2,  # Points awarded
            'Organization': 1,
            'Product': 1,
            'Service': 1,
            'ItemList': 2,
            'CollectionPage': 1,
            'BreadcrumbList': 2,
            'AggregateRating': 2,
            'Review': 1,
            'FAQPage': 1,
            'WebSite': 1,
            'SearchAction': 1,
        }
        
        for schema_name, pts in critical_schemas.items():
            if any(schema_name.lower() in str(s).lower() for s in schema_types):
                findings.append(f"✅ {schema_name} schema implemented")
                points += pts
            else:
                if schema_name in ['LocalBusiness', 'ItemList', 'BreadcrumbList', 'AggregateRating']:
                    recommendations.append(f"Add {schema_name} schema markup")
                    
        # Check schema completeness for LocalBusiness
        has_complete_local = False
        for schema in self.all_schemas:
            if 'LocalBusiness' in str(schema.get('@type', '')):
                required_fields = ['name', 'address', 'telephone']
                optional_fields = ['openingHours', 'geo', 'image', 'priceRange']
                
                found_required = sum(1 for f in required_fields if f in str(schema))
                found_optional = sum(1 for f in optional_fields if f in str(schema))
                
                if found_required >= 2:
                    has_complete_local = True
                    if found_optional >= 2:
                        findings.append("✅ LocalBusiness schema is comprehensive")
                        points += 1
                    else:
                        findings.append("⚠️ LocalBusiness schema could be more complete")
                        recommendations.append("Add openingHours, geo, and image to LocalBusiness schema")
                break
                
        details['has_local_business'] = has_complete_local
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_pagination_canonicals(self) -> CategoryScore:
        """Category 10: Pagination/Canonicals (10 pts)
        Proper handling of paginated category pages?
        """
        score = CategoryScore(name="Pagination & Canonicals")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # Check homepage for canonical
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Add canonical tags and proper pagination handling"]
            return score
            
        # Check canonical tag
        canonical = self.soup.find('link', rel='canonical')
        if canonical and canonical.get('href'):
            findings.append(f"✅ Canonical tag present")
            points += 3
            details['canonical_url'] = canonical['href']
        else:
            findings.append("❌ No canonical tag found")
            recommendations.append("Add canonical tags to all pages")
            
        # Check a category page for pagination
        pagination_checked = False
        for cat_page in self.category_pages[:3]:
            try:
                html, soup = self.fetch_page(cat_page['url'], timeout=8)
                if not soup:
                    continue
                    
                # Look for pagination elements
                pagination = soup.find(class_=re.compile(r'paginat', re.I)) or \
                            soup.find('nav', {'aria-label': re.compile(r'paginat', re.I)}) or \
                            soup.find_all('a', href=re.compile(r'page[=/]?\d+', re.I))
                            
                if pagination:
                    pagination_checked = True
                    findings.append("✅ Pagination detected on category pages")
                    
                    # Check for rel prev/next (deprecated but still useful)
                    prev_link = soup.find('link', rel='prev')
                    next_link = soup.find('link', rel='next')
                    
                    if prev_link or next_link:
                        findings.append("✅ rel='prev'/'next' links present")
                        points += 2
                    else:
                        findings.append("ℹ️ No rel='prev'/'next' (optional)")
                        points += 1
                        
                    # Check canonical on paginated page
                    page_canonical = soup.find('link', rel='canonical')
                    if page_canonical:
                        findings.append("✅ Canonical on paginated page")
                        points += 2
                    else:
                        recommendations.append("Add canonical tags to paginated pages")
                        
                    break
            except:
                continue
                
        if not pagination_checked:
            findings.append("ℹ️ No pagination detected (may be single-page categories)")
            points += 3  # Not penalized if no pagination needed
            
        # Check for noindex on filter/sort pages
        if self.robots_txt:
            if 'disallow: /*?' in self.robots_txt.lower() or 'disallow: /*sort' in self.robots_txt.lower():
                findings.append("✅ Filter/sort URLs blocked in robots.txt")
                points += 2
            else:
                recommendations.append("Block filter/sort URLs in robots.txt to prevent duplicate content")
                
        # Check meta robots
        meta_robots = self.soup.find('meta', {'name': 'robots'})
        if meta_robots:
            content = meta_robots.get('content', '').lower()
            details['meta_robots'] = content
            if 'noindex' not in content:
                findings.append("✅ Main pages are indexable")
                points += 1
        else:
            points += 1  # Default is indexable
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    # =========================================================================
    # CONTENT QUALITY CHECKS (40 points)
    # =========================================================================
    
    def check_listing_descriptions(self) -> CategoryScore:
        """Category 11: Listing Descriptions (10 pts)
        Unique, substantive content vs thin/duplicate?
        """
        score = CategoryScore(name="Listing Descriptions")
        findings = []
        recommendations = []
        points = 0
        details = {'descriptions_analyzed': []}
        
        if not self.listing_pages:
            findings.append("❌ No listing pages to analyze")
            recommendations.append("Create dedicated listing pages with unique, substantive content (300+ words)")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        # Analyze sample of listings for description quality
        descriptions = []
        for listing in self.listing_pages[:8]:
            try:
                html, soup = self.fetch_page(listing['url'], timeout=8)
                if not soup:
                    continue
                    
                # Find main content area
                main_content = soup.find('main') or soup.find('article') or \
                              soup.find(class_=re.compile(r'content|description|detail', re.I))
                              
                if main_content:
                    # Remove nav, footer, scripts
                    for tag in main_content.find_all(['nav', 'footer', 'script', 'style', 'aside']):
                        tag.decompose()
                        
                    text = main_content.get_text(separator=' ', strip=True)
                    word_count = len(text.split())
                    
                    descriptions.append({
                        'url': listing['url'],
                        'word_count': word_count,
                        'text_sample': text[:200] if text else ''
                    })
                    
                time.sleep(0.1)
            except:
                continue
                
        if not descriptions:
            findings.append("❌ Could not extract listing descriptions")
            recommendations.append("Ensure listing pages have substantial, unique content (300+ words per listing)")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        details['descriptions_analyzed'] = descriptions
        
        # Analyze word counts
        word_counts = [d['word_count'] for d in descriptions]
        avg_words = sum(word_counts) / len(word_counts)
        
        details['avg_word_count'] = f"{avg_words:.0f}"
        
        if avg_words >= 300:
            findings.append(f"✅ Substantive descriptions (avg {avg_words:.0f} words)")
            points += 4
        elif avg_words >= 150:
            findings.append(f"⚠️ Moderate description length (avg {avg_words:.0f} words)")
            points += 2
            recommendations.append("Expand listing descriptions to 300+ words")
        else:
            findings.append(f"❌ Thin content (avg {avg_words:.0f} words)")
            recommendations.append("Significantly expand listing descriptions - aim for 300+ words")
            
        # Check for duplicate content
        text_samples = [d['text_sample'] for d in descriptions if d['text_sample']]
        unique_samples = set(text_samples)
        
        if len(unique_samples) == len(text_samples):
            findings.append("✅ All descriptions appear unique")
            points += 3
        else:
            duplicate_count = len(text_samples) - len(unique_samples)
            findings.append(f"❌ {duplicate_count} potentially duplicate descriptions")
            recommendations.append("Generate unique descriptions for each listing")
            points += 1
            
        # Check for templated/boilerplate content
        boilerplate_ratio = 0
        if len(text_samples) >= 2:
            # Simple similarity check
            common_phrases = []
            for i, sample1 in enumerate(text_samples):
                for sample2 in text_samples[i+1:]:
                    # Find common substrings
                    words1 = set(sample1.lower().split())
                    words2 = set(sample2.lower().split())
                    overlap = len(words1 & words2) / max(len(words1), len(words2)) if words1 and words2 else 0
                    if overlap > 0.5:
                        boilerplate_ratio += 1
                        
        if boilerplate_ratio == 0:
            findings.append("✅ Descriptions are not templated")
            points += 3
        elif boilerplate_ratio <= 2:
            findings.append("⚠️ Some templated content detected")
            points += 1
            recommendations.append("Reduce boilerplate text, add unique content per listing")
        else:
            findings.append("❌ Heavy use of templated content")
            recommendations.append("Use AI to generate unique descriptions based on listing data")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_user_generated_content(self) -> CategoryScore:
        """Category 12: User-Generated Content (10 pts)
        Reviews, ratings, comments?
        """
        score = CategoryScore(name="User-Generated Content")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # Check for reviews/ratings on homepage and listings
        ugc_indicators = {
            'reviews': False,
            'ratings': False,
            'comments': False,
            'questions': False,
            'user_photos': False
        }
        
        # Check homepage
        if self.soup:
            text = self.soup.get_text().lower()
            html_lower = str(self.soup).lower()
            
            # Reviews
            if 'review' in text or 'testimonial' in text:
                ugc_indicators['reviews'] = True
                
            # Ratings (star ratings)
            if re.search(r'\d+(\.\d+)?\s*(star|rating|out of)', text) or \
               'star-rating' in html_lower or 'rating' in html_lower:
                ugc_indicators['ratings'] = True
                
            # Comments
            if 'comment' in text and 'leave a comment' not in text:
                ugc_indicators['comments'] = True
                
        # Check listing pages for UGC
        for listing in self.listing_pages[:3]:
            try:
                html, soup = self.fetch_page(listing['url'], timeout=8)
                if soup:
                    text = soup.get_text().lower()
                    html_lower = str(soup).lower()
                    
                    if 'review' in text:
                        ugc_indicators['reviews'] = True
                    if re.search(r'\d+\s*reviews?', text):
                        ugc_indicators['reviews'] = True
                    if 'star' in html_lower or 'rating' in html_lower:
                        ugc_indicators['ratings'] = True
                    if 'q&a' in text or 'question' in text:
                        ugc_indicators['questions'] = True
                        
                    # User photos
                    if 'user photo' in text or 'customer photo' in text:
                        ugc_indicators['user_photos'] = True
                        
            except:
                continue
                
        details['ugc_indicators'] = ugc_indicators
        
        # Score based on UGC presence
        if ugc_indicators['reviews']:
            findings.append("✅ Review system detected")
            points += 3
        else:
            findings.append("❌ No review system detected")
            recommendations.append("Add a review/rating system for listings")
            
        if ugc_indicators['ratings']:
            findings.append("✅ Rating system (stars) present")
            points += 3
        else:
            recommendations.append("Display star ratings on listings")
            
        if ugc_indicators['comments'] or ugc_indicators['questions']:
            findings.append("✅ Comments or Q&A feature detected")
            points += 2
        else:
            recommendations.append("Consider adding Q&A or comments section")
            
        if ugc_indicators['user_photos']:
            findings.append("✅ User-submitted photos supported")
            points += 2
        else:
            recommendations.append("Allow users to upload photos for listings")
            
        # Check for AggregateRating schema
        has_rating_schema = any('AggregateRating' in str(s) or 'aggregateRating' in str(s) 
                               for s in self.all_schemas)
        if has_rating_schema:
            findings.append("✅ AggregateRating schema implemented")
            points += 2
        else:
            recommendations.append("Add AggregateRating schema for rich snippets")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_editorial_content(self) -> CategoryScore:
        """Category 13: Editorial Content (10 pts)
        Blog posts, guides, 'best of' articles?
        """
        score = CategoryScore(name="Editorial Content")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Add a blog section with industry guides and 'Best of' articles"]
            return score
            
        # Check navigation for editorial sections
        nav_text = ''
        for nav in self.soup.find_all(['nav', 'header']):
            nav_text += nav.get_text().lower()
            
        editorial_sections = {
            'blog': False,
            'guides': False,
            'resources': False,
            'articles': False,
            'news': False,
            'best_of': False
        }
        
        if 'blog' in nav_text:
            editorial_sections['blog'] = True
        if 'guide' in nav_text or 'how to' in nav_text:
            editorial_sections['guides'] = True
        if 'resource' in nav_text:
            editorial_sections['resources'] = True
        if 'article' in nav_text or 'insight' in nav_text:
            editorial_sections['articles'] = True
        if 'news' in nav_text:
            editorial_sections['news'] = True
            
        # Check for "best of" content
        page_text = self.soup.get_text().lower()
        if 'best ' in page_text or 'top 10' in page_text or 'top ' in page_text:
            editorial_sections['best_of'] = True
            
        details['editorial_sections'] = editorial_sections
        
        # Score based on editorial presence
        sections_found = sum(editorial_sections.values())
        
        if sections_found >= 3:
            findings.append(f"✅ Rich editorial content ({sections_found} sections)")
            points += 6
        elif sections_found >= 2:
            findings.append(f"⚠️ Some editorial content ({sections_found} sections)")
            points += 4
        elif sections_found >= 1:
            findings.append(f"⚠️ Limited editorial content ({sections_found} section)")
            points += 2
        else:
            findings.append("❌ No editorial content sections found")
            recommendations.append("Add a blog section with industry content")
            
        # List what was found
        found_sections = [k for k, v in editorial_sections.items() if v]
        if found_sections:
            findings.append(f"Found: {', '.join(found_sections)}")
            
        # Check for "best of" or comparison pages
        if editorial_sections['best_of']:
            findings.append("✅ 'Best of' or comparison content present")
            points += 2
        else:
            recommendations.append("Create 'Best [Category] in [Location]' articles")
            
        # Specific recommendations based on what's missing
        if not editorial_sections['blog']:
            recommendations.append("Start a blog with weekly industry content")
        if not editorial_sections['guides']:
            recommendations.append("Create how-to guides for your audience")
            
        # Check for article schema
        has_article_schema = any('Article' in str(s.get('@type', '')) for s in self.all_schemas)
        if has_article_schema:
            findings.append("✅ Article schema implemented")
            points += 2
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_content_freshness(self) -> CategoryScore:
        """Category 14: Content Freshness (10 pts)
        Recently updated listings? Dates visible?
        """
        score = CategoryScore(name="Content Freshness")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Display last updated dates on listings and add dateModified schema"]
            return score
            
        # Check for dates on the page
        text = self.soup.get_text()
        
        # Look for recent dates (2024, 2025, 2026)
        recent_date_patterns = [
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+202[4-6]',
            r'202[4-6]-\d{2}-\d{2}',
            r'\d{1,2}/\d{1,2}/202[4-6]',
            r'updated?\s*:?\s*202[4-6]',
            r'last updated',
        ]
        
        recent_dates_found = []
        for pattern in recent_date_patterns:
            matches = re.findall(pattern, text, re.I)
            recent_dates_found.extend(matches)
            
        if recent_dates_found:
            findings.append(f"✅ Recent dates visible in content")
            points += 3
        else:
            findings.append("⚠️ No recent dates visible")
            recommendations.append("Display last updated dates on listings and categories")
            
        # Check for dateModified/datePublished in schema
        has_date_schema = False
        for schema in self.all_schemas:
            if 'dateModified' in str(schema) or 'datePublished' in str(schema):
                has_date_schema = True
                break
                
        if has_date_schema:
            findings.append("✅ Date metadata in schema markup")
            points += 3
        else:
            findings.append("❌ No date metadata in schema")
            recommendations.append("Add dateModified and datePublished to schema")
            
        # Check for "new" or "recently added" sections
        freshness_indicators = ['new listing', 'recently added', 'latest', 'new arrival', 
                               'just added', 'updated today', 'this week']
        page_text_lower = text.lower()
        
        freshness_found = any(indicator in page_text_lower for indicator in freshness_indicators)
        if freshness_found:
            findings.append("✅ 'New' or 'Recently Added' content sections")
            points += 2
        else:
            recommendations.append("Add 'Recently Added' or 'New Listings' section")
            
        # Check meta tag dates
        meta_date = self.soup.find('meta', {'property': 'article:modified_time'}) or \
                   self.soup.find('meta', {'property': 'article:published_time'})
        if meta_date:
            findings.append("✅ Date meta tags present")
            points += 2
            details['meta_date'] = meta_date.get('content', '')
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    # =========================================================================
    # TECHNICAL SEO CHECKS (30 points)
    # =========================================================================
    
    def check_page_speed(self) -> CategoryScore:
        """Category 15: Page Speed (10 pts)
        Core Web Vitals for listing/category pages
        """
        score = CategoryScore(name="Page Speed")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Optimize page speed with lazy loading, WebP images, and async scripts"]
            return score
            
        # Basic performance indicators we can check without API
        
        # 1. Check for render-blocking resources
        head = self.soup.find('head')
        if head:
            scripts_in_head = head.find_all('script', src=True)
            blocking_scripts = [s for s in scripts_in_head 
                              if not s.get('async') and not s.get('defer')]
            
            if len(blocking_scripts) <= 2:
                findings.append(f"✅ Minimal render-blocking scripts ({len(blocking_scripts)})")
                points += 2
            else:
                findings.append(f"⚠️ {len(blocking_scripts)} render-blocking scripts in head")
                recommendations.append("Add async/defer to JavaScript files")
                points += 1
                
            details['blocking_scripts'] = len(blocking_scripts)
            
        # 2. Check image optimization
        images = self.soup.find_all('img')
        if images:
            lazy_images = [img for img in images if img.get('loading') == 'lazy']
            webp_images = [img for img in images if '.webp' in str(img.get('src', ''))]
            
            details['total_images'] = len(images)
            details['lazy_loaded'] = len(lazy_images)
            details['webp_format'] = len(webp_images)
            
            if len(lazy_images) >= len(images) * 0.5:
                findings.append(f"✅ Lazy loading implemented ({len(lazy_images)}/{len(images)} images)")
                points += 2
            else:
                findings.append(f"⚠️ Limited lazy loading ({len(lazy_images)}/{len(images)} images)")
                recommendations.append("Implement lazy loading for below-fold images")
                points += 1
                
            if len(webp_images) >= len(images) * 0.3:
                findings.append("✅ WebP image format in use")
                points += 1
            else:
                recommendations.append("Convert images to WebP format")
                
        # 3. Check page size
        if self.html:
            html_size_kb = len(self.html) / 1024
            details['html_size_kb'] = f"{html_size_kb:.1f}"
            
            if html_size_kb < 100:
                findings.append(f"✅ Lightweight HTML ({html_size_kb:.0f}KB)")
                points += 2
            elif html_size_kb < 300:
                findings.append(f"⚠️ Moderate HTML size ({html_size_kb:.0f}KB)")
                points += 1
            else:
                findings.append(f"❌ Heavy HTML ({html_size_kb:.0f}KB)")
                recommendations.append("Reduce page size - compress HTML, remove unused code")
                
        # 4. Check for CDN indicators
        cdn_indicators = ['cloudflare', 'cloudfront', 'akamai', 'fastly', 'cdn']
        html_lower = self.html.lower() if self.html else ''
        
        if any(cdn in html_lower for cdn in cdn_indicators):
            findings.append("✅ CDN detected")
            points += 1
        else:
            recommendations.append("Consider using a CDN for faster global delivery")
            
        # 5. Check for preload/preconnect
        preloads = self.soup.find_all('link', rel='preload')
        preconnects = self.soup.find_all('link', rel='preconnect')
        
        if preloads or preconnects:
            findings.append(f"✅ Resource hints present (preload/preconnect)")
            points += 1
        else:
            recommendations.append("Add preconnect for critical third-party domains")
            
        # Note about full CWV
        findings.append("ℹ️ Full Core Web Vitals require PageSpeed Insights API")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_mobile_usability(self) -> CategoryScore:
        """Category 16: Mobile Usability (10 pts)
        Responsive design, touch-friendly filters?
        """
        score = CategoryScore(name="Mobile Usability")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Add mobile viewport, responsive design, and touch-friendly elements"]
            return score
            
        # 1. Check viewport meta tag
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if viewport:
            content = viewport.get('content', '')
            details['viewport'] = content
            
            if 'width=device-width' in content:
                findings.append("✅ Mobile viewport configured correctly")
                points += 3
            else:
                findings.append("⚠️ Viewport meta tag present but may not be optimal")
                points += 1
        else:
            findings.append("❌ No viewport meta tag")
            recommendations.append("Add mobile viewport meta tag")
            
        # 2. Check for responsive design indicators
        # Look for media queries in inline styles or responsive classes
        html_str = str(self.soup)
        
        responsive_indicators = [
            '@media',
            'col-md', 'col-sm', 'col-lg',  # Bootstrap
            'sm:', 'md:', 'lg:',  # Tailwind
            'responsive',
            'mobile'
        ]
        
        responsive_count = sum(1 for indicator in responsive_indicators if indicator in html_str)
        
        if responsive_count >= 3:
            findings.append("✅ Strong responsive design indicators")
            points += 3
        elif responsive_count >= 1:
            findings.append("⚠️ Some responsive design elements")
            points += 1
        else:
            findings.append("⚠️ Limited responsive indicators (may still be responsive)")
            
        # 3. Check for touch-friendly elements
        # Look for appropriately sized buttons/links
        buttons = self.soup.find_all(['button', 'a'], class_=re.compile(r'btn|button', re.I))
        
        if len(buttons) >= 5:
            findings.append("✅ Touch-friendly buttons present")
            points += 2
        else:
            recommendations.append("Ensure buttons are at least 44x44px for touch targets")
            
        # 4. Check for mobile-specific features
        tel_links = self.soup.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            findings.append("✅ Click-to-call phone links")
            points += 1
        else:
            recommendations.append("Make phone numbers clickable with tel: links")
            
        # 5. Check for sticky navigation (mobile-friendly pattern)
        sticky_nav = self.soup.find(['nav', 'header'], class_=re.compile(r'sticky|fixed', re.I))
        if sticky_nav:
            findings.append("✅ Sticky/fixed navigation for mobile")
            points += 1
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_crawlability(self) -> CategoryScore:
        """Category 17: Crawlability (10 pts)
        XML sitemaps for listings? Robots.txt proper?
        """
        score = CategoryScore(name="Crawlability")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # 1. Check robots.txt
        if self.robots_txt:
            findings.append("✅ robots.txt exists")
            points += 2
            
            # Check for sitemap declaration
            if 'sitemap' in self.robots_txt.lower():
                findings.append("✅ Sitemap declared in robots.txt")
                points += 1
            else:
                recommendations.append("Add Sitemap: directive to robots.txt")
                
            # Check for sensible disallows
            if 'disallow: /wp-admin' in self.robots_txt.lower() or \
               'disallow: /admin' in self.robots_txt.lower():
                findings.append("✅ Admin areas blocked appropriately")
                points += 1
                
            # Check for query parameter handling
            if 'disallow: /*?' in self.robots_txt.lower() or 'disallow: /*sort' in self.robots_txt.lower():
                findings.append("✅ Dynamic URLs/filters blocked")
                points += 1
            else:
                recommendations.append("Consider blocking filter/sort URLs: Disallow: /*?sort")
                
            details['robots_txt_sample'] = self.robots_txt[:500]
        else:
            findings.append("⚠️ No robots.txt found")
            recommendations.append("Create robots.txt with sitemap reference")
            
        # 2. Check sitemap
        if self.sitemap_urls:
            findings.append(f"✅ Sitemap found with {len(self.sitemap_urls)} URLs")
            points += 3
            
            # Check if listings are in sitemap
            listing_urls_in_sitemap = [u for u in self.sitemap_urls 
                                       if any(p in u.lower() for p in ['/listing', '/business', '/company'])]
            if listing_urls_in_sitemap:
                findings.append(f"✅ {len(listing_urls_in_sitemap)} listing URLs in sitemap")
                points += 1
            else:
                findings.append("⚠️ Listing pages may not be in sitemap")
                recommendations.append("Ensure all listing pages are included in sitemap")
        else:
            findings.append("❌ No sitemap found")
            recommendations.append("Create XML sitemap with all listing and category pages")
            
        # 3. Check for IndexNow or ping capabilities
        # (Can't directly check, but we can recommend)
        recommendations.append("Consider implementing IndexNow for faster indexing")
        
        # 4. Check internal crawlability (orphan pages)
        # This is a simplified check
        if self.soup:
            all_links = self.soup.find_all('a', href=True)
            unique_internal_paths = set()
            for link in all_links:
                href = link['href']
                if href.startswith('/') or self.domain in href:
                    path = urlparse(href).path
                    unique_internal_paths.add(path)
                    
            details['unique_internal_paths'] = len(unique_internal_paths)
            
            if len(unique_internal_paths) >= 30:
                findings.append(f"✅ Good internal link diversity ({len(unique_internal_paths)} unique paths)")
                points += 1
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    # =========================================================================
    # AUTHORITY & TRUST CHECKS (30 points)
    # =========================================================================
    
    def check_backlink_profile(self) -> CategoryScore:
        """Category 18: Backlink Profile (10 pts)
        DR/DA, referring domains (use DataForSEO if available)
        """
        score = CategoryScore(name="Backlink Profile")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # Try DataForSEO if available
        if DATAFORSEO_AVAILABLE and DATAFORSEO_AUTH:
            try:
                # DataForSEO Backlinks Summary
                api_url = "https://api.dataforseo.com/v3/backlinks/summary/live"
                payload = [{"target": self.domain, "internal_list_limit": 10}]
                
                resp = requests.post(
                    api_url,
                    headers={
                        'Authorization': f'Basic {DATAFORSEO_AUTH}',
                        'Content-Type': 'application/json'
                    },
                    json=payload,
                    timeout=30
                )
                
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('tasks') and data['tasks'][0].get('result'):
                        result = data['tasks'][0]['result'][0]
                        
                        rank = result.get('rank', 0)
                        backlinks = result.get('backlinks', 0)
                        referring_domains = result.get('referring_domains', 0)
                        
                        details['dataforseo_rank'] = rank
                        details['backlinks'] = backlinks
                        details['referring_domains'] = referring_domains
                        
                        findings.append(f"📊 Domain Rank: {rank}")
                        findings.append(f"📊 Backlinks: {backlinks:,}")
                        findings.append(f"📊 Referring Domains: {referring_domains:,}")
                        
                        # Score based on metrics
                        if rank >= 60:
                            points += 4
                            findings.append("✅ Strong domain authority")
                        elif rank >= 40:
                            points += 3
                            findings.append("⚠️ Moderate domain authority")
                        elif rank >= 20:
                            points += 2
                            findings.append("⚠️ Building domain authority")
                        else:
                            points += 1
                            recommendations.append("Focus on building quality backlinks")
                            
                        if referring_domains >= 500:
                            points += 3
                        elif referring_domains >= 100:
                            points += 2
                        elif referring_domains >= 20:
                            points += 1
                            
                        # Additional recommendations based on metrics
                        if referring_domains < 100:
                            recommendations.append("Build more referring domains through outreach and content")
                        if rank < 40:
                            recommendations.append("Pursue high-authority backlinks (DR50+)")
                            
            except Exception as e:
                findings.append(f"⚠️ DataForSEO API error: {str(e)[:50]}")
        else:
            findings.append("ℹ️ DataForSEO not configured - using on-site indicators")
            
            # Fall back to on-site indicators
            if self.soup:
                text = self.soup.get_text().lower()
                
                # Check for "as seen on" / press mentions
                press_indicators = ['as seen on', 'featured in', 'press', 'media coverage', 'trusted by']
                if any(p in text for p in press_indicators):
                    findings.append("✅ Press/media mentions present")
                    points += 3
                else:
                    recommendations.append("Pursue PR and press coverage for backlinks")
                    
                # Check for partner/association mentions
                if 'partner' in text or 'association' in text or 'member of' in text:
                    findings.append("✅ Partnership/association mentions")
                    points += 2
                    
            # General recommendations
            recommendations.append("Use Ahrefs, Moz, or DataForSEO for detailed backlink analysis")
            recommendations.append("Build links through digital PR and industry outreach")
            points += 3  # Base points for unknown profile
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_social_proof(self) -> CategoryScore:
        """Category 19: Social Proof (10 pts)
        Social links, review counts, trust badges?
        """
        score = CategoryScore(name="Social Proof")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Add social proof elements: social links, review counts, trust badges"]
            return score
            
        # 1. Check for social media links
        social_patterns = {
            'facebook': r'facebook\.com/',
            'twitter': r'(twitter|x)\.com/',
            'linkedin': r'linkedin\.com/',
            'instagram': r'instagram\.com/',
            'youtube': r'youtube\.com/',
        }
        
        socials_found = []
        for link in self.soup.find_all('a', href=True):
            href = link['href'].lower()
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href) and platform not in socials_found:
                    socials_found.append(platform)
                    
        details['social_profiles'] = socials_found
        
        if len(socials_found) >= 4:
            findings.append(f"✅ Strong social presence: {', '.join(socials_found)}")
            points += 3
        elif len(socials_found) >= 2:
            findings.append(f"⚠️ Some social profiles: {', '.join(socials_found)}")
            points += 2
        else:
            findings.append("❌ Limited social media links")
            recommendations.append("Add links to active social media profiles")
            
        # 2. Check for review counts/mentions
        text = self.soup.get_text().lower()
        
        review_patterns = [
            r'(\d+)\s*reviews?',
            r'(\d+)\s*ratings?',
            r'(\d+)\s*testimonials?',
        ]
        
        review_counts = []
        for pattern in review_patterns:
            matches = re.findall(pattern, text)
            review_counts.extend(matches)
            
        if review_counts:
            findings.append(f"✅ Review/rating counts displayed")
            points += 2
        else:
            recommendations.append("Display review counts prominently (e.g., '500+ reviews')")
            
        # 3. Check for trust badges
        trust_patterns = ['bbb', 'accredited', 'verified', 'certified', 'secure', 
                         'trusted', 'award', 'best of', '5-star', 'five star']
        
        trust_found = sum(1 for p in trust_patterns if p in text)
        details['trust_indicators'] = trust_found
        
        if trust_found >= 3:
            findings.append("✅ Multiple trust signals present")
            points += 3
        elif trust_found >= 1:
            findings.append("⚠️ Some trust signals")
            points += 1
        else:
            findings.append("❌ No trust badges or signals")
            recommendations.append("Add trust badges (BBB, industry certifications)")
            
        # 4. Check for testimonial section
        testimonial_section = self.soup.find(class_=re.compile(r'testimonial|review|client', re.I))
        if testimonial_section:
            findings.append("✅ Testimonial/review section present")
            points += 2
        else:
            recommendations.append("Add a testimonials section with real customer feedback")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_eeat_signals(self) -> CategoryScore:
        """Category 20: E-E-A-T Signals (10 pts)
        About page, contact info, editorial standards?
        """
        score = CategoryScore(name="E-E-A-T Signals")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            score.recommendations = ["Add About page, contact info, team bios, and editorial standards"]
            return score
            
        text = self.soup.get_text().lower()
        
        # Check navigation for key pages
        nav_links = []
        for link in self.soup.find_all('a', href=True):
            nav_links.append({
                'text': link.get_text().lower(),
                'href': link['href'].lower()
            })
            
        # 1. About page
        has_about = any('about' in l['text'] or '/about' in l['href'] for l in nav_links)
        if has_about:
            findings.append("✅ About page linked")
            points += 2
        else:
            findings.append("❌ No visible About page link")
            recommendations.append("Add About page with company history and mission")
            
        # 2. Contact page/info
        has_contact = any('contact' in l['text'] or '/contact' in l['href'] for l in nav_links)
        has_phone = bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text))
        has_address = bool(re.search(r'\d+\s+\w+\s+(street|st|avenue|ave|road|rd)', text))
        
        contact_score = sum([has_contact, has_phone, has_address])
        details['contact_elements'] = {
            'contact_page': has_contact,
            'phone': has_phone,
            'address': has_address
        }
        
        if contact_score >= 2:
            findings.append("✅ Contact information readily available")
            points += 2
        elif contact_score >= 1:
            findings.append("⚠️ Some contact info present")
            points += 1
        else:
            findings.append("❌ Limited contact information")
            recommendations.append("Add clear contact page with phone, email, and address")
            
        # 3. Privacy policy / Terms
        has_privacy = any('privacy' in l['text'] or '/privacy' in l['href'] for l in nav_links)
        has_terms = any('terms' in l['text'] or '/terms' in l['href'] for l in nav_links)
        
        if has_privacy and has_terms:
            findings.append("✅ Privacy Policy and Terms present")
            points += 2
        elif has_privacy or has_terms:
            findings.append("⚠️ Partial legal pages")
            points += 1
            recommendations.append("Add both Privacy Policy and Terms of Service")
        else:
            recommendations.append("Add Privacy Policy and Terms of Service pages")
            
        # 4. Editorial standards / How we rate
        editorial_patterns = ['editorial', 'how we rate', 'methodology', 'our process', 'how we select']
        has_editorial = any(p in text for p in editorial_patterns)
        
        if has_editorial:
            findings.append("✅ Editorial standards/methodology explained")
            points += 2
        else:
            recommendations.append("Add 'How We Rate' or 'Our Methodology' page")
            
        # 5. Author/Team information
        team_patterns = ['our team', 'meet the team', 'about us', 'authors', 'editors']
        has_team = any(p in text for p in team_patterns)
        
        if has_team:
            findings.append("✅ Team/author information present")
            points += 2
        else:
            recommendations.append("Add team bios with credentials")
            
        # 6. HTTPS
        if self.url.startswith('https'):
            findings.append("✅ HTTPS enabled")
            points += 1
        else:
            findings.append("❌ Not using HTTPS")
            recommendations.append("Enable HTTPS immediately")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    # =========================================================================
    # MAIN AUDIT RUNNER
    # =========================================================================
    
    def run_full_audit(self) -> DirectoryAuditResult:
        """Run complete directory SEO audit"""
        print(f"\n{'='*60}")
        print(f"DIRECTORY SEO AUDIT: {self.url}")
        print(f"{'='*60}\n")
        
        # Initialize result
        result = DirectoryAuditResult(url=self.url)
        
        # Fetch main page
        print("[1/7] Fetching main page...")
        html, soup = self.fetch_page()
        if not soup:
            print("ERROR: Could not fetch main page")
            return result
            
        # Extract business/directory name
        title = soup.find('title')
        if title:
            result.directory_name = title.get_text().split('|')[0].split('-')[0].strip()
            
        # Fetch robots.txt and sitemap
        print("[2/7] Fetching robots.txt and sitemap...")
        self.fetch_robots_txt()
        self.fetch_sitemap()
        
        # Discover and classify pages
        print("[3/7] Discovering pages...")
        self.discover_pages()
        
        # Run all checks
        print("\n[4/7] Running Structure & Architecture checks...")
        structure_checks = [
            self.check_listing_completeness(),
            self.check_category_taxonomy(),
            self.check_location_structure(),
            self.check_internal_linking(),
            self.check_url_structure(),
        ]
        result.structure_categories = structure_checks
        result.structure_score = sum(c.score for c in structure_checks)
        
        print("[4/7] Running On-Page SEO checks...")
        onpage_checks = [
            self.check_title_optimization(),
            self.check_meta_descriptions(),
            self.check_heading_structure(),
            self.check_schema_markup(),
            self.check_pagination_canonicals(),
        ]
        result.onpage_categories = onpage_checks
        result.onpage_score = sum(c.score for c in onpage_checks)
        
        print("[5/7] Running Content Quality checks...")
        content_checks = [
            self.check_listing_descriptions(),
            self.check_user_generated_content(),
            self.check_editorial_content(),
            self.check_content_freshness(),
        ]
        result.content_categories = content_checks
        result.content_score = sum(c.score for c in content_checks)
        
        print("[6/7] Running Technical SEO checks...")
        technical_checks = [
            self.check_page_speed(),
            self.check_mobile_usability(),
            self.check_crawlability(),
        ]
        result.technical_categories = technical_checks
        result.technical_score = sum(c.score for c in technical_checks)
        
        print("[6/7] Running Authority & Trust checks...")
        authority_checks = [
            self.check_backlink_profile(),
            self.check_social_proof(),
            self.check_eeat_signals(),
        ]
        result.authority_categories = authority_checks
        result.authority_score = sum(c.score for c in authority_checks)
        
        # Run AI Visibility checks using the enhanced analyzer
        print("[7/7] Running AI Visibility checks...")
        result.ai_categories = self._run_ai_visibility_checks()
        result.ai_visibility_score = sum(c.score for c in result.ai_categories)
        
        # Calculate total scores
        result.directory_health_score = (
            result.structure_score + 
            result.onpage_score + 
            result.content_score + 
            result.technical_score + 
            result.authority_score
        )
        result.total_score = result.directory_health_score + result.ai_visibility_score
        
        # Assign grade based on total score (/300)
        pct = result.total_score / 300 * 100
        if pct >= 90:
            result.grade = 'A+'
        elif pct >= 80:
            result.grade = 'A'
        elif pct >= 70:
            result.grade = 'B'
        elif pct >= 60:
            result.grade = 'C'
        elif pct >= 50:
            result.grade = 'D'
        else:
            result.grade = 'F'
            
        # Generate quick wins
        all_categories = (
            result.structure_categories + 
            result.onpage_categories + 
            result.content_categories + 
            result.technical_categories + 
            result.authority_categories +
            result.ai_categories
        )
        
        # Quick wins: Easy recommendations from high-scoring categories
        for cat in all_categories:
            if cat.score >= 7 and cat.recommendations:
                result.quick_wins.append(f"{cat.name}: {cat.recommendations[0]}")
                
        # Priority fixes: From low-scoring categories
        for cat in all_categories:
            if cat.score < 5:
                result.priority_fixes.append(f"⚠️ {cat.name} ({cat.score}/10): {cat.recommendations[0] if cat.recommendations else 'Needs improvement'}")
                
        # Technical data
        result.technical_data = {
            'pages_discovered': len(self.listing_pages) + len(self.category_pages) + len(self.location_pages),
            'listing_pages': len(self.listing_pages),
            'category_pages': len(self.category_pages),
            'location_pages': len(self.location_pages),
            'sitemap_urls': len(self.sitemap_urls),
            'schemas_found': len(self.all_schemas),
        }
        
        # Print summary
        self._print_summary(result)
        
        return result
    
    def _run_ai_visibility_checks(self) -> List[CategoryScore]:
        """Run AI visibility checks using the enhanced analyzer"""
        ai_categories = []
        
        if AI_ANALYZER_AVAILABLE:
            try:
                # Create an enhanced analyzer instance for AI checks
                ai_analyzer = EnhancedWebsiteAnalyzer(self.url)
                
                # Share our already-fetched data to avoid duplicate requests
                ai_analyzer.html = self.html
                ai_analyzer.soup = self.soup
                ai_analyzer.robots_txt = self.robots_txt
                ai_analyzer.schema_data = self.all_schemas
                
                # Run all 10 AI visibility checks
                ai_categories = [
                    ai_analyzer.check_crawler_access(),
                    ai_analyzer.check_structured_data(),
                    ai_analyzer.check_content_structure(),
                    ai_analyzer.check_eeat_signals(),
                    ai_analyzer.check_brand_mentions(),
                    ai_analyzer.check_content_freshness(),
                    ai_analyzer.check_question_content(),
                    ai_analyzer.check_citations(),
                    ai_analyzer.check_technical_performance(),
                    ai_analyzer.check_ai_platform_presence(),
                ]
                print(f"  AI Visibility Score: {sum(c.score for c in ai_categories)}/100")
                
            except Exception as e:
                print(f"  [!] Enhanced analyzer error: {e}")
                # Fall back to basic AI checks
                ai_categories = self._basic_ai_visibility_checks()
        else:
            # Fall back to basic analyzer if enhanced not available
            try:
                from analyzer import WebsiteAnalyzer
                ai_analyzer = WebsiteAnalyzer(self.url)
                ai_analyzer.html = self.html
                ai_analyzer.soup = self.soup
                ai_analyzer.robots_txt = self.robots_txt
                
                ai_categories = [
                    ai_analyzer.check_crawler_access(),
                    ai_analyzer.check_structured_data(),
                    ai_analyzer.check_content_structure(),
                    ai_analyzer.check_eeat_signals(),
                    ai_analyzer.check_brand_mentions(),
                    ai_analyzer.check_content_freshness(),
                    ai_analyzer.check_question_content(),
                    ai_analyzer.check_citations(),
                    ai_analyzer.check_technical_performance(),
                    ai_analyzer.check_ai_platform_presence(),
                ]
                print(f"  AI Visibility Score: {sum(c.score for c in ai_categories)}/100")
            except Exception as e:
                print(f"  [!] AI visibility checks failed: {e}")
                ai_categories = self._basic_ai_visibility_checks()
            
        return ai_categories
    
    def _basic_ai_visibility_checks(self) -> List[CategoryScore]:
        """Basic AI visibility checks fallback"""
        categories = []
        
        # 1. AI Crawler Access
        score = CategoryScore(name="AI Crawler Access")
        if self.robots_txt:
            blocked_bots = ['gptbot', 'claudebot', 'anthropic', 'perplexity']
            robots_lower = self.robots_txt.lower()
            is_blocked = any(bot in robots_lower and 'disallow: /' in robots_lower 
                           for bot in blocked_bots)
            if not is_blocked:
                score.score = 7
                score.findings = ["✅ AI bots not explicitly blocked in robots.txt"]
            else:
                score.score = 3
                score.findings = ["⚠️ Some AI bots may be blocked"]
                score.recommendations = ["Review robots.txt for AI bot access"]
        else:
            score.score = 5
            score.findings = ["ℹ️ No robots.txt (AI bots allowed by default)"]
        categories.append(score)
        
        # 2. Structured Data Quality
        score = CategoryScore(name="Structured Data Quality")
        if self.all_schemas:
            schema_count = len(self.all_schemas)
            score.score = min(schema_count * 2 + 2, 10)
            score.findings = [f"✅ {schema_count} schema object(s) found"]
        else:
            score.score = 0
            score.findings = ["❌ No structured data found"]
            score.recommendations = ["Add JSON-LD structured data"]
        categories.append(score)
        
        # 3-10: Basic checks based on page content
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Content Structure
            h1_count = len(self.soup.find_all('h1'))
            h2_count = len(self.soup.find_all('h2'))
            score = CategoryScore(name="Content Structure")
            score.score = min(2 + h2_count, 10) if h1_count == 1 else min(h2_count, 8)
            score.findings = [f"H1: {h1_count}, H2: {h2_count}"]
            categories.append(score)
            
            # E-E-A-T Signals
            score = CategoryScore(name="E-E-A-T Signals")
            eeat_signals = sum(1 for p in ['about', 'contact', 'team', 'author', 'experience'] if p in text)
            score.score = min(eeat_signals * 2, 10)
            score.findings = [f"{eeat_signals} E-E-A-T signals detected"]
            categories.append(score)
            
            # Brand Presence
            score = CategoryScore(name="Brand Presence")
            social_count = sum(1 for p in ['facebook', 'twitter', 'linkedin', 'youtube', 'instagram'] 
                              if p in str(self.soup).lower())
            score.score = min(social_count * 2, 10)
            score.findings = [f"{social_count} social platform links"]
            categories.append(score)
            
            # Content Freshness
            score = CategoryScore(name="Content Freshness")
            has_dates = bool(re.search(r'202[4-6]', text))
            score.score = 7 if has_dates else 3
            score.findings = ["✅ Recent dates found" if has_dates else "⚠️ No recent dates"]
            categories.append(score)
            
            # Question-Based Content
            score = CategoryScore(name="Question-Based Content")
            questions = len(re.findall(r'\?', text))
            has_faq = 'faq' in text or 'frequently asked' in text
            score.score = min(3 + (questions // 5) + (3 if has_faq else 0), 10)
            score.findings = [f"{questions} questions found" + (", FAQ section present" if has_faq else "")]
            categories.append(score)
            
            # Citations & Sources
            score = CategoryScore(name="Citations & Sources")
            external_links = len([a for a in self.soup.find_all('a', href=True) 
                                 if a['href'].startswith('http') and self.domain not in a['href']])
            score.score = min(external_links, 10)
            score.findings = [f"{external_links} external links/citations"]
            categories.append(score)
            
            # Technical Performance
            score = CategoryScore(name="Technical Performance")
            has_viewport = bool(self.soup.find('meta', {'name': 'viewport'}))
            is_https = self.url.startswith('https')
            score.score = 5 + (2 if has_viewport else 0) + (3 if is_https else 0)
            score.findings = [f"HTTPS: {'✅' if is_https else '❌'}, Viewport: {'✅' if has_viewport else '❌'}"]
            categories.append(score)
            
            # AI Platform Presence
            score = CategoryScore(name="AI Platform Presence")
            youtube = 'youtube' in str(self.soup).lower()
            llms_txt = False  # Would need to check
            score.score = 5 + (3 if youtube else 0) + (2 if llms_txt else 0)
            score.findings = [f"YouTube: {'✅' if youtube else '❌'}"]
            score.recommendations = ["Create llms.txt for AI discoverability"]
            categories.append(score)
        else:
            # Fallback minimal scores
            for name in ["Content Structure", "E-E-A-T Signals", "Brand Presence", 
                        "Content Freshness", "Question-Based Content", "Citations & Sources",
                        "Technical Performance", "AI Platform Presence"]:
                score = CategoryScore(name=name)
                score.score = 3
                score.findings = ["ℹ️ Could not fully analyze"]
                categories.append(score)
            
        return categories
        
    def _print_summary(self, result: DirectoryAuditResult):
        """Print audit summary to console"""
        print(f"\n{'='*60}")
        print(f"TOTAL SCORE: {result.total_score}/300 ({result.grade})")
        print(f"{'='*60}")
        
        print(f"\n📊 Directory SEO: {result.directory_health_score}/200")
        print(f"  Structure & Architecture: {result.structure_score}/50")
        print(f"  On-Page SEO:              {result.onpage_score}/50")
        print(f"  Content Quality:          {result.content_score}/40")
        print(f"  Technical SEO:            {result.technical_score}/30")
        print(f"  Authority & Trust:        {result.authority_score}/30")
        
        print(f"\n🤖 AI Visibility: {result.ai_visibility_score}/100")
        if result.ai_categories:
            for cat in result.ai_categories:
                bar = '█' * cat.score + '░' * (10 - cat.score)
                print(f"  {cat.name}: {bar} {cat.score}/10")
        
        if result.priority_fixes:
            print(f"\n🚨 Priority Fixes ({len(result.priority_fixes)}):")
            for fix in result.priority_fixes[:5]:
                print(f"  {fix}")
                
        if result.quick_wins:
            print(f"\n✅ Quick Wins ({len(result.quick_wins)}):")
            for win in result.quick_wins[:5]:
                print(f"  {win}")
                
        print(f"\n📈 Pages Analyzed:")
        print(f"  Listings:   {result.technical_data.get('listing_pages', 0)}")
        print(f"  Categories: {result.technical_data.get('category_pages', 0)}")
        print(f"  Locations:  {result.technical_data.get('location_pages', 0)}")
        print(f"  Sitemap URLs: {result.technical_data.get('sitemap_urls', 0)}")
        print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 directory_analyzer.py <url>")
        print("Example: python3 directory_analyzer.py https://yelp.com")
        sys.exit(1)
        
    url = sys.argv[1]
    
    # Run audit
    analyzer = DirectorySEOAnalyzer(url)
    result = analyzer.run_full_audit()
    
    # Generate PDF if requested
    if '--pdf' in sys.argv or '-p' in sys.argv:
        try:
            from directory_pdf_generator import generate_directory_pdf
            output_path = f"directory_audit_{result.directory_name or 'report'}.pdf".replace(' ', '_')
            generate_directory_pdf(result, output_path)
            print(f"\n📄 PDF saved to: {output_path}")
        except ImportError:
            print("\n⚠️ PDF generator not found. Run without --pdf flag.")
            
    # Save JSON results
    if '--json' in sys.argv or '-j' in sys.argv:
        import dataclasses
        output_path = f"directory_audit_{result.directory_name or 'report'}.json".replace(' ', '_')
        
        def serialize(obj):
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)
            return str(obj)
            
        with open(output_path, 'w') as f:
            json.dump(dataclasses.asdict(result), f, indent=2, default=serialize)
        print(f"\n📋 JSON saved to: {output_path}")


if __name__ == "__main__":
    main()
