from functools import reduce
import re
import sys

instructions = []

dig = {(0, 0)}

dirs = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}

def vadd(a, b):
    return (a[0]+b[0], a[1]+b[1])

def pp(d, fn):
    f = open(fn + '.txt', 'w')
    dig = list(d)
    minx = reduce(lambda x, y: min(x, y[0]), dig, dig[0][0])
    maxx = reduce(lambda x, y: max(x, y[0]), dig, dig[0][0])
    miny = reduce(lambda x, y: min(x, y[1]), dig, dig[0][1])
    maxy = reduce(lambda x, y: max(x, y[1]), dig, dig[0][1])

    for y in range(miny, maxy+1):
        s = ''
        for x in range(minx, maxx+1):
            s += '#' if (x, y) in dig else '.'
        f.write(s + '\n')
    f.close()

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input18.txt') as f:
    lines = f.readlines()

    for line in lines:
        bits = line.strip().split(' ')
        instructions.append((bits[0], int(bits[1]), bits[2]))

#print(instructions)

loc = (0, 0)
for i in instructions:
    for step in range(i[1]):
        loc = vadd(loc, dirs[i[0]])
        dig.add(loc)

#print(dig)
#print(len(dig))

dig = list(dig)

minx = reduce(lambda x, y: min(x, y[0]), dig, dig[0][0])
maxx = reduce(lambda x, y: max(x, y[0]), dig, dig[0][0])
miny = reduce(lambda x, y: min(x, y[1]), dig, dig[0][1])
maxy = reduce(lambda x, y: max(x, y[1]), dig, dig[0][1])
print(minx, '-', maxx)
print(miny, '-', maxy)

dig = set(dig)

new_dig = set()

for y in range(miny, maxy+1):
    inside = False
    edge_from = ''
    for x in range(minx, maxx+1):
        if (x,y) in dig:
            new_dig.add((x,y))
            hole_up = y > miny and (x, y-1) in dig
            hole_down = y < maxy and (x, y+1) in dig
            if edge_from == '':
                if hole_up and not hole_down:
                    edge_from = 'U'
                elif hole_down and not hole_up:
                    edge_from = 'D'
                else:
                    inside = not inside
            else: # edge_from != ''
                if x==maxx or (x+1, y) not in dig:
                    cross = edge_from == 'D' and hole_up or edge_from == 'U' and hole_down
                    if cross:
                        inside = not inside
                    edge_from = ''
        else: # (x, y) not in dig
            if inside:
                new_dig.add((x, y))

#pp(dig, 'dig')
#pp(new_dig, 'nd')
print(len(new_dig))