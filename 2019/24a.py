input = ['.#.#.',
		 '.##..',
		 '.#...',
		 '.###.',
		 '##..#']

def get_biodiversity(value):
	out = 0
	for row in range(5):
		for column in range(5):
			if value[row][column]:
				out += (2 ** column) * (32 ** row)
	return out

current = [[input[row][column] == '#' for column in range(5)] for row in range(5)]
seen = set()
while get_biodiversity(current) not in seen:
	print(get_biodiversity(current))
	seen.add(get_biodiversity(current))
	next = [[False] * 5 for i in range(5)]
	for row in range(5):
		for column in range(5):
			adjacent_count = 0
			if row < 4 and current[row + 1][column]:
				adjacent_count += 1
			if row > 0 and current[row - 1][column]:
				adjacent_count += 1
			if column < 4 and current[row][column + 1]:
				adjacent_count += 1
			if column > 0 and current[row][column - 1]:
				adjacent_count += 1

			if current[row][column] and adjacent_count == 1:
				next[row][column] = True
			if (not current[row][column]) and adjacent_count > 0 and adjacent_count < 3:
				next[row][column] = True
	current = next
print(get_biodiversity(current))
