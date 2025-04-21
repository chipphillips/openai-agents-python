import asyncio
from typing import Dict, List, Optional
import yaml
import os
from datetime import datetime
import json
from ..tools.web_search import WebSearchTool
from ..tools.content_analysis import ContentAnalysisTool

class ContentDirector:
    def __init__(self, config_path: str = "config/agent_config.yaml"):
        """
        Initialize the Content Director with configuration and tools.
        
        Args:
            config_path: Path to the agent configuration file
        """
        self.config = self._load_config(config_path)
        self.web_search = WebSearchTool()
        self.content_analysis = ContentAnalysisTool()
        self.output_dir = self.config['global']['output_dir']
        self._ensure_output_dir()

    def _load_config(self, config_path: str) -> Dict:
        """
        Load agent configuration from YAML file.
        """
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            return {}

    def _ensure_output_dir(self):
        """
        Ensure the output directory exists.
        """
        os.makedirs(self.output_dir, exist_ok=True)

    async def create_content(
        self,
        topic: str,
        platforms: List[str],
        tone: str = "professional",
        target_audience: str = "general",
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Create content for specified platforms.
        
        Args:
            topic: The main topic or subject
            platforms: List of platforms to create content for
            tone: The desired tone of the content
            target_audience: The target audience
            keywords: Optional list of keywords to include
            
        Returns:
            Dictionary containing created content and metadata
        """
        # Create a unique directory for this content creation task
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        task_dir = os.path.join(self.output_dir, f"content_{timestamp}")
        os.makedirs(task_dir, exist_ok=True)

        # Initialize results dictionary
        results = {
            'topic': topic,
            'platforms': platforms,
            'tone': tone,
            'target_audience': target_audience,
            'keywords': keywords or [],
            'created_at': timestamp,
            'content': {},
            'metadata': {}
        }

        # Research phase
        research_results = await self._conduct_research(topic, keywords)
        results['metadata']['research'] = research_results

        # Content creation phase
        for platform in platforms:
            platform_content = await self._create_platform_content(
                topic=topic,
                platform=platform,
                tone=tone,
                target_audience=target_audience,
                research=research_results
            )
            
            # Save platform-specific content
            filename = f"{platform}-content.md"
            filepath = os.path.join(task_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(platform_content['content'])
            
            # Store content and analysis in results
            results['content'][platform] = platform_content['content']
            results['metadata'][platform] = platform_content['analysis']

        # Save complete results
        results_file = os.path.join(task_dir, "metadata.json")
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)

        return results

    async def _conduct_research(
        self,
        topic: str,
        keywords: Optional[List[str]] = None
    ) -> Dict:
        """
        Conduct research on the topic.
        """
        research_results = {
            'topic_research': [],
            'trending_topics': {},
            'competitor_analysis': []
        }

        # Search for topic information
        search_query = f"{topic} {' '.join(keywords) if keywords else ''}"
        search_results = await self.web_search.search(search_query)
        research_results['topic_research'] = search_results

        # Get trending topics for each platform
        for platform in ['x', 'linkedin']:
            trending = await self.web_search.get_trending_topics(platform)
            research_results['trending_topics'][platform] = trending

        return research_results

    async def _create_platform_content(
        self,
        topic: str,
        platform: str,
        tone: str,
        target_audience: str,
        research: Dict
    ) -> Dict:
        """
        Create content for a specific platform.
        """
        # Get platform-specific instructions
        platform_config = self.config['platform_agents'].get(platform, {})
        instructions = platform_config.get('instructions', '')

        # Create content using the platform-specific agent
        content = await self._generate_content(
            topic=topic,
            platform=platform,
            tone=tone,
            target_audience=target_audience,
            research=research,
            instructions=instructions
        )

        # Analyze the content
        analysis = self.content_analysis.analyze_content(content, platform)

        return {
            'content': content,
            'analysis': analysis
        }

    async def _generate_content(
        self,
        topic: str,
        platform: str,
        tone: str,
        target_audience: str,
        research: Dict,
        instructions: str
    ) -> str:
        """
        Generate content using the platform-specific agent.
        """
        # This is a placeholder implementation
        # In a real implementation, you would use the OpenAI API to generate content
        # based on the provided parameters and research
        
        # For now, we'll create a simple template
        content = f"""# {topic}

Based on our research and analysis, here's content optimized for {platform}:

{research['topic_research'][0]['snippet'] if research['topic_research'] else 'Content placeholder'}

Target Audience: {target_audience}
Tone: {tone}

Platform-specific optimizations:
- Character count: {280 if platform == 'x' else 'No limit'}
- Hashtags: {', '.join(research['trending_topics'][platform][:3]) if platform in research['trending_topics'] else 'None specified'}
"""

        return content

    async def review_content(self, content_id: str) -> Dict:
        """
        Review and provide feedback on created content.
        """
        # Load content and metadata
        content_dir = os.path.join(self.output_dir, f"content_{content_id}")
        metadata_file = os.path.join(content_dir, "metadata.json")
        
        try:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
        except Exception as e:
            print(f"Error loading content metadata: {str(e)}")
            return {}

        review_results = {
            'content_id': content_id,
            'review_date': datetime.now().isoformat(),
            'platform_reviews': {}
        }

        # Review content for each platform
        for platform, content in metadata['content'].items():
            analysis = self.content_analysis.analyze_content(content, platform)
            seo_suggestions = self.content_analysis.generate_seo_suggestions(content)
            
            review_results['platform_reviews'][platform] = {
                'analysis': analysis,
                'seo_suggestions': seo_suggestions,
                'recommendations': self._generate_recommendations(analysis, platform)
            }

        # Save review results
        review_file = os.path.join(content_dir, "review_results.json")
        with open(review_file, 'w', encoding='utf-8') as f:
            json.dump(review_results, f, indent=2)

        return review_results

    def _generate_recommendations(self, analysis: Dict, platform: str) -> List[str]:
        """
        Generate recommendations based on content analysis.
        """
        recommendations = []

        # Check readability
        if analysis['readability']['flesch_reading_ease'] < 60:
            recommendations.append("Content might be too complex for the target audience")

        # Check engagement potential
        engagement = analysis['engagement_potential']
        if not engagement['metrics']['has_questions']:
            recommendations.append("Consider adding questions to increase engagement")
        if not engagement['metrics']['has_hashtags']:
            recommendations.append("Add relevant hashtags to increase visibility")

        # Platform-specific recommendations
        if platform == 'x':
            if engagement['metrics']['word_count'] > 280:
                recommendations.append("Content exceeds X character limit")
        elif platform == 'linkedin':
            if engagement['metrics']['word_count'] < 100:
                recommendations.append("Content might be too short for LinkedIn")

        return recommendations 