with open('2a.dat', 'r') as file:
	text = file.read()
	strings = text.split(',')
	values = [int(s) for s in strings]
	values[1] = 12
	values[2] = 2
	for i in range(0, len(values), 4):
		if values[i] == 1:
			values[values[i + 3]] = values[values[i + 1]] + values[values[i + 2]]
		elif values[i] == 2:
			values[values[i + 3]] = values[values[i + 1]] * values[values[i + 2]]
		elif values[i] == 99:
			break
		else:
			print("invalid opcode")

print(values[0])
