__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"

# Se importan los modulos de python
import numpy as np
import scipy.linalg

# Se importan los modulos creados por el usuario
from parametros import *


def timer(funcion):
    """
    Se crea un decorador (googlear) del tipo timer para testear el tiempo
    de ejecucion del programa
    """
    def inner(*args, **kwargs):

        inicio = time.time()
        resultado = funcion(*args, **kwargs)
        final = round(time.time() - inicio, 3)
        print("\nTiempo de ejecucion total: {}[s]".format(final))

        return resultado
    return inner

def LASSO(A, b, tau, iteracion_maxima):
    """
    Esta funcion recibe como input una matriz A y un vector b. Se busca resolver
    el problema de regularizacion L1 con un parametro tau y haciendo un numero maximo
    de iteraciones definidas por el usuario, mediante el metodo del subgradiente.

    Su entrada posee:
        - A : Matriz de m muestras (filas) de cada variable n (columnas).
        - b : Matriz de m muestras obtenidas que depende de las n variables.
        - tau: Escalar que entrega significancia a las variables o entrega
               significancia al error del modelo (trade-off).
        - iteracion_maxima : Numero maximo de iteraciones a realizar.

    Su salida es:
        - valor_optimo : Valor optimo del problema a minimizar.

    """

    # Dimensiones correspondientes
    m, n = A.shape

    # Se setean los valores de las iteraciones k, k-1 y k-2, respectivamente
    xk = np.zeros((n, 1))
    xk_1 = xk
    xk_2 = xk_1

    # Se setea el angulo entre las soluciones
    angulo = 0
    a = 0.001

    # Se despliega el mensaje en pantalla
    print("\n\n**********    METODO DE SUBGRADIENTE    *********\n")
    print("ITERACION     VALOR OBJ      ERROR       ANGULO")

    # Comienza el algoritmo
    for iteracion in range(iteracion_maxima):

        # 1º Se calcula el subgradiente de la funcion objetivo
        subgradiente = 2*np.dot(np.transpose(A), np.dot(A, xk) - b) + tau*np.sign(xk)

        # 2º Se actualiza el pasado
        xk_2 = xk_1
        xk_1 = xk

        # 3º Se actualiza el valor objetivo
        theta = a/np.sqrt(iteracion+1)
        xk = xk - theta*subgradiente

        # 4º Se evalua el error de ajuste
        error = (np.linalg.norm(np.dot(A, xk) - b)) / np.linalg.norm(b)

        # 5º Se evalua el valor en la funcion objetivo
        valor = np.linalg.norm(np.dot(A, xk) - b, 2)**2 + tau*np.linalg.norm(xk, 1)

        n1 = np.linalg.norm(xk, 1)
        
         # La rutina de subgradiente muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        #  error de ajuste y la norma 1 de xk.
        retorno_en_pantalla = [iteracion, valor, error, n1]
#        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")
        print("%12.6f %12.6f %12.6f %12.6f" % (retorno_en_pantalla[0],retorno_en_pantalla[1],retorno_en_pantalla[2],retorno_en_pantalla[3]))
    return xk

if __name__ == '__main__':
    # Esto es para que simepre se generen los mismos numeros aleatorios
    np.random.seed(1000)

    tau = 0.5
    iteracion_maxima = 20000
    
    A, b = generar_datos(50, 300)
    xsol = LASSO(A, b, tau, iteracion_maxima)


