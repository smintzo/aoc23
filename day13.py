from functools import reduce
import re

def plus(x, y): return x + y

def v_symc(plan):
    is_mirror = False
    for y in range(len(plan)-1):
        if plan[y] == plan[y+1]:
            #print(y, plan[y], plan[y+1])
            is_mirror = True
            for i in range(min(y, len(plan)-y-2)):
                #print(i, y, len(plan), plan[y-1-i], plan[y+2+i])
                is_mirror = is_mirror and plan[y-1-i] == plan[y + 2 + i]
            if is_mirror:
                break
    return y if is_mirror else -1

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
    if y == -1:
        planT = []
        for i in range(len(plan[0])):
            row = ''
            for j in range(len(plan)):
                row += plan[j][i]
            planT.append(row)
        #print(planT)
        x = v_symc(planT)
    #print(x, y)
    total += (x + 1) if x >= 0 else (y + 1) * 100

print(total)
