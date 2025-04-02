from crewai import Task
from app.agents.base_agent import AgentFactory
import logging
from app.core.utils import AnalysisUtils

logger = logging.getLogger(__name__)

class SEOAgent:
    @staticmethod
    def create():
        """
        Create the SEO expert agent
        """
        return AgentFactory.create_agent(
            role="SEO Expert",
            goal="Analyze webpage SEO and provide optimization recommendations",
            backstory="You are a leading SEO specialist who has helped numerous websites achieve top rankings. You have deep knowledge of search engine algorithms and optimization techniques.",
        )
        
    @staticmethod
    def create_task(agent, url, html_content, metadata):
        """
        Create an SEO analysis task
        
        Args:
            agent: The SEO agent
            url: Website URL
            html_content: HTML content
            metadata: Extracted metadata
            
        Returns:
            CrewAI Task
        """
        return Task(
            description=f"""
            Analyze the SEO of the webpage at {url}.
            
            HTML Content Preview (first 5000 chars):
            {html_content[:5000]}
            
            Metadata:
            Title: {metadata.get('title')}
            Description: {metadata.get('description')}
            H1 Count: {metadata.get('h1_count')}
            Image Count: {metadata.get('image_count')}
            Links Count: {metadata.get('links_count')}
            Has Canonical URL: {metadata.get('has_canonical', 'Unknown')}
            
            Evaluate the following aspects:
            1. Meta tags (title, description, keywords, robots)
            2. URL structure and friendliness
            3. Canonical URL implementation
            4. Structured data/schema markup
            5. Content keyword optimization
            6. Internal linking structure and anchor text
            7. Heading structure (exclusively from SEO perspective)
            8. Open Graph and social media tags
            
            Focus STRICTLY on search engine optimization factors.
            
            IMPORTANT: You MUST provide a complete, valid JSON response following the exact structure specified in the expected output.
            Keep your descriptions concise  and limit to 3-5 most important issues.
            """,
            agent=agent,
            expected_output=AnalysisUtils.get_expected_output()
        )