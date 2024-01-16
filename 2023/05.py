import argparse
from collections import defaultdict
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

LAYERS = 8

class Almanac_Dict():
	def __init__(self):
		self.entries = []

	def add_entry(self, dest_range_start, source_range_start, range_length):
		self.entries.append((source_range_start, dest_range_start, range_length))

	def lookup_range(self, start, length):
		out = Range_Object()
		for entry in self.entries:
			if start >= entry[0] and start < entry[0] + entry[2]:
				start_out = start - entry[0] + entry[1]
				if start + length <= entry[0] + entry[2]:
					out.add_range(start_out, length)
					return out
				length_out = entry[0] + entry[2] - start
				out.add_range(start_out, length_out)
				recursive_output = self.lookup_range(start + length_out, length - length_out)
				out.add_range_object(recursive_output)
				return out

		lowest_over = None
		for entry in self.entries:
			if entry[0] > start:
				lowest_over = entry[0] if lowest_over is None else min(entry[0], lowest_over)
		
		if lowest_over is None or start + length <= lowest_over:
			out.add_range(start, length)
			return out
		
		length_out = lowest_over - start
		out.add_range(start, length_out)
		recursive_output = self.lookup_range(start + length_out, length - length_out)
		out.add_range_object(recursive_output)
		return out
	

	def lookup_range_object(self, range_object):
		out = Range_Object()
		for start, length in range_object:
			out.add_range_object(self.lookup_range(start, length))
		return out


	def __getitem__(self, key):
		assert type(key) is int
		for entry in self.entries:
			if key >= entry[0] and key < entry[0] + entry[2]:
				return key - entry[0] + entry[1]
		return key


class Almanac():
	def __init__(self):
		self.dicts = [Almanac_Dict() for _ in range(LAYERS - 1)]

	def add_entry(self, layer, dest_range_start, source_range_start, range_length):
		self.dicts[layer].add_entry(dest_range_start, source_range_start, range_length)

	def lookup_full(self, seed):
		n = seed
		for i in range(LAYERS - 1):
			n = self.dicts[i][n]
		return n

	def lookup_range_object_full(self, range_object):
		for i in range(LAYERS - 1):
			print(range_object)
			range_object = self.dicts[i].lookup_range_object(range_object)
		print(range_object)
		return range_object


class Range_Object():
	def __init__(self):
		self.ranges = []
	
	def add_range(self, start, length):
		self.ranges.append((start, length))

	def add_range_object(self, range_object):
		for start, length in range_object:
			self.add_range(start, length)

	def __iter__(self):
		self.current_index = 0
		return self
	
	def __next__(self):
		if self.current_index >= len(self.ranges):
			raise StopIteration
		out = self.ranges[self.current_index]
		self.current_index += 1
		return out
	
	def __str__(self):
		out = 'Range Object with ranges:\n'
		out += '\n'.join([f'({entry[0]}, {entry[1]})' for entry in self.ranges])
		return out
			


def parse_file(file):
	state = 0
	layer = -1
	almanac = Almanac()
	for line in file:
		line = line.strip()
		if state == 0:
			assert line[:7] == 'seeds: '
			seeds_a = [int(n) for n in line[7:].split()]
			seeds_b = Range_Object()
			for i in range(0, len(seeds_a), 2):
				seeds_b.add_range(seeds_a[i], seeds_a[i+1])
			state = 1
		elif state == 1 or len(line) == 0:
			assert len(line) == 0
			layer += 1
			state = 2
		elif state == 2:
			assert line[-5:] == ' map:'
			state = 3
		elif state == 3:
			assert re.match(r'^\d+ \d+ \d+$', line)
			ns = [int(n) for n in line.split()]
			almanac.add_entry(layer, ns[0], ns[1], ns[2])


	return almanac, seeds_a, seeds_b


def main(file):
	almanac, seeds_a, seeds_b = parse_file(file)
	best_a = None
	for seed in seeds_a:
		location = almanac.lookup_full(seed)
		best_a = location if best_a is None else min(best_a, location)

	ranges_b = almanac.lookup_range_object_full(seeds_b)
	best_b = None
	for start, length in ranges_b:
		best_b = start if best_b is None else min(best_b, start)

	return best_a, best_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		print(main(file))

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

wrapper(args)
