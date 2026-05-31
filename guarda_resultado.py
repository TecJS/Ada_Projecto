import pandas as pd


def guardar_resultado_ag(
    tipo_caso,
    semilla,
    n_trabajos,
    n_maquinas,
    mejor_historico_makespan,
    mejor_historico_cromosoma,
):
    """Guarda los resultados del Algoritmo Genético en un archivo CSV estructurado.

    Parámetros:
    - tipo_caso: str, nombre de la instancia.
    - semilla: int, semilla utilizada.
    - n_trabajos: int, número de trabajos.
    - n_maquinas: int, número de máquinas.
    - mejor_historico_makespan: float/int, el mejor makespan encontrado.
    - mejor_historico_cromosoma: list/array, la secuencia del mejor cromosoma.
    """
    # Definir el nombre del archivo de salida
    archivo_salida = f"Resultado_AG_{tipo_caso}_{semilla}.csv"

    # Encabezado (Dataframe)
    info = pd.DataFrame(
        {
            "Parametro": [
                "Instancia",
                "Semilla",
                "Trabajos",
                "Maquinas",
                "Mejor_Makespan",
            ],
            "Valor": [
                tipo_caso,
                semilla,
                n_trabajos,
                n_maquinas,
                mejor_historico_makespan,
            ],
        }
    )

    # Guardar el primer DataFrame (crea el archivo o lo sobrescribe si ya existía)
    info.to_csv(archivo_salida, index=False)

    # Abrir el archivo en modo 'append' ('a') para agregar el resto de los bloques
    with open(archivo_salida, mode="a", encoding="utf-8") as f:
        # 1. Línea vacía con dos columnas
        f.write("\n,\n")

        # 2. Título del cromosoma
        f.write("MEJOR_CROMOSOMA,\n")

        # 3. Cromosoma (convierte listas/arrays a texto separado por comas)
        if isinstance(mejor_historico_cromosoma, (list, tuple)):
            linea_cromosoma = ",".join(map(str, mejor_historico_cromosoma))
        else:
            linea_cromosoma = str(mejor_historico_cromosoma)

        f.write(f"{linea_cromosoma}\n")

    print(f"\nResultado guardado en: {archivo_salida}\n")

    # Opcional: retornar el nombre del archivo por si lo necesitas después
    return archivo_salida