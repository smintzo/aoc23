from functools import reduce
import re

seeds = []
mappings = {}

def pp():
    print('seeds', seeds, '\n')
    for map_from, map_data in mappings.items():
        print(map_from, " to ", map_data[0], ":")

        for range_deets in map_data[1]:
            print(range_deets[0], range_deets[1], range_deets[2])

#mappings structure:
# { from: (to, [ (to_range_start, from_range_start, range_length) ] ) }

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
                mappings[current_map_from_to[0]] = (current_map_from_to[1], current_map_ranges)
                current_map_ranges = []

            #capture what mapping is from / to
            hyphen_split = line.split('-')
            current_map_from_to = (hyphen_split[0], hyphen_split[2][0:-6])

        elif line[0] in '0123456789':
            #new range
            current_map_ranges.append(tuple([int(x) for x in line.strip().split(' ')]))

    #add last mapping
    mappings[current_map_from_to[0]] = (current_map_from_to[1], current_map_ranges)
        
#pp()

closest = -1

for i in range(0,len(seeds),2):
    print(i)
    for j in range(seeds[i],seeds[i]+seeds[i+1]):   
        this_map = 'seed'
        current_id = j
        while this_map != 'location':
            mapping = mappings[this_map]
            this_map = mapping[0]

            new_id = -1
            for range_deets in mapping[1]:
                
                if current_id >= range_deets[1] and current_id < range_deets[1] + range_deets[2]:
                    new_id = range_deets[0] + current_id - range_deets[1]
                #print(current_id, range_deets, new_id)

            if new_id < 0: new_id = current_id
            current_id = new_id

        closest = current_id if closest < 0 else min(current_id, closest)
        
print(closest)
