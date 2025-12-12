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

EMPTY = '.'
ROLL = '@'

def parse_file(file):
	state = 0
	fresh_ranges = []
	inventory = []
	for line in file:
		line = line.strip()
		if state == 0:
			if not line:
				state = 1
			else:
				assert re.match(r"^\d+-\d+$", line)
				parts = line.split('-')
				assert len(parts) == 2
				fresh_ranges.append((int(parts[0]), int(parts[1])))
		else:
			inventory.append(int(line))
	
	return fresh_ranges, inventory

def consolidate(ranges):
	out = []
	for low, high in ranges:
		found = False
		for i in range(len(out)):
			low_i, high_i = out[i]
			if low > high_i or high < low_i:
				continue

			found = True
			out[i] = min(low, low_i), max(high, high_i)
			break

		if found:
			continue

		out.append((low, high))
	return out

def main(input, printing=False):
	fresh_ranges, inventory = input
	out_a = 0
	out_b = 0

	for item in inventory:
		for low, high in fresh_ranges:
			if item >= low and item <= high:
				out_a += 1
				break

	for i in range(50):
		fresh_ranges = consolidate(fresh_ranges)

	for low, high in fresh_ranges:
		out_b += high - low + 1

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
