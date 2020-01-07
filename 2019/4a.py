input = '272091-815432'

d = [0] * 6

for i in range(6):
	d[i] = int(input[i])

counter = 0
is_max = False
while not is_max:
	non_decreasing = True
	duplicate = False
	for i in range(5):
		if d[i + 1] < d[i]:
			non_decreasing = False
			break
		if d[i + 1] == d[i]:
			duplicate = True
	if duplicate and non_decreasing:
		counter += 1

	is_max = True
	for i in range(6):
		if d[i] < int(input[7 + i]):
			is_max = False
			break

	for i in range(5, -1, -1):
		d[i] += 1
		if d[i] == 10:
			d[i] = 0
		else:
			break

print(counter)
