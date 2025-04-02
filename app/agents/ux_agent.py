from crewai import Task
from app.agents.base_agent import AgentFactory
import logging
from app.core.utils import AnalysisUtils

logger = logging.getLogger(__name__)

class UXAgent:
    @staticmethod
    def create():
        """
        Create the UX analyst agent
        """
        return AgentFactory.create_agent(
            role="UX Analyst",
            goal="Evaluate website user experience and provide actionable recommendations",
            backstory="You are an expert UX analyst with 10+ years of experience in usability testing and interface design. You've worked with major tech companies and e-commerce platforms to optimize their user experiences.",
        )
        
    @staticmethod
    def create_task(agent, url, html_content, metadata):
        """
        Create a UX analysis task
        
        Args:
            agent: The UX agent
            url: Website URL
            html_content: HTML content
            metadata: Extracted metadata
            
        Returns:
            CrewAI Task
        """
        return Task(
            description=f"""
            Analyze the UX of the webpage at {url}.
            
            HTML Content Preview (first 5000 chars):
            {html_content[:5000]}
            
            Metadata:
            Title: {metadata.get('title')}
            Description: {metadata.get('description')}
            Has Viewport Meta: {metadata.get('has_viewport_meta')}
            Navigation Elements: {metadata.get('nav_elements', 'Unknown')}
            CTAs: {metadata.get('cta_elements', 'Unknown')}
            Form Elements: {metadata.get('form_elements', 'Unknown')}
            
            Evaluate the following aspects:
            1. Navigation and information architecture
            2. Content readability and organization
            3. Visual hierarchy indicators
            4. Responsiveness and mobile-friendliness indicators
            5. Call-to-action effectiveness
            6. User flow and journey obstructions
            7. Form usability (from UX perspective only)
            8. Page load indicators (visible in HTML)

            Focus STRICTLY on user experience factors that affect how users interact with the site.
            
            IMPORTANT: You MUST provide a complete, valid JSON response following the exact structure specified in the expected output.
            Keep your descriptions concise  and limit to 3-5 most important issues.
            """,
            agent=agent,
            expected_output=AnalysisUtils.get_expected_output()
        )