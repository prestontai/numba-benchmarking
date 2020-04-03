import json
import os
import sys

def choose_run(normal_file, size, cached="finalstats.txt"):
    numba_file = normal_file[:-3] + 'opt.py'
    with open(cached, 'r') as db:
        reg, opt = db.readlines()
    if reg < opt:
        print("using reg")
        args = "python3 {} {}".format(normal_file, str(size))
    else:
        print("using numba")
        args = "python3 {} {}".format(numba_file, str(size))
    os.system(args)

choose_run(sys.argv[1], sys.argv[2])
