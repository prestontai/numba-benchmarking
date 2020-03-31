from numba import jit
import numpy as np
import sys
import math
import random

size = int(sys.argv[1])

@jit(cache=True, nopython=True)
def s112(a, b):
    for i in range(size - 2, -1, -1):
        a[i + 1] = a[i] + b[i]


a = np.arange(size)
b = np.arange(size)

s112(a,b)

