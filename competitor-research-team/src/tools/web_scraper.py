"""
Web Scraping Tool for Constructiv AI Competitive Analysis

This module provides functions to extract structured information from competitor websites.
"""
import json
import os
from pathlib import Path
import re
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse

# Import configuration
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))
from config import RAW_DIR, PROCESSED_DIR, WEB_SCRAPING_CONFIG

class WebScraper:
    """Class for scraping competitor websites"""
    
    def __init__(self, url):
        """
        Initialize the web scraper with a URL
        
        Parameters:
        - url: Website URL to scrape
        """
        self.url = self._normalize_url(url)
        self.domain = self._extract_domain(self.url)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': WEB_SCRAPING_CONFIG.get('user_agent'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        self.timeout = WEB_SCRAPING_CONFIG.get('timeout', 30)
        self.max_retries = WEB_SCRAPING_CONFIG.get('max_retries', 3)
        
        # Initialize data structure
        self.data = {
            "company_name": "",
            "domain": self.domain,
            "homepage_url": self.url,
            "meta_description": "",
            "meta_keywords": "",
            "homepage_content": "",
            "about_page": {
                "url": "",
                "content": ""
            },
            "product_pages": [],
            "team_page": {
                "url": "",
                "content": ""
            },
            "contact_info": {
                "email": "",
                "phone": "",
                "address": ""
            },
            "social_media": {},
            "technologies": []
        }
    
    def _normalize_url(self, url):
        """Normalize URL format"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')
    
    def _extract_domain(self, url):
        """Extract domain from URL"""
        parsed_url = urllib.parse.urlparse(url)
        return parsed_url.netloc
    
    def _make_request(self, url):
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(url, timeout=self.timeout)
                response.raise_for_status()
                return response
            except requests.exceptions.RequestException as e:
                print(f"Request failed (attempt {attempt+1}/{self.max_retries}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return None
    
    def _extract_page_content(self, url):
        """Extract main content from a page"""
        response = self._make_request(url)
        if not response:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style', 'iframe', 'nav', 'footer']):
            element.decompose()
        
        # Try to find main content
        main_content = soup.find('main') or soup.find(id='main') or soup.find(id='content') or soup.find('article')
        
        if main_content:
            text = main_content.get_text(separator=' ', strip=True)
        else:
            # Fallback to the body
            text = soup.body.get_text(separator=' ', strip=True)
        
        # Clean up the text
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def scrape_homepage(self):
        """Scrape the homepage"""
        response = self._make_request(self.url)
        if not response:
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract meta information
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            self.data["meta_description"] = meta_desc.get('content', '')
        
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            self.data["meta_keywords"] = meta_keywords.get('content', '')
        
        # Try to extract company name
        title = soup.find('title')
        if title:
            self.data["company_name"] = title.text.split('|')[0].split('-')[0].strip()
        
        # Get homepage content
        self.data["homepage_content"] = self._extract_page_content(self.url)
        
        # Find important links
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.text.lower().strip()
            
            # Make absolute URL
            if not href.startswith(('http://', 'https://')):
                href = urllib.parse.urljoin(self.url, href)
            
            # Only include links from the same domain
            if self.domain not in href:
                continue
            
            # Find about page
            if any(keyword in text for keyword in ['about', 'about us', 'company', 'who we are']) and not self.data["about_page"]["url"]:
                self.data["about_page"]["url"] = href
            
            # Find team/leadership page
            if any(keyword in text for keyword in ['team', 'leadership', 'management', 'people']) and not self.data["team_page"]["url"]:
                self.data["team_page"]["url"] = href
            
            # Find product pages
            if any(keyword in text for keyword in ['product', 'solution', 'service', 'platform', 'software']):
                if href not in [p["url"] for p in self.data["product_pages"]]:
                    self.data["product_pages"].append({
                        "url": href,
                        "title": text,
                        "content": ""
                    })
        
        # Extract social media links
        social_patterns = {
            'linkedin': r'linkedin\.com',
            'twitter': r'twitter\.com|x\.com',
            'facebook': r'facebook\.com',
            'instagram': r'instagram\.com',
            'youtube': r'youtube\.com'
        }
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            for platform, pattern in social_patterns.items():
                if re.search(pattern, href):
                    self.data["social_media"][platform] = href
        
        # Extract contact information
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', soup.get_text())
        if emails:
            self.data["contact_info"]["email"] = emails[0]
        
        phone_pattern = re.compile(r'(?:\+\d{1,2}\s*)?(?:\(\d{3}\)|\d{3})[-.\s]?\d{3}[-.\s]?\d{4}')
        phones = phone_pattern.findall(soup.get_text())
        if phones:
            self.data["contact_info"]["phone"] = phones[0]
        
        return True
    
    def scrape_about_page(self):
        """Scrape the about page"""
        if not self.data["about_page"]["url"]:
            return False
        
        self.data["about_page"]["content"] = self._extract_page_content(self.data["about_page"]["url"])
        return True
    
    def scrape_team_page(self):
        """Scrape the team/leadership page"""
        if not self.data["team_page"]["url"]:
            return False
        
        self.data["team_page"]["content"] = self._extract_page_content(self.data["team_page"]["url"])
        return True
    
    def scrape_product_pages(self, max_pages=3):
        """Scrape product pages"""
        if not self.data["product_pages"]:
            return False
        
        # Limit the number of product pages to scrape
        for i, product in enumerate(self.data["product_pages"][:max_pages]):
            product["content"] = self._extract_page_content(product["url"])
            # Avoid overloading the server
            if i < len(self.data["product_pages"]) - 1:
                time.sleep(1)
        
        return True
    
    def detect_technologies(self):
        """Attempt to detect technologies used on the website"""
        response = self._make_request(self.url)
        if not response:
            return False
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Technology patterns to look for in HTML
        tech_patterns = {
            'React': [r'react', r'reactjs', r'react-dom'],
            'Angular': [r'angular', r'ng-'],
            'Vue': [r'vue', r'vuejs'],
            'WordPress': [r'wp-content', r'wp-includes'],
            'Bootstrap': [r'bootstrap'],
            'jQuery': [r'jquery'],
            'Shopify': [r'shopify'],
            'Google Analytics': [r'google-analytics', r'gtag', r'ga'],
            'Google Tag Manager': [r'gtm'],
            'Hubspot': [r'hubspot'],
            'Salesforce': [r'salesforce'],
            'Marketo': [r'marketo'],
            'Cloudflare': [r'cloudflare'],
            'AWS': [r'amazonaws', r'aws'],
            'Azure': [r'azure'],
            'Google Cloud': [r'googlecloud', r'gcloud']
        }
        
        # Check in scripts
        scripts = soup.find_all('script', src=True)
        scripts_text = ' '.join([script.get('src', '') for script in scripts])
        
        # Check in HTML
        html_text = str(soup)
        
        for tech, patterns in tech_patterns.items():
            for pattern in patterns:
                if re.search(pattern, scripts_text, re.IGNORECASE) or re.search(pattern, html_text, re.IGNORECASE):
                    if tech not in self.data["technologies"]:
                        self.data["technologies"].append(tech)
        
        return True
    
    def scrape_all(self):
        """Scrape all available information"""
        self.scrape_homepage()
        self.scrape_about_page()
        self.scrape_team_page()
        self.scrape_product_pages()
        self.detect_technologies()
        
        return self.data
    
    def save_data(self, output_path=None):
        """
        Save the scraped data to a JSON file
        
        Parameters:
        - output_path: Path to save the JSON file (optional)
        """
        if not output_path:
            # Create output path in raw directory
            company_name = self.data["company_name"]
            if not company_name:
                company_name = self.domain
            
            # Sanitize filename
            company_name = re.sub(r'[^\w\-\. ]', '_', company_name)
            output_dir = RAW_DIR / "competitors" / "primary" / company_name / "web_data"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"{self.domain}_scraped.json"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
        
        return output_path

def scrape_competitor_website(url, output_path=None):
    """
    Extract basic information from a competitor website.
    
    Parameters:
    - url: Website URL to scrape
    - output_path: Optional path to save the scraped data
    
    Returns:
    - Dictionary with key website information
    """
    scraper = WebScraper(url)
    data = scraper.scrape_all()
    
    if data and output_path:
        scraper.save_data(output_path)
    
    return data

if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python web_scraper.py <website_url> [output_path]")
        sys.exit(1)
    
    url = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    data = scrape_competitor_website(url, output_path)
    if data:
        print(f"Successfully scraped data from {url}")
        if output_path:
            print(f"Saved to {output_path}")
    else:
        print(f"Failed to scrape data from {url}") 