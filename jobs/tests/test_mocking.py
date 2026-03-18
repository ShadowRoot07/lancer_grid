import pytest
from unittest.mock import patch
from django.urls import reverse
from django.contrib.auth.models import User
from jobs.models import Bid

@pytest.mark.django_db
def test_notificacion_al_aceptar_bid(client, test_user, sample_job):
    # 1. Setup: Crear el freelancer y la propuesta
    freelancer = User.objects.create_user(username='lucky_lancer', password='123')
    bid = Bid.objects.create(
        job=sample_job,
        freelancer=freelancer,
        proposal_text="Prueba de mock",
        estimated_days=1,
        bid_amount=100
    )

    # 2. MOCKING: "Parcheamos" la función de notificación
    # Usamos la ruta completa hacia donde se USA la función, no donde se define.
    with patch('jobs.views.enviar_notificacion_push') as mock_push:
        mock_push.return_value = {"status": "success"} # Forzamos la respuesta
        
        # 3. Acción: El cliente acepta el bid
        client.force_login(test_user)
        url = reverse('accept_bid', kwargs={'bid_id': bid.id})
        client.post(url)

        # 4. Verificación del Mock
        # ¿Se llamó a la función realmente?
        assert mock_push.called is True
        # ¿Se llamó con los argumentos correctos?
        mock_push.assert_called_with(freelancer.id, "¡Tu propuesta ha sido aceptada!")

    print("\n✅ El test pasó sin tocar servidores externos.")

