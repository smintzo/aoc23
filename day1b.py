from functools import reduce
import re

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input1.txt') as f:

    lines = f.readlines()

    total = 0
    num_map = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
    for i in range(1, 10):
        num_map[str(i)] = i

    #print(num_map)

    for line in lines:
        #ms = re.findall(r'\d|one|two|three|four|five|six|seven|eight|nine', line)

        matches = re.finditer(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line)
        ms = [match.group(1) for match in matches]
        #print(ms)
        
        #for test in tests:
        #    print(test.group(1))

        num = num_map[ms[0]] * 10 + num_map[ms[-1]]
        total += num
        #print(line, ms, num, total)

    print(total)
