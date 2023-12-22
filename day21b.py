from functools import reduce
import re
import sys

def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

drns = [(1, 0), (0, 1), (-1, 0), (0, -1)]

plan = []
width = height = sx = sy = 0
steps = {}

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\test21.txt') as f:
    lines = f.readlines()
    width = len(lines[0].strip())
    height = len(lines)
    i = 0
    for line in lines:
        plan.append(line.strip())
        if 'S' in line:
            sx = line.find('S')
            sy = i
            print(sx, sy)
        i += 1

    for x in range(width):
        for y in range(height):
            if (x, y) == (sx, sy):
                steps[(x, y)] = {(0, 0)}
            else:
                steps[(x, y)] = set()

#print(plan, width, height, steps)
print(width, height)

target = 6

prev_gen = {(x, y): set() for x in range(width) for y in range(height)}

for i in range(target):
    next_gen = {(x, y): set() for x in range(width) for y in range(height)}
    for (x, y) in [(xx, yy) for xx in range(width) for yy in range(height) if steps[(xx, yy)]]:
        neighbours = [vadd((x, y), drn) for drn in drns]

        for (nx, ny) in neighbours:
            if 0 <= nx < width and 0 <= ny < height:
                if plan[ny][nx] != '#':
                    #print(nx, ny, next_gen[(nx, ny)], x, y, steps[(x, y)])
                    next_gen[(nx, ny)] |= steps[(x, y)]
                    #print(next_gen)
            else:
                drn = (0, 0)
                if nx < 0:
                    drn = (-1, 0)
                    nx += width
                elif nx >= width:
                    drn = (1, 0)
                    nx -= width
                elif ny < 0:
                    drn = (0, -1)
                    ny += height
                else:
                    drn = (0, 1)
                    ny -= height
                if plan[ny][nx] != '#':
                    #print(steps[(x, y)])
                    #print(steps)
                    next_gen[(nx, ny)] |= {vadd(z, drn) for z in steps[(x, y)]}

    if ((i + 1) % 2) == (target % 2):


    prev_gen = steps
    steps = next_gen

#print({k: v for k, v in steps.items() if len(v)>0})
total = 0
for k, v in steps.items():
    total += len(v)
print(total)

#some analysis of totals for whole / partial increases every couple of squares gave the following formula:
#def total(n):
#    return(n*n*7734 + (n-1)*(n-1)*7719 + n*30988 - 3802)

