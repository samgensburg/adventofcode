from collections import defaultdict, deque

with open('20.dat', 'r') as file:
	grid = []
	row = -1
	for line in file:
		row += 1
		line = line.strip('\n')
		grid.append([c for c in line])

portals = defaultdict(list)
portal_lookup = dict()

width = len(grid[2])
height = len(grid)

for row in range(height):
	for column in range(width):
		char = grid[row][column]
		if char.isupper():
			grid[row][column] = '#'
			char2 = grid[row][column + 1]
			if char2.isupper():
				portal_row = row
				if column == 0:
					is_left = True
				elif column == width - 2:
					is_left = False
				elif grid[row][column - 1] == '.':
					is_left = False
				else:
					is_left = True

				if is_left:
					portal_column = column + 2
				else:
					portal_column = column - 1
				grid[row][column + 1] = '#'
			else:
				char2 = grid[row + 1][column]
				assert char2.isupper()
				portal_column = column
				if row == 0:
					is_top = True
				elif row == height - 2:
					is_top = False
				elif grid[row - 1][column] == '.':
					is_top = False
				else:
					is_top = True

				if is_top:
					portal_row = row + 2
				else:
					portal_row = row - 1

				grid[row + 1][column] = '#'

			portal_name = char + char2
			portal_lookup[(portal_row, portal_column)] = portal_name
			portals[portal_name].append((portal_row, portal_column))

queue = deque()
queue.append((portals['AA'][0], 0))
del portal_lookup[portals['AA'][0]]
del portals['AA']

visited = set()
while len(queue) > 0:
	(row, column), distance = queue.popleft()
	if (row, column) in visited:
		continue

	visited.add((row, column))

	if (row, column) in portal_lookup:
		portal_name = portal_lookup[(row, column)]
		if portal_name == 'ZZ':
			print(distance)
			break
		portal_list = portals[portal_name]
		portal_loc = portal_list[0]
		if portal_loc == (row, column):
			portal_loc = portal_list[1]
		queue.append((portal_loc, distance + 1))

	potential_moves = [(row + 1, column), (row - 1, column), (row, column + 1), (row, column - 1)]
	for move_row, move_column in potential_moves:
		if grid[move_row][move_column] == '.':
			queue.append(((move_row, move_column), distance + 1))
