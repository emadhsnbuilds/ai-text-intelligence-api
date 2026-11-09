from anthropic import Anthropic

from .settings import settings


client = Anthropic(
    api_key=settings.anthropic_api_key,
)
