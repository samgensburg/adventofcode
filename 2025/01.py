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
    out = []
    for line in file:
        line = line.strip()
        regex_match = re.match(r'^([RL])(\d+)$', line)
        assert regex_match
        out.append((regex_match.group(1) == 'R', int(regex_match.group(2))))

    return out

def main(input, printing=False):
    loc = 50
    out_a = 0
    out_b = 0
    for right, n in input:
        last = loc
        while n >= 100:
             n -= 100
             out_b += 1

        if right:
            loc += n
        else:
            loc -= n
        
        if loc >= 100 or (loc <= 0 and last > 0):
             out_b += 1

        if printing:
            print(loc)

        loc %= 100
        if loc == 0:
             out_a += 1

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
