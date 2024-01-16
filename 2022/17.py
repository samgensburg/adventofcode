from collections import defaultdict
from itertools import cycle
from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

LEFT = -1
RIGHT = 1
FALL = 0

FALLING = '@'
EMPTY = '.'
SOLID = '#'

ROCKS = [['@@@@', '....', '....', '....'],
         ['.@..', '@@@.', '.@..', '....'],
         ['@@@.', '..@.', '..@.', '....'],
		 ['@...', '@...', '@...', '@...'],
		 ['@@..', '@@..', '....', '....']]

def process_input(lines):
	return [LEFT if c == '<' else RIGHT for c in lines[0]]

class Board():
	def __init__(self, winds) -> None:
		self.board = []
		self.max_height = 0
		self.winds = winds
		self.winds_index_cycle = cycle(range(len(winds)))

	def get_wind(self):
		self.last_winds_index = next(self.winds_index_cycle)
		return self.winds[self.last_winds_index]

	def get_init_loc(self):
		while len(self.board) < self.max_height + 8:
			self.board.append([EMPTY] * 7)

		return (2, self.max_height + 3)

	def try_action(self, action, rock, loc):
		x, y = loc
		for i in range(4):
			for j in range(4):
				assert y + i >= self.max_height or x + j >= 7 or rock[i][j] == EMPTY or self.board[y + i][x + j] == EMPTY

		if action == FALL:
			if y == 0:
				return False
			
			for i in range(4):
				for j in range(4):
					if rock[i][j] == EMPTY:
						continue

					if self.board[y + i - 1][x + j] == SOLID:
						return False
		
		elif action == LEFT:
			if x == 0:
				return False

			for i in range(4):
				for j in range(4):
					if rock[i][j] == EMPTY:
						continue

					if self.board[y + i][x + j - 1] == SOLID:
						return False
		
		else:
			assert action == RIGHT
			for i in range(4):
				for j in range(4):
					if rock[i][j] == EMPTY:
						continue

					if x + j + 1 >= 7:
						return False
					if self.board[y + i][x + j + 1] == SOLID:
						return False

		return True

	def solidify(self, rock, loc):
		x, y = loc
		for i in range(4):
			for j in range(4):
				assert rock[i][j] == EMPTY or self.board[y + i][x + j] == EMPTY
				if rock[i][j] == FALLING:
					self.board[y + i][x + j] = SOLID

					self.max_height = max(self.max_height, y + i + 1)

	def hash(self, rock_index):
		if self.max_height < 20:
			return None
		out = ''
		for row in self.board[-25:]:
			out += ''.join(row)
		out += 'X' + str(rock_index) + 'X'
		out += 'X' + str(self.last_winds_index) + 'X'
		return out

	def display_full(self):
		for i in range(len(self.board) - 1, -1, -1):
			line = self.board[i]
			print('|' + ''.join(line) + '|')
		print ('+-------+')

def drop(rock, board):
	x, y = board.get_init_loc()
	while True:
		action = board.get_wind()
		if board.try_action(action, rock, (x, y)):
			x += action
		if board.try_action(FALL, rock, (x, y)):
			y -= 1
		else:
			board.solidify(rock, (x, y))
			return

def solve_a(winds, count=2022):
	board = Board(winds)
	rock_index_cycle = cycle(range(5))
	for _ in range(count):
		rock_index = next(rock_index_cycle)
		drop(ROCKS[rock_index], board)

	return board.max_height

def solve_b(winds):
	count = 1000000000000
	board = Board(winds)
	rock_index_cycle = cycle(range(5))
	hash_lookup = dict()
	i = 0
	jumped = False
	while i < count:
		rock_index = next(rock_index_cycle)
		drop(ROCKS[rock_index], board)
		if not jumped:
			hash = board.hash(rock_index)
			if hash == None:
				pass
			elif hash in hash_lookup:
				i_old, height_old = hash_lookup[hash]
				loop_length = i - i_old
				height_diff = board.max_height - height_old
				loop_count = (count - i) // loop_length - 1
				i += loop_length * loop_count
				height_offset = height_diff * loop_count
				jumped = True
			else:
				hash_lookup[hash] = (i, board.max_height)
		i += 1
		if i % 10 == 0:
			#import pdb; pdb.set_trace()
			print(i // 10)


	return board.max_height + height_offset

def main():
	assert solve_a(process_input(['>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'])) == 3068
	with open(DATA_FILE, 'r') as file:
		lines = file.read().strip().split('\n')
	input = process_input(lines)
	assert solve_a(input) == 3151
	return solve_a(input), solve_b(input)


print(main())
