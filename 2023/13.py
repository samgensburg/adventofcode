import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

def parse_file(file):
	patterns = []
	pattern = []
	for i, line in enumerate(file):
		line = line.strip()
		if len(line):
			pattern.append(line)
		else:
			patterns.append(pattern)
			pattern = []
	patterns.append(pattern)

	return patterns


def score_a(pattern):
	row = find_row_a(pattern)
	column = find_column_a(pattern)

	assert row == -1 or column == -1
	if row == -1 and column == -1:
		pretty_print(pattern)
		assert False

	if row != -1:
		return 100 * row
	return column


def score_b(pattern):
	row = find_row_b(pattern)
	column = find_column_b(pattern)

	assert row == -1 or column == -1
	if row == -1 and column == -1:
		pretty_print(pattern)
		assert False

	if row != -1:
		return 100 * row
	return column


def pretty_print(pattern):
	for line in pattern:
		print(line)

def find_row_a(pattern):
	row_count = len(pattern)
	for reflection_row in range(1, row_count):
		reflection = True
		for i in range(row_count):
			if i < reflection_row:
				reflected_i = reflection_row * 2 - i - 1
				if reflected_i < row_count:
					if pattern[i] != pattern[reflected_i]:
						reflection = False
						break
			else:
				reflected_i = reflection_row * 2 - 1 - i
				if reflected_i >= 0:
					if pattern[i] != pattern[reflected_i]:
						reflection = False
						break
		if reflection:
			return reflection_row
	return -1
		
	
def find_column_a(pattern):
	column_count = len(pattern[0])
	for reflection_column in range(1, column_count):
		reflection = True
		for i in range(column_count):
			if i < reflection_column:
				reflected_i = reflection_column * 2 - i - 1
				if reflected_i < column_count:
					if get_column(pattern, i) != get_column(pattern, reflected_i):
						reflection = False
						break
			else:
				reflected_i = reflection_column * 2 - 1 - i
				if reflected_i >= 0:
					if get_column(pattern, i) != get_column(pattern, reflected_i):
						reflection = False
						break
		if reflection:
			return reflection_column
	return -1

def count_diffs(str_a, str_b):
	count = 0
	for i in range(len(str_a)):
		if str_a[i] != str_b[i]:
			count += 1
	return count

def find_row_b(pattern):
	row_count = len(pattern)
	#import pdb; pdb.set_trace()
	for reflection_row in range(1, row_count):
		smudge_count = 0
		for i in range(row_count):
			if i < reflection_row:
				reflected_i = reflection_row * 2 - i - 1
				if reflected_i < row_count:
					smudge_count += count_diffs(pattern[i], pattern[reflected_i])
			else:
				reflected_i = reflection_row * 2 - 1 - i
				if reflected_i >= 0:
					smudge_count += count_diffs(pattern[i], pattern[reflected_i])
		if smudge_count == 2:
			return reflection_row
	return -1
		
	
def find_column_b(pattern):
	column_count = len(pattern[0])
	for reflection_column in range(1, column_count):
		smudge_count = 0
		for i in range(column_count):
			if i < reflection_column:
				reflected_i = reflection_column * 2 - i - 1
				if reflected_i < column_count:
					smudge_count += count_diffs(get_column(pattern, i), get_column(pattern, reflected_i))
			else:
				reflected_i = reflection_column * 2 - 1 - i
				if reflected_i >= 0:
					smudge_count += count_diffs(get_column(pattern, i), get_column(pattern, reflected_i))
		if smudge_count == 2:
			return reflection_column
	return -1


def get_column(pattern, i):
	return ''.join([row[i] for row in pattern])


def main(patterns):
	total_a = sum([score_a(pattern) for pattern in patterns])
	total_b = sum([score_b(pattern) for pattern in patterns])

	return total_a, total_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--sample', action='store_true')
	args = parser.parse_args()

	wrapper(args)
