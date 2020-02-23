import sys
import json
from main import RUNS, SIZES

def parse(filename, source):
    nojit = list()
    yesjit = list()


    with open(source, 'w+') as stats, open(filename, 'r') as f:
        stats.seek(0)
        lines = stats.readlines()
        total = len(SIZES)
        
        counter = 0
        tmp = []
        for line in f.readlines():
            if 'Elapsed Time' in line:
                tmp.append(float(line[14:-2]))
                #if counter < RUNS * total:
                #    nojit.append(float(line[14:-2]))
                #else:
                #    yesjit.append(float(line[14:-2]))
                counter = counter + 1
            if counter == total:
                counter = 0
                stats.write(str(tmp) + '\n')
                tmp = []


        #stats.write('\n' + str(nojit) + '\n')
        #stats.write(str(yesjit))
        


if __name__ == '__main__':
    source = sys.argv[1]
    parse('results.txt', source)
    
