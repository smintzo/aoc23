from functools import reduce
import re

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input1.txt') as f:

    lines = f.readlines()

    total = 0

    for line in lines:
        ms = re.findall(r'\d', line)

        #print(ms)
        total += int(ms[0]) * 10 + int(ms[-1])

    print(total)
