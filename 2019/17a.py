from collections import defaultdict, deque
from functools import reduce

class intcode:
	def __init__(self, program, inputs):
		self.values = program.copy()
		self.inputs = inputs.copy()
		self.done = False
		self.ip = 0
		self.rb = 0

	def add_input(self, input):
		self.inputs.append(input)

	def set_value(self, i, n):
		while i >= len(self.values):
			self.values.append(0)

		self.values[i] = n

	def get_value(self, i):
		while i >= len(self.values):
			self.values.append(0)

		return self.values[i]

	def run(self):
		while True:
			def get_value(n):
				if modes[n - 1] == 0:
					return self.get_value(self.get_value(self.ip + n))
				elif modes[n - 1] == 1:
					return self.get_value(self.ip + n)
				else:
					return self.get_value(self.get_value(self.ip + n) + self.rb)

			def set_value(n, value):
				if modes[n - 1] == 0:
					self.set_value(self.get_value(self.ip + n), value)
				elif modes[n - 1] == 1:
					print("I don't know what this means")
				elif modes[n - 1] == 2:
					self.set_value(self.get_value(self.ip + n) + self.rb, value)

			operation = self.get_value(self.ip)
			opcode = operation % 100
			modes = [operation // 100 % 10, operation // 1000 % 10, operation // 10000 % 10]

			if opcode == 1:
				set_value(3, get_value(1) + get_value(2))
				self.ip += 4
			elif opcode == 2:
				if modes[2] == 1:
					print("I still don't know what this means")
				set_value(3, get_value(1) * get_value(2))
				self.ip += 4
			elif opcode == 3:
				if len(self.inputs) == 0:
					return None
				set_value(1, self.inputs[0])
				self.inputs = self.inputs[1:]
				self.ip += 2
			elif opcode == 4:
				out = get_value(1)
				self.ip += 2
				return out
			elif opcode == 5:
				if get_value(1) != 0:
					self.ip = get_value(2)
				else:
					self.ip += 3
			elif opcode == 6:
				if get_value(1) == 0:
					self.ip = get_value(2)
				else:
					self.ip += 3
			elif opcode == 7:
				if get_value(1) < get_value(2):
					set_value(3, 1)
				else:
					set_value(3, 0)
				self.ip += 4
			elif opcode == 8:
				if get_value(1) == get_value(2):
					set_value(3, 1)
				else:
					set_value(3, 0)
				self.ip += 4
			elif opcode == 9:
				self.rb += get_value(1)
				self.ip += 2
			elif opcode == 99:
				self.done = True
				return None
			else:
				print("invalid opcode: " + str(opcode))
				break

def print_text(output):
	text = ''.join([chr(c) for c in output])
	print(text)

def output_to_grid(output_array):
	grid = []
	row = []
	for c in output_array:
		if c != ord('\n'):
			row.append(c)
		else:
			if len(row) > 0:
				grid.append(row)
			row = []
	assert len(row) == 0
	return grid

with open('17.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	program = [int(s) for s in strings]

	machine = intcode(program, [])
	output_array = []
	while True:
		output = machine.run()
		if output is None:
			break

		output_array.append(output)

	print_text(output_array)
	grid = output_to_grid(output_array)

	total = 0
	for row in range(1, len(grid) - 1):
		for column in range(1, len(grid[row]) - 1):
			#print((row, column))
			if (grid[row][column] == ord('#') and
					grid[row + 1][column] == ord('#') and
					grid[row - 1][column] == ord('#') and
					grid[row][column + 1] == ord('#') and
					grid[row][column - 1] == ord('#')):
				total += row * column

	print(total)
