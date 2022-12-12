from pathlib import Path

DATA_FILE = Path(__file__).stem + '.dat'

shape_score_table = {
	'X': 1,
	'Y': 2,
	'Z': 3,
}

outcome_score_table = {
	'AX': 3,
	'BY': 3,
	'CZ': 3,
	'AY': 6,
	'BZ': 6,
	'CX': 6,
	'AZ': 0,
	'BX': 0,
	'CY': 0,
}

translation_table = {
	'AX': 'Z',
	'BX': 'X',
	'CX': 'Y',
	'AY': 'X',
	'BY': 'Y',
	'CY': 'Z',
	'AZ': 'Y',
	'BZ': 'Z',
	'CZ': 'X',
}

def main():
	with open(DATA_FILE, 'r') as file:
		lines = [line.strip().split() for line in file]
		out1 = sum([shape_score_table[line[1]] + outcome_score_table[line[0] + line[1]] for line in lines])
		lines = [[line[0], translation_table[line[0] + line[1]]] for line in lines]
		out2 = sum([shape_score_table[line[1]] + outcome_score_table[line[0] + line[1]] for line in lines])
	return out1, out2

print(main())
