from concurrent.futures import ProcessPoolExecutor


# ==========================================
# ALGORITMOS DE ORDENAMIENTO Y FUSIÓN (Python)
# ==========================================

def _fusionar_dos_listas(izq: list[int], der: list[int]) -> list[int]:
    """Fusiona dos sublistas ya ordenadas."""
    resultado = []
    i = j = 0
    len_izq, len_der = len(izq), len(der)

    while i < len_izq and j < len_der:
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


def merge_sort_python(datos: list[int]) -> list[int]:
    """Ordenamiento Merge Sort recursivo."""
    n = len(datos)
    if n <= 1:
        return datos

    medio = n // 2
    izquierda = merge_sort_python(datos[:medio])
    derecha = merge_sort_python(datos[medio:])
    return _fusionar_dos_listas(izquierda, derecha)


def fusionar_k_bloques(bloques: list[list[int]]) -> list[int]:
    """
    Une los k bloques ordenados fusionándolos de a pares en rondas
    sin usar librerías externas como heapq.
    """
    if not bloques:
        return []

    actuales = bloques
    while len(actuales) > 1:
        siguiente_ronda = []
        for i in range(0, len(actuales), 2):
            if i + 1 < len(actuales):
                siguiente_ronda.append(_fusionar_dos_listas(actuales[i], actuales[i + 1]))
            else:
                siguiente_ronda.append(actuales[i])
        actuales = siguiente_ronda

    return actuales[0]


# ==========================================
# ACTIVIDAD 1: Versiones Secuenciales
# ==========================================

def busqueda_secuencial(datos: list[int], objetivo: int) -> list[int]:
    """Devuelve todas las posiciones donde aparece el valor objetivo."""
    return [i for i, valor in enumerate(datos) if valor == objetivo]


def ordenamiento_secuencial(datos: list[int]) -> list[int]:
    """Devuelve una nueva lista ordenada de forma secuencial."""
    return merge_sort_python(datos)


# ==========================================
# PARTICIONAMIENTO DE DATOS
# ==========================================

def dividir_en_bloques_con_offset(datos: list[int], num_bloques: int) -> list[tuple[list[int], int]]:
    """
    Divide la lista en 'num_bloques' partes aproximadamente iguales.
    Devuelve una lista de tuplas: (sublista, indice_inicio_original).
    """
    n = len(datos)
    if num_bloques <= 1 or n == 0:
        return [(datos, 0)]

    tam_base, resto = divmod(n, num_bloques)
    bloques = []
    inicio = 0

    for i in range(num_bloques):
        fin = inicio + tam_base + (1 if i < resto else 0)
        if inicio < fin:
            bloques.append((datos[inicio:fin], inicio))
        inicio = fin

    return bloques


# ==========================================
# ACTIVIDAD 2: Búsqueda Concurrente / Paralela
# ==========================================

def _worker_busqueda(args: tuple[list[int], int, int]) -> list[int]:
    """Suma el 'offset' al índice local para recuperar la posición original."""
    sublista, offset, objetivo = args
    return [offset + i for i, valor in enumerate(sublista) if valor == objetivo]


def busqueda_paralela(datos: list[int], objetivo: int, num_workers: int) -> list[int]:
    """Divide la lista, busca en paralelo y reconstruye las posiciones originales."""
    bloques = dividir_en_bloques_con_offset(datos, num_workers)
    tareas = [(sublista, offset, objetivo) for sublista, offset in bloques]

    posiciones_totales = []
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        resultados_por_bloque = executor.map(_worker_busqueda, tareas)
        for posiciones_bloque in resultados_por_bloque:
            posiciones_totales.extend(posiciones_bloque)

    return posiciones_totales


# ==========================================
# ACTIVIDAD 3: Ordenamiento y Fusión Paralela
# ==========================================

def _worker_ordenamiento(sublista: list[int]) -> list[int]:
    """Ordena un bloque individual dentro de un proceso hijo."""
    return merge_sort_python(sublista)


def ordenamiento_paralelo(datos: list[int], num_workers: int) -> list[int]:
    """
    Divide la lista en bloques, los ordena en paralelo en distintos procesos
    y luego fusiona los bloques ya ordenados de a pares.
    """
    bloques_con_offset = dividir_en_bloques_con_offset(datos, num_workers)
    sublistas = [sublista for sublista, _ in bloques_con_offset]

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        bloques_ordenados = list(executor.map(_worker_ordenamiento, sublistas))

    return fusionar_k_bloques(bloques_ordenados)