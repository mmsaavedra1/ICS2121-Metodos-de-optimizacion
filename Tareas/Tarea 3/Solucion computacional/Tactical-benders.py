#!/usr/bin/python

# Modelo del problema táctico de planificación de aserraderos

from gurobipy import *
import time

# Basic sets of elements

LOG = ["LOG1","LOG2","LOG3",	"LOG4","LOG5","LOG6"]
BOARD = ["LU1","LU2","LU3","LU4","LU5","LU6","LU7"]
CUT = ["E1", "E2", "E3", "E4"]
MONTH = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

# Procurement and procesing cost for logs

CTt = {
("LOG1","Jan") :	260,
("LOG1","Feb") :	260,
("LOG1","March") :	260,
("LOG1","April") :	260,
("LOG1","May") :	260,
("LOG1","June") :	260,
("LOG1","July") :	260,
("LOG1","Aug") :	260,
("LOG1","Sept") :	260,
("LOG1","Oct") :	260,
("LOG1","Nov") :	260,
("LOG1","Dec") :	260,
("LOG2","Jan") :	265,
("LOG2","Feb") :	265,
("LOG2","March") :	265,
("LOG2","April") :	265,
("LOG2","May") :	265,
("LOG2","June") :	265,
("LOG2","July") :	265,
("LOG2","Aug") :	265,
("LOG2","Sept") :	265,
("LOG2","Oct") :	265,
("LOG2","Nov") :	265,
("LOG2","Dec") :	265,
("LOG3","Jan") :	233,
("LOG3","Feb") :	233,
("LOG3","March") :	233,
("LOG3","April") :	233,
("LOG3","May") :	233,
("LOG3","June") :	233,
("LOG3","July") :	233,
("LOG3","Aug") :	233,
("LOG3","Sept") :	233,
("LOG3","Oct") :	233,
("LOG3","Nov") :	233,
("LOG3","Dec") :	233,
("LOG4","Jan") :	241,
("LOG4","Feb") :	241,
("LOG4","March") :	241,
("LOG4","April") :	241,
("LOG4","May") :	241,
("LOG4","June") :	241,
("LOG4","July") :	241,
("LOG4","Aug") :	241,
("LOG4","Sept") :	241,
("LOG4","Oct") :	241,
("LOG4","Nov") :	241,
("LOG4","Dec") :	241,
("LOG5","Jan") :	102,
("LOG5","Feb") :	102,
("LOG5","March") :	102,
("LOG5","April") :	102,
("LOG5","May") :	102,
("LOG5","June") :	102,
("LOG5","July") :	102,
("LOG5","Aug") :	102,
("LOG5","Sept") :	102,
("LOG5","Oct") :	102,
("LOG5","Nov") :	102,
("LOG5","Dec") :	102,
("LOG6","Jan") :	140,
("LOG6","Feb") :	140,
("LOG6","March") :	140,
("LOG6","April") :	140,
("LOG6","May") :	140,
("LOG6","June") :	140,
("LOG6","July") :	140,
("LOG6","Aug") :	140,
("LOG6","Sept") :	140,
("LOG6","Oct") :	140,
("LOG6","Nov") :	140,
("LOG6","Dec") :	140,
}


CFt = {
("LOG1","Jan") :	2600000	,
("LOG1","Feb") :	3120000	,
("LOG1","March") :	2080000	,
("LOG1","April") :	2600000	,
("LOG1","May") :	2600000	,
("LOG1","June") :	2600000	,
("LOG1","July") :	2600000	,
("LOG1","Aug") :	3120000	,
("LOG1","Sept") :	2600000	,
("LOG1","Oct") :	2600000	,
("LOG1","Nov") :	2080000	,
("LOG1","Dec") :	3120000	,
("LOG2","Jan") :	2650000	,
("LOG2","Feb") :	3180000	,
("LOG2","March") :	2650000	,
("LOG2","April") :	2650000	,
("LOG2","May") :	3180000	,
("LOG2","June") :	2650000	,
("LOG2","July") :	3180000	,
("LOG2","Aug") :	3180000	,
("LOG2","Sept") :	3180000	,
("LOG2","Oct") :	2120000	,
("LOG2","Nov") :	2120000	,
("LOG2","Dec") :	2120000	,
("LOG3","Jan") :	2330000	,
("LOG3","Feb") :	2330000	,
("LOG3","March") :	1864000	,
("LOG3","April") :	2796000	,
("LOG3","May") :	2796000	,
("LOG3","June") :	2330000	,
("LOG3","July") :	2330000	,
("LOG3","Aug") :	2330000	,
("LOG3","Sept") :	2796000	,
("LOG3","Oct") :	2330000	,
("LOG3","Nov") :	1864000	,
("LOG3","Dec") :	2330000	,
("LOG4","Jan") :	2892000	,
("LOG4","Feb") :	2892000	,
("LOG4","March") :	1928000	,
("LOG4","April") :	2410000	,
("LOG4","May") :	2410000	,
("LOG4","June") :	2410000	,
("LOG4","July") :	2892000	,
("LOG4","Aug") :	2892000	,
("LOG4","Sept") :	2892000	,
("LOG4","Oct") :	2410000	,
("LOG4","Nov") :	2892000	,
("LOG4","Dec") :	1928000	,
("LOG5","Jan") :	816000	,
("LOG5","Feb") :	1224000	,
("LOG5","March") :	1224000	,
("LOG5","April") :	816000	,
("LOG5","May") :	816000	,
("LOG5","June") :	1224000	,
("LOG5","July") :	1224000	,
("LOG5","Aug") :	816000	,
("LOG5","Sept") :	1224000	,
("LOG5","Oct") :	1224000	,
("LOG5","Nov") :	1224000	,
("LOG5","Dec") :	1020000	,
("LOG6","Jan") :	1680000	,
("LOG6","Feb") :	1120000	,
("LOG6","March") :	1400000	,
("LOG6","April") :	1120000	,
("LOG6","May") :	1120000	,
("LOG6","June") :	1400000	,
("LOG6","July") :	1680000	,
("LOG6","Aug") :	1120000	,
("LOG6","Sept") :	1680000	,
("LOG6","Oct") :	1120000	,
("LOG6","Nov") :	1120000	,
("LOG6","Dec") :	1680000	,
}

# Inventory costo for logs

CBt = {
("LU1","Jan") :	2,
("LU1","Feb") :	2,
("LU1","March") :	2,
("LU1","April") :	2,
("LU1","May") :	2,
("LU1","June") :	2,
("LU1","July") :	2,
("LU1","Aug") :	2,
("LU1","Sept") :	2,
("LU1","Oct") :	2,
("LU1","Nov") :	2,
("LU1","Dec") :	2,
("LU2","Jan") :	2,
("LU2","Feb") :	2,
("LU2","March") :	2,
("LU2","April") :	2,
("LU2","May") :	2,
("LU2","June") :	2,
("LU2","July") :	2,
("LU2","Aug") :	2,
("LU2","Sept") :	2,
("LU2","Oct") :	2,
("LU2","Nov") :	2,
("LU2","Dec") :	2,
("LU3","Jan") :	2,
("LU3","Feb") :	2,
("LU3","March") :	2,
("LU3","April") :	2,
("LU3","May") :	2,
("LU3","June") :	2,
("LU3","July") :	2,
("LU3","Aug") :	2,
("LU3","Sept") :	2,
("LU3","Oct") :	2,
("LU3","Nov") :	2,
("LU3","Dec") :	2,
("LU4","Jan") :	2,
("LU4","Feb") :	2,
("LU4","March") :	2,
("LU4","April") :	2,
("LU4","May") :	2,
("LU4","June") :	2,
("LU4","July") :	2,
("LU4","Aug") :	2,
("LU4","Sept") :	2,
("LU4","Oct") :	2,
("LU4","Nov") :	2,
("LU4","Dec") :	2,
("LU5","Jan") :	2,
("LU5","Feb") :	2,
("LU5","March") :	2,
("LU5","April") :	2,
("LU5","May") :	2,
("LU5","June") :	2,
("LU5","July") :	2,
("LU5","Aug") :	2,
("LU5","Sept") :	2,
("LU5","Oct") :	2,
("LU5","Nov") :	2,
("LU5","Dec") :	2,
("LU6","Jan") :	2,
("LU6","Feb") :	2,
("LU6","March") :	2,
("LU6","April") :	2,
("LU6","May") :	2,
("LU6","June") :	2,
("LU6","July") :	2,
("LU6","Aug") :	2,
("LU6","Sept") :	2,
("LU6","Oct") :	2,
("LU6","Nov") :	2,
("LU6","Dec") :	2,
("LU7","Jan") :	2,
("LU7","Feb") : 2,
("LU7","March") :	2,
("LU7","April") :	2,
("LU7","May") :	2,
("LU7","June") :	2,
("LU7","July") :	2,
("LU7","Aug") :	2,
("LU7","Sept") :	2,
("LU7","Oct") :	2,
("LU7","Nov") :	2,
("LU7","Dec") :	2,
}

# Processing and inventory capacities

PAt = {
"Jan" : 28500,		
"Feb" : 28500,
"March" : 28500,
"April" : 28500,
"May" : 28500,
"June" : 28500,
"July" : 28500,
"Aug" : 28500,
"Sept" : 28500,
"Oct" : 28500,
"Nov" : 28500,
"Dec" : 28500,
}	


PBt = {
"Jan" : 40000,		
"Feb" : 8000,
"March" : 50000,
"April" : 50000,
"May" : 50000,
"June" : 50000,
"July" : 50000,
"Aug" : 50000,
"Sept" : 35000,
"Oct" : 50000,
"Nov" : 50000,
"Dec" : 50000,
}	

# Demand for final products									

D = {
"LU1" : {"Jan":2450,"Feb":2558,"March":2708,"April":2208,"May":2433,"June":2354,"July":2359,"Aug":2699,"Sept":2107,"Oct":2309,"Nov":2624,"Dec":2725},
"LU2" : {"Jan":152,"Feb":176,"March":139,"April":142,"May":167,"June":147,"July":139,"Aug":152,"Sept":156,"Oct":137,"Nov":137,"Dec":126},	
"LU3" : {"Jan":420,"Feb":346,"March":	371,"April":	360,"May":497,"June":458,"July":	490,"Aug":502,"Sept":441,"Oct":495,"Nov":392,"Dec":396},	
"LU4" : {"Jan":2100,"Feb":2515,"March":1745,"April":1906,"May":2320,"June":2335,"July":2028,"Aug":2218,"Sept":1931,"Oct":	2465,"Nov":2131,"Dec":2383},	
"LU5" : {"Jan":1818,"Feb":2108,"March":2015,"April":1471,"May":1956,"June":2063,"July":1473,"Aug":2165,"Sept":2130,"Oct":2166,"Nov":1489,"Dec":1588},	
"LU6" : {"Jan":1120,"Feb":975,"March":1130,"April":1163,"May":1003,"June":1233,"July":1161,"Aug":1253,"Sept":951,"Oct":1074,"Nov":1244,"Dec":1144},	
#"LU6" : {"Jan":0,"Feb":0,"March":0,"April":0,"May":0,"June":1233,"July":1161,"Aug":0,"Sept":0,"Oct":0,"Nov":0,"Dec":0},
"LU7" : {"Jan":342,"Feb":295,"March":310,"April":400,"May":335,"June":334,"July":282,"Aug":277,"Sept":325,"Oct":280,"Nov":308,"Dec":344}
}

# Aggregated yield of the sawing process 

Rt	= {
"LOG1" : {"LU1":0.0611,"LU2":0.01742,"LU3":0.0611,"LU4":0.13936,"LU5":0.05954,"LU6":0.12194,"LU7":0.05954},		
"LOG2" : {"LU1":0.08996,"LU2":0.0078,"LU3":0.08996,"LU4":	0.10582,"LU5":0.06422,"LU6":0.09802,"LU7":0.06422},		
"LOG3" : {"LU1":0.065,"LU2":0.065,"LU3":0.0624,"LU4":0.169,"LU5":0.026,"LU6":0.13,"LU7":	0.0026},		
"LOG4" : {"LU1":0.091,"LU2":0.0234,"LU3":0.143,"LU4":0.0676,"LU5":0.0494,"LU6":0.104,"LU7":0.0416},		
"LOG5" : {"LU1":0.155,"LU2":0.055,"LU3":0.045,"LU4":0.105,"LU5":0.0715,"LU6":0.025,"LU7":0.05616},		
"LOG6" : {"LU1":0.12246,"LU2":0.00286,"LU3":	0.04004,"LU4":0.13546,"LU5":0.09542,"LU6":0.00208,"LU7":0.12168}
}

# Initial log inventory

w0t = {											
"LU1": 0,													
"LU2": 0,													
"LU3": 0,													
"LU4": 0,													
"LU5": 0,													
"LU6": 0,													
"LU7": 0,
}
	
BIGM = 50000

NITERACIONES = 30000
TOL = 0.000001

# Model
m = Model("Sawmil_Tactical")

# variables
wt = m.addVars(BOARD,MONTH,name="Board_inventory")
rt = m.addVars(BOARD,MONTH,name="Board_production")
st = m.addVars(LOG,MONTH,name="Logs_processed")
zt = m.addVars(LOG,MONTH,vtype=GRB.INTEGER,name="Setup")

# Objective function

m.setObjective(sum((sum((CTt[k,t]+4.5)*st[k,t] for k in LOG)+sum((CFt[k,t])*zt[k,t] for k in LOG)+(sum(CBt[m,t]*wt[m,t] for m in BOARD))) for t in MONTH), GRB.MINIMIZE)
 
# Constraints

m.addConstrs(((sum(st[k,t] for k in LOG) <= PAt[t]) for t in MONTH), name = "Processing_capacity")

m.addConstrs(((st[k,t] <= BIGM*zt[k,t]) for t in MONTH for k in LOG), name = "Cargas_fijas")

m.addConstrs(((sum(wt[m,t] for m in BOARD) <= PBt[t]) for t in MONTH), name = "Storage_capacity")

m.addConstrs(((sum(Rt[k][m]*st[k,t] for k in LOG) == rt[m,t]) for m in BOARD for t in MONTH), name = "Transformation")

m.addConstrs((w0t[m]+ rt[m,MONTH[0]]-wt[m,MONTH[0]]==D[m][MONTH[0]] for m in BOARD), name = "Initial_balance")

m.addConstrs(((wt[m,MONTH[MONTH.index(t)-1]]+ rt[m,t]-wt[m,t]==D[m][t]) for m in BOARD for t in MONTH if t != MONTH[0]), name = "Board_balance")

     

# Solve
m.optimize()
m.update()


valorobjetivo = m.objval

print('\n Valor óptimo: %8.4f \n' % valorobjetivo)

#m.write("Tactical.sol")

#Seteamos el satélite, el dual del problema interior a usar en la RL

satelite = Model("SawmilLR_Satelite")
satelite.Params.InfUnbdInfo = 1
satelite.Params.OutputFlag = 0

pi = satelite.addVars(MONTH,lb=0,name="Pidual")
ud = satelite.addVars(BOARD,MONTH,lb=-GRB.INFINITY,ub=GRB.INFINITY,name="Udual")

# Aquí definimos una lista auxiliar para el lado derecho corregido por las variables s

                                                               

satelite.setObjective((sum(-PBt[t]*pi[t] for t in MONTH)+sum((D[m][t] - rt[m,t].X)*ud[m,t] for m in BOARD for t in MONTH)),GRB.MAXIMIZE)

satelite.addConstrs(((-pi[MONTH[11]] - ud[m,MONTH[11]] <= CBt[m,MONTH[11]]) for m in BOARD), name = "dual1")
satelite.addConstrs(((-pi[t] + ud[m,MONTH[MONTH.index(t)+1]] - ud[m,t] <= CBt[m,t]) for m in BOARD for t in MONTH if t != MONTH[11]), name = "dual2")

satelite.optimize()

etak = satelite.objval

valornuevo = etak + sum((sum((CTt[k,t]+4.5)*st[k,t].X for k in LOG)+sum((CFt[k,t])*zt[k,t].X for k in LOG)) for t in MONTH)

print('\n Valor con dual: %8.4f \n' % valornuevo)


# Ahora seteamos el problema maestro

master = Model("Problema_maestro")
master.Params.OutputFlag = 0

# variables
rtm = master.addVars(BOARD,MONTH,name="Board_production")
stm = master.addVars(LOG,MONTH,name="Logs_processed")
ztm = master.addVars(LOG,MONTH,vtype=GRB.INTEGER,name="Setup")
gamma = master.addVar(vtype=GRB.CONTINUOUS,name="Cota")

# Objective function

master.setObjective(gamma + sum((sum((CTt[k,t]+4.5)*stm[k,t] for k in LOG)+sum((CFt[k,t])*ztm[k,t] for k in LOG)) for t in MONTH), GRB.MINIMIZE)
 
# Constraints

master.addConstrs(((sum(stm[k,t] for k in LOG) <= PAt[t]) for t in MONTH), name = "Processing_capacity")
master.addConstrs(((stm[k,t] <= BIGM*ztm[k,t]) for t in MONTH for k in LOG), name = "Cargas_fijas")
master.addConstrs(((sum(Rt[k][m]*stm[k,t] for k in LOG) == rtm[m,t]) for m in BOARD for t in MONTH), name = "Transformation")


print("")
print("---------- CICLOS BENDERS-------------")
print("")
print("Ciclo - Master - Subproblema")
inicio = time.time()
contador = 0
lista = []

# Se inician las iteracion controladas
FOold = 0
while contador <= NITERACIONES:
    contador += 1
#    input("Press Enter to continue...")

    # Resuelve el modelo maestro
    master.update()
    master.optimize()

    # Optimizacion del subproblema satélite.

    satelite.setObjective((sum(-PBt[t]*pi[t] for t in MONTH)+sum((D[m][t] - rtm[m,t].X)*ud[m,t] for m in BOARD for t in MONTH)),GRB.MAXIMIZE)

    satelite.update()
    satelite.optimize()

        # Acumula el valor en la FO
    FO = master.objVal
    #print(contador, "/", master.objVal, "/", satelite.objVal)
    lista.append(FO)
    cota = satelite.objVal + sum((sum((CTt[k,t]+4.5)*stm[k,t].X for k in LOG)+sum((CFt[k,t])*ztm[k,t].X for k in LOG)) for t in MONTH)

    # Ahora se usa la solución del satélite para generar un corte y agregarlo al master
    
    if satelite.status == 2:
    # Si es acotado se agrega corte de optimalidad
        print(contador, "/", FO, "/", cota, "/", satelite.status)    
        master.addConstr((sum(-PBt[t]*pi[t].X for t in MONTH)+sum((D[m][t] - rtm[m,t])*ud[m,t].X for m in BOARD for t in MONTH)) <= gamma)
    else:
        # El dual es no acotado, se agrega un corte de factibilidad que se obtiene del rayo
        rayopi = {}
        rayoud = {}
        for t in MONTH:
            rayopi[t] = pi[t].UnbdRay
        for m in BOARD:
            for t in MONTH:
                rayoud[m,t] = ud[m,t].UnbdRay
                
        print(contador, "/", FO, "/", cota, "/", satelite.status) 
        master.addConstr((sum(-PBt[t]*rayopi[t] for t in MONTH)+sum((D[m][t] - rtm[m,t])*rayoud[m,t] for m in BOARD for t in MONTH)) <= 0)
        
    if (cota - FO)/(FO+0.1) <= TOL:
        break

final = time.time()
print("")
print(" Tiempo de ejecucion:", (final - inicio))


