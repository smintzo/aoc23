from functools import reduce
import re

instructions = ''
LRs = {}
locations = []

def done(locations):
    non_end_found = False
    for location in locations:
        if location[2] != 'Z':
            non_end_found = True
    return (not non_end_found)

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input8.txt') as f:

    lines = f.readlines()

    instructions = lines[0]

    print(instructions)
    
    for i in range(2, len(lines)):
        l = lines[i]
        LRs[l[:3]] = (l[7:10], l[12:15])
        if l[2] == 'A': locations.append(l[:3])

print(locations)
i = 0
num_steps = 0



while not done(locations):

    for n in range(len(locations)):
        location = locations[n]
        if location[2] == 'Z':
            print(n, num_steps, i, location)

    next_locations = []
    for location in locations:
        next_locations.append(LRs[location][(0 if instructions[i] == 'L' else 1)])
    locations = next_locations
    i += 1
    if i >= len(instructions)-1: i=0
    num_steps += 1

print(num_steps)


