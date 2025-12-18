FROM python:3.11-slim

WORKDIR /app

COPY api/main.py .
COPY orchestrator ./orchestrator

RUN pip install redis

CMD ["python", "main.py"]

