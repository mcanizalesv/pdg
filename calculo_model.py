import numpy as np

# Parámetros de Antoine rango de temperatura de 0 a 200 °C y presión de kPa
At = 16.3872
Bt = 3885.70
Ct = -230.170
# Capacidad calorífica del vapor
Av = 3.47
Bv = 1.45E-3
Dv = 0.121E5

def askForInputs():
    # La matriz "L" recibe los flujos másicos, propiedades y composición másica de las corrientes concentradas, alimentación y producto final.
    # La matriz "V" recibe los flujos másicos, propiedades de las corrientes de vapor, vapor vivo y vapor final.
    n = int(input('¿Cuantos efectos usará?: '))
    Tst = float(
        input('Ingresa la temperatura del vapor de calentamiento en °C: '))  # °C
    V = np.zeros((n+1, 5))
    L = np.zeros((n+1, 5))
    Q = []
    P = 100  # % de pureza de la solución agua - azúcar
    Tol = float(input('Ingrese el porcentaje de tolerancia de error: '))
    eleccion = input('¿Conoces la presión absoluta o manométrica del sistema? (m/a): ')

    if eleccion == 'm':
        Pman = round(float(input('Ingresa la presión manométrica en kPa. Nota: Si la presión es de vacío, ingresa con el signo menos: ')), 2)

        def Pabs(Patm, Pman):
            return Patm + Pman
        Pabsres_ = Pabs(101.325, Pman)

    elif eleccion == 'a':
        Pabsres_ = round(float(input('Ingresa la presión absoluta en kPa')), 2)

    else:
        pass

    L[0, 0] = float(input('Corriente de alimentación (kg/h): '))
    L[0, 1] = float(input('Grados brix alimentación (m/m): '))
    L[n, 1] = float(input('Grados brix salida (m/m): '))
    L[0, 2] = float(input('Temperatura de alimentación (ºC): '))

    return [L,
            n,
            Tst,
            V,
            L,
            Q,
            P,
            Tol,
            Pman,
            Pabsres_,
            ]

def Tdif(a, b):
    return a - b

def calculateTemperature(L, Tst, DT, n):
    i = 0
    T1 = Tst - DT[0]
    for i in range(1, n+1):
        if i == 1:
            L[i, 2] = T1
        elif i > 1:
            L[i, 2] = L[i-1, 2] - DT[i-1]
    i += 1

def calculateCondensedTemperature(V, n, Tst, L):
    i = 0
    for i in range(0, n+1):
        if i == 0:
            V[i, 1] = Tst
        elif i > 0:
            V[i, 1] = L[i, 2]
    i += 1


def calculateFirstProximity(V, Vt, n):
    k = 0
    for k in range(0, n+1):
        V[k, 0] = Vt
    k += 1
    return k


def calculateBpe(L, Vt, n):
    Bpe = []
    for i in range(1, n+1):
        L[i, 0] = L[i-1, 0] - Vt
        L[i, 1] = (L[i-1, 0]*L[i-1, 1])/L[i, 0]
        cal2 = round(2*(L[i, 1]*100)/(100 - (L[i, 1]*100)), 2)
        Bpe.append(cal2)
    return Bpe


def calculateU(n):
    U = []
    k=0
    for k in range(1, n+1):
        stp = (2500 - 1000)/n
        cal = ((2500 - (k-1)*stp))/1000  # kW//°C m
        U.append(cal)
    k=+1
    return U


def calculateDT(n, DeltaTdisp, iU):
    DT = []
    for i in range(1, n+1):
        for i in range(1, n+1):
            iU = iU + (1/U[i-1])
        cal1 = round(DeltaTdisp*(1/U[i-1])/iU, 3)
        DT.append(cal1)
    return DT

[L,
 n,
 Tst,
 V,
 L,
 Q,
 P,
 Tol,
 Pman,
 Pabsres] = askForInputs()

# Balance de masa inicial - Primera aproximación de los flujos de vapor Vi = Vi+1 =...= Vn

L[n, 0] = (L[0, 0]*L[0, 1])/(L[n, 1])  # Flujo de salida
Vt = (L[0, 0] - L[n, 0])/n

BPE = calculateBpe(L, Vt, n)
U = calculateU(n)

Tsatn = ((Bt/(At - np.log(Pabsres))) + Ct)

DeltaTneto = Tdif(Tst, Tsatn)
DeltaTdisp = DeltaTneto + np.sum(BPE)

iU = 0
DT = calculateDT(n,DeltaTdisp, iU)

calculateTemperature(L, Tst, DT, n)
calculateCondensedTemperature(V, n, Tst, L)
calculateFirstProximity(V, Vt, n)

k = 0
A = []
count = 1
iter = 0

while (iter <= 100 or count >= Tol):

    DeltaTdisp = DeltaTneto + np.sum(BPE)

    # Entalpía corrientes de líquido concentrado
    i = 0
    c = []
    for i in range(0, n+1):
        c.append(round((1 - (0.6 - 0.0018*L[i, 2])*L[i, 1])*4.184, 3))
        L[i, 3] = float(np.multiply(c[i], L[i, 2]))
    i += 1

    # Entalpías de corrientes de vapor
    # Capacidad calorifica del vapor

    Av = 3.47
    Bv = 1.45E-3
    Dv = 0.121E5

    i = 0
    
    for i in range(0, n+1):
        if i == 0:
            V[i,2] = 2501.3 + 0.4618 * (Av*(Tst+273) + (Bv/2)*((Tst+273)**2-273**2) - Dv*((Tst+273)**-1 - 273**-1 )); #kJ/kg
        elif i > 0:
            V[i,2] = 2501.3 + 0.4618 * (Av*(V[i,1]+273) + (Bv/2)*((V[i,1]+273)**2-273**2) - Dv*((V[i,1]+273)**-1 - 273**-1 )); #kJ/kg  
    i += 1

    # Calor latente para la generación de vapor
    i = 0
    for i in range(0, n+1):
        if i == 0:
            V[i, 3] = (607-0.6*Tst)*4.184  # kJ/kg
        elif i > 0:
            V[i, 3] = (607-0.6*V[i, 1])*4.184
    i += 1

    # Reasignación de flujos de vapor y corrientes concentradas
    x = np.zeros((2*n+1, 1))
    i = 0
    for i in range(0, 2*n+1):
        if i >= 0 and i <= n:
            x[i] = V[i, 0]
        elif i > n and i <= (2*n + 1):
            x[i] = L[i-n, 0]
    i += 1

    # Balances de materia y energía
    i = 0
    G = np.zeros((n+1, n+1))
    for i in range(0, n+1):
        if i == 1:
            G[1,0] = V[0,2]*L[1, 3] - x[1]*V[1,2] + (L[0,0]*L[0,4]) - x[0]*V[1,3]
            G[1,1] = L[1,3] - V[1,2] 
            
        elif (i == 0):
            y=0
            for y in range (1,n+1):
                G[0,y] = 1
            y=+1
            
        else:
            G[i,i] = -V[i,3]
            G[i,i-1] = V[i-1,3] - L[i,4]
    
    ind = np.zeros((n+1,1))
    
    u=0
    for u in range(0,n+1):
        if u == 1:
            ind[u] = L[0,0]*(L[1,3]-L[0,3])
        elif u==0:
            ind[u] = L[0,0] - L[n,0]
        else: 
            ind[u] = L[u,3]*L[u,0] - L[u-1,3]*L[u-3,0]
    u=+1
    
    result_vap= np.linalg.solve(G,ind)
                             
    i = i + 1
    k = 0
    for k in range(1, n):
        V[k-1, 0] = G[k-1]
    k =+1
    for y in range(n+1, 2*n):
        L[y-1, 0] = G[y-1]
    y=+1
    
    for k in range(2, n+1):
        L[k+1, 0] = L[k-2, 1] - V[k-2, 0]
        L[k+1, 1] = (L[k-2, 1]*L[k-2, 1])/L[k+1, 0]
   

    A = []
    # Cálculo del calor y el área de transferencia de calor en cada efecto
    i = 0
    dif = []
    
    for i in range(0, n):
        # Estar atenta, porque no se ha llenado la columna cero de V
        cal3 = V[i, 3]*V[i, 0]*(1/3600)
        Q.append((cal3))
        cal4 = 1000*Q[i-1]/((DT[i-1] - L[i, 4])*U[i-1])
        A.append((cal4))
        cal5 = ((A[i] - A[i-1]))
        dif.append((cal5))
    i += 0
    count = np.sum(dif)
    #Nuevo cálculo de Ti 
    deltaTinuevo=[]
    
    if count >= Tol:
        for u in range(1,n):
            Asum= np.sum(Q[i]/U[i])
            deltaTinuevo.append(Q[i/calculateU[i]*Asum])
    
    #calculateTemperature(L, Tst, deltaTinuevo, n)
iter = iter + 1