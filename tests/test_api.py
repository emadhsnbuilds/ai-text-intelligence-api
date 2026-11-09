import ai_text_intelligence_api.main as main
from anthropic import APIError
import httpx
from fastapi.testclient import TestClient
from ai_text_intelligence_api.schemas import AnalysisResponse


client = TestClient(main.app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_analyze_success(monkeypatch):
    def mock_analyze_text(text: str):
        return AnalysisResponse(
            summary="The team needs to prepare a report.",
            key_points=["Sarah will prepare the report."],
            action_items=[
                {
                    "task": "Prepare the report",
                    "owner": "Sarah",
                    "deadline": "Friday",
                }
            ],
        )

    monkeypatch.setattr(main, "analyze_text", mock_analyze_text)

    response = client.post(
        "/analyze",
        json={"text": "Sarah will prepare a report by Friday."},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["summary"] == "The team needs to prepare a report."
    assert len(data["key_points"]) == 1
    assert data["action_items"][0]["owner"] == "Sarah"


def test_analyze_rejects_empty_text():
    response = client.post(
        "/analyze",
        json={"text": ""},
    )

    assert response.status_code == 422



def test_analyze_rejects_missing_text():
    response = client.post(
        "/analyze",
        json={},
    )

    assert response.status_code == 422


def test_analyze_rejects_non_string_text():
    response = client.post(
        "/analyze",
        json={"text": 123},
    )

    assert response.status_code == 422


def test_analyze_handles_anthropic_api_error(monkeypatch):
    def mock_analyze_text(text: str):
        raise APIError(
    message="Simulated provider failure",
    request=httpx.Request(
        "POST",
        "https://api.anthropic.com/v1/messages",
    ),
    body=None,
)

    monkeypatch.setattr(main, "analyze_text", mock_analyze_text)

    response = client.post(
        "/analyze",
        json={"text": "Test provider failure."},
    )

    assert response.status_code == 502
    assert response.json() == {
        "detail": "The AI analysis provider is temporarily unavailable."
    }