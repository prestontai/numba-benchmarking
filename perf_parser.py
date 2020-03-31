import sys
import json
from main import RUNS, SIZES

def parse(filename, dest, write_type):
    nojit = list()
    yesjit = list()

    with open(dest, write_type) as stats, open(filename, 'r') as f:
        stats.seek(0)
        lines = stats.readlines()
        total = len(SIZES)
        
        tmp = []
        counter = 0
        for line in f.readlines():
            if 'time elapsed' in line:
                tmp.append(float(line[:15]))
                counter += 1
                if (counter)%10 == 0:
                    stats.write(str(tmp) + '\n')
                    tmp = []

if __name__ == '__main__':
    #dest = sys.argv[1]
    write_type = 'w+'
    parse('perf_results1.txt', 'finalstats.txt', write_type)
    parse('perf_results2.txt', 'finalstats.txt', 'a+')
