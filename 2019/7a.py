def run_intcode(program, inputs):
	values = program.copy()
	ip = 0
	while True:
		opcode = values[ip] % 100
		modes = [values[ip] // 100 % 10, values[ip] // 1000 % 10, values[ip] // 10000 % 10]
		get_value = lambda n: values[ip + n] if modes[n - 1] == 1 else values[values[ip + n]]
		if opcode == 1:
			if modes[2] == 1:
				print("I don't know what this means")
			values[values[ip + 3]] = get_value(1) + get_value(2)
			ip += 4
		elif opcode == 2:
			if modes[2] == 1:
				print("I still don't know what this means")
			values[values[ip + 3]] = get_value(1) * get_value(2)
			ip += 4
		elif opcode == 3:
			if modes[0] == 1:
				print("Really no idea")
			values[values[ip + 1]] = inputs[0]
			inputs = inputs[1:]
			ip += 2
		elif opcode == 4:
			if modes[0] == 1:
				return values[ip + 1]
			else:
				return values[values[ip + 1]]
			ip += 2
		elif opcode == 5:
			if get_value(1) != 0:
				ip = get_value(2)
			else:
				ip += 3
		elif opcode == 6:
			if get_value(1) == 0:
				ip = get_value(2)
			else:
				ip += 3
		elif opcode == 7:
			if get_value(1) < get_value(2):
				values[values[ip + 3]] = 1
			else:
				values[values[ip + 3]] = 0
			ip += 4
		elif opcode == 8:
			if get_value(1) == get_value(2):
				values[values[ip + 3]] = 1
			else:
				values[values[ip + 3]] = 0
			ip += 4
		elif opcode == 99:
			break
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
	strings = text.split(',')
	program = [int(s) for s in strings]
	max = -1
	for permutation in list_permutations([0, 1, 2, 3, 4]):
		output = 0
		for i in range(5):
			output = run_intcode(program, [permutation[i], output])
		if output > max:
			max = output
	print(max)
