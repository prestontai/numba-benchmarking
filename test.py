def summing(a,b):
    return a+b

def multi():
    return 5*5

def subtract(a,b):
    return a-b

def run():
    total = 0

    for i in range(1,2000):
        for j in range(1,2000):
            total += i
            total *= j

    print(total)

if __name__ == '__main__':
    run()
