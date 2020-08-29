__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"

# Se importan los modulos de python
import numpy as np
import scipy.linalg
import time 

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

@timer
def LASSO(A, b, tau, iteracion_maxima):
    """
    Esta funcion recibe como input una matriz A y un vector b. Se busca resolver
    el problema de regulacion L1 con un parametro tau y haciendo un numero maximo
    de iteraciones definidas por el usuario, mediante el metodo del subgradiente.

    Su entrada posee:
        - A : Matriz de m muestras (filas) de cada variable n (columnas).
        - b : Matriz de m muestras obtenidas que depende de las n variables.
        - tau: Escalar que entrega significancia a las variables o entrega
               significancia al error del modelo (trade-off).
        - iteracion_maxima : Numero maximo de iteraciones a realizar.

    Su salida es:
        - valor_optimo : Valor optimo del problema a minimizar.
        - xk : Vector solucion del problema de k iteraciones.

    """

    # Dimensiones correspondientes
    m, n = A.shape

    # Se setean los valores de las iteraciones k, k-1 y k-2, respectivamente
    xk = np.zeros((n, 1))
    xk_1 = xk
    xk_2 = xk_1

    # Se setea el angulo entre las soluciones
    angulo = 0

    # Estimacion del valor de R (radio) y L (connstante de Lipschitz)
    # segun teoria vista en clases
    R = np.sqrt(np.linalg.norm(np.linalg.inv(np.dot(A, np.transpose(A))))*np.linalg.norm(b))
    L = tau*np.sqrt(n) + np.linalg.norm(np.dot(A, np.transpose(A)))*R + np.linalg.norm(np.dot(np.transpose(A), b))

    # Numero de iteraciones segun el teorema de la convergencia (NOS AHORAMOS EL LINESEARCH)
    thetak = R/(L*np.sqrt(iteracion_maxima+1))

    # Se despliega el mensaje en pantalla
    print("\n\n**********    METODO DE SUBGRADIENTE    *********\n")
    print("ITERACION     VALOR OBJ      ERROR       ANGULO")

    # Comienza el algoritmo
    for iteracion in range(iteracion_maxima):

        # 1º Se calcula el gradiente de la funcion objetivo
        subgradiente = 2*np.dot(np.transpose(A), np.dot(A, xk) - b) + tau*np.sign(xk)

        # 2º Se actualiza el pasado
        xk_2 = xk_1
        xk_1 = xk

        # 3º Se actualiza el valor objetivo
        xk = xk - thetak*subgradiente

        # 4º Se evalua el error de ajuste
        error = np.amax(np.abs(np.dot(A, xk) - b)) / np.amax(np.abs(b))

        # 5º Se evalua el valor en la funcion objetivo
        valor = np.linalg.norm(np.dot(A, xk) - b, 2)**2 + tau*np.linalg.norm(xk, 1)

        if iteracion >= 3:
            # 6º Se calcula el angulo entre las soluciones
            diferencia1 = xk - xk_1
            diferencia2 = xk_2 - xk_1
            angulo = np.dot(np.transpose(diferencia2), diferencia1)/(np.linalg.norm(diferencia2)*np.linalg.norm(diferencia1))
            angulo = angulo[0][0]


         # La rutina de subgradiente muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        #  error y angulo formado por las soluciones.
        retorno_en_pantalla = [iteracion, valor, error, angulo]
        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")


if __name__ == '__main__':
    # Esto es para que simepre se generen los mismos numeros aleatorios
    np.random.seed(1000)

    # Esto es aprueba de errores de singularidad
    while True:
        try:
            # Setea las dimensiones deseadas
            A, b = generar_datos(30, 100)
            # Se prueba la singularidad (NO HACER CASO A ESTA LINEA)
            prueba = np.linalg.inv(A)

        except:
            print("¡Error de singularidad!")

        finally:
            # Se corre el programa
            LASSO(A, b, 10, 20000)
            break
