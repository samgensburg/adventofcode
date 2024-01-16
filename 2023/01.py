from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

TEXT = [
	'zero_', # not in problem
	'one',
	'two',
	'three',
	'four',
	'five',
	'six',
	'seven',
	'eight',
	'nine'
]

def main():
	with open(DATA_FILE, 'r') as file:
		sum_a = 0
		sum_b = 0
		for line in file:
			line = line.strip()
			first = None
			last = None
			for i, c in enumerate(line):
				if c.isdigit():
					last = int(c)
					last_index = i
					if first is None:
						first_index = i
						first = int(c)
			sum_a += first * 10 + last

			for n, text in enumerate(TEXT):
				index = line.find(text)
				if index != -1 and index < first_index:
					first_index = index
					first = n

				index = line.rfind(text)
				if index != -1 and index > last_index:
					last_index = index
					last = n
			sum_b += first * 10 + last


		return sum_a, sum_b


			


print(main())
