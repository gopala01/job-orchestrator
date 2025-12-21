FROM python:3.11-slim

WORKDIR /app

COPY api/main.py .
COPY orchestrator ./orchestrator

RUN pip install fastapi uvicorn redis celery

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

