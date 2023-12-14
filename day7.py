from functools import reduce
import re

hands = []
CARDS = 0
BID = 1

card_scores = {'A': 13, 'K': 12, 'Q': 11, 'J': 1, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}

def j_switch(s):
    ans = []
    if len(s) == 1:
        if s == 'J':
            ans = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
        else:
            ans = [s]
    else:
        for x in j_switch(s[:-1]):
            for y in j_switch(s[-1]):
                ans.append(x + y)
    return ans

def hand_key(h):
    type_rank = 0

    phs = j_switch(h)

    #print(j_switch('QJJKA'))
            
    best_rank = 0

    for ph in phs:
    
        sh = ''.join(sorted(ph, key=(lambda x: card_scores[x])))
        if re.search(r'(.)\1\1\1\1', sh) is not None:
            best_rank = max(best_rank, 7)
        elif re.search(r'(.)\1\1\1', sh) is not None:
            best_rank = max(best_rank, 6)
        elif re.search(r'(.)\1\1(.)\2', sh) is not None or re.search(r'(.)\1(.)\2\2', sh) is not None:
            best_rank = max(best_rank, 5)
        elif re.search(r'(.)\1\1', sh) is not None:
            best_rank = max(best_rank, 4)
        elif re.search(r'(.)\1.?(.)\2', sh) is not None:
            best_rank = max(best_rank, 3)
        elif re.search(r'(.)\1', sh) is not None:
            best_rank = max(best_rank, 2)
        else:
            best_rank = max(best_rank, 1)

        #print(h, ph, sh, best_rank)
    
    #print(sh, best_rank)

    key = 0
    for i in range(5):
        key += pow(13, 4-i) * card_scores[h[i]]

    key += pow(13, 5) * best_rank

    return key
    

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input7.txt') as f:

    lines = f.readlines()
    for line in lines:
        hand_data = line.split(' ')
        hands.append((hand_data[0], int(hand_data[1].strip())))

print(hands)

hand_ranks = []
for hand in hands:
    hand_ranks.append((hand[CARDS], hand[BID], hand_key(hand[CARDS])))
    
hand_ranks.sort(key=(lambda x: x[2]))

total = 0
for i in range(len(hand_ranks)):
    total += hand_ranks[i][BID] * (i + 1)

print(total)
