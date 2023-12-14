from functools import reduce
import re
import sys

def plus(x, y): return x + y
def nl(x, y): return x + '\n' + y

platform = []
platform_hist = []

def transpose_platform():
    global platform

    platform = [reduce(plus, ([platform[y][x] for y in range(len(platform)-1, -1, -1)])) for x in range(len(platform[0]))]

def pp(n=0, d=0):
    print(n, d, '\n', reduce(nl, platform) + '\n')

def score():
    width = len(platform[0])
    total = 0
    for row in platform:
        total += reduce(plus, [width - x for x in range(width) if row[x] == 'O'], 0)
    return total

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input14.txt') as f:

    lines = f.readlines()

    for line in lines:
        platform.append(line.strip())

transpose_platform()
transpose_platform()
transpose_platform()

for n in range(100000):
    for d in range(4):
        width = len(platform[0])
        height = len(platform)

        for y in range(height):
            row = platform[y]
            
            for x in range(1, width):
                j = x
                stopped = False
                while j > 0 and not stopped:
                    if row[j-1:j+1] == '.O':
                        row = row[:j-1] + 'O.' + row[j+1:]
                    else:
                        stopped = True
                    j -= 1
            platform[y] = row
            
        transpose_platform()

    key = str(d) + reduce(plus, platform) + str(score())
    if key in platform_hist:
        loop_start = platform_hist.index(key)
        print('loop found!!!', n, loop_start, score())
        #print(key, '\n')
        #print(reduce(nl, platform_hist))
        cycl = n - platform_hist.index(key)
        print('cycle length = ', cycl)
        offset = (999999999 - loop_start) % cycl
        print('offset = ', offset)
        print(platform_hist[loop_start + offset])
        sys.exit()
    else:
        platform_hist.append(key)
    #pp(n,d)
            
print(score())

