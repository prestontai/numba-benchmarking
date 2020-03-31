from numba import jit
import numpy as np
import sys

size = int(sys.argv[1])

#       no dependence - vectorizable
#       jump in data access
@jit(cache=True, nopython=True)
def s1111(a, b, c, d):
    for i in range(size//2):
        a[2*i] = c[i] * b[i] + d[i] * b[i] + c[i] * c[i] + d[i] * b[i] + d[i] * c[i]


a = np.arange(size)
b = np.arange(size)
c = np.arange(size)
d = np.arange(size)

s1111(a, b, c, d)

