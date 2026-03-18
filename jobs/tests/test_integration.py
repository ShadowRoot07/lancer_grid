import pytest
from django.urls import reverse
from django.contrib.auth.models import User  # <--- FALTABA ESTA LÍNEA
from jobs.models import Bid, Contract        # <--- Y ASEGURARNOS DE ESTA

@pytest.mark.django_db
def test_workflow_complete(client, test_user, sample_job):
    # 1. Creamos un freelancer
    freelancer = User.objects.create_user(username='freelancer_x', password='123')
    
    # El fixture 'client' simula un navegador. 
    # Forzamos el login del freelancer para que pueda enviar la propuesta.
    client.force_login(freelancer)

    # 2. El freelancer envía un Bid (POST)
    url_bid = reverse('bid_create', kwargs={'job_id': sample_job.id})
    response = client.post(url_bid, {
        'proposal_text': 'Soy el mejor para esto, tengo experiencia en mainframes.',
        'estimated_days': 5,
        'bid_amount': 1500
    })

    # Verificamos que se creó en la DB
    assert Bid.objects.count() == 1
    assert Bid.objects.first().freelancer == freelancer

    # 3. El cliente (test_user) acepta el Bid
    client.force_login(test_user) # Cambiamos de "sesión" al dueño del trabajo
    bid = Bid.objects.first()
    url_accept = reverse('accept_bid', kwargs={'bid_id': bid.id})
    
    client.post(url_accept)

    # 4. Verificaciones finales (Integridad de la base de datos)
    sample_job.refresh_from_db() # Obligamos a Django a traer los datos nuevos del Job
    
    assert sample_job.status == 'IN_PROGRESS'
    assert Contract.objects.count() == 1
    
    contrato = Contract.objects.first()
    assert contrato.freelancer == freelancer
    assert contrato.job == sample_job

