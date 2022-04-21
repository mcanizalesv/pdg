
import numpy as np
import math 

Elección = float(input('¿Conoces la presión absoluta o manometrica del sistema? (m/a)' ))

if Elección == 'm': 
    Pman = float(input('Ingresa la peresión manométrica en inHg. Nota: Si la presión es de vacío, ingresa con el signo menos'))
    def Pabs(Patm,Pman):
        return Patm + Pman
    Pabsres = Pabs(26.67, Pman)
    
    
    
n   = int(input('¿Cuantos efectos usará?: '))
V   = np.zeros((n+1,5))
L   = np.zeros((n+1,5))
BPE  = np.zeros((1,n))    
U   = np.zeros((1,n))  
Q = np.zeros((1,n))     

#Antoine Parameters
At = 11.6834
Bt = 3816.44
Ct = -46.13

#Steam heat capacity coefficients 
Av = 3.47
Bv = 1.45E-3
Dv = 0.121E5

L[1,1]    = float(input('Corriente de alimentación (kg/h): '))         
L[1,2]    = float(input('Grados brix alimentación (m/m): ')) 
L[n+1,2]  = float(input('Grados brix salida (m/m): '))
L[1,3]    = float(input('Temperatura de alimentación (ºC): '))           
V[1,2]   = float(input('Temperatura de vapor de calentamiento (ºC): '))  
V[n+1,2]  = float(input('Temperatura de vapor condensado (ºC): '))


Tst = 125 # °C Temperatura del vapor saturado

#for k in range(1,n):
    





#Efecto de temperatura

DeltaT = V[1,2] - V[n+1,2]

for i in range(1,n):
    BPE[i] = (DeltaT*(1/U(i)))/iU #Está cómo arreglo, pero es una matriz???



#Balance de masa inicial 

L[n+1,1] = L[1,1]*L[1,2]/(L[n+1,2])
Vt = (L[1,1] - L[n+1,1])/n

for i in range(2,n):
    L[i,1] = L[i-1,1] - Vt
    L[i,2] = (L[i-1,1]*L[i-1,2])/L[i,1]
    
#V(:1) == Vt

flag2 = 0

#Iteraciones

for i in range(2,n):
    
    iU = iU + (1/U(i))
        
    for i in range(2,n):

        BPE[i] = (DeltaT*(1/U(i)))/iU



#Presión de saturación
#Parámetros de Antoine
    At = 11.6834
    Bt = 3816.44
    Ct = -46.13

    for k in range(1,n+1):
        V[i,5] = 1E2 * math.exp(At - (Bt/((V[i,2])+273+Ct)))
        L[i,5] = 0.8474E-2 * (L[i,2]*100)^0.9895 * math.exp(2.570E-2 * (L[i,2]*100))*V[i,5]^0.1163
        L[i,3] = V[i,2] + L[i,5]
    

# Calor latente y entalpía

    for i in range(1,n+1):

        L[i,4] == (L[i,3]*(1549*L[i,2]+4176*(1-L[i,2]))+(((L[i,3])^2)/2)*(1.96*L[i,2]-0.0909*(1-L[i,2])) +((L[i,3]^3)/3)*(-0.00549*L[i,2]+0.00547*(1-L[i,2])))/1000; # kJ/kg

#Capacidad calorifica del vapor
    Av = 3.47
    Bv = 1.45E-3
    Dv = 0.121E5

    for i in range(2,n+1):

        V[i,3] = 2501.3 + 0.4618 * (Av*(V[i,2]) + (Bv/2)*((V[i,2]+273)^2-273^2) - Dv*((V[i,2]+273)^-1 - 273^-1 )); #kJ/kg
        V[i,3] = 2501.3 + 0.4618 * (Av*(V[i,2]) + (Bv/2)*((V[i,2]+273)^2-273^2) - Dv*((V[i,2]+273)^-1 - 273^-1 )); #kJ/kg
    

# Calor latente para la generación de vapor
    for i in range(1,n+1):
       V[i,4] =  2257 * ((1 - (V[i,2]+273)/(647.1))/(1-0.577))^0.38


# Función de solución
    x0 = np.zeros[2*n,1]

    for i in range(1,n+1):
        x0[i] = V[i,1]
    
    
    for i in range(n+2,2*n):
        x0[i] = L[i-n,1]
    
A = np.zeros[n,1]

# Crear array con [x, fval, exitflag] = fsolve(@evaporator, x0, [] , L, V, n)
    
# El resultado de la función de solución (corrientes de vapor y líquido) son puestos en las matrices
  
for i in range(1,n+1):
        V[i,1] = x0[i]

    
for i in range(n+1,2*n):
        L[i-n,1] = x0(i)
    

for i in range(2,n+1):
        L(i,1) == L(i-1,1) - V(i,1)
        L(i,2) == (L(i-1,1)*L(i-1,2))/L(i,1)
    
    
# Cálculo del calor y el área de transferencia de calor en cada efecto
for i in range(1,n):
     Q(i) == V(i,4)*V(i,1)*(1/3600)
     A(i) == 1000*Q(i)/((BPE(i) - L(i+1,5))*U(i))
    


# Recálculo de DeltaT 
if (flag2 == 0):

    Am = sum(A)/n
        
    for i in range(1,n):
        BPE(i) == BPE(i)*A(i)/Am
        
else:
        
    Am = sum(A in range (2,n))/(n-1)
        
    for i in range(2,n):
        BPE(i) == BPE(i)*A(i)/Am
            

        
def G(x, L, V, n):
    pass
    G = np.zeros(2*n,1)
    for i in range (1,n):
        if(i == 1):
            G(1) == x(n+2)*L(2,4) + x(2)*V(2,3) - L(1,1)*L(1,4) - x(1)*V(1,4)
            G(2) == x(2) + x(n+2) - L(1,1)
        elif (i == n):
            G(2*n-1) == L(n+1,1)*L(n+1,4) + x(n+1)*V(n+1,3) - x(2*n)*L(n,4) - x(n)*V(n,4)
            G(2*n) == L(n+1,1) + x(n+1) - x(2*n)
        else:
            G(2*i-1) == x(i+1+n)*L(i+1,4) + x(i+1)*V(i+1,3) - x(n+i)*L(i,4) - x(i)*V(i,4)
            G(2*i) == x(i+1) + x(i+1+n) - x(i+n)

