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
        
        counter = 0
        tmp = []
        prev = 0
        for line in f.readlines():
            if 'Elapsed Time' in line:
                tmp.append(float(line[14:-2]))
                #if counter < RUNS * total:
                #    nojit.append(float(line[14:-2]))
                #else:
                #    yesjit.append(float(line[14:-2]))
            '''
                counter = counter + 1
            if counter == total:
                counter = 0
                stats.write(str(tmp) + '\n')
                tmp = []
            '''
        stats.write(str(tmp) + '\n')

        #stats.write('\n' + str(nojit) + '\n')
        #stats.write(str(yesjit))
        


if __name__ == '__main__':
    #dest = sys.argv[1]
    write_type = 'w+'
    parse('results1.txt', 'justopt.txt', write_type)
    parse('results2.txt', 'justopt.txt', 'a+')
