from functools import reduce
import re
import sys


def plus(x, y): return x + y


def nl(x, y): return x + '\n' + y


with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input15.txt') as f:
    line = f.read()
    strings = line.strip().split(',')

total = 0
for string in strings:
    score = 0
    for ch in string:
        ascii = ord(ch)
        score += ascii
        score *= 17
        score = score % 256
    #print(string, score)
    total += score
print(total)
