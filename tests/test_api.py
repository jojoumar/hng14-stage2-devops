from fastapi.testclient import TestClient
from api.main import app, get_redis
import fakeredis

# mock Redis
fake_redis = fakeredis.FakeRedis()
app.dependency_overrides[get_redis] = lambda: fake_redis

client = TestClient(app)


def test_create_job():
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_get_job_not_found():
    response = client.get("/jobs/invalid")
    assert response.status_code == 200


def test_health():
    response = client.get("/health")
    assert response.status_code == 200