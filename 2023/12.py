import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

BROKEN = '#'
WORKING = '.'
UNKNOWN = '?'

def parse_file(file):
	out = []
	for i, line in enumerate(file):
		line = line.strip()
		record, numbers = line.split()
		numbers = numbers.split(',')
		numbers = [int(n) for n in numbers]
		out.append((record, numbers))

	return out


def n_possible_arrangements(record, numbers):
	out = n_possible_arrangements_recursive([], record, numbers, dict())
	return out

def n_possible_arrangements_unfolded(record, numbers):
	#print(record, numbers)
	out = n_possible_arrangements_recursive([], '?'.join([record] * 5), numbers * 5, dict())
	#print(out)
	return out

def n_possible_arrangements_recursive(prefix, record, numbers, cache=None):
	if (out := try_fetch_cache(prefix, cache)) != -1:
		return out

	if not is_valid_prefix(prefix, numbers):
		out = 0
		try_update_cache(prefix, cache, out)
		return out
	
	i = len(prefix)
	if i == len(record):
		prefix_ext = prefix.copy()
		prefix_ext.append('.')
		if is_valid_prefix(prefix_ext, numbers):
			if len(get_counts(prefix_ext)) == len(numbers):
				out = 1
				try_update_cache(prefix, cache, out)
				return out
		out = 0
		try_update_cache(prefix, cache, out)
		return out
	
	if record[i] != UNKNOWN:
		prefix = prefix.copy()
		prefix.append(record[i])
		out = n_possible_arrangements_recursive(prefix, record, numbers, cache)
		try_update_cache(prefix, cache, out)
		return out
	
	prefix_a = prefix.copy()
	prefix_b = prefix.copy()
	prefix_a.append(BROKEN)
	prefix_b.append(WORKING)
	out = n_possible_arrangements_recursive(prefix_a, record, numbers, cache) \
		+ n_possible_arrangements_recursive(prefix_b, record, numbers, cache)
	
	try_update_cache(prefix, cache, out)
	return out

def try_update_cache(prefix, cache, out):
	if cache is not None:
		key = cache_key(prefix)
		cache[key] = out

def try_fetch_cache(prefix, cache):
	if cache is not None:
		key = cache_key(prefix)
		if key not in cache:
			return -1
		return cache[key]
	return -1

def cache_key(prefix):
	l = len(prefix)
	if l == 0:
		return ' '
	last_spring = prefix[-1]
	counts = get_counts(prefix)
	return str(l) + '|' + last_spring + '|' + ','.join([str(c) for c in counts])


def is_valid_prefix(prefix, numbers):
	counts = get_counts(prefix)

	if (l := len(counts)) == 0:
		return True
	
	if l > len(numbers):
		return False
	
	for i in range(l - 1):
		if counts[i] != numbers[i]:
			return False
	
	if counts[l - 1] == numbers[l - 1]:
		return True

	return counts[l - 1] < numbers[l - 1] and prefix[-1] == BROKEN

def get_counts(springs):
	past = []
	running = 0
	in_run = False
	for spring in springs:
		if spring == WORKING:
			if in_run:
				past.append(running)
				running = 0
				in_run = False
		else:
			assert spring == BROKEN
			if in_run:
				running += 1
			else:
				in_run = True
				running = 1
	if in_run:
		past.append(running)
	
	return past

def main(input):
	total_a = sum([n_possible_arrangements(record, numbers) for record, numbers in input])
	total_b = sum([n_possible_arrangements_unfolded(record, numbers) for record, numbers in input])	

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
