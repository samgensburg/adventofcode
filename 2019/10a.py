from functools import reduce

def is_almost_int(f):
	diff = abs(f - round(f))
	return diff < 0.01

with open('10.dat', 'r') as file:
	grid = []
	for line in file:
		line = line.strip()
		row = [c == '#' for c in line]
		grid.append(row)

	count = reduce(lambda acc, val: val + acc, [reduce(lambda acc2, val2: 1 + acc2 if val2 else acc2, row, 0) for row in grid])
	width = len(grid[0])
	height = len(grid)
	max_count = 0
	for i in range(width):
		for j in range(height):
			if not grid[j][i]:
				continue

			asteroid_count = 0
			for x in range(width):
				for y in range(height):
					if not grid[y][x]:
						continue
					if y == j and x == i:
						continue

					visible = True
					if x == i:
						for n in range(height):
							if n > min(y, j) and n < max(y, j) and grid[n][x]:
								visible = False
								break
					else:
						if x < i:
							iterator = range(x + 1, i)
						else:
							iterator = range(x - 1, i, -1)
						for m in iterator:
							n = (y - j) / (x - i) * (m - x) + y
							if is_almost_int(n):
								n = round(n)
							else:
								continue
							if grid[n][m]:
								visible = False
								break
					if visible:
						asteroid_count += 1

			if asteroid_count > max_count:
				max_count = asteroid_count
	print(max_count)
