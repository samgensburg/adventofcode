SUM = 1124361034

def main():
	with open('9.dat', 'r') as file:
		running = []
		for line in file:
			line = line.strip()
			number = int(line)

			trim = 0
			for i in range(len(running)):
				inner_min, inner_max, total = running[i]
				total += number
				if total <= SUM:
					if number < inner_min:
						inner_min = number
					elif number > inner_max:
						inner_max = number
					if total == SUM:
						return inner_min + inner_max
					running[i] = (inner_min, inner_max, total)
				else:
					trim += 1

			running = running[trim:]
			running.append((number, number, number))

print(main())
