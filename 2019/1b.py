total = 0
with open('1a.dat', 'r') as file:
	for line in file:
		num = int(line)
		while num > 8:
			fuel = num // 3 - 2
			total += fuel
			num = fuel
print(total)
