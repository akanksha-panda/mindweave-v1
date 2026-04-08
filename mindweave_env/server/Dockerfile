ARG BASE_IMAGE=ghcr.io/meta-pytorch/openenv-base:latest
FROM ${BASE_IMAGE}

WORKDIR /app

# 1. Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/*

# 2. Install uv globally
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv

# 3. Copy the entire project
COPY . /app/

# 4. Install dependencies globally in the container (Simplest for Docker)
# This avoids the ".venv bin folder not found" issue
RUN uv pip install --system --no-cache -e .
RUN uv pip install --system fastapi uvicorn

# 5. Set Environment Variables
ENV PYTHONPATH="/app"
# Ensure the server can be found
ENV MODULE_PATH="mindweave_env.server.app:app"

# 6. Health check
HEALTHCHECK --interval=10s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# 7. Use the system uvicorn directly
CMD ["uvicorn", "mindweave_env.server.app:app", "--host", "0.0.0.0", "--port", "8000"]