from functools import reduce
import re

records = []

def get_possibles(p_so_far, string, num_hashes):
    #print(p_so_far, string, num_hashes)
    if '?' not in string and len(re.findall('#', string)) == num_hashes:
        p_so_far.append(string)
    elif '?' in string:
        new_hash = string.replace('?', '#', 1)
        new_dot = string.replace('?', '.', 1)
        if len(re.findall('#', new_hash)) <= num_hashes:
            get_possibles(p_so_far, new_hash, num_hashes)
        get_possibles(p_so_far, new_dot, num_hashes)
    return p_so_far
                                 

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input12.txt') as f:

    lines = f.readlines()

    for line in lines:
        bits = line.strip().split(' ')
        records.append((bits[0], bits[1].split(',')))

#print(records)

total = 0

for record in records:
    num_hashes = reduce(lambda x, y: int(x) + int(y), record[1])
    possibles = get_possibles([], record[0], num_hashes)

    pattern = ['#'*int(x) for x in record[1]]
    #print(pattern)
    matches = [x for x in possibles if re.findall('#+', x) == pattern]
    total += len(matches)
    print(len(matches), total)
