from functools import reduce
import re

def plus(x, y): return x + y

def v_symc(plan):
    is_mirror = False
    smudged = False
    for y in range(len(plan)-1):
        smudged = False
        abandon = False
        if plan[y] != plan[y+1]:
            for x in range(len(plan[y])):
                if plan[y][x] != plan[y+1][x]:
                    if smudged:
                        smudged = False
                        abandon = True
                        break
                    else:
                        smudged = True

        if abandon:
            continue

        #print(y, plan[y], plan[y+1], smudged)
        is_mirror = True
        #smudged = False
        for i in range(min(y, len(plan)-y-2)):
            #print(i, y, len(plan), plan[y-1-i], plan[y+2+i])
            row_up = plan[y-1-i]
            row_down = plan[y + 2 + i]
            if row_up != row_down:
                for x in range(len(row_up)):
                    if row_up[x]!=row_down[x]:
                        if smudged:
                            is_mirror = False
                            break
                        else:
                            smudged = True
            if not is_mirror: break
        if is_mirror and smudged:
            break
    return y if is_mirror and smudged else -1

plans = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input13.txt') as f:

    lines = f.readlines()

    plan = []
    for line in lines:
        if line == '\n':
            if plan != []:
                plans.append(plan)
                plan = []
        else:
            plan.append(line.strip())
    plans.append(plan)

#print(plans)
total = 0
for plan in plans:
    x = -1
    y = v_symc(plan)

    planT = []
    for i in range(len(plan[0])):
        row = ''
        for j in range(len(plan)):
            row += plan[j][i]
        planT.append(row)
    #print(planT)
    x = v_symc(planT)
    print(x, y)
    total += (x + 1) if x >= 0 else (y + 1) * 100

print(total)
