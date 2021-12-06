def main():
	with open('01.dat', 'r') as file:
		previous = [-1] * 3
		count = 0
		for line in file:
			current = int(line)
			if previous[0] != -1 and current > previous[0]:
				count += 1
			previous[0] = previous[1]
			previous[1] = previous[2]
			previous[2] = current
		return count

print(main())
