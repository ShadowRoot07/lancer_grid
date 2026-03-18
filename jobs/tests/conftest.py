import pytest
from django.contrib.auth.models import User
from jobs.models import Job

@pytest.fixture
def test_user(db):
    """Crea un usuario de prueba reutilizable."""
    return User.objects.create_user(username='cyber_lancer', password='password123')

@pytest.fixture
def sample_job(db, test_user):
    """Crea un trabajo de prueba vinculado al usuario anterior."""
    return Job.objects.create(
        client=test_user,
        title="Misión de Incógnito",
        description="Hackear el mainframe",
        min_budget=1000,
        max_budget=2000
    )

