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

START = 'start'
FLIP = '%'
CONJUNCTION = '&'

LOW = 1
HIGH = 2

def parse_file(file):
	modules = {}
	for line in file:
		line = line.strip()
		if line[0] in '&%':
			mode = line[0]
			module_name = line[1:3]
			assert line[3:7] == ' -> '
			targets = line[7:].split(', ')
			modules[module_name] = (mode, targets)
		else:
			assert line[:15] == 'broadcaster -> '
			targets = line[15:].split(', ')
			modules[START] = (None, targets)

	return modules

OFF = 6
ON = 7

class Status():
	def __init__(self, modules):
		self.status = {}
		self.outputs = defaultdict(list)
		self.modules = modules
		for module_name in modules:
			module_type, module_targets = modules[module_name]
			if module_type == FLIP:
				self.status[module_name] = OFF
			if module_type == CONJUNCTION:
				self.status[module_name] = defaultdict(dict)
		
		self.status['rx'] = defaultdict(dict)

		for module_name in modules:
			module_type, module_targets = modules[module_name]
			for target_name in module_targets:
				if target_name in modules and modules[target_name][0] == CONJUNCTION:
					self.status[target_name][module_name] = LOW
	
	def add_output(self, origin, round_n):
		self.outputs[origin].append(round_n)

	def pretty_print_outputs(self):
		for key in self.outputs:
			print(f'{key}: {str(self.outputs[key])}')
		
		print()
		print('--differences--')
		for key in self.outputs:
			rounds = self.outputs[key]
			differences = [rounds[i+1] - rounds[i] for i in range(len(rounds) - 1)]
			print(f'{key}: {str(differences)}')

	def get_and_flip_module_state(self, target):
		out = self.status[target]
		assert out in [ON, OFF]
		if out == ON:
			self.status[target] = OFF
		else:
			self.status[target] = ON
		
		return out
	
	def update_source(self, target, input, pulse_type):
		self.status[target][input] = pulse_type

	def inputs_all_high(self, target):
		for key in self.status[target]:
			if self.status[target][key] != HIGH:
				return False
		
		return True


def send_pulse(status, modules, input, target, pulse_type):
	if target not in modules:
		assert target == 'rx'
		return [], pulse_type == LOW
	
	module_type, module_targets = modules[target]

	send_high_to_targets = False
	send_low_to_targets = False

	if module_type == FLIP:
		if pulse_type == HIGH:
			return [], False
		
		module_state = status.get_and_flip_module_state(target)

		if module_state == OFF:
			send_high_to_targets = True
		else:
			send_low_to_targets = True
	else:
		status.update_source(target, input, pulse_type)
		if status.inputs_all_high(target):
			send_low_to_targets = True
		else:
			send_high_to_targets = True
			
	if send_high_to_targets:
		return [(target, module_target, HIGH) for module_target in module_targets], False

	if send_low_to_targets:
		return [(target, module_target, LOW) for module_target in module_targets], False
	
	return [], False


def press_the_button(status, modules, printing, round_n=None):
	found_final = False

	if printing:
		print()
		print('button -low-> start')

	low_total, high_total = 1, 0
	pulse_queue = Queue()
	for target in modules[START][1]:
		pulse_queue.put((START, target, LOW))

	while pulse_queue.qsize():
		origin, target, pulse_type = pulse_queue.get()
		if pulse_type == LOW:
			low_total += 1
		else:
			high_total += 1

		if printing:
			type_text = '-low->' if pulse_type == LOW else '-high->'
			print(f'{origin} {type_text} {target}')
		
		if target == 'hp' and pulse_type == HIGH:
			status.add_output(origin, round_n)


		pulses, found = send_pulse(status, modules, origin, target, pulse_type)
		for pulse in pulses:
			pulse_queue.put(pulse)
		
		found_final = found_final or found
	
	return low_total, high_total, found_final

def main(modules, printing=False):
	#import pdb; pdb.set_trace()
	total_low, total_high = 0, 0
	out_b = -1
	status = Status(modules)
	for i in range(10000):
		#print(f'---round {i}---')
		local_low, local_high, found = press_the_button(status, modules, printing and i < 5, round_n=i)
		if i < 1000:
			total_low += local_low
			total_high += local_high
		if found and out_b < 0:
			out_b = i + 1
	
	out_a = total_low * total_high

	out_b = 1
	for key in status.outputs:
		out_b *= status.outputs[key][0] + 1

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
