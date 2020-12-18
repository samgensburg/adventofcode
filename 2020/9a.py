def main():
	with open('9.dat', 'r') as file:
		last25 = []
		for line in file:
			line = line.strip()
			number = int(line)
			missing = False
			if len(last25) == 25:
				old_number, value_set = last25[0]
				last25 = last25[1:]
				missing = True
				if number in value_set:
					missing = False

			for i in range(len(last25)):
				old_number, value_set = last25[i]
				if number in value_set:
					missing = False
				value_set.add(number + old_number)

			last25.append((number, set()))

			if missing:
				print(last25)
				return number


print(main())
