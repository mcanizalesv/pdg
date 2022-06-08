import numpy as np
import math


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
    n = 3 #int(input('¿Cuantos efectos usará?: '))
    Tst = 121 #float(input('Ingresa la temperatura del vapor de calentamiento en °C: '))  # °C
    V = np.zeros((n+1, 5))
    L = np.zeros((n+1, 5))
    Q = []
    P = 100  # % de pureza de la solución agua - azúcar
    eleccion = input('¿Conoces la presión absoluta o manométrica del sistema? (m/a): ')

    if eleccion == 'm':
        Pman = round(float(input('Ingresa la presión manométrica en kPa. Nota: Si la presión es de vacío, ingresa con el signo menos: ')), 2)

        def Pabs(Patm, Pman):
            return Patm + Pman
        Pabsres_ = Pabs(101.325, Pman)

    elif eleccion == 'a':
        Pabsres_ = round(float(input('Ingresa la presión absoluta en kPa: ')), 2)

    else:
        pass

    L[0, 0] = 22680 #float(input('Corriente de alimentación (kg/h): ')) 
    L[0, 1] = 0.05 #float(input('Grados brix alimentación (m/m): '))
    L[n, 1] = 0.25 #float(input('Grados brix salida (m/m): '))
    L[0, 2] = 26.85 #float(input('Temperatura de alimentación (ºC): '))

    return [L,
            n,
            Tst,
            V,
            L,
            Q,
            P,
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
            L[i, 2] = L[i-1, 2] - DT[i-1] - BPE[i-1]
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
        cal2 = 1.78*L[i,1] + 6.22*(L[i, 1]**2)
        Bpe.append(cal2)
    return Bpe


def calculateU(n):
    U = []
    k=0
    for k in range(1, n+1):
        stp = (2500 - 1000)/n
        cal = ((2500 - (k-1)*stp))/1000  # kW//°C m^2
        U.append(cal)
    k=+1
    return U

# Verificar que la suma dé lo mismo que el disponible 
# Pasar el vector de las U como parámetro

def calculateDT(n, DeltaTdisp):
    DT = []
    iU = []
    sum = 0

    for i in range(0, n):
        cal2=1/U[i]
        iU.append(cal2)
    for k in range(0,len(iU)):
        sum = sum + iU[k]
    for j in range(0, n):   
        cal1 = round((DeltaTdisp*(1/U[j]))/sum, 3)
        DT.append(cal1)
    return DT

[L,
 n,
 Tst,
 V,
 L,
 Q,
 P,
 Pabsres] = askForInputs()

# Balance de masa inicial - Primera aproximación de los flujos de vapor Vi = Vi+1 =...= Vn

L[n, 0] = (L[0, 0]*L[0, 1])/(L[n, 1])  # Flujo de salida
Vt = round((L[0, 0] - L[n, 0])/n,2)

BPE = calculateBpe(L, Vt, n)
U = [3.123,1.987,1.136]

Tsatn = round(((Bt/(At - np.log(Pabsres))) + Ct),2)

DeltaTneto = round(Tdif(Tst, Tsatn),2)
DeltaTdisp = round(DeltaTneto - np.sum(BPE),2)

DT = [15.9,18.94,33.1]

calculateTemperature(L, Tst, DT, n)
calculateCondensedTemperature(V, n, Tst, L)
calculateFirstProximity(V, Vt, n)

k = 0
A = []
iter = 0

while iter <= 100 or cont > 0.35:
    
    #Capacidad calorífica de los líquidos concentrados

    d1= -2.844669*10**-2
    d2= 4.211925
    d3= -1.017034*10**-3
    d4= 1.311054*10**-5
    d5= -6.756469*10**-8
    d6= 1.724481*10**-10
    
    # Entalpía de corrientes de líquido concentrado

    cont = []
    hLi = []
    for i in range(0, n+1):
        h= round(d1 + d2*L[i,2] + d3*L[i,2]**2 + d4*L[i,2]**3 + d5*L[i,2]**4 + d6*L[i,2]**5,2)
        hLi.append(h)
    
    for i in range(0, n+1):
        cont.append(round(hLi[i] + (((1 - ((0.6 - 0.0018*L[i, 2])*L[i,1]))*4.184)/1000), 3))
        L[i, 3] = cont[i]
        
    #Entalpía de los condensados
    
    hci=[]
    i=0
    for i in range(0, n+1):
        cal2= round(d1 + d2*V[i,1] + d3*V[i,1]**2 + d4*V[i,1]**3 + d5*V[i,1]**4 + d6*V[i,1]**5,2)
        hci.append(cal2)
        L[i,4]= hci[i]
        i += 1
    

    # Entalpía específica de las corrientes de vapor saturado
    
    a=64.87678
    b=11.76476
    c=-11.94431
    d=6.29015
    e=-0.99893
    Tcr=647.096 #K
    i = 0
    
    for i in range(0, n+1):
        if i == 0:
            V[i,2] = np.exp(math.sqrt(a+b*np.log(1/((Tst+273.15)/Tcr))**0.35 + c/((Tst+273.15)/Tcr)**2 + d/((Tst+273.15)/Tcr)**3 + e/((Tst+273.15)/Tcr)**4)) #kJ/kg
            
        elif i > 0:
            V[i,2] = np.exp(math.sqrt(a+b*np.log(1/((V[i,1]+273.15)/Tcr))**0.35 + c/((V[i,1]+273.15)/Tcr)**2 + d/((V[i,1]+273.15)/Tcr)**3 + e/((V[i,1]+273.15)/Tcr)**4)) #kJ/kg
    i += 1

    # Entalpía de vaporización para la generación de vapor
    
    for i in range(1, n+1):
        V[i, 3] = V[i-1,2]-L[i,4]
        
    # Balances de materia y energía
    i = 0
    G = np.zeros((n+1, n+1))
    for i in range(0, n+1):
        if i == 1:
            G[i,i-1] = (V[0,2]-L[1, 4]) 
            G[i,i] = - V[1,2]
            
        elif (i == 0):
            for y in range (1,n+1):
                G[0,y] = 1
            
        else:
            G[i,i] = -V[i,2]
            G[i,i-1] = V[i-1,2] - L[i,4]
        i=+1
    
    ind = np.zeros((n+1,1))
    
    u=0
    for u in range(0,n+1):
        if u == 0:
            ind[u] = L[0,0] - L[n,0]
        else: 
            ind[u] = L[u,3]*L[u,0] - L[u-1,3]*L[u-1,0]
        u=u+1
    
    result_vap= np.linalg.solve(G,ind)
                             
    i = i + 1
    
    #Reasignación de flujos másicos de vapor 
    
    
    for k in range(0, n+1):
        V[k, 0] = result_vap[k]
    
    
    #Cálculo porcentaje de error entre los flujos de vapor
    
    porcentaje_error=[]
    for p in range(1, n+1):
        porcentaje_error.append(abs(round((Vt-V[p,0])/Vt,2)))
    
    
    #Cálculo del calor transferido en cada efecto
    
    Q=[]
    for j in range(0,n):
        cal6=round(V[j+1,3]*V[j,0]*(1/3600),2) 
        Q.append(round(cal6,2)) # kW

    #Cálculo de áreas de tansferencia y porcentaje de error
    
    for y in range(0,n):
        cal7=(Q[y])/(U[y]*(DT[y]))
        A.append(round(cal7,2)) # m^2
    
    error_areas_array = np.zeros((n,1))
    j=0
    for j in range (0,n):
        if j >= 0 and j < n-1:
            error_areas_array[j]= abs((A[j] - A[j+1])/A[j+1])
        elif j == n-1: 
            error_areas_array[j]= abs((A[0] - A[j])/A[j])
        j+=1

    cont = np.sum(error_areas_array)
    
    if cont > (0.35):
        
        #Cálculo de área promedio
        A_prom=np.sum(A)/n

        #Cálculo de nuevos DT 
        
        DT_nuevo=[]
        
        for i in range(0,n):
            cal8= (DT[i]*A[i])/A_prom
            DT_nuevo.append(cal8)
        
        #Nuevo cálculo de las corrientes de líquido concentrado
        
        for k in range(1, n+1):
            L[k, 0] = L[k-1, 0] - V[k, 0]
            L[k, 1] = (L[k-1, 0]*L[k-1, 1])/L[k, 0]
        
        for h in range (0,n):
            DT[h]= DT_nuevo[h]
        
        calculateTemperature(L, Tst, DT, n)
        calculateCondensedTemperature(V, n, Tst, L)
        
            
    else:
        iter=101 
    
    iter = iter + 1 

    
#Cálculo de la economía del sistema 
suma_vap = 0 

for u in range (1,n+1):
    suma_vap=suma_vap + V[u,0]
    
Economy = (suma_vap/V[0,0]) #Economía del sistema      

    
print("La economía del sistema es ", Economy)    

    
# Cálculo del calor y el área de transferencia de calor en cada efecto
i = 0