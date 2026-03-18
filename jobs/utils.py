from functools import lru_cache

def calcular_pago_neto(monto_bruto, nivel_reputacion):
    comisiones = {
        'NOVATO': 0.20,
        'VETERANO': 0.10,
        'LEYENDA': 0.05
    }
    
    # .upper() para que no importe si escriben 'novato' o 'NOVATO'
    porcentaje = comisiones.get(nivel_reputacion.upper(), 0.20)
    comision = monto_bruto * porcentaje
    return monto_bruto - comision

def clasificar_reputacion(proyectos_completados):
    if proyectos_completados >= 50:
        return 'LEYENDA'
    elif proyectos_completados >= 10:
        return 'VETERANO'
    else:
        return 'NOVATO'



@lru_cache(maxsize=128) # Guarda los últimos 128 cálculos distintos
def calcular_pago_neto(monto_bruto, nivel_reputacion):
    comisiones = {
        'NOVATO': 0.20,
        'VETERANO': 0.10,
        'LEYENDA': 0.05
    }
    porcentaje = comisiones.get(nivel_reputacion.upper(), 0.20)
    return monto_bruto - (monto_bruto * porcentaje)

