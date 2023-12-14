from functools import reduce
import re

pipes = []
sx = 0
sy = 0
dn = 'D'

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input10.txt') as f:

    lines = f.readlines()

    i = 0
    for line in lines:
        pipes.append(line.strip())
        if 'S' in line.strip():
            sy = i
            sx = line.strip().find('S')
        i += 1

#print(pipes)
#print(sx, sy, '\n')

nx = sx
ny = sy + 1
nl = pipes[ny][nx]
length = 1
while nl != 'S':
    decision = '{0}, {1}, dir {2} via {3} -> '.format(nx, ny, dn, nl)
    #print(nx, ny)
    if length % 100 == 0: print(length)
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

print(length)
print(length/2)
