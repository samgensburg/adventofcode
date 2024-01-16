import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

ROUND = 'O'
EMPTY = '.'
SQUARE = '#'

CYCLE_COUNT = 1000000000

class Grid():
	def __init__(self, grid):
		self.grid = []
		self.row_count = len(grid)
		self.column_count = len(grid[0])
		for i, line in enumerate(grid):
			grid_line = []
			for j, c in enumerate(line):
				grid_line.append(c)
			self.grid.append(grid_line)
	
	def hash(self):
		return ''.join([''.join(row) for row in self.grid])

	def spin(self):
		self.tilt_north()
		self.tilt_west()
		self.tilt_south()
		self.tilt_east()

	def tilt_north(self):
		while self._once_north():
			pass

	def tilt_south(self):
		while self._once_south():
			pass

	def tilt_east(self):
		while self._once_east():
			pass

	def tilt_west(self):
		while self._once_west():
			pass

	def _once_north(self):
		out = False
		for i in range(self.row_count):
			for j in range(self.column_count):
				val = self.try_get(i, j)
				if val != ROUND:
					continue
				destination = self.try_get(i - 1, j)
				if destination == EMPTY:
					self.set(i, j, EMPTY)
					self.set(i - 1, j, ROUND)
					out = True
		return out
	
	def _once_west(self):
		out = False
		for j in range(self.column_count):
			for i in range(self.row_count):
				val = self.try_get(i, j)
				if val != ROUND:
					continue
				destination = self.try_get(i, j - 1)
				if destination == EMPTY:
					self.set(i, j, EMPTY)
					self.set(i, j - 1, ROUND)
					out = True
		return out

	def _once_south(self):
		out = False
		for i in range(self.row_count - 1, -1, -1):
			for j in range(self.column_count):
				val = self.try_get(i, j)
				if val != ROUND:
					continue
				destination = self.try_get(i + 1, j)
				if destination == EMPTY:
					self.set(i, j, EMPTY)
					self.set(i + 1, j, ROUND)
					out = True
		return out
	
	def _once_east(self):
		out = False
		for j in range(self.column_count - 1, -1, -1):
			for i in range(self.row_count):
				val = self.try_get(i, j)
				if val != ROUND:
					continue
				destination = self.try_get(i, j + 1)
				if destination == EMPTY:
					self.set(i, j, EMPTY)
					self.set(i, j + 1, ROUND)
					out = True
		return out

	def try_get(self, i, j):
		if i < 0 or i >= self.row_count or j < 0 or j >= self.column_count:
			return None
		return self.grid[i][j]
	
	def set(self, i, j, val):
		self.grid[i][j] = val

	def calculate_score(self):
		total = 0
		for i in range(self.row_count):
			for j in range(self.column_count):
				if self.try_get(i, j) == ROUND:
					total += self.row_count - i
		return total
	
	def pretty_print(self):
		for row in self.grid:
			print(''.join(row))


def parse_file(file):
	grid = []
	for i, line in enumerate(file):
		line = line.strip()
		grid.append(line)

	return Grid(grid), Grid(grid)


def main(input, printing=False):
	grid_a, grid_b = input
	grid_a.tilt_north()

	score_a = grid_a.calculate_score()

	cache = dict()
	for i in range(CYCLE_COUNT):
		if printing:
			print(f'After {i} cycle(s), the grid appears as follows:')
			grid_b.pretty_print()
			print()

		#import pdb; pdb.set_trace()
		key = grid_b.hash()
		if key in cache:
			diff = i - cache[key]
			if (CYCLE_COUNT - i) % diff == 0:
				score_b = grid_b.calculate_score()
				break
		cache[key] = i
		grid_b.spin()

	return score_a, score_b


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
