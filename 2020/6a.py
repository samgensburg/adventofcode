def main():
	with open('6.dat', 'r') as file:
		items = set()
		total = 0
		for line in file:
			line = line.strip()
			if line:
				for c in line:
					items.add(c)
			else:
				total += len(items)
				print(total)
				items = set()
		total += len(items)
		print(total)

print(main())
