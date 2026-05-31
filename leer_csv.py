import os
import pandas as pd
import numpy as np

def leer_instancia_jssp(tipo_caso, semilla=100):
    # Crear los nombres de los archivos usando f-strings
    archivo_secuencia = f"instancia_{tipo_caso}_secuencia_{semilla}.csv"
    archivo_tiempos = f"instancia_{tipo_caso}_tiempos_{semilla}.csv"

    # Verificar que los archivos existan
    if not os.path.exists(archivo_secuencia):
        raise FileNotFoundError(
            f"No se encontró el archivo: {archivo_secuencia}\n"
            f"Solución: ejecuta primero el PASO 1 para generar los CSV."
        )
        
    if not os.path.exists(archivo_tiempos):
        raise FileNotFoundError(
            f"No se encontró el archivo: {archivo_tiempos}\n"
            f"Solución: ejecuta primero el PASO 1 para generar los CSV."
        )

    # Leer CSVs
    # index_col=0 equivale a row.names=1 en R (usa la primera columna como índice)
    # .to_numpy() equivale a as.matrix() en R
    secuencia_ops = pd.read_csv(archivo_secuencia, index_col=0).to_numpy()
    tiempos_ops = pd.read_csv(archivo_tiempos, index_col=0).to_numpy()

    # Extraer dimensiones (.shape en Python devuelve (filas, columnas))
    n_trabajos = secuencia_ops.shape[0] # Equivalente a nrow()
    n_maquinas = tiempos_ops.shape[1]   # Equivalente a ncol()

    # Imprimir el mensaje en consola
    print(f"Instancia '{tipo_caso}' cargada: {n_trabajos} trabajos, {n_maquinas} maquinas (semilla {semilla})")

    # Retornar un diccionario (equivalente a la list() con nombres de R)
    return {
        "secuencia": secuencia_ops,
        "tiempos": tiempos_ops,
        "n_trabajos": n_trabajos,
        "n_maquinas": n_maquinas
    }
