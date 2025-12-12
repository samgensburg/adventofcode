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
    out = [[c for c in line.strip()] for line in file]

    return out

def main(input, printing=False):
	out_a = 0
	out_b = 0

	dim_y = len(input)
	dim_x = len(input[0])

	for i in range(dim_y):
		for j in range(dim_x):
			if input[i][j] == EMPTY:
				continue

			locs = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1),
					(i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
			
			count = 0
			for y, x in locs:
				if y >= dim_y or y < 0 or x >= dim_x or x < 0:
					continue
				if input[y][x] == ROLL:
					count += 1
			if count < 4:
				out_a += 1

	while True:
		round_rolls = 0
		for i in range(dim_y):
			for j in range(dim_x):
				if input[i][j] == EMPTY:
					continue

				locs = [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1),
						(i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]
				
				count = 0
				for y, x in locs:
					if y >= dim_y or y < 0 or x >= dim_x or x < 0:
						continue
					if input[y][x] == ROLL:
						count += 1
				if count < 4:
					round_rolls += 1
					input[i][j] = EMPTY
		if round_rolls == 0:
			break

		out_b += round_rolls

	

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
