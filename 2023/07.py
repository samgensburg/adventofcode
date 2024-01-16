import argparse
from collections import defaultdict
import math
from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'
SAMPLE_FILE = Path(__file__).stem + '.sample'

LAYERS = 8


def parse_file(file):
	hands = [line.strip().split() for line in file]
	hands = [(hand, int(weight)) for hand, weight in hands]

	return hands


def hand_sorting_key_a(hand):
	out = 0
	counts = defaultdict(int)
	hand = hand[0]
	for c in hand:
		counts[c] += 1

	pair_count = 0
	triple_count = 0

	for key in counts:
		if counts[key] == 5:
			out = 6
		elif counts[key] == 4:
			out = 5
		elif counts[key] == 3:
			triple_count += 1
		elif counts[key] == 2:
			pair_count += 1
	
	if triple_count == 1 and pair_count == 1:
		out = 4
	elif triple_count == 1:
		out = 3
	elif pair_count == 2:
		out = 2
	elif pair_count == 1:
		out = 1
	
	card_value_table = {
		'A': 12,
		'K': 11,
		'Q': 10,
		'J': 9,
		'T': 8,
		'9': 7,
		'8': 6,
		'7': 5,
		'6': 4,
		'5': 3,
		'4': 2,
		'3': 1,
		'2': 0
	}

	for i, c in enumerate(hand):
		out += card_value_table[c] * ((1 / 13) ** (i + 1))
	return out


def hand_sorting_key_b(hand):
	out = 0
	counts = defaultdict(int)
	hand = hand[0]
	for c in hand:
		counts[c] += 1

	pair_count = 0
	triple_count = 0

	joker_count = counts['J']

	for key in counts:
		if key == 'J':
			pass
		elif counts[key] == 5:
			out = 6
		elif counts[key] == 4 and joker_count == 1:
			out = 6
		elif counts[key] == 4 and joker_count == 0:
			out = 5
		elif counts[key] == 3 and joker_count == 2:
			out = 6
		elif counts[key] == 3 and joker_count == 1:
			out = 5
		elif counts[key] == 3:
			triple_count += 1
		elif counts[key] == 2:
			pair_count += 1
	
	if out > 0:
		pass
	elif joker_count == 5 or joker_count == 4:
		out = 6
	elif triple_count == 1 and pair_count == 1:
		out = 4
	elif triple_count == 1:
		out = 3
	elif pair_count == 2 and joker_count == 1:
		out = 4
	elif pair_count == 2 and joker_count == 0:
		out = 2
	elif pair_count == 1 and joker_count == 3:
		out = 6
	elif pair_count == 1 and joker_count == 2:
		out = 5
	elif pair_count == 1 and joker_count == 1:
		out = 3
	elif pair_count == 1 and joker_count == 0:
		out = 1
	elif joker_count == 3:
		out = 5
	elif joker_count == 2:
		out = 3
	elif joker_count == 1:
		out = 1

	names = {
		6: 'Five-of-a-kind',
		5: 'Four-of-a-kind',
		4: 'Full House',
		3: 'Trips',
		2: 'Two-pair',
		1: 'One-pair',
		0: 'High card'
	}
	#print ((hand, names[out]))
	
	card_value_table = {
		'A': 12,
		'K': 11,
		'Q': 10,
		'J': 0,
		'T': 9,
		'9': 8,
		'8': 7,
		'7': 6,
		'6': 5,
		'5': 4,
		'4': 3,
		'3': 2,
		'2': 1
	}

	for i, c in enumerate(hand):
		out += card_value_table[c] * ((1 / 13) ** (i + 1))
	return out


def main(hands):
	hands_a = sorted(hands, key=hand_sorting_key_a)
	sum_a = 0
	for i, (_, weight) in enumerate(hands_a):
		sum_a += (i + 1) * weight

	hands_b = sorted(hands, key=hand_sorting_key_b)
	sum_b = 0
	for i, (_, weight) in enumerate(hands_b):
		sum_b += (i + 1) * weight


	return sum_a, sum_b


def wrapper(args):
	data_source = SAMPLE_FILE if args.sample else DATA_FILE
	with open(data_source, 'r') as file:
		data = parse_file(file)
		print(main(data))

parser = argparse.ArgumentParser()

parser.add_argument('-s', '--sample', action='store_true')
args = parser.parse_args()

wrapper(args)
