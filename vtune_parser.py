import sys
import json

def parse(filename):
    nojit = list()
    yesjit = list()


    with open('stats.txt', 'a+') as stats, open(filename, 'r') as f:
        stats.seek(0)
        lines = stats.readlines()
        if len(lines) != 1:
            print('Invalid file stats.txt')
            return

        try:
            s = json.loads(lines[0])
        except ValueError:
            print('Error in stats.txt')
            return

        total = len(s)
        counter = 0

        for line in f.readlines():
            if 'Elapsed Time' in line:
                if counter < 4:
                    nojit.append(float(line[14:-2]))
                else:
                    yesjit.append(float(line[14:-2]))
                counter = counter + 1

        stats.write('\n' + str(nojit) + '\n')
        stats.write(str(yesjit))
        


if __name__ == '__main__':
    filename = sys.argv[1]

    parse(filename)

