from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

def print_visited(i_max, j_max, visited):
	for i in range(i_max):
		row = ''
		for j in range(j_max):
			if (i, j) in visited:
				row += 'X'
			else:
				row += '.'
		print(row)
	print()
	print()

def main(text):
	return (main_a(text), main_b(text))

def main_a(text):
	grid = []
	queue = Queue()
	visited = set()
	for i in range(len(text)):
		row = text[i]
		int_row = []
		for j in range(len(row)):
			c = row[j]
			if c == 'S':
				queue.put((0, i, j))
				int_row.append(0)
			elif c == 'E':
				end_i = i
				end_j = j
				int_row.append(25)
			else:
				int_row.append(ord(c) - ord('a'))
		grid.append(int_row)
	
	while not queue.empty():
		print_visited(len(grid), len(grid[0]), visited)
		l, i, j = queue.get()
		targets = []
		if i > 0:
			targets.append((i - 1, j))
		if j > 0:
			targets.append((i, j - 1))
		if i < len(grid) - 1:
			targets.append((i + 1, j))
		if j < len(grid[0]) - 1:
			targets.append((i, j + 1))
		
		for target in targets:
			target_i, target_j = target
			if grid[target_i][target_j] - grid[i][j] > 1:
				continue
			if (target_i, target_j) in visited:
				continue
			if target_i == end_i and target_j == end_j:
				return l + 1
			visited.add((target_i, target_j))
			queue.put((l + 1, target_i, target_j))

def main_b(text):
	grid = []
	queue = Queue()
	visited = set()
	for i in range(len(text)):
		row = text[i]
		int_row = []
		for j in range(len(row)):
			c = row[j]
			if c == 'E':
				queue.put((0, i, j))
				int_row.append(25)
			elif c == 'S':
				int_row.append(0)
			else:
				int_row.append(ord(c) - ord('a'))
		grid.append(int_row)
	
	while not queue.empty():
		print_visited(len(grid), len(grid[0]), visited)
		l, i, j = queue.get()
		targets = []
		if i > 0:
			targets.append((i - 1, j))
		if j > 0:
			targets.append((i, j - 1))
		if i < len(grid) - 1:
			targets.append((i + 1, j))
		if j < len(grid[0]) - 1:
			targets.append((i, j + 1))
		
		for target in targets:
			target_i, target_j = target
			if grid[i][j] - grid[target_i][target_j] > 1:
				continue
			if (target_i, target_j) in visited:
				continue
			if grid[target_i][target_j] == 0:
				return l + 1
			visited.add((target_i, target_j))
			queue.put((l + 1, target_i, target_j))

with open(DATA_FILE, 'r') as file:
	print(main(file.read().strip().split('\n')))
