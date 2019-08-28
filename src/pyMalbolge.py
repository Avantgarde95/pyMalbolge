#!usr/bin/env python

import sys

TABLE_CRAZY = (
    (1, 0, 0),
    (1, 0, 2),
    (2, 2, 1)
)

ENCRYPT = list(map(ord,
              '5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1CB'\
              '6v^=I_0/8|jsb9m<.TVac`uY*MK\'X~xDl}REokN:#?G\"i@'))

OPS_VALID = (4, 5, 23, 39, 40, 62, 68, 81)

POW9, POW10 = 3**9, 3**10

# --------------------------------------------------

def rotate(n):
    return POW9*(n%3) + n/3

def crazy(a, b):
    result = 0
    d = 1

    for i in range(10):
        result += TABLE_CRAZY[int((b/d)%3)][int((a/d)%3)] * d
        d *= 3

    return result

def initialize(source, mem):
    i = 0

    for c in source:
        if c == ' ' or c == '\n':
            continue

        if (ord(c)+i) % 94 not in OPS_VALID:
            print('Invalid character in the source file')
            sys.exit(1)

        if i == POW10:
            print('Source file is too long')
            sys.exit(1)

        mem[i] = ord(c)
        i += 1

    while i < POW10:
        mem[i] = crazy(mem[i-1], mem[i-2])
        i += 1

def interpret(mem):
    write = sys.stdout.write
    flush = sys.stdout.flush
    read = sys.stdin.read

    a, c, d = 0, 0, 0

    while 1:
        if mem[c] < 33 or mem[c] > 126:
            return

        v = (mem[c]+c) % 94

        if v == 4:                        # jmp [d]
            c = mem[d]
        elif v == 5:                      # out a
            write(chr(int(a % 256)))
            flush()
        elif v == 23:                     # in a
            a = ord(read(1))
        elif v == 39:                     # rotr[d]; mov a, [d]
            a = mem[d] = rotate(mem[d])
        elif v == 40:                     # mov d, [d]
            d = mem[d]
        elif v == 62:                     # crz [d], a; mov a, [d]
            a = mem[d] = crazy(a, mem[d])
        # elif v == 68:                   # nop
        #     pass
        elif v == 81:                     # end
            return
        else:
            pass

        if mem[c] >= 33 and mem[c] <= 126:
            mem[c] = ENCRYPT[mem[c] - 33]

        c = 0 if c == POW10-1 else c+1
        d = 0 if d == POW10-1 else d+1

# --------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('No arguments')
        sys.exit(1)

    filename = sys.argv[1]

    try:
        with open(filename, 'r') as p:
            source = p.read()
    except IOError:
        print('Unable to open the file')
        sys.exit(1)

    mem = [0] * POW10
    initialize(source, mem)

    try:
        interpret(mem)
    except KeyboardInterrupt:
        print('\nUser interrupt')
        sys.exit(0)
