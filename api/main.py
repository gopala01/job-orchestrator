import time
import uuid
from orchestrator.state import create_job, get_job, update_state
from orchestrator.models import JobState

if __name__ == "__main__":
    job_id = str(uuid.uuid4())
    print(f"Creating job {job_id}")

    create_job(job_id)
    time.sleep(2)

    update_state(job_id, JobState.RUNNING)
    time.sleep(2)

    update_state(job_id, JobState.COMPLETED)

    job = get_job(job_id)
    print("Final job state:", job)
    
    while True:
        time.sleep(10)