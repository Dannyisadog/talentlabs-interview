from uuid import uuid4

import pytest
from django.urls import reverse
from ninja.testing import TestClient

from api.models.jobs import Job
from api.routes.jobs import router

client = TestClient(router)

@pytest.fixture
def sample_job_data() -> dict:
    return {
        "id": uuid4(),
        "title": "Software Engineer",
        "company_name": "Test Company",
        "location": "Remote",
        "description": "Test job description",
        "salary_range": {"min": 100000, "max": 150000, "currency": "USD"},
        "posting_date": "2024-03-20",
        "expiration_date": "2024-04-20",
        "required_skills": ["Python", "Django", "PostgreSQL"]
    }

@pytest.fixture
def sample_job(db, sample_job_data):
    return Job.objects.create(**sample_job_data)

@pytest.mark.django_db
class TestJobsAPI:
    def test_create_job_success(self, sample_job_data):
        response = client.post("/", json=sample_job_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == sample_job_data["title"]
        assert data["company_name"] == sample_job_data["company_name"]
        assert data["location"] == sample_job_data["location"]

    def test_create_job_invalid_data(self):
        invalid_data = {"title": ""}  # Missing required fields
        response = client.post("/", json=invalid_data)
        assert response.status_code == 422  # Django Ninja uses 422 for validation errors
        assert "detail" in response.json()  # Django Ninja uses 'detail' for error messages

    def test_get_job_success(self, sample_job):
        response = client.get(f"/{sample_job.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == str(sample_job.id)
        assert data["title"] == sample_job.title

    def test_get_job_not_found(self):
        non_existent_id = uuid4()
        response = client.get(f"/{non_existent_id}")
        assert response.status_code == 404
        assert "error" in response.json()

    def test_list_jobs_success(self, sample_job):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["id"] == str(sample_job.id)

    def test_list_jobs_with_filters(self, sample_job):
        response = client.get(f"/?title={sample_job.title}&company_name={sample_job.company_name}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        assert data[0]["title"] == sample_job.title
        assert data[0]["company_name"] == sample_job.company_name

    def test_update_job_success(self, sample_job):
        update_data = {
            "title": "Senior Software Engineer",
            "salary_range": {"min": 150000, "max": 200000, "currency": "USD"}
        }
        response = client.put(f"/{sample_job.id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["salary_range"] == update_data["salary_range"]
        assert data["company_name"] == sample_job.company_name  # Unchanged field

    def test_update_job_not_found(self):
        non_existent_id = uuid4()
        update_data = {"title": "New Title"}
        response = client.put(f"/{non_existent_id}", json=update_data)
        assert response.status_code == 404
        assert "error" in response.json()

    def test_delete_job_success(self, sample_job):
        response = client.delete(f"/{sample_job.id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Job deleted successfully"
        
        # Verify job is actually deleted
        get_response = client.get(f"/{sample_job.id}")
        assert get_response.status_code == 404

    def test_delete_job_not_found(self):
        non_existent_id = uuid4()
        response = client.delete(f"/{non_existent_id}")
        assert response.status_code == 404
        assert "error" in response.json()
