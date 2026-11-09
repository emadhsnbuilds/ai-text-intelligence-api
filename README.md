# AI Text Intelligence API

A reusable AI-powered text analysis microservice built with **FastAPI**, **Pydantic**, and **Anthropic Claude**.

It accepts text and returns structured analysis containing a summary, key points, and actionable tasks with owners and deadlines when explicitly mentioned.

## Features

- Structured text analysis using Anthropic Claude
- Automatic request and response validation with Pydantic
- REST API built with FastAPI
- Environment-based configuration and secret management
- Error handling and application logging
- Automated API tests with pytest
- Docker containerization

## Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- Anthropic Python SDK
- uv
- pytest
- HTTPX
- Docker

## Project Structure

```text
ai-text-intelligence-api/
├── src/
│   └── ai_text_intelligence_api/
│       ├── __init__.py
│       ├── main.py
│       ├── schemas.py
│       ├── settings.py
│       ├── anthropic_client.py
│       ├── analysis_service.py
│       └── prompts.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile
├── pyproject.toml
├── uv.lock
└── README.md
```

## Requirements

- Python 3.12
- uv
- An Anthropic API key
- Docker (optional, for containerized execution)

## Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd ai-text-intelligence-api
```

Install dependencies:

```bash
uv sync
```

## Configuration

Create your local environment file:

```bash
cp .env.example .env
```

Update `.env` with your Anthropic API key:

```env
ANTHROPIC_API_KEY=your_actual_api_key
ANTHROPIC_MODEL=claude-haiku-5-5
```

Never commit your `.env` file or expose your API key.

## Running Locally

Start the API:

```bash
uv run uvicorn ai_text_intelligence_api.main:app --reload
```

API base URL:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

`GET /health`

Example response:

```json
{
  "status": "healthy"
}
```

### Analyze Text

`POST /analyze`

Example request:

```json
{
  "text": "Sarah will prepare the marketing report by Friday. John will review it on Monday."
}
```

Example response:

```json
{
  "summary": "Sarah will prepare the marketing report by Friday, and John will review it on Monday.",
  "key_points": [
    "Sarah is responsible for preparing the marketing report, due by Friday.",
    "John is responsible for reviewing the marketing report on Monday."
  ],
  "action_items": [
    {
      "task": "Prepare the marketing report",
      "owner": "Sarah",
      "deadline": "Friday"
    },
    {
      "task": "Review the marketing report",
      "owner": "John",
      "deadline": "Monday"
    }
  ]
}
```

## Running Tests

Run the automated test suite:

```bash
uv run pytest -v
```

## Running with Docker

Build the image:

```bash
docker build --platform linux/amd64 -t ai-text-intelligence-api:local .
```

Run the container:

```bash
docker run --rm \
  --name ai-text-intelligence-api \
  -p 8001:8080 \
  --env-file .env \
  ai-text-intelligence-api:local
```

Access the API documentation:

```text
http://localhost:8001/docs
```

## Deployment

The intended deployment platform is **Google Cloud Run**, with the Anthropic API key managed through Google Secret Manager.

The live deployment URL will be added here after deployment.

## License

MIT License (to be added when the project license is finalized).
