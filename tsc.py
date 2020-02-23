import numpy as np

#	linear dependence testing
#	no dependence - vectorizable
def s000():
    # call init to create 5 1D arrays U,V,X,Y,Z
    # X[i] = 1,...,111
    # Y[i] = 2,...,112
    # Z[i] = 3,...,113
    # U[i] = 4,...,114
    # V[i] = 5,...,115
    
    X = np.array([i for i in range(1,112)])
    Y = np.array([i for i in range(2,113)])
    Z = np.array([i for i in range(3,114)])
    U = np.array([i for i in range(4,115)])
    V = np.array([i for i in range(5,116)])
    
    for i in range(111):
        X[i] = Y[i] + 1
    
    # dummy


#	linear dependence testing
#	no dependence - vectorizable
def s111():
    a = np.array([1 for i in range(111)])
    b = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    c = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    d = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    e = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    
    for i in range(1, 111, 2):
        a[i] = a[i - 1] + b[i]
        
        
#	no dependence - vectorizable
#	jump in data access
def s1111():
    a = np.array([1 for i in range(111)])
    b = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    c = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    d = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    e = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    
    for i in range(111/2):
        a[2*i] = c[i] * b[i] + d[i] * b[i] + c[i] * c[i] + d[i] * b[i] + d[i] * c[i]
        
#   linear dependence testing
#	loop reversal
def s112():
    a = np.array([1 for i in range(111)])
    b = np.array([(1.0/(float((i+1)*(i+1)))) for i in range(111)])
    
    for i in range(111 - 2, -1, -1):
        a[i + 1] = a[i] + b[i]