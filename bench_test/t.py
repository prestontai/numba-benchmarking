import numpy as np
import sys
import time

x = np.arange(10000).reshape(100, 100)

def go_fast(a):
    trace = 0
    for i in range(a.shape[0]):
        trace += np.tanh(a[i, i])
    return a + trace

'''
# DO NOT REPORT THIS... COMPILATION TIME IS INCLUDED IN THE EXECUTION TIME!
start = time.time()
go_fast(x)
end = time.time()
print("Elapsed (with compilation) = %s" % (end - start))
'''

# NOW THE FUNCTION IS COMPILED, RE-TIME IT EXECUTING FROM CACHE
#start = time.time()

for i in range(int(sys.argv[1])):
    go_fast(x)
#end = time.time()
#print("Elapsed (after compilation) = %s" % (end - start))
