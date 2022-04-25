
import numpy as np
import math 

n   = int(input('¿Cuantos efectos usará?: '))
Tst = float(int(input('Ingresa la temperatura del vapor de calentamiento en °C: '))) #°C 
V   = np.zeros((n+1,5))
L   = np.zeros((n+1,5))
BPE  = np.zeros((1,n))    
U   = np.zeros((1,n))  
Q = np.zeros((1,n))   

eleccion = input('¿Conoces la presión absoluta o manométrica del sistema? (m/a)' )

if eleccion == 'm': 
    Pman = round(float(input('Ingresa la presión manométrica en kPa. Nota: Si la presión es de vacío, ingresa con el signo menos')),2)
    def Pabs(Patm,Pman):
        return Patm + Pman
    Pabsres = Pabs(101.325, Pman)
    print(Pabsres)

elif eleccion == 'a':
    Pabsist = round(float(input('Ingresa la presión absoluta en kPa')),2)
    Pabsres = Pabsist
    print(Pabsres)


#Parámetros de Antoine rango de temperatura de 0 a 200 °C y presión de kPa
At = 16.3872
Bt = 3885.70
Ct = -230.170
    
#Capacidad calorífica del vapor
Av = 3.47
Bv = 1.45E-3
Dv = 0.121E5

L[0,0]    = float(input('Corriente de alimentación (kg/h): '))         
L[0,1]    = float(input('Grados brix alimentación (m/m): ')) 
L[n,1]  = float(input('Grados brix salida (m/m): '))
L[0,2]    = float(input('Temperatura de alimentación (ºC): '))           
V[0,1]   = float(input('Temperatura de vapor de calentamiento (ºC): '))  
V[n,1]  = float(input('Temperatura de vapor condensado (ºC): '))

#Cálculo de U 
for k in range(1,n):
    stp= (2500 - 1000)/n
    U = (2500 - (k-1)*stp) #kW//°C* m
    print(U, end =", ")
    

#Cálculo del BPE

for i in range(1,n):
    BPE[i] = 1 #Está cómo arreglo, pero es una matriz??
    
Tsatn = ((Bt/(At - np.log(Pabsres))) + Ct)


#Cálculo de diferencia de temperatura

def Tdif(a, b):                                   
    return a - b 
DeltaTneto = Tdif(Tst,Tsatn)


#Balance de masa inicial 

L[n,0] = L[1,1]*L[1,2]/(L[n+1,2])
Vt = (L[1,1] - L[n,0])/n

for i in range(2,n):
    L[i+1,0] = L[i,1] - Vt
    L[i+1,1] = (L[i,0]*L[i,1])/L[i+1,0]
    

#Iteraciones

for i in range(1,n):
    
    iU = iU + (1/U(i))
        
    for i in range(1,n):

        BPE[i] = 2*L[n,1]/100 - L[n,1]



#Presión de saturación



    for k in range(1,n+1):
        V[i+1,4] = 1E2 * math.exp(At - (Bt/((V[i+1,1])+273+Ct)))
        L[i+1,4] = 0.8474E-2 * (L[i+1,1]*100)^0.9895 * math.exp(2.570E-2 * (L[i+1,1]*100))*4^0.1163
        L[i+1,2] = V[i+1,1] + L[i+1,4]
    

# Calor latente y entalpía

    for i in range(1,n+1):

        L[i+1,3] = (L[i+1,2]*(1549*L[i+1,1]+4176*(1-L[i+1,1]))+(((L[i+1,3])^2)/2)*(1.96*L[i+1,1]-0.0909*(1-L[i+1,1])) +((L[i+1,3]^3)/3)*(-0.00549*L[i+1,1]+0.00547*(1-L[i+1,1])))/1000; # kJ/kg

#Capacidad calorifica del vapor
    Av = 3.47
    Bv = 1.45E-3
    Dv = 0.121E5

    for i in range(2,n+1):

        V[i+1,2] = 2501.3 + 0.4618 * (Av*(V[i+1,1]) + (Bv/2)*((V[i+1,1]+273)^2-273^2) - Dv*((V[i+1,1]+273)^-1 - 273^-1 )); #kJ/kg
    

# Calor latente para la generación de vapor
    for i in range(1,n+1):
       V[i+1,3] =  2257 * ((1 - (V[i+1,1]+273)/(647.1))/(1-0.577))^0.38


# Función de solución
    x0 = np.zeros[2*n,1]

    for i in range(1,n+1):
        x0[i-1] = V[i,0]
    
    
    for i in range(n+2,2*n):
        x0[i-1] = L[i,0]
    
A = np.zeros[n,1]

# Crear array con [x, fval, exitflag] = fsolve(@evaporator, x0, [] , L, V, n)
    
# El resultado de la función de solución (corrientes de vapor y líquido) son puestos en las matrices
  
for i in range(1,n+1):
        V[i-1,0] = x0[i-1]

    
for i in range(n+1,2*n):
        L[i-1,0] = x0[i-1]
    

for i in range(2,n+1):
        L[i+1,0] = L[i-2,1] - V[i-2,0]
        L[i+1,1] = (L[i-2,1]*L[i-2,1])/L[i+1,0]
    
    
# Cálculo del calor y el área de transferencia de calor en cada efecto
for i in range(1,n):
     Q[i-1] = V[i-1,3]*V[i-1,0]*(1/3600)
     A[i-1] = 1000*Q[i-1]/((BPE[i-1] - L[i,4])*U[i-1])

def G(x,L,V,n):
    pass
    G = np.zeros[2*n,1]
    for i in range (1,n):
        if i == 1:
            G[0] = x[n+2]*L[1,3] + x(2)*V[1,2] - L[0,0]*L[0,3] - x(1)*V[0,3]
            G[1] = x(2) + x(n+2) - L[0,0]
        elif (i == n):
            G[2*n] = L[n,0]*L[n,3] + x[n]*V[n,2] - x(2*n)*L[n-1,3] - x(n)*V[n-1,3]
            G[2*n-1] = L[n,0] + x[n] - x(2*n)
        else:
            G[2*i-2]= x(i+1+n)*L[i+1,4] + x(i+1)*V[i-1,2] - x(n+i)*L[i-1,3]- x(i)*V[i-1,3]
            G[2*i-1] = x(i+1) + x(i+1+n) - x(i+n)

