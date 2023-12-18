from functools import reduce
import re
import sys


def plus(x, y): return x + y


def nl(x, y): return x + '\n' + y


def hsah(code):
    score = 0
    for ch in code:
        ascii = ord(ch)
        score += ascii
        score *= 17
        score = score % 256
    return score

with open('C:\\Users\\smint\\Dropbox\\steve\\advent_of_code\\2023\\input15.txt') as f:
    line = f.read()
    strings = line.strip().split(',')

boxes = {x : [] for x in range(256)}

for string in strings:
    fl = string[-1]
    label = string[:-1] if string[-1] == '-' else string[:-2]
    score = hsah(label)

    #print(string, score, fl, label)

    if string[-1] == '-':
        #print('delete')
        #print({k: v for k, v in boxes.items() if v != []})
        for k, box in boxes.items():
            box = [x for x in box if x[0] != label]
            boxes[k] = box
        #print({k: v for k, v in boxes.items() if v != []})
        #boxes[score] = box
    else:
        box = boxes[score]
        box = [x if x[0] != label else (label, fl) for x in box]
        if (label, fl) not in box:
            box.append((label, fl))
        boxes[score] = box

    #print({k: v for k,v in boxes.items() if v != []})

total = 0
for box_no, box in boxes.items():
    score = 0
    for lens_i in range(len(box)):
        fl = box[lens_i][1]
        lens_score = (box_no + 1) * (lens_i + 1) * int(fl)
        score += lens_score
        #print(box_no, box[lens_i][0], fl, lens_score)
    total += score
print(total)