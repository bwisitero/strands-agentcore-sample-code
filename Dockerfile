FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app

# All environment variables in one layer
ENV UV_SYSTEM_PYTHON=1 \
    UV_COMPILE_BYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DOCKER_CONTAINER=1 \
    AWS_REGION=us-east-1 \
    AWS_DEFAULT_REGION=us-east-1

# Copy project files and install dependencies
COPY . .
RUN cd . && uv pip install .
RUN uv pip install aws-opentelemetry-distro>=0.10.1

# Create non-root user and change ownership
RUN useradd -m -u 1000 bedrock_agentcore && \
    chown -R bedrock_agentcore:bedrock_agentcore /app

USER bedrock_agentcore

EXPOSE 8080
EXPOSE 8000

CMD ["opentelemetry-instrument", "python", "agentcore_deployment.py"]
