# Distributed Job Orchestration System

This project implements a distributed job orchestration system with
explicit job lifecycle management, failure handling, and cancellation,
built on top of Celery, RabbitMQ, and Redis.

Current status:

- Core infrastructure running via Docker Compose
- Redis and RabbitMQ provisioned
- API and worker services containerised

Next steps:

- Job state model
- Job submission API
- Celery task execution
