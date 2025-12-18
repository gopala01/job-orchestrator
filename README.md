# Distributed Job Orchestration System

This repository implements a distributed job orchestration system with
explicit job lifecycle management, failure handling, and cancellation.
The system is built on top of Redis and RabbitMQ and is designed to
separate control-plane logic from task execution.

## Architecture Overview

The system is composed of the following services:

- **API Service**  
  Responsible for job creation and lifecycle management.

- **Worker Service**  
  Executes jobs asynchronously (execution logic to be added).

- **Redis**  
  Acts as the central job state store and coordination backend.

- **RabbitMQ**  
  Provides durable message queuing for distributed task execution.

Shared orchestration logic (job models and state management) lives in the
`orchestrator/` module and is reused by both API and worker services.

## Current Status

- Docker Compose–based local environment
- Redis-backed job state model with explicit lifecycle states
- Shared control-plane logic across services
- RabbitMQ provisioned and ready for task execution

## Running the System

```bash
docker compose up --build
```
