import random
import numpy as np
import Auxiliares as aux
#==============Mwr inicio
def cromosoma_mwr_lwr(n_maquinas,n_trabajos,n_max_operaciones,tiempos_ops,secuencia_ops,tipo=True):
    cromosoma=[[] for _ in range(n_maquinas)] #guardaremos aqui cromosoma
    tiempo_actual=0 # tiempo de reloj
    #es el indice actual de cada trabajo su index es el num trabajo [0] es J1
    indice_operacion = np.zeros(n_max_operaciones)
    #sumamos el tiempo total de cada trabajo
    tiempo_restante_r=aux.suma_por_fila(tiempos_ops)
    maquinas_reloj=np.zeros(n_maquinas)# El timepo que se libera la maquina 
    pendientes_siguientes=[]#primera/correspondiente actividad de cada job/trabajo
    todas_actividades=crear_actividades(secuencia_ops,tiempos_ops)#son todas las actividades
    
    trabajo_reloj=np.zeros(n_trabajos)
    #se anaden los primeras actividades de todos los trabajos
    #a pendientes
    for i in range(len(todas_actividades)):
        # 0 por que queremos el primero actividade del trabajo i 
        pendientes_siguientes.append(todas_actividades[i][0])
        #print(todas_actividades[i][0])

    #seguir hasta vaciar 
    while(comprobar_hay_mas_actividades(pendientes_siguientes)):
        #bandera se hizo algo?
        bandera=False
            # Recorrer TODOS los trabajos ordenados por prioridad
        trabajos_activos = [j for j in range(len(tiempo_restante_r)) if tiempo_restante_r[j] > 0]
        trabajos_activos.sort(key=lambda j: tiempo_restante_r[j], reverse=tipo)
        print(trabajos_activos)
        print(tiempo_actual)
        print(tiempo_restante_r)
        #time.sleep(0)
        
        for job_id in trabajos_activos:
            act_seleccionada = buscar_por_job(pendientes_siguientes, job_id + 1)
            if act_seleccionada != None:

                if tiempo_actual >= maquinas_reloj[act_seleccionada.maquina-1] and tiempo_actual>=trabajo_reloj[act_seleccionada.trabajo_id-1]:
                    # si tiempo actual es mayor igual a el tiempo de la maquina de la actividad seleccionada
                    #se hace la actividad, es decir se aumenta el tiempo de maquina

                    #aumentamos el reloj de la maquina
                    maquinas_reloj[act_seleccionada.maquina-1]= tiempo_actual+act_seleccionada.tiempo_duracion
                    trabajo_reloj[act_seleccionada.trabajo_id-1]=maquinas_reloj[act_seleccionada.maquina-1]
                    pendientes_siguientes.remove(act_seleccionada)
                    cromosoma[act_seleccionada.maquina-1].append(act_seleccionada.trabajo_id)
                    print(act_seleccionada)
                    print("termina maquina en tiempo",maquinas_reloj[act_seleccionada.maquina-1])
                    print("termina trabajo en tiempo",trabajo_reloj[act_seleccionada.trabajo_id-1])
                    bandera=True #se hizo algo
                    
                    tiempo_restante_r[act_seleccionada.trabajo_id-1]-= act_seleccionada.tiempo_duracion
                    if  act_seleccionada.siguiente != None:
                        print("Actividad Siguiente: ",act_seleccionada.siguiente)
                        pendientes_siguientes.append(act_seleccionada.siguiente)
        if bandera == False:
            tiempos_proximos = []
            tiempos_proximos.extend(maquinas_reloj)
            tiempos_proximos.extend(trabajo_reloj)
            
            tiempo_actual = min([t for t in tiempos_proximos if t > tiempo_actual])
    cromosoma=completar_listas_con_semilla(cromosoma,n_trabajos,semilla=100)
    return cromosoma

def completar_listas_con_semilla(listas,n_trabajos, semilla=42):
    """
    Completa listas incompletas con números faltantes de forma aleatoria.
    
    Args:
        listas: Lista de listas con números del 1 al n_maquinas (pueden estar incompletas)
        semilla: Valor de semilla para reproducibilidad (default: 42)
    
    Returns:
        Lista de listas completadas con los números faltantes distribuidos aleatoriamente
    """
    
    random.seed(semilla)
    
    resultado = []
    
    for lista in listas:
        # Encontrar números faltantes del 1 al n_maquinas
        numeros_presentes = set(lista)
        numeros_faltantes = [i for i in range(1, n_trabajos + 1) if i not in numeros_presentes]
        
        # Mezclar aleatoriamente los números faltantes
        random.shuffle(numeros_faltantes)
        
        # Crear la lista completa con números faltantes agregados
        lista_completada = lista + numeros_faltantes
        resultado.append(lista_completada)
    
    return np.array(resultado)

def buscar_por_job(lista,job):
    for actividad in lista:
        if actividad.trabajo_id==job:
            return actividad
    return None    

def comprobar_hay_mas_actividades(lista):
    # Retorna True si la lista NO está vacía
    return len(lista) > 0

def crear_actividades(secuencia_ops,tiempos_ops):
    lista_actividades=[]
    for trabajo in range(len(secuencia_ops)):
        actividades_trabajo = []
        
        # Recorrer las máquinas de atrás hacia adelante
        for maquina in reversed(secuencia_ops[trabajo]):
            if maquina != 0:
                duracion = tiempos_ops[trabajo][maquina-1]  # en secuencia el 1 seria indice 0
                actividad = Actividad(duracion, trabajo+1,maquina)  # va de 0 a n entonces +1 hace que empiece en 1
                
                # Si ya hay actividades, encadenar a la anterior
                if actividades_trabajo:
                    actividad.siguiente = actividades_trabajo[-1]
                
                actividades_trabajo.append(actividad)
        
        actividades_trabajo.reverse()# revertir ya que empezamos de fin al comienzo en la creacion
        #agrega la lista como 1 elemento
        lista_actividades.append(actividades_trabajo)
    
    return lista_actividades
class Actividad:
    """Representa una actividad dentro de un trabajo"""
    def __init__(self, tiempo_duracion, trabajo_id,maquina_id):
        self.tiempo_duracion = tiempo_duracion  # en minutos o segundos
        self.trabajo_id = trabajo_id
        self.maquina=maquina_id
        self.siguiente = None  # Referencia a la siguiente actividad
    
    def __repr__(self):
        return f"Actividad({self.tiempo_duracion}s,maquina={self.maquina} ,trabajo_id={self.trabajo_id})"

def indice_mayor(lista):
    return np.argmax(lista) if len(lista) > 0 else None
#===================== fin mwr