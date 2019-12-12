import sys
import re


def run(input_path, output_path):
    regexfunc = '^def [\w]+\([\w\,]*\):$'
    decorator = '@jit\n'
    prog = re.compile(regexfunc)
    

    input_file = open(input_path, 'r')
    optimized_file = open(output_path, 'w+')

    optimized_file.write('from numba import jit\n')

    for line in input_file:
        if prog.match(line):
            optimized_file.write(decorator)
            optimized_file.write(line)
        else:
            optimized_file.write(line)

    input_file.close()
    optimized_file.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Invalid use: ......." )
        exit()
    run(sys.argv[1], sys.argv[2])
