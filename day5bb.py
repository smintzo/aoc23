from functools import reduce
import re

seeds = []
mappings = {}
FROM_START = 0
FROM_END = 1
TO_START = 2
TO_END = 3
SHIFT = 4
LENGTH = 5

SEED_START = 0
SEED_END = 1

def pp():
    print('seeds', seeds, '\n')
    for map_from, map_data in mappings.items():
        print(map_from, " to ", map_data[0], ":")

        for rds in map_data[1]:
            print('{0} to {1} => {2} to {3}. dx = {4}, l = {5}'.format(rds[0], rds[1], rds[2], rds[3], rds[4], rds[5]))

def map_seed_range(seed_range, map_range):

    #seed_range:              [              ]
    #case 1:       [       ]                      [        ]   :case 2
    #case 3:           [           ]    [       ]              :case 4
    #case 5:                      [    ]
    #case 6:            [                            ]

    #print('seeds', seed_range, 'map', map_range)

    out_ranges = []
    left_over = ()
    if map_range[FROM_END] < seed_range[SEED_START]:   #case 1
        left_over=seed_range

    elif map_range[FROM_START] > seed_range[SEED_END]: #case 2
        out_ranges.append(seed_range)

    elif map_range[FROM_START] <= seed_range[SEED_START] and map_range[FROM_END] >= seed_range[SEED_START] and map_range[FROM_END] < seed_range[SEED_END]: #case 3
        out_ranges.append((seed_range[SEED_START] + map_range[SHIFT], map_range[TO_END]))
        left_over=(map_range[FROM_END]+1, seed_range[SEED_END])

    elif map_range[FROM_START] > seed_range[SEED_START] and map_range[FROM_START] <= seed_range[SEED_END] and map_range[FROM_END] >= seed_range[SEED_END]: #case 4
        left_over=(seed_range[SEED_START], map_range[FROM_START]-1)
        out_ranges.append((map_range[TO_START], seed_range[SEED_END] + map_range[SHIFT]))

    elif map_range[FROM_START] > seed_range[SEED_START] and map_range[FROM_END] < seed_range[SEED_END]: #case 5
        out_ranges.append((seed_range[SEED_START], map_range[FROM_START]-1))
        out_ranges.append((map_range[TO_START], map_range[TO_END]))
        left_over=(map_range[FROM_END]+1, seed_range[SEED_END])

    elif map_range[FROM_START] <= seed_range[SEED_START] and map_range[FROM_END] >= seed_range[SEED_END]: #case 6
        out_ranges.append((seed_range[SEED_START] + map_range[SHIFT], seed_range[SEED_END] + map_range[SHIFT]))

    #print('mapped ranges:', out_ranges, 'remainder:', left_over)
    return (out_ranges, left_over)

#mappings structure:
# { from: (to, [ (from_range_start, from_range_end, to_range_start, to_range_end, shift, range_length) ] ) }

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input5.txt') as f:

    lines = f.readlines()

    current_map_from_to = ()
    current_map_ranges = []

    for line in lines:
        if line[0:6] == 'seeds:':
            seeds = [int(x.strip()) for x in line.split(':')[1].strip().split(' ')]

        elif len(line.strip())>0 and line[0] not in '0123456789':
            #new map
            #print(line)
            
            #may have finished previous mapping
            if len(current_map_from_to) > 0:
                current_map_ranges.sort()
                mappings[current_map_from_to[0]] = (current_map_from_to[1], current_map_ranges)
                current_map_ranges = []

            #capture what mapping is from / to
            hyphen_split = line.split('-')
            current_map_from_to = (hyphen_split[0], hyphen_split[2][0:-6])

        elif line[0] in '0123456789':
            #new range
            lbits = [int(x) for x in line.strip().split(' ')]
            current_map_ranges.append((lbits[1], lbits[1]+lbits[2]-1, lbits[0], lbits[0]+lbits[2]-1, lbits[0]-lbits[1], lbits[2]))

    #add last mapping
    current_map_ranges.sort()
    mappings[current_map_from_to[0]] = (current_map_from_to[1], current_map_ranges)

#print(mappings)
#pp()

seed_ranges = []
for i in range(0, len(seeds), 2):
    seed_ranges.append((seeds[i], seeds[i] + seeds[i+1] - 1))

#print(seed_ranges)

closest = -1

next_map = 'seed'
while next_map != 'location':
    this_map = mappings[next_map]
    #print("current map", this_map)

    new_seed_ranges = []
    
    for seed_range in seed_ranges:
        remainder = seed_range[:]
        for map_range in this_map[1]:
            (new_mapped_ranges, remainder) = map_seed_range(remainder, map_range)
            new_seed_ranges += new_mapped_ranges
            if remainder == (): break

        if remainder != ():
            new_seed_ranges.append(remainder)
    
    seed_ranges = new_seed_ranges
                
    next_map = this_map[0]
    
    #print("seed ranges", seed_ranges)
    
winner = -1
for seed_range in seed_ranges:
    winner = seed_range[0] if winner == -1 else min(winner, seed_range[0])

print(winner)
