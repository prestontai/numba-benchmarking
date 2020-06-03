import numpy as np
import sys

#       no dependence - vectorizable
#       jump in data access
def s1111(a, b, c, d):
    for i in range(a.shape[0]//2):
        a[2*i] = c[i] * b[i] + d[i] * b[i] + c[i] * c[i] + d[i] * b[i] + d[i] * c[i]

if __name__ == '__main__':
    size = int(sys.argv[1])
    a = np.arange(size)
    b = np.arange(size)
    c = np.arange(size)
    d = np.arange(size)

    s1111(a, b, c, d)

