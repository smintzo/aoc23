from functools import reduce
import re
import sys

rules = {}

debug=False

xmas = {'x': 0, 'm': 1, 'a': 2, 's': 3}

def range_score(r):
    score = reduce(lambda x, y: x * (y[1] - y[0] + 1), r, 1)
    return score

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input19.txt') as f:
    lines = f.readlines()

    for line in lines:
        if line.strip() == "":
            break

        name, rule_list = line.strip()[:-1].split('{')
        rules[name] = rule_list.split(',')

#print(rules)

wfs_to_do = [('in', [(1, 4000), (1, 4000), (1, 4000), (1, 4000)])]
total = 0
out_total = 0
while wfs_to_do:
    if debug: print('\n****\nNEXT\n****')
    if debug: print(len(wfs_to_do), 'to do:', wfs_to_do, '\n')

    next_wf = wfs_to_do[0]
    wfs_to_do = wfs_to_do[1:]

    rule_set = rules[next_wf[0]]
    remainder = next_wf[1]

    if debug: print('next:', next_wf, '\n')
    if debug: print('rules:', rule_set)

    for rule in rule_set:
        if debug: print('rule:', rule, '\n\tremainder:', remainder)
        if rule == 'A':
            score = reduce(lambda x, y: x * (y[1] - y[0] + 1), remainder, 1)
            if debug: print('\tscore added', score)
            total += score
        elif rule == 'R':
            score = reduce(lambda x, y: x * (y[1] - y[0] + 1), remainder, 1)
            if debug: print('\tscore excluded', score)
            out_total += score
            break
        elif ':' not in rule:
            if debug: print('\tnew todo added: ', rule, 'for range', remainder)
            wfs_to_do.append((rule, remainder))
        else: # it's a conditional rule
            cond, outcome = rule.split(':')
            range_id = xmas[cond[0]]
            cond_range = remainder[range_id]
            cond_amt = int(cond[2:])
            in_range = out_range = ()
            if cond[1] == '<':
                in_range = (cond_range[0], cond_amt - 1)
                out_range = (cond_amt, cond_range[1])
            else: # it's a > condition
                out_range = (cond_range[0], cond_amt)
                in_range = (cond_amt+1, cond_range[1])
            if debug: print('\tin', in_range, 'out', out_range)
            if outcome == 'A':
                #print(in_range, next_wf)
                score = 1
                for i in range(4):
                    if i == range_id:
                        multiple = (in_range[1] - in_range[0] + 1)
                        if debug: print('\trange', str(i), 'multiple:', str(multiple))
                        score *= multiple
                    else:
                        multiple = (remainder[i][1] - remainder[i][0] + 1)
                        if debug: print('\trange', str(i), 'multiple:', str(multiple))
                        score *= multiple
                if debug: print('\tscore added:', score)
                total += score
                old_left = range_score(remainder)
                old_rem = remainder
                remainder = remainder[:range_id] + [out_range] + remainder[range_id+1:]
                chk = score + range_score(remainder)-old_left
                #print('chk:', chk)
                if chk != 0:
                    #print('rule:', rule, '\noldrem:', old_rem, '\nremainder:', remainder, '\ncondition_range:', cond_range, '\ncond_amt:', cond_amt, '\nin_range:', in_range, '\nout_range', out_range, '\nscore:', score, '\nold_left:', old_left)
                    break
            elif outcome == 'R':
                score = 1
                for i in range(4):
                    if i == range_id:
                        multiple = (in_range[1] - in_range[0] + 1)
                        if debug: print('\trange', str(i), 'multiple:', str(multiple))
                        score *= multiple
                    else:
                        multiple = (remainder[i][1] - remainder[i][0] + 1)
                        if debug: print('\trange', str(i), 'multiple:', str(multiple))
                        score *= multiple
                if debug: print('\tscore excluded:', score)
                out_total += score

                remainder = remainder[:range_id] + [out_range] + remainder[range_id + 1:]
            else: # must be a new rule

                new_range = remainder[:range_id] + [in_range] + remainder[range_id+1:]
                if debug: print('\tNew todo added:', outcome, 'for range', new_range)
                wfs_to_do.append((outcome, new_range))
                remainder = remainder[:range_id] + [out_range] + remainder[range_id + 1:]
        if debug: print('\tnew remainder:', remainder)
print(total)
print(out_total)
print(total + out_total)
print(4000*4000*4000*4000)