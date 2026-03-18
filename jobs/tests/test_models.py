import pytest
from django.contrib.auth.models import User
from jobs.models import Job

@pytest.mark.django_db
def test_job_creation():
    # Setup
    user = User.objects.create_user(username='testclient', password='password123')
    job = Job.objects.create(
        client=user,
        title="Test Project",
        description="A simple test description",
        min_budget=100,
        max_budget=500
    )
    
    # Assert
    assert job.title == "Test Project"
    assert job.status == "OPEN"
    assert str(job) == "Test Project"

