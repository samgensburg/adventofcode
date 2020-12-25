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
				y += 2
			else:
				y -= 2
			if char2 == 'w':
				x -= 1
			else:
				assert char2 == 'e'
				x += 1
			i += 1
		elif char == 'w':
			x -= 2
		elif char == 'e':
			x += 2
		else:
			assert False

		i += 1
	return x, y


def main():
	black = set()
	with open('24.dat', 'r') as file:
		state = 0
		for line in file:
			line = line.strip()
			coords = string_to_coords(line)
			if coords in black:
				black.remove(coords)
			else:
				black.add(coords)

	return len(black)

print(main())
