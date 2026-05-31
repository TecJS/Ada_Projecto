import numpy as np
import random
import math
import time

# ==============================================================================
# ALGORITMO GENÉTICO PARA JSSP BASADO EN PSEUDOCÓDIGO DEL USUARIO
# ==============================================================================

# 1. Asignar cantidad de trabajos y máquinas
n_trabajos = 8
n_maquinas = 14
n_individuos = 20
m_generaciones = 50
k_torneo = 3

# 3. Establecer secuencia de operaciones (Orden de máquinas para cada trabajo J1 a J8)
secuencia_ops = np.array([
    [1,  3,  0,  0, 0],  # J1
    [7, 13,  5,  1, 3],  # J2
    [7, 14,  5,  9, 0],  # J3
    [6,  0,  0,  0, 0],  # J4
    [10, 0,  0,  0, 0],  # J5
    [1,  3,  0,  0, 0],  # J6
    [6, 12, 11,  0, 0],  # J7
    [11, 0,  0,  0, 0]   # J8
])

# 4. Establecer la matriz de tiempos (Trabajo x Máquina)
tiempos_ops = np.array([
    # M1, M2, M3, M4, M5, M6, M7, M8, M9, M10, M11, M12, M13, M14
    [30,  0, 10,  0,  0,  0,  0,  0,  0,   0,   0,   0,   0,   0], # J1
    [120, 0, 30,  0, 20,  0, 30,  0,  0,   0,   0,   0,  30,   0], # J2
    [0,   0,  0,  0, 20,  0, 30,  0, 90,   0,   0,   0,   0,  30], # J3
    [0,   0,  0,  0,  0, 10,  0,  0,  0,   0,   0,   0,   0,   0], # J4
    [0,   0,  0,  0,  0,  0,  0,  0,  0,  20,   0,   0,   0,   0], # J5
    [120, 0, 30,  0,  0,  0,  0,  0,  0,   0,   0,   0,   0,   0], # J6
    [0,   0,  0,  0,  0, 20,  0,  0,  0,   0,  20,  20,   0,   0], # J7
    [0,   0,  0,  0,  0,  0,  0,  0,  0,   0,  20,   0,   0,   0]  # J8
])

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
start_time = time.time()
print("Creando población inicial...")

# 5. Crear Población Inicial
poblacion = []
for i in range(n_individuos):
    cromosoma = np.array([np.random.permutation(np.arange(1, n_trabajos + 1)) for _ in range(n_maquinas)])
    poblacion.append(cromosoma)

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
        print(f"Generación {gen} procesada...")

end_time = time.time()
print("\n" + "="*50)
print(f"Ejecución Finalizada en {round(end_time - start_time, 2)} segundos.")
print(f"Mejor Makespan encontrado: {mejor_historico_makespan} minutos.")
print("="*50)