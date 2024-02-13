import argparse
from collections import defaultdict
import heapq
import math
from pathlib import Path
from queue import LifoQueue as Stack
from queue import Queue
import re

#import matplotlib.pyplot as plt

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'


def parse_file(file):
	instructions = []
	for line in file:
		line = line.strip()
		match = re.match(r'([UDLR]) (\d+) \(\#([0-9a-f]{6})\)', line)
		assert match
		instructions.append((match.group(1), int(match.group(2)), match.group(3)))

	return instructions

def dig(instructions, printing):
	grid_dict = defaultdict(str)
	x = y = 0
	x_min = x_max = y_min = y_max = 0
	grid_dict[(y, x)] = "XXXXXX"
	for instruction in instructions:
		dir, n, color = instruction
		if dir == 'R':
			for i in range(n):
				x += 1
				grid_dict[(y, x)] = color
			x_max = max(x, x_max)
		elif dir == 'L':
			for i in range(n):
				x -= 1
				grid_dict[(y, x)] = color
			x_min = min(x, x_min)		
		elif dir == 'D':
			for i in range(n):
				y += 1
				grid_dict[(y, x)] = color
			y_max = max(y, y_max)
		elif dir == 'U':
			for i in range(n):
				y -= 1
				grid_dict[(y, x)] = color
			y_min = min(y, y_min)
		else:
			assert False

	x_min -= 1
	y_min -= 1
	x_max += 1
	y_max += 1

	grid = [[None for x in range(x_max - x_min + 1)] for y in range(y_max - y_min + 1)]
	for y in range(len(grid)):
		for x in range(len(grid[0])):
			grid[y][x] = grid_dict[(y + y_min, x + x_min)]
	return grid

def total_size(grid):
	assert not grid[0][0]

	y_max = len(grid)
	x_max = len(grid[0])
	queue = Queue()
	queue.put((0, 0))
	visited = set()
	while queue.qsize():
		loc = queue.get()
		if loc in visited:
			continue
		y, x = loc
		if grid[y][x] != '':
			continue
		visited.add(loc)
		if y > 0:
			queue.put((y - 1, x))
		if y < y_max - 1:
			queue.put((y + 1, x))
		if x > 0:
			queue.put((y, x - 1))
		if x < x_max - 1:
			queue.put((y, x + 1))
	return y_max * x_max - len(visited)

def print_grid(grid):
	for y in range(len(grid)):
		line = ['#' if grid[y][x] != '' else '.' for x in range(len(grid[0]))]
		print (''.join(line))


def dig_large(instructions):
	y = x = 0
	lines = []
	critical_rows = set()
	for i in range(len(instructions) - 1):
		dir_a = int(instructions[i][5])
		dir_b = int(instructions[i+1][5])
		assert abs(dir_a - dir_b) in [1, 3]

	#import pdb; pdb.set_trace()

	vertices_x = []
	vertices_y = []
	horizontal_lines = defaultdict(list)
	for instruction in instructions:
		vertices_x.append(x)
		vertices_y.append(y)
		dir = instruction[5]
		assert dir in ['1', '2', '3', '0']
		dist = int(instruction[:5], 16)

		if dir == '2' or dir == '3':
			dist = -dist
		if dir == '0' or dir == '2':
			critical_rows.add(y)
			x_new = x + dist
			y_new = y
			horizontal_lines[y].append((x, x_new))
		else:
			x_new = x
			y_new = y + dist
			lines.append((x, y, y_new))
		x = x_new
		y = y_new
	
	vertices_x.append(0)
	vertices_y.append(0)
	#plt.figure()
	#plt.plot(vertices_x,vertices_y) 
	#plt.show()
	#import pdb; pdb.set_trace()

	critical_rows = sorted(list(critical_rows))
	lookup_table = defaultdict(list)
	for critical_row in critical_rows:
		row_only = str(critical_row)
		row_minus = row_only + '-'
		row_plus = row_only + '+'
		for line in lines:
			x, y, y_new = line
			if y < critical_row and y_new < critical_row:
				continue
			if y > critical_row and y_new > critical_row:
				continue
			lookup_table[row_only].append(line)
			if y > critical_row or y_new > critical_row:
				lookup_table[row_plus].append(line)
			if y < critical_row or y_new < critical_row:
				lookup_table[row_minus].append(line)
	
	out = 0
	#import pdb; pdb.set_trace()
	for y in critical_rows:
		lines = lookup_table[str(y)]
		xs_up = []
		xs_down = []
		xs = []
		horizontals = horizontal_lines[y]
		for line in lines:
			x, y_line, y_new = line
			xs.append(x)
			if y != y_line and y != y_new: # crossing the critical y
				pass
			elif y_line < y or y_new < y:
				xs_down.append(x)
			else:
				xs_up.append(x)


		joins_same = dict()
		joins_cross = dict()
		for horizontal in horizontals:
			x_start, x_end = horizontal
			x_start, x_end = min(x_start, x_end), max(x_start, x_end)
			if (x_start in xs_up and x_end in xs_up) or (x_start in xs_down and x_end in xs_down):
				joins_same[x_start] = x_end
			else:
				joins_cross[x_start] = x_end

		xs = sorted(xs)
		counter = 0
		skip_next = False
		#import pdb; pdb.set_trace()
		for i in range(len(xs)):
			x = xs[i]
			if skip_next:
				skip_next = False
				continue

			if counter % 2 == 0:
				out -= x - 1
				if x in joins_same:
					pass
				if x in joins_cross:
					skip_next = True

			else:
				if x in joins_same:
					skip_next = True
					continue
				if x in joins_cross:
					continue
				out += x
			
			counter += 1

	for i in range(len(critical_rows) - 1):
		y_low = critical_rows[i]
		y_high = critical_rows[i+1]
		assert y_high > y_low
		assert set(lookup_table[str(y_low) + '+']) == set(lookup_table[str(y_high) + '-'])
		lines = lookup_table[str(y_low) + '+']
		assert len(lines) % 2 == 0
		xs = sorted([x for x, _, _ in lines])
		xs = sorted(xs)

		column_count = 0
		for i in range(len(xs)):
			if i % 2 == 0:
				column_count -= xs[i] - 1
			else:
				column_count += xs[i]
		out += (y_high - y_low - 1) * column_count

	return out
	

def main(instructions, printing=False):
	grid = dig(instructions, printing)
	if printing:
		print_grid(grid)
	out_a = total_size(grid)
	
	out_b = dig_large([color for _, _, color in instructions])

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
