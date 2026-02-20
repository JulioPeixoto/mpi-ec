FROM python:3.12-slim

ENV UV_COMPILE_BYTECODE=0 \
    UV_LINK_MODE=copy

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY src ./src

EXPOSE 8000

CMD ["uv", "run", "fastapi", "dev", "src/main.py", "--host", "0.0.0.0"]
