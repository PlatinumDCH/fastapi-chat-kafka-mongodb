FROM python:3.11.1-slim-bullseye

ENV PYTHONDONTERITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-dev \
    gcc \
    musl-dev

ADD pyproject.toml /app
RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY /app/* /app/