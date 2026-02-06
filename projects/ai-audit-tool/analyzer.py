#!/usr/bin/env python3
"""
AI & Local Visibility Audit Analyzer
Automatically analyzes a website against 20 SOP categories
"""

import requests
import json
import re
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import time

# DataForSEO integration
try:
    from dataforseo_client import DataForSEOClient
    DATAFORSEO_AVAILABLE = True
except ImportError:
    DATAFORSEO_AVAILABLE = False

@dataclass
class CategoryScore:
    name: str
    score: int = 0  # 0-10
    max_score: int = 10
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
@dataclass
class AuditResult:
    url: str
    business_name: Optional[str] = None
    ai_visibility_score: int = 0
    local_seo_score: int = 0
    total_score: int = 0
    ai_categories: List[CategoryScore] = field(default_factory=list)
    local_categories: List[CategoryScore] = field(default_factory=list)
    quick_wins: List[str] = field(default_factory=list)
    priority_fixes: List[str] = field(default_factory=list)
    
class WebsiteAnalyzer:
    def __init__(self, url: str):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.parsed_url = urlparse(self.url)
        self.domain = self.parsed_url.netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; KuriosAuditBot/1.0; +https://kuriosbrand.com)'
        })
        self.html = None
        self.soup = None
        self.robots_txt = None
        
    def fetch_page(self) -> bool:
        """Fetch the main page"""
        try:
            resp = self.session.get(self.url, timeout=15)
            resp.raise_for_status()
            self.html = resp.text
            self.soup = BeautifulSoup(self.html, 'html.parser')
            return True
        except Exception as e:
            print(f"Error fetching {self.url}: {e}")
            return False
            
    def fetch_robots_txt(self) -> str:
        """Fetch robots.txt"""
        try:
            robots_url = f"{self.parsed_url.scheme}://{self.domain}/robots.txt"
            resp = self.session.get(robots_url, timeout=10)
            if resp.status_code == 200:
                self.robots_txt = resp.text
                return self.robots_txt
        except:
            pass
        return ""
        
    def fetch_llms_txt(self) -> str:
        """Check for llms.txt file"""
        try:
            llms_url = f"{self.parsed_url.scheme}://{self.domain}/llms.txt"
            resp = self.session.get(llms_url, timeout=10)
            if resp.status_code == 200:
                return resp.text
        except:
            pass
        return ""

    # ============ AI VISIBILITY CHECKS ============
    
    def check_crawler_access(self) -> CategoryScore:
        """Category 1: Crawler Access (GPTBot, ClaudeBot, llms.txt, SSR)"""
        score = CategoryScore(name="Crawler Access")
        findings = []
        recommendations = []
        points = 0
        
        robots = self.fetch_robots_txt()
        llms = self.fetch_llms_txt()
        
        # Check GPTBot
        if robots:
            if 'GPTBot' in robots:
                if 'Disallow' in robots.split('GPTBot')[1].split('\n')[0]:
                    findings.append("❌ GPTBot is BLOCKED in robots.txt")
                    recommendations.append("Allow GPTBot in robots.txt to be visible in ChatGPT")
                else:
                    findings.append("✅ GPTBot is allowed")
                    points += 2
            else:
                findings.append("⚠️ GPTBot not explicitly mentioned (defaults to allowed)")
                points += 1
                
            # Check ClaudeBot/Anthropic
            if 'Claude' in robots or 'Anthropic' in robots or 'anthropic' in robots:
                if 'Disallow' in robots.lower():
                    findings.append("❌ Claude/Anthropic bot may be blocked")
                    recommendations.append("Allow ClaudeBot and anthropic-ai in robots.txt")
                else:
                    findings.append("✅ Claude/Anthropic bot allowed")
                    points += 2
            else:
                findings.append("⚠️ Claude/Anthropic not mentioned (defaults to allowed)")
                points += 1
        else:
            findings.append("⚠️ No robots.txt found - all bots allowed by default")
            points += 2
            
        # Check llms.txt
        if llms:
            findings.append("✅ llms.txt file found - excellent for AI visibility")
            points += 3
        else:
            findings.append("❌ No llms.txt file")
            recommendations.append("Create llms.txt to help AI systems understand your site")
            
        # Check for SSR indicators
        if self.soup:
            # Check if content is present without JS
            main_content = self.soup.find('main') or self.soup.find('article') or self.soup.find('div', class_=re.compile(r'content|main', re.I))
            if main_content and len(main_content.get_text(strip=True)) > 100:
                findings.append("✅ Content appears server-rendered (good for crawlers)")
                points += 2
            else:
                findings.append("⚠️ Limited server-rendered content detected")
                recommendations.append("Ensure critical content is server-side rendered for AI crawlers")
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_structured_data(self) -> CategoryScore:
        """Category 2: Structured Data (Schema.org)"""
        score = CategoryScore(name="Structured Data")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Find JSON-LD scripts
        json_ld_scripts = self.soup.find_all('script', type='application/ld+json')
        schemas_found = []
        
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    for item in data:
                        if '@type' in item:
                            schemas_found.append(item['@type'])
                elif '@type' in data:
                    schemas_found.append(data['@type'])
            except:
                pass
                
        # Check for key schemas
        desired_schemas = {
            'LocalBusiness': 3,
            'LegalService': 3,
            'Attorney': 3,
            'Organization': 2,
            'FAQPage': 2,
            'WebSite': 1,
            'BreadcrumbList': 1,
            'Article': 1,
        }
        
        for schema, pts in desired_schemas.items():
            if any(schema.lower() in s.lower() for s in schemas_found):
                findings.append(f"✅ {schema} schema found")
                points += pts
            else:
                recommendations.append(f"Add {schema} schema markup")
                
        if not schemas_found:
            findings.append("❌ No structured data (JSON-LD) found")
            recommendations.append("Add JSON-LD structured data for better AI understanding")
        else:
            findings.insert(0, f"Found {len(schemas_found)} schema type(s): {', '.join(set(schemas_found))}")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations[:3]  # Top 3 recommendations
        return score
        
    def check_content_structure(self) -> CategoryScore:
        """Category 3: Content Structure (headings, paragraphs, lists)"""
        score = CategoryScore(name="Content Structure")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check heading hierarchy
        h1s = self.soup.find_all('h1')
        h2s = self.soup.find_all('h2')
        h3s = self.soup.find_all('h3')
        
        if len(h1s) == 1:
            findings.append("✅ Single H1 tag (correct)")
            points += 2
        elif len(h1s) == 0:
            findings.append("❌ No H1 tag found")
            recommendations.append("Add a single H1 tag with your main keyword")
        else:
            findings.append(f"⚠️ Multiple H1 tags ({len(h1s)}) - should have only one")
            recommendations.append("Use only one H1 tag per page")
            
        if h2s:
            findings.append(f"✅ {len(h2s)} H2 tags for content sections")
            points += 2
        else:
            findings.append("❌ No H2 tags found")
            recommendations.append("Add H2 tags to structure your content")
            
        if h3s:
            findings.append(f"✅ {len(h3s)} H3 tags for subsections")
            points += 1
            
        # Check for lists
        lists = self.soup.find_all(['ul', 'ol'])
        if lists:
            findings.append(f"✅ {len(lists)} lists found (good for AI parsing)")
            points += 2
        else:
            recommendations.append("Add bullet/numbered lists for better AI comprehension")
            
        # Check for tables
        tables = self.soup.find_all('table')
        if tables:
            findings.append(f"✅ {len(tables)} tables found")
            points += 1
            
        # Check paragraph structure
        paragraphs = self.soup.find_all('p')
        if paragraphs:
            avg_length = sum(len(p.get_text()) for p in paragraphs) / len(paragraphs)
            if avg_length < 300:
                findings.append("✅ Short paragraphs (easy to read/parse)")
                points += 2
            else:
                findings.append("⚠️ Long paragraphs - consider breaking up")
                recommendations.append("Break long paragraphs into shorter chunks")
                points += 1
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_eeat_signals(self) -> CategoryScore:
        """Category 4: E-E-A-T Signals (expertise, experience, authority, trust)"""
        score = CategoryScore(name="E-E-A-T Signals")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text().lower()
        
        # Check for author information
        author_patterns = ['author', 'written by', 'by attorney', 'attorney profile']
        if any(p in text for p in author_patterns):
            findings.append("✅ Author attribution found")
            points += 2
        else:
            recommendations.append("Add author bios with credentials")
            
        # Check for credentials
        credential_patterns = ['esq', 'j.d.', 'attorney', 'lawyer', 'years experience', 'licensed']
        creds_found = sum(1 for p in credential_patterns if p in text)
        if creds_found >= 2:
            findings.append("✅ Professional credentials mentioned")
            points += 2
        else:
            recommendations.append("Highlight attorney credentials and experience")
            
        # Check for case results / testimonials
        result_patterns = ['case result', 'verdict', 'settlement', 'recovered', 'won', 'testimonial', 'review']
        if any(p in text for p in result_patterns):
            findings.append("✅ Case results or testimonials present")
            points += 2
        else:
            recommendations.append("Add case results and client testimonials")
            
        # Check for trust signals
        trust_patterns = ['bbb', 'avvo', 'super lawyers', 'martindale', 'bar association', 'award']
        if any(p in text for p in trust_patterns):
            findings.append("✅ Trust badges/awards mentioned")
            points += 2
        else:
            recommendations.append("Add trust badges (Avvo, BBB, Bar Association)")
            
        # Check for contact info
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        if re.search(phone_pattern, self.html or ''):
            findings.append("✅ Phone number visible")
            points += 1
            
        # Check for physical address
        address_patterns = ['address', 'located at', 'office']
        if any(p in text for p in address_patterns):
            findings.append("✅ Physical address present")
            points += 1
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_brand_mentions(self) -> CategoryScore:
        """Category 5: Brand Mentions (external presence)"""
        score = CategoryScore(name="Brand Mentions")
        findings = []
        recommendations = []
        points = 0
        
        # This would ideally query external sources
        # For now, check for social proof on the site itself
        
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Check for social media links
            social_platforms = ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube']
            socials_found = []
            for link in self.soup.find_all('a', href=True):
                for platform in social_platforms:
                    if platform in link['href'].lower():
                        socials_found.append(platform)
                        
            if socials_found:
                findings.append(f"✅ Social media links: {', '.join(set(socials_found))}")
                points += len(set(socials_found))
            else:
                recommendations.append("Add social media profile links")
                
            # Check for press/media mentions
            press_patterns = ['featured in', 'as seen on', 'media', 'press', 'news']
            if any(p in text for p in press_patterns):
                findings.append("✅ Press/media mentions found")
                points += 2
            else:
                recommendations.append("Pursue PR opportunities for brand mentions")
                
            # Check for review platform mentions
            review_platforms = ['google reviews', 'yelp', 'avvo', 'lawyers.com']
            if any(p in text for p in review_platforms):
                findings.append("✅ Review platform presence indicated")
                points += 2
                
        findings.append("⚠️ Full brand mention analysis requires external API calls")
        recommendations.append("Build Reddit presence in relevant subreddits")
        recommendations.append("Pursue Wikipedia mention if notable enough")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations[:3]
        return score
        
    def check_content_freshness(self) -> CategoryScore:
        """Category 6: Content Freshness (dates, updates)"""
        score = CategoryScore(name="Content Freshness")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check for datePublished/dateModified in schema
        json_ld = self.soup.find_all('script', type='application/ld+json')
        has_dates = False
        for script in json_ld:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    if 'datePublished' in data or 'dateModified' in data:
                        has_dates = True
                        findings.append("✅ datePublished/dateModified in schema")
                        points += 3
                        break
            except:
                pass
                
        if not has_dates:
            findings.append("❌ No date metadata in structured data")
            recommendations.append("Add datePublished and dateModified to schema")
            
        # Check for visible dates
        date_patterns = [
            r'\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'updated:?\s*\d',
            r'published:?\s*\d'
        ]
        
        text = self.soup.get_text()
        dates_found = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.I)
            dates_found.extend(matches)
            
        if dates_found:
            findings.append(f"✅ {len(dates_found)} date references found on page")
            points += 2
        else:
            findings.append("⚠️ No visible dates on page")
            recommendations.append("Display publication and update dates on content")
            
        # Check for blog/news section
        blog_patterns = ['blog', 'news', 'articles', 'resources', 'insights']
        nav_text = ''
        for nav in self.soup.find_all(['nav', 'header']):
            nav_text += nav.get_text().lower()
            
        if any(p in nav_text for p in blog_patterns):
            findings.append("✅ Blog/news section appears present")
            points += 2
        else:
            recommendations.append("Add a blog for fresh content")
            
        # Check meta tags for dates
        meta_date = self.soup.find('meta', {'property': 'article:published_time'})
        if meta_date:
            findings.append("✅ Open Graph publish date meta tag")
            points += 2
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_question_content(self) -> CategoryScore:
        """Category 7: Question-Based Content (FAQs, Q&A)"""
        score = CategoryScore(name="Question-Based Content")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text()
        
        # Check for FAQ sections
        faq_patterns = ['faq', 'frequently asked', 'common questions', 'q&a', 'questions and answers']
        if any(p in text.lower() for p in faq_patterns):
            findings.append("✅ FAQ section found")
            points += 3
        else:
            recommendations.append("Add an FAQ section with common questions")
            
        # Check for FAQ schema
        json_ld = self.soup.find_all('script', type='application/ld+json')
        has_faq_schema = False
        for script in json_ld:
            try:
                data = json.loads(script.string)
                if 'FAQPage' in str(data):
                    has_faq_schema = True
                    break
            except:
                pass
                
        if has_faq_schema:
            findings.append("✅ FAQPage schema markup found")
            points += 3
        else:
            recommendations.append("Add FAQPage schema for rich results")
            
        # Count question marks (questions in content)
        questions = re.findall(r'[^.!?]*\?', text)
        if len(questions) > 5:
            findings.append(f"✅ {len(questions)} questions found in content")
            points += 2
        elif len(questions) > 0:
            findings.append(f"⚠️ Only {len(questions)} questions in content")
            points += 1
        else:
            findings.append("❌ No questions found in content")
            recommendations.append("Add question-format headings that match user queries")
            
        # Check for HowTo content
        howto_patterns = ['how to', 'step by step', 'guide', 'process']
        if any(p in text.lower() for p in howto_patterns):
            findings.append("✅ How-to/guide content present")
            points += 2
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_citations(self) -> CategoryScore:
        """Category 8: Citations & Sources"""
        score = CategoryScore(name="Citations & Sources")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text().lower()
        
        # Check for external links
        external_links = []
        for link in self.soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http') and self.domain not in href:
                external_links.append(href)
                
        if len(external_links) > 5:
            findings.append(f"✅ {len(external_links)} external citations/links")
            points += 3
        elif external_links:
            findings.append(f"⚠️ Only {len(external_links)} external links")
            points += 1
        else:
            findings.append("❌ No external citations")
            recommendations.append("Cite authoritative sources (gov sites, studies)")
            
        # Check for statistics
        stat_patterns = [r'\d+%', r'\d+ percent', 'according to', 'study shows', 'research', 'statistics']
        stats_found = sum(1 for p in stat_patterns if re.search(p, text))
        if stats_found >= 3:
            findings.append("✅ Statistics and data citations present")
            points += 3
        elif stats_found > 0:
            findings.append("⚠️ Some statistics found")
            points += 1
        else:
            recommendations.append("Add statistics with source attribution")
            
        # Check for authoritative domain links
        auth_domains = ['.gov', '.edu', 'nhtsa', 'cdc', 'who.int', 'nih.gov']
        auth_found = [l for l in external_links if any(d in l.lower() for d in auth_domains)]
        if auth_found:
            findings.append(f"✅ {len(auth_found)} authoritative source links (.gov, .edu)")
            points += 3
        else:
            recommendations.append("Link to government and educational sources")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_technical_performance(self) -> CategoryScore:
        """Category 9: Technical Performance"""
        score = CategoryScore(name="Technical Performance")
        findings = []
        recommendations = []
        points = 0
        
        # Check HTTPS
        if self.url.startswith('https'):
            findings.append("✅ HTTPS enabled")
            points += 2
        else:
            findings.append("❌ Not using HTTPS")
            recommendations.append("Enable HTTPS immediately")
            
        if not self.soup:
            score.findings = findings + ["❌ Could not fully analyze"]
            return score
            
        # Check mobile viewport
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if viewport:
            findings.append("✅ Mobile viewport configured")
            points += 2
        else:
            findings.append("❌ No mobile viewport meta tag")
            recommendations.append("Add mobile viewport meta tag")
            
        # Check for render-blocking resources
        scripts_in_head = len(self.soup.head.find_all('script', src=True)) if self.soup.head else 0
        if scripts_in_head > 5:
            findings.append(f"⚠️ {scripts_in_head} scripts in head (may slow load)")
            recommendations.append("Defer non-critical JavaScript")
        else:
            findings.append("✅ Minimal render-blocking scripts")
            points += 2
            
        # Check for image optimization indicators
        imgs = self.soup.find_all('img')
        lazy_loaded = sum(1 for img in imgs if img.get('loading') == 'lazy' or 'lazy' in str(img.get('class', '')))
        if imgs:
            if lazy_loaded > len(imgs) / 2:
                findings.append("✅ Images appear lazy-loaded")
                points += 2
            else:
                recommendations.append("Implement lazy loading for images")
                
        # Check page size (rough estimate)
        if self.html:
            size_kb = len(self.html) / 1024
            if size_kb < 100:
                findings.append(f"✅ Page HTML size: {size_kb:.0f}KB (light)")
                points += 2
            elif size_kb < 500:
                findings.append(f"⚠️ Page HTML size: {size_kb:.0f}KB (moderate)")
                points += 1
            else:
                findings.append(f"❌ Page HTML size: {size_kb:.0f}KB (heavy)")
                recommendations.append("Reduce page size for faster load times")
                
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_ai_platform_presence(self) -> CategoryScore:
        """Category 10: AI Platform Presence"""
        score = CategoryScore(name="AI Platform Presence")
        findings = []
        recommendations = []
        points = 0
        
        if self.soup:
            text = self.soup.get_text().lower()
            html = str(self.soup).lower()
            
            # Check for YouTube embeds/links
            youtube_found = False
            for link in self.soup.find_all('a', href=True):
                if 'youtube.com' in link['href'] or 'youtu.be' in link['href']:
                    youtube_found = True
                    break
            for iframe in self.soup.find_all('iframe'):
                if 'youtube' in str(iframe.get('src', '')):
                    youtube_found = True
                    break
                    
            if youtube_found:
                findings.append("✅ YouTube content embedded/linked")
                points += 3
            else:
                recommendations.append("Create YouTube videos and embed on site")
                
            # Check for podcast mentions
            if 'podcast' in text:
                findings.append("✅ Podcast presence mentioned")
                points += 2
                
            # Check for Wikipedia/edu links (authority signals for AI)
            for link in self.soup.find_all('a', href=True):
                href = link['href']
                if '.edu' in href or 'wikipedia.org' in href:
                    findings.append("✅ Links to authoritative sources (.edu/Wikipedia)")
                    points += 2
                    break
                    
            # Check for Reddit mentions
            if 'reddit' in html:
                findings.append("✅ Reddit presence/link found")
                points += 2
                
            # Check for llms.txt (we already have this in crawler check but mention if found)
            if hasattr(self, 'llms_txt') and self.llms_txt:
                findings.append("✅ llms.txt present - excellent for AI discoverability")
                points += 3
                
        if points == 0:
            findings.append("⚠️ Limited AI platform presence detected")
            
        recommendations.append("Create content on platforms AI trains on (YouTube, Reddit)")
        recommendations.append("Add llms.txt file to help AI understand your site")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score

    # ============ LOCAL SEO CHECKS ============
    
    def check_gbp_basics(self) -> CategoryScore:
        """Category 1: Google Business Profile Basics"""
        score = CategoryScore(name="GBP Basics")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check for Google Maps embed
        maps_embed = False
        for iframe in self.soup.find_all('iframe'):
            src = iframe.get('src', '')
            if 'google.com/maps' in src or 'maps.google.com' in src:
                maps_embed = True
                break
                
        if maps_embed:
            findings.append("✅ Google Maps embed found")
            points += 2
        else:
            recommendations.append("Embed Google Maps on contact/location page")
            
        # Check LocalBusiness schema
        json_ld = self.soup.find_all('script', type='application/ld+json')
        local_schema = False
        for script in json_ld:
            try:
                data = json.loads(script.string)
                if 'LocalBusiness' in str(data) or 'LegalService' in str(data) or 'Attorney' in str(data):
                    local_schema = True
                    break
            except:
                pass
                
        if local_schema:
            findings.append("✅ LocalBusiness/LegalService schema found")
            points += 3
        else:
            recommendations.append("Add LocalBusiness schema with full NAP")
            
        # Check for phone number
        text = self.html or ''
        phone = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        if phone:
            findings.append(f"✅ Phone number found: {phone.group()}")
            points += 2
        else:
            findings.append("❌ No phone number detected")
            recommendations.append("Add clickable phone number prominently")
            
        # Check for address
        address_patterns = [
            r'\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln|way|court|ct)',
            r'suite\s+\d+',
        ]
        address_found = any(re.search(p, text, re.I) for p in address_patterns)
        if address_found:
            findings.append("✅ Physical address detected")
            points += 2
        else:
            recommendations.append("Add full physical address")
            
        findings.append("ℹ️ GBP claim/verification status requires manual check")
        recommendations.append("Verify GBP is claimed and verified at business.google.com")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_gbp_optimization(self) -> CategoryScore:
        """Category 2: GBP Optimization (categories, photos, services)"""
        score = CategoryScore(name="GBP Optimization")
        findings = []
        recommendations = []
        points = 0
        
        # Check what we CAN verify from the website
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Check for services listed
            service_indicators = ['services', 'practice areas', 'what we do', 'areas of practice']
            if any(s in text for s in service_indicators):
                findings.append("✅ Services/practice areas listed on website")
                points += 3
            else:
                recommendations.append("Add a clear services/practice areas section")
                
            # Check for team/about section
            team_indicators = ['our team', 'our attorneys', 'about us', 'meet the team', 'our lawyers']
            if any(t in text for t in team_indicators):
                findings.append("✅ Team/about section found")
                points += 2
            else:
                recommendations.append("Add team bios and photos")
                
            # Check for business hours mentioned
            hour_indicators = ['hours', 'open', 'monday', 'available 24']
            if any(h in text for h in hour_indicators):
                findings.append("✅ Business hours mentioned")
                points += 2
            else:
                recommendations.append("Display business hours on website")
        
        # Note what requires manual GBP check
        findings.append("💡 Full GBP audit requires checking business.google.com")
        recommendations.append("Verify GBP has 10+ photos, complete description, all categories")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations[:3]
        return score
        
    def check_gbp_engagement(self) -> CategoryScore:
        """Category 3: GBP Engagement (posts, Q&A, messaging)"""
        score = CategoryScore(name="GBP Engagement")
        findings = []
        recommendations = []
        points = 0
        
        # Check what we CAN verify from website
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Check for review mentions/widgets
            if 'review' in text and ('google' in text or 'client' in text):
                findings.append("✅ Reviews referenced on website")
                points += 3
            else:
                recommendations.append("Display Google reviews on your website")
                
            # Check for blog/news (indicates active business)
            blog_indicators = ['blog', 'news', 'articles', 'resources', 'recent posts']
            if any(b in text for b in blog_indicators):
                findings.append("✅ Blog/news section indicates active updates")
                points += 3
            else:
                recommendations.append("Add a blog for regular content updates")
                
            # Check for contact options
            contact_indicators = ['contact', 'call us', 'email', 'message', 'chat']
            if sum(1 for c in contact_indicators if c in text) >= 2:
                findings.append("✅ Multiple contact options available")
                points += 2
        
        findings.append("💡 GBP post frequency & Q&A require manual review")
        recommendations.append("Post weekly updates to Google Business Profile")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations[:3]
        return score
        
    def check_website_local_signals(self) -> CategoryScore:
        """Category 4: Website Local Signals"""
        score = CategoryScore(name="Website Local Signals")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check title for local keywords
        title = self.soup.find('title')
        if title:
            title_text = title.get_text().lower()
            local_keywords = ['attorney', 'lawyer', 'law firm', 'legal']
            city_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b'  # Basic city pattern
            
            if any(kw in title_text for kw in local_keywords):
                findings.append("✅ Legal keywords in title")
                points += 2
            else:
                recommendations.append("Add practice area keywords to page title")
                
        # Check meta description
        meta_desc = self.soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            findings.append("✅ Meta description present")
            points += 2
        else:
            recommendations.append("Add meta description with local keywords")
            
        # Check for city/location mentions in content
        text = self.soup.get_text().lower()
        location_indicators = ['located in', 'serving', 'office in', 'based in']
        if any(ind in text for ind in location_indicators):
            findings.append("✅ Location/service area mentioned in content")
            points += 2
        else:
            recommendations.append("Mention your city and service areas in content")
            
        # Check mobile-friendliness
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if viewport:
            findings.append("✅ Mobile-friendly (viewport set)")
            points += 2
        else:
            findings.append("❌ Not mobile-friendly")
            recommendations.append("Make site mobile-responsive")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_nap_consistency(self) -> CategoryScore:
        """Category 5: NAP Consistency"""
        score = CategoryScore(name="NAP Consistency")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check for consistent NAP on page
        text = self.html or ''
        
        # Phone check (clickable)
        phone_links = self.soup.find_all('a', href=re.compile(r'^tel:'))
        if phone_links:
            findings.append("✅ Clickable phone number (tel: link)")
            points += 3
        else:
            recommendations.append("Make phone number clickable with tel: link")
            
        # Check HTTPS
        if self.url.startswith('https'):
            findings.append("✅ HTTPS secure")
            points += 2
        else:
            findings.append("❌ Not using HTTPS")
            recommendations.append("Enable HTTPS")
            
        # Check for schema with NAP
        json_ld = self.soup.find_all('script', type='application/ld+json')
        schema_has_nap = False
        for script in json_ld:
            try:
                data = json.loads(script.string)
                if 'telephone' in str(data) and 'address' in str(data):
                    schema_has_nap = True
                    break
            except:
                pass
                
        if schema_has_nap:
            findings.append("✅ NAP in structured data")
            points += 3
        else:
            recommendations.append("Include full NAP in LocalBusiness schema")
            
        findings.append("ℹ️ Cross-directory NAP consistency requires external checks")
        recommendations.append("Audit NAP across all directories (Yelp, Avvo, etc.)")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_location_pages(self) -> CategoryScore:
        """Category 6: Location Pages"""
        score = CategoryScore(name="Location Pages")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check for location-specific links in navigation
        nav_links = []
        for nav in self.soup.find_all(['nav', 'header', 'footer']):
            for link in nav.find_all('a', href=True):
                nav_links.append(link.get_text().lower())
                
        # Look for city/location patterns
        location_patterns = ['locations', 'areas we serve', 'service areas', 'offices']
        has_location_section = any(p in ' '.join(nav_links) for p in location_patterns)
        
        if has_location_section:
            findings.append("✅ Location/service area section found")
            points += 4
        else:
            recommendations.append("Create city-specific landing pages")
            recommendations.append("Add 'Areas We Serve' section")
            
        # Check for testimonials
        text = self.soup.get_text().lower()
        if 'testimonial' in text or 'review' in text or 'client said' in text:
            findings.append("✅ Testimonials present")
            points += 3
        else:
            recommendations.append("Add local client testimonials")
            
        # Check for local case studies
        if 'case study' in text or 'case result' in text:
            findings.append("✅ Case studies/results present")
            points += 3
        else:
            recommendations.append("Add local case studies with results")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_citations_directories(self) -> CategoryScore:
        """Category 7: Citations & Directories"""
        score = CategoryScore(name="Citations & Directories")
        findings = []
        recommendations = []
        points = 0
        
        if self.soup:
            text = self.soup.get_text().lower()
            html = str(self.soup).lower()
            
            # Check for directory badges/links on site
            directories = {
                'avvo': 3,
                'findlaw': 2, 
                'martindale': 3,
                'super lawyers': 3,
                'yelp': 2,
                'lawyers.com': 2,
                'justia': 2,
                'nolo': 1,
                'bbb': 2,
            }
            
            found_dirs = []
            for dir_name, pts in directories.items():
                if dir_name in text or dir_name in html:
                    found_dirs.append(dir_name)
                    points += pts
                    
            if found_dirs:
                findings.append(f"✅ Directory presence indicated: {', '.join(found_dirs)}")
            else:
                findings.append("⚠️ No directory badges or links found on site")
                recommendations.append("Add badges from Avvo, Super Lawyers, Martindale-Hubbell")
            
            # Check for award/recognition mentions
            award_terms = ['award', 'recognized', 'best lawyers', 'top rated', 'rising star']
            if any(a in text for a in award_terms):
                findings.append("✅ Awards/recognition mentioned")
                points += 2
                
        recommendations.append("Claim listings on Avvo, FindLaw, Justia, Lawyers.com")
        recommendations.append("Ensure NAP consistency across all directories")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations[:3]
        return score
        
    def check_reviews(self) -> CategoryScore:
        """Category 8: Reviews"""
        score = CategoryScore(name="Reviews")
        findings = []
        recommendations = []
        points = 0
        
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Check for review mentions
            review_patterns = ['review', 'testimonial', 'rating', '5 star', 'five star', 'google review']
            if any(p in text for p in review_patterns):
                findings.append("✅ Reviews/ratings mentioned on site")
                points += 3
            else:
                recommendations.append("Display Google reviews on your website")
                
            # Check for review schema
            json_ld = self.soup.find_all('script', type='application/ld+json')
            for script in json_ld:
                if 'aggregateRating' in (script.string or '').lower():
                    findings.append("✅ Review schema markup found")
                    points += 3
                    break
                    
        findings.append("ℹ️ Actual review count/rating requires Google API")
        
        recommendations.append("Target: 50+ Google reviews, 4.5+ rating")
        recommendations.append("Implement review generation campaign")
        recommendations.append("Respond to ALL reviews (positive and negative)")
        recommendations.append("Ask recent clients for reviews via email/text")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_local_content(self) -> CategoryScore:
        """Category 9: Local Content"""
        score = CategoryScore(name="Local Content")
        findings = []
        recommendations = []
        points = 0
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text().lower()
        
        # Check for blog
        nav_links = []
        for link in self.soup.find_all('a', href=True):
            nav_links.append(link.get_text().lower())
            
        if 'blog' in ' '.join(nav_links):
            findings.append("✅ Blog section found")
            points += 3
        else:
            recommendations.append("Start a blog with local legal content")
            
        # Check for local content indicators
        local_content = ['local', 'community', 'neighborhood', 'serving', 'our city']
        if any(lc in text for lc in local_content):
            findings.append("✅ Local content references found")
            points += 2
        else:
            recommendations.append("Create content about local laws, courts, news")
            
        # Check for resources section
        if 'resources' in ' '.join(nav_links) or 'guides' in ' '.join(nav_links):
            findings.append("✅ Resources/guides section found")
            points += 2
            
        # Check for community involvement
        community = ['sponsor', 'community', 'charity', 'volunteer', 'event']
        if any(c in text for c in community):
            findings.append("✅ Community involvement mentioned")
            points += 2
        else:
            recommendations.append("Highlight community involvement/sponsorships")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_local_links(self) -> CategoryScore:
        """Category 10: Local Link Building"""
        score = CategoryScore(name="Local Link Building")
        findings = []
        recommendations = []
        points = 0
        
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Check for partnership/sponsor mentions
            if 'partner' in text or 'sponsor' in text:
                findings.append("✅ Partnership/sponsorship mentions found")
                points += 3
                
            # Check for affiliate/association memberships
            assoc_terms = ['bar association', 'member of', 'association', 'chamber of commerce', 'affiliated']
            if any(a in text for a in assoc_terms):
                findings.append("✅ Professional associations mentioned")
                points += 3
                
            # Check for news/press mentions
            press_terms = ['featured in', 'as seen on', 'news', 'press', 'media coverage']
            if any(p in text for p in press_terms):
                findings.append("✅ Press/media coverage mentioned")
                points += 2
                
            # Check for local event involvement
            event_terms = ['event', 'seminar', 'workshop', 'webinar', 'speaking']
            if any(e in text for e in event_terms):
                findings.append("✅ Events/speaking engagements mentioned")
                points += 2
                
        if points == 0:
            findings.append("⚠️ No link-building signals found on site")
            
        findings.append("💡 Full backlink audit requires tools like Ahrefs or DataForSEO Backlinks API")
        recommendations.append("Get featured in local news and legal publications")
        recommendations.append("Sponsor local events for backlinks")
        recommendations.append("Join and get listed by bar associations")
        
        score.score = 5  # Middle score
        score.findings = findings
        score.recommendations = recommendations
        return score
    
    # ============ DATAFORSEO-POWERED CHECKS ============
    
    def check_serp_rankings(self, keywords: List[str] = None) -> CategoryScore:
        """Check actual Google SERP rankings using DataForSEO API"""
        score = CategoryScore(name="SERP Rankings (Live)")
        findings = []
        recommendations = []
        points = 0
        
        if not DATAFORSEO_AVAILABLE:
            findings.append("⚠️ DataForSEO client not available")
            score.score = 5
            score.findings = findings
            return score
            
        try:
            client = DataForSEOClient()
            
            # Generate keywords if not provided
            if not keywords:
                # Try to detect business type from page content
                business_type = "personal injury lawyer"  # Default
                if self.soup:
                    text = self.soup.get_text().lower()
                    if "car accident" in text:
                        business_type = "car accident lawyer"
                    elif "truck accident" in text:
                        business_type = "truck accident lawyer"
                    elif "medical malpractice" in text:
                        business_type = "medical malpractice lawyer"
                        
                # Try to detect city
                city = None
                if self.soup:
                    # Look for city in schema or content
                    text = self.soup.get_text()
                    # Common Texas cities for MVA
                    cities = ["Houston", "Dallas", "Austin", "San Antonio", "Fort Worth"]
                    for c in cities:
                        if c.lower() in text.lower():
                            city = c
                            break
                            
                keywords = client.generate_local_keywords(business_type, city)
            
            # Check rankings
            results = client.check_serp_rankings(self.domain, keywords[:5])
            
            findings.append(f"📊 Checked {results['keywords_checked']} keywords (live Google data)")
            
            if results['rankings_found'] > 0:
                findings.append(f"✅ Found {results['rankings_found']} ranking(s)")
                if results['top_3_count'] > 0:
                    findings.append(f"🏆 {results['top_3_count']} keyword(s) in top 3!")
                    points += results['top_3_count'] * 3
                if results['top_10_count'] > 0:
                    findings.append(f"✅ {results['top_10_count']} keyword(s) in top 10")
                    points += results['top_10_count'] * 2
                if results['top_20_count'] > 0:
                    findings.append(f"⚠️ {results['top_20_count'] - results['top_10_count']} keyword(s) in positions 11-20")
                    points += 1
                    
                # Show specific rankings
                for r in results['rankings'][:3]:
                    findings.append(f"  #{r['position']} for '{r['keyword']}'")
            else:
                findings.append("❌ No rankings found for target keywords")
                recommendations.append("Focus on ranking for your primary keywords")
                recommendations.append("Build more backlinks and optimize content")
                
            if results.get('cost'):
                findings.append(f"💰 API cost: ${results['cost']:.4f}")
                
        except Exception as e:
            findings.append(f"⚠️ Could not fetch SERP data: {str(e)[:50]}")
            points = 5  # Neutral score on error
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score
    
    def check_competitors(self, keyword: str = None) -> CategoryScore:
        """Analyze top competitors for primary keyword"""
        score = CategoryScore(name="Competitor Analysis")
        findings = []
        recommendations = []
        points = 5  # Neutral starting point
        
        if not DATAFORSEO_AVAILABLE:
            findings.append("⚠️ DataForSEO client not available")
            score.score = 5
            score.findings = findings
            return score
            
        try:
            client = DataForSEOClient()
            
            # Default keyword if not provided
            if not keyword:
                keyword = "personal injury lawyer"
                if self.soup:
                    text = self.soup.get_text().lower()
                    # Try to detect city
                    cities = ["houston", "dallas", "austin", "san antonio"]
                    for city in cities:
                        if city in text:
                            keyword = f"personal injury lawyer {city}"
                            break
            
            competitors = client.get_serp_competitors(keyword)
            
            if competitors:
                findings.append(f"📊 Top 5 competitors for '{keyword}':")
                for c in competitors[:5]:
                    findings.append(f"  #{c['position']}: {c['domain']}")
                    
                # Check if target domain is in top 10
                is_ranking = any(self.domain in c['domain'] for c in competitors)
                if is_ranking:
                    findings.append(f"✅ {self.domain} is ranking in top 10!")
                    points = 8
                else:
                    findings.append(f"❌ {self.domain} not in top 10")
                    recommendations.append("Analyze top competitors' content and backlinks")
                    recommendations.append("Create better, more comprehensive content")
                    points = 3
                    
        except Exception as e:
            findings.append(f"⚠️ Could not fetch competitor data")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        return score

    def run_full_audit(self, include_serp_check: bool = True) -> AuditResult:
        """Run complete audit across all 20 categories
        
        Args:
            include_serp_check: If True, includes live Google SERP ranking check via DataForSEO
                               (adds ~$0.01 to API costs but gives real ranking data)
        """
        result = AuditResult(url=self.url)
        
        # Fetch the page
        if not self.fetch_page():
            result.ai_categories = [CategoryScore(name="Error", findings=["Could not fetch website"])]
            return result
            
        # Try to extract business name
        if self.soup:
            title = self.soup.find('title')
            if title:
                result.business_name = title.get_text().split('|')[0].split('-')[0].strip()
                
        # AI Visibility Checks (10 categories)
        result.ai_categories = [
            self.check_crawler_access(),
            self.check_structured_data(),
            self.check_content_structure(),
            self.check_eeat_signals(),
            self.check_brand_mentions(),
            self.check_content_freshness(),
            self.check_question_content(),
            self.check_citations(),
            self.check_technical_performance(),
            self.check_ai_platform_presence(),
        ]
        
        # Local SEO Checks (10 categories)
        local_checks = [
            self.check_gbp_basics(),
            self.check_gbp_optimization(),
            self.check_gbp_engagement(),
            self.check_website_local_signals(),
            self.check_nap_consistency(),
            self.check_location_pages(),
            self.check_citations_directories(),
            self.check_reviews(),
            self.check_local_content(),
            self.check_local_links(),
        ]
        
        # Add live SERP check if enabled and DataForSEO is available
        if include_serp_check and DATAFORSEO_AVAILABLE:
            serp_check = self.check_serp_rankings()
            local_checks.append(serp_check)
            
        result.local_categories = local_checks
        
        # Calculate scores
        result.ai_visibility_score = sum(c.score for c in result.ai_categories)
        result.local_seo_score = sum(c.score for c in result.local_categories)
        result.total_score = result.ai_visibility_score + result.local_seo_score
        
        # Quick wins: Top recommendations from ALL categories, prioritized by impact
        # Focus on diverse, actionable items (not just from lowest scores)
        all_recs = []
        for cat in result.ai_categories + result.local_categories:
            if cat.recommendations and cat.max_score > 0:  # Skip informational categories
                # Weight by potential improvement (10 - current score)
                potential = cat.max_score - cat.score
                all_recs.append((potential, cat.name, cat.recommendations[0]))
        
        # Sort by potential improvement, take top unique categories
        all_recs.sort(key=lambda x: x[0], reverse=True)
        seen_cats = set()
        result.quick_wins = []
        for potential, cat_name, rec in all_recs:
            if cat_name not in seen_cats:
                result.quick_wins.append(rec)  # Just the recommendation, no category prefix
                seen_cats.add(cat_name)
            if len(result.quick_wins) >= 6:
                break
                
        # Priority fixes: Categories scoring below 50% (5/10)
        # Show what's broken, not what to do (that's in quick wins)
        priority_cats = [
            cat for cat in result.ai_categories + result.local_categories
            if cat.score < 5 and cat.max_score > 0
        ]
        priority_cats.sort(key=lambda c: c.score)
        
        result.priority_fixes = []
        for cat in priority_cats[:8]:
            # Show score and main issue
            main_issue = ""
            for f in cat.findings:
                if f.startswith("❌") or f.startswith("⚠️"):
                    main_issue = f.replace("❌ ", "").replace("⚠️ ", "")
                    break
            if main_issue:
                result.priority_fixes.append(f"{cat.name}: {main_issue}")
            else:
                result.priority_fixes.append(f"{cat.name} ({cat.score}/{cat.max_score})")
        
        return result


def main():
    """Test the analyzer"""
    import sys
    
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    
    print(f"\n🔍 Analyzing: {url}\n")
    
    analyzer = WebsiteAnalyzer(url)
    result = analyzer.run_full_audit()
    
    print(f"Business: {result.business_name}")
    print(f"\n📊 SCORES:")
    print(f"  AI Visibility: {result.ai_visibility_score}/100")
    print(f"  Local SEO: {result.local_seo_score}/100")
    print(f"  TOTAL: {result.total_score}/200")
    
    print(f"\n🤖 AI VISIBILITY BREAKDOWN:")
    for cat in result.ai_categories:
        print(f"\n  {cat.name}: {cat.score}/10")
        for f in cat.findings[:3]:
            print(f"    {f}")
            
    print(f"\n📍 LOCAL SEO BREAKDOWN:")
    for cat in result.local_categories:
        print(f"\n  {cat.name}: {cat.score}/10")
        for f in cat.findings[:3]:
            print(f"    {f}")
            
    print(f"\n⚡ QUICK WINS:")
    for qw in result.quick_wins[:5]:
        print(f"  • {qw}")
        
    print(f"\n🚨 PRIORITY FIXES:")
    for pf in result.priority_fixes[:5]:
        print(f"  • {pf}")


if __name__ == "__main__":
    main()
