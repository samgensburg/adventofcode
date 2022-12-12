from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

def main():
	with open(DATA_FILE, 'r') as file:
		count_full = 0
		count_part = 0
		for line in file:
			match = re.match(r'(\d+)-(\d+),(\d+)-(\d+)', line)
			assert match
			vals = [int(match.group(i)) for i in range(1, 5)]
			if vals[0] <= vals[2] and vals[1] >= vals[3]:
				count_full += 1
				print(vals)
			elif vals[0] >= vals[2] and vals[1] <= vals[3]:
				count_full += 1
				print(vals)

			if vals[1] < vals[2] or vals[3] < vals[0]:
				continue
			else:
				count_part += 1
	return count_full, count_part

			


print(main())
