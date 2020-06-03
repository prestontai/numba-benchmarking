import numpy as np
import sys
import math
import random

def s112(a, b):
    for i in range(a.shape[0] - 2, -1, -1):
        a[i + 1] = a[i] + b[i]

if __name__ == '__main__':
    size = int(sys.argv[1])
    a = np.arange(size)
    b = np.arange(size)

    s112(a,b)

