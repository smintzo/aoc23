from functools import reduce
import re
import sys
from collections import deque

MTYPE = 'type'
MDSTS = 'dests'
FFST = 'ffst'
IINS = 'iins'

PFRM = 'from'
PSIG = 'sig'
PTO = 'to'

NONE = 'n'
FF = 'ff'
CNJ = 'cnj'

modules = {}

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input20.txt') as f:
    lines = f.readlines()

    for line in lines:
        bits = line.strip().split(' -> ')
        left = bits[0].strip()
        mod_type = ''
        mod_name = ''
        if left[0] == '%':
            mod_type = FF
            mod_name = left[1:]
        elif left[0] == '&':
            mod_type = CNJ
            mod_name = left[1:]
        else:
            mod_type = NONE
            mod_name = left
        rights = bits[1].strip().split(', ')
        modules[mod_name] = {MTYPE: mod_type, MDSTS: rights}

most_ins = 0
for mod_name, mod_data in modules.items():
    if mod_data[MTYPE] == FF:
        mod_data[FFST] = False
    elif mod_data[MTYPE] == CNJ:
        mod_data[IINS] = {}
        n_ins = 0
        for mn2, md2 in modules.items():
            if mod_name in md2[MDSTS]:
                n_ins += 1
                mod_data[IINS][mn2] = False
        most_ins = max(most_ins, n_ins)
        if mod_name == 'rx': print(mod_data)
print('most ins:', most_ins)

#print(modules)

def pp():
    s = ''
    for k, v in modules.items():

        if v[MTYPE] == FF:
            s += '1 ' if v[FFST] else '0 '
        elif v[MTYPE] == CNJ:
            for in_mod, in_state in v[IINS].items():
                s += '1' if in_state else '0'
            s += ' '
    print(s)

n_lows = 0
n_highs = 0

#cnjs_of_interest = {'sn': True, 'hl': True, 'tf': True, 'lr': True}
cnjs_of_interest = {'lr': True}
ffs_of_interest = {} # {'tv': (True, 0), 'tm': (True, 0), 'gz': (True, 0), 'gx': (True, 0)}

for i in range(1000000):
    if i % 100000 == 0: print(i)
    #pp()

    for mdle, stte in cnjs_of_interest.items():
        low_ones = {k: v for k, v in modules[mdle][IINS].items() if not v}
        has_low = (len(low_ones) > 0)
        if has_low != stte:
            print('CHANGE: at', i, mdle, stte, ' -> ', has_low)
            cnjs_of_interest[mdle] = has_low

    for mdle, stte in ffs_of_interest.items():
        s = str(i) + (' 1' if modules[mdle][FFST] else ' 0')
        changed = False
        if (modules[mdle][FFST] != stte[0]):
            changed = True
            s += ' ' + mdle + ' was: ' + str(stte[1]) + ' diff: ' + str(i - stte[1])
            ffs_of_interest[mdle] = (not stte[0], i)
            #print(ffs_of_interest)
        if changed: print(s)

    #push the button!
    pulses = deque([{PFRM: 'button', PSIG: False, PTO: ['broadcaster']}])

    while pulses:

        for mdle, stte in cnjs_of_interest.items():
            low_ones = {k: v for k, v in modules[mdle][IINS].items() if not v}
            has_low = (len(low_ones) > 0)
            if has_low != stte:
                print('CHANGE: at', i, mdle, stte, ' -> ', has_low)
                cnjs_of_interest[mdle] = has_low

        #print(pulses)
        pulse = pulses.popleft()
        #print(pulse)
        if pulse[PSIG]:
            n_highs += len(pulse[PTO])
        else:
            n_lows += len(pulse[PTO])
        for dest in pulse[PTO]:
            if dest not in modules:
                if not pulse[PSIG]:
                    print("DONE!!!", i)
                continue
            dest_mod = modules[dest]

            if dest_mod[MTYPE] == NONE:
                pulses.append({PFRM: dest, PSIG: pulse[PSIG], PTO: [t for t in dest_mod[MDSTS]]})  # pulse!

            elif dest_mod[MTYPE] == FF:
                if not pulse[PSIG]:             # i.e. low signal
                    dest_mod[FFST] = not dest_mod[FFST]     # flip, or indeed, flop!
                    pulses.append({PFRM: dest, PSIG: dest_mod[FFST], PTO: [t for t in dest_mod[MDSTS]]})      # pulse!

            elif dest_mod[MTYPE] == CNJ:
                dest_mod[IINS][pulse[PFRM]] = pulse[PSIG]
                lows = len({k: v for k, v in dest_mod[IINS].items() if not v})
                pulses.append({PFRM: dest, PSIG: (lows > 0), PTO: [t for t in dest_mod[MDSTS]]})  # pulse!

print('lows', n_lows, 'highs', n_highs)
print(n_lows * n_highs)