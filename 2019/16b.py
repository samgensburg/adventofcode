def get_sign(n, m):
	numbers = [0, 1, 0, -1]
	offset = ((n + 1) % (4 * (m + 1))) // (m + 1)
	return numbers[offset]

cache = dict()
def get_value(n, cycle):
	if n % 100000 == 0:
		print(n, cycle)
	if (n, cycle) in cache:
		return cache[(n, cycle)]

	sum = 0
	for i in range(n - 1, total_length):
		sum += get_value(i, cycle - 1)

	value = abs(sum) % 10
	cache[(n, cycle)] = value
	return value

with open('16.dat', 'r') as file:
	offset = 5971269
	text = file.read().strip()

#	offset = 303673
#	text = '03036732577212944063491565474664'
	array = [int(c) for c in text] * 10000
	total_length = len(array)
	for i in range(total_length):
		cache[(i, 0)] = array[i]


	for cycle in range(1, 100):
		sum = 0
		for n in range(total_length - 1, offset - 101 + cycle, -1):
			sum += get_value(n, cycle - 1)
			cache[(n, cycle)] = abs(sum) % 10

	out = 0
	for i in range(8):
		out *= 10
		out += get_value(offset + i + 1, 100)
		print(get_value(offset + i + 1, 100))

	print(out)
