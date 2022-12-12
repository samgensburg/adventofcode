from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

DELTA_MAP = {
	'R': (1, 0),
	'L': (-1, 0),
	'U': (0, 1),
	'D': (0, -1)
}

def sign(n):
	if n > 0:
		return 1
	if n < 0:
		return -1
	return 0

def move(loc, delta):
	return (loc[0] + delta[0], loc[1] + delta[1])

def snap(head, tail, delta):
	head_x, head_y = head
	tail_x, tail_y = tail
	delta_x, delta_y = head_x - tail_x, head_y - tail_y
	assert abs(delta_x) <= 2 and abs(delta_y) <= 2

	if abs(delta_x) == 2 or abs(delta_y) == 2:
		return (tail_x + sign(delta_x), tail_y + sign(delta_y))
	return tail

def main(text):
	visited1 = set()
	visited1.add((0, 0))
	visited9 = set()
	visited9.add((0, 0))
	rope = [(0, 0)] * 10

	for line in text:
		vals = line.strip().split()
		delta = DELTA_MAP[vals[0]]
		for i in range(int(vals[1])):
			rope[0] = move(rope[0], delta)
			for i in range(9):
				rope[i + 1] = snap(rope[i], rope[i+1], delta)
			visited1.add(rope[1])
			visited9.add(rope[9])

	return len(visited1), len(visited9)


SAMPLE = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

SAMPLE2 = """U 1
R 1
D 2
L 1
R 2
U 1
L 1
U 1
L 2
R 1
D 2
U 1
R 2"""

print(main(SAMPLE.strip().split('\n')))
print(main(SAMPLE2.strip().split('\n')))

with open(DATA_FILE, 'r') as file:
	print(main(file.read().strip().split('\n')))
