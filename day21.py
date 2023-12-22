from functools import reduce
import re
import sys

def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

drns = [(1, 0), (0, 1), (-1, 0), (0, -1)]

plan = []
width = height = 0
steps = set()

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input21.txt') as f:
    lines = f.readlines()
    width = len(lines[0].strip())
    height = len(lines)
    x = y = 0
    for line in lines:
        plan.append(line.strip())
        if 'S' in line:
            x = line.find('S')
            steps.add((x, y))
        y += 1

#print(plan, width, height, steps)
print(width, height)

for i in range(64):
    next_gen = set()
    for step in steps:
        neighbours = [vadd(step, drn) for drn in drns]
        neighbours = [x for x in neighbours if 0 <= x[0] < width and 0 <= x[1] < height]
        neighbours = [x for x in neighbours if plan[x[1]][x[0]] != '#']
        for neighbour in neighbours:
            next_gen.add(neighbour)
    steps = next_gen

print(len(steps)) # , steps)