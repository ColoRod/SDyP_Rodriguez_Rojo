import random
import time
from algoritmos import (
    busqueda_secuencial,
    busqueda_paralela,
    ordenamiento_secuencial,
    ordenamiento_paralelo,
)


def generar_datos(tamano: int, min_val: int = 0, max_val: int = 10000, semilla: int = 42) -> list[int]:
    """Genera una lista reproducible de números enteros aleatorios."""
    rng = random.Random(semilla)
    return [rng.randint(min_val, max_val) for _ in range(tamano)]


def evaluar_tamano(tamano: int, lista_workers: list[int], valor_buscado: int = 500) -> list[dict]:
    """
    Ejecuta las pruebas secuenciales y paralelas para un tamaño de lista N
    y devuelve una lista de diccionarios con todas las métricas.
    """
    datos = generar_datos(tamano)
    resultados_experimento = []

    # 1. Ejecución Secuencial (Línea base)
    t0 = time.perf_counter()
    res_busq_sec = busqueda_secuencial(datos, valor_buscado)
    t_busq_sec = time.perf_counter() - t0

    t0 = time.perf_counter()
    res_ord_sec = ordenamiento_secuencial(datos)
    t_ord_sec = time.perf_counter() - t0

    # 2. Ejecución Paralela variando la cantidad de trabajadores
    for w in lista_workers:
        # --- Búsqueda Paralela ---
        t0 = time.perf_counter()
        res_busq_par = busqueda_paralela(datos, valor_buscado, w)
        t_busq_par = time.perf_counter() - t0

        # Validación estricta (Actividad 4)
        assert res_busq_sec == res_busq_par, f"Error en búsqueda con N={tamano}, workers={w}"

        # --- Ordenamiento Paralelo ---
        t0 = time.perf_counter()
        res_ord_par = ordenamiento_paralelo(datos, w)
        t_ord_par = time.perf_counter() - t0

        # Validación estricta (Actividad 4)
        assert res_ord_sec == res_ord_par, f"Error en ordenamiento con N={tamano}, workers={w}"

        # Cálculo de Speedup (T_secuencial / T_paralelo)
        speedup_busq = t_busq_sec / t_busq_par if t_busq_par > 0 else 0.0
        speedup_ord = t_ord_sec / t_ord_par if t_ord_par > 0 else 0.0

        resultados_experimento.append({
            "tamano": tamano,
            "workers": w,
            "ocurrencias": len(res_busq_sec),
            "t_busq_sec": t_busq_sec,
            "t_busq_par": t_busq_par,
            "speedup_busq": speedup_busq,
            "res_busq_sec": res_busq_sec,
            "t_ord_sec": t_ord_sec,
            "t_ord_par": t_ord_par,
            "speedup_ord": speedup_ord,
        })

    return resultados_experimento