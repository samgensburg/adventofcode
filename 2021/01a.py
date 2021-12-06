def main():
	with open('01.dat', 'r') as file:
		last = -1
		count = 0
		for line in file:
			current = int(line)
			if last != -1 and current > last:
				count += 1
			last = current
		return count

print(main())
