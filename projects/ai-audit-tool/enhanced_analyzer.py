#!/usr/bin/env python3
"""
Enhanced AI & Local Visibility Audit Analyzer
Real API checks, granular analysis, actually valuable insights
"""

import requests
import json
import re
from urllib.parse import urlparse, urljoin, quote_plus
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
import time
import concurrent.futures
from collections import Counter
import hashlib

@dataclass
class CategoryScore:
    name: str
    score: int = 0  # 0-10
    max_score: int = 10
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)  # Raw data for advanced analysis
    
@dataclass
class AuditResult:
    url: str
    business_name: Optional[str] = None
    industry: Optional[str] = None
    ai_visibility_score: int = 0
    local_seo_score: int = 0
    total_score: int = 0
    grade: str = "F"
    ai_categories: List[CategoryScore] = field(default_factory=list)
    local_categories: List[CategoryScore] = field(default_factory=list)
    quick_wins: List[str] = field(default_factory=list)
    priority_fixes: List[str] = field(default_factory=list)
    technical_data: Dict[str, Any] = field(default_factory=dict)
    competitive_insights: List[str] = field(default_factory=list)
    

class EnhancedWebsiteAnalyzer:
    """
    Enhanced analyzer with:
    - Real PageSpeed API checks
    - Schema.org validation
    - Content quality analysis
    - Keyword density analysis
    - Mobile-friendliness checks
    - Security header analysis
    - Structured data completeness scoring
    """
    
    def __init__(self, url: str, pagespeed_api_key: str = None):
        self.url = url if url.startswith('http') else f'https://{url}'
        self.parsed_url = urlparse(self.url)
        self.domain = self.parsed_url.netloc.replace('www.', '')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.html = None
        self.soup = None
        self.robots_txt = None
        self.pagespeed_api_key = pagespeed_api_key
        self.page_speed_data = None
        self.all_pages = []  # For multi-page analysis
        self.schema_data = []
        
    def fetch_page(self, url: str = None) -> Tuple[str, BeautifulSoup]:
        """Fetch a page and return HTML + soup"""
        target_url = url or self.url
        try:
            resp = self.session.get(target_url, timeout=15, allow_redirects=True)
            resp.raise_for_status()
            html = resp.text
            soup = BeautifulSoup(html, 'html.parser')
            
            if url is None:  # Main page
                self.html = html
                self.soup = soup
                
            return html, soup
        except Exception as e:
            print(f"Error fetching {target_url}: {e}")
            return None, None
            
    def fetch_robots_txt(self) -> str:
        """Fetch and analyze robots.txt"""
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
        """Fetch sitemap and extract URLs"""
        urls = []
        sitemap_locations = [
            f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/sitemap.xml",
            f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/sitemap_index.xml",
        ]
        
        # Check robots.txt for sitemap location
        if self.robots_txt:
            for line in self.robots_txt.split('\n'):
                if line.lower().startswith('sitemap:'):
                    sitemap_locations.insert(0, line.split(':', 1)[1].strip())
                    
        for sitemap_url in sitemap_locations[:2]:  # Try first 2
            try:
                resp = self.session.get(sitemap_url, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'xml')
                    for loc in soup.find_all('loc'):
                        urls.append(loc.text)
                    if urls:
                        break
            except:
                continue
                
        return urls[:100]  # Limit to 100 URLs
        
    def fetch_pagespeed_data(self) -> Dict:
        """Get real PageSpeed Insights data (free API)"""
        # Using PageSpeed Insights API (free, no key required for basic)
        api_url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            'url': self.url,
            'strategy': 'mobile',
            'category': ['performance', 'accessibility', 'best-practices', 'seo']
        }
        if self.pagespeed_api_key:
            params['key'] = self.pagespeed_api_key
            
        try:
            resp = self.session.get(api_url, params=params, timeout=60)
            if resp.status_code == 200:
                self.page_speed_data = resp.json()
                return self.page_speed_data
        except Exception as e:
            print(f"PageSpeed API error: {e}")
        return {}
        
    def extract_all_schema(self) -> List[Dict]:
        """Extract and validate all schema.org data"""
        schemas = []
        if not self.soup:
            return schemas
            
        for script in self.soup.find_all('script', type='application/ld+json'):
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    schemas.extend(data)
                else:
                    schemas.append(data)
            except:
                pass
                
        self.schema_data = schemas
        return schemas
        
    def analyze_content_quality(self) -> Dict:
        """Deep content quality analysis"""
        if not self.soup:
            return {}
            
        # Get main content (exclude nav, footer, sidebar)
        for tag in self.soup(['nav', 'footer', 'aside', 'header', 'script', 'style']):
            tag.decompose()
            
        text = self.soup.get_text(separator=' ', strip=True)
        words = text.split()
        
        # Word count
        word_count = len(words)
        
        # Reading level (Flesch-Kincaid approximation)
        sentences = re.split(r'[.!?]+', text)
        sentence_count = len([s for s in sentences if s.strip()])
        
        # Syllable count approximation
        def count_syllables(word):
            word = word.lower()
            count = 0
            vowels = 'aeiouy'
            if word[0] in vowels:
                count += 1
            for i in range(1, len(word)):
                if word[i] in vowels and word[i-1] not in vowels:
                    count += 1
            if word.endswith('e'):
                count -= 1
            return max(1, count)
            
        total_syllables = sum(count_syllables(w) for w in words[:500])  # Sample
        
        # Flesch Reading Ease
        if sentence_count > 0 and word_count > 0:
            avg_sentence_length = word_count / sentence_count
            avg_syllables = total_syllables / min(500, word_count)
            flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables)
        else:
            flesch_score = 0
            
        # Keyword density (top words)
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                      'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
                      'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                      'should', 'may', 'might', 'must', 'shall', 'can', 'this', 'that',
                      'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'your',
                      'our', 'their', 'my', 'his', 'her', 'its', 'if', 'then', 'else', 'when',
                      'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                      'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                      'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here'}
        
        meaningful_words = [w.lower() for w in words if w.lower() not in stop_words and len(w) > 3]
        word_freq = Counter(meaningful_words)
        top_keywords = word_freq.most_common(10)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'flesch_score': round(flesch_score, 1),
            'reading_level': self._flesch_to_grade(flesch_score),
            'top_keywords': top_keywords,
            'avg_sentence_length': round(word_count / max(1, sentence_count), 1)
        }
        
    def _flesch_to_grade(self, score: float) -> str:
        """Convert Flesch score to grade level"""
        if score >= 90: return "5th grade (very easy)"
        if score >= 80: return "6th grade (easy)"
        if score >= 70: return "7th grade (fairly easy)"
        if score >= 60: return "8th-9th grade (standard)"
        if score >= 50: return "10th-12th grade (fairly difficult)"
        if score >= 30: return "College (difficult)"
        return "College graduate (very difficult)"
        
    def check_security_headers(self) -> Dict:
        """Check security headers"""
        try:
            resp = self.session.head(self.url, timeout=10)
            headers = resp.headers
            
            security_headers = {
                'Strict-Transport-Security': headers.get('Strict-Transport-Security'),
                'Content-Security-Policy': headers.get('Content-Security-Policy'),
                'X-Frame-Options': headers.get('X-Frame-Options'),
                'X-Content-Type-Options': headers.get('X-Content-Type-Options'),
                'X-XSS-Protection': headers.get('X-XSS-Protection'),
                'Referrer-Policy': headers.get('Referrer-Policy'),
            }
            
            return {
                'headers': security_headers,
                'score': sum(1 for v in security_headers.values() if v) / len(security_headers)
            }
        except:
            return {'headers': {}, 'score': 0}

    # ============ AI VISIBILITY CHECKS (Enhanced) ============
    
    def check_crawler_access(self) -> CategoryScore:
        """Enhanced: Crawler Access with specific bot analysis"""
        score = CategoryScore(name="AI Crawler Access")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        robots = self.fetch_robots_txt()
        
        # Specific AI bots to check
        ai_bots = {
            'GPTBot': {'name': 'ChatGPT/OpenAI', 'critical': True},
            'ClaudeBot': {'name': 'Claude/Anthropic', 'critical': True},
            'Claude-Web': {'name': 'Claude Web', 'critical': True},
            'anthropic-ai': {'name': 'Anthropic AI', 'critical': True},
            'PerplexityBot': {'name': 'Perplexity', 'critical': True},
            'Bytespider': {'name': 'TikTok/ByteDance', 'critical': False},
            'CCBot': {'name': 'Common Crawl', 'critical': False},
            'Google-Extended': {'name': 'Google AI Training', 'critical': True},
        }
        
        bot_status = {}
        
        for bot, info in ai_bots.items():
            if robots:
                # Check if explicitly blocked
                bot_section = False
                is_blocked = False
                
                lines = robots.lower().split('\n')
                for i, line in enumerate(lines):
                    if f'user-agent: {bot.lower()}' in line or f'user-agent: *' in line:
                        # Check subsequent lines for disallow
                        for j in range(i+1, min(i+10, len(lines))):
                            if lines[j].startswith('user-agent:'):
                                break
                            if 'disallow: /' in lines[j] and lines[j].strip() == 'disallow: /':
                                is_blocked = True
                                break
                                
                if is_blocked:
                    bot_status[bot] = 'blocked'
                    if info['critical']:
                        findings.append(f"❌ {info['name']} ({bot}) is BLOCKED")
                        recommendations.append(f"Remove {bot} block from robots.txt")
                else:
                    bot_status[bot] = 'allowed'
                    if info['critical']:
                        findings.append(f"✅ {info['name']} ({bot}) is allowed")
                        points += 1
            else:
                bot_status[bot] = 'allowed (no robots.txt)'
                points += 0.5
                
        details['bot_status'] = bot_status
        
        # Check for llms.txt
        try:
            llms_url = f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/llms.txt"
            resp = self.session.get(llms_url, timeout=5)
            if resp.status_code == 200:
                findings.append("✅ llms.txt file found (excellent for AI visibility)")
                details['llms_txt'] = resp.text[:500]
                points += 2
            else:
                findings.append("❌ No llms.txt file")
                recommendations.append("Create llms.txt file to help AI systems understand your business")
        except:
            findings.append("❌ No llms.txt file")
            recommendations.append("Create llms.txt with business description for AI systems")
            
        # Check for AI-specific meta tags
        if self.soup:
            ai_meta = self.soup.find('meta', {'name': 'robots'})
            if ai_meta:
                content = ai_meta.get('content', '').lower()
                if 'noai' in content or 'noimageai' in content:
                    findings.append("⚠️ AI-restrictive meta robots tag found")
                    details['meta_robots'] = content
                    
        score.score = min(int(points), 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_structured_data(self) -> CategoryScore:
        """Enhanced: Deep structured data analysis"""
        score = CategoryScore(name="Structured Data Quality")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        schemas = self.extract_all_schema()
        details['schemas_found'] = []
        
        if not schemas:
            findings.append("❌ No structured data (JSON-LD) found")
            recommendations.append("Add JSON-LD structured data - this is critical for AI visibility")
            score.score = 0
            score.findings = findings
            score.recommendations = recommendations
            return score
            
        # Analyze each schema
        schema_types = []
        has_local_business = False
        has_faq = False
        has_organization = False
        has_webpage = False
        has_breadcrumbs = False
        
        required_local_fields = ['name', 'address', 'telephone', 'openingHours', 'geo']
        local_fields_present = []
        
        for schema in schemas:
            schema_type = schema.get('@type', 'Unknown')
            if isinstance(schema_type, list):
                schema_type = schema_type[0]
            schema_types.append(schema_type)
            details['schemas_found'].append(schema_type)
            
            # Check LocalBusiness completeness
            if 'LocalBusiness' in str(schema_type) or 'LegalService' in str(schema_type) or 'Attorney' in str(schema_type):
                has_local_business = True
                for field in required_local_fields:
                    if field in schema or field in str(schema):
                        local_fields_present.append(field)
                        
            if 'FAQPage' in str(schema_type):
                has_faq = True
                # Count FAQ items
                if 'mainEntity' in schema:
                    faq_count = len(schema['mainEntity']) if isinstance(schema['mainEntity'], list) else 1
                    details['faq_count'] = faq_count
                    
            if 'Organization' in str(schema_type):
                has_organization = True
                
            if 'WebPage' in str(schema_type) or 'WebSite' in str(schema_type):
                has_webpage = True
                
            if 'BreadcrumbList' in str(schema_type):
                has_breadcrumbs = True
                
        # Score based on findings
        findings.append(f"Found {len(schemas)} schema object(s): {', '.join(set(schema_types))}")
        
        if has_local_business:
            findings.append("✅ LocalBusiness/LegalService schema found")
            points += 3
            completeness = len(set(local_fields_present)) / len(required_local_fields)
            details['local_business_completeness'] = f"{completeness*100:.0f}%"
            if completeness < 0.8:
                missing = set(required_local_fields) - set(local_fields_present)
                recommendations.append(f"Add missing LocalBusiness fields: {', '.join(missing)}")
        else:
            findings.append("❌ No LocalBusiness/LegalService schema")
            recommendations.append("Add LocalBusiness schema with full NAP and hours")
            
        if has_faq:
            findings.append(f"✅ FAQPage schema found ({details.get('faq_count', '?')} questions)")
            points += 2
        else:
            findings.append("❌ No FAQPage schema")
            recommendations.append("Add FAQPage schema for rich results and AI visibility")
            
        if has_organization:
            findings.append("✅ Organization schema found")
            points += 1
        else:
            recommendations.append("Add Organization schema with logo, social profiles")
            
        if has_breadcrumbs:
            findings.append("✅ BreadcrumbList schema found")
            points += 1
            
        # Check for author schema (important for E-E-A-T)
        has_author = any('author' in str(s).lower() for s in schemas)
        if has_author:
            findings.append("✅ Author information in schema")
            points += 1
        else:
            recommendations.append("Add author schema with credentials for E-E-A-T")
            
        # Check for review/rating schema
        has_reviews = any('aggregateRating' in str(s) or 'Review' in str(s) for s in schemas)
        if has_reviews:
            findings.append("✅ Review/rating schema found")
            points += 2
        else:
            recommendations.append("Add AggregateRating schema to display star ratings")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_content_structure(self) -> CategoryScore:
        """Enhanced: Content structure with AI-readability focus"""
        score = CategoryScore(name="Content Structure")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Heading analysis
        h1s = self.soup.find_all('h1')
        h2s = self.soup.find_all('h2')
        h3s = self.soup.find_all('h3')
        
        details['h1_count'] = len(h1s)
        details['h2_count'] = len(h2s)
        details['h3_count'] = len(h3s)
        details['h1_text'] = [h.get_text(strip=True)[:100] for h in h1s]
        
        if len(h1s) == 1:
            findings.append(f"✅ Single H1: \"{h1s[0].get_text(strip=True)[:60]}...\"")
            points += 2
        elif len(h1s) == 0:
            findings.append("❌ No H1 tag found")
            recommendations.append("Add a single, keyword-rich H1 tag")
        else:
            findings.append(f"⚠️ Multiple H1 tags ({len(h1s)}) - should have only one")
            recommendations.append("Use only one H1 tag per page")
            points += 1
            
        if len(h2s) >= 3:
            findings.append(f"✅ {len(h2s)} H2 tags structuring content")
            points += 2
        elif h2s:
            findings.append(f"⚠️ Only {len(h2s)} H2 tags")
            points += 1
        else:
            findings.append("❌ No H2 tags")
            recommendations.append("Add H2 tags to structure content into clear sections")
            
        # Content quality analysis
        content_analysis = self.analyze_content_quality()
        details.update(content_analysis)
        
        word_count = content_analysis.get('word_count', 0)
        if word_count >= 1500:
            findings.append(f"✅ Comprehensive content ({word_count:,} words)")
            points += 2
        elif word_count >= 500:
            findings.append(f"⚠️ Moderate content ({word_count:,} words)")
            points += 1
        else:
            findings.append(f"❌ Thin content ({word_count:,} words)")
            recommendations.append("Expand content to 1,500+ words for competitive rankings")
            
        # Reading level
        flesch = content_analysis.get('flesch_score', 0)
        reading_level = content_analysis.get('reading_level', 'Unknown')
        if 50 <= flesch <= 70:
            findings.append(f"✅ Good readability ({reading_level})")
            points += 1
        else:
            findings.append(f"ℹ️ Reading level: {reading_level}")
            
        # Lists and tables (AI-friendly formatting)
        lists = self.soup.find_all(['ul', 'ol'])
        tables = self.soup.find_all('table')
        
        if len(lists) >= 3:
            findings.append(f"✅ {len(lists)} lists (great for AI parsing)")
            points += 1
        else:
            recommendations.append("Add bullet/numbered lists for better AI comprehension")
            
        if tables:
            findings.append(f"✅ {len(tables)} data table(s)")
            points += 1
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_eeat_signals(self) -> CategoryScore:
        """Enhanced: E-E-A-T analysis"""
        score = CategoryScore(name="E-E-A-T Signals")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text().lower()
        html_lower = (self.html or '').lower()
        
        # Experience indicators
        experience_patterns = [
            (r'\d+\+?\s*years?\s*(of\s*)?(experience|practicing)', 'years experience'),
            (r'since\s*(19|20)\d{2}', 'established date'),
            (r'handled\s*\d+', 'case count'),
            (r'helped\s*(over\s*)?\d+', 'clients helped'),
        ]
        
        experience_found = []
        for pattern, name in experience_patterns:
            if re.search(pattern, text):
                experience_found.append(name)
                
        if experience_found:
            findings.append(f"✅ Experience signals: {', '.join(experience_found)}")
            points += 2
            details['experience_signals'] = experience_found
        else:
            recommendations.append("Add specific experience metrics (years, case count)")
            
        # Expertise indicators
        expertise_patterns = [
            ('esq', 'Esq. credential'),
            ('j.d.', 'J.D. degree'),
            ('board certified', 'board certification'),
            ('specializ', 'specialization'),
            ('super lawyers', 'Super Lawyers'),
            ('best lawyers', 'Best Lawyers'),
            ('martindale', 'Martindale rating'),
            ('avvo', 'Avvo profile'),
        ]
        
        expertise_found = []
        for pattern, name in expertise_patterns:
            if pattern in text:
                expertise_found.append(name)
                
        if len(expertise_found) >= 2:
            findings.append(f"✅ Expertise signals: {', '.join(expertise_found[:4])}")
            points += 2
        elif expertise_found:
            findings.append(f"⚠️ Some expertise signals: {', '.join(expertise_found)}")
            points += 1
        else:
            findings.append("❌ No expertise credentials found")
            recommendations.append("Highlight attorney credentials, awards, and certifications")
            
        details['expertise_signals'] = expertise_found
        
        # Authoritativeness
        authority_patterns = [
            ('as seen on', 'media mentions'),
            ('featured in', 'press features'),
            ('quoted in', 'press quotes'),
            ('award', 'awards'),
            ('recognition', 'recognition'),
            ('member of', 'memberships'),
            ('bar association', 'bar membership'),
        ]
        
        authority_found = []
        for pattern, name in authority_patterns:
            if pattern in text:
                authority_found.append(name)
                
        if authority_found:
            findings.append(f"✅ Authority signals: {', '.join(authority_found[:3])}")
            points += 2
            details['authority_signals'] = authority_found
        else:
            recommendations.append("Add media mentions, awards, and professional memberships")
            
        # Trustworthiness
        trust_patterns = [
            (r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', 'phone number'),
            (r'[\w\.-]+@[\w\.-]+\.\w+', 'email'),
            ('privacy policy', 'privacy policy'),
            ('terms', 'terms of service'),
            ('bbb', 'BBB'),
            ('secure', 'security mention'),
        ]
        
        trust_found = []
        for pattern, name in trust_patterns:
            if re.search(pattern, text):
                trust_found.append(name)
                
        if len(trust_found) >= 3:
            findings.append(f"✅ Trust signals: {', '.join(trust_found[:4])}")
            points += 2
        elif trust_found:
            findings.append(f"⚠️ Some trust signals: {', '.join(trust_found)}")
            points += 1
        else:
            recommendations.append("Add clear contact info, privacy policy, and trust badges")
            
        details['trust_signals'] = trust_found
        
        # Check for author/about pages
        about_links = self.soup.find_all('a', href=re.compile(r'(about|team|attorney|lawyer|author)', re.I))
        if about_links:
            findings.append(f"✅ {len(about_links)} about/team page links found")
            points += 1
        else:
            recommendations.append("Add prominent links to attorney bio pages")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_brand_mentions(self) -> CategoryScore:
        """Brand presence and mentions"""
        score = CategoryScore(name="Brand Presence")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Social media links
        social_patterns = {
            'facebook': r'facebook\.com/(?!sharer)',
            'twitter': r'(twitter|x)\.com/',
            'linkedin': r'linkedin\.com/(company|in)/',
            'youtube': r'youtube\.com/(channel|c|@)',
            'instagram': r'instagram\.com/',
            'tiktok': r'tiktok\.com/@',
        }
        
        socials_found = []
        for link in self.soup.find_all('a', href=True):
            href = link['href'].lower()
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href):
                    socials_found.append(platform)
                    
        socials_found = list(set(socials_found))
        details['social_profiles'] = socials_found
        
        if len(socials_found) >= 4:
            findings.append(f"✅ Strong social presence: {', '.join(socials_found)}")
            points += 3
        elif len(socials_found) >= 2:
            findings.append(f"⚠️ Some social profiles: {', '.join(socials_found)}")
            points += 1
        else:
            findings.append("❌ Limited social media presence")
            recommendations.append("Add links to active social media profiles")
            
        # Check for schema social links
        for schema in self.schema_data:
            if 'sameAs' in schema:
                same_as = schema['sameAs']
                if isinstance(same_as, list):
                    details['schema_social'] = same_as
                    findings.append(f"✅ {len(same_as)} social profiles in schema")
                    points += 1
                    break
                    
        # Review platform mentions
        review_platforms = ['google', 'yelp', 'avvo', 'lawyers.com', 'findlaw', 'justia', 'martindale']
        platforms_mentioned = []
        text = self.soup.get_text().lower()
        
        for platform in review_platforms:
            if platform in text:
                platforms_mentioned.append(platform)
                
        if platforms_mentioned:
            findings.append(f"✅ Review platform mentions: {', '.join(platforms_mentioned)}")
            points += 2
            details['review_platforms'] = platforms_mentioned
        else:
            recommendations.append("Mention and link to review profiles (Google, Avvo, etc.)")
            
        # Video presence
        youtube_embeds = self.soup.find_all('iframe', src=re.compile(r'youtube', re.I))
        video_tags = self.soup.find_all('video')
        
        if youtube_embeds or video_tags:
            findings.append(f"✅ Video content found ({len(youtube_embeds)} YouTube embeds)")
            points += 2
        else:
            recommendations.append("Add video content to increase engagement and AI visibility")
            
        # External brand mentions (would need API for full check)
        findings.append("ℹ️ Full brand mention analysis requires external API")
        recommendations.append("Build Reddit presence in legal subreddits")
        recommendations.append("Pursue Wikipedia mention if notable")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_content_freshness(self) -> CategoryScore:
        """Content freshness analysis"""
        score = CategoryScore(name="Content Freshness")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Check schema dates
        for schema in self.schema_data:
            if 'datePublished' in schema:
                details['datePublished'] = schema['datePublished']
                findings.append(f"✅ datePublished in schema: {schema['datePublished']}")
                points += 2
            if 'dateModified' in schema:
                details['dateModified'] = schema['dateModified']
                findings.append(f"✅ dateModified in schema: {schema['dateModified']}")
                points += 2
                
        if 'datePublished' not in details:
            findings.append("❌ No datePublished in schema")
            recommendations.append("Add datePublished and dateModified to schema markup")
            
        # Check meta tags
        og_date = self.soup.find('meta', {'property': 'article:published_time'})
        if og_date:
            findings.append("✅ Open Graph publish date found")
            points += 1
            
        # Check visible dates
        date_patterns = [
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+202[4-6]',
            r'(updated|modified|published)[\s:]+[\w\s,]+202[4-6]',
        ]
        
        text = self.soup.get_text()
        recent_dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.I)
            recent_dates.extend(matches)
            
        if recent_dates:
            findings.append(f"✅ Recent dates found in content")
            points += 2
        else:
            findings.append("⚠️ No recent dates visible in content")
            recommendations.append("Display publication/update dates on content")
            
        # Check for blog
        nav_links = [a.get_text().lower() for a in self.soup.find_all('a', href=True)]
        has_blog = any(word in ' '.join(nav_links) for word in ['blog', 'news', 'articles', 'insights', 'resources'])
        
        if has_blog:
            findings.append("✅ Blog/news section present")
            points += 2
        else:
            findings.append("❌ No blog section found")
            recommendations.append("Start a blog with weekly content updates")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_question_content(self) -> CategoryScore:
        """FAQ and question-based content"""
        score = CategoryScore(name="Question-Based Content")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text()
        
        # FAQ section check
        faq_patterns = ['faq', 'frequently asked', 'common questions', 'questions and answers']
        has_faq_section = any(p in text.lower() for p in faq_patterns)
        
        if has_faq_section:
            findings.append("✅ FAQ section found on page")
            points += 2
        else:
            recommendations.append("Add an FAQ section answering common client questions")
            
        # FAQ schema check
        has_faq_schema = any('FAQPage' in str(s) for s in self.schema_data)
        if has_faq_schema:
            findings.append("✅ FAQPage schema markup present")
            points += 3
        else:
            findings.append("❌ No FAQPage schema")
            recommendations.append("Add FAQPage schema for rich snippets in search")
            
        # Count questions in content
        questions = re.findall(r'[^.!?]*\?', text)
        meaningful_questions = [q for q in questions if len(q.strip()) > 20]
        details['question_count'] = len(meaningful_questions)
        
        if len(meaningful_questions) >= 10:
            findings.append(f"✅ {len(meaningful_questions)} questions in content (excellent)")
            points += 3
        elif len(meaningful_questions) >= 5:
            findings.append(f"⚠️ {len(meaningful_questions)} questions in content")
            points += 1
        else:
            findings.append(f"❌ Only {len(meaningful_questions)} questions in content")
            recommendations.append("Add more question-format headings that mirror user queries")
            
        # How-to content
        howto_patterns = ['how to', 'step by step', 'guide', 'what to do', 'process']
        if any(p in text.lower() for p in howto_patterns):
            findings.append("✅ How-to/guide content present")
            points += 2
        else:
            recommendations.append("Add how-to guides for common legal processes")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_citations(self) -> CategoryScore:
        """Citations and source analysis"""
        score = CategoryScore(name="Citations & Sources")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # External links analysis
        external_links = []
        internal_links = []
        
        for link in self.soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('http') and self.domain not in href:
                external_links.append(href)
            elif href.startswith('/') or self.domain in href:
                internal_links.append(href)
                
        details['external_link_count'] = len(external_links)
        details['internal_link_count'] = len(internal_links)
        
        # Authoritative domains
        auth_domains = ['.gov', '.edu', 'nhtsa.gov', 'cdc.gov', 'nih.gov', 'who.int', 'law.cornell.edu']
        auth_links = [l for l in external_links if any(d in l.lower() for d in auth_domains)]
        
        if len(auth_links) >= 3:
            findings.append(f"✅ {len(auth_links)} authoritative source links (.gov, .edu)")
            points += 4
        elif auth_links:
            findings.append(f"⚠️ {len(auth_links)} authoritative link(s)")
            points += 2
        else:
            findings.append("❌ No authoritative (.gov, .edu) sources cited")
            recommendations.append("Cite government and educational sources for credibility")
            
        details['authoritative_links'] = auth_links[:5]
        
        # Statistics check
        text = self.soup.get_text()
        stat_patterns = [r'\d+%', r'\$[\d,]+', r'\d+ (million|billion|thousand)', 'according to', 'study shows', 'research']
        stats_found = sum(1 for p in stat_patterns if re.search(p, text, re.I))
        
        if stats_found >= 4:
            findings.append(f"✅ Rich in statistics and data citations")
            points += 3
        elif stats_found >= 2:
            findings.append(f"⚠️ Some statistics present")
            points += 1
        else:
            recommendations.append("Add statistics with source attribution")
            
        # Internal linking
        if len(internal_links) >= 10:
            findings.append(f"✅ Strong internal linking ({len(internal_links)} links)")
            points += 2
        elif len(internal_links) >= 5:
            findings.append(f"⚠️ Moderate internal linking ({len(internal_links)} links)")
            points += 1
        else:
            recommendations.append("Add more internal links to related content")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_technical_performance(self) -> CategoryScore:
        """Technical performance with real metrics"""
        score = CategoryScore(name="Technical Performance")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        # HTTPS check
        if self.url.startswith('https'):
            findings.append("✅ HTTPS enabled")
            points += 1
        else:
            findings.append("❌ Not using HTTPS")
            recommendations.append("Enable HTTPS immediately - critical for trust and SEO")
            
        # Security headers
        security = self.check_security_headers()
        details['security_headers'] = security
        
        if security['score'] >= 0.5:
            findings.append(f"✅ Good security headers ({security['score']*100:.0f}%)")
            points += 1
        else:
            recommendations.append("Add security headers (HSTS, CSP, X-Frame-Options)")
            
        if not self.soup:
            score.findings = findings + ["⚠️ Could not analyze page content"]
            score.score = points
            return score
            
        # Mobile viewport
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if viewport:
            findings.append("✅ Mobile viewport configured")
            points += 1
        else:
            findings.append("❌ No mobile viewport")
            recommendations.append("Add mobile viewport meta tag")
            
        # Page size estimation
        if self.html:
            html_size = len(self.html) / 1024
            details['html_size_kb'] = round(html_size, 1)
            
            if html_size < 100:
                findings.append(f"✅ Lightweight HTML ({html_size:.0f}KB)")
                points += 1
            elif html_size < 300:
                findings.append(f"⚠️ Moderate HTML size ({html_size:.0f}KB)")
            else:
                findings.append(f"❌ Heavy HTML ({html_size:.0f}KB)")
                recommendations.append("Reduce page size for faster loading")
                
        # Image optimization check
        images = self.soup.find_all('img')
        lazy_images = sum(1 for img in images if img.get('loading') == 'lazy')
        webp_images = sum(1 for img in images if '.webp' in str(img.get('src', '')))
        
        details['total_images'] = len(images)
        details['lazy_loaded'] = lazy_images
        details['webp_format'] = webp_images
        
        if images:
            if lazy_images > len(images) / 2:
                findings.append(f"✅ {lazy_images}/{len(images)} images lazy-loaded")
                points += 1
            else:
                recommendations.append("Implement lazy loading for images")
                
        # Scripts analysis
        scripts = self.soup.find_all('script', src=True)
        async_scripts = sum(1 for s in scripts if s.get('async') or s.get('defer'))
        
        details['total_scripts'] = len(scripts)
        details['async_scripts'] = async_scripts
        
        if scripts:
            if async_scripts > len(scripts) / 2:
                findings.append(f"✅ Scripts properly async/deferred")
                points += 1
            else:
                recommendations.append("Add async/defer to scripts to improve load time")
                
        # Try PageSpeed API (if not too slow)
        # Commenting out to avoid delays - can enable if needed
        # psi = self.fetch_pagespeed_data()
        # if psi and 'lighthouseResult' in psi:
        #     perf_score = psi['lighthouseResult']['categories']['performance']['score'] * 100
        #     findings.append(f"📊 PageSpeed Performance: {perf_score:.0f}/100")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_ai_platform_presence(self) -> CategoryScore:
        """AI platform visibility"""
        score = CategoryScore(name="AI Platform Presence")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if self.soup:
            # YouTube presence
            youtube_links = self.soup.find_all('a', href=re.compile(r'youtube\.com', re.I))
            youtube_embeds = self.soup.find_all('iframe', src=re.compile(r'youtube', re.I))
            
            if youtube_links or youtube_embeds:
                findings.append(f"✅ YouTube presence ({len(youtube_links)} links, {len(youtube_embeds)} embeds)")
                points += 3
            else:
                recommendations.append("Create YouTube content and embed on site")
                
            # Podcast mentions
            podcast_platforms = ['spotify', 'apple podcasts', 'podcast']
            text = self.soup.get_text().lower()
            if any(p in text for p in podcast_platforms):
                findings.append("✅ Podcast presence mentioned")
                points += 2
                
        # llms.txt check (already done in crawler access, but relevant here too)
        try:
            llms_resp = self.session.get(f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/llms.txt", timeout=5)
            if llms_resp.status_code == 200:
                points += 2  # Bonus for AI discoverability
        except:
            pass
            
        # Structured data for AI (already scored, but matters here)
        if self.schema_data:
            points += 2
            
        findings.append("ℹ️ To verify AI visibility:")
        findings.append("  → Ask ChatGPT: 'What law firms handle [your practice] in [your city]?'")
        findings.append("  → Ask Perplexity the same question")
        findings.append("  → Check if you appear in AI Overview results")
        
        recommendations.append("Test AI visibility by querying ChatGPT/Claude about your practice area")
        recommendations.append("Enable YouTube transcripts for AI training")
        recommendations.append("Build presence on Reddit in relevant communities")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    # ============ LOCAL SEO CHECKS (Enhanced) ============
    
    def check_gbp_basics(self) -> CategoryScore:
        """Google Business Profile basics"""
        score = CategoryScore(name="GBP Basics")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Google Maps embed
        maps_embeds = self.soup.find_all('iframe', src=re.compile(r'google.*map', re.I))
        if maps_embeds:
            findings.append(f"✅ Google Maps embed found")
            points += 2
        else:
            recommendations.append("Embed Google Maps on contact page")
            
        # LocalBusiness schema
        has_local_schema = any(
            'LocalBusiness' in str(s) or 'LegalService' in str(s) or 'Attorney' in str(s)
            for s in self.schema_data
        )
        
        if has_local_schema:
            findings.append("✅ LocalBusiness/LegalService schema present")
            points += 2
        else:
            findings.append("❌ No LocalBusiness schema")
            recommendations.append("Add LocalBusiness schema with complete NAP")
            
        # Phone number
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_match = re.search(phone_pattern, self.html or '')
        if phone_match:
            findings.append(f"✅ Phone number: {phone_match.group()}")
            points += 2
            details['phone'] = phone_match.group()
        else:
            findings.append("❌ No phone number found")
            recommendations.append("Add prominently displayed phone number")
            
        # Clickable phone
        tel_links = self.soup.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            findings.append("✅ Clickable phone (tel: link)")
            points += 1
        else:
            recommendations.append("Make phone number clickable with tel: link")
            
        # Address
        address_patterns = [
            r'\d+\s+[\w\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|way|lane|ln)',
            r'suite\s+\d+',
        ]
        has_address = any(re.search(p, (self.html or '').lower()) for p in address_patterns)
        
        if has_address:
            findings.append("✅ Physical address present")
            points += 2
        else:
            recommendations.append("Add full physical address")
            
        findings.append("ℹ️ Verify GBP is claimed at business.google.com")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_gbp_optimization(self) -> CategoryScore:
        """GBP optimization"""
        score = CategoryScore(name="GBP Optimization")
        findings = []
        recommendations = []
        
        findings.append("ℹ️ GBP optimization requires manual review:")
        findings.append("  → Check: business.google.com/dashboard")
        findings.append("  → Verify: categories, description, photos, services, hours")
        
        recommendations.append("Add 3-5 secondary categories (e.g., 'Personal Injury Attorney')")
        recommendations.append("Upload 25+ high-quality photos (office, team, logo, case results)")
        recommendations.append("List all services with descriptions")
        recommendations.append("Write 750-character keyword-rich description")
        recommendations.append("Keep hours accurate and add holiday hours")
        
        score.score = 5  # Middle score - can't verify
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_gbp_engagement(self) -> CategoryScore:
        """GBP engagement"""
        score = CategoryScore(name="GBP Engagement")
        findings = []
        recommendations = []
        
        findings.append("ℹ️ GBP engagement requires manual review or API:")
        findings.append("  → Check posting frequency")
        findings.append("  → Verify messaging is enabled")
        findings.append("  → Review Q&A section")
        
        recommendations.append("Post weekly updates (events, tips, case results)")
        recommendations.append("Enable and monitor messaging")
        recommendations.append("Proactively add Q&A with common questions")
        recommendations.append("Add all relevant attributes (wheelchair access, etc.)")
        recommendations.append("Respond to all reviews within 24 hours")
        
        score.score = 5  # Middle score
        score.findings = findings
        score.recommendations = recommendations
        return score
        
    def check_website_local_signals(self) -> CategoryScore:
        """Website local signals"""
        score = CategoryScore(name="Website Local Signals")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Title tag analysis
        title = self.soup.find('title')
        if title:
            title_text = title.get_text()
            details['title'] = title_text
            
            # Check for practice area keywords
            legal_keywords = ['attorney', 'lawyer', 'law firm', 'legal', 'injury', 'accident']
            if any(kw in title_text.lower() for kw in legal_keywords):
                findings.append(f"✅ Legal keywords in title")
                points += 2
            else:
                recommendations.append("Add practice area keywords to title")
                
            # Check for location
            if len(title_text) > 60:
                findings.append(f"⚠️ Title too long ({len(title_text)} chars) - may be truncated")
            else:
                findings.append(f"✅ Good title length ({len(title_text)} chars)")
                points += 1
        else:
            findings.append("❌ No title tag")
            recommendations.append("Add a keyword-optimized title tag")
            
        # Meta description
        meta_desc = self.soup.find('meta', {'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            desc = meta_desc['content']
            details['meta_description'] = desc
            
            if 120 <= len(desc) <= 160:
                findings.append(f"✅ Good meta description length ({len(desc)} chars)")
                points += 2
            elif len(desc) > 0:
                findings.append(f"⚠️ Meta description: {len(desc)} chars (aim for 120-160)")
                points += 1
        else:
            findings.append("❌ No meta description")
            recommendations.append("Add meta description with location and practice area")
            
        # Local content indicators
        text = self.soup.get_text().lower()
        local_phrases = ['serving', 'located in', 'office in', 'based in', 'near', 'local']
        local_mentions = sum(1 for p in local_phrases if p in text)
        
        if local_mentions >= 3:
            findings.append(f"✅ Strong local language ({local_mentions} mentions)")
            points += 2
        elif local_mentions > 0:
            findings.append(f"⚠️ Some local signals ({local_mentions} mentions)")
            points += 1
        else:
            recommendations.append("Add local language (serving [city], located in [area])")
            
        # Mobile friendly
        viewport = self.soup.find('meta', {'name': 'viewport'})
        if viewport:
            findings.append("✅ Mobile viewport set")
            points += 1
        else:
            findings.append("❌ Not mobile-friendly")
            recommendations.append("Critical: Make site mobile-responsive")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_nap_consistency(self) -> CategoryScore:
        """NAP consistency"""
        score = CategoryScore(name="NAP Consistency")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Extract NAP from page
        text = self.html or ''
        
        # Phone extraction
        phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        unique_phones = list(set(phones))
        details['phones_found'] = unique_phones
        
        if len(unique_phones) == 1:
            findings.append(f"✅ Consistent phone number: {unique_phones[0]}")
            points += 2
        elif len(unique_phones) > 1:
            findings.append(f"⚠️ Multiple phone numbers: {', '.join(unique_phones[:3])}")
            recommendations.append("Use one consistent phone number throughout site")
            points += 1
        else:
            findings.append("❌ No phone number found")
            recommendations.append("Add phone number to every page")
            
        # Clickable phone
        tel_links = self.soup.find_all('a', href=re.compile(r'^tel:'))
        if tel_links:
            findings.append("✅ Clickable phone link(s)")
            points += 2
        else:
            recommendations.append("Make phone number clickable (tel: link)")
            
        # NAP in schema
        schema_nap = False
        for schema in self.schema_data:
            if 'telephone' in str(schema) and 'address' in str(schema):
                schema_nap = True
                break
                
        if schema_nap:
            findings.append("✅ NAP in structured data")
            points += 2
        else:
            recommendations.append("Add complete NAP to LocalBusiness schema")
            
        # HTTPS
        if self.url.startswith('https'):
            findings.append("✅ HTTPS secure")
            points += 1
        else:
            findings.append("❌ Not HTTPS")
            
        # Footer NAP (common pattern)
        footer = self.soup.find('footer')
        if footer:
            footer_text = footer.get_text()
            has_footer_nap = bool(re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', footer_text))
            if has_footer_nap:
                findings.append("✅ NAP in footer")
                points += 1
                
        findings.append("ℹ️ Cross-directory NAP check requires external tools")
        recommendations.append("Audit NAP across all directories (Yelp, Avvo, FindLaw, etc.)")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_location_pages(self) -> CategoryScore:
        """Location/city pages"""
        score = CategoryScore(name="Location Pages")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Look for location-related links
        all_links = self.soup.find_all('a', href=True)
        location_links = []
        
        location_patterns = [
            r'/location', r'/office', r'/areas', r'/cities', r'/serving',
            r'-attorney', r'-lawyer', r'-accident', r'-injury'
        ]
        
        for link in all_links:
            href = link['href'].lower()
            text = link.get_text().lower()
            if any(re.search(p, href) for p in location_patterns):
                location_links.append(href)
            elif 'location' in text or 'office' in text or 'serving' in text:
                location_links.append(href)
                
        details['location_links'] = list(set(location_links))[:10]
        
        if len(location_links) >= 5:
            findings.append(f"✅ {len(location_links)} location-related pages")
            points += 4
        elif location_links:
            findings.append(f"⚠️ {len(location_links)} location page(s)")
            points += 2
        else:
            findings.append("❌ No dedicated location pages found")
            recommendations.append("Create city-specific landing pages for each service area")
            
        # Testimonials
        text = self.soup.get_text().lower()
        if 'testimonial' in text or 'client reviews' in text or 'what our clients say' in text:
            findings.append("✅ Testimonials section present")
            points += 2
        else:
            recommendations.append("Add client testimonials (ideally with location)")
            
        # Case results
        if 'case result' in text or 'verdict' in text or 'settlement' in text or 'recovered' in text:
            findings.append("✅ Case results displayed")
            points += 2
        else:
            recommendations.append("Display notable case results with amounts")
            
        # Local photos/imagery
        images = self.soup.find_all('img')
        alt_texts = [img.get('alt', '').lower() for img in images]
        local_images = sum(1 for alt in alt_texts if any(word in alt for word in ['office', 'team', 'building', 'location']))
        
        if local_images >= 3:
            findings.append(f"✅ Local imagery with descriptive alt text")
            points += 1
        else:
            recommendations.append("Add local photos with descriptive alt text")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_citations_directories(self) -> CategoryScore:
        """Citations and directories"""
        score = CategoryScore(name="Citations & Directories")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Check for directory mentions/links
            directories = {
                'avvo': 'Avvo',
                'findlaw': 'FindLaw',
                'justia': 'Justia',
                'martindale': 'Martindale-Hubbell',
                'lawyers.com': 'Lawyers.com',
                'yelp': 'Yelp',
                'bbb': 'BBB',
                'super lawyers': 'Super Lawyers',
                'best lawyers': 'Best Lawyers',
            }
            
            found_dirs = []
            for pattern, name in directories.items():
                if pattern in text:
                    found_dirs.append(name)
                    
            details['directories_mentioned'] = found_dirs
            
            if len(found_dirs) >= 4:
                findings.append(f"✅ Strong directory presence: {', '.join(found_dirs)}")
                points += 5
            elif found_dirs:
                findings.append(f"⚠️ Some directory mentions: {', '.join(found_dirs)}")
                points += 2
            else:
                findings.append("❌ No directory/citation mentions found")
                
        findings.append("ℹ️ Full citation audit requires external tools")
        
        recommendations.append("Claim/verify: Google, Yelp, Avvo, FindLaw, Justia")
        recommendations.append("Submit to legal directories: Lawyers.com, Martindale")
        recommendations.append("Join local chamber of commerce")
        recommendations.append("Get listed on Apple Maps and Bing Places")
        recommendations.append("Ensure NAP is identical across all citations")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_reviews(self) -> CategoryScore:
        """Reviews analysis"""
        score = CategoryScore(name="Reviews")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        text = self.soup.get_text().lower()
        
        # Review mentions
        review_patterns = ['review', 'testimonial', 'rating', '5 star', 'five star', 'google review']
        review_mentions = sum(1 for p in review_patterns if p in text)
        
        if review_mentions >= 3:
            findings.append("✅ Strong review presence on site")
            points += 3
        elif review_mentions > 0:
            findings.append("⚠️ Some review mentions")
            points += 1
        else:
            recommendations.append("Display Google reviews prominently on site")
            
        # Review schema
        has_review_schema = any('aggregateRating' in str(s) or 'Review' in str(s) for s in self.schema_data)
        if has_review_schema:
            findings.append("✅ Review schema markup present")
            points += 3
        else:
            findings.append("❌ No review schema")
            recommendations.append("Add AggregateRating schema for star ratings in search")
            
        # Star rating display
        star_patterns = ['★', '⭐', 'stars', 'rating']
        if any(p in text for p in star_patterns):
            findings.append("✅ Star ratings displayed")
            points += 2
            
        findings.append("ℹ️ Actual review metrics require Google API:")
        findings.append("  → Target: 50+ reviews")
        findings.append("  → Target: 4.5+ star average")
        findings.append("  → Target: Reviews within last 30 days")
        
        recommendations.append("Launch review generation campaign")
        recommendations.append("Respond to ALL reviews within 24 hours")
        recommendations.append("Ask satisfied clients for reviews via email/text")
        recommendations.append("Add review links to email signature")
        
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_local_content(self) -> CategoryScore:
        """Local content"""
        score = CategoryScore(name="Local Content")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if not self.soup:
            score.findings = ["❌ Could not analyze page"]
            return score
            
        # Blog check
        nav_links = [a.get_text().lower() for a in self.soup.find_all('a', href=True)]
        nav_hrefs = [a['href'].lower() for a in self.soup.find_all('a', href=True)]
        
        has_blog = any('blog' in link or 'news' in link or 'article' in link 
                       for link in nav_links + nav_hrefs)
        
        if has_blog:
            findings.append("✅ Blog/news section present")
            points += 3
        else:
            findings.append("❌ No blog section")
            recommendations.append("Start a blog with local legal content")
            
        # Resources section
        has_resources = any('resource' in link or 'guide' in link or 'faq' in link
                           for link in nav_links + nav_hrefs)
        if has_resources:
            findings.append("✅ Resources/guides section present")
            points += 2
            
        # Local content indicators
        text = self.soup.get_text().lower()
        
        local_content_patterns = [
            ('community', 'community involvement'),
            ('sponsor', 'sponsorships'),
            ('volunteer', 'volunteer work'),
            ('charity', 'charitable activities'),
            ('local event', 'local events'),
            ('local news', 'local news'),
        ]
        
        found_local = []
        for pattern, name in local_content_patterns:
            if pattern in text:
                found_local.append(name)
                
        if found_local:
            findings.append(f"✅ Local involvement: {', '.join(found_local)}")
            points += 2
            details['local_involvement'] = found_local
        else:
            recommendations.append("Highlight community involvement and local activities")
            
        # Practice area pages
        practice_areas = ['car accident', 'truck accident', 'motorcycle', 'slip and fall', 
                         'wrongful death', 'personal injury', 'medical malpractice']
        pa_pages = sum(1 for pa in practice_areas if pa in ' '.join(nav_links + nav_hrefs))
        
        if pa_pages >= 3:
            findings.append(f"✅ Multiple practice area pages ({pa_pages})")
            points += 2
        elif pa_pages > 0:
            findings.append(f"⚠️ {pa_pages} practice area page(s)")
            points += 1
        else:
            recommendations.append("Create dedicated pages for each practice area")
            
        score.score = min(points, 10)
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score
        
    def check_local_links(self) -> CategoryScore:
        """Local link building"""
        score = CategoryScore(name="Local Link Building")
        findings = []
        recommendations = []
        points = 0
        details = {}
        
        if self.soup:
            text = self.soup.get_text().lower()
            
            # Partnership mentions
            partnership_patterns = ['partner', 'sponsor', 'affiliate', 'member of', 'association']
            found_partnerships = sum(1 for p in partnership_patterns if p in text)
            
            if found_partnerships >= 2:
                findings.append("✅ Partnership/membership mentions found")
                points += 3
            elif found_partnerships > 0:
                findings.append("⚠️ Some partnership mentions")
                points += 1
                
        findings.append("ℹ️ Backlink analysis requires Ahrefs/Moz/SEMrush")
        
        recommendations.append("Get featured on local news sites")
        recommendations.append("Sponsor local events and charities")
        recommendations.append("Partner with complementary businesses (doctors, mechanics)")
        recommendations.append("Join local bar association and get listed")
        recommendations.append("Create linkable local resources (accident statistics, guides)")
        recommendations.append("Guest post on local blogs and news sites")
        
        score.score = min(points + 2, 10)  # Base points since we can't verify
        score.findings = findings
        score.recommendations = recommendations
        score.details = details
        return score

    def run_full_audit(self) -> AuditResult:
        """Run comprehensive audit"""
        result = AuditResult(url=self.url)
        
        # Fetch main page
        html, soup = self.fetch_page()
        if not html:
            result.ai_categories = [CategoryScore(name="Error", findings=["❌ Could not fetch website"])]
            return result
            
        # Extract business name
        if self.soup:
            title = self.soup.find('title')
            if title:
                result.business_name = title.get_text().split('|')[0].split('-')[0].strip()
                
        # Extract schemas first (used by multiple checks)
        self.extract_all_schema()
        
        # AI Visibility Checks
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
        
        # Local SEO Checks
        result.local_categories = [
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
        
        # Calculate scores
        result.ai_visibility_score = sum(c.score for c in result.ai_categories)
        result.local_seo_score = sum(c.score for c in result.local_categories)
        result.total_score = result.ai_visibility_score + result.local_seo_score
        
        # Grade
        if result.total_score >= 160:
            result.grade = "A"
        elif result.total_score >= 140:
            result.grade = "B+"
        elif result.total_score >= 120:
            result.grade = "B"
        elif result.total_score >= 100:
            result.grade = "C+"
        elif result.total_score >= 80:
            result.grade = "C"
        elif result.total_score >= 60:
            result.grade = "D"
        else:
            result.grade = "F"
            
        # Quick wins (highest impact from lowest scoring categories)
        all_cats = result.ai_categories + result.local_categories
        sorted_cats = sorted(all_cats, key=lambda c: c.score)
        
        result.quick_wins = []
        for cat in sorted_cats[:6]:
            if cat.recommendations:
                result.quick_wins.append(f"[{cat.name}] {cat.recommendations[0]}")
                
        # Priority fixes
        result.priority_fixes = [
            f"{cat.name}: {cat.score}/10"
            for cat in all_cats if cat.score < 5
        ]
        
        return result


def main():
    """Test enhanced analyzer"""
    import sys
    
    url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com"
    
    print(f"\n🔍 Enhanced Analysis: {url}\n")
    print("=" * 60)
    
    analyzer = EnhancedWebsiteAnalyzer(url)
    result = analyzer.run_full_audit()
    
    print(f"\n📊 OVERALL GRADE: {result.grade}")
    print(f"   Business: {result.business_name}")
    print(f"   AI Visibility: {result.ai_visibility_score}/100")
    print(f"   Local SEO: {result.local_seo_score}/100")
    print(f"   TOTAL: {result.total_score}/200")
    
    print(f"\n🤖 AI VISIBILITY ({result.ai_visibility_score}/100)")
    print("-" * 40)
    for cat in result.ai_categories:
        bar = "█" * cat.score + "░" * (10 - cat.score)
        print(f"  {cat.name}: {bar} {cat.score}/10")
        
    print(f"\n📍 LOCAL SEO ({result.local_seo_score}/100)")
    print("-" * 40)
    for cat in result.local_categories:
        bar = "█" * cat.score + "░" * (10 - cat.score)
        print(f"  {cat.name}: {bar} {cat.score}/10")
        
    print(f"\n⚡ TOP QUICK WINS")
    print("-" * 40)
    for qw in result.quick_wins[:5]:
        print(f"  → {qw}")
        
    if result.priority_fixes:
        print(f"\n🚨 PRIORITY FIXES (Below 50%)")
        print("-" * 40)
        for pf in result.priority_fixes[:5]:
            print(f"  ⚠️ {pf}")


if __name__ == "__main__":
    main()
