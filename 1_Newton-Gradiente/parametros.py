__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos nativos de python
import numpy as np
import scipy.linalg
import random

def generar_datos(dimension):
    """
    Esta funcion crea una matriz cuadrada semidefinida positiva parada
    ocuparla en los programas presentados.
    """

    # Se crea un vector aleatorio segun la dimension entregada
    vector = np.random.rand(dimension, dimension)
    # Se obtienen las dimensiones del vector
    m, n = vector.shape

    # Se crea una matriz que contenga en su diagonal
    # el vector ingresado como argumento
    D = np.diag(np.diag(vector))
    B = scipy.linalg.orth(np.random.rand(n,n))
    Q = np.transpose(B)*D*B
    b = np.random.rand(n, 1)

    # Retorna la matriz y vector listo para ejecutar
    return Q, b
