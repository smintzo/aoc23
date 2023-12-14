from functools import reduce
import re

cards = {}

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input4.txt') as f:

    lines = f.readlines()

    for line in lines:
        left, right = line.split('|')

        leftleft, leftright = left.split(': ')

        cardnum = int(leftleft[4:].strip())

        winners = [int(x) for x in re.findall(r'\d+', leftright)]
        guesses = [int(x) for x in re.findall(r'\d+', right)]

        cards[cardnum] = (1, winners, guesses, 0)

total = 0
for card_id, card_data in cards.items():
    num_matches = 0
    for guess in card_data[2]:
        if guess in card_data[1]:
            num_matches += 1
    cards[card_id] = (cards[card_id][0], cards[card_id][1], cards[card_id][2], num_matches)
    for match in range(num_matches):
        next_id = card_id + match + 1
        if next_id <= len(cards):
            cards[next_id] = (card_data[0] + cards[next_id][0], cards[next_id][1], cards[next_id][2], cards[next_id][3])
    total += card_data[0]

for card_id, card_data in cards.items():
    print(card_id, card_data[3], card_data[0])

print('\n', total)

        
