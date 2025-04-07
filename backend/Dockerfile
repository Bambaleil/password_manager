FROM python:3.10-slim-bullseye AS builder

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==2.1.1 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-interaction --no-ansi --no-root && \
    rm -rf $(poetry config cache-dir)/{cache,artifacts}

FROM python:3.10-slim-bullseye

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app

COPY --from=builder /app /app
COPY . /app

CMD ["python", "app/main.py"]
