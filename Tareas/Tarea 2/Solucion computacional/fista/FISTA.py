__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Se importan los modulos de python
import numpy as np
import scipy.linalg
import time
import matplotlib
import matplotlib.pyplot as plt

from pprint import pprint


# Se importan los modulos creados por el usuario
from leerExcel import importar_excel


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

def LASSO_FISTA(A, b, tau, iteracion_maxima):
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
        - xk : Vector solucion del problema de k iteraciones."""

    """ IMPLEMENTADO """
    errores = list()
    """ IMPLEMENTADO """

    m, n = A.shape

    # Se setean las condiciones iniciales, junto a los vectores que almacenand
    # informacion de la iteracion k, k-1, k-2, respectivamente.
    xk = np.zeros((n, 1))
    print(xk)
    quit()


    # Se setea el segundo punto de sucesion (que le otorga el caracter de acelerado)
    zk = xk


    # La sucesion thetak se setea simplemente como 1 y se modifica en cada iteración (ver el código))
    thetak = 1


    # Estimacion del valor de R (radio) y L (connstante de Lipschitz)
    # segun teoria vista en clases
    R = np.sqrt(np.linalg.norm(np.linalg.inv(np.dot(A, np.transpose(A)))))*np.linalg.norm(np.dot(np.transpose(A), b))
    L = tau*np.sqrt(n) + np.linalg.norm(np.dot(A, np.transpose(A)))*R + np.linalg.norm(np.dot(np.transpose(A), b))

    # Se calcula el valor optimo actual en la iteracion 0
    valor_optimo = tau*np.linalg.norm(xk, 1) + 0.5*np.linalg.norm(np.dot(A, xk) - b)**2

    # Se calcula la norma inifinito de b
    norma_b = np.linalg.norm(b)

    # Se despliega el mensaje en pantalla
    print("\n\n**********    METODO FISTA    *********\n")
    print("ITERACION     VALOR OBJ      ERROR AJUSTE  ||x||_1")

    # Se comienza el ciclo de iteraciones
    for iteracion in range(iteracion_maxima):
        # 1º Vector que se evalua en el gradiente para el paso xk+1
        yk = (1-thetak)*xk + thetak*zk

        # 2º Se actualizan los valores de almacenamiento


        # 3º Se crea el paso zk+1
        zk = zk - (2*np.dot(np.transpose(A), np.dot(A, yk) - b) + tau*np.sign(yk))/(thetak*L)

        # 4º Se crea el paso xk+1
        xk = (1 - thetak)*xk + thetak*zk

        # 5º Se actualiza la sucesion thetak se crean dos sucesiones para thethak
        # puedes testear cada una comentando la otra linea

        #thetak = 2/(1+np.sqrt(1+4/(thetak**2)))
        thetak = 2/(2+iteracion)

        # 6º Se actualiza el valor objetivo
        valor_optimo = tau*np.linalg.norm(xk, 1) + 0.5*np.linalg.norm(np.dot(A, xk) - b)**2

        # 7º Se calcula el error (segun norma infito de b) para mostrar en pantalla.
        error = np.linalg.norm(np.dot(A, xk) - b)/norma_b

        # 8º Se guarda el error para ser graficado despues
        """ IMPLEMENTADO """
        errores.append(error)
        """ IMPLEMENTADO """

        n1 = np.linalg.norm(xk, 1)        

         # La rutina de FISTA muestra en pantalla para cada iteracion:
        # nº de iteracion, valor de la funcion evaluada en el x de la iteracion,
        #  error y angulo formado por las soluciones.
        retorno_en_pantalla = [iteracion, valor_optimo, error, n1]
#        print(f"{retorno_en_pantalla[0]: ^12d}{retorno_en_pantalla[1]: ^12f} {retorno_en_pantalla[2]: ^12f} {retorno_en_pantalla[3]: ^12f}")
        print("%12.6f %12.6f %12.6f %12.6f" % (retorno_en_pantalla[0],retorno_en_pantalla[1],retorno_en_pantalla[2],retorno_en_pantalla[3]))

    return xk, errores

if __name__ == '__main__':
    """ IMPLEMENTADO """
    # Esto es para que simepre se generen los mismos numeros aleatorios
    np.random.seed(1000)

    # Seteo de datos estaticos para el metodo
    X, Y = importar_excel()
    iteracion_maxima = 5000 # Aqui se debe ir cambiando el valor para el analisis
    tau = 0.000000001       # Aqui se debe ir cambiando el valor para el analisis
    
    xsol, errores = LASSO_FISTA(np.array(X), np.array(Y), tau, iteracion_maxima)
    
    """ IMPLEMENTADO """
    import matplotlib
    import matplotlib.pyplot as plt


    fig, ax = plt.subplots()
    ax.plot(range(iteracion_maxima), errores)

    ax.set(xlabel='Iteracion', ylabel='Error',
        title='Análisis de convergencia del error')
    ax.grid()

    fig.savefig("[FISTA] Convergencia del error.png")
    plt.show()
    """ IMPLEMENTADO """
