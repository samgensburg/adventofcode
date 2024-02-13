import argparse
from collections import defaultdict
import heapq
import math
from pathlib import Path
from queue import LifoQueue as Stack
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'


def parse_file(file):
	grid = []
	for line in file:
		line = line.strip()
		grid.append([int(n) for n in line])

	return grid

class Direction():
	def __init__(self, value):
		self.value = value

	def __repr__(self):
		if self.value == _RIGHT:
			return 'right'
		elif self.value == _DOWN:
			return 'down'
		elif self.value == _LEFT:
			return 'left'
		elif self.value == _UP:
			return 'up'
	
	def __lt__(self, obj):
		return self.value < obj

	def	__eq__(self, obj):
		return self.value == obj
	def __ne__(self, obj):
		return self.value != obj
	def __le__(self, obj):
		return self.value <= obj
	def __gt__(self, obj):
		return self.value > obj
	def __ge__(self, obj):
		return self.value >= obj
	def __hash__(self):
		return self.value

_RIGHT = 0
_DOWN = 1
_LEFT = 2
_UP = 3

RIGHT = Direction(_RIGHT)
DOWN = Direction(_DOWN)
LEFT = Direction(_LEFT)
UP = Direction(_UP)

class Cache():
	def __init__(self):
		self.active = set()
		self.results = dict()
	
	def __contains__(self, key):
		return key in self.active or key in self.results
	
	def open(self, key):
		#print(f"open: {key}")
		assert key not in self
		self.active.add(key)

	def close(self, key, value):
		#print(f"close: {key}")
		assert key not in self.results
		self.results[key] = value
		if key in self.active:
			self.active.remove(key)
	
	def __setitem__(self, key, value):
		assert key not in self
		self.results[key] = value
	
	def __getitem__(self, key):
		assert key in self
		if key in self.active:
			return None

		return self.results[key]

def is_valid_x(grid, x):
	return x >= 0 and x < len(grid[0])

def is_valid_y(grid, y):
	return y >= 0 and y < len(grid)

def list_options(grid, start):
	out = []
	dir, y, x = start
	if dir == RIGHT or dir == LEFT:
		heat = 0
		if dir == RIGHT:
			r = range(x+1, x+4)
		else:
			r = range(x-1, x-4, -1)
		for x in r:
			if is_valid_x(grid, x):
				heat += grid[y][x]
				out.append((heat, (UP, y, x)))
				out.append((heat, (DOWN, y, x)))
	else:
		heat = 0
		if dir == DOWN:
			r = range(y+1, y+4)
		else:
			r = range(y-1, y-4, -1)
		for y in r:
			if is_valid_y(grid, y):
				heat += grid[y][x]
				out.append((heat, (RIGHT, y, x)))
				out.append((heat, (LEFT, y, x)))
	return out				


def is_finish(grid, loc):
	_, y, x = loc
	return y == len(grid) - 1 and x == len(grid[0]) - 1

def find_low_heat_unrestricted_paths(grid):
	to_process = []
	low_heats = dict()
	heapq.heappush(to_process, (0, (len(grid) - 1, len(grid[0]) - 1)))
	while to_process:
		heat, loc = heapq.heappop(to_process)
		y, x = loc
		if loc in low_heats:
			assert low_heats[loc] <= heat
			continue
		low_heats[loc] = heat
		heat += grid[y][x]
		neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
		for neighbor in neighbors:
			n_y, n_x = neighbor
			if not (is_valid_x(grid, n_x) and is_valid_y(grid, n_y)):
				continue
			heapq.heappush(to_process, (heat, (n_y, n_x)))
	return low_heats


def low_heat_ultra(grid, printing=False, cache=None):
	if cache is None:
		cache = Cache()
	y_max = len(grid) - 1
	x_max = len(grid[0]) - 1

	to_process = []
	low_heats = dict()
	heapq.heappush(to_process, (0, (DOWN, y_max, x_max)))
	heapq.heappush(to_process, (0, (RIGHT, y_max, x_max)))
	heapq.heappush(to_process, (0, (LEFT, y_max, x_max)))
	heapq.heappush(to_process, (0, (UP, y_max, x_max)))
	while to_process:
		heat, start = heapq.heappop(to_process)
		dir, y, x = start
		if start in low_heats:
			assert low_heats[start] <= heat
			continue
		low_heats[start] = heat
		heat += grid[y][x]
		neighbors = []
		if dir == RIGHT or dir == LEFT:
			heat_up = heat
			heat_down = heat
			for i in range(1,11):
				if is_valid_y(grid, y + i):
					if i > 3:
						neighbors.append((heat_up, (UP, y+i, x)))
					heat_up += grid[y+i][x]
				if is_valid_y(grid, y - i):
					if i > 3:
						neighbors.append((heat_down, (DOWN, y-i, x)))
					heat_down += grid[y-i][x]
		else:
			heat_right = heat
			heat_left = heat
			for i in range(1,11):
				if is_valid_x(grid, x + i):
					if i > 3:
						neighbors.append((heat_left, (LEFT, y, x+i)))
					heat_left += grid[y][x+i]
				if is_valid_x(grid, x - i):
					if i > 3:
						neighbors.append((heat_right, (RIGHT, y, x-i)))
					heat_right += grid[y][x-i]

		for neighbor in neighbors:
			heapq.heappush(to_process, neighbor)

	r_v = low_heats[(RIGHT, 0, 0)]
	d_v = low_heats[(DOWN, 0, 0)]

	if r_v is not None and d_v is not None:
		return min(r_v, d_v)
	else:
		return r_v or d_v


def low_heat(grid, printing=False, cache=None):
	if cache is None:
		cache = Cache()
	y_max = len(grid) - 1
	x_max = len(grid[0]) - 1

	heat_mins = find_low_heat_unrestricted_paths(grid)

	to_process = []
	low_heats = dict()
	#import pdb; pdb.set_trace()
	heapq.heappush(to_process, (0, (DOWN, y_max, x_max)))
	heapq.heappush(to_process, (0, (RIGHT, y_max, x_max)))
	heapq.heappush(to_process, (0, (LEFT, y_max, x_max)))
	heapq.heappush(to_process, (0, (UP, y_max, x_max)))
	while to_process:
		heat, start = heapq.heappop(to_process)
		dir, y, x = start
		if start in low_heats:
			assert low_heats[start] <= heat
			continue
		low_heats[start] = heat
		heat += grid[y][x]
		neighbors = []
		if dir == RIGHT or dir == LEFT:
			heat_up = heat
			heat_down = heat
			for i in range(1,4):
				if is_valid_y(grid, y + i):
					neighbors.append((heat_up, (UP, y+i, x)))
					heat_up += grid[y+i][x]
				if is_valid_y(grid, y - i):
					neighbors.append((heat_down, (DOWN, y-i, x)))
					heat_down += grid[y-i][x]
		else:
			heat_right = heat
			heat_left = heat
			for i in range(1,4):
				if is_valid_x(grid, x + i):
					neighbors.append((heat_left, (LEFT, y, x+i)))
					heat_left += grid[y][x+i]
				if is_valid_x(grid, x - i):
					neighbors.append((heat_right, (RIGHT, y, x-i)))
					heat_right += grid[y][x-i]

		for neighbor in neighbors:
			heapq.heappush(to_process, neighbor)

	r_v = low_heats[(RIGHT, 0, 0)]
	d_v = low_heats[(DOWN, 0, 0)]

	if r_v is not None and d_v is not None:
		return min(r_v, d_v)
	else:
		return r_v or d_v

def find_best_and_cache(grid, cache, start, max_heat=None, printing=False, lookup_best=None, heat_mins=None):
	if is_finish(grid, start):
		cache.close(start, 0)
		return 0

	if max_heat is None:
		max_heat = find_best_immediate(grid, cache, start, printing)
		if max_heat is None:
			cache.close(start, None)
			return None
	
	if printing:
		print(start)
	
	best = find_best(grid, cache, start, max_heat, printing, lookup_best=lookup_best, heat_mins=heat_mins)
	cache.close(start, best)
	return best

def find_best_immediate(grid, cache, start, printing=False):
	options = list_options(grid, start)
	cached_options = [(heat, option) for heat, option in options if option in cache]
	if len(cached_options) == 0:
		assert len(options) == 0
		return None
	
	best = None
	for option in cached_options:
		if cache[option[1]] is not None:
			heat = option[0] + cache[option[1]]
			if best is None or heat < best:
				best = heat
	
	return best

def find_best(grid, cache, start, max_heat, printing, path=None, lookup_best=None, heat_mins=None):
	if path is None:
		path = []

	dir, y, x = start

	assert heat_mins is not None
	if max_heat < heat_mins[(y, x)]:
		return None
	
	if lookup_best is not None and max_heat <= lookup_best:
		return None

	options = list_options(grid, start)
	best = None
	for heat, option in options:
		if option in cache:
			recursive_best = cache[option]
		elif option in path:
			recursive_best = None
		else:
			recursive_path = path.copy()
			recursive_path.append(start)
			recursive_best = find_best(grid, cache, option, max_heat - heat, printing, path=recursive_path, lookup_best=lookup_best, heat_mins=heat_mins)

		if recursive_best is None:
			continue
		option_heat = heat + recursive_best
		if best is None or option_heat < best:
			best = option_heat
	return best


def main(grid, printing=False):#
	out_a = low_heat(grid, printing)
	out_b = low_heat_ultra(grid, printing)
	
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
