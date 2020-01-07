with open('5.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	values = [int(s) for s in strings]
	inputs = [1]

	ip = 0
	while True:
		opcode = values[ip] % 100
		modes = [values[ip] // 100 % 10, values[ip] // 1000 % 10, values[ip] // 10000 % 10]
		if opcode == 1:
			value1 = values[ip + 1] if modes[0] == 1 else values[values[ip + 1]]
			value2 = values[ip + 2] if modes[1] == 1 else values[values[ip + 2]]
			if modes[2] == 1:
				print("I don't know what this means")
			values[values[ip + 3]] =  value1 + value2
			ip += 4
		elif opcode == 2:
			value1 = values[ip + 1] if modes[0] == 1 else values[values[ip + 1]]
			value2 = values[ip + 2] if modes[1] == 1 else values[values[ip + 2]]
			if modes[2] == 1:
				print("I still don't know what this means")
			values[values[ip + 3]] =  value1 * value2
			ip += 4
		elif opcode == 3:
			if modes[0] == 1:
				print("Really no idea")
			values[values[ip + 1]] = inputs[0]
			inputs = inputs[1:]
			ip += 2
		elif opcode == 4:
			if modes[0] == 1:
				print(values[ip + 1])
			else:
				print(values[values[ip + 1]])
			ip += 2
		elif opcode == 99:
			break
		else:
			print("invalid opcode: " + str(opcode))
			break
