FROM python:3.13.1-slim-bullseye AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libffi-dev musl-dev git g++ \
    && rm -rf /var/lib/apt/lists/*
RUN pip install "poetry==2.0.1"

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY entrypoint.sh analyze.py ./
CMD ["./entrypoint.sh"]