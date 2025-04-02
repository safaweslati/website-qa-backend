# app/services/analyzer.py
from crewai import Crew, Process
import logging
from fastapi import HTTPException
from app.core.webpage_fetcher import WebpageFetcher
from app.agents.ux_agent import UXAgent
from app.agents.seo_agent import SEOAgent
from app.agents.html_agent import HTMLStructureAgent
from app.agents.accessibility_agent import AccessibilityAgent
from app.core.models import WebsiteAnalysisResponse
from app.core.utils import AnalysisUtils

logger = logging.getLogger(__name__)

class WebsiteAnalyzer:
    @staticmethod
    def analyze(url: str) -> WebsiteAnalysisResponse:
        try:
            soup = WebpageFetcher.fetch(url)
            if not soup:
                raise HTTPException(status_code=400, detail="Failed to fetch webpage")

            html_content = str(soup)
            metadata = WebpageFetcher.extract_metadata(html_content)
            
            # Create agents and tasks
            agents_tasks = [
                (UXAgent, "ux_analysis"),
                (SEOAgent, "seo_analysis"),
                (HTMLStructureAgent, "html_analysis"),
                (AccessibilityAgent, "accessibility_analysis")
            ]

            crew_tasks = []
            results = {}
            
            for agent_class, result_key in agents_tasks:
                agent = agent_class.create()
                task = agent_class.create_task(agent, url, html_content, metadata)
                crew_tasks.append((agent, task, result_key))

            crew = Crew(
                agents=[a for a, _, _ in crew_tasks],
                tasks=[t for _, t, _ in crew_tasks],
                verbose=True,
                process=Process.sequential,
            )

            try:
                crew.kickoff()
                
                # Process results
                for _, task, result_key in crew_tasks:
                    results[result_key] = AnalysisUtils.parse_agent_output(str(task.output))
                
                return WebsiteAnalyzer._build_response(url, results)
                
            except Exception as e:
                logger.error(f"Crew execution failed: {str(e)}")
                raise HTTPException(status_code=500, detail="Analysis failed")

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Analysis error: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    def _build_response(url: str, results: dict) -> WebsiteAnalysisResponse:
        """Convert parsed results to response model"""
        return WebsiteAnalysisResponse(
            url=url,
            ux_analysis=results.get('ux_analysis'),
            seo_analysis=results.get('seo_analysis'),
            html_analysis=results.get('html_analysis'),
            accessibility_analysis=results.get('accessibility_analysis')
        )