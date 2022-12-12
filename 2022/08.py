from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

def visible_in_line(line):
	output = [False for n in line]
	current_left = -1
	current_right = -1
	for i in range(len(line)):
		n = line[i]
		if n > current_left:
			output[i] = True
			current_left = n
	for i in range(len(line) - 1, -1, -1):
		n = line[i]
		if n > current_right:
			output[i] = True
			current_right = n
	return output

def main():
	grid = []
	grid_visible = []
	with open(DATA_FILE, 'r') as file:
		for line in file:
			grid.append([int(c) for c in line.strip()])
			grid_visible.append([False for c in line.strip()])
	
	x_max = len(grid[0])
	y_max = len(grid)

	for i in range(y_max):
		row_visible = visible_in_line(grid[i])
		for j in range(len(row_visible)):
			if row_visible[j]:
				grid_visible[i][j] = True
	
	for i in range(x_max):
		column_visible = visible_in_line([grid[j][i] for j in range(y_max)])
		for j in range(y_max):
			if column_visible[j]:
				grid_visible[j][i] = True

	total = 0
	for row in grid_visible:
		for b in row:
			if b:
				total += 1

	best = 0

	for i in range(y_max):
		for j in range(x_max):
			height = grid[i][j]
			up = 0
			down = 0
			right = 0
			left = 0
			up_i = i - 1
			down_i = i + 1
			right_j = j + 1
			left_j = j - 1

			while up_i >= 0:
				up += 1
				if grid[up_i][j] >= height:
					break
				up_i -= 1

			while down_i < y_max:
				down += 1
				if grid[down_i][j] >= height:
					break
				down_i += 1

			while left_j >= 0:
				left += 1
				if grid[i][left_j] >= height:
					break
				left_j -= 1

			while right_j < x_max:
				right += 1
				if grid[i][right_j] >= height:
					break
				right_j += 1
			
			score = up * down * left * right
			if score > best:
				best = score

	return total, best

assert visible_in_line([1,2,3,4]) == [True, True, True, True]
assert visible_in_line([0,0,0,0]) == [True, False, False, True]

print(main())
