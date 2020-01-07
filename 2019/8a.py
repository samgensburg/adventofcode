width = 25
height = 6

with open('8.dat', 'r') as file:
	text = file.read()
	text = text.strip()
	layer_count = len(text) // (25 * 6)
	counts = [[0] * 3 for i in range(layer_count)]
	for i in range(len(text)):
		print(counts)
		value = int(text[i])
		if value < 3:
			counts[i // (25 * 6)][value] += 1
	min_value = 0
	min_count = counts[0][0] + 1
	for count in counts:
		print(count)
		if count[0] < min_count:
			min_count = count[0]
			min_value = count[1] * count[2]
	print(min_value)
