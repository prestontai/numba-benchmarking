from numba import jit
import numpy as np
import sys
import time

@jit(cache=True, nopython=True)
def go_fast(a):
    trace = 0
    for i in range(a.shape[0]):
        for j in range(a.shape[0]):
            trace += np.tanh(a[i, j])
    return a + trace

size = int(sys.argv[1])
x = np.arange(size * size).reshape(size, size)
go_fast(x)

