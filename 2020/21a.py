from collections import defaultdict
from functools import reduce
import re

class Food:
	def __init__(self, line):
		line = line.strip()
		assert line[-1] == ')'
		parts = line.split(' (contains ')
		self.ingredients = set(parts[0].split())
		self.allergens = set(parts[1][:-1].split(', '))

def main():
	with open('21.dat', 'r') as file:
		foods = [Food(line) for line in file]

	ingredients = reduce(lambda acc, f: acc.union(f.ingredients), foods, set())
	allergens = reduce(lambda acc, f: acc.union(f.allergens), foods, set())

	allergen_dict = {}
	for allergen in allergens:
		potential_ingredients = None
		for food in foods:
			if allergen in food.allergens:
				if potential_ingredients is None:
					potential_ingredients = food.ingredients
				else:
					potential_ingredients = potential_ingredients.intersection(food.ingredients)
		allergen_dict[allergen] = potential_ingredients

	may_contain_allergen = reduce(lambda acc, s: acc.union(s), allergen_dict.values())
	does_not_contain_allergens = ingredients - may_contain_allergen

	count = 0
	for ingredient in does_not_contain_allergens:
		for food in foods:
			if ingredient in food.ingredients:
				count += 1

	#import pdb; pdb.set_trace()
	return count

print(main())
