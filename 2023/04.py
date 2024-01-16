import argparse
from collections import defaultdict
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

N_CARDS = 193

def line_to_data(line):
	line = line.strip()
	match = re.search(r'Card +(\d+):', line)
	id = int(match.group(1))
	line = line[match.end():]
	split_index = line.find('|')
	assert split_index > 0
	correct_text = line[:split_index].strip().replace('  ', ' ')
	card_text = line[split_index+1:].strip().replace('  ',' ')
	correct_nums = set([int(n) for n in correct_text.split()])
	card_nums = set([int(n) for n in card_text.split()])
	return id, correct_nums, card_nums


def main(data_source):
	with open(data_source, 'r') as file:
		sum_a = 0
		lookup = [0] * N_CARDS
		totals = [1] * N_CARDS

		for line in file:
			id, correct_nums, card_nums = line_to_data(line)
			overlap = correct_nums.intersection(card_nums)
			count = len(overlap)
			if count == 0:
				continue
			score = 2 ** (count - 1)
			sum_a += score
			lookup[id - 1] = count
		for i in range(N_CARDS):
			n_cards = totals[i]
			count = lookup[i]
			for j in range(i + 1, i + 1 + count):
				totals[j] += n_cards
		sum_b = sum(totals)
		return sum_a, sum_b


parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

data_source = SAMPLE_FILE if args.sample else DATA_FILE
N_CARDS = 6 if args.sample else N_CARDS
print(main(data_source))
