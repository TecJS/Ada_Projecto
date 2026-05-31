from typing import List, Tuple, Dict, Union
import numpy as np
import Cromo_Km as ckm
def crear_poblacion(regla: int, perfil: bool,k_clusters,n_maquinas,tiempos_ops,n_individuos,secuencia_ops, 
                    n_trabajos,n_max_operaciones,semilla_inicial: int = 122) -> List[np.ndarray]:
    """
    Crea población inicial de cromosomas.
    
    Args:
        regla: Regla de ordenamiento (1-4)
        perfil: Perfil de agrupamiento
        semilla_inicial: Semilla base
    
    Returns:
        Lista de cromosomas
    """
    poblacion = []
    
    for i in range(n_individuos):
        semilla = semilla_inicial + i
        cromosoma = ckm.cromosoma_kmeans(regla, semilla, k_clusters,n_maquinas,tiempos_ops,secuencia_ops,n_trabajos,n_max_operaciones,perfil)
        poblacion.append(cromosoma)
    
    return poblacion