FROM python:3.10-slim

WORKDIR app

RUN python -m pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev

COPY main.py .
COPY ./src ./src

ENV PYTHONPATH=src
ENV UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=443 \
    UVICORN_SSL_KEYFILE=resources/certs/key.pem \
    UVICORN_SSL_CERTFILE=resources/certs/certificate.pem \
    UVICORN_SSL_KEYFILE_PASSWORD=" "

ENTRYPOINT [ "poetry", "run", "uvicorn", "app:create_app", "--factory"]
