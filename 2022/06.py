from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'


def main():
	with open(DATA_FILE, 'r') as file:
		text = list(file.read())

	for i in range(1000000):
		if len(set(text[i:i+4])) == 4:
			out1 = i + 4
			break

	for i in range(1000000):
		if len(set(text[i:i+14])) == 14:
			out2 = i + 14
			break

	return (out1, out2)

print(main())
