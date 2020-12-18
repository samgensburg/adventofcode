def main():
	facing = 0
	x = 0
	y = 0
	with open('12.dat', 'r') as file:
		for line in file:
			line = line.strip()
			direction = line[0]
			value = int(line[1:])

			if direction == 'F':
				if facing == 0:
					direction = 'E'
				elif facing == 90:
					direction = 'N'
				elif facing == 180:
					direction = 'W'
				elif facing == 270:
					direction = 'S'
				else:
					assert False
			if direction == 'E':
				x += value
			elif direction == 'W':
				x -= value
			elif direction == 'N':
				y += value
			elif direction == 'S':
				y -= value
			elif direction == 'L':
				facing = (facing + value) % 360
			elif direction == 'R':
				facing = (facing - value) % 360
			else:
				assert False
	return abs(x) + abs(y)

print(main())
