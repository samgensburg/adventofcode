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


START = 'S'
GARDEN = '.'
WALL = '#'

def parse_file(file):
	grid = []
	for line in file:
		line = line.strip()
		grid.append(line)

	return grid

STEP_COUNT = 64
OFFSETS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def find_start(grid):
	for y in range(len(grid)):
		if START in grid[y]:
			return y, grid[y].find(START)

def print_grid_with_visit_options(grid, visit_options):
	for y in range(len(grid)):
		line = grid[y]
		for y_v, x_v in visit_options:
			if y_v == y:
				line = line[:x_v] + 'O' + line[x_v + 1:]
		print(line)
	print()


def distances_from_start(grid, start):
	queue = Queue()
	queue.put((0, start))

	distance_map = {}
	reverse_distance_map = defaultdict(set)

	y_max = len(grid)
	x_max = len(grid[0])

	while queue.qsize():
		distance, loc = queue.get()
		if loc in distance_map:
			continue

		y, x = loc
		if y < 0 or x < 0 or y >= y_max or x >= x_max:
			continue

		if grid[y][x] == WALL:
			continue

		distance_map[loc] = distance
		reverse_distance_map[distance].add(loc)
		for y_offset, x_offset in OFFSETS:
			queue.put((distance + 1, (y + y_offset, x + x_offset)))

	return reverse_distance_map

FULL_STEP_COUNT = 26501365
#FULL_STEP_COUNT = 50

def main(grid, printing=False):
	start = find_start(grid)

	reverse_distance_map = distances_from_start(grid, start)

	out_a = 0
	for i in range(0, 66, 2):
		out_a += len(reverse_distance_map[i])

	out_b = extended_walk(grid, FULL_STEP_COUNT)

	return out_a, out_b


def extended_walk(grid, dist):
	grid_dim = len(grid)
	midpoint = (grid_dim - 1) // 2
	grid[midpoint] = grid[midpoint].replace(START, GARDEN)

	reverse_distance_map = distances_from_start(grid, (midpoint, midpoint))
	even_total = 0
	for i in range(0, 200, 2):
		even_total += len(reverse_distance_map[i])

	odd_total = 0
	for i in range(1, 201, 2):
		odd_total += len(reverse_distance_map[i])

	reverse_distance_map_from_right = distances_from_start(grid, (midpoint, grid_dim - 1))
	reverse_distance_map_from_left = distances_from_start(grid, (midpoint, 0))
	reverse_distance_map_from_bottom = distances_from_start(grid, (grid_dim - 1, midpoint))
	reverse_distance_map_from_top = distances_from_start(grid, (0, midpoint))

	reverse_distance_map_from_bottom_right = distances_from_start(grid, (grid_dim-1, grid_dim - 1))
	reverse_distance_map_from_bottom_left = distances_from_start(grid, (grid_dim-1, 0))
	reverse_distance_map_from_top_right = distances_from_start(grid, (0, 0))
	reverse_distance_map_from_top_left = distances_from_start(grid, (0, grid_dim - 1))


	grid_lengths_traversed = (dist - midpoint * 2) // grid_dim

	even_grid_count = (grid_lengths_traversed + 1) ** 2
	odd_grid_count = grid_lengths_traversed ** 2

	if dist % 2:
		even_total, odd_total = odd_total, even_total

	if grid_lengths_traversed % 2:
		even_total, odd_total = odd_total, even_total


	grids_to_far_corners = grid_lengths_traversed + 1
	grids_to_ultra_far_corners = grids_to_far_corners + 1 

	distance_to_far_midpoint = grid_lengths_traversed * grid_dim + midpoint + 1
	distance_to_ultra_far_midpoint = distance_to_far_midpoint + grid_dim
	distance_to_far_corner = grid_lengths_traversed * grid_dim + 1
	distance_to_ultra_far_corner = distance_to_far_corner + grid_dim

	out = even_grid_count * even_total + odd_grid_count * odd_total


	far_left = sum([len(reverse_distance_map_from_right[i]) for i in range(dist - distance_to_far_midpoint, -1, -2)])
	ultra_far_left = sum([len(reverse_distance_map_from_right[i]) for i in range(dist - distance_to_ultra_far_midpoint, -1, -2)])
	far_right = sum([len(reverse_distance_map_from_left[i]) for i in range(dist - distance_to_far_midpoint, -1, -2)])
	ultra_far_right = sum([len(reverse_distance_map_from_left[i]) for i in range(dist - distance_to_ultra_far_midpoint, -1, -2)])
	far_top = sum([len(reverse_distance_map_from_bottom[i]) for i in range(dist - distance_to_far_midpoint, -1, -2)])
	ultra_far_top = sum([len(reverse_distance_map_from_bottom[i]) for i in range(dist - distance_to_ultra_far_midpoint, -1, -2)])
	far_bottom = sum([len(reverse_distance_map_from_top[i]) for i in range(dist - distance_to_far_midpoint, -1, -2)])
	ultra_far_bottom = sum([len(reverse_distance_map_from_top[i]) for i in range(dist - distance_to_ultra_far_midpoint, -1, -2)])

	out += far_left + ultra_far_left
	out += far_right + ultra_far_right
	out += far_top + ultra_far_top
	out += far_bottom + ultra_far_bottom

	far_top_right = sum([len(reverse_distance_map_from_bottom_left[i]) for i in range(dist - distance_to_far_corner, -1, -2)])
	ultra_far_top_right = sum([len(reverse_distance_map_from_bottom_left[i]) for i in range(dist - distance_to_ultra_far_corner, -1, -2)])
	far_bottom_left = sum([len(reverse_distance_map_from_top_right[i]) for i in range(dist - distance_to_far_corner, -1, -2)])
	ultra_far_bottom_left = sum([len(reverse_distance_map_from_top_right[i]) for i in range(dist - distance_to_ultra_far_corner, -1, -2)])
	far_top_left = sum([len(reverse_distance_map_from_bottom_right[i]) for i in range(dist - distance_to_far_corner, -1, -2)])
	ultra_far_top_left = sum([len(reverse_distance_map_from_bottom_right[i]) for i in range(dist - distance_to_ultra_far_corner, -1, -2)])
	far_bottom_right = sum([len(reverse_distance_map_from_top_left[i]) for i in range(dist - distance_to_far_corner, -1, -2)])
	ultra_far_bottom_right = sum([len(reverse_distance_map_from_top_left[i]) for i in range(dist - distance_to_ultra_far_corner, -1, -2)])

	out += (grids_to_far_corners - 1) * (far_top_right + far_top_left + far_bottom_right + far_bottom_left)
	out += (grids_to_ultra_far_corners - 1) * (ultra_far_top_right + ultra_far_top_left + ultra_far_bottom_right + ultra_far_bottom_left)

	return out


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
