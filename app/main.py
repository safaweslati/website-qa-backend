from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.models import WebsiteAnalysisRequest, WebsiteAnalysisResponse
from app.services.analyzer import WebsiteAnalyzer
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="WebQA API",
    description="API for website quality analysis",
    version="1.0.0",
    docs_url="/docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post(
    "/analyze",
    response_model=WebsiteAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze website quality"
)
def analyze_website(request: WebsiteAnalysisRequest):
    """
    Analyze a webpage for:
    - UX
    - SEO 
    - HTML Structure
    - Accessibility
    """
    try:
        url = str(request.url)
        logger.info(f"Analyzing: {url}")
        return  WebsiteAnalyzer.analyze(url)
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Website analysis failed"
        )

@app.get("/test", tags=["Testing"])
async def test_endpoint():
    """
    Test endpoint to verify API is running
    Returns simple health check response
    """
    return {
        "status": "API is working",
        "version": "1.0.0",
        "health": "good"
    }

if __name__ == "__main__":
    # Run directly with hardcoded values
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )