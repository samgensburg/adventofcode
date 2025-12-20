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

def parse_file(file):
	out = []
	for line in file:
		line = line.strip()
		coords = [int(s) for s in line.split(',')]
		coords = (coords[0], coords[1])
		out.append(coords)

	return out

def sgn(n):
	if n == 0:
		return 0
	
	return 1 if n > 0 else -1

def make_boundary_set(input):
	out = set()
	for i in range(len(input)):
		start = input[i]
		end = input[i+1] if i+1 < len(input) else input[0]
		x1, y1 = start
		x2, y2 = end

		if x1 == x2:
			for y in range(y1, y2, sgn(y2 - y1)):
				out.add((x1, y))
		else:
			assert y1 == y2
			for x in range(x1, x2, sgn(x2 - x1)):
				out.add((x, y1))
	
	return out


def is_interior(x1, y1, x2, y2, input_set, boundary_set):
	assert (x1, y1) in input_set
	assert (x2, y2) in input_set
	
	if y1 != y2:
		x2_sgn = sgn(x1 - x2)
		x1_sgn = sgn(x2 - x1)
		for y in range(y1, y2, sgn(y2 - y1)):
			if y == y1:
				continue
			if (x2 + x2_sgn, y) in boundary_set:
				return False
			if (x1 + x1_sgn, y) in boundary_set:
				return False

	if x1 != x2:
		y2_sgn = sgn(y1 - y2)
		y1_sgn = sgn(y2 - y1)
		for x in range(x1, x2, sgn(x2 - x1)):
			if x == x1:
				continue
			if (x, y2 + y2_sgn) in boundary_set:
				return False
			if (x, y1 + y1_sgn) in boundary_set:
				return False
	
	return True


def main(input, printing=False):
	out_a = 0
	out_b = 0

	input_set = set(input)
	boundary_set = make_boundary_set(input)

	for i in range(len(input)):
		x1, y1 = input[i]
		for j in range(i + 1, len(input)):
			x2, y2 = input[j]
			if printing:
				print(i, j)
			current = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
			out_a = max(current, out_a)

			#import pdb; pdb.set_trace()
			if current > out_b and is_interior(x1, y1, x2, y2, input_set, boundary_set):
				out_b = current


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
