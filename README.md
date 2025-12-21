# Distributed Job Orchestration System

This repository implements a **distributed job orchestration system** with
explicit job lifecycle management, retries, failure handling, and cooperative
cancellation.

The system is built on top of **FastAPI, Celery, Redis, and RabbitMQ**, and is
designed to **separate control-plane logic from task execution**, mirroring
production orchestration architectures.

---

## Architecture Overview

The system is composed of the following services:

- **API Service (FastAPI)**  
  Exposes a REST interface for job submission, status inspection, and
  cancellation.  
  Owns control-plane responsibilities and enforces valid job state transitions.

- **Worker Service (Celery)**  
  Executes jobs asynchronously, updates job state, handles retries with backoff,
  and cooperatively respects cancellation requests.

- **Redis**  
  Acts as the **authoritative job state store**, persisting lifecycle state,
  attempt counts, timestamps, and error information.

- **RabbitMQ**  
  Provides durable message queuing for distributed task execution and worker
  coordination.

Shared orchestration logic (job models, state transitions, and validation)
lives in the `orchestrator/` module and is reused by both API and worker
services, ensuring consistency across the system.

All services communicate over an internal Docker network.

---

## Job Lifecycle

Jobs follow a strict, explicit state machine:

CREATED → RUNNING → COMPLETED
↘ FAILED
↘ CANCELLED

State transitions are validated and persisted to Redis, ensuring correctness
under retries, failures, and concurrent worker execution.

Cancellation is **cooperative**: workers periodically check job state and
terminate execution early if cancellation is requested.

---

## API Surface

- `POST /jobs` — submit a new job
- `GET /jobs/{job_id}` — retrieve job state and metadata
- `DELETE /jobs/{job_id}` — request job cancellation

The API is intentionally minimal and focused on orchestration concerns.

---

## Current Status

- Docker Compose–based local environment
- Redis-backed job state model with explicit lifecycle enforcement
- Celery-based distributed execution with retries and backoff
- Cooperative job cancellation support
- Shared control-plane logic across API and worker services
- RabbitMQ fully integrated for task delivery

---

## Running the System

```bash
docker compose up --build
```
