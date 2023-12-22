from functools import reduce
import re
import sys

def vadd(a, b):
    return (a[0] + b[0], a[1] + b[1])


blocks = []
ID = 'id'
UL = 'low'
UH = 'high'
DL = 'dlow'
DH = 'dhigh'
DOWN = 'DOWN'
PL = 'pl'
DTO = 'dto'
SUPS = 'sups'
SUP = 'sup'
SBY = 'sby'
H = 'h'

maxx = 0
maxy = 0

def block_by_id(i):
    return [b for b in blocks if b[ID] == i][0]

maxminz = 0
with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input22.txt') as f:
    lines = f.readlines()
    i = 0
    for line in lines:
        bits = line.strip().split('~')
        end1 = [int(x.strip()) for x in bits[0].split(',')]
        end2 = [int(x.strip()) for x in bits[1].split(',')]
        lend = (min(end1[0], end2[0]), min(end1[1], end2[1]), min(end1[2], end2[2]))
        hend = (max(end1[0], end2[0]), max(end1[1], end2[1]), max(end1[2], end2[2]))
        maxminz = max(maxminz, lend[2])
        maxx = max(maxx, hend[0])
        maxy = max(maxy, hend[1])
        blocks.append({ID: i, UL: lend, UH: hend, DOWN: False, SBY: set(), SUPS: set(), PL: True})
        i += 1

#print(blocks, '\n')

print(maxx, maxy, '\n')

blocks.sort(key = lambda b: b[UL][2])

max_heights = {(x, y): {H: 0} for x in range(maxx + 1) for y in range(maxy + 1)}

def pmh():
    for y in range(maxy + 1):
        s1 = ''
        s2 = ''
        for x in range(maxx + 1):
            s1 += ('{:<5}').format(max_heights[(x, y)][H])
            s2 += ('{:<5}').format(max_heights[(x, y)][SUP])
        print(s1)
        print(s2)
        print('')
    print('')

def pb():
    max_h = reduce(lambda x, b: max(x, b[H]), max_heights.values(), 0)
    for z in range(2, -1, -1):
        blocks_at_z = [b for b in blocks if b[DL][2] <= z <= b[DH][2]]
        for y in range(maxx + 1):
            blocks_at_yz = [b for b in blocks_at_z if b[DL][1] <= y <= b[DH][1]]
            s = ''
            for x in range(maxy + 1):
                block_at_xyz = [b for b in blocks_at_yz if b[DL][0] <= x <= b[DH][0]]
                if block_at_xyz == []:
                    s += '[-..-] '
                else:
                    the_block = block_at_xyz[0]
                    s += '  ' if the_block[PL] else '* '
                    s += '{:<5}'.format(the_block[ID])
            print(s)
        print('')

flying_blocks = [b for b in blocks if not b[DOWN]]
while flying_blocks:

#    pmh()

    block = flying_blocks[0]
    z = block[UL][2]
    drop = -1
    while not block[DOWN]:
        z -= 1
        drop += 1
        if z == 0:
            block[DOWN] = True
            break
        for x in range(block[UL][0], block[UH][0]+1):
            for y in range(block[UL][1], block[UH][1]+1):
                if max_heights[(x, y)][H] == z:
                    block[SBY].add(max_heights[(x, y)][SUP])
                    block[DOWN] = True
                    blocks[max_heights[(x, y)][SUP]][SUPS].add(block[ID])

    for x in range(block[UL][0], block[UH][0] + 1):
        for y in range(block[UL][1], block[UH][1] + 1):
            max_heights[(x, y)] = {H: block[UH][2] - drop, SUP: block[ID]}
    block[DL] = (block[UL][0], block[UL][1], z + 1)
    block[DH] = (block[UH][0], block[UH][1], block[UH][2] - drop)
    del flying_blocks[0]

pmh()

#print(blocks, '\n')

necessary_count = 0
for block in blocks:
    if block[ID] == 546:
        print(block)
    necessary = False
    for supported_id in block[SUPS]:
        supported_block = block_by_id(supported_id)
        if len(supported_block[SBY]) == 1:
            necessary = True
            break
    if block[ID] == 546:
        print(supported_block)
    if necessary:
        necessary_count += 1
        block[PL] = False

print('of', str(len(blocks)), 'blocks,', necessary_count, 'are necessary and',
      len(blocks) - necessary_count, 'can be killed.')

print(len([b for b in blocks if b[PL]]))

pb()

#print(blocks)