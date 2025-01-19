FROM python:3.13.1-alpine3.21 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base AS builder

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==2.0.1"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry install  # Install dependencies, including transformers

FROM base AS final

RUN apk add --no-cache libffi libpq git
COPY --from=builder /venv /venv
COPY entrypoint.sh analyze.py ./
CMD ["./entrypoint.sh"]