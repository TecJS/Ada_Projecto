import numpy as np
import Cromo_MWR_LWR as wr #wr work remaing
import LPT_SPT as pt # pt process time
def cromosoma_kmeans(regla: int, semilla: int,k_clusters,n_maquinas,tiempos_ops,secuencia_ops,n_trabajos,n_max_operaciones ,perfil: bool) -> np.ndarray:
    """
    Genera cromosoma (matriz de ordenamiento de trabajos).
    
    Args:
        regla: 1=SPT, 2=LPT, 3=MWR, 4=LWR
        semilla: Random seed
        perfil: True=tiempos, False=secuencia
    
    Returns:
        Cromosoma (n_maquinas × n_trabajos)
    """
    
    if regla == 3:
        # MWR/LWR
        return wr.cromosoma_mwr_lwr(n_maquinas,n_trabajos,n_max_operaciones,tiempos_ops,secuencia_ops)
    elif regla == 4:
        return wr.cromosoma_mwr_lwr(n_maquinas,n_trabajos,n_max_operaciones,tiempos_ops,secuencia_ops,False)
    else:
        # LPT/SPT: replicar ordenamiento
        return pt.cromosoma_lpt_spt(regla, semilla, k_clusters,n_maquinas,tiempos_ops,secuencia_ops,perfil)
