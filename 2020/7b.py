"light red bags contain 1 bright white bag, 2 muted yellow bags."

def main():
	with open('7.dat', 'r') as file:
		map = dict()
		for line in file:
			line = line.strip()
			index = line.find(' bags contain ')
			type = line[:index]
			line = line[index + 14:]
			if line == 'no other bags.':
				map[type] = []
				continue

			contents = []
			while len(line):
				index = line.find(' ')
				number = int(line[:index])
				line = line[index + 1:]
				index = line.find(' bag')
				inner_type = line[:index]
				contents.append((number, inner_type))
				line = line[index + 4:]
				if line[0] == 's':
					line = line[1:]
				if line[0] == ',':
					line = line[1:]
				line = line[1:]

			map[type] = contents

	total = 0
	return has_inside('shiny gold', map)

cache = dict()
def has_inside(type, map):
	print(type)
	if type in cache:
		return cache[type]

	total = 0
	for (number, inner_type) in map[type]:
		total += number * (has_inside(inner_type, map) + 1)
	cache[type] = total
	print(total)
	return total

outer_cache = dict()
def can_be_outer(type, map):
	if type in outer_cache:
		return outer_cache[type]
	if type == 'shiny gold':
		return True

	output = False
	for (number, inner_type) in map[type]:
		if can_be_outer(inner_type, map):
			output = True
	outer_cache[type] = output
	return output

print(main())
