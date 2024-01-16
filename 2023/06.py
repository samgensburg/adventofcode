import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

LAYERS = 8


def parse_file(file):
	n_races = 4
	pairs = [(0, 0) for i in range(n_races)]
	out_b = [0, 0]
	for i, line in enumerate(file):
		line = line.strip()
		if i == 0:
			assert line[:5] == 'Time:'
			line = line[5:]
		else:
			assert i == 1
			assert line[:9] == 'Distance:'
			line = line[9:]
		line = line.strip()
		line_b = line
		for j in range(10):
			line = line.replace('  ', ' ')
		line_a = line.split()
		for j, n in enumerate(line_a):
			n = int(n)
			pair = pairs[j]
			if i == 0:
				pair = (n, pair[1])
			else:
				pair = (pair[0], n)

			pairs[j] = pair
		line_b = line_b.replace(' ', '')
		out_b[i] = int(line_b)

	return pairs, out_b


def main(file):
	pairs, pair_b = parse_file(file)
	product_a = 1
	for time, distance in pairs:
		count = 0
		for hold_time in range(time):
			distance_traveled = (time - hold_time) * hold_time
			if distance_traveled > distance:
				count += 1
		product_a *= count

	t = pair_b[0]
	dt = pair_b[1]
	low = math.ceil((t - math.sqrt(t**2 - 4 * dt)) / 2)
	high = math.floor((t + math.sqrt(t**2 - 4 * dt)) / 2)
	out_b = high - low + 1
	
	return product_a, out_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		print(main(file))

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

wrapper(args)
