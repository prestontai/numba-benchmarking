import sys
import re


def run(inputfile, outputfile):
    regexfunc = '^def [\w]+\([\w\,]*\):$'
    decorator = '@jit\n'
    regexshebang = '^#![/\w+]+/*$'
    prog = re.compile(regexfunc)
    prog2 = re.compile(regexshebang)
    shebangline = -1
    futureline = -1
    
    i = open(inputfile, 'r')
    o = open(outputfile, 'w')

    for line in enumerate(i):
        if prog2.match(line[1]):
            shebangline = line[0]

        elif line[1] == 'import __future__\n':
            futureline = line[0]

    print(shebangline, futureline)

    i.seek(0)

    if shebangline == -1 and futureline == -1:
        o.write('from numba import jit\n')
        
        for line in i:
            if prog.match(line):
                o.write(decorator)
                o.write(line)
            else:
                o.write(line)
    else:
        beginning = max(shebangline, futureline)
        
        for line in enumerate(i):
            if line[0] == beginning:
                o.write(line[1])
                o.write('from numba import jit\n')
            elif prog.match(line[1]):
                o.write(decorator)
                o.write(line[1])
            else:
                o.write(line[1])
                
            

    i.close()
    o.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid use: ......." )
        exit()
    run(sys.argv[1], sys.argv[2])
