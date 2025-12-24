FROM python:3.11-slim

WORKDIR /app

COPY worker/worker.py worker/worker.py
COPY orchestrator orchestrator

RUN pip install celery redis

CMD ["sh", "-c", "sleep 10 && celery -A worker.worker worker --loglevel=info"]

