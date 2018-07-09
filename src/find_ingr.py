"""
Gives the ingrediants found while in the given terrain
Written by Dietrich Geisler
"""

import sys
import math
import random

def parse_table(table, terrain, rarity):
	to_return = []
	for item in table:
		temp = item.strip().split("\t")
		while len(temp)>3:
			temp.pop(1)
		if temp[2].lower().strip()==terrain:
			if int(temp[1].lower().strip())==rarity:
				to_return.append(temp[0])
	return to_return

terrain = sys.argv[1].lower().strip()
rarity = 5-int(math.log(random.randint(1, 20), 2))
amount = random.randint(15, 20)-3*rarity
if amount <= 0:
	amount = 1

f = open("Ingredients.txt", 'r')
ingr = parse_table(f, terrain, rarity)
if len(ingr)==0:
	name = "nothing"
	amount = 0
else:
	name = ingr[random.randint(0, len(ingr)-1)]

print(amount, name)