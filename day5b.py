from functools import reduce
import re

seeds = []
mappings = {}

def pp():
    print('seeds', seeds, '\n')
    for map_from, map_data in mappings.items():
        print(map_from, " to ", map_data[0], ":")

        for range_deets in map_data[1]:
            print(range_deets[0], '-', range_deets[1], '    shift:', range_deets[2], '    ', range_deets[3], '-', range_deets[4])

#mappings structure:
# { to: (from, [ (from_range_start, from_range_to, shift, dest_range_start, dest_range_to) ] ) }

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\test5.txt') as f:

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
            bits = [int(x.strip()) for x in line.strip().split(' ')]
            current_map_ranges.append((bits[1], bits[1]+bits[2]-1, bits[0]-bits[1], bits[0], bits[0]+bits[2]-1))

    #add last mapping
    mappings[current_map_from_to[0]] = (current_map_from_to[1], current_map_ranges)

pp()

for x in range(1000000000):
    continue

print('hi')
    
    


