from functools import reduce
import re

pipes = []
sx = 0
sy = 0
dn = 'D'

width = 0
height = 0

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input10.txt') as f:

    lines = f.readlines()

    height = len(lines)

    i = 0
    for line in lines:
        pipes.append(line.strip())
        if 'S' in line.strip():
            sy = i
            sx = line.strip().find('S')
            width = len(line.strip())
        i += 1

#print(pipes)
#print(sx, sy, '\n')
print('grid is {0} x {1}'.format(width, height))

loop = [(sx, sy)]

nx = sx
ny = sy + 1
nl = pipes[ny][nx]
length = 1
while nl != 'S':
    loop.append((nx, ny))
    decision = '{0}, {1}, dir {2} via {3} -> '.format(nx, ny, dn, nl)
    #print(nx, ny)
    #if length % 100 == 0: print(length)
    if nl == '|':
        ny += (1 if dn == 'D' else -1)
    elif nl == '-':
        nx += (1 if dn == 'R' else -1)
    elif nl == 'L':
        if dn == 'D':
            dn = 'R'
            nx += 1
        else: #dn = L
            dn = 'U'
            ny -= 1
    elif nl == 'J':
        if dn == 'D':
            dn = 'L'
            nx -= 1
        else: #dn = R
            dn = 'U'
            ny -= 1
    elif nl == '7':
        if dn == 'R':
            dn = 'D'
            ny += 1
        else: #dn=U
            dn = 'L'
            nx -= 1
    elif nl == 'F':
        if dn == 'U':
            dn = 'R'
            nx += 1
        else: #dn = L
            dn = 'D'
            ny += 1

    #print(decision + '{0}, {1}, dir: {2}'.format(nx, ny, dn))
    
    length += 1
    nl = pipes[ny][nx]

#print(loop)

internals = 0

for x in range(width):
    print(x)
    for y in range(height):
        if (x, y) not in loop:
            crossings = 0
            dirn = ''
            for px in range(x+1, width):                
                if (px, y) in loop:
                    letter = pipes[y][px]
                    if letter == 'S': letter = '7'
                    if letter == '|': crossings += 1
                    elif letter == 'L': dirn = 'D'
                    elif letter == 'F': dirn = 'U'
                    elif letter == 'J':
                        if dirn == 'U': crossings += 1
                        dirn = ''
                    elif letter == '7':
                        if dirn == 'D': crossings += 1
                        dirn = ''
                        
            if crossings % 2 == 1: internals += 1

print(internals)
