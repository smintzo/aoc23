from functools import reduce
import re

s = [] #schematic
width = 0
height = 0
gears = {}

def gear_check(x, y):
    global s, width, height
    gear = (-1, -1)
    for nx in range(x-1 if x>0 else x, x+2 if x<width-1 else x+1):
        for ny in range(y-1 if y>0 else y, y+2 if y<height-1 else y+1):
            if s[ny][nx] == '*':
                gear = (nx, ny)
    return gear

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
    n_gears = set()
    for x in range(width):
        c = s[y][x]
        if c in '0123456789':
            num_found = True
            num = num * 10 + int(c)
            gear = gear_check(x, y)
            if gear != (-1, -1):
                n_gears.add(gear)
            #print(num, x, y, neighbour)
        if c not in '0123456789' or x==width-1:
            for gear_x in n_gears:
                if gear_x not in gears:
                    gears[gear_x] = [num]
                else:
                    gears[gear_x].append(num)
            n_gears = set()
            num_found = False
            num = 0

for gear, nums in gears.items():
    if len(nums) == 2:
        total += nums[0]*nums[1]
    elif len(nums)>2:
        print(gear, nums)

print(total)
