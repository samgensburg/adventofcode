from collections import defaultdict, deque
from functools import reduce

options_cache = dict()
def find_options(loc, passthroughs):
	passthroughs_key = ''.join(sorted(passthroughs))
	if (loc, passthroughs_key) in options_cache:
		return options_cache[(loc, passthroughs_key)]
	row, column = loc
	next = deque([(loc, 0)])
	visited = set()
	out = []
	while len(next) > 0:
		current_loc, distance = next.popleft()
		row, column = current_loc
		if current_loc in visited:
			continue
		visited.add(current_loc)
		char = grid[row][column]
		if char == '#':
			continue
		if char in passthroughs:
			next.append(((row + 1, column), distance + 1))
			next.append(((row - 1, column), distance + 1))
			next.append(((row, column + 1), distance + 1))
			next.append(((row, column - 1), distance + 1))
		elif char.islower():
			out.append((current_loc, char, distance))
	options_cache[(loc, passthroughs_key)] = out
	return out

with open('18.dat', 'r') as file:
	grid = []
	keys = set()
	for line in file:
		line = line.strip()
		grid.append(line)
		for i in range(len(line)):
			char = line[i]
			if char.islower():
				keys.add(char)
			if char == '@':
				start = (len(grid) - 1, i)

	paths = deque([(start, [], 0)])
	best = None
	while len(paths) > 0:
		loc, visited, length = paths.pop()
		if best is not None and length >= best:
			continue

		if set(visited) == set(keys):
			best = length
			print(best, visited)

		passthroughs = set(['.', '@'])
		for key in visited:
			passthroughs.add(key)
			passthroughs.add(key.upper())
		options = find_options(loc, passthroughs)

		for option in options:
			new_loc, new_key, new_length = option
			new_visited = visited.copy()
			new_visited.append(new_key)
			paths.append((new_loc, new_visited, length + new_length))

	print(best)
