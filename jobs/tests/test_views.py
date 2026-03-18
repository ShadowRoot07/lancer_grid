import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_job_list_view(client):
    # client es un fixture de pytest-django que simula un navegador
    url = reverse('job_list')
    response = client.get(url)
    
    assert response.status_code == 200
    assert 'jobs/job_list.html' in [t.name for t in response.templates]

