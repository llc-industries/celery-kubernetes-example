FROM python:3.12-slim

WORKDIR /app

RUN apt-get update -y && apt-get install -y --no-install-recommends procps gcc && rm -rf /var/lib/apt/lists/*

COPY lcs /usr/src/lcs
COPY consumer-large/celery_app.py /app/celery_app.py

RUN pip install --no-cache-dir 'celery>=5.3.0' /usr/src/lcs

ENTRYPOINT ["celery", "-A", "celery_app", "worker"]
