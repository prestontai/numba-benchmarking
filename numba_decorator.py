import os
import re
import sys

OVERWRITE = True

def run(input_path, output_path):
    # I don't need to make the file if it already exists.
    if os.path.exists(output_path) and not OVERWRITE:
        return 0

    regexfunc = '^(\s*)(def [\w_]+\([\w\,_\s]*\):)$'
    decorator = '@jit(cache=True, nopython=True)\n'
    #decorator = '@jit(nopython=True)\n'
    regexshebang = '^#![/\w+]+/*$'
    prog = re.compile(regexfunc)
    prog2 = re.compile(regexshebang)
    shebangline = -1
    futureline = -1

    i = open(input_path, 'r')
    o = open(output_path, 'w')

    for line in enumerate(i):
        if prog2.match(line[1]):
            shebangline = line[0]
        elif '__future__' in line[1] and 'import' in line[1]:
            futureline = line[0]

    print(shebangline, futureline)

    i.seek(0)

    if shebangline == -1 and futureline == -1:
        o.write('from numba import jit\n')

        for line in i:
            if prog.search(line):
                o.write(prog.search(line).group(1) + decorator)
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
                o.write(prog.match(line[1].group(1)) + decorator)
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

