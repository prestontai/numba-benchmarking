import sys
import json

def parse(filename, dest, write_type):
    with open(dest, write_type) as stats, open(filename, 'r') as f:
        stats.seek(0)
        lines = stats.readlines()
        for line in f.readlines():
            if 'time elapsed' in line:
                stats.write(str(float(line[:15])) + '\n')

if __name__ == '__main__':
    #dest = sys.argv[1]
    write_type = 'w+'
    parse('perf_results1.txt', 'finalstats.txt', write_type)
    parse('perf_results2.txt', 'finalstats.txt', 'a+')
