import os
import random
import numpy as np
import pandas as pd


def generar_instancia_jssp(tipo_caso, semilla=100):
    # Fijamos la semilla para reproducibilidad
    random.seed(semilla)
    np.random.seed(semilla)

    # ---------------------------------------------------------
    # PARTE 1: Configuración de Parámetros según el Caso
    # ---------------------------------------------------------
    if tipo_caso == "base":
        num_trabajos = 8
        num_maquinas = 14
        min_ops = 1
        max_ops = 5
    elif tipo_caso == "mediano":
        num_trabajos = 15
        num_maquinas = 14
        min_ops = 5
        max_ops = 7
    elif tipo_caso == "grande":
        num_trabajos = 30
        num_maquinas = 20
        min_ops = 8
        max_ops = 10
    else:
        raise ValueError("Caso no válido. Usa 'base', 'mediano' o 'grande'.")

    # ---------------------------------------------------------
    # PARTE 2: Construcción de las Matrices (Llenas de 0s al inicio)
    # ---------------------------------------------------------
    # Creamos matrices de ceros con numpy
    matriz_secuencia = np.zeros((num_trabajos, max_ops), dtype=int)
    matriz_tiempos = np.zeros((num_trabajos, num_maquinas), dtype=int)

    # En Python los índices empiezan en 0, por lo que las máquinas irán de 1 a num_maquinas
    lista_maquinas = list(range(1, num_maquinas + 1))
    lista_tiempos_posibles = list(range(10, 120))  # 10 a 120 inclusivo

    for i in range(num_trabajos):
        # Determinamos al azar cuántas operaciones tendrá este trabajo
        k_ops = random.randint(min_ops, max_ops)

        # Elegimos 'k_ops' máquinas distintas para formar la ruta del trabajo (sin reemplazo)
        ruta = random.sample(lista_maquinas, k_ops)

        # Generamos los tiempos para esas operaciones (con reemplazo)
        tiempos = random.choices(lista_tiempos_posibles, k=k_ops)

        # Guardamos la secuencia (los ceros restantes quedan intactos al final de la fila)
        matriz_secuencia[i, :k_ops] = ruta

        # Llenamos la matriz de tiempos en las columnas de las máquinas correspondientes
        for op in range(k_ops):
            maquina_asignada = ruta[op]
            # Restamos 1 a maquina_asignada porque los índices de las columnas en Python van de 0 a N-1
            matriz_tiempos[i, maquina_asignada - 1] = tiempos[op]

    # Convertimos a DataFrames de Pandas para etiquetar filas y columnas como en R
    filas_trabajos = [f"J{x}" for x in range(1, num_trabajos + 1)]
    columnas_ops = [f"Op{x}" for x in range(1, max_ops + 1)]
    columnas_maquinas = [f"M{x}" for x in range(1, num_maquinas + 1)]

    secuencia_ops = pd.DataFrame(
        matriz_secuencia, index=filas_trabajos, columns=columnas_ops
    )
    tiempos_ops = pd.DataFrame(
        matriz_tiempos, index=filas_trabajos, columns=columnas_maquinas
    )

    # ---------------------------------------------------------
    # PARTE 3: Exportación a Archivos CSV
    # ---------------------------------------------------------
    # 1. Ruta de destino (Usa barras normales '/' o doble barra '\\' en Windows)
    ruta_destino = "/"

    # Nota opcional: Crea la carpeta si no existe para evitar errores
    if not os.path.exists(ruta_destino):
        os.makedirs(ruta_destino)

    # 2. Concatena la ruta con el nombre de tus archivos
    archivo_secuencia = f"{ruta_destino}instancia_{tipo_caso}_secuencia_{semilla}.csv"
    archivo_tiempos = f"{ruta_destino}instancia_{tipo_caso}_tiempos_{semilla}.csv"

    # 3. Exportación a CSV (index_label=' ' emula el comportamiento por defecto de R de dejar la celda A1 vacía)
    secuencia_ops.to_csv(archivo_secuencia, index_label=" ")
    tiempos_ops.to_csv(archivo_tiempos, index_label=" ")

    print(
        f"¡Éxito! Instancia {tipo_caso.upper()} generada y guardada en CSV con semilla {semilla}"
    )

    # Retornamos un diccionario (el equivalente a list() en R) por si se usa en memoria
    return {"secuencia": secuencia_ops, "tiempos": tiempos_ops}


# ==========================================
# EJECUCIÓN PARA CREAR LOS 3 CASOS DE PRUEBA
# ==========================================
instancia_base = generar_instancia_jssp("base", semilla=100)
instancia_mediana = generar_instancia_jssp("mediano", semilla=100)
instancia_grande = generar_instancia_jssp("grande", semilla=100)