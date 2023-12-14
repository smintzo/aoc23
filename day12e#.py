from functools import reduce
import re

def plus(x, y): return x + y

records = []

def get_matches(string, pattern, level=0):

    #print(' ' * level, string, pattern)

    matches = []

    if len(pattern)==0:
        if '#' not in string:
            matches.append(string.replace('?', '.'))

    elif len(pattern)==1:
        only_RE = r'(?=(' + '[\?|#]' * pattern[0] + '))'
        #print('len = 1', only_RE, string)
        
        matches = []
        for match in re.finditer(only_RE, string):
            match_pos = match.span()[0]
            if '#' not in string[:match_pos] and '#' not in string[match_pos + pattern[0]:]:
                matches.append('.' * len(string[:match_pos]) + '#' * pattern[0] + '.' * len(string[match_pos + pattern[0]:]))

    elif len(pattern)==2:
        left_RE = '(?=(' + '[\?|#]' * pattern[0] + '[\?|\.].' + '.' * (pattern[1]-1) + '))'
        #print('len = 2', left_RE, string)
        matches = []
        for match in re.finditer(left_RE, string):
            match_pos = match.span()[0]
            if '#' not in string[:match_pos]:
                for rmatch in get_matches(string[match_pos+pattern[0]+1:], [pattern[-1]], level + 1):
                    #print('.' * match_pos + '#' * pattern[0] + '.', rmatch)
                    matches.append('.' * match_pos + '#' * pattern[0] + '.' + rmatch)
            
    else:
        #find the longest bit of the pattern
        max_l = max(pattern)
        middle_pattern_i = pattern.index(max_l)
        #print(max_l, middle_pattern_i)
        middle_pattern = pattern[middle_pattern_i]
        min_left_length = reduce(plus, pattern[:middle_pattern_i], 0) + middle_pattern_i
        min_right_length = reduce(plus, pattern[middle_pattern_i+1:], 0) + len(pattern) - middle_pattern_i - 1
        #print('mid_i: {0}, mid_l: {1}, l_min_l: {2}, r_min_l: {3}'.format(middle_pattern_i, middle_pattern, min_left_length, min_right_length))
        
        #determine possible matching substrings for the middle pattern
        if middle_pattern_i == 0: #we're looking at the left-most bit of the pattern
            middle_RE = '(?=(' + '[\?|#]' * middle_pattern + '[\?|\.]' + '.' * (min_right_length-1) + '))'
            #print('left', middle_RE)

            matches = []
            for match in re.finditer(middle_RE, string):
                #print(match.span()[0], match.group(1))
                    
                match_pos = match.span()[0]

                if '#' not in string[:match_pos]:
                    for rmatch in get_matches(string[match_pos+pattern[0]+1:], pattern[1:], level + 1):
                        #print('.' * match_pos + '#' * pattern[0] + '.', rmatch)
                        matches.append('.' * match_pos + '#' * pattern[0] + '.' + rmatch)
                        
        elif middle_pattern_i == len(pattern) - 1: #right-most part of the pattern
            middle_RE = '(?=(' + '.' * (min_left_length-1) + '[\?|\.]' + '[\?|#]' * middle_pattern + '))'
            #print('right', middle_RE)

            matches = []
            for match in re.finditer(middle_RE, string):
                #print(match.span()[0], match.group(1))
                    
                match_pos = match.span()[0] + min_left_length

                if '#' not in string[match_pos + middle_pattern:]:
                    for lmatch in get_matches(string[:match_pos], pattern[:-1], level + 1):
                        #print('.' * match_pos + '#' * pattern[0] + '.', rmatch)
                        matches.append(lmatch + '.' + '#' * pattern[0] + '.' * (len(string)-match_pos-middle_pattern))
        else:
            middle_RE = '(?=(' + '.' * (min_left_length - 1) + '[\?|\.]' + '[\?|#]' * middle_pattern + '[\?|\.]' + '.' * (min_right_length - 1) + '))'
            #print(middle_RE)

            matches = []
            for match in re.finditer(middle_RE, string):
                #print(match.span()[0], match.group(1))
                    
                match_pos = match.span()[0] + min_left_length

                #print(string[:match_pos-1], '.' + '#' * middle_pattern + '.', string[match_pos + middle_pattern + 1:])

                if (max(pattern[:middle_pattern_i]) > max(pattern[middle_pattern_i + 1:])):
                    lmatches = get_matches(string[:match_pos - 1], pattern[:middle_pattern_i], level + 1)
                    for lmatch in lmatches:
                        rmatches = get_matches(string[match_pos + middle_pattern + 1:], pattern[middle_pattern_i + 1:], level + 1)
                        for rmatch in rmatches:
                            matches.append(lmatch + '.' + '#' * middle_pattern + '.' + rmatch)

                else:
                    rmatches = get_matches(string[match_pos + middle_pattern + 1:], pattern[middle_pattern_i + 1:], level + 1)
                    for rmatch in rmatches:
                        lmatches = get_matches(string[:match_pos - 1], pattern[:middle_pattern_i], level + 1)
                        for lmatch in lmatches:
                            matches.append(lmatch + '.' + '#' * middle_pattern + '.' + rmatch)                    

    #print(string, pattern, matches)
    return matches

        #establish patterns and strings for the left and right parts or each middle match

        #recurse!

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
    total += len(matches)
#    print('matches:', record[0], record[1], len(matches))
    print(record[0], len(matches))
#    for match in matches:
#        print(match)

print(total)
