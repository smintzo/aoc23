from functools import reduce
import re
import sys

plan = {} # (x, y): (cost, {dir: (best_score0steps, bs1s, bs2s, bs3s)})

L = (-1, 0)
R = (1, 0)
U = (0, -1)
D = (0, 1)

turn_dirs = {L: (U, D), R: (U, D), U: (L, R), D: (L, R)}

width = height = 0

LOC = 'loc'
DRN = 'drn'
SCORE = 'score'
STEPS = 'steps'

def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def valid_loc(l):
    return 0 <= l[0] < width and 0 <= l[1] < height

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\test17.txt') as f:
    lines = f.readlines()
    width, height = len(lines[0].strip()), len(lines)
    start_steps = (-1, -1, -1, -1)
    start_scores = {(L, 0): start_steps, (R, 0): start_steps, (U, 0): start_steps, (D, 0): start_steps}
    plan = {(x, y): (lines[y][x], start_scores) for y in range(height) for x in range(width)}

#print(plan)

positions = [{LOC: (0, 0), DRN: R, STEPS: 0, SCORE: 0},
             {LOC: (0, 0), DRN: D, STEPS: 0, SCORE: 0}] # ((x, y), dir, num_steps, cost)
while positions:
    new_positions = []
    for pos in positions:
        next_loc = v_add(pos[LOC], pos[DRN])
        if not valid_loc(next_loc): continue
        next_score = pos[COST] + plan[next_loc][0]
        prv_best = plan[next_loc][1][pos[DRN]]
        if next_score < prv_best:
            steps = pos[STEPS]
            if steps < 3:
                new_positions.append({LOC: next_loc, DRN: [pos[DRN]], STEPS: steps + 1, COST: next_score})
                if next_score < plan[next_loc]

                plan = {k: {k2: next_cost if k2 == pos[DRN] else v2 for k2, v2 in v.items()} for k, v in plan.items()}
            for new_drn in turn_dirs[pos[DRN]]:
                new_positions.append({LOC: next_loc, DRN: new_drn, STEPS: 0, COST: next_cost})
                plan = {k: {k2: next_cost if k2 == pos[DRN] else v2 for k2, v2 in v.items()} for k, v in plan.items()}


