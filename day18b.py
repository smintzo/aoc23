from functools import reduce
import re
import sys

instructions = []

START = 0
DRN = 1
LNG = 2
END = 3

channels=[] # start, drn, lngth, end

def channelsAtRow(y):
    ans=[]
    for channel in channels:
        channel_at_row = (channel[START][1] == y) if channel[DRN] == 'H' else channel[START][1] <= y and channel[END][1] >= y
        if channel_at_row:
            ans.append(channel)
    ans.sort(key = lambda x: (min(x[START][0], x[END][0]) * 10 + (5 if x[START][0] == x[END][0] else 0)))
    return ans

minx = maxx = miny = maxy = 0

dirs = {'R': (1, 0), 'L': (-1, 0), 'U': (0, -1), 'D': (0, 1)}

def vadd(a, b):
    return (a[0]+b[0], a[1]+b[1])
def vscale(v, s):
    return (v[0] * s, v[1] * s)

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input18.txt') as f:
    lines = f.readlines()

    hdirs = ['R', 'D', 'L', 'U']

    start = (0, 0)
    for line in lines:
        bits = line.strip().split(' ')
        hx = '0x' + bits[2][2:7]
        lng = int(hx, 16)
        #lng = int(bits[1].strip())
        idir = int(bits[2][7])
        drn = hdirs[idir]
        #drn = bits[0].strip()
        instructions.append((drn, lng))
        end = vadd(start, vscale(dirs[drn], lng))
        if drn == 'R': channels.append((start, 'H', lng, end))
        elif drn == 'D': channels.append((start, 'V', lng, end))
        elif drn == 'L': channels.append((end, 'H', lng, start))
        else: channels.append((end, 'V', lng, start))
        minx = min(minx, start[0], end[0])
        maxx = max(maxx, start[0], end[0])
        miny = min(miny, start[1], end[1])
        maxy = max(maxy, start[1], end[1])
        start = end

#print(instructions)
#for channel in channels: print(channel[START], channel[END], channel[DRN], channel[LNG])
print('{0}, {1} - {2}, {3}'.format(minx, miny, maxx, maxy))

total = 0
old_rs = 0
for y in range(miny, maxy+1):
    row_sum = 0
    cars = channelsAtRow(y)
    #print(cars)
    inside = False
    inside_start = 0
    i = 0
    while i < len(cars):
        car1 = cars[i]
        if car1[DRN] == 'V': # vertical only so crossing inside <> outside
            if not inside:
                inside_start = car1[START][0]
                inside = True
            else: # going inside -> outside
                row_sum += car1[START][0] - inside_start + 1
                inside = False
            i += 1
        else: # horizontal channel
            car2 = cars[i+1]
            car3 = cars[i+2]
            #print(cars)
            #print(car1, '\n', car2, '\n', car3, '\n', inside_start)
            if car2[END][1] == car3[START][1] or car2[START][1] == car3[END][1]:
                if not inside:
                    row_sum += car1[LNG]
                    inside_start = car1[END][0]
                    inside = True
                else:
                    row_sum += car1[END][0] - inside_start + 1
                    inside = False
            else:
                if not inside:
                    row_sum += car1[LNG] + 1

            i += 3

    if old_rs != row_sum:
        print(y, row_sum)
    old_rs = row_sum
    total += row_sum
print(total)





