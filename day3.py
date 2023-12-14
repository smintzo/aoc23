from functools import reduce
import re

s = [] #schematic
width = 0
height = 0

def neighbour_check(x, y):
    global s, width, height
    neigh = False
    for nx in range(x-1 if x>0 else x, x+2 if x<width-1 else x+1):
        for ny in range(y-1 if y>0 else y, y+2 if y<height-1 else y+1):
            if s[ny][nx] not in '.0123456789':
                neigh = True
    return neigh

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input3.txt') as f:

    lines = f.readlines()

    for line in lines:
        s.append(line.strip())

#print(s)

width = len(s[0])
height = len(s)

print(width, height)

total = 0
for y in range(height):
    num = 0
    num_found = False
    neighbour = False
    for x in range(width):
        c = s[y][x]
        if c in '0123456789':
            num_found = True
            num = num * 10 + int(c)
            neighbour = neighbour or neighbour_check(x, y)
            #print(num, x, y, neighbour)
        if c not in '0123456789' or x==width-1:
            if num_found and neighbour:
                total += num
                #print(num, total)
            num = 0
            num_found = False
            neighbour = False

print(total)
