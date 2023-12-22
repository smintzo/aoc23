from functools import reduce
import re
import sys

rules = {}
items = []

xmas = {'x': 0, 'm': 1, 'a': 2, 's': 3}

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input19.txt') as f:
    lines = f.readlines()

    mode = 'Rules'
    for line in lines:
        if line.strip() == "":
            mode = 'Items'
            continue

        if mode == 'Rules':
            name, rule_list = line.strip()[:-1].split('{')
            rules[name] = rule_list.split(',')

        else:
            item_stats_strings = line.strip()[1:-1].split(',')
            item_stats = [int(x[2:]) for x in item_stats_strings]
            items.append(item_stats)

#print(rules)
#print(items)

total = 0
for item in items:
    wf = 'in'
    wf_step = 0
    done = False
    while not done:
        rule = rules[wf][wf_step]
        #print(rule)
        if rule == 'A':
            total += reduce(lambda x, y: x + y, item)
            done = True
        elif rule == 'R':
            done = True
        elif ':' not in rule:
            wf = rule
            wf_step = 0
        else: # conditional rule
            cond, outcome = rule.split(':')
            result = False
            if cond[1] == '<':
                result = item[xmas[cond[0]]] < int(cond[2:])
            else:
                result = item[xmas[cond[0]]] > int(cond[2:])
            if result:
                if outcome == 'A':
                    sum = reduce(lambda x, y: x + y, item)
                    #print(sum)
                    total += sum
                    done = True
                elif outcome == 'R':
                    done = True
                else:
                    wf = outcome
                    wf_step = 0
            else:
                wf_step += 1

print(total)