total = 0
with open('1a.dat', 'r') as file:
	for line in file:
		num = int(line)
		fuel = num // 3 - 2
		total += fuel
print(total)
