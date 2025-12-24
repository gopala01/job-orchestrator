import os
import time
from redis import Redis
from redis.exceptions import ConnectionError
from orchestrator.models import Job, JobState
from typing import Optional

_redis = None

def get_redis() -> Redis:
    global _redis
    if _redis is not None:
        return _redis

    redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

    for _ in range(10):
        try:
            r = Redis.from_url(redis_url, decode_responses=True)
            r.ping()
            _redis = r
            return r
        except ConnectionError:
            time.sleep(1)

    raise RuntimeError("Redis not reachable after retries")


def _job_key(job_id: str) -> str:
    return f"job:{job_id}"


def create_job(job_id: str) -> Job:
    job = Job(
        job_id=job_id,
        state=JobState.SUBMITTED,
        attempt=0,
        created_at=Job.now(),
        updated_at=Job.now(),
    )
    r = get_redis()
    r.hset(
        _job_key(job_id),
        mapping={
            "job_id": job.job_id,
            "state": job.state.value,
            "attempt": job.attempt,
            "created_at": job.created_at,
            "updated_at": job.updated_at,
            "error": "",
        },
    )
    return job


def get_job(job_id: str) -> Optional[Job]:
    r = get_redis()
    data = r.hgetall(_job_key(job_id))
    if not data:
        return None

    return Job(
        job_id=data["job_id"],
        state=JobState(data["state"]),
        attempt=int(data["attempt"]),
        created_at=data["created_at"],
        updated_at=data["updated_at"],
        error=data.get("error") or None,
    )


def update_state(job_id: str, new_state: JobState, error: Optional[str] = None):
    r = get_redis()
    r.hset(
        _job_key(job_id),
        mapping={
            "state": new_state.value,
            "updated_at": Job.now(),
            "error": error or "",
        },
    )


def increment_attempt(job_id: str):
    r = get_redis()
    r.hincrby(_job_key(job_id), "attempt", 1)
    r.hset(_job_key(job_id), "updated_at", Job.now())


def cancel_job(job_id: str) -> bool:
    job = get_job(job_id)
    if not job:
        return False

    if job.state in {JobState.COMPLETED, JobState.FAILED}:
        return False

    update_state(job_id, JobState.CANCELLED)
    return True
