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
	text = file.read()
	text = text.replace('\n', '')
	ranges = text.split(',')

	out = []
	for range in ranges:
		numbers = range.split('-')
		out.append((int(numbers[0]), int(numbers[1])))

	return out

def digit_count(n):
	assert n >= 0
	out = 0
	while n > 0:
		out += 1
		n = n // 10
	return out

def digit_count_is_odd(n):
	n = digit_count(n)
	return n % 2 == 1

def main(input, printing=False):
	out_a = 0
	out_b = 0
	for low, high in input:
		codes_b = set()
		repeats = 2
		while repeats < 50:
			low_working = low
			while low_working < high:
				digit_count_low = digit_count(low_working)
				digit_count_high = digit_count(high)

				if digit_count_low % repeats != 0:
					low_working = 10 ** digit_count_low
					continue

				#import pdb; pdb.set_trace()
				divisor = 0
				for i in range(0, digit_count_low, digit_count_low // repeats):
					divisor += 10 ** i
				print(divisor)
				low_working = (low_working // divisor) * divisor + divisor if low_working % divisor else low
				high_tmp = high if digit_count_low == digit_count_high else 10 ** digit_count_low - 1
				while low_working <= high_tmp:
					if repeats == 2:
						out_a += low_working
					codes_b.add(low_working)
					low_working += divisor

				low_working = 10 ** digit_count_low
			repeats += 1
		out_b += sum(codes_b)

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
