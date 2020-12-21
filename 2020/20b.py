from collections import defaultdict
import re

SIZE = 10
GRID_SIZE = 12

class Tile:
	def __init__(self, input):
		match = re.match(r'^Tile (\d+):$', input)
		assert match
		self.id = int(match.group(1))
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
		self.min_values.append(string_to_min_value(self.top()))
		self.min_values.append(string_to_min_value(self.bottom()))
		self.min_values.append(string_to_min_value(self.left()))
		self.min_values.append(string_to_min_value(self.right()))

	# Left to right
	def top(self):
		return [self.lines[0][i] for i in range(SIZE)]

	# Left to right
	def bottom(self):
		return [self.lines[-1][i] for i in range(SIZE)]

	# Top to bottom
	def left(self):
		return [self.lines[i][0] for i in range(SIZE)]

	# Top to bottom
	def right(self):
		return [self.lines[i][-1] for i in range(SIZE)]

	def center(self):
		out = []
		for i in range(SIZE - 2):
			out.append([self.lines[i + 1][j + 1] for j in range(SIZE - 2)])

		return out

	def left_right_flip(self):
		for i in range(SIZE):
			self.lines[i] = [self.lines[i][SIZE - 1 - j] for j in range(SIZE)]

	def rotate_right(self):
		new_lines = []
		for i in range(SIZE):
			new_lines.append([self.lines[SIZE - 1 - j][i] for j in range(SIZE)])

		self.lines = new_lines


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

	tile_map = defaultdict(list)
	for tile in tiles:
		for min_value in tile.min_values:
			tile_map[min_value].append(tile)

	corners = []
	for tile in tiles:
		unique_count = 0
		for min_value in tile.min_values:
			if len(tile_map[min_value]) == 1:
				unique_count += 1
		if unique_count == 2:
			corners.append(tile)
		assert unique_count < 3
	product = 1

	assert len(corners) == 4
	grid = []
	for i in range(GRID_SIZE):
		grid.append([])
		for j in range(GRID_SIZE):
			if i == 0 and j == 0:
				tile = corners[0]
				if not is_unique(tile.left(), tile_map):
					tile.left_right_flip()
				assert is_unique(tile.left(), tile_map)
				if not is_unique(tile.top(), tile_map):
					tile.rotate_right()
				assert is_unique(tile.left(), tile_map)
				assert is_unique(tile.top(), tile_map)
				grid[i].append(tile)
			elif j == 0:
				edge = grid[i - 1][j].bottom()
				old_id = grid[i - 1][j].id
				potential_tiles = tile_map[string_to_min_value(edge)]
				assert len(potential_tiles) == 2
				tile = potential_tiles[0] if potential_tiles[0].id != old_id else potential_tiles[1]
				assert tile.id != old_id
				for n in range(4):
					if tile.top() == edge:
						break
					tile.rotate_right()
				if tile.top() != edge:
					tile.left_right_flip()
					for n in range(3):
						if tile.top() == edge:
							break
						tile.rotate_right()
				assert tile.top() == edge
				grid[i].append(tile)
			else:
				edge = grid[i][j - 1].right()
				old_id = grid[i][j - 1].id
				potential_tiles = tile_map[string_to_min_value(edge)]
				assert len(potential_tiles) == 2
				tile = potential_tiles[0] if potential_tiles[0].id != old_id else potential_tiles[1]
				assert tile.id != old_id
				for n in range(4):
					if tile.left() == edge:
						break
					tile.rotate_right()
				if tile.left() != edge:
					tile.left_right_flip()
					for n in range(3):
						if tile.left() == edge:
							break
						tile.rotate_right()
				assert tile.left() == edge
				grid[i].append(tile)

	for i in range(GRID_SIZE - 1):
		for j in range(GRID_SIZE - 1):
			assert grid[i][j].right() == grid[i][j + 1].left()
			assert grid[i][j].bottom() == grid[i + 1][j].top()

	for i in range(GRID_SIZE):
		assert is_unique(grid[i][0].left(), tile_map)
		assert is_unique(grid[i][-1].right(), tile_map)
		assert is_unique(grid[0][i].top(), tile_map)
		assert is_unique(grid[-1][i].bottom(), tile_map)

	grid = [[grid[i][j].center() for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

	map = []
	for i in range(GRID_SIZE * (SIZE - 2)):
		map.append([grid[i // 8][j // 8][i % 8][j % 8] for j in range(GRID_SIZE * (SIZE - 2))])
	grid = map

	monster = ['                  # ',
			   '#    ##    ##    ###',
			   ' #  #  #  #  #  #   ']

	monster_offsets = []
	for i in range(len(monster)):
		for j in range(len(monster[1])):
			if monster[i][j] == '#':
				monster_offsets.append((i, j))

	grid_width = len(grid)
	assert grid_width == GRID_SIZE * (SIZE - 2)
	for n in range(4):
		for i in range(len(grid) - 2):
			for j in range(len(grid[0]) + 1 - len(monster[1])):
				is_monster = True
				for i_offset, j_offset in monster_offsets:
					if grid[i + i_offset][j + j_offset] == '.':
						is_monster = False
						break
				if is_monster:
					for i_offset, j_offset in monster_offsets:
						grid[i + i_offset][j + j_offset] = 'O'
					#print_grid(grid)
					#import pdb; pdb.set_trace()

		new_grid = []
		for i in range(grid_width):
			new_grid.append([grid[grid_width - 1 - j][i] for j in range(grid_width)])

		grid = new_grid

	count = 0
	for i in range(grid_width):
		for j in range(grid_width):
			if grid[i][j] == '#':
				count += 1
	print_grid(grid)

	return count


def print_grid(grid):
	for line in grid:
		print(''.join(line))
	print('')
	print('')

def is_unique(edge, map):
	min_value = string_to_min_value(edge)
	return len(map[min_value]) == 1

print(main())
