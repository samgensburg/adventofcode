from collections import defaultdict, deque
from functools import reduce

options_cache = dict()
def find_options(locs, passthroughs):
	passthroughs_key = ''.join(sorted(passthroughs))
	locs_key = ''.join(['%3s%3s' % loc for loc in locs])
	if (locs_key, passthroughs_key) in options_cache:
		return options_cache[(locs_key, passthroughs_key)]
	next = deque([(0, locs[0], 0), (1, locs[1], 0), (2, locs[2], 0), (3, locs[3], 0)])
	visited = set()
	out = []
	while len(next) > 0:
		bot, current_loc, distance = next.popleft()
		row, column = current_loc
		if current_loc in visited:
			continue
		visited.add(current_loc)
		char = grid[row][column]
		if char == '#':
			continue
		if char in passthroughs:
			next.append((bot, (row + 1, column), distance + 1))
			next.append((bot, (row - 1, column), distance + 1))
			next.append((bot, (row, column + 1), distance + 1))
			next.append((bot, (row, column - 1), distance + 1))
		elif char.islower():
			out_locs = locs.copy()
			out_locs[bot] = current_loc
			out.append((out_locs, char, distance))
	options_cache[(locs_key, passthroughs_key)] = out
	return out

with open('18b.dat', 'r') as file:
	grid = []
	keys = set()
	start = []
	for line in file:
		line = line.strip()
		grid.append(line)
		for i in range(len(line)):
			char = line[i]
			if char.islower():
				keys.add(char)
			if char == '@':
				start.append((len(grid) - 1, i))

	paths = deque([(start, [], 0)])
	best = None
	while len(paths) > 0:
		locs, visited, length = paths.pop()
		if best is not None and length >= best:
			continue

		if len(visited) <= 8:
			print('    ', visited)

		if set(visited) == set(keys):
			best = length
			print(best, visited)

		passthroughs = set(['.', '@'])
		for key in visited:
			passthroughs.add(key)
			passthroughs.add(key.upper())
		options = find_options(locs, passthroughs)

		for option in options:
			new_locs, new_key, new_length = option
			new_visited = visited.copy()
			new_visited.append(new_key)
			paths.append((new_locs, new_visited, length + new_length))

	print(best)
