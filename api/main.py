import time
from fastapi import FastAPI, HTTPException
import uuid
from orchestrator.state import create_job, get_job, update_state
from orchestrator.models import JobState

app = FastAPI(title="Job Orchestrator API")

@app.post("/jobs")
def submit_job():
    job_id = str(uuid.uuid4())
    create_job(job_id)
    return {"job_id": job_id, "status": "created"}

@app.get("/jobs/{job_id}")
def fetch_job(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return{
        "job_id": job.job_id,
        "state": job.state,
        "attempt": job.attempt,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "error": job.error,
    }