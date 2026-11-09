
from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(
        min_length=1,
        description="The text to analyze.",
    )


class ActionItem(BaseModel):
    task: str
    owner: str | None = None
    deadline: str | None = None


class AnalysisResponse(BaseModel):
    summary: str
    key_points: list[str]
    action_items: list[ActionItem]
