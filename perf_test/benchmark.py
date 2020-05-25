import numpy as np
from eager import eager_decorator
from simple import simple
from numba import jit, njit, prange, int64, cuda, typeof
import time
from collections import defaultdict
import sys

TIME_JIT = len(sys.argv) > 1

def s1111(a, b, c, d):
    for i in prange(a.shape[0]//2):
        a[2*i] = c[i] * b[i] + d[i] * b[i] + c[i] * c[i] + d[i] * b[i] + d[i] * c[i]
    return a

def s111(a, b):
    for i in range(1, a.shape[0], 2):
        a[i] = a[i - 1] + b[i]
    return a

def s112(a, b):
    for i in range(a.shape[0] - 2, -1, -1):
        a[i + 1] = a[i] + b[i]
    return a

def go_fast(a):
    trace = 0
    for i in prange(a.shape[0]):
        for j in prange(a.shape[0]):
            trace += np.tanh(a[i, j])
    return a + trace

def many_arr(a, b, c, d, e, f, g):
    for i in prange(a.shape[0]):
        for j in prange(a.shape[1]):
            a[i-1, j] = b[i, j] + c[i, j] + d[i, j] + e[i, j] + f[i, j] + g[i, j]
        b[i-1, j] = a[i, j] + c[i, j]
    return a, b, c, d

def loop1(a,b):
    for i in prange (1,a.shape[1]-1):
        for j in prange (1,a.shape[0]-1):
            a[j,i] = a[j - 1,i] + b[j,i];
            b[j,i] = b[j,i] **2;

    return a,b

def loop2(a, b, c):
    for j in prange (1,a.shape[0]-1):
        for i in prange (1,a.shape[1]-1):
            a[j][i] = a[j-1][i] + c[j][i]

    for j in prange (1,a.shape[0]-1):
        for i in prange (1,b.shape[1]-1):
            b[j][i] = b[j][i-1] + c[j][i]

    return a, b

alpha, beta = np.int32(1), np.int32(2)
def sgemm_manual (a, b, d):
    for i in prange(d.shape[0]):
        for j in prange(d.shape[1]):
            d[i,j] *= beta
        for k in prange(a.shape[1]):
            for j in prange(d.shape[1]):
                d[i,j] += alpha * a[i,k] * b[k,j]
    return d

def sgemm (a, b, d):
    return np.dot(np.multiply(alpha, a), b) + np.multiply(beta, d)

def laplacian(a):
    x = a.shape[0]
    y = a.shape[1]
    laplacian = np.empty((x - 2, y - 2))
    for i in prange(1, x - 1):
        for j in prange(1, y - 1):
            laplacian[i-1, j-1] = np.abs(a[i-1, j] + a[i+1, j] + a[i, j-1] + a[i, j+1] - 4*a[i, j]) > 0.05

    return laplacian

def exp(a, b):
    for n in prange(10):
        for i in prange(a.shape[0]):
            for j in prange(a.shape[1]):
                a[i,j] = b[j] + a[i-1, j]
    return a


a = np.random.rand(1000, 1000)
b = np.random.rand(5000)
a1 = a.copy(), b.copy()
a2 = a.copy(), b.copy()

if TIME_JIT:
    print('jit')
else:
    print('eager')
print('exp')
if TIME_JIT:
    start = time.perf_counter()
    jit_res = njit(exp, parallel=False)(*a1)
    jit_duration = time.perf_counter() - start
    print('{} jit'.format(jit_duration))
else:
    typings = exp(*a1)
    start = time.perf_counter()
    eager_res = simple(exp, typings , parallel=False)(*a2)
    eager_duration = time.perf_counter() - start
    print('{} eager'.format(eager_duration))


flat_sizes = [16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608]
matrix_sizes = [4, 8, 32, 64, 128, 256, 512, 1024, 2048, 4096]
ss = 1000

function_mapping = [
                    ('s111', s111, [ss], 2),
                    ('s112', s112, [ss], 2),
                    ('s1111', s1111,[ss], 4),
                    ('go_fast', go_fast, [ss], 1),
                    ('many_arr', many_arr, [ss], 7),
                    ('loop1', loop1, [ss], 2),
                    ('loop2', loop2, [ss], 3),
                    ('sgemm_manual', sgemm_manual, [ss], 3),
                    #('sgemm', sgemm, [ss], 3),
                    ('laplacian', laplacian, [ss], 1),
                
                    ]
matrix_functions = {go_fast, loop1, loop2, sgemm_manual, sgemm, laplacian, many_arr}
abnormal_step_functions = {s111, s112}
stats_dict = defaultdict(int)

before = False
for (name, f, sizes, arrays) in function_mapping:
    s = sizes[0]

    if f in matrix_functions:
        #orig = [np.arange(s*s, dtype=np.).reshape(s, s) for i in range(arrays)]
        #warm = [np.arange(5*5, dtype=np.float64).reshape(5, 5) for i in range(arrays)]
        orig = [np.random.randint(99999, size=s * s, dtype=np.int32).reshape(s, s) for i in range(arrays)]
        warm = [np.random.randint(99999, size= 25 * 25, dtype=np.int32).reshape(25, 25) for i in range(arrays)]
    else:
        orig = [np.random.randint(99999, size=s, dtype=np.int32) for i in range(arrays)]
        warm = [np.random.randint(99999, size=25, dtype=np.int32) for i in range(arrays)]
    args = [arr.copy() for arr in orig]
    print(typeof(args))

    if f in abnormal_step_functions:
        parallel = False
    else:
        #parallel=True
        parallel = False

    print(name, arrays)

    if TIME_JIT:
        start = time.perf_counter()
        jit_res = njit(f, parallel=parallel)(*args)
        jit_duration = time.perf_counter() - start
        print('{} jit'.format(jit_duration))
    else: 
        typings = f(*warm)
        start = time.perf_counter()
        eager_res = simple(f, typings, parallel=parallel)(*args)
        eager_duration = time.perf_counter() - start
        print('{} eager'.format(eager_duration))
    del args
    del orig

    '''
    print('same result:', np.allclose(jit_res, eager_res))
    print(" It is", "%.4f" % ((jit_duration)/(eager_duration)), "times faster with eager compilation")
    print()
    '''
print()
