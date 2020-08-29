__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos creados por usuario
from newton import *
from parametros import *


# Primero se generan datos para la funcion
# esta informacion es la que pueden cambiar a su antojo
dimension_matriz_Q = 10
iteracion_maxima_newton = 100
iteracion_maxima_gradiente = 100
epsilon = 0.1


# ******* NO TOCAR NADA DE AQUI PARA ABAJO ********
# (si deseas probar un metodo y no ambos comenta la linea 31 o 34, respectivamente)


# Para que siempre genere los mismos numeros al azar
np.random.seed(1)

# En base a su informacion entregada como input de aqui en adelante el programa
# se corre solo
Q, c = generar_datos(dimension_matriz_Q)

# Se ocupa el vector de "unos" como punto de inicio
# (notar el salto que pega) de la iteracion 1 a la 2 el valor objetivo
# -- Queda a tu eleccion que vector ingresar como solucion para la iteracion 1 --
x0 = np.random.rand(dimension_matriz_Q, 1)

# Maximo de iteraciones para newton (y asi no quede un loop infinito)

# El ultimo argumento es para ver en pantalla el proceso interno de cada BACKTRACKING
# en la iteracion K del metodo de Newton
newton(Q, c, x0, epsilon, iteracion_maxima_newton, True)

