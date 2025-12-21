FROM python:3.11-slim

WORKDIR /app

COPY worker/worker.py .
COPY orchestrator ./orchestrator

RUN pip install celery redis

CMD ["celery", "-A", "worker", "worker", "--loglevel=info"]

