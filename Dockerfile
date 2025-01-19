FROM python:3.13.1-alpine3.21 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder

RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev
RUN pip install "poetry==2.0.1"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry self add poetry-plugin-export
RUN poetry install

FROM base AS final

RUN apk add --no-cache libffi libpq
COPY --from=builder /venv /venv
COPY --from=builder /app /app
COPY entrypoint.sh analyze.py ./
CMD ["./entrypoint.sh"]