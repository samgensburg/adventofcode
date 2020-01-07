from collections import defaultdict

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

with open('11.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	program = [int(s) for s in strings]
	max = -1

	machine = intcode(program, [])
	grid = defaultdict(lambda: defaultdict(int))
	loc = (0, 0)
	direction = 1
	painted = set()
	grid[0][0] = 1
	while True:
		machine.add_input(grid[loc[0]][loc[1]])
		color_output = machine.run()
		if color_output is None:
			break
		assert color_output == 0 or color_output == 1
		grid[loc[0]][loc[1]] = color_output
		painted.add(loc)
		turn_output = machine.run()
		if turn_output is None:
			break
		assert turn_output == 0 or turn_output == 1
		if turn_output == 0:
			direction += 1
		else:
			direction -= 1

		direction %= 4

		if direction == 0:
			loc = (loc[0] + 1, loc[1])
		elif direction == 1:
			loc = (loc[0], loc[1] + 1)
		elif direction == 2:
			loc = (loc[0] - 1, loc[1])
		elif direction == 3:
			loc = (loc[0], loc[1] - 1)
		else:
			assert False

	min_x = 0
	max_x = 0
	min_y = 0
	max_y = 0
	for square in painted:
		x, y = square
		if x < min_x:
			min_x = x
		elif x > max_x:
			max_x = x

		if y < min_y:
			min_y = y
		elif y > max_y:
			max_y = y

	for y in range(max_y, min_y - 1, -1):
		string = ''.join(['#' if c == 1 else '.' for c in [grid[x][y] for x in range(min_x, max_x + 1)]])
		print(string)
