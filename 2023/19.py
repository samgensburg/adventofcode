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

ALWAYS = 0
LT = 1
GT = 2

COMMAND_MAP = {'<': LT, '>': GT}

def parse_file(file):
	workflows = dict()
	parts = []
	state = 0
	for line in file:
		line = line.strip()
		if state == 0:
			if len(line) == 0:
				state = 1
				continue

			i = line.find('{')
			assert i > 0
			assert line[-1] == '}'
			name = line[:i]

			instructions = line[i+1:-1]
			instructions = instructions.split(',')
			workflow_actions = []
			for instruction in instructions:
				i = instruction.find(':')
				if i < 0:
					workflow_actions.append((ALWAYS, '', 0, instruction))
				else:
					assert instruction[0] in 'xmas'
					assert instruction[1] in '<>'
					v = int(instruction[2:i])
					target = instruction[i+1:]
					workflow_actions.append((COMMAND_MAP[instruction[1]], instruction[0], v, target))
			
			workflows[name] = workflow_actions
		
		else:
			match = re.match(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', line)
			assert match

			parts.append({
				'x': int(match.group(1)),
				'm': int(match.group(2)),
				'a': int(match.group(3)),
				's': int(match.group(4))
			})

	return workflows, parts
	
def accept(workflows, part, part_min=None, part_max=None):
	current_workflow_name = 'in'
	while True:
		if current_workflow_name == 'R':
			out = False
			break
		if current_workflow_name == 'A':
			out = True
			break
		
		current_workflow = workflows[current_workflow_name]
		for instruction in current_workflow:
			command, variable, value, target = instruction
			satisfied = (command == ALWAYS)
			if command == LT:
				satisfied = part[variable] < value
				if part_max and part_max[variable] >= value:
					part_max[variable] = value - 1
			if command == GT:
				satisfied = part[variable] > value
				if part_min and part_min[variable] <= value:
					part_max[variable] = value + 1
			
			if satisfied:
				current_workflow_name = target
				break
	
	if part_min:
		return part_min, part_max, out
	return out

def accept_full(workflows, part):
	return accept(workflows, part,
			   part_min={'x':1, 'm':1, 'a':1, 's':1},
			   part_max={'x':VAL_MAX, 'm':VAL_MAX, 'a':VAL_MAX, 's':VAL_MAX})

def value(part):
	return part['x'] + part['m'] + part['a'] + part['s']

VAL_MAX = 4000

class Cache():
	def __init__(self):
		s = Tree_Node('s', None)
		a = Tree_Node('a', s)
		m = Tree_Node('m', a)
		x = Tree_Node('x', m)
		self.tree = x

	def set_range(self, part_min, part_max, result):
		self.tree.set_recursive(part_min, part_max, result)

	def __contains__(self, part):
		return part in self.tree

class Tree_Node():
	def __init__(self, property, default):
		self.property = property
		self.is_recursive = (type(default) == type(self))
		self.ranges = [(1, 4000, default)]


	def __contains__(self, part):
		key = part[self.property]
		for r in self.ranges:
			low, high, val = r
			if high >= key:
				assert low <= key
				break

		if self.is_recursive:
			return part in val
		return val is not None


	def set_recursive(self, low, high, value):
		low_val = low[self.property]
		high_val = high[self.property]
		for i, r in enumerate(self.ranges):
			r_low, r_high, r_value = r
			r_value_new = r_value
			r_value_new_2 = r_value
			if self.is_recursive:
				r_value_new = r_value.clone()
				r_value_new.set_recursive(low, high, value)
				r_value_new_2 = r_value.clone()

			if high_val < r_low:
				continue

			print (low_val, high_val, r_low, r_high)
			assert low_val >= r_low
			assert high_val <= r_high
			if low_val == r_low and high_val == r_high:
				self.ranges[i] = (low_val, high_val, r_value_new)
			elif low_val == r_low and high_val < r_high:
				self.ranges[i] = (high_val + 1, r_high, r_value)
				self.ranges.insert(i, (low_val, high_val, r_value_new))
			elif low_val > r_low and high_val < r_high:
				self.ranges[i] = (high_val + 1, r_high, r_value)
				self.ranges.insert(i, (low_val, high_val, r_value_new))
				self.ranges.insert(i, (r_low, low_val - 1, r_value_new_2))
	
	def clone(self):
		out = Tree_Node(self.property, None)
		out.is_recursive = self.is_recursive
		out.ranges = self.ranges
		if self.is_recursive:
			for i in range(len(out.ranges)):
				a, b, c = out.ranges[i]
				c = c.clone()
				out.ranges[i] = (a,b,c)
		return out


class Part_Range():
	def __init__(self, x_low, x_high, m_low, m_high, a_low, a_high, s_low, s_high):
		self.lows = {'x':x_low, 'm':m_low, 'a':a_low, 's':s_low}
		self.highs = {'x':x_high, 'm':m_high, 'a':a_high, 's':s_high}

	
	def split(self, variable, min_new):
		assert variable in 'xmas'
		low, high = self[variable]
		assert low < min_new and high >= min_new
		other = self.clone()
		self.highs[variable] = min_new - 1
		other.lows[variable] = min_new
		return self, other

	def clone(self):
		return Part_Range(self.lows['x'], self.highs['x'],
					self.lows['m'], self.highs['m'],
					self.lows['a'], self.highs['a'],
					self.lows['s'], self.highs['s'])

	def __getitem__(self, key):
		assert key in 'xmas'
		return (self.lows[key], self.highs[key])

	def __repr__(self):
		return f"x:({self.lows['x']}, {self.highs['x']}), " + \
			f"m:({self.lows['m']}, {self.highs['m']}), " + \
			f"a:({self.lows['a']}, {self.highs['a']}), " + \
			f"s:({self.lows['s']}, {self.highs['s']})"

def calculate_full(workflows, printing=False):
	queue = Queue()
	queue.put((Part_Range(1,4000,1,4000,1,4000,1,4000),'in'))
	accept_ranges = []

	while queue.qsize():
		#import pdb; pdb.set_trace()
		part_range, workflow_name = queue.get()
		if workflow_name == 'R':
			continue
		if workflow_name == 'A':
			accept_ranges.append(part_range)
			continue

		workflow = workflows[workflow_name]
		
		for instruction in workflow:
			command, variable, value, target = instruction

			full_match = False
			partial_match = False
			part_range_a, part_range_b = None, None
			if command == ALWAYS:
				full_match = True
			elif command == LT:
				if part_range[variable][1] < value:
					full_match = True
				elif part_range[variable][0] < value:
					partial_match = True
					part_range_a, part_range_b = part_range.split(variable, value)
			else:
				if part_range[variable][0] > value:
					full_match = True
				elif part_range[variable][1] > value:
					partial_match = True
					part_range_a, part_range_b = part_range.split(variable, value + 1)
			
			if full_match:
				queue.put((part_range, target))
				break
			if partial_match:
				queue.put((part_range_a, workflow_name))
				queue.put((part_range_b, workflow_name))
				break
	
	out = 0
	for accept_range in accept_ranges:
		n_x = accept_range['x'][1] - accept_range['x'][0] + 1
		n_m = accept_range['m'][1] - accept_range['m'][0] + 1
		n_a = accept_range['a'][1] - accept_range['a'][0] + 1
		n_s = accept_range['s'][1] - accept_range['s'][0] + 1

		out += n_x * n_m * n_a * n_s

		"""
		total_x = n_x * (accept_range['x'][1] + accept_range['x'][0]) / 2
		total_m = n_m * (accept_range['m'][1] + accept_range['m'][0]) / 2
		total_a = n_a * (accept_range['a'][1] + accept_range['a'][0]) / 2
		total_s = n_s * (accept_range['s'][1] + accept_range['s'][0]) / 2
		out += total_x * n_m * n_a * n_s
		out += n_x * total_m * n_a * n_s
		out += n_x * n_m * total_a * n_s
		out += n_x * n_m * n_a * total_s
		"""
	return out


def main(input, printing=False):
	workflows, parts = input

	parts_filtered = [part for part in parts if accept(workflows, part)]
	part_values = [value(part) for part in parts_filtered]
	out_a = sum(part_values)
	
	out_b = calculate_full(workflows)

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
