from crewai import Task
from app.agents.base_agent import AgentFactory
import logging
from app.core.utils import AnalysisUtils

logger = logging.getLogger(__name__)

class HTMLStructureAgent:
    @staticmethod
    def create():
        """
        Create the HTML structure analyzer agent
        """
        return AgentFactory.create_agent(
            role="HTML Structure Analyst",
            goal="Identify HTML structure issues, validate HTML quality and identify code-level problems",
            backstory="You are an experienced front-end developer specializing in HTML validation and clean code practices. You focus on ensuring HTML documents are properly structured and follow best practices.",
        )
        
    @staticmethod
    def create_task(agent, url, html_content, metadata):
        """
        Create an HTML structure analysis task
        
        Args:
            agent: The HTML structure agent
            url: Website URL
            html_content: HTML content
            metadata: Extracted metadata
            
        Returns:
            CrewAI Task
        """
        return Task(
            description=f"""
            Analyze the HTML structure of the webpage at {url}.
            
            HTML Content Preview (first 5000 chars):
            {html_content[:5000]}
            
            Evaluate the following aspects:
            1. HTML validation (unclosed tags, improperly nested elements)
            2. Proper document structure (doctype, head, body)
            3. Script and style placement (proper loading strategy)
            4. HTML5 compliance
            5. Deprecated element usage
            6. Code duplication issues
            7. Unnecessary div nesting ("div soup")
            8. HTML comments that may expose sensitive information
            
            
            Focus STRICTLY on HTML code quality and structure issues.
            
            IMPORTANT: You MUST provide a complete, valid JSON response following the exact structure specified in the expected output.
            Keep your descriptions concise and limit to 3-5 most important issues.
            """,
            agent=agent,
            expected_output=AnalysisUtils.get_expected_output()
        )