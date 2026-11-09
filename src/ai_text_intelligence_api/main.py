import logging

from anthropic import APIError
from fastapi import FastAPI, HTTPException

from .analysis_service import analyze_text
from .schemas import AnalysisResponse, TextRequest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI Text Intelligence API",
    description="An API for analyzing text using AI.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_endpoint(request: TextRequest):
    try:
        return analyze_text(request.text)

    except APIError as exc:
        logger.exception("Anthropic API request failed")

        raise HTTPException(
            status_code=502,
            detail="The AI analysis provider is temporarily unavailable.",
        ) from exc