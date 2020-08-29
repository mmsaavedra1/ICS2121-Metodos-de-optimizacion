__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos nativos de python
import numpy as np
import scipy.linalg
import random


def generar_datos(m, n):
    """
    Esta funcion crea una matriz cuadrada semidefinida positiva parada
    ocuparla en los programas presentados.
    """

    # Se crea un vector aleatorio segun la dimension entregada
    A = np.random.rand(m, n)
    b = np.random.rand(m, 1)

    # Retorna la matriz y vector listo para ejecutar
    return A, b


if __name__ == '__main__':
    A, b = generar_datos(5, 5)
    print(b)
