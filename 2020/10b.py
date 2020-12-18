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
		ways_running = [1]
		ways_running.append(1 if 1 in meters else 0)
		ways_running.append(ways_running[0] + ways_running[1] if 2 in meters else 0)
		for i in range(3, max + 1):
			if i in meters:
				ways = ways_running[i - 1] + ways_running[i - 2] + ways_running[i - 3]
			else:
				ways = 0
			ways_running.append(ways)
		return ways_running[max]

print(main())
