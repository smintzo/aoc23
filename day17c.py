from functools import reduce
import re
import sys

class State:
    def __init__(self, drn, steps, score):
        self.drn = drn
        self.steps = steps
        self.score = score
        self.new = True

    def __repr__(self):
        return 'drn=' + str(self.drn) + ' steps=' + str(self.steps) + \
            ' score=' + str(self.score) + ' new=' + str(self.new)

class Location:
    def __init__(self, loc, cost):
        self.loc = loc
        self.cost = cost
        self.bests = {} # keyed by direction, steps

    def __repr__(self):
        return 'loc=' + str(self.loc) + ' cost=' + str(self.cost) + ' bests=' + str(self.bests)

    def set_best(self, new):
        for steps in range(new.steps, 4):
            if (new.drn, steps) in self.bests:
                if self.bests[(new.drn, steps)].score > new.score:
                    if steps == new.steps:
                        self.bests[(new.drn, steps)].score = new.score
                        self.bests[(new.drn, steps)].new = True
                    else:
                        del self.bests[(new.drn, steps)]
            else:
                if steps == new.steps:
                    self.bests[(new.drn, steps)] = State(new.drn, steps, new.score)

    def finished(self):
        done = (len({k: v for k, v in self.bests.items() if v.new}) == 0)
        return done

    def first_new_end(self):
        for k, v in self.bests.items():
            if v.new:
                return v

    def min_score(self):
        ms = -1
        for k, v in self.bests.items():
            ms = v.score if ms == -1 else min(ms, v.score)
        return ms

plan = {} # (x, y): Location

def pp():
    for k, v in plan.items():
        print(v.loc, v.min_score())

def plan_finished():
    done = True
    for k, v in plan.items():
        if not v.finished():
            done = False
            break
    return done

def first_open_loc():
    for k, v in plan.items():
        if not v.finished():
            return v

def open_locs():
    n = 0
    for k, v in plan.items():
        if not v.finished():
            n += 1
    return n

L = (-1, 0)
R = (1, 0)
U = (0, -1)
D = (0, 1)

drns = [L, R, U, D]

turn_dirs = {L: (U, D), R: (U, D), U: (L, R), D: (L, R)}

width = height = 0

def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def valid_loc(l):
    return 0 <= l[0] < width and 0 <= l[1] < height

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\test17.txt') as f:
    lines = f.readlines()
    width, height = len(lines[0].strip()), len(lines)
    plan = {(x, y): {'score': int(lines[y][x])} for y in range(height) for x in range(width)}

print(plan)

plan[(width-1, height-1)]['bests']=[{'drn': R, 'steps': 0, 'loss': 0}, {'drn': D, 'steps': 0, 'loss': 0}]

improvement_found = True
while improvement_found:
    improvement_found = False

    for y in range(height-1, -1, -1):
        for x in range(width-1, -1, -1):
            if x == width-1 and y == height-1:
                for drn in drns:
                    neighbour = v_add((x, y), drn)
                    if neighbour not in plan:
                        continue
                    
