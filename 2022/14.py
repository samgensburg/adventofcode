from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

X_MAX = 1000
Y_MAX = 1000

EMPTY = '.'
SAND = 'o'
WALL = '#'

def process_input(lines, base=False):
	grid = [[EMPTY for i in range(X_MAX)] for j in range(Y_MAX)]
	y_max = 0
	for line in lines:
		parts = line.split()
		assert len(parts) % 2 == 1
		for i in range(1, len(parts), 2):
			assert parts[i] == '->'
		parts = [parts[i] for i in range(0, len(parts), 2)]

		x, y = parts[0].split(',')
		x, y = int(x), int(y)
		y_max = max(y, y_max)
		for part in parts[1:]:
			new_x, new_y = part.split(',')
			new_x, new_y = int(new_x), int(new_y)
			assert (x == new_x) != (y == new_y)

			if new_x == x:
				start_y, end_y = min(y, new_y), max(y, new_y)
				for j in range(start_y, end_y + 1):
					grid[j][x] = WALL
			else:
				assert new_y == y
				start_x, end_x = min(x, new_x), max(x, new_x)
				for i in range(start_x, end_x + 1):
					grid[y][i] = WALL

			x, y = new_x, new_y
			y_max = max(y, y_max)

	if base:
		for i in range(X_MAX):
			grid[y_max + 2][i] = WALL

	return grid

def drop(grid):
	x = 500
	y = 0
	while True:
		if y == Y_MAX - 1:
			return False
		if grid[y + 1][x] == EMPTY:
			y = y + 1
			continue
		if grid[y + 1][x - 1] == EMPTY:
			y, x = y + 1, x - 1
			continue
		if grid[y + 1][x + 1] == EMPTY:
			y, x = y + 1, x + 1
			continue
		grid[y][x] = SAND
		return True

def solve(grid):
	for count in range(1000000):
		if grid[0][500] == SAND:
			draw_map(grid)
			return count
		if not drop(grid):
			return count

def draw_map(grid):
	for row in grid:
		print(''.join(row))

def main():
	with open(DATA_FILE, 'r') as file:
		lines = file.read().strip().split('\n')

	data = process_input(lines)
	data2 = process_input(lines, base=True)
	return solve(data), solve(data2)


print(main())
