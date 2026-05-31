import numpy as np
from typing import List, Tuple, Dict, Union
def binariza_matriz(matriz: np.ndarray) -> np.ndarray:
    """
    Convierte matriz a binaria (0 o 1).
    0 → 0, cualquier otro valor → 1
    """
    return (matriz != 0).astype(int)


def suma_por_fila(matriz: np.ndarray) -> np.ndarray:
    """Retorna suma de cada fila"""
    return np.sum(matriz, axis=1)


def indices_de_info_ordenado(info_grupos_ordenado: List[Tuple]) -> np.ndarray:
    """
    Extrae índices de una lista ordenada de tuplas (grupo, suma, indices).
    Devuelve array plano con todos los índices en orden.
    """
    indices_en_orden = []
    for _, _, indices in info_grupos_ordenado:
        indices_en_orden.extend(indices)
    return np.array(indices_en_orden, dtype=int)


def obtener_trabajos_por_maquina(maquina_id: int,n_trabajos,secuencia_ops) -> np.ndarray:
    """Retorna indices de trabajos que usan una máquina específica"""
    trabajos = []
    for j in range(n_trabajos):
        if maquina_id in secuencia_ops[j]:
            trabajos.append(j)
    return np.array(trabajos)
