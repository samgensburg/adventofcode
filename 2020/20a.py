from collections import defaultdict
import re

SIZE = 10

class Tile:
	def __init__(self, input):
		match = re.match(r'^Tile (\d+):$', input)
		assert match
		self.number = int(match.group(1))
		self.lines = []

	def add_line(self, line):
		assert len(line) == 10
		assert len(self.lines) < 10
		self.lines.append(line)
		if len(self.lines) == 10:
			self.finalize()

	def finalize(self):
		self.strings = []
		self.min_values = []
		self.strings.append(self.lines[0])
		self.strings.append([self.lines[i][-1] for i in range(SIZE)])
		self.strings.append([self.lines[-1][SIZE - i - 1] for i in range(SIZE)])
		self.strings.append([self.lines[SIZE - i - 1][0] for i in range(SIZE)])
		for string in self.strings:
			self.min_values.append(string_to_min_value(string))


def string_to_min_value(string):
	assert len(string) == SIZE
	left = 0
	right = 0
	for i in range(SIZE):
		if string[i] == '#':
			left += 1 << (SIZE - 1 - i)
			right += 1 << i

	return left if left < right else right


def main():
	tiles = []
	with open('20.dat', 'r') as file:
		tile = None
		for line in file:
			line = line.strip()
			if tile is None:
				tile = Tile(line)
				tiles.append(tile)
			elif line:
				tile.add_line(line)
			else:
				tile = None
	counts = defaultdict(int)
	for tile in tiles:
		for min_value in tile.min_values:
			counts[min_value] += 1

	corners = []
	edges = []
	for tile in tiles:
		unique_count = 0
		for min_value in tile.min_values:
			if counts[min_value] == 1:
				unique_count += 1
		if unique_count == 2:
			corners.append(tile)
		if unique_count == 1:
			edges.append(tile)
		if unique_count >= 3:
			import pdb; pdb.set_trace()
		assert unique_count < 3
	product = 1

	assert len(corners) == 4
	for corner in corners:
		product *= corner.number

	return product


print(main())
