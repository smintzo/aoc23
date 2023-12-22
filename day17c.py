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
    for y in range(height):
        s = ''
        for x in range(width):
            node = plan[(x, y)]
            best = reduce(min, node['bests'].values())
            s += '{:<4}'.format(str(best))
        print(s)


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

opposite_dirs = {L: R, R: L, U: D, D: U}

width = height = 0

def v_add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def valid_loc(l):
    return 0 <= l[0] < width and 0 <= l[1] < height

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input17.txt') as f:
    lines = f.readlines()
    width, height = len(lines[0].strip()), len(lines)
    plan = {(x, y): {'cost': int(lines[y][x]), 'bests': {}} for y in range(height) for x in range(width)}

plan[(width-1, height-1)]['bests']={(R, 0): 0, (D, 0): 0}

#print(plan)

changed_locs = {(width-1, height-1)}

while changed_locs:
    new_changed_locs = set()
    for changed_loc in list(changed_locs):
        changed = plan[changed_loc]
        for drn in drns:
            neighbour_loc = v_add(changed_loc, opposite_dirs[drn])
            if neighbour_loc not in plan:               # might be off the edge ...
                continue
            neighbour = plan[neighbour_loc]
            for best_key, best_score in plan[changed_loc]['bests'].items():
                if best_key[0] == opposite_dirs[drn]: continue
                if best_key[0] == drn:
                    steps = best_key[1] + 1
                    if steps <= 10:
                        #print(changed['cost'])
                        #print(best_score + changed['cost'])
                        if (drn, steps) not in neighbour['bests'] or neighbour['bests'][(drn, steps)] > best_score + changed['cost']:
                            neighbour['bests'][(drn, steps)] = best_score + changed['cost']
                            new_changed_locs.add(neighbour_loc)
                else:
                    steps = best_key[1]
                    if steps >= 4:
                        if (drn, 1) not in neighbour['bests'] or neighbour['bests'][(drn, 1)] > best_score +changed['cost']:
                            neighbour['bests'][(drn, 1)] = best_score + changed['cost']
                            new_changed_locs.add(neighbour_loc)

    changed_locs = new_changed_locs

#print(plan[(0, 0)])

best = -1
for k, v in plan[(0, 0)]['bests'].items():
    if k[1] >= 4:
        if best < 0:
            best = v
        else:
            best = min(best, v)
print(best)

#print(plan)

#pp()