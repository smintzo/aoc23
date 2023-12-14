from functools import reduce
import re

sequences = []

with open('c:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input9.txt') as f:

    lines = f.readlines()

    for line in lines:
        sequences.append([int(x.strip()) for x in line.strip().split(' ')])

total = 0
for sequence in sequences:
    diff_tree = [sequence]

    bottom = diff_tree[-1]
    while not bottom == [0] * len(bottom):

        new_bottom = []
        for i in range(len(bottom) - 1):
            new_bottom.append(bottom[i+1] - bottom[i])

        diff_tree.append(new_bottom)
        bottom = new_bottom

    diff_tree[-1].append(0)

    #print(diff_tree)
    #print('\n')

    for i in range(len(diff_tree)-1, 0, -1):
        diff_tree[i-1].append(diff_tree[i-1][-1] + diff_tree[i][-1])

    #print(diff_tree)

    total += diff_tree[0][-1]

print(total)
