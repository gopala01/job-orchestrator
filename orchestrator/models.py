from enum import Enum
from typing import Optional
from dataclasses import dataclass
from datetime import datetime


class JobState(str, Enum):
    SUBMITTED = "submitted"
    QUEUED = "queued"
    RUNNING = "running"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    job_id: str
    state: JobState
    attempt: int = 0
    created_at: str = ""
    updated_at: str = ""
    error: Optional[str] = None

    @staticmethod
    def now() -> str:
        return datetime.utcnow().isoformat()
