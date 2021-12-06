def main():
	with open('02.dat', 'r') as file:
		x = 0
		y = 0
		for line in file:
			parts = line.split()
			value = int(parts[1])
			if parts[0] == 'forward':
				x += value
			elif parts[0] == 'down':
				y += value
			elif parts[0] == 'up':
				y -= value
			else:
				raise 'how did I get here?'
		return x * y

print(main())
