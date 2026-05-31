import Auxiliares as aux
import numpy as np
from sklearn.cluster import KMeans
# ============================================================================
# 4. K-MEANS CLUSTERING
# ============================================================================

def k_agrupamiento(semilla: int,tiempos_ops,secuencia_ops, k_clusters,perfil_agrupamiento: bool = True) -> np.ndarray:
    """
    Agrupa trabajos con K-Means.
    
    Args:
        semilla: Random seed para reproducibilidad
        perfil_agrupamiento: True = usa tiempos, False = usa secuencia binaria
    
    Returns:
        labels: Array con asignación de cluster para cada trabajo
    """
    X = tiempos_ops if perfil_agrupamiento else aux.binariza_matriz(secuencia_ops)
    
    kmeans = KMeans(n_clusters=k_clusters, random_state=semilla, n_init=10)
    labels = kmeans.fit_predict(X)
    
    return labels
