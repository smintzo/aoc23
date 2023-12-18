from functools import reduce
import re
import sys

plan = {}  # (x, y): (symbol, bEnergised)

dir_map = {('R', '\\'): 'D', ('R', '/'): 'U', ('L', '\\'): 'U', ('L', '/'): 'D'}
dir_map.update({('U', '\\'): 'L', ('U', '/'): 'R', ('D', '\\'): 'R', ('D', '/'): 'L'})
dir_map.update({('L', '-'): 'L', ('R', '-'): 'R', ('U', '|'): 'U', ('D', '|'): 'D'})
dir_map.update({(d, '.'): d for d in ['L', 'R', 'U', 'D']})

dirs = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}

width = height = 0

def pp(allE = False):
    print('  0123456789')
    i = 0
    for y in range(height):
        string = str(i) + ' '
        i += 1
        for x in range(width):
            node = plan[(x, y)]
            if node[0] == '.' or allE:
                string += '*' if node[1] else '.'
            else:
                string += node[0]
        print(string)
    print()

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input16.txt') as f:
    lines = f.readlines()
    width = len(lines[0].strip())
    height = len(lines)
    #print(width, height)
    for y in range(len(lines)):
        line = lines[y]
        for x in range(len(line)):
            plan[(x, y)] = (line[x], False)

starts = [((0, y), 'R') for y in range(height)]
starts += [((width-1, y), 'L') for y in range(height)]
starts += [((x, 0), 'D') for x in range(width)]
starts += [((x, height-1), 'U') for x in range(width)]
#print(starts)

best = 0
for start in starts:
    #print(start)
    light = [start]  # ((x, y), dir)
    light_history = []
    light_done = False
    plan = {k: (v[0], False) for k, v in plan.items()}

    while not light_done:

        light_done = True
        old_light = []
        for beam in light:
            plan[beam[0]] = (plan[beam[0]][0], True)
            if beam not in light_history:
                old_light.append(beam)
                light_done = False
        light_history += old_light

        if not light_done:
            new_light = []
            for beam in old_light:
                symbol = plan[beam[0]][0]
                if (beam[1], symbol) in dir_map:
                    new_dir = dir_map[(beam[1], symbol)]
                    x, y = beam[0][0], beam[0][1]
                    nd = dirs[new_dir]
                    nx, ny = x + nd[0], y + nd[1]
                    if 0 <= nx < width and 0 <= ny < height:
                        new_light.append(((nx, ny), new_dir))
                else:
                    if symbol == '|':
                        nl1 = ((beam[0][0], beam[0][1]+1), 'D')
                        nl2 = ((beam[0][0], beam[0][1]-1), 'U')
                        if 0 <= nl1[0][1] < height:
                            new_light.append(nl1)
                        if 0 <= nl2[0][1] < height:
                            new_light.append(nl2)

                    else: # symbol = '-'
                        nl1 = ((beam[0][0] + 1, beam[0][1]), 'R')
                        nl2 = ((beam[0][0] - 1, beam[0][1]), 'L')
                        if 0 <= nl1[0][0] < width:
                            new_light.append(nl1)
                        if 0 <= nl2[0][0] < width:
                            new_light.append(nl2)
            light = new_light
    #pp()
    #print('\n')
    #pp(True)
    score = len({k: v for k, v in plan.items() if v[1]})
    print(start, score)
    best = max(best, score)

print(best)