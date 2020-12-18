def main():
	data = []
	with open('11.dat', 'r') as file:
		max = 0
		for line in file:
			line = line.strip()
			data.append(line)

	repeat = True
	while repeat:
		repeat = False
		new_data = []
		for i in range(len(data)):
			new_data.append([])
			for j in range(len(data[0])):
				seat =  data[i][j]
				if seat == '.':
					new_data[i].append('.')
				else:
					count = get_count(data, i, j)
					if seat == 'L':
						if count == 0:
							new_data[i].append('#')
							repeat = True
						else:
							new_data[i].append('L')
					else:
						if count < 4:
							new_data[i].append('#')
						else:
							new_data[i].append('L')
							repeat = True
		data = new_data

	count = 0
	for i in range(len(data)):
		for j in range(len(data[0])):
			if data[i][j] == '#':
				count += 1
	return count

def get_count(data, i, j):
	count = 0
	above = i != 0
	below = i != len(data) - 1
	left = j != 0
	right = j != len(data[0]) - 1
	if above:
		if left and data[i - 1][j - 1] == '#':
			count += 1
		if data[i - 1][j] == '#':
			count += 1
		if right and data[i - 1][j + 1] == '#':
			count += 1
	if left and data[i][j - 1] == '#':
		count += 1
	if right and data[i][j + 1] == '#':
		count += 1
	if below:
		if left and data[i + 1][j - 1] == '#':
			count += 1
		if data[i + 1][j] == '#':
			count += 1
		if right and data[i + 1][j + 1] == '#':
			count += 1
	return count



print(main())
