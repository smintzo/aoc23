from functools import reduce
import re
import sys

def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])

drns = [(1, 0), (0, 1), (-1, 0), (0, -1)]

TODO = 'todo'
DONE = 'done'

plan = []
width = height = 0
steps = {} # {(pal_x, pal_y): {TODO: {locations}, DONE: {(location): even?}}

def pp(s):
    for p_id, p in s.items():
        print('palette: ', p_id)
        for y in range(height):
            l = ''
            for x in range(width):
                if (x, y) in p[DONE]:
                    l += 'E' if p[DONE][(x, y)] else 'O'
                elif (x, y) in p[TODO]:
                    l += '*'
                else:
                    l += plan[y][x]
            print(l)
        print('')
    print('\n')

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input21.txt') as f:
    lines = f.readlines()
    width = len(lines[0].strip())
    height = len(lines)
    x = i = 0
    for line in lines:
        plan.append(line.strip())
        if 'S' in line:
            x, y = line.find('S'), i
            steps[(0, 0)] = {TODO: {(x, y)}, DONE: {}}
        i += 1

#print(plan, width, height, steps)
print(width, height)

done_palettes = set()
target = 65 + 131 * 8
target_is_even = (target % 2 == 0)
total = 0
for i in range(target+1):
    evens = (i % 2 == 0)

    #print('iteration ', i)
    #print('===============')

    if i % 100 == 0:
        count_ends = 0
        for p_id, pal in steps.items():
            count_ends += len(pal[TODO])
        print(i, ": ", count_ends)

    next_gen = {k: {TODO: set(), DONE: v[DONE]} for k, v in steps.items()}
    for p_id, palette in steps.items():
        for step in palette[TODO]:
            next_gen[p_id][DONE][step] = evens
            neighbours = [vadd(step, drn) for drn in drns]
            for (nx, ny) in neighbours:
                if 0 <= nx < width and 0 <= ny < height:
                    if plan[ny][nx] != '#' and (nx, ny) not in next_gen[p_id][DONE].keys():
                        next_gen[p_id][TODO] |= {(nx, ny)}
                else:
                    if nx < 0:
                        nk = vadd(p_id, (-1, 0))
                        nx += width
                    elif nx >= width:
                        nk = vadd(p_id, (1, 0))
                        nx -= width
                    elif ny < 0:
                        nk = vadd(p_id, (0, -1))
                        ny += height
                    else:
                        nk = vadd(p_id, (0, 1))
                        ny -= height
                    if plan[ny][nx] != '#':
                        if nk not in done_palettes:
                            if nk not in next_gen:
                                next_gen[nk] = {TODO: {(nx, ny)}, DONE: {}}
                            else:
                                next_gen[nk][TODO] |= {(nx, ny)}


        if len(next_gen[p_id][TODO]) == 0:
            score = len({k: v for k, v in next_gen[p_id][DONE].items() if v == target_is_even})
            #print(i % 2, p_id, score)
            total += score
            done_palettes.add(p_id)
            del next_gen[p_id]

    #pp(steps)
    #pp(next_gen)

    prev = steps
    steps = next_gen

old_score = total
for p_id, pal in next_gen.items():
    score = len({k: v for k, v in next_gen[p_id][DONE].items() if v == target_is_even})
    #print(p_id, score)
    total += score

print(total, old_score, total-old_score)
