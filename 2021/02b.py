def main():
	with open('02.dat', 'r') as file:
		x = 0
		y = 0
		aim = 0
		for line in file:
			parts = line.split()
			value = int(parts[1])
			if parts[0] == 'forward':
				x += value
				y += value * aim
			elif parts[0] == 'down':
				aim += value
			elif parts[0] == 'up':
				aim -= value
			else:
				raise 'how did I get here?'
		return x * y

print(main())
