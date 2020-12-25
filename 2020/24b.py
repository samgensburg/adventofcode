from collections import defaultdict
import re

def string_to_coords(string):
	assert re.match(r'^[nsew]+$', string)
	x, y = 0, 0
	i = 0
	while i < len(string):
		char = string[i]
		if char == 'n' or char == 's':
			assert i + 1 < len(string)
			char2 = string[i + 1]
			if char == 'n':
				y += 1
				if char2 == 'e':
					x += 1
			else:
				y -= 1
				if char2 == 'w':
					x -= 1
			i += 1
		elif char == 'w':
			x -= 1
		elif char == 'e':
			x += 1
		else:
			assert False

		i += 1
	return x, y


def main():
	black = defaultdict(bool)
	with open('24.dat', 'r') as file:
		state = 0
		for line in file:
			line = line.strip()
			coords = string_to_coords(line)
			if black[coords]:
				black[coords] = False
			else:
				black[coords] = True

	for n in range(100):
		print_grid(black)
#		import pdb; pdb.set_trace()
		print(len([coords for coords in black if black[coords]]))
		new_black = defaultdict(bool)
		neighbor_count = defaultdict(int)
		for x, y in black.keys():
			if black[(x, y)]:
				neighbor_count[(x + 1, y)] += 1
				neighbor_count[(x + 1, y + 1)] += 1
				neighbor_count[(x, y + 1)] += 1
				neighbor_count[(x - 1, y)] += 1
				neighbor_count[(x - 1, y - 1)] += 1
				neighbor_count[(x, y - 1)] += 1

		for key in neighbor_count:
			if neighbor_count[key] == 2:
				new_black[key] = True
			if neighbor_count[key] == 1 and black[key]:
				new_black[key] = True

		black = new_black

	return len([coords for coords in black if black[coords]])

def print_grid(black):
	x_min, x_max, y_min, y_max = 0, 0, 0, 0
	for x, y in black:
		if x < x_min:
			x_min = x
		if x > x_max:
			x_max = x
		if y < y_min:
			y_min = y
		if y > y_max:
			y_max = y

	print()
	for y in range(y_max, y_min - 1, -1):
		values = ['#' if black[(x, y)] else '.' for x in range(x_min, x_max + 1)]
		print(''.join(values))
	print()

print(main())
