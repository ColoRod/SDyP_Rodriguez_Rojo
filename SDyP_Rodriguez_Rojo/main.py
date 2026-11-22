import csv
import os
from benchmark import evaluar_tamano


def imprimir_tabla(resultados: list[dict]) -> None:
    """Imprime en consola una tabla prolija con los tiempos y el Speedup."""
    encabezado = (
        f"{'Tamaño (N)':>12} | {'Workers':>7} | "
        f"{'Búsq Sec (s)':>12} | {'Búsq Par (s)':>12} | {'Speedup B.':>10} | "
        f"{'Ord Sec (s)':>11} | {'Ord Par (s)':>11} | {'Speedup O.':>10}"
    )
    separador = "-" * len(encabezado)
    print("\n" + separador)
    print(encabezado)
    print(separador)

    tamano_actual = None
    for fila in resultados:
        if tamano_actual is not None and fila["tamano"] != tamano_actual:
            print(separador)
        tamano_actual = fila["tamano"]

        print(
            f"{fila['tamano']:>12,d} | {fila['workers']:>7d} | "
            f"{fila['t_busq_sec']:>12.5f} | {fila['t_busq_par']:>12.5f} | {fila['speedup_busq']:>9.2f}x | "
            f"{fila['t_ord_sec']:>11.5f} | {fila['t_ord_par']:>11.5f} | {fila['speedup_ord']:>9.2f}x"
        )
    print(separador)


def exportar_csv(resultados: list[dict], nombre_archivo: str = "resultados_tiempos.csv") -> None:
    """Guarda los resultados en un archivo CSV para facilitar gráficos o tablas en el informe."""
    if not resultados:
        return
    campos = list(resultados[0].keys())
    with open(nombre_archivo, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(resultados)
    print(f"\n[OK] Resultados exportados correctamente a '{nombre_archivo}'.")


if __name__ == "__main__":
    print("=== TP: Algoritmos Concurrentes de Búsqueda y Ordenamiento ===")
    print(f"Procesadores lógicos detectados por el SO: {os.cpu_count()}")
    print("Arquitectura objetivo: 4 núcleos físicos / 8 hilos lógicos\n")

    # Parámetros de experimentación acordados
    tamanos_datos = [10_000, 100_000, 1_000_000, 5_000_000]
    cantidades_workers = [1, 2, 4, 8, 12]
    entrada = input("Ingrese un número a buscar entre 0 y 10000 (Enter para usar 500): ").strip()
    valor_a_buscar = int(entrada) if entrada.isdigit() else 500
    print(f"-> Buscando el valor: {valor_a_buscar}\n")

    todos_los_resultados = []

    for n in tamanos_datos:
        print(f"Procesando pruebas para N = {n:,d} elementos...")
        resultados_n = evaluar_tamano(n, cantidades_workers, valor_a_buscar)
        todos_los_resultados.extend(resultados_n)

    imprimir_tabla(todos_los_resultados)
    exportar_csv(todos_los_resultados)