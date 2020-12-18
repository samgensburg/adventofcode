def main():
	meters = set()
	with open('10.dat', 'r') as file:
		max = 0
		for line in file:
			line = line.strip()
			number = int(line)
			meters.add(number)
			if number > max:
				max = number

		last = 0
		count1 = 0
		count3 = 1
		for i in range(1, max + 1):
			if i in meters:
				difference = i - last
				last = i
				if difference == 1:
					count1 += 1
				elif difference == 3:
					count3 += 1
				else:
					assert difference == 2

		return count1 * count3

print(main())
