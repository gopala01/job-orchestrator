from celery import Celery
import time

from orchestrator.state import get_job, update_state, increment_attempt
from orchestrator.models import JobState

app = Celery(
    "worker",
    broker="amqp://rabbitmq",
    backend="redis://redis"
)
@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={'max_retries': 3},
)

def run_job(self, job_id: str):
    job = get_job(job_id)
    if not job:
        raise ValueError("Job not found")

    if job.state == JobState.CANCELLED:
        return
    increment_attempt(job_id)
    update_state(job_id, JobState.RUNNING)

    try:
        # Simulate job processing
        time.sleep(10)  # Replace with actual job logic
        update_state(job_id, JobState.COMPLETED)
    except Exception as e:
        update_state(job_id, JobState.FAILED, error=str(e))
        raise e