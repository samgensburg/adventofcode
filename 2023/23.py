import argparse
from collections import defaultdict
import heapq
import math
from pathlib import Path
from queue import LifoQueue as Stack
from queue import Queue
import re

#import matplotlib.pyplot as plt

PATH = '.'
FOREST = '#'
SLOPES = {
	'>': (0, 1),
	'<': (0, -1),
	'^': (-1, 0),
	'v': (1, 0)
}

ADJACENCIES = [(0, 1), (0, -1), (-1, 0), (1, 0)]

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

class Grid():
	def __init__(self, grid):
		self.grid = grid
		self.y_max = len(grid) - 1
		self.x_max = len(grid[0]) - 1
		self.start = (0, grid[0].find(PATH))
		self.end = (self.y_max, grid[self.y_max].find(PATH))
		self.find_and_set_decision_points()
		self.find_and_set_paths()

	def find_and_set_decision_points(self):
		decision_points = [self.start, self.end]
		for y in range(1, self.y_max):
			for x in range(1, self.x_max):
				if self.grid[y][x] != PATH:
					continue

				count_passable = 0
				for y_a, x_a in ADJACENCIES:
					if self.grid[y + y_a][x + x_a] != FOREST:
						count_passable += 1
				if count_passable > 2:
					decision_points.append((y, x))

		self.decision_points = set(decision_points)

	def find_and_set_paths(self):
		self.decision_point_paths = dict()
		for decision_point in self.decision_points:
			self.decision_point_paths[decision_point] = self.find_paths_to_decision_points(decision_point)
	
	def find_paths_to_decision_points(self, decision_point):
		if decision_point == self.end:
			return dict()
		
		y_dp, x_dp = decision_point

		out = dict()
		for y_a, x_a in ADJACENCIES:
			path = [(y_dp, x_dp)]
			y, x = y_dp + y_a, x_dp + x_a
			if y < 0 or self.grid[y][x] == FOREST:
				continue
			while True:
				assert (y, x) not in path
				assert self.grid[y][x] != FOREST

				if (y, x) in self.decision_points:
					out[(y, x)] = path
					break

				path.append((y, x))
				if self.grid[y][x] == PATH:
					found = False
					for y_a2, x_a2 in ADJACENCIES:
						y_n, x_n = y + y_a2, x + x_a2
						if self.grid[y_n][x_n] == FOREST:
							continue

						if (y_n, x_n) in path:
							continue

						assert not found
						found = True
						y_n_found, x_n_found = y_n, x_n
					
					if not found:
						break
				
					y, x = y_n_found, x_n_found
					continue

				y_a2, x_a2 = SLOPES[self.grid[y][x]]
				y, x = y + y_a2, x + x_a2
				if self.grid[y][x] == FOREST:
					break

				if (y, x) in path:
					break
		
		return out

	def enumerate_all_paths(self):
		self.all_paths = []
		stack = Stack()
		stack.put(([self.start], 1))
		max_length = 0
		while stack.qsize():
			if stack.qsize() < 10:
				print(stack.qsize())
			path, length = stack.get()
			current = path[-1]
			if current == self.end:
				self.all_paths.append(path)
				if length > max_length:
					max_length = length
				continue

			nexts = [next for next in self.decision_point_paths[current]]
			for next in nexts:
				mini_path_len = 1 + len(set(self.decision_point_paths[current][next]))
				if next in path:
					continue

				new_path = [l for l in path]
				new_path.append(next)
				stack.put((new_path, length + mini_path_len))
		
		return max_length
	
	def validate_paths_and_return_longest(self):
		self.validated_paths = []
		longest = 0
		#import pdb; pdb.set_trace()
		for n, path in enumerate(self.all_paths):
			print(len(self.all_paths) - n)
			visited = set()
			invalid = False
			for i in range(len(path) - 1):
				start = path[i]
				end = path[i+1]
				assert start not in visited
				assert end not in visited
				assert start != self.end

				mini_path = set(self.decision_point_paths[start][end])
				assert start in mini_path
				if visited & mini_path:
					invalid = True
					break

				visited = visited | mini_path

			if invalid:
				print('INVALID!')
				continue

			dist = len(visited)
			self.validated_paths.append((path, dist))
			if dist > longest:
				longest = dist
		return longest


def parse_file(file):
	grid = []
	grid_b = []
	for line in file:
		line = line.strip()
		grid.append(line)
		grid_b.append(remove_slopes(line))


	return Grid(grid), Grid(grid_b)

def remove_slopes(l):
	for slope in SLOPES:
		l = l.replace(slope, PATH)
	return l


def main(input, printing=False):
	grid_a, grid_b = input
	out_a = grid_a.enumerate_all_paths()
	#out_a = grid_a.validate_paths_and_return_longest()
	out_b = grid_b.enumerate_all_paths()
	#out_b = grid_b.validate_paths_and_return_longest()

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
