import pytest
from jobs.utils import calcular_pago_neto, clasificar_reputacion

# Test con múltiples casos usando Parametrize (Nivel Pro)
@pytest.mark.parametrize("completados, esperado", [
    (5, 'NOVATO'),
    (10, 'VETERANO'),
    (49, 'VETERANO'),
    (50, 'LEYENDA'),
    (100, 'LEYENDA'),
])
def test_clasificacion_reputacion(completados, esperado):
    assert clasificar_reputacion(completados) == esperado

def test_calculo_pago_neto_leyenda():
    # Si cobra 1000 y es Leyenda (5%), debe recibir 950
    resultado = calcular_pago_neto(1000, 'LEYENDA')
    assert resultado == 950

def test_calculo_pago_neto_novato():
    # Si cobra 1000 y es Novato (20%), debe recibir 800
    resultado = calcular_pago_neto(1000, 'NOVATO')
    assert resultado == 800


def test_calculo_pago_neto_nivel_inexistente():
    # Si el nivel no existe, debe aplicar la comisión por defecto (20%)
    resultado = calcular_pago_neto(1000, 'NIVEL_HACKER_DESCONOCIDO')
    assert resultado == 800

def test_calculo_pago_neto_monto_cero():
    # Probar que no explote con 0
    assert calcular_pago_neto(0, 'LEYENDA') == 0

def test_calculo_pago_neto_monto_negativo():
    # Comportamiento esperado con números negativos (deuda)
    assert calcular_pago_neto(-100, 'VETERANO') == -90

