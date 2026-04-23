from fastapi import FastAPI, Depends
import redis
import uuid
import os


app = FastAPI()


def get_redis():
    return redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379))
    )


@app.post("/jobs")
def create_job(r: redis.Redis = Depends(get_redis)):
    job_id = str(uuid.uuid4())
    r.lpush("job", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str, r: redis.Redis = Depends(get_redis)):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return {"error": "not found"}
    return {"job_id": job_id, "status": status.decode()}


@app.get("/health")
def health():
    return {"status": "ok"}
