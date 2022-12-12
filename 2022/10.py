from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

def main(text):
	x = 1
	x_history = [1]
	for line in text:
		vals = line.split()
		if vals[0] == 'noop':
			x_history.append(x)
		elif vals[0] == 'addx':
			x_history.append(x)
			x_history.append(x)
			x += int(vals[1])

	out =  sum([i * x_history[i] for i in [20, 60, 100, 140, 180, 220]])

	#import pdb; pdb.set_trace()
	for i in range(6):
		row = ''
		for j in range(i * 40 + 1, i * 40 + 41):
			p = j - i * 40
			x = x_history[j]
			if x == p or x == p-1 or x == p-2:
				row += '#'
			else:
				row += '.'
		print(row)

	return out


SAMPLE = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

main(SAMPLE.split('\n'))
print()
print()
print()
with open(DATA_FILE, 'r') as file:
	print(main(file.read().strip().split('\n')))
