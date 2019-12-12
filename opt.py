from numba import jit
@jit
def summing(a,b):
    return a+b

@jit
def multi():
    return 5*5

@jit
def subtract(a,b):
    return a-b

@jit
def run():
    total = 0

    for i in range(1,100):
        for j in range(1,100):
            total += i
            total *= j

    print(total)

if __name__ == '__main__':
    run()
