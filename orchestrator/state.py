import redis
from orchestrator.models import Job, JobState
from typing import Optional

REDIS_HOST = "redis"
REDIS_PORT = 6379

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


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
    r.hset(
        _job_key(job_id),
        mapping={
            "state": new_state.value,
            "updated_at": Job.now(),
            "error": error or "",
        },
    )


def increment_attempt(job_id: str):
    r.hincrby(_job_key(job_id), "attempt", 1)
    r.hset(_job_key(job_id), "updated_at", Job.now())
