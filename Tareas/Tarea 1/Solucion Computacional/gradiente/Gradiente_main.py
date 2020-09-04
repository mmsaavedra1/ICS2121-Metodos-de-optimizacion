__author__ = "Moises Saavedra Caceres"
__email__ = "mmsaavedra1@ing.puc.cl"


# Modulos creados por usuario
from leerExcel import importar_excel
from steepest import *


# Generacion de parametros necesarios para la funcion de GRADIENTE
iteracion_maxima = 300
epsilon = 0.0001

# Matriz rescatada de Excel
X, Y = importar_excel()
X = np.array(X)*10e-8
Y = np.array(Y)*10e-8

# Se ocupa el vector de "unos" como punto de inicio
var_alfa_inicial = np.zeros(5)
var_beta_inicial = np.zeros(5)

# Maximo de iteraciones para gradiente (y asi no quede un loop infinito)
gradiente(X, Y, var_alfa_inicial, var_beta_inicial, epsilon, iteracion_maxima)
