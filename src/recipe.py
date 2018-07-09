"""
Script to generate potion recipes
All arguments are optional
1st argument- integer 1-4 indicating potion quality, assumed to be random if excluded
2nd argument- string indicating potion type, assumed to be random if excluded
Note that the a potion type can be specified without quality
Written by Dietrich Geisler
"""
import sys
import random
from potion import Potion, Ingredient, RANGES

def strQ(quality):
	if quality == 4:
		return "IV"
	return "I"*quality

def createRecipe(quality, type):
	range = RANGES[quality-1]
	ingredients = []
	with open("Ingredients.txt", 'r') as f:
		for i in f:
			item = [*map(str.lower, i.split("\t")[1:14])]
			if type in item[range[0] : range[1]]:
				ingredients.append(Ingredient(i.split("\t")[0], item))
	count = 2 if quality == 4 else quality
	if count > len(ingredients):
		print("There are not enough ingredients to make a potion of type " + type + " with quality " + strQ(quality))
		exit()
	#return ingredients #<-- uncomment if you want a complete list of the given quality
	return random.sample(ingredients, count)

def selectTraits(quality, type):
	if quality == 0:
		quality = random.randint(1, 4)
	if not type == "random":
		return quality, type
	with open("Types.txt", 'r') as f:
		typeList = []
		for i in f:
			typeList.append(i.split("\t")[1])
		type = random.choice(typeList).lower().strip()
	return quality, type

def main():
	quality = 0
	type = "random"
	for i in sys.argv[1:]:
		s = i.lower().strip()
		if s in ["1", "2", "3", "4"]:
			quality = int(s)
		else:
			type = s
	ingredients = createRecipe(*selectTraits(quality, type))
	print(ingredients)
	print(Potion(ingredients))

if __name__ == "__main__":
	main()