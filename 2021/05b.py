from collections import defaultdict
import re

MAX_DIM = 1000

def main():
	with open('05.dat', 'r') as file:
		map = [defaultdict(int) for i in range(1000)]
		for line in file:
			line = line.strip()
			if not line:
				continue
			match = re.match(r'(\d+),(\d+) -> (\d+),(\d+)', line)
			x1 = int(match.group(1))
			y1 = int(match.group(2))
			x2 = int(match.group(3))
			y2 = int(match.group(4))
			if x1 == x2:
				x = x1
				for y in range(min(y1, y2), max(y1, y2) + 1):
					map[y][x] += 1
			elif y1 == y2:
				y = y1
				for x in range(min(x1, x2), max(x1, x2) + 1):
					map[y][x] += 1
			else:
				if x2 > x1:
					x_offset = 1
				else:
					x_offset = -1

				if y2 > y1:
					y_offset = 1
				else:
					y_offset = -1

				size = abs(x2 - x1)
				assert size == abs(y2 - y1)
				for i in range(size + 1):
					x = x1 + (x_offset * i)
					y = y1 + (y_offset * i)
					map[y][x] += 1

		count = 0
		for x in range(MAX_DIM):
			for y in range(MAX_DIM):
				if map[y][x] >= 2:
					count += 1

		return count

print(main())
