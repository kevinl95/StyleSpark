FROM python:3.13.1-alpine3.21 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base AS builder

RUN apk add --no-cache gcc libffi-dev musl-dev git g++ linux-headers
RUN pip install "poetry==2.0.1"

COPY pyproject.toml poetry.lock ./
RUN poetry install --without dev

COPY entrypoint.sh analyze.py ./
CMD ["./entrypoint.sh"]