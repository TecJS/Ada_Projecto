import permutacion as pm
import CreaPoblacion as pobla
# ============================================================================
def merge_config_a(n_individuos,n_trabajos,n_maquinas):
    """
    Configuración A: 100% aleatoria
    """
    lista_aleatoria = pm.poblacion1_permutacion(n_individuos,n_trabajos,n_maquinas,seed=523)
    return lista_aleatoria

def merge_config_b(k_clusters,n_maquinas,tiempos_ops,n_individuos,n_trabajos,secuencia_ops,n_max_operaciones):
    """
    Configuración B: 70% KM Perfil 1 + SPT, 30% aleatoria
    """
    lista_km_perfil1 = pobla.crear_poblacion(regla=1, perfil=True,
                                             k_clusters=k_clusters,n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,n_individuos=n_individuos,
                                             secuencia_ops=secuencia_ops,n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=291)
    lista_aleatoria = pm.poblacion1_permutacion(n_individuos,n_trabajos,n_maquinas,seed=231)

    size_km = int(len(lista_km_perfil1) * 0.7)
    size_random = int(len(lista_aleatoria) * 0.3)
    
    return lista_km_perfil1[:size_km] + lista_aleatoria[:size_random]

def merge_config_c(k_clusters,n_maquinas,tiempos_ops,n_individuos,n_trabajos,secuencia_ops,n_max_operaciones):
    """
    Configuración C: 40% KM Perfil 1, 40% KM Perfil 2, 20% aleatoria
    """
    lista_km_perfil1 = pobla.crear_poblacion(regla=1, perfil=True,k_clusters=k_clusters,
                                             n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,
                                             n_individuos=n_individuos,secuencia_ops=secuencia_ops, 
                                             n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=589)
    lista_km_perfil2 = pobla.crear_poblacion(regla=1, perfil=False, k_clusters=k_clusters,
                                             n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,
                                             n_individuos=n_individuos,secuencia_ops=secuencia_ops,
                                             n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=296)
    lista_aleatoria = pm.poblacion1_permutacion(n_individuos,n_trabajos,n_maquinas,seed=3452)

    size_p1 = int(len(lista_km_perfil1) * 0.4)
    size_p2 = int(len(lista_km_perfil2) * 0.4)
    size_random = int(len(lista_aleatoria) * 0.2)
    
    return lista_km_perfil1[:size_p1] + lista_km_perfil2[:size_p2] + lista_aleatoria[:size_random]

def merge_config_d(k_clusters,n_maquinas,tiempos_ops,n_individuos,n_trabajos,secuencia_ops,n_max_operaciones):
    """
    Configuración D: 20% KM Perfil 1 + SPT, 20% KM Perfil 1 + LPT, 20% KM Perfil 2 + MWR, 20% KM Perfil 2 + regla, 20% aleatoria
    """

    lista_km_perfil1_spt=pobla.crear_poblacion(regla=1, perfil=True,k_clusters=k_clusters,
                                               n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,
                                               n_individuos=n_individuos,secuencia_ops=secuencia_ops, 
                                               n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=234)
    lista_km_perfil1_lpt=pobla.crear_poblacion(regla=2, perfil=True, k_clusters=k_clusters,
                                               n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,
                                               n_individuos=n_individuos,secuencia_ops=secuencia_ops,
                                               n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=810)
    lista_km_perfil2_mwr=pobla.crear_poblacion(regla=3, perfil=False, k_clusters=k_clusters,
                                               n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,
                                               n_individuos=n_individuos,secuencia_ops=secuencia_ops,
                                               n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=903)    
    lista_km_perfil2_swr=pobla.crear_poblacion(regla=4, perfil=False, k_clusters=k_clusters,
                                               n_maquinas=n_maquinas,tiempos_ops=tiempos_ops,
                                               n_individuos=n_individuos,secuencia_ops=secuencia_ops,
                                               n_trabajos=n_trabajos,n_max_operaciones=n_max_operaciones,semilla_inicial=280) 
    lista_aleatoria = pm.poblacion1_permutacion(n_individuos,n_trabajos,n_maquinas,seed=1457)

    size_p1_spt = int(len(lista_km_perfil1_spt) * 0.2)
    size_p1_lpt = int(len(lista_km_perfil1_lpt) * 0.2)
    size_p2_mwr = int(len(lista_km_perfil2_mwr) * 0.2)
    size_p2_swr = int(len(lista_km_perfil2_swr) * 0.2)
    size_random = int(len(lista_aleatoria) * 0.2)
    
    return (lista_km_perfil1_spt[:size_p1_spt] + 
            lista_km_perfil1_lpt[:size_p1_lpt] + 
            lista_km_perfil2_mwr[:size_p2_mwr] + 
            lista_km_perfil2_swr[:size_p2_swr] + 
            lista_aleatoria[:size_random])
