import numpy as np
from numba import jit, njit, typeof, int32, int64, float32, float64, prange, vectorize, guvectorize, typeof
from functools import wraps, partial
import timeit
import time
import copy


def simple(old_func, ret_object, parallel=False):
    eager = dict()
    @wraps(old_func)
    def new_func(*args, **kwargs):
        arg_typings = [typeof(arg) for arg in args]
        return  njit((typeof(ret_object))(*arg_typings), parallel=parallel)(old_func)(*args, **kwargs)
        #eager[old_func] = njit((typeof(ret_object))(*arg_typings), parallel=parallel)(old_func)
        #return eager[old_func](*args, **kwargs)
    return new_func


def arg_list(*args):
    info = []
    for i in args:
        if type(i) == np.ndarray:
            info.append(i.size)
        elif type(i) == int:
            info.append(i)
    return info


def eager_decorator(old_func):
    cache = dict() # maps function to its fastest version
    @wraps(old_func)
    def new_func(*args, **kwargs):
        #print(set(cache.values()))
        arg_sizes = tuple(arg_list(*args))
        if (old_func, *arg_sizes) in cache:
            #print('pulling from cache')
            return cache[(old_func, *arg_sizes)](*args, **kwargs)
        arg_typings = [typeof(arg) for arg in args]
        argc = len(arg_typings)

        dup = copy.deepcopy(args)
        #get return typings
        start = time.perf_counter()
        res = old_func(*dup, **kwargs)
        old_duration = time.perf_counter() - start
        res_typings = typeof(res)

        #old_time_duration = timeit.timeit(partial(old_func, *args, **kwargs))

        # one run to warm it up first
        numba_f = njit((res_typings)(*arg_typings), cache=True)(old_func)
        numba_f(*args, **kwargs)
        start = time.perf_counter()
        numba_f(*args, **kwargs)
        numba_duration = time.perf_counter() - start
        
        #numba_time_duration = timeit.timeit(partial(numba_f, *args, **kwargs))

        #print(old_duration, numba_duration)
        if old_duration < numba_duration:
            cache[(old_func, *arg_sizes)] = old_func
        else:
            cache[(old_func, *arg_sizes)] = numba_f
        return res
    return new_func

'''
#actual experiment
@eager_decorator
def one(a):
    print(a)
    return np.arange(40)

@eager_decorator
def two(a, b):
    print(a, b)
    return np.arange(40)


#print(two(3.78, np.arange(20)))
print(one(5.0))
print(two(np.arange(3), 3.0))
print(two(np.arange(3), 3.0))
#print(one(np.arange(56)))
#print(two(np.arange(5), np.arange(9)))
#print(two(5.0, 2.8))

@eager_decorator
def loop1(A,B):
    a=np.copy(A)
    b=np.copy(B)

    for i in range (1,a.shape[1]-1):
        for j in range (1,a.shape[0]-1):
            a[j,i] = a[j - 1,i] + b[j,i];
            b[j,i] = b[j,i]**2

    return a,b

a = np.arange(300000)
b = np.arange(300000)
a = a.reshape(100, 3000)
b = b.reshape(100, 3000)

for i in range(10):
    print(loop1(a, b))
'''
