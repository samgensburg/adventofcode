with open('5.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	values = [int(s) for s in strings]
	inputs = [5]
#	values = [3,9,8,9,10,9,4,9,99,-1,8]

	ip = 0
	while True:
#		print(ip)
#		print(values)
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
				print(values[ip + 1])
			else:
				print(values[values[ip + 1]])
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
