from numba import jit
import numpy as np
import sys
import math
import random

size = int(sys.argv[1])

@jit(cache=True, nopython=True)
def s111(a, b):
    for i in range(1, size, 2):
        a[i] = a[i - 1] + b[i]

a = np.arange(size)
b = np.arange(size)

s111(a,b)

