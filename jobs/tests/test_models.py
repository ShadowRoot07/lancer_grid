import pytest
from django.contrib.auth.models import User
from jobs.models import Job

@pytest.mark.django_db
def test_job_creation():
    """Prueba la creación manual de un trabajo y su método __str__"""
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
    # Verificamos que el __str__ coincida con la realidad del modelo
    assert str(job) == "Test Project - testclient"

@pytest.mark.django_db
def test_job_with_fixture(sample_job):
    """Prueba que la fixture 'sample_job' de conftest.py funciona correctamente"""
    # Assert
    assert sample_job.title == "Misión de Incógnito"
    assert sample_job.client.username == "cyber_lancer"
    assert sample_job.status == "OPEN"

