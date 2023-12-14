from functools import reduce
import re

def plus(x, y): return x + y

platform = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input14.txt') as f:

    lines = f.readlines()

    for line in lines:
        platform.append(line.strip())

width = len(platform[0])
height = len(platform)

total = 0
for x in range(width):
    col = reduce(lambda a, b: a + b, [platform[y][x] for y in range(height)])
    #print(col)

    i = 1
    while i < height:
        j = i
        stopped = False
        while j > 0 and not stopped:
            if col[j-1:j+1] == '.O':
                col = col[:j-1] + 'O.' + col[j+1:]
            else:
                stopped = True
            j -= 1
        i += 1

    score = reduce(plus, [height - i for i in range(height) if col[i] == 'O'], 0)
    total += score
    
    #print(col, score)

print(total)

