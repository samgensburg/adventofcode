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
	grid = []
	grid_b = []
	for line in file:
		if line[-1] == '\n':
			line = line[:-1]
		grid_b.append(line)
		line = line.strip()
		for i in range(10):
			line = line.replace('  ', ' ')
		
		parts = line.split()
		if parts[0].isdigit():
			grid.append([int(part) for part in parts])
		else:
			operations = parts

	return grid, operations, grid_b

def main(input, printing=False):
	grid, operations, grid_b = input
	out_a = 0
	out_b = 0

	for column in range(len(grid[0])):
		operation = operations[column]
		if operation == '+':
			value = 0
			for row in range(len(grid)):
				value += grid[row][column]
		else:
			assert operation == '*'
			value = 1
			for row in range(len(grid)):
				value *= grid[row][column]
		if printing:
			print(value)
		out_a += value

	print(grid_b)
	num_list = []
	last_row = len(grid_b) - 1
	for column in range(len(grid_b[0]) - 1, -1, -1):
		chars = [grid_b[row][column] for row in range(last_row)]
		text = ''.join(chars).strip()
		if len(text):
			num = int(text)
		else:
			assert len(num_list) == 0
			continue

		num_list.append(num)
		operator = grid_b[last_row][column]
		if operator == ' ':
			continue
		
		if operator == '+':
			out_b += sum(num_list)

		else:
			assert operator == '*'
			out_b += math.prod(num_list)

		num_list = []


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
