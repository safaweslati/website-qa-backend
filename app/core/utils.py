import json
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AnalysisUtils:
    @staticmethod
    def get_expected_output() -> str:
        """Standard expected output for all agents"""
        return """
            Your response MUST be a complete, valid JSON object with EXACTLY this structure:
            {
                "score": <integer_between_0_and_100>,
                "issues": [
                    {
                        "severity": "<low|medium|high>", # ONLY these values allowed
                        "description": "<concise_issue_description>",
                        "recommendation": "<concise_actionable_recommendation>"
                    }
                ],
                "summary": "<brief_summary_of_findings>"
            }

            Keep your JSON compact and valid. Ensure all strings are properly escaped.
            The entire JSON must be less than 2000 characters total.
            Ensure you complete the entire JSON object including the closing brace.
            """

    @staticmethod
    def parse_agent_output(output_str: str) -> Dict[str, Any]:
        """Robust parsing of agent output with multiple fallback strategies"""
        if not output_str:
            return {
                "score": 0,
                "issues": [],
                "summary": "Empty agent response"
            }

        # First try direct JSON parse
        try:
            parsed_json = json.loads(output_str)
            return AnalysisUtils._validate_json(parsed_json)
        except json.JSONDecodeError:
            pass

        # Try extracting JSON from markdown code block
        json_match = re.search(r'```json\n?(.*?)\n?```', output_str, re.DOTALL)
        if json_match:
            try:
                parsed_json = json.loads(json_match.group(1).strip())
                return AnalysisUtils._validate_json(parsed_json)
            except json.JSONDecodeError:
                pass

        # Try finding innermost JSON
        json_candidates = re.findall(r'\{.*?\}', output_str, re.DOTALL)
        for candidate in json_candidates[::-1]:  # Reverse to try the last one first
            try:
                parsed_json = json.loads(candidate)
                return AnalysisUtils._validate_json(parsed_json)
            except json.JSONDecodeError:
                continue

        # Fallback: Return error structure
        return {
            "score": 0,
            "issues": [
                {
                    "severity": "high",
                    "description": "Failed to parse agent output",
                    "recommendation": "Check agent response format"
                }
            ],
            "summary": "Output parsing failed"
        }

    @staticmethod
    def _validate_json(parsed_json: Dict[str, Any]) -> Dict[str, Any]:
        """Ensures the JSON structure is valid and fields contain expected values"""
        valid_severities = {"low", "medium", "high"}
        
        if not isinstance(parsed_json, dict):
            return {
                "score": 0,
                "issues": [{
                    "severity": "high",
                    "description": "Invalid JSON format",
                    "recommendation": "Ensure output follows expected JSON schema"
                }],
                "summary": "Invalid JSON structure"
            }
        
        if "issues" in parsed_json and isinstance(parsed_json["issues"], list):
            for issue in parsed_json["issues"]:
                if issue.get("severity") not in valid_severities:
                    issue["severity"] = "medium"  # Default to medium if invalid
        
        return parsed_json
