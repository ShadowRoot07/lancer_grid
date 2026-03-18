import timeit
from utils import calcular_pago_neto

# Definimos qué queremos medir
def test_performance():
    # Simulamos 100,000 cálculos con diferentes niveles
    calcular_pago_neto(1000, 'LEYENDA')
    calcular_pago_neto(500, 'NOVATO')
    calcular_pago_neto(2500, 'VETERANO')

if __name__ == "__main__":
    print("🚀 Iniciando Benchmark de LancerGrid...")
    
    # Ejecutamos la función 100,000 veces
    numero_ejecuciones = 100000
    tiempo_total = timeit.timeit(test_performance, number=numero_ejecuciones)
    
    tiempo_por_operacion = (tiempo_total / (numero_ejecuciones * 3)) * 1000000 # en microsegundos
    operaciones_por_segundo = (numero_ejecuciones * 3) / tiempo_total

    print("-" * 40)
    print(f"⏱️ Tiempo total para {numero_ejecuciones * 3} cálculos: {tiempo_total:.4f} segundos")
    print(f"⚡ Operaciones por segundo: {operaciones_por_segundo:,.0f}")
    print(f"💎 Latencia promedio: {tiempo_por_operacion:.4f} μs (microsegundos)")
    print("-" * 40)

