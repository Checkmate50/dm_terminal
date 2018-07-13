"""
Generates a potion with a quantity and quality of ingredients based on the given level
Written by Dietrich Geisler
"""
from potion import *
import sys
import random


# level > 3
def gen_rarity(level):
    unchecked = []
    to_return = []
    for i in range(1, min(6, level)):
        temp = rarity_recursive(level, i, i)
        for j in temp:
            j.append(i)
            unchecked.append(j)
    for i in unchecked:
        if len(i) <= 6 and (level == 5 or len(i) > 2):
            to_return.append(i)
    return to_return


def rarity_recursive(level, m, u):
    to_return = []
    i = 1
    for i in range(1, min(u, level - m) + 1):
        temp = rarity_recursive(level, i + m, i)
        for j in temp:
            j.append(i)
            to_return.append(j)
    if i + m == level:
        to_return.append([i])
    return to_return


def gen_potion(level):
    f = open("ingredients.txt", 'r')
    ing_list = [[], [], [], [], []]
    for i in f:
        item = i.split("\t")
        ing_list[int(item[-2]) - 1].append(item[0].lower())
    ing = []
    rares = gen_rarity(level + 4)
    rarities = rares[random.randint(0, len(rares) - 1)]
    for i in rarities:
        ing.append(ing_list[i - 1][random.randint(0, len(ing_list[i - 1]) - 1)])
    f = open("ingredients.txt", 'r')
    return str(Potion(parse_table(f, ing))) + "\nLevel: " + str(level)


def main():
    print(gen_potion(int(sys.argv[1])))


if __name__ == "__main__":
    main()
