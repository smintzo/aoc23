from functools import reduce
import re

records = []

def pattern_compat(strings, pattern, level = 0):
    #print('PC:', strings, pattern, level)
    output = False
    if pattern == []:
        output = (strings == [])
    elif strings == []:
        output = True
    elif len(strings[0]) > len(pattern[0]):
        output = pattern_compat(strings, pattern[1:], level+1)
    elif len(strings[0]) == len(pattern[0]):
        output = pattern_compat(strings[1:], pattern[1:], level+1)
    elif len(pattern[0])>len(strings[0])+1:
        output = pattern_compat(strings[1:], [pattern[0][len(strings[0])+1:]] + pattern[1:], level+1)
    else:
        output = pattern_compat(strings[1:], pattern[1:], level+1)
        
    #print('\t'*level, 'PC', level, strings, pattern, output)
    return output
    
def get_possibles(p_so_far, string, num_hashes, pattern):
    #print("GP", p_so_far, string, num_hashes, pattern)

    if len(re.findall('#|\?', string)) < num_hashes:
        return p_so_far
    
    if '?' not in string and len(re.findall('#', string)) == num_hashes:
        p_so_far.append(string)

    elif '?' in string:
        
        new_hash = string.replace('?', '#', 1)
        hash_compat = pattern_compat(re.findall('#+', new_hash), pattern)
        #print('\tGPh', string, new_hash, pattern, hash_compat)
        if hash_compat:
            get_possibles(p_so_far, new_hash, num_hashes, pattern)

        if len(re.findall('#|\?', string)) > num_hashes:
            new_dot = string.replace('?', '.', 1)
            dot_compat = pattern_compat(re.findall('#+', new_dot), pattern)
            #print('\tGPd', string, new_dot, pattern, dot_compat)
            if dot_compat:
                get_possibles(p_so_far, new_dot, num_hashes, pattern)

    return p_so_far
                                 

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\test12.txt') as f:

    lines = f.readlines()

    for line in lines:
        bits = line.strip().split(' ')
        #records.append((bits[0], bits[1].split(',')))
        records.append(((bits[0]+'?')*4+bits[0], bits[1].split(',')*5))

print(records)

total = 0

for record in records:
    num_hashes = reduce(lambda x, y: int(x) + int(y), record[1])
    pattern = ['#'*int(x) for x in record[1]]
    possibles = get_possibles([], record[0], num_hashes, pattern)

    #print('pat_mat', pattern, possibles)
    
    #print(pattern)
    matches = [x for x in possibles if re.findall('#+', x) == pattern]
    total += len(matches)
    print(len(matches), total)
