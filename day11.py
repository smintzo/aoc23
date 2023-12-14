from functools import reduce
import re

galaxy = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input11.txt') as f:

    lines = f.readlines()

    for line in lines:
        
        if '#' not in line:
            galaxy.append('M' * len(line.strip()))
        else:
            galaxy.append(line.strip())

col = 0
while col < len(galaxy[0]):
    blank = True
    for row in range(len(galaxy)):
        if galaxy[row][col] == '#':
            blank = False
            break
    if blank:
        for row in range(len(galaxy)):
            galaxy[row] = galaxy[row][0:col] + 'M' + galaxy[row][col+1:]
        col += 1
    col += 1

#print(galaxy)

stars = []
for y in range(len(galaxy)):
    for x in range(len(galaxy[0])):
        if galaxy[y][x] == '#':
            stars.append((x, y))

#print(stars)
total_distance = 0
for f in range(len(stars)-1):
    for t in range(f + 1, len(stars)):
        #print(f, t)

        distance = 0

        fs = ts = ()
        
        if stars[f][0] <= stars[t][0]:
            fs = stars[f]
            ts = stars[t]
        else:
            fs = stars[t]
            ts = stars[f]

        for x in range(fs[0]+1,ts[0]+1):
            distance += 1000000 if galaxy[fs[1]][x] == 'M' else 1

        if stars[f][1] <= stars[t][1]:
            fs = stars[f]
            ts = stars[t]
        else:
            fs = stars[t]
            ts = stars[f]

        for y in range(fs[1]+1,ts[1]+1):
            distance += 1000000 if galaxy[y][ts[0]] == 'M' else 1
        
        total_distance += distance

        #print(f, t, distance)

print(total_distance)        
