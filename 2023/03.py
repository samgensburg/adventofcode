import argparse
from collections import defaultdict
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'


RED_TARGET = 12
GREEN_TARGET = 13
BLUE_TARGET = 14

def check_adjacency(c):
	if c.isdigit() or c == '.':
		return False
	return True


def is_gear(c):
	return c == '*'


def has_adjacency(y, x_start, x_end, grid):
	y_max = len(grid) - 1
	x_max = len(grid[0]) - 1
	out = False

	if y > 0:
		for x in range(x_start, x_end + 1):
			out = out or check_adjacency(grid[y-1][x])
	if y < y_max:
		for x in range(x_start, x_end + 1):
			out = out or check_adjacency(grid[y+1][x])
	out = out or (x_start > 0 and check_adjacency(grid[y][x_start-1]))
	out = out or (x_end < x_max and check_adjacency(grid[y][x_end+1]))
	out = out or (x_start > 0 and y > 0 and check_adjacency(grid[y-1][x_start-1]))
	out = out or (x_end < x_max and y > 0 and check_adjacency(grid[y-1][x_end+1]))
	out = out or (x_start > 0 and y < y_max and check_adjacency(grid[y+1][x_start-1]))
	out = out or (x_end < x_max and y < y_max and check_adjacency(grid[y+1][x_end+1]))
	return out


def get_gear_loc(y, x_start, x_end, grid):
	y_max = len(grid) - 1
	x_max = len(grid[0]) - 1
	out = False
	
	if y > 0:
		for x in range(x_start, x_end + 1):
			if is_gear(grid[y-1][x]):
				return (y-1, x)
	
	if y < y_max:
		for x in range(x_start, x_end + 1):
			if is_gear(grid[y+1][x]):
				return (y+1, x)
	
	if x_start > 0 and is_gear(grid[y][x_start-1]):
		return (y, x_start - 1)
	if x_end < x_max and is_gear(grid[y][x_end+1]):
		return (y, x_end + 1)
	if x_start > 0 and y > 0 and is_gear(grid[y-1][x_start-1]):
		return (y - 1, x_start - 1)
	if x_end < x_max and y > 0 and is_gear(grid[y-1][x_end+1]):
		return (y - 1, x_end + 1)
	if x_start > 0 and y < y_max and is_gear(grid[y+1][x_start-1]):
		return (y + 1, x_start - 1)
	if x_end < x_max and y < y_max and is_gear(grid[y+1][x_end+1]):
		return (y + 1, x_end + 1)
	return None


def main(data_source):
	with open(data_source, 'r') as file:
		grid = []
		for line in file:
			line = line.strip()
			grid.append(line)
		
		sum_a = sum_b = 0
		gear_list = defaultdict(list)
		for y, line in enumerate(grid):
			i = 0
			while True:
				match = re.search(r'(\d+)', line[i:])
				if not match:
					break

				part_number = int(match.group(1))
				x_start = i + match.start()
				x_end = x_start + len(match.group(1)) - 1
				i = x_end + 1
				if has_adjacency(y, x_start, x_end, grid):
					sum_a += part_number
				gear_loc = get_gear_loc(y, x_start, x_end, grid)
				if gear_loc:
					gear_list[gear_loc].append(part_number)

		for key in gear_list:
			assert len(gear_list[key]) <= 2
			if len(gear_list[key]) == 2:
				sum_b += gear_list[key][0] * gear_list[key][1]



		return sum_a, sum_b

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

data_source = SAMPLE_FILE if args.sample else DATA_FILE
print(main(data_source))
