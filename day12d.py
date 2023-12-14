from functools import reduce
import re

def plus(x, y): return x + y

records = []

matches = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\test12.txt') as f:

    lines = f.readlines()

    for line in lines:
        bits = line.strip().split(' ')
        records.append((bits[0], [int(x) for x in bits[1].split(',')]))
        #records.append(((bits[0]+'?')*4+bits[0], bits[1].split(',')*5))

print(records)

total = 0

for record in records:
    counts = record[1]

    match_re = r'(?=(^[\?|\.]*' + r'[#|\?]' * counts[0]

    for count in counts[1:-1]:
        match_re += r'[\?|\.]+' + r'[\?|#]' * count

    match_re += r'[\?|\.]+' + r'[\?|#]' * counts[-1] + r'[\?|\.]*$))'

    print(match_re)
    print([x.group(1) for x in re.finditer(match_re, record[0])])
