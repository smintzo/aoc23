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
#                    if steps == new.steps:
                    self.bests[(new.drn, steps)].score = new.score
                    self.bests[(new.drn, steps)].new = True
 #                   else:
  #                      del self.bests[(new.drn, steps)]
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

    def num_new_ends(self):
        n = 0
        for k, v in self.bests.items():
            if v.new:
                n += 1
        return n


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

def num_open_locs():
    n = 0
    for k, v in plan.items():
        if not v.finished():
            n += 1
    return n

def num_open_ends():
    n = 0
    for k, v in plan.items():
        if not v.finished():
            n += v.num_new_ends()
    return n

def num_ends():
    n = 0
    for k, v in plan.items():
        if not v.finished():
            n += len(list(v.bests))
    return n



L = (-1, 0)
R = (1, 0)
U = (0, -1)
D = (0, 1)

turn_dirs = {L: (U, D), R: (U, D), U: (L, R), D: (L, R)}

width = height = 0

def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def valid_loc(l):
    return 0 <= l[0] < width and 0 <= l[1] < height

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input17.txt') as f:
    lines = f.readlines()
    width, height = len(lines[0].strip()), len(lines)
    start_steps = (-1, -1, -1, -1)
    start_scores = {(L, 0): start_steps, (R, 0): start_steps, (U, 0): start_steps, (D, 0): start_steps}
    plan = {(x, y): Location((x, y), int(lines[y][x])) for y in range(height) for x in range(width)}

#print(plan)

plan[(0, 0)].set_best(State(R, 0, 0))
plan[(0, 0)].set_best(State(D, 0, 0))

#print(plan)

q = 0
while not plan_finished():
    q += 1

    if q % 2000 == 0:
        print(num_open_locs(), num_open_ends(), num_ends())

    loc = first_open_loc()
    end = loc.first_new_end()
    #print(end)

    if end.steps < 3: # straight on is an option
        new_xy = v_add(loc.loc, end.drn)
        if 0 <= new_xy[0] < width and 0 <= new_xy[1] < height:
            next_loc = plan[new_xy]
            new_steps = end.steps + 1
            #print(end.score, next_loc.cost)
            #print(type(next_loc.cost))
            new_score = end.score + next_loc.cost
            #print(new_steps, new_score)
            next_loc.set_best(State(end.drn, new_steps, new_score))

    #turn l / r
    for new_drn in turn_dirs[end.drn]:
        new_xy = v_add(loc.loc, new_drn)
        if 0 <= new_xy[0] < width and 0 <= new_xy[1] < height:
            next_loc = plan[new_xy]
            new_steps = 1
            new_score = end.score + next_loc.cost
            next_loc.set_best(State(new_drn, new_steps, new_score))

    end.new = False

#pp()

print(plan[(width-1, height-1)].min_score())