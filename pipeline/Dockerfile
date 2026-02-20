FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
#important for syncing dependancies
COPY "pyproject.toml" "uv.lock" ".python-version" ./
RUN uv sync --locked
COPY pipeline.py pipeline.py
ENTRYPOINT ['python', 'pipeline.py']