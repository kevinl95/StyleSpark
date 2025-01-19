FROM python:3.13.1-alpine3.21 AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

FROM base AS builder

# Install necessary build dependencies
RUN apk add --no-cache gcc libffi-dev musl-dev postgresql-dev git

# Install Poetry
RUN pip install "poetry==2.0.1"

# Create and activate virtual environment
RUN python -m venv /venv

# Copy and install project dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry self add poetry-plugin-export
RUN poetry install --without dev

FROM base AS final

# Install runtime dependencies
RUN apk add --no-cache libffi libpq git

# Copy virtual environment and scripts
COPY --from=builder /venv /venv
COPY entrypoint.sh analyze.py ./

# Set working directory
WORKDIR /repo

CMD ["./entrypoint.sh"]
