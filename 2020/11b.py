def main():
	data = []
	with open('11.dat', 'r') as file:
		max = 0
		for line in file:
			line = line.strip()
			data.append(line)

	height = len(data)
	width = len(data[0])
	repeat = True
	while repeat:
		repeat = False
		new_data = []
		for i in range(height):
			new_data.append([])
			for j in range(width):
				seat =  data[i][j]
				if seat == '.':
					new_data[i].append('.')
				else:
					count = get_count(data, i, j, height, width)
					if seat == 'L':
						if count == 0:
							new_data[i].append('#')
							repeat = True
						else:
							new_data[i].append('L')
					else:
						if count < 5:
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

def get_count(data, i, j, height, width):
	count = 0
	count += peer(data, i, j, -1, -1, height, width)
	count += peer(data, i, j, -1, 0, height, width)
	count += peer(data, i, j, -1, 1, height, width)
	count += peer(data, i, j, 0, -1, height, width)
	count += peer(data, i, j, 0, 1, height, width)
	count += peer(data, i, j, 1, -1, height, width)
	count += peer(data, i, j, 1, 0, height, width)
	count += peer(data, i, j, 1, 1, height, width)
	return count

def peer(data, i, j, delta_i, delta_j, height, width):
	assert delta_i or delta_j
	while True:
		i += delta_i
		j += delta_j
		if not on_map(i, j, height, width):
			return 0
		seat = data[i][j]
		if seat == 'L':
			return 0
		if seat == '#':
			return 1

def on_map(i, j, height, width):
	return i >= 0 and j >= 0 and i < height and j < width


print(main())
