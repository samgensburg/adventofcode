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

class Brick_Map():
	def __init__(self, bricks):
		self.bricks = bricks

		self.columns = defaultdict(set)
		for i, brick in enumerate(bricks):
			for x, y, _ in brick.locs_below():
				self.columns[(x, y)].add(i)
	
	def drop_recursive(self):
		priority_queue = [(brick.z_s, i) for i, brick in enumerate(self.bricks)]
		heapq.heapify(priority_queue)

		while priority_queue:
			z, i = heapq.heappop(priority_queue)
			while self.try_drop_by_index(i):
				pass
	
	def try_drop_by_index(self, i):
		#import pdb ; pdb.set_trace()
		if self.bricks[i].z_s <= 1:
			return False
		for loc in self.bricks[i].locs_below():
			if loc in self:
				return False
		self.bricks[i].drop_one()
		return True
		
	
	def __contains__(self, loc):
		for brick in self.bricks:
			if loc in brick:
				return True
		return False
	
	def count_non_bearing(self):
		bearing_bricks = set()
		#import pdb; pdb.set_trace()
		for floating_brick in self.bricks:
			print(floating_brick.x_s, floating_brick.y_s, floating_brick.z_s)
			if floating_brick.z_s == 1:
				continue
			bricks_below = set()
			for loc in floating_brick.locs_below():
				brick_id = self.find_brick_id_from_loc(loc)
				if brick_id is not None:
					bricks_below.add(brick_id)
			assert len(bricks_below)
			floating_brick.bricks_below = bricks_below
			if len(bricks_below) == 1:
				bearing_bricks.add(list(bricks_below)[0])

		return len(self.bricks) - len(bearing_bricks)
	
	def find_brick_id_from_loc(self, loc):
		for i, brick in enumerate(self.bricks):
			if loc in brick:
				return i
		return None
	
	def count_falling_total(self):
		return sum([self.count_falling_for_brick(i, brick) for i, brick in enumerate(self.bricks)])
	
	def count_falling_for_brick(self, i, missing_brick):
		bricks_removed = set([i])
		something_added = True
		while something_added:
			something_added = False
			for j, brick in enumerate(self.bricks):
				if j in bricks_removed:
					continue
				if brick.bricks_below is None:
					assert brick.z_s == 1
					continue
				if set(brick.bricks_below).issubset(bricks_removed):
					bricks_removed.add(j)
					something_added = True

		return len(bricks_removed) - 1


class Brick():
	def __init__(self, brick) -> None:
		start, end = brick
		x_s, y_s, z_s = start
		x_e, y_e, z_e = end
		count_equal = 1 if x_s == x_e else 0
		count_equal += 1 if y_s == y_e else 0
		count_equal += 1 if z_s == z_e else 0
		assert count_equal >= 2

		self.x_s = min(x_s, x_e)
		self.y_s = min(y_s, y_e)
		self.z_s = min(z_s, z_e)
		self.x_e = max(x_s, x_e)
		self.y_e = max(y_s, y_e)
		self.z_e = max(z_s, z_e)

		self.below_cache = None
		self.bricks_below = None

	def locs_below(self):
		if self.below_cache:
			return self.below_cache
		if self.z_e == self.z_s:
			if self.y_e == self.y_s:
				self.below_cache = [(x, self.y_s, self.z_s - 1) for x in range(self.x_s, self.x_e + 1)]
			else:
				self.below_cache = [(self.x_s, y, self.z_s - 1) for y in range(self.y_s, self.y_e + 1)]
		else:
			assert self.x_s == self.x_e and self.y_s == self.y_e and self.z_s < self.z_e
			self.below_cache = [(self.x_s, self.y_s, self.z_s - 1)]
		return self.below_cache
	
	def __contains__(self, loc):
		x, y, z = loc
		return x >= self.x_s and y >= self.y_s and z >= self.z_s and x <= self.x_e and y <= self.y_e and z <= self.z_e

	def drop_one(self):
		self.below_cache = None
		print(self.x_s, self.y_s, self.z_s)
		self.z_s -= 1
		self.z_e -= 1

def parse_file(file):
	bricks = []
	for line in file:
		line = line.strip()
		match = re.match(r'(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)', line)
		assert match
		start = int(match.group(1)), int(match.group(2)), int(match.group(3))
		end = int(match.group(4)), int(match.group(5)), int(match.group(6))
		bricks.append((start, end))

	return Brick_Map([Brick(brick) for brick in bricks])

def main(brick_map, printing=False):
	brick_map.drop_recursive()
	out_a = brick_map.count_non_bearing()
	out_b = brick_map.count_falling_total()

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
