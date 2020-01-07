class intcode:
	def __init__(self, program, inputs):
		self.values = program.copy()
		self.inputs = inputs.copy()
		self.done = False
		self.ip = 0

	def add_input(self, input):
		self.inputs.append(input)

	def run(self):
		while True:
			opcode = self.values[self.ip] % 100
			modes = [self.values[self.ip] // 100 % 10, self.values[self.ip] // 1000 % 10, self.values[self.ip] // 10000 % 10]
			get_value = lambda n: self.values[self.ip + n] if modes[n - 1] == 1 else self.values[self.values[self.ip + n]]
			if opcode == 1:
				if modes[2] == 1:
					print("I don't know what this means")
				self.values[self.values[self.ip + 3]] = get_value(1) + get_value(2)
				self.ip += 4
			elif opcode == 2:
				if modes[2] == 1:
					print("I still don't know what this means")
				self.values[self.values[self.ip + 3]] = get_value(1) * get_value(2)
				self.ip += 4
			elif opcode == 3:
				if modes[0] == 1:
					print("Really no idea")
				self.values[self.values[self.ip + 1]] = self.inputs[0]
				self.inputs = self.inputs[1:]
				self.ip += 2
			elif opcode == 4:
				if modes[0] == 1:
					out = self.values[self.ip + 1]
				else:
					out = self.values[self.values[self.ip + 1]]
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
					self.values[self.values[self.ip + 3]] = 1
				else:
					self.values[self.values[self.ip + 3]] = 0
				self.ip += 4
			elif opcode == 8:
				if get_value(1) == get_value(2):
					self.values[self.values[self.ip + 3]] = 1
				else:
					self.values[self.values[self.ip + 3]] = 0
				self.ip += 4
			elif opcode == 99:
				self.done = True
				return None
			else:
				print("invalid opcode: " + str(opcode))
				break

def list_permutations(values):
	if len(values) == 1:
		return [[values[0]]]

	permutations = []
	for value in values:
		sub_values = values.copy()
		sub_values.remove(value)
		prefixes = list_permutations(sub_values)
		for prefix in prefixes:
			prefix.append(value)
			permutations.append(prefix)
	return permutations

with open('7.dat', 'r') as file:
	text = file.read()
#	text = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
	strings = text.split(',')
	program = [int(s) for s in strings]
	max = -1
	for permutation in list_permutations([5, 6, 7, 8, 9]):
		output = 0
		machines = [intcode(program, [permutation[i]]) for i in range(5)]
		i = 0
		while True:
			print(permutation, i, output)
			machine = machines[i]
			machine.add_input(output)
			new_output = machine.run()
			if new_output is None:
				total = output
				break
			output = new_output
			i = (i + 1) % 5

		if total > max:
			max = total
	print(max)
