import argparse
from collections import defaultdict
import math
from pathlib import Path
import re
from typing import Any

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'


UP_DOWN = '|'
LEFT_RIGHT = '-'
UP_RIGHT = 'L'
UP_LEFT = 'J'
DOWN_LEFT = '7'
DOWN_RIGHT = 'F'
GROUND = '.'
START = 'S'

def is_left(d):
	return d in [LEFT_RIGHT, DOWN_LEFT, UP_LEFT]

def is_right(d):
	return d in [LEFT_RIGHT, DOWN_RIGHT, UP_RIGHT]

def is_down(d):
	return d in [UP_DOWN, DOWN_LEFT, DOWN_RIGHT]

def is_up(d):
	return d in [UP_DOWN, UP_RIGHT, UP_LEFT]

def left(loc):
	y, x = loc
	return y, x-1

def right(loc):
	y, x = loc
	return y, x+1

def up(loc):
	y, x = loc
	return y-1, x

def down(loc):
	y, x = loc
	return y+1, x

class Map():
	def __init__(self, map):
		self.map = map
	
	def __getitem__(self, loc):
		y, x = loc
		return self.map[y][x]

	def start_loc(self):
		for y, line in enumerate(self.map):
			if START in line:
				x = line.find(START)
				return y, x
		assert False

def parse_file(file):
	map = []
	for i, line in enumerate(file):
		line = line.strip()
		map.append(line)

	map = Map(map)

	return map
		
def nexts_after_start(start, map):
	out = []
	if is_right(map[left(start)]):
		out.append(left(start))
	if is_left(map[right(start)]):
		out.append(right(start))
	if is_up(map[down(start)]):
		out.append(down(start))
	if is_down(map[up(start)]):
		out.append(up(start))
	assert len(out) == 2
	if is_up(map[down(start)]) and is_down(map[up(start)]):
		out.append(UP_DOWN)
	else:
		assert False # I just don't feel like typing out the other cases
	return out

def next_after_previous(current, previous, map):
	c = map[current]
	options = []
	if is_up(c):
		options.append(up(current))
	if is_down(c):
		options.append(down(current))
	if is_right(c):
		options.append(right(current))
	if is_left(c):
		options.append(left(current))
	for option in options:
		if option != previous:
			return option
		
	assert False

def is_inside(y, x, visited):
	loc = (y, x)
	if loc in visited:
		return False
	
	inside = False
	last_corner = None
	for y_i in range(y):
		loc_i = (y_i, x)
		if loc_i not in visited:
			continue
		val = visited[loc_i]
		
		if loc_i not in visited:
			continue
		if val == LEFT_RIGHT:
			inside = not inside
		elif val == UP_DOWN:
			assert last_corner != None
		elif last_corner is None:
			last_corner = val
		else:
			together = set([val, last_corner])
			last_corner = None
			assert len(together) == 2
			if together == set([UP_LEFT, DOWN_LEFT]):
				pass
			elif together == set([UP_RIGHT, DOWN_RIGHT]):
				pass
			elif together == set([UP_LEFT, DOWN_RIGHT]):
				inside = not inside
			elif together == set([UP_RIGHT, DOWN_LEFT]):
				inside = not inside
			else:
				assert False
	return inside

def main(map):
	start = map.start_loc()
	tracker_a, tracker_b, start_shape = nexts_after_start(start, map)
	previous_a = previous_b = start
	count_a = 1
	visited = dict()
	visited[start] = start_shape
	visited[tracker_a] = map[tracker_a]
	visited[tracker_b] = map[tracker_b]

	while tracker_a != tracker_b:
		tracker_a, previous_a = next_after_previous(tracker_a, previous_a, map), tracker_a
		tracker_b, previous_b = next_after_previous(tracker_b, previous_b, map), tracker_b

		visited[tracker_a] = map[tracker_a]
		visited[tracker_b] = map[tracker_b]

		count_a += 1
	
	count_b = 0

	for y in range(len(map.map)):
		for x in range(len(map.map[0])):
			if is_inside(y, x, visited):
				count_b += 1

	return count_a, count_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data))

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

wrapper(args)
