import os
from celery import Celery
import time

from orchestrator.state import get_job, update_state, increment_attempt
from orchestrator.models import JobState

celery = Celery(
    "worker",
    broker= os.getenv("CELERY_BROKER_URL"),
    backend= os.getenv("REDIS_URL"),
)
@celery.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=5,
    retry_kwargs={'max_retries': 3},
)

def run_job(self, job_id: str):
    job = get_job(job_id)
    if not job:
        return

    if job.state == JobState.CANCELLED:
        return
    increment_attempt(job_id)
    update_state(job_id, JobState.RUNNING)

    try:
        for _ in range(5):
            time.sleep(10)  # Replace with actual job logic
        job = get_job(job_id)
        if job and job.state == JobState.CANCELLED:
            return
        update_state(job_id, JobState.COMPLETED)
    except Exception as e:
        update_state(job_id, JobState.FAILED, error=str(e))
        raise
    