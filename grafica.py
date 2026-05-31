import matplotlib.pyplot as plt
import os

def graficar_convergencia_ag(m_generaciones, historial_makespan, tipo_caso, semilla):
    """Genera y muestra la gráfica de convergencia del Algoritmo Genético.

    Parámetros:
    - m_generaciones: int, número total de generaciones.
    - historial_makespan: list o array, el mejor makespan registrado en cada generación.
    - tipo_caso: str, nombre de la instancia.
    - semilla: int, semilla utilizada.
    """
    # Definir el título dinámico (equivalente a paste y toupper de R)
    titulo = f"Convergencia AG — {tipo_caso.upper()} | Semilla: {semilla}"

    # Crear la figura (puedes ajustar el tamaño aquí)
    plt.figure(figsize=(8, 5))

    # Graficar los datos (se usa range(1, m_generaciones + 1) para que el eje X empiece en 1)
    plt.plot(
        range(1, m_generaciones + 1),
        historial_makespan,
        color="steelblue",
        linewidth=2,
    )

    # Configurar etiquetas, título y cuadrícula
    plt.xlabel("Generación")
    plt.ylabel("Mejor Makespan")
    plt.title(titulo)
    plt.grid(True, linestyle="--", alpha=0.6)

   # --- CONTROL DE SOBRESCRITURA ---
    inicial_mk = int(historial_makespan[0])
    final_mk = int(historial_makespan[-1])

    # Nombre base y extensión
    nombre_base = f"convergencia_{tipo_caso.lower()}_semilla_{semilla}_mk_{inicial_mk}_a_{final_mk}"
    extension = ".png"

    nombre_archivo = f"{nombre_base}{extension}"

    # Bucle para añadir un número si el archivo ya existe
    contador = 1
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"{nombre_base}_{contador}{extension}"
        contador += 1
    # ----------------------------------------
    # Guardar la gráfica antes de mostrarla
    plt.savefig(nombre_archivo, dpi=300, bbox_inches="tight")
    print(f"Gráfica guardada exitosamente como: {nombre_archivo}")

    # -----------------------------------------
    # Mostrar la gráfica
    plt.show()