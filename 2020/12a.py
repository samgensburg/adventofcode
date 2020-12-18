def main():
	waypoint_x = 10
	waypoint_y = 1
	x = 0
	y = 0
	with open('12.dat', 'r') as file:
		for line in file:
			line = line.strip()
			direction = line[0]
			value = int(line[1:])

			if direction == 'F':
				x += waypoint_x * value
				y += waypoint_y * value
			elif direction == 'E':
				waypoint_x += value
			elif direction == 'W':
				waypoint_x -= value
			elif direction == 'N':
				waypoint_y += value
			elif direction == 'S':
				waypoint_y -= value
			elif direction == 'L' or direction == 'R':
				if direction == 'R':
					value = 360 - value
				value //= 90
				for _ in range(value):
					waypoint_x, waypoint_y = -waypoint_y, waypoint_x
			else:
				assert False
	return abs(x) + abs(y)

print(main())
