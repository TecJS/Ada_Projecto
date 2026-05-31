import numpy as np
import random
import math
import time
import Configuraciones as conf
from typing import List, Tuple, Dict, Union
import time
import leer_csv
import guarda_resultado 
import grafica
# ==============================================================================
# ALGORITMO GENÉTICO PARA JSSP BASADO EN PSEUDOCÓDIGO DEL USUARIO
# ==============================================================================

# 1. Asignar cantidad de trabajos y máquinas
n_trabajos = 8
n_maquinas = 14
n_individuos = 100
m_generaciones = 50
k_torneo = 20
k_clusters = 3
n_max_operaciones=5

semillaAG=3812
#=====================Leer excel
tipo_caso="mediano"
semilla=100 #semilla de instancia
secuencia_ops, tiempos_ops, n_trabajos, n_maquinas = leer_csv.leer_instancia_jssp(tipo_caso, semilla).values()
print(secuencia_ops)
print(tiempos_ops)
#====================================
# Función Auxiliar: Cruza PMX (CORREGIDA PARA EVITAR BUCLE INFINITO)
def cruza_pmx(padreA, padreB, celdas):
    cortes = sorted(random.sample(range(1, celdas - 1), 2))
    inicio, fin = cortes[0], cortes[1]
    
    hijoA = np.full(celdas, -1)
    hijoB = np.full(celdas, -1)
    
    hijoA[inicio:fin+1] = padreB[inicio:fin+1]
    hijoB[inicio:fin+1] = padreA[inicio:fin+1]
    
    def rellenar_extremos(hijo, p_origen):
        for c in range(celdas):
            if c < inicio or c > fin:
                val = p_origen[c]
                centro_hijo = hijo[inicio:fin+1]
                # Bucle de reparación estricto al centro
                while val in centro_hijo:
                    ind_relativo = np.where(centro_hijo == val)[0][0]
                    ind_real = inicio + ind_relativo
                    # Corrección Clave: Tomar el valor del padre correcto en ese índice
                    val = p_origen[ind_real]
                hijo[c] = val
        return hijo

    hijoA = rellenar_extremos(hijoA, padreA)
    hijoB = rellenar_extremos(hijoB, padreB)
    
    return hijoA, hijoB

# Función Auxiliar: Obtener Makespan
def calcular_makespan(cromosoma, tiempos, secuencias):
    tiempo_maq = np.zeros(cromosoma.shape[0])
    tiempo_trabajo = np.zeros(cromosoma.shape[1])
    paso_trabajo = np.zeros(cromosoma.shape[1], dtype=int) 
    
    operaciones_pendientes = np.sum(tiempos > 0)
    
    while operaciones_pendientes > 0:
        asignacion_hecha = False
        for col in range(cromosoma.shape[1]):
            for m in range(cromosoma.shape[0]):
                trabajo = cromosoma[m, col] - 1 
                if paso_trabajo[trabajo] < secuencias.shape[1]:
                    maq_requerida = secuencias[trabajo, paso_trabajo[trabajo]]
                    if maq_requerida != 0 and maq_requerida == (m + 1):
                        t_inicio = max(tiempo_maq[m], tiempo_trabajo[trabajo])
                        t_fin = t_inicio + tiempos[trabajo, m]
                        
                        tiempo_maq[m] = t_fin
                        tiempo_trabajo[trabajo] = t_fin
                        
                        paso_trabajo[trabajo] += 1
                        operaciones_pendientes -= 1
                        asignacion_hecha = True
                        
        if not asignacion_hecha:
            break 
            
    if operaciones_pendientes > 0:
        return float('inf')
        
    return np.max(tiempo_maq)


# ==============================================================================
# INICIO DE EJECUCIÓN
# ==============================================================================
def ejecucion(config_poblacion):
    random.seed(semillaAG)
    start_time = time.time()
    print("Creando población inicial...")
    historial_makespan=[]
    # 5. Crear Población Inicial
    poblacion = config_poblacion

    mejor_historico_cromosoma = None
    mejor_historico_makespan = float('inf')

    # 6. Evolución
    print("Iniciando Evolución...")
    for gen in range(1, m_generaciones + 1):
        
        # a. Obtener makespan
        makespans = np.array([calcular_makespan(ind, tiempos_ops, secuencia_ops) for ind in poblacion])
        
        # b. Peor y Mejor
        peor_makespan = np.max(makespans)
        idx_peor = np.argmax(makespans)
        idx_mejor = np.argmin(makespans)
        
        if makespans[idx_mejor] < mejor_historico_makespan:
            mejor_historico_makespan = makespans[idx_mejor]
            mejor_historico_cromosoma = np.copy(poblacion[idx_mejor])

        historial_makespan.append(mejor_historico_makespan)
           
        # c. Elitismo
        if gen > 1:
            poblacion[idx_peor] = np.copy(mejor_historico_cromosoma)
            makespans[idx_peor] = mejor_historico_makespan
            
        # d. Fitness
        makespans_validos = makespans[makespans != float('inf')]
        max_valido = np.max(makespans_validos) if len(makespans_validos) > 0 else 0
        
        fitness = np.zeros(n_individuos)
        for i in range(n_individuos):
            if makespans[i] == float('inf'):
                fitness[i] = 0
            else:
                fitness[i] = max_valido - makespans[i]
                
        # f. Torneo
        ganadores = []
        for i in range(n_individuos):
            participantes = random.sample(range(n_individuos), k_torneo)
            idx_ganador = max(participantes, key=lambda idx: fitness[idx])
            ganadores.append(np.copy(poblacion[idx_ganador]))
            
        # g. Cruza
        nueva_generacion = []
        limite_cruzas = math.floor((n_individuos * 0.95) / 2)
        
        for i in range(limite_cruzas):
            idx_padres = random.sample(range(n_individuos), 2)
            padreA = ganadores[idx_padres[0]]
            padreB = ganadores[idx_padres[1]]
            
            hijoA_matriz = np.zeros((n_maquinas, n_trabajos), dtype=int)
            hijoB_matriz = np.zeros((n_maquinas, n_trabajos), dtype=int)
            
            for f in range(n_maquinas):
                hA, hB = cruza_pmx(padreA[f, :], padreB[f, :], n_trabajos)
                hijoA_matriz[f, :] = hA
                hijoB_matriz[f, :] = hB
                
            nueva_generacion.append(hijoA_matriz)
            nueva_generacion.append(hijoB_matriz)
            
        # h. Clonar el resto
        mientras_falten = n_individuos - len(nueva_generacion)
        if mientras_falten > 0:
            idx_clones = random.sample(range(n_individuos), mientras_falten)
            for clon in idx_clones:
                nueva_generacion.append(np.copy(ganadores[clon]))
                
        # MÚTACIÓN DINÁMICA
        porcentaje_gen = gen / m_generaciones
        if porcentaje_gen <= 0.25: tasa_muta = 0.02
        elif porcentaje_gen <= 0.50: tasa_muta = 0.03
        elif porcentaje_gen <= 0.60: tasa_muta = 0.04
        else: tasa_muta = 0.05
            
        num_mutar = max(1, round(n_individuos * tasa_muta))
        idx_a_mutar = random.sample(range(n_individuos), num_mutar)
        
        for idx in idx_a_mutar:
            cromosoma_mutar = nueva_generacion[idx]
            for maq in range(n_maquinas):
                tipo = random.choice(["intercambio", "inversion"])
                pts = sorted(random.sample(range(n_trabajos), 2))
                
                if tipo == "intercambio":
                    temp = cromosoma_mutar[maq, pts[0]]
                    cromosoma_mutar[maq, pts[0]] = cromosoma_mutar[maq, pts[1]]
                    cromosoma_mutar[maq, pts[1]] = temp
                else:
                    cromosoma_mutar[maq, pts[0]:pts[1]+1] = np.flip(cromosoma_mutar[maq, pts[0]:pts[1]+1])
                    
            nueva_generacion[idx] = cromosoma_mutar
            
        poblacion = nueva_generacion
        
        if gen % 10 == 0:
            print(f"Generación {gen} procesada... Mejor maxpans{mejor_historico_makespan}")
            

    end_time = time.time()
    print("\n" + "="*50)
    print(f"Ejecución Finalizada en {round(end_time - start_time, 2)} segundos.")
    print(f"Mejor Makespan encontrado: {mejor_historico_makespan} minutos.")
    print("="*50)
    guarda_resultado.guardar_resultado_ag(tipo_caso,
    semilla,
    n_trabajos,
    n_maquinas,
    mejor_historico_makespan,
    mejor_historico_cromosoma)
    grafica.graficar_convergencia_ag(m_generaciones, historial_makespan, tipo_caso, semilla)
    #historial_makespan=[]#limpia el hisotrial para la proxima ejecucion
    return
#=============================Guardar resultado



#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("Configuracion A")
ejecucion(conf.merge_config_a(n_individuos,n_trabajos,n_maquinas))
print("Configuracion B")
ejecucion(conf.merge_config_b(k_clusters,n_maquinas,tiempos_ops,n_individuos,n_trabajos,secuencia_ops,n_max_operaciones))
print("Configuracion C")
ejecucion(conf.merge_config_c(k_clusters,n_maquinas,tiempos_ops,n_individuos,n_trabajos,secuencia_ops,n_max_operaciones))
print("Configuracion D")
ejecucion(conf.merge_config_d(k_clusters,n_maquinas,tiempos_ops,n_individuos,n_trabajos,secuencia_ops,n_max_operaciones))


#print(cromosoma_mwr_lwr())
#print(poblacion1_permutacion()[0])