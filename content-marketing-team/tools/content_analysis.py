from typing import Dict, List, Optional
import re
from collections import Counter
import json
from datetime import datetime

class ContentAnalysisTool:
    def __init__(self):
        self.readability_scores = {
            'flesch_kincaid': self._calculate_flesch_kincaid,
            'flesch_reading_ease': self._calculate_flesch_reading_ease
        }

    def analyze_content(self, content: str, platform: str) -> Dict:
        """
        Analyze content for various metrics.
        
        Args:
            content: The content to analyze
            platform: The platform the content is intended for
            
        Returns:
            Dictionary containing content analysis metrics
        """
        return {
            'readability': self._analyze_readability(content),
            'sentiment': self._analyze_sentiment(content),
            'keyword_density': self._analyze_keyword_density(content),
            'engagement_potential': self._analyze_engagement_potential(content, platform),
            'hashtag_analysis': self._analyze_hashtags(content),
            'timestamp': datetime.now().isoformat()
        }

    def _analyze_readability(self, content: str) -> Dict:
        """
        Calculate readability scores using various metrics.
        """
        scores = {}
        for metric, calculator in self.readability_scores.items():
            scores[metric] = calculator(content)
        return scores

    def _calculate_flesch_kincaid(self, content: str) -> float:
        """
        Calculate Flesch-Kincaid Grade Level.
        """
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        syllables = sum(self._count_syllables(word) for word in content.split())
        
        if sentences == 0:
            return 0.0
            
        return 0.39 * (words / sentences) + 11.8 * (syllables / words) - 15.59

    def _calculate_flesch_reading_ease(self, content: str) -> float:
        """
        Calculate Flesch Reading Ease score.
        """
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        syllables = sum(self._count_syllables(word) for word in content.split())
        
        if sentences == 0:
            return 0.0
            
        return 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)

    def _count_syllables(self, word: str) -> int:
        """
        Count syllables in a word.
        """
        word = word.lower()
        count = 0
        vowels = "aeiouy"
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                count += 1
            previous_was_vowel = is_vowel
            
        if word.endswith('e'):
            count -= 1
        if count == 0:
            count = 1
            
        return count

    def _analyze_sentiment(self, content: str) -> Dict:
        """
        Analyze sentiment of the content.
        """
        # Simple sentiment analysis based on word lists
        positive_words = {'great', 'excellent', 'amazing', 'wonderful', 'good', 'best', 'love', 'happy'}
        negative_words = {'bad', 'terrible', 'awful', 'hate', 'worst', 'poor', 'sad', 'angry'}
        
        words = content.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            return {'score': 0, 'label': 'neutral'}
            
        score = (positive_count - negative_count) / total
        label = 'positive' if score > 0 else 'negative' if score < 0 else 'neutral'
        
        return {
            'score': score,
            'label': label,
            'positive_count': positive_count,
            'negative_count': negative_count
        }

    def _analyze_keyword_density(self, content: str) -> List[Dict]:
        """
        Analyze keyword density in the content.
        """
        words = content.lower().split()
        word_freq = Counter(words)
        total_words = len(words)
        
        # Filter out common words and short words
        common_words = {'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at'}
        keywords = {word: freq for word, freq in word_freq.items() 
                   if word not in common_words and len(word) > 3}
        
        # Calculate density and sort by frequency
        keyword_density = [
            {
                'word': word,
                'count': freq,
                'density': (freq / total_words) * 100
            }
            for word, freq in keywords.items()
        ]
        
        return sorted(keyword_density, key=lambda x: x['count'], reverse=True)[:10]

    def _analyze_engagement_potential(self, content: str, platform: str) -> Dict:
        """
        Analyze potential for engagement based on platform-specific metrics.
        """
        metrics = {
            'has_questions': bool(re.search(r'\?', content)),
            'has_hashtags': bool(re.search(r'#\w+', content)),
            'has_mentions': bool(re.search(r'@\w+', content)),
            'has_links': bool(re.search(r'https?://\S+', content)),
            'has_emojis': bool(re.search(r'[\U0001F300-\U0001F9FF]', content)),
            'word_count': len(content.split()),
            'sentence_count': len(re.split(r'[.!?]+', content))
        }
        
        # Platform-specific recommendations
        recommendations = []
        if platform == 'x':
            if metrics['word_count'] > 280:
                recommendations.append('Content exceeds X character limit')
            if not metrics['has_hashtags']:
                recommendations.append('Consider adding relevant hashtags')
        elif platform == 'linkedin':
            if metrics['word_count'] < 100:
                recommendations.append('Content might be too short for LinkedIn')
            if not metrics['has_links']:
                recommendations.append('Consider adding relevant links')
        
        return {
            'metrics': metrics,
            'recommendations': recommendations
        }

    def _analyze_hashtags(self, content: str) -> Dict:
        """
        Analyze hashtags in the content.
        """
        hashtags = re.findall(r'#\w+', content)
        return {
            'count': len(hashtags),
            'hashtags': hashtags,
            'unique_hashtags': list(set(hashtags))
        }

    def generate_seo_suggestions(self, content: str) -> List[str]:
        """
        Generate SEO suggestions for the content.
        """
        suggestions = []
        
        # Check title length
        title = content.split('\n')[0]
        if len(title) < 30 or len(title) > 60:
            suggestions.append('Title length should be between 30-60 characters')
        
        # Check keyword placement
        keywords = self._analyze_keyword_density(content)
        if not any(k['word'] in title.lower() for k in keywords[:3]):
            suggestions.append('Consider including main keywords in the title')
        
        # Check content length
        if len(content.split()) < 300:
            suggestions.append('Content might be too short for optimal SEO')
        
        # Check paragraph structure
        paragraphs = content.split('\n\n')
        if any(len(p.split()) > 150 for p in paragraphs):
            suggestions.append('Consider breaking up long paragraphs')
        
        return suggestions

    def analyze_competitor_content(self, content: str, competitor_content: str) -> Dict:
        """
        Compare content with competitor content.
        """
        return {
            'readability_comparison': {
                'content': self._analyze_readability(content),
                'competitor': self._analyze_readability(competitor_content)
            },
            'keyword_overlap': self._find_keyword_overlap(content, competitor_content),
            'unique_selling_points': self._identify_unique_points(content, competitor_content),
            'timestamp': datetime.now().isoformat()
        }

    def _find_keyword_overlap(self, content1: str, content2: str) -> List[str]:
        """
        Find overlapping keywords between two pieces of content.
        """
        keywords1 = {k['word'] for k in self._analyze_keyword_density(content1)}
        keywords2 = {k['word'] for k in self._analyze_keyword_density(content2)}
        return list(keywords1.intersection(keywords2))

    def _identify_unique_points(self, content1: str, content2: str) -> Dict:
        """
        Identify unique points in each piece of content.
        """
        # Simple implementation - could be enhanced with more sophisticated analysis
        sentences1 = set(re.split(r'[.!?]+', content1))
        sentences2 = set(re.split(r'[.!?]+', content2))
        
        return {
            'unique_to_content': list(sentences1 - sentences2),
            'unique_to_competitor': list(sentences2 - sentences1)
        } 