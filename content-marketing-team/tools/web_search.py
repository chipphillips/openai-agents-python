import aiohttp
import asyncio
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import json
from datetime import datetime

class WebSearchTool:
    def __init__(self, max_results: int = 5, timeout: int = 30):
        self.max_results = max_results
        self.timeout = timeout
        self.search_engines = {
            "google": "https://www.google.com/search?q={}",
            "bing": "https://www.bing.com/search?q={}"
        }

    async def search(self, query: str, engine: str = "google") -> List[Dict]:
        """
        Perform a web search and return structured results.
        
        Args:
            query: The search query
            engine: The search engine to use ("google" or "bing")
            
        Returns:
            List of dictionaries containing search results
        """
        if engine not in self.search_engines:
            raise ValueError(f"Unsupported search engine: {engine}")

        url = self.search_engines[engine].format(query)
        results = []

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract search results (simplified example)
                        for result in soup.select('div.g')[:self.max_results]:
                            title_elem = result.select_one('h3')
                            link_elem = result.select_one('a')
                            snippet_elem = result.select_one('div.VwiC3b')
                            
                            if title_elem and link_elem:
                                results.append({
                                    'title': title_elem.get_text(),
                                    'url': link_elem.get('href'),
                                    'snippet': snippet_elem.get_text() if snippet_elem else '',
                                    'timestamp': datetime.now().isoformat()
                                })
        
        except Exception as e:
            print(f"Error during web search: {str(e)}")
            return []

        return results

    async def analyze_content(self, url: str) -> Dict:
        """
        Analyze content from a specific URL.
        
        Args:
            url: The URL to analyze
            
        Returns:
            Dictionary containing content analysis
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract main content
                        content = soup.get_text()
                        
                        # Basic content analysis
                        return {
                            'title': soup.title.string if soup.title else '',
                            'word_count': len(content.split()),
                            'has_images': bool(soup.find_all('img')),
                            'has_links': bool(soup.find_all('a')),
                            'timestamp': datetime.now().isoformat()
                        }
        
        except Exception as e:
            print(f"Error analyzing content: {str(e)}")
            return {}

    async def get_trending_topics(self, platform: str) -> List[Dict]:
        """
        Get trending topics for a specific platform.
        
        Args:
            platform: The social media platform
            
        Returns:
            List of dictionaries containing trending topics
        """
        # This is a placeholder implementation
        # In a real implementation, you would integrate with platform APIs
        trending_urls = {
            "x": "https://twitter.com/trends",
            "linkedin": "https://www.linkedin.com/trends"
        }
        
        if platform not in trending_urls:
            raise ValueError(f"Unsupported platform: {platform}")
            
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(trending_urls[platform], timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract trending topics (simplified example)
                        topics = []
                        for topic in soup.select('.trending-topic')[:10]:
                            topics.append({
                                'topic': topic.get_text(),
                                'timestamp': datetime.now().isoformat()
                            })
                        
                        return topics
        
        except Exception as e:
            print(f"Error getting trending topics: {str(e)}")
            return []

    async def get_competitor_content(self, competitor_url: str) -> Dict:
        """
        Analyze competitor content.
        
        Args:
            competitor_url: The competitor's website URL
            
        Returns:
            Dictionary containing competitor analysis
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(competitor_url, timeout=self.timeout) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extract social media links
                        social_links = {}
                        for link in soup.find_all('a', href=True):
                            href = link['href']
                            if 'twitter.com' in href:
                                social_links['twitter'] = href
                            elif 'linkedin.com' in href:
                                social_links['linkedin'] = href
                            elif 'instagram.com' in href:
                                social_links['instagram'] = href
                        
                        return {
                            'social_links': social_links,
                            'has_blog': bool(soup.find_all('article')),
                            'has_newsletter': bool(soup.find_all('form')),
                            'timestamp': datetime.now().isoformat()
                        }
        
        except Exception as e:
            print(f"Error analyzing competitor: {str(e)}")
            return {} 