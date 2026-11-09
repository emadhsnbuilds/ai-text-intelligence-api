from .anthropic_client import client
from .prompts import ANALYSIS_SYSTEM_PROMPT
from .schemas import AnalysisResponse
from .settings import settings


def analyze_text(text: str) -> AnalysisResponse:
    response = client.messages.parse(
        model=settings.anthropic_model,
        max_tokens=2048,
        system=ANALYSIS_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        output_format=AnalysisResponse,
    )

    return response.parsed_output