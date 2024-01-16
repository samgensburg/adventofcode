import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

GALAXY = '#'

class Galaxy_Map():
	def __init__(self):
		self.galaxy_list = []
		self.y_values = set()
		self.x_values = set()

	def add_line(self, y, line):
		for x, c in enumerate(line):
			if c == GALAXY:
				self.galaxy_list.append((y, x))
				self.y_values.add(y)
				self.x_values.add(x)

	def clone(self):
		out = Galaxy_Map()
		out.galaxy_list = self.galaxy_list.copy()
		out.y_values = self.y_values.copy()
		out.x_values = self.x_values.copy()
		return out

	def expand(self, super=False):
		expansion_size = 999999 if super else 1
		y_values = list(self.y_values)
		x_values = list(self.x_values)
		max_y = max(y_values)
		max_x = max(x_values)

		y_increments = []
		x_increments = []

		for y in range(1, max_y):
			if y not in self.y_values:
				y_increments.append(y)

		for x in range(1, max_x):
			if x not in self.x_values:
				x_increments.append(x)

		new_galaxy_list = []
		for y_g, x_g in self.galaxy_list:
			y_increments_local = [y_i for y_i in y_increments if y_i < y_g]
			y_g += len(y_increments_local) * expansion_size
			x_increments_local = [x_i for x_i in x_increments if x_i < x_g]
			x_g += len(x_increments_local) * expansion_size
			new_galaxy_list.append((y_g, x_g))

		self.galaxy_list = new_galaxy_list
	
	def super_expand(self):
		self.expand(super=True)

	def list(self):
		return self.galaxy_list


def galaxy_distance(galaxy_1, galaxy_2):
	y_1, x_1 = galaxy_1
	y_2, x_2 = galaxy_2
	return abs(y_1 - y_2) + abs(x_1 - x_2)

def parse_file(file):
	galaxy_map = Galaxy_Map()
	for y, line in enumerate(file):
		line = line.strip()
		galaxy_map.add_line(y, line)
	
	return galaxy_map

def sum_distances(galaxy_list):
	out = 0
	for i, galaxy_1 in enumerate(galaxy_list):
		for galaxy_2 in galaxy_list[i+1:]:
			out += galaxy_distance(galaxy_1, galaxy_2)
	return out


def main(galaxy_map):
	galaxy_map_b = galaxy_map.clone()
	galaxy_map.expand()
	galaxy_list = galaxy_map.list()
	sum_a = sum_distances(galaxy_list)

	galaxy_map_b.super_expand()
	sum_b = sum_distances(galaxy_map_b.list())

	return sum_a, sum_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data))

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

wrapper(args)
