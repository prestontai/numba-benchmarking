import numpy as np
from numba import jit, njit

def arg_list(*args):
    info = []
    for i in args:
        try:
            if type(i) == np.ndarray:
                info.append(i.size)
            elif type(i) == int:
                info.append(i)
        except Exception as e:
            print(e)
    print(info)
    return info

def wrapper(*args, **kwargs):
    arg_list(*args)
    arg_list(*kwargs)

wrapper(1, 2, 5, np.arange(50).reshape(2, 25), bob=50, jerry=np.arange(30))
