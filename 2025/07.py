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
EMPTY = '.'
SPLITTER = '^'

def parse_file(file):
	out = []
	for line in file:
		line = line.strip()
		out.append(line)

	return out

def main(input, printing=False):
	out_a = 0
	out_b = 0

	line = input[0]
	for i in range(len(line)):
		if line[i] == START:
			next = [i]
			next_counts = defaultdict(int)
			next_counts[i] += 1

	for line in input[1:]:
		current = next
		next = set()
		current_counts = next_counts
		next_counts = defaultdict(int)

		for i in current:
			if line[i] == EMPTY:
				next.add(i)
				next_counts[i] += current_counts[i]
			else:
				assert line[i] == SPLITTER
				out_a += 1
				next.add(i-1)
				next.add(i+1)
				next_counts[i-1] += current_counts[i]
				next_counts[i+1] += current_counts[i]

	for n in next_counts:
		out_b += next_counts[n]

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
