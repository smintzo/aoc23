from functools import reduce
import re

times = []
records = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input6b.txt') as f:

    times = [int(x) for x in re.findall(r'\d+', f.readline())]
    records = [int(x) for x in re.findall(r'\d+', f.readline())]
    time = times[0]
    record = records[0]

#print(times, records)

low = 0
high = 0

t = 1
win_found = False
while not win_found:
    d = (time - t) * t
    if d >= record:
        print(t, record, d)
        win_found = True
        low = t
    t += 1

t = time - 1

win_found = False
while not win_found:
    d = (time - t) * t
    if d >= record:
        print(t, record, d)
        win_found = True
        high = t
    t -= 1

print(low, high, high-low+1)

