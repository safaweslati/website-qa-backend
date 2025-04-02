from crewai import Task
from app.agents.base_agent import AgentFactory
import logging
from app.core.utils import AnalysisUtils

logger = logging.getLogger(__name__)

class AccessibilityAgent:
    @staticmethod
    def create():
        """
        Create the accessibility specialist agent
        """
        return AgentFactory.create_agent(
            role="Accessibility Specialist",
            goal="Evaluate website accessibility compliance with WCAG standards",
            backstory="You are an accessibility consultant helping organizations make their digital content accessible to all users, including those with disabilities. You have expertise in WCAG 2.1 guidelines.",
        )
        
    @staticmethod
    def create_task(agent, url, html_content, metadata):
        """
        Create an accessibility analysis task
        
        Args:
            agent: The accessibility agent
            url: Website URL
            html_content: HTML content
            metadata: Extracted metadata
            
        Returns:
            CrewAI Task
        """
        return Task(
            description=f"""
            Analyze the accessibility of the webpage at {url}.
            
            HTML Content Preview (first 5000 chars):
            {html_content[:5000]}
            
            Metadata:
            Images without alt text: {metadata.get('images_without_alt', 'Unknown')}
            Form inputs without labels: {metadata.get('inputs_without_labels', 'Unknown')}
            
            Evaluate the following aspects according to WCAG 2.1:
            1. Alternative text for images and non-text content
            2. Keyboard navigability indicators (focus states, tabindex)
            3. ARIA attributes and roles
            4. Form accessibility (labels, error messages)
            5. Color and contrast issues (where detectable in code)
            6. Skip navigation links
            7. Language declaration
            
            
            Focus STRICTLY on accessibility concerns for users with disabilities.
            
            IMPORTANT: You MUST provide a complete, valid JSON response following the exact structure specified in the expected output.
            Keep your descriptions concise and limit to 3-5 most important issues.
            """,
            agent=agent,
            expected_output=AnalysisUtils.get_expected_output()
        )