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
        out.append([int(c) for c in line])

    return out

def max_joltage_2(bank):
	current_best = 0
	current_best_first = 0

	for n in bank:
		if current_best_first and 10 * current_best_first + n > current_best:
			current_best = 10 * current_best_first + n
		if n > current_best_first:
			current_best_first = n
	
	return current_best

def max_joltage_12(bank):
	current_bests = [0] * 12
	for n in bank:
		for i in range(10, -1, -1):
			current_bests[i+1] = max(current_bests[i+1], 10 * current_bests[i] + n)

		current_bests[0] = max(n, current_bests[0])
	return current_bests[11]


def main(input, printing=False):
	out_a = sum([max_joltage_2(bank) for bank in input])
	out_b = sum([max_joltage_12(bank) for bank in input])

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
