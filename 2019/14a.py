from collections import defaultdict
import math
import re

def sgn(i):
	if i > 0:
		return 1
	elif i == 0:
		return 0
	else:
		return -1

class recipe:
	def __init__(self, output, quantity, ingredients):
		self.output = output
		self.quantity = quantity
		self.ingredients = ingredients

isnumber = re.compile(r'\d+')
recipes = dict()
with open('14.dat', 'r') as file:
	for line in file:
		parts = line.split()
		ingredients = []
		number = None
		isoutput = False
		for part in parts:
			part = part.strip(',')
			if not isnumber.match(part) is None:
				number = int(part)
			elif part == '=>':
				isoutput = True
			elif not isoutput:
				assert number is not None
				ingredients.append((number, part))
				number = None
			else:
				assert number is not None
				recipes[part] = recipe(part, number, ingredients)

inventory = defaultdict(int)
def create_item(item, quantity):
	if item == 'ORE':
		return quantity

	if inventory[item] > quantity:
		inventory[item] -= quantity
		return 0

	recipe = recipes[item]
	times = math.ceil((quantity - inventory[item]) / recipe.quantity)
	out = 0
	for ingredient_number, ingredient_name in recipe.ingredients:
		out += create_item(ingredient_name, ingredient_number * times)

	inventory[item] += recipe.quantity * times - quantity

	return out

print(create_item('FUEL', 1))
