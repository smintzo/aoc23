from functools import reduce
import re

loops = [(0, 19631, 39262), (1, 13771, 27542), (2, 21389, 42778), (3, 17287, 34574), (4, 23147, 46294), (5, 20803, 41606)]

ls = []
for l in loops:
    ls.append((l[0], l[1], l[2]-l[1], l[2]))

print(ls)

