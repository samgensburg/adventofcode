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

def sgn(i):
	if i > 0:
		return 1
	elif i == 0:
		return 0
	else:
		return -1

def run_search(machine, full):
	grid = dict()
	queue = deque([(0, 0)])
	grid[(0, 0)] = []
	while len(queue) > 0:
		print(queue)
		loc_x, loc_y = queue.popleft()
		actions = grid[(loc_x, loc_y)]
		if full:
			print(len(actions))
		for action in actions:
			machine.add_input(action)
			out = machine.run()
			assert out == 1

		for direction in range(1, 5):
			machine.add_input(direction)
			out = machine.run()
			if out == 2 and not full:
				print(actions, direction)
				print(len(actions) + 1)
				return
			elif out == 1 or out == 2:
				new_actions = actions.copy()
				new_actions.append(direction)
				if direction == 1:
					new_loc_x, new_loc_y = loc_x, loc_y + 1
					new_direction = 2
				if direction == 2:
					new_loc_x, new_loc_y = loc_x, loc_y - 1
					new_direction = 1
				if direction == 3:
					new_loc_x, new_loc_y = loc_x - 1, loc_y
					new_direction = 4
				if direction == 4:
					new_loc_x, new_loc_y = loc_x + 1, loc_y
					new_direction = 3

				machine.add_input(new_direction)
				out = machine.run()
				assert out == 1 or out == 2
				if not (new_loc_x, new_loc_y) in grid:
					grid[(new_loc_x, new_loc_y)] = new_actions
					queue.append((new_loc_x, new_loc_y))
			else:
				# Can you really do NOTHING here?!
				pass

		for i in range(len(actions) - 1, -1, -1):
			action = actions[i]
			if action == 1:
				reverse_action = 2
			if action == 2:
				reverse_action = 1
			if action == 3:
				reverse_action = 4
			if action == 4:
				reverse_action = 3

			machine.add_input(reverse_action)
			out = machine.run()
			assert out == 1 or out == 2

with open('15.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	program = [int(s) for s in strings]

	machine = intcode(program, [])
	run_search(machine, False)
	run_search(machine, True)
