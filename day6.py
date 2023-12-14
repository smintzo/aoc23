from functools import reduce
import re

times = []
records = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input6b.txt') as f:

    times = [int(x) for x in re.findall(r'\d+', f.readline())]
    records = [int(x) for x in re.findall(r'\d+', f.readline())]

#print(times, records)

scores = []

for i in range(len(times)):
    score = 0
    time = times[i]
    for t in range(1,time):
        d = (time - t) * t
        if d > records[i]:
            score += 1
    scores.append(score)
    score = 0

print(reduce(lambda x, y: x * y, scores))
