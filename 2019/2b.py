with open('2a.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	for noun in range(100):
		for verb in range(100):
			values = [int(s) for s in strings]
			values[1] = noun
			values[2] = verb
			for i in range(0, len(values), 4):
				if values[i] == 1:
					values[values[i + 3]] = values[values[i + 1]] + values[values[i + 2]]
				elif values[i] == 2:
					values[values[i + 3]] = values[values[i + 1]] * values[values[i + 2]]
				elif values[i] == 99:
					break
				else:
					print("invalid opcode")
			if values[0] == 19690720:
				print(100 * noun + verb)
