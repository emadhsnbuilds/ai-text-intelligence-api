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

The API is deployed on **Google Cloud Run**.

| Setting | Value |
|---|---|
| Project | `fde-sprint` |
| Service | `ai-text-intelligence-api` |
| Region | `europe-west1` |
| Access | Private: Google IAM authentication required (no public access) |
| Runtime service account | `ai-text-api-runtime@fde-sprint.iam.gserviceaccount.com` |
| Anthropic API key | Google Secret Manager secret `anthropic-api-key`, exposed as `ANTHROPIC_API_KEY` |
| Memory / CPU | 512 MiB / 1 CPU |
| Concurrency | 2 requests per instance |
| Maximum instances | 2 |
| Request timeout | 60 seconds |

The service is not publicly accessible. Callers need the `roles/run.invoker` role on the service.

### Deploy

The API key is never passed on the command line: it is read from Secret Manager at runtime.

```bash
gcloud run deploy ai-text-intelligence-api \
  --project fde-sprint \
  --region europe-west1 \
  --source . \
  --no-allow-unauthenticated \
  --service-account ai-text-api-runtime@fde-sprint.iam.gserviceaccount.com \
  --set-secrets ANTHROPIC_API_KEY=anthropic-api-key:<version> \
  --set-env-vars ANTHROPIC_MODEL=claude-haiku-5-5 \
  --memory 512Mi \
  --cpu 1 \
  --concurrency 2 \
  --max-instances 2 \
  --timeout 60
```

Replace `<version>` with the secret version to use (for example `latest`). The runtime service account needs the `roles/secretmanager.secretAccessor` role on the secret.

### Access the private service locally

Start an authenticated local proxy to the service (uses your own `gcloud` credentials):

```bash
gcloud run services proxy ai-text-intelligence-api \
  --project fde-sprint \
  --region europe-west1 \
  --port 8090
```

While the proxy is running, open the Swagger UI at:

```text
http://localhost:8090/docs
```

## License

MIT License (to be added when the project license is finalized).
