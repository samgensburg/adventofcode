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

START = 'S'
EMPTY = '.'
SPLITTER = '^'

def parse_file(file):
	out = []
	for line in file:
		parts = line.strip().split(',')
		assert len(parts) == 3
		out.append([int(p) for p in parts])

	return out

def square_distance(p1, p2):
	return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2

def find_circuit(circuits, i):
	for out in range(len(circuits)):
		if i in circuits[out]:
			return out
		
	return None

def main(input, wires, printing=False):
	out_b = 0

	lengths = []

	for i in range(len(input)):
		for j in range(i + 1, len(input)):
			index = square_distance(input[i], input[j])
			lengths.append([index, i, j])
	
	lengths = sorted(lengths)

	circuits = []

	for k in range(wires * 1000):
		if k == wires:
			if printing:
				print(circuits)
			outputs = sorted([len(circuit) for circuit in circuits], reverse=True)
			out_a = outputs[0] * outputs[1] * outputs[2]

		if len(circuits) and len(circuits[0]) == len(input):
			break

		_, i, j = lengths[k]
		out_b = input[i][0] * input[j][0]
		i_circuit = find_circuit(circuits, i)
		j_circuit = find_circuit(circuits, j)

		if printing:
			print(circuits)
			print((i, j))

		assert len(circuits) < 3 or len(circuits[0] & circuits[2]) == 0

		if i_circuit is not None and j_circuit is not None:
			if i_circuit == j_circuit:
				if printing:
					print ("No action taken")
				continue

			circuits[i_circuit] = circuits[i_circuit] | circuits[j_circuit]
			del circuits[j_circuit]

			continue

		if i_circuit is not None:
			circuits[i_circuit].add(j)
			continue

		if j_circuit is not None:
			circuits[j_circuit].add(i)
			continue

		circuits.append(set([i, j]))


	return out_a, out_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data, 10 if args.sample else 1000, printing=args.print))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-s', '--sample', action='store_true')
	parser.add_argument('-p', '--print', action='store_true')
	args = parser.parse_args()

	wrapper(args)
