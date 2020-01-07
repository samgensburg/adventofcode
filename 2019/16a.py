with open('16.dat', 'r') as file:
	text = file.read().strip()
	values = [int(c) for c in text] * 10000
	patterns = []
	for n in range(len(values)):
		print(n)
		pattern = []
		repeat = 0
		while len(pattern) <= len(values):
			if repeat == 1:
				number = 1
			elif repeat == 3:
				number = -1
			else:
				number = 0

			repeat = (repeat + 1) % 4
			pattern.extend([number] * (n + 1))
		pattern = pattern[1:]
		patterns.append(pattern)

	for cycle in range(100):
		print(str(cycle) + ': ' + str(values[:8]))
		new_values = []
		for n in range(len(values)):
			value = 0
			for m in range(len(values)):
				value += values[m] * patterns[n][m]
			new_values.append(abs(value) % 10)
		values = new_values

	print(values[:8])
