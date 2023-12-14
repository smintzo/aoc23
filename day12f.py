from functools import reduce
import re

def plus(x, y): return x + y
def comma(x, y): return x + ', ' + y

records = []

cache = {}

def get_matches(string, pattern, level=1):
    ckey = tuple(string) + tuple(pattern)
    if ckey in cache:
        return cache[ckey]
    
    call = str(level) + ' ' * level + string + ' ' + reduce(comma, [str(x) for x in pattern])
    #print(call)
    count = 0
    if len(pattern) == 1:
        single_RE = r'(?=((?<!#)' + r'[\?|#]' * pattern[0] + r'[\?|\.]*$))'
        #print(single_RE)
        for match in re.finditer(single_RE, string):
            if '#' not in string[:match.start()]:
                count += 1
    else:
        #find slots for left-most pattern
        #first, find right-most possible slots for the rest of the pattern
        backstring = string[::-1]

        #fill up with the remaining pattern sections
        for i in range(len(pattern)-1, 0, -1):
            pattern_to_eat = r'(?<!#)' + '[\?|#]' * pattern[i] + '[\?|\.]+'
            #print(pattern_to_eat, backstring)
            first_slot = re.search(pattern_to_eat, backstring).start()
            #print(pattern_to_eat, backstring, first_slot)
            backstring = backstring[first_slot + pattern[i] + 1:]
            #print(backstring)

        leftover = backstring[::-1]
        #print(leftover)

        #where can we slot the left-most section now?
        first_RE = r'(?=((?<!#)' + r'[\?|#]' * pattern[0] + r'(?!#)))'
        #print(first_RE)
        for match in re.finditer(first_RE, leftover):
            #print(match.group(1), match.start())

            if '#' not in leftover[:match.start()]:
                count += get_matches(string[match.start() + pattern[0] + 1:], pattern[1:], level + 1)

    #print(call, '->', count)
    cache[ckey] = count
    return count

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input12.txt') as f:

    lines = f.readlines()

    for line in lines:
        bits = line.strip().split(' ')
        #records.append((bits[0], [int(x) for x in bits[1].split(',')]))
        records.append(((bits[0]+'?')*4+bits[0], [int(x) for x in bits[1].split(',')*5]))

#print(records)

total = 0

for record in records:
    matches = get_matches(record[0], record[1])
    total += matches
#    print('matches:', record[0], record[1], len(matches))
    print(record[0], record[1], matches)
#    for match in matches:
#        print(match)

print(total)
