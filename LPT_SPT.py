import numpy as np
import Auxiliares as aux
import Kmeans_agrupa as km
# ============================================================================
# 5. REGLAS DE ORDENAMIENTO: LPT Y SPT
# ============================================================================

def base_regla(grupos: np.ndarray, num_grupos: int, sf: np.ndarray, 
               rever: bool = False):
    """
    Regla base para SPT y LPT.
    
    Args:
        grupos: Array de asignación de cluster
        num_grupos: Número de clusters
        sf: Array de suma (trabajo total por trabajo)
        rever: True=LPT (descendente), False=SPT (ascendente)
    
    Returns:
        info_grupos_ordenado: [(grupo, suma, [indices])]
    """
    # Suma total por grupo
    suma_por_grupo = np.bincount(grupos, weights=sf, minlength=num_grupos)
    
    # Miembros de cada grupo, ordenados internamente
    miembros_grupo_ordenados = [
        [int(i) for i in sorted(
            np.where(grupos == g)[0], 
            key=lambda i: sf[i], 
            reverse=rever
        )]
        for g in range(num_grupos)
    ]
    
    # Información de cada grupo
    info_grupos = [
        (g, suma_por_grupo[g], miembros_grupo_ordenados[g])
        for g in range(num_grupos)
    ]
    
    # Ordenar grupos por suma
    info_grupos_ordenado = sorted(info_grupos, key=lambda x: x[1], reverse=rever)
    
    #print(f'\n{"LPT" if rever else "SPT"} - Grupos ordenados por suma:')
    #for g, suma, indices in info_grupos_ordenado:
    #    print(f'  Grupo {g}: suma={suma:.0f}, trabajos={list(indices)}')
    
    return info_grupos_ordenado


def cromosoma_lpt_spt(regla: int, semilla: int,k_clusters,n_maquinas,tiempos_ops, secuencia_ops,perfil: bool) -> np.ndarray:
    """Cromosoma para LPT/SPT (replicado en todas las máquinas)"""
    
    grupos = km.k_agrupamiento(semilla,tiempos_ops,secuencia_ops, k_clusters ,perfil_agrupamiento=perfil)
    sf = aux.suma_por_fila(tiempos_ops)
    
    # Ordenamiento único
    if regla == 1:  # SPT
        info_grupos = base_regla(grupos, k_clusters, sf, rever=False)
    else:  # LPT (regla == 2)
        info_grupos = base_regla(grupos, k_clusters, sf, rever=True)
    
    indices_ordenados = aux.indices_de_info_ordenado(info_grupos) + 1
    
    # Replicar en todas las máquinas
    cromosoma = np.tile(indices_ordenados, (n_maquinas, 1))
    
    return cromosoma



