def main():
	with open('6.dat', 'r') as file:
		items = default_set
		total = 0
		for line in file:
			line = line.strip()

			if line:
				items = items.intersection(make_set(line))
			else:
				total += len(items)
				items = default_set
		total += len(items)
		return(total)

make_set = lambda line: set([c for c in line])
default_set = make_set('abcdefghijklmnopqrstuvwxyz')

print(main())
