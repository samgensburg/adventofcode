import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

def parse_file(file):
	text = file.read().strip()
	text = text.replace('\n', '')
	out = text.split(',')

	return out


def hash_value(s):
	v = 0
	for c in s:
		v += ord(c)
		v *= 17
		v %= 256
	return v

def lens_string(l):
	return f'[{l[0]} {l[1]}]'

def box_string(box):
	return ' '.join([lens_string(l) for l in box])

def main(input, printing=False):
	out_a = sum([hash_value(s) for s in input])
	boxes = [[] for i in range(256)]
	for s in input:
		if ((i := s.find('-')) >= 0):
			label = s[:i]
			box_n = hash_value(label)
			for j, lens in enumerate(boxes[box_n]):
				if lens[0] == label:
					boxes[box_n].pop(j)
					break
		else:
			i = s.find('=')
			assert i >= 0
			label = s[:i]
			box_n = hash_value(label)
			v = int(s[i+1:])
			found = False
			for j, lens in enumerate(boxes[box_n]):
				if lens[0] == label:
					boxes[box_n][j] = ((label, v))
					found = True
					break
			if not found:
				boxes[box_n].append((label, v))
		
		if printing:
			print(f'After "{s}"')
			for i in range(256):
				if len(boxes[i]):
					print(f'Box {i}: {box_string(boxes[i])}')
			print()
	
	total_b = 0
	for box_n in range(256):
		for i, lens in enumerate(boxes[box_n]):
			total_b += (box_n + 1) * (i + 1) * lens[1]

	return out_a, total_b


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
