from collections import defaultdict
from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

DIM_MAX = 4000000

EMPTY = '.'
SAND = 'o'
WALL = '#'

def distance(sensor, beacon):
	s_x, s_y = sensor
	b_x, b_y = beacon
	return abs(s_x - b_x) + abs(s_y - b_y)

def process_input(lines):
	sensors = []
	for line in lines:
		match = re.match(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', line)
		assert match
		sensor = (int(match.group(1)), int(match.group(2)))
		beacon = (int(match.group(3)), int(match.group(4)))
		sensors.append((sensor, distance(sensor, beacon), beacon))

	beacons = set([item[2] for item in sensors])

	return get_map(sensors), beacons

def get_map(sensors):
	rows = defaultdict(list)
	for sensor, d, _ in sensors:
		sensor_x, sensor_y = sensor
		for y in range(sensor_y - d, sensor_y + d + 1):
			if y < 0 or y > DIM_MAX:
				continue
			if y % 10000 == 0:
				print(y)
			d_remainder = d - abs(y - sensor_y)
			rows[y].append((sensor_x - d_remainder, sensor_x + d_remainder))
	return rows

def solve_old(data):
	count = 0
	y = 2000000
	beacons = set([item[2] for item in data])
	for x in range(-4000000, 8000000):
		if x % 100000 == 0:
			print(x)
		loc = (x, y)
		if loc in beacons:
			continue

		for sensor, d, _ in data:
			if distance (sensor, loc) <= d:
				count += 1
				break
	return count

def solve_a(map, beacons):
	row = map[2000000]
	sorted_row = sorted(row, key=lambda p: p[0])
	count = 0
	working_min, working_max = sorted_row[0]
	for current_min, current_max in sorted_row[1:]:
		if current_min > working_max:
			count += working_max - working_min + 1
			working_min, working_max = current_min, current_max
		else:
			working_max = max(current_max, working_max)
	count += working_max - working_min + 1

	for x, y in beacons:
		if y == 2000000:
			count -= 1
	return count

def solve_b(map):
	for y in range(DIM_MAX + 1):
		row = map[y]
		sorted_row = sorted(row, key=lambda p: p[0])
		working_min, working_max = sorted_row[0]
		for current_min, current_max in sorted_row[1:]:
			if current_min > working_max:
				if working_max > DIM_MAX:
					break
				return (working_max + 1) * DIM_MAX + y
			else:
				working_max = max(current_max, working_max)

def main():
	with open(DATA_FILE, 'r') as file:
		lines = file.read().strip().split('\n')

	map, beacons = process_input(lines)
	return solve_a(map, beacons), solve_b(map)


print(main())
