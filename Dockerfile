FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock README.md ./
COPY src ./src

RUN pip install --no-cache-dir uv \
    && uv pip install --system .

EXPOSE 8010

CMD ["python", "-m", "bvolt_infra.main"]
