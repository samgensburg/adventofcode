input = ['.#.#.',
		 '.##..',
		 '.#...',
		 '.###.',
		 '##..#']

center = [[input[row][column] == '#' for column in range(5)] for row in range(5)]
current = dict()
for i in range(-201, 202):
	if i != 0:
		current[i] = [[False] * 5 for j in range(5)]
	else:
		current[i] = center

for i in range(200):
	print(current[0])
	next = dict()
	for j in range(-201, 202):
		next[j] = [[False] * 5 for j in range(5)]

	for level in range(-200, 201):
		for row in range(5):
			for column in range(5):
				if row == 2 and column == 2:
					continue

				adjacent_count = 0
				if row < 4 and current[level][row + 1][column]:
					adjacent_count += 1
				if row > 0 and current[level][row - 1][column]:
					adjacent_count += 1
				if column < 4 and current[level][row][column + 1]:
					adjacent_count += 1
				if column > 0 and current[level][row][column - 1]:
					adjacent_count += 1
				if row == 0 and current[level - 1][1][2]:
					adjacent_count += 1
				if row == 4 and current[level - 1][3][2]:
					adjacent_count += 1
				if column == 0 and current[level - 1][2][1]:
					adjacent_count += 1
				if column == 4 and current[level - 1][2][3]:
					adjacent_count += 1
				if row == 1 and column == 2:
					for inner_column in range(5):
						if current[level + 1][0][inner_column]:
							adjacent_count += 1
				if row == 3 and column == 2:
					for inner_column in range(5):
						if current[level + 1][4][inner_column]:
							adjacent_count += 1
				if column == 1 and row == 2:
					for inner_row in range(5):
						if current[level + 1][inner_row][0]:
							adjacent_count += 1
				if column == 3 and row == 2:
					for inner_row in range(5):
						if current[level + 1][inner_row][4]:
							adjacent_count += 1

				if current[level][row][column] and adjacent_count == 1:
					next[level][row][column] = True
				if (not current[level][row][column]) and adjacent_count > 0 and adjacent_count < 3:
					next[level][row][column] = True
	current = next

count = 0
for level in range(-200, 201):
	for row in range(5):
		for column in range(5):
			if current[level][row][column]:
				count += 1
print(count)
