# Builds for the host platform; for AWS ARM: docker build --platform linux/arm64 .
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev --no-install-project
COPY src ./src
RUN uv sync --no-dev
RUN useradd --create-home --uid 10001 app
USER app
CMD ["uv", "run", "--no-dev", "python", "-m", "app.main"]
