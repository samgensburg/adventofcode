width = 25
height = 6

with open('8.dat', 'r') as file:
	text = file.read()
	text = text.strip()
	layer_count = len(text) // (width * height)
	values = [2] * width * height
	for i in range(len(text)):
		layer_index = i % (width * height)
		if values[layer_index] == 2:
			values[layer_index] = int(text[i])
		print(values)

	i = 0
	s = ''
	for m in values:
		s = s + ('X' if m else ' ')
		if i % width == width - 1:
			print(s)
			s = ''
		i += 1
