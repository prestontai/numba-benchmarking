if __name__ == '__main__':
    with open('perf_results1.txt', 'r') as f:
        lines = f.readlines()

        group = 0
        counter = 0
        jit = 0
        eager = 0

        for i in lines:
            x = i.split()
            if counter == 0:
                jit += float(x[0])

            elif counter == 1:
                eager += float(x[0])

            counter += 1

            if i == '\n':
                group += 1
                counter = 0

            if group == 4:
                print('jit: ' + str(jit / 4))
                print('eager: ' + str(eager / 4))
                print()
                group = 0
                jit = 0
                eager = 0


