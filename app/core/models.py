# app/core/models.py
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, HttpUrl

class SeverityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class AnalysisIssue(BaseModel):
    severity: SeverityLevel
    description: str
    recommendation: str

class AnalysisResult(BaseModel):
    score: int = Field(..., ge=0, le=100)  # Score between 0-100
    issues: List[AnalysisIssue]
    summary: str

class WebsiteAnalysisRequest(BaseModel):
    url: HttpUrl

class WebsiteAnalysisResponse(BaseModel):
    url: str
    ux_analysis: AnalysisResult
    seo_analysis: AnalysisResult
    html_analysis: AnalysisResult
    accessibility_analysis: AnalysisResult