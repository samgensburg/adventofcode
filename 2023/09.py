import argparse
from collections import defaultdict
from functools import reduce
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'


def parse_file(file):
	lines = []
	for line in file:
		line = [int(n) for n in line.strip().split()]
		lines.append(line)

	return lines


def predict_next_value(line):
	is_constant = True
	for i in range(len(line)):
		is_constant = is_constant and line[0] == line[i]
	
	if is_constant:
		return line[i]
	
	diffs = [line[i+1] - line[i] for i in range(len(line) - 1)]
	return predict_next_value(diffs) + line[-1]


def predict_previous_value(line):
	is_constant = True
	for i in range(len(line)):
		is_constant = is_constant and line[0] == line[i]
	
	if is_constant:
		return line[i]
	
	diffs = [line[i+1] - line[i] for i in range(len(line) - 1)]
	return line[0] - predict_previous_value(diffs) 


def main(lines):
	values_a = [predict_next_value(line) for line in lines]
	sum_a = sum(values_a)
	values_b = [predict_previous_value(line) for line in lines]
	sum_b = sum(values_b)

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
