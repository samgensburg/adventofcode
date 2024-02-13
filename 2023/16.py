import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3

def parse_file(file):
	grid = []
	for line in file:
		line = line.strip()
		grid.append(line)

	return grid


def count_energized(grid, y_in, x_in, direction, printing=False):
	energized = set()
	visited = set()
	actions = [(y_in, x_in, direction)]
	while len(actions) > 0:
		y, x, direction = actions.pop()
		if (y, x, direction) in visited:
			continue
		visited.add(((y, x, direction)))
		if printing:
			print(y, x, direction)
		energized.add((y, x))
		if direction == RIGHT:
			y_next = y
			x_next = x + 1
		elif direction == LEFT:
			y_next = y
			x_next = x - 1
		elif direction == UP:
			y_next = y - 1
			x_next = x
		elif direction == DOWN:
			y_next = y + 1
			x_next = x
	
		if y_next < 0 or x_next < 0 or y_next >= len(grid) or x_next >= len(grid[0]):
			continue

		next_symbol = grid[y_next][x_next]
		if next_symbol == '.':
			actions.append((y_next, x_next, direction))
		elif next_symbol == '-':
			if direction == LEFT or direction == RIGHT:
				actions.append((y_next, x_next, direction))
			else:
				actions.append((y_next, x_next, RIGHT))
				actions.append((y_next, x_next, LEFT))
		elif next_symbol == '|':
			if direction == UP or direction == DOWN:
				actions.append((y_next, x_next, direction))
			else:
				actions.append((y_next, x_next, DOWN))
				actions.append((y_next, x_next, UP))
		elif next_symbol == '/':
			reflection = {RIGHT:UP, UP:RIGHT, DOWN:LEFT, LEFT:DOWN}
			actions.append((y_next, x_next, reflection[direction]))
		elif next_symbol == '\\':
			reflection = {RIGHT:DOWN, DOWN:RIGHT, UP:LEFT, LEFT:UP}
			actions.append((y_next, x_next, reflection[direction]))
		else:
			assert False

	energized.remove((y_in, x_in))
	return len(energized)

def main(grid, printing=False):
	out_a = count_energized(grid, 0, -1, RIGHT)
	out_b = 0
	for y in range(len(grid)):
		out_b = max(out_b, count_energized(grid, y, -1, RIGHT), count_energized(grid, y, len(grid[0]), LEFT))
	for x in range(len(grid[0])):
		out_b = max(out_b, count_energized(grid, -1, x, DOWN), count_energized(grid, len(grid), x, UP))
	
	return out_a, out_b
		


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data, printing=args.print))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--sample', action='store_true')
	parser.add_argument('-p', '--print', action='store_true')
	args = parser.parse_args()

	wrapper(args)
