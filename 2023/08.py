import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

LAYERS = 8


def parse_file(file):
	mapping = dict()
	for i, line in enumerate(file):
		line = line.strip()
		if i == 0:
			instructions = line
		elif i == 1:
			pass
		else:
			match = re.match(r'^([A-Z]{3}) = \(([A-Z]{3})\, ([A-Z]{3})\)$', line)
			assert match
			source = match.group(1)
			assert source not in mapping
			mapping[source] = (match.group(2), match.group(3))

	return instructions, mapping


def step(current, count, instruction_i, instructions, mapping):
	instruction_count = len(instructions)
	if instructions[instruction_i] == 'L':
		current = mapping[current][0]
	else:
		current = mapping[current][1]
	
	instruction_i += 1
	if instruction_i == instruction_count:
		instruction_i = 0
	
	count += 1	
	return current, count, instruction_i

def to_next_end(current, count, instruction_i, instructions, mapping, is_simple, cache=None):
	SIMPLE_END = 'ZZZ'
	if cache is not None:
		if out := cache.lookup(current, count, instruction_i):
			return out
		cache.set_start(current, count, instruction_i)

	while True:
		current, count, instruction_i = step(current, count, instruction_i, instructions, mapping)

		if is_simple and current == SIMPLE_END:
			break

		if not is_simple and current[2] == 'Z':
			break

	if cache is not None:
		cache.record(current, count, instruction_i)
	return current, count, instruction_i


class Period_Cache():
	def __init__(self):
		self.table = dict()
		self.current = None
		self.count = None
		self.instruction_i = None
	
	@staticmethod
	def key_string(current, instruction_i):
		return f'{current}_{instruction_i}'
	
	def lookup(self, current, count, instruction_i):
		key = self.key_string(current, instruction_i)
		if key in self.table:
			current, increment, instruction_i = self.table[key]
			return current, count + increment, instruction_i
		return None
	
	def set_start(self, current, count, instruction_i):
		assert self.lookup(current, count, instruction_i) is None
		assert self.current == None
		assert self.count == None
		assert self.instruction_i == None

		self.current = current
		self.count = count
		self.instruction_i = instruction_i

	def record(self, current, count, instruction_i):
		assert self.lookup(current, count, instruction_i) is None
		assert self.current is not None
		assert self.count is not None
		assert self.instruction_i is not None

		key_string = self.key_string(self.current, self.instruction_i)
		to_record = (current, count - self.count, instruction_i)
		self.table[key_string] = to_record
		self.current = None
		self.count = None
		self.instruction_i = None


def status_key(status):
	return status[1]


def main(input):
	START = 'AAA'

	instructions, mapping = input
	import pdb; pdb.set_trace()

	current = START
	count = 0
	instruction_i = 0

	_, count_a, _ = to_next_end(current, count, instruction_i, instructions, mapping, True)

	starts = [loc for loc in mapping if loc[2] == 'A']
	statuses = [(start, 0, 0) for start in starts]
	
	current_statuses = [to_next_end(curr, c, i_i, instructions, mapping, False) for curr, c, i_i in statuses]
	cache = Period_Cache()
	while True:
		print(current_statuses)
		current_statuses = sorted(current_statuses, key=status_key)
		if status_key(current_statuses[0]) == status_key(current_statuses[-1]):
			count_b = status_key(current_statuses[0])
			break
		curr, c, i_i = current_statuses[0]
		current_statuses[0] = to_next_end(curr, c, i_i, instructions, mapping, False, cache=cache)

	return count_a, count_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data))

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

wrapper(args)
