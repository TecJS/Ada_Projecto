import numpy as np
def poblacion1_permutacion(n_individuos,n_trabajos,n_maquinas):
    pobla1=[]
    for i in range(n_individuos):
        cromosoma = np.array([np.random.permutation(np.arange(1, n_trabajos + 1)) for _ in range(n_maquinas)])
        pobla1.append(cromosoma)
    return pobla1
