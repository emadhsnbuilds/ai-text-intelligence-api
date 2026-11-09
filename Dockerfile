# Use Python 3.12 as the base image
FROM python:3.12-slim

# Copy the uv executable from its official image
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /bin/

# Set the working directory inside the container
WORKDIR /app

# Configure Python and uv
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Copy dependency definitions
COPY pyproject.toml uv.lock ./
COPY README.md ./

# Copy application source code
COPY src ./src

# Install production dependencies
RUN uv sync --frozen --no-dev

# Use the project's virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Cloud Run expects the application to listen on port 8080
EXPOSE 8080

# Start the FastAPI application
CMD ["uvicorn", "ai_text_intelligence_api.main:app", "--host", "0.0.0.0", "--port", "8080"]