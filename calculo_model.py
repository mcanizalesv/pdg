import numpy as np
import math
import itertools


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
    n = 3  # int(input('¿Cuantos efectos usará?: '))
    # float(input('Ingresa la temperatura del vapor de calentamiento en °C: '))  # °C
    Tst = 121
    V = np.zeros((n+1, 5))
    L = np.zeros((n+1, 5))
    Q = []
    P = 100  # % de pureza de la solución agua - azúcar
    eleccion = input(
        '¿Conoces la presión absoluta o manométrica del sistema? (m/a): ')

    if eleccion == 'm':
        Pman = round(float(input(
            'Ingresa la presión manométrica en kPa. Nota: Si la presión es de vacío, ingresa con el signo menos: ')), 2)

        def Pabs(Patm, Pman):
            return Patm + Pman
        Pabsres_ = Pabs(101.325, Pman)

    elif eleccion == 'a':
        Pabsres_ = round(
            float(input('Ingresa la presión absoluta en kPa: ')), 2)

    else:
        pass

    L[0, 0] = 100  # float(input('Corriente de alimentación (kg/h): '))
    L[0, 1] = 0.1  # float(input('Grados brix alimentación (m/m): '))
    L[n, 1] = 0.6  # float(input('Grados brix salida (m/m): '))
    L[0, 2] = 26.7  # float(input('Temperatura de alimentación (ºC): '))

    return [L,
            n,
            Tst,
            V,
            Q,
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


def calculateTemperaturePure(n, L, BPE):
    Tpuros = []
    for i in range(1, n+1):
        Temp_puros = L[i, 2] - BPE[i-1]
        Tpuros.append(Temp_puros)
    return Tpuros


def calculateCondensedTemperature(V, n, Tst, L):
    i = 0
    for i in range(0, n+1):
        if i == 0:
            V[i, 1] = Tst
        elif i > 0:
            V[i, 1] = L[i, 2]
    i += 1


def calculateBpe(L, Vt, n):
    Bpe = []
    for i in range(1, n+1):
        L[i, 0] = L[i-1, 0] - Vt
        L[i, 1] = (L[i-1, 0]*L[i-1, 1])/L[i, 0]
        cal2 = round(2*(L[i-1, 1]*100)/(100 - (L[i-1, 1]*100)), 2)
        Bpe.append(cal2)
    return Bpe


def calculateBpe_New(L, n):
    Bpe = []
    for i in range(0, n):
        cal2 = round(2*(L[i, 1]*100)/(100 - (L[i, 1]*100)), 2)
        Bpe.append(cal2)
    return Bpe


def calculateU(n):
    U = []
    k = 0
    for k in range(1, n+1):
        stp = (1500)/n
        cal = ((2500 - (k-1)*stp))/1000  # kW//°C m^2
        U.append(cal)
    k = +1
    return U

# Verificar que la suma dé lo mismo que el disponible
# Pasar el vector de las U como parámetro


def calculateDT(n, DeltaTdisp, U):
    DT = []
    iU = []
    sum = 0

    for i in range(0, n):
        cal2 = 1/U[i]
        iU.append(cal2)
    for k in range(0, len(iU)):
        sum = sum + iU[k]
    for j in range(0, n):
        cal1 = round((DeltaTdisp*(1/U[j]))/sum, 3)
        DT.append(cal1)
    return DT


def globalCalculate(inputs):
    [
        L,
        n,
        Tst,
        V,
        Q,
        Pabsres] = inputs
    print(inputs)

    # Balance de masa inicial - Primera aproximación de los flujos de vapor Vi = Vi+1 =...= Vn

    L[n, 0] = (L[0, 0]*L[0, 1])/(L[n, 1])  # Flujo de salida
    Vt = round((L[0, 0] - L[n, 0])/n, 2)

    BPE = calculateBpe(L, Vt, n)
    U = calculateU(n)

    Tsatn = round(((Bt/(At - np.log(Pabsres))) + Ct), 2)

    DeltaTneto = round(Tdif(Tst, Tsatn), 2)
    DeltaTdisp = round(DeltaTneto - np.sum(BPE), 2)

    DT = calculateDT(n, DeltaTdisp, U)

    calculateTemperature(L, Tst, DT, n)
    Tpuros = calculateTemperaturePure(n, L, BPE)
    calculateCondensedTemperature(V, n, Tst, L)

    k = 0
    iter = 0
    count = False
    while not count:

        # Capacidad calorífica de los líquidos concentrados

        d1 = -2.844669*10**-2
        d2 = 4.211925
        d3 = -1.017034*10**-3
        d4 = 1.311054*10**-5
        d5 = -6.756469*10**-8
        d6 = 1.724481*10**-10

        # Entalpía de corrientes de líquido concentrado

        cont = []
        hLi = []

        L[0, 3] = d1 + d2*L[0, 2] + d3*L[0, 2] + \
            d4*L[0, 2] + d5*L[0, 2] + d6*L[0, 2]

        for i in range(0, n):
            h = (d1 + d2*Tpuros[i] + d3*Tpuros[i]**2 + d4 *
                 Tpuros[i]**3 + d5*Tpuros[i]**4 + d6*Tpuros[i]**5)
            hLi.append(h)

        for i in range(0, n):
            cont.append(
                hLi[i] + (((1 - ((0.6 - 0.0008*L[i, 2])*L[i, 1]))*4.184))*BPE[i])
            L[i+1, 3] = cont[i]

        # Entalpía de los condensados

        hci = []
        i = 0
        for i in range(0, n):
            if i == 0:
                L[i+1, 4] = round(d1 + d2*Tst + d3*Tst**2 + d4 *
                                  Tst**3 + d5*Tst**4 + d6*Tst**5, 2)
            else:
                L[i+1, 4] = round(d1 + d2*Tpuros[i] + d3*Tpuros[i]**2 +
                                  d4*Tpuros[i]**3 + d5*Tpuros[i]**4 + d6*Tpuros[i]**5, 2)
                # hci.append(cal2)
                #L[i+1,4]= hci[i]

        # Entalpía específica de las corrientes de vapor saturado

        a = 64.87678
        b = 11.76476
        c = -11.94431
        d = 6.29015
        e = -0.99893
        Tcr = 647.096  # K

        for i in range(0, n+1):
            if i == 0:
                V[i, 2] = np.exp(math.sqrt(a+b*np.log(1/((Tst+273.15)/Tcr))**0.35 + c/(
                    (Tst+273.15)/Tcr)**2 + d/((Tst+273.15)/Tcr)**3 + e/((Tst+273.15)/Tcr)**4))  # kJ/kg

            elif i > 0:
                V[i, 2] = np.exp(math.sqrt(a+b*np.log(1/((V[i, 1]+273.15)/Tcr))**0.35 + c/(
                    (V[i, 1]+273.15)/Tcr)**2 + d/((V[i, 1]+273.15)/Tcr)**3 + e/((V[i, 1]+273.15)/Tcr)**4))  # kJ/kg

        # Entalpía de vaporización para la generación de vapor

        for i in range(1, n+1):
            V[i, 3] = V[i-1, 2]-L[i, 4]

        # Balances de materia y energía
        i = 0
        G = np.zeros((n+1, n+1))
        for i in range(0, n+1):
            if i == 1:
                G[i, i-1] = V[i, 3]
                G[i, i] = - V[1, 2]

            elif (i == 0):
                for y in range(1, n+1):
                    G[0, y] = 1

            else:
                G[i, i] = -V[i, 2]
                G[i, i-1] = V[i, 3]
            i = +1

        ind = np.zeros((n+1, 1))

        u = 0
        for u in range(0, n+1):
            if u == 0:
                ind[u] = L[0, 0] - L[n, 0]
            else:
                ind[u] = L[u, 3]*L[u, 0] - L[u-1, 3]*L[u-1, 0]
            u = u+1

        result_vap = np.linalg.solve(G, ind)

        # Reasignación de flujos másicos de vapor

        for k in range(0, n+1):
            V[k, 0] = result_vap[k]

        # Cálculo porcentaje de error entre los flujos de vapor

        porcentaje_error = []
        for p in range(1, n+1):
            porcentaje_error.append(abs(round((Vt-V[p, 0])/Vt, 2)))

        # Cálculo del calor transferido en cada efecto

        Q = []
        for j in range(0, n):
            cal6 = round(V[j+1, 3]*V[j, 0]*(1/3600), 2)
            Q.append(round(cal6, 2))  # kW

        # Cálculo de áreas de tansferencia y porcentaje de error
        A = []
        for y in range(0, n):
            cal7 = (Q[y])/(U[y]*DT[y])
            A.append(round(cal7, 2))  # m^2
            print("El área es, :", A[y])

        error_areas_array = np.zeros((n, 1))
        j = 0
        for j in range(0, n):
            if j >= 0 and j < n-1:
                error_areas_array[j] = abs((A[j] - A[j+1])/A[j+1])
            elif j == n-1:
                error_areas_array[j] = abs((A[0] - A[j])/A[j])
            j += 1

        mayor_10_porciento = any(ele > 0.10 for ele in error_areas_array)
        if(mayor_10_porciento == True):           
            sum_areas=[]
            for u in range (0,n):
                sum_areas.append(Q[u]/U[u])
            
            A_prom =  np.sum(sum_areas)/DeltaTdisp
            # Cálculo de nuevos DT 
            
            DT_nuevo=[]
            
            for k in range(0,n):
                cal8= Q[k]/(A_prom*U[k])
                DT_nuevo.append(round(cal8,2))
                print(DT_nuevo[k])
                
            # Nuevo cálculo de las corrientes de líquido concentrado
            
            for k in range(1, n+1):
                L[k, 0] = L[k-1, 0] - V[k, 0]
                L[k, 1] = (L[k-1, 0]*L[k-1, 1])/L[k, 0]
            
            for h in range (0,n):
                DT[h]= DT_nuevo[h]
            
            BPE = calculateBpe_New(L,n)  
            U = calculateU(n)
            calculateTemperature(L, Tst, DT, n)
            calculateCondensedTemperature(V, n, Tst, L)
            Tpuros=calculateTemperaturePure(n, L, BPE)
            iter+=1 
        else:
            count = True

        if iter >= 100: 
            count = True 

        
    print("Numero de iter: ,",iter)


    # Cálculo de la economía del sistema
    suma_vap = 0

    for u in range(1, n+1):
        suma_vap = suma_vap + V[u, 0]

    Economy = round((suma_vap/V[0, 0]), 2)  # Economía del sistema
    last_effects = []

    for i in range(1, n+1):

        effect = []
        effect.append(str(i))
        effect.append(str(L[i, 0]))
        effect.append(str(V[i, 0]))
        effect.append(str(L[i, 1]))
        effect.append(str(U[i - 1]))
        effect.append(str(A[i - 1]))
        effect.append(str(V[i, 1]))
        last_effects.append(effect)

        print("Numero de iter: ,", iter)
        print("Corriente L", i, "=", L[i, 0])
        print("Corriente V", i, "=", V[i, 0])
        print("Fracción másica de azúcar en la corriente L", i, "=", L[i, 1])

    for i in range(0, n):
        print("Coeficiente global de transferencia U", i+1, "=", U[i])
        print("Área de transferencia en el efecto", i+1, "=", A[i])

    print("Temperatura de la corriente de vapor de salida en el efecto n",
          i, "=", V[n, 1])
    print("Temperatura de la corriente de líquido de salida en el efecto n",
          i, "=", L[n, 2])
    print("La economía del sistema es ", round(Economy, 2))

    return [last_effects,  round(V[0, 0], 2), round(Economy, 2)]


