ARG PYTHON_VERSION=3.12.0

FROM --platform=arm64 python:${PYTHON_VERSION}-slim as poetry-base

RUN apt-get update && apt-get install -y libgeos-dev

ENV PYTHONPATH=/app \
    PYTHONDONTWRITEBYTECODE=1

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

WORKDIR $PYTHONPATH

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_VERSION=1.6.0 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100


WORKDIR /app

RUN pip install poetry==${POETRY_VERSION}
COPY pyproject.toml poetry.lock /app/

FROM poetry-base as core-dev

COPY src/core core 
COPY src/shop shop

FROM core-dev as server-dev

RUN poetry install --only backend,core && rm -rf ${POETRY_CACHE_DIR}

RUN touch /app/__init__.py
COPY src/server server
COPY src/run_server.py run_server.py

CMD ["python", "-m", "run_server"]


## Production stages
FROM poetry-base as poetry-export

FROM poetry-export as server-export

RUN poetry export --only core,backend --without-hashes --no-interaction --output requirements.txt

FROM python:${PYTHON_VERSION}-slim as production-server
ENV PYTHONUNBUFFERED=1 PYTHONFAULTHANDLER=1

COPY --from=server-export /requirements.txt requirements.txt
RUN pip install --no-cache-dir --disable-pip-version-check --no-input -r requirements.txt

WORKDIR /app
COPY src/server /server
COPY src/core /core 
COPY src/shop /shop

CMD ["python", "-m", "run_server"]









