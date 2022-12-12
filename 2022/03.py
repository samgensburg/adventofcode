from pathlib import Path

DATA_FILE = Path(__file__).stem + '.dat'

def priority(c):
	v = ord(c)
	if v >= ord('a') and v <= ord('z'):
		return v - ord('a') + 1
	return v - ord('A') + 27

def main():
	with open(DATA_FILE, 'r') as file:
		lines = [line.strip() for line in file]

	overlap = [set(list(line[:(len(line) // 2)])).intersection(
		set(list(line[(len(line) // 2):]))).pop() for line in lines]
	out1 = sum([priority(c) for c in overlap])

	out2 = 0
	for i in range(0, len(lines), 3):
		s0 = set(list(lines[i]))
		s1 = set(list(lines[i+1]))
		s2 = set(list(lines[i+2]))
		out2 += priority((s0 & s1 & s2).pop())
	return out1, out2


			


print(main())
