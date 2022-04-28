import numpy as np 
n=3
U = []
for k in range(1,n):
    stp= (2500 - 1000)/n
    cal= ((2500 - (k-1)*stp))/1000 #kW//°C* m
    U.append((cal))
print(U[1])

L= np.zeros((n,5))
BPE=[]
for i in range(1,n):
    L[i,0] = L[i-1,0] - 5000
    L[i,1] = (L[i-1,0]*L[i-1,1])/L[i,0]
    cal2 = 2*L[i-1,1]/100 - L[i-1,1]
    BPE.append(cal2)
print(BPE[2])


