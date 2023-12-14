from functools import reduce
import re

cards = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input4.txt') as f:

    lines = f.readlines()

    for line in lines:
        left, right = line.split('|')

        leftleft, leftright = left.split(': ')

        cardnum = int(leftleft[4:].strip())

        winners = [int(x) for x in re.findall(r'\d+', leftright)]
        guesses = [int(x) for x in re.findall(r'\d+', right)]

        cards.append((cardnum, winners, guesses))

total = 0
for card in cards:
    num_matches = 0
    for guess in card[2]:
        if guess in card[1]:
            num_matches += 1
    if num_matches > 0:
        total += pow(2, num_matches - 1)

print(total)


        
