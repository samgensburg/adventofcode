from collections import defaultdict
from functools import reduce
from math import degrees, atan

def is_almost_int(f):
	diff = abs(f - round(f))
	return diff < 0.01

def are_in_line(a, b, i, j, x, y):
	if x == i:
		return a == i
	n = (y - j) / (x - i) * (a - x) + y
	if is_almost_int(n):
		n = round(n)
	else:
		return False
	return n == b

with open('10.dat', 'r') as file:
	grid = []
	for line in file:
		line = line.strip()
		row = [c == '#' for c in line]
		grid.append(row)

	count = reduce(lambda acc, val: val + acc, [reduce(lambda acc2, val2: 1 + acc2 if val2 else acc2, row, 0) for row in grid])
	width = len(grid[0])
	height = len(grid)
	max_count = 0
	for i in range(width):
		for j in range(height):
			if not grid[j][i]:
				continue

			asteroid_count = 0
			for x in range(width):
				for y in range(height):
					if not grid[y][x]:
						continue
					if y == j and x == i:
						continue

					visible = True
					if x == i:
						for n in range(height):
							if n > min(y, j) and n < max(y, j) and grid[n][x]:
								visible = False
								break
					else:
						if x < i:
							iterator = range(x + 1, i)
						else:
							iterator = range(x - 1, i, -1)
						for m in iterator:
							n = (y - j) / (x - i) * (m - x) + y
							if is_almost_int(n):
								n = round(n)
							else:
								continue
							if grid[n][m]:
								visible = False
								break
					if visible:
						asteroid_count += 1

			if asteroid_count > max_count:
				station_x = i
				station_y = j
				max_count = asteroid_count

	polar_coordinates = defaultdict(list)
	for x in range(width):
		for y in range(height):
			if x == station_x and y == station_y:
				continue
			if not grid[y][x]:
				continue

			if y == station_y:
				if x > station_x:
					direction = 90
				else:
					direction = 270
			else:
				if x >= station_x and y < station_y:
					quadrant = 0
				elif x > station_x and y > station_y:
					quadrant = 1
				elif x <= station_x and y > station_y:
					quadrant = 2
				else:
					quadrant = 3

				if quadrant == 0 or quadrant == 2:
					direction = 90 * quadrant + degrees(atan(abs((station_x - x)/(station_y - y))))
				else:
					direction = 90 + 90 * quadrant - degrees(atan(abs((station_x - x)/(station_y - y))))

			polar_coordinates[direction].append((x, y))
	keys = sorted(polar_coordinates.keys())
	for i in range(len(keys) - 1):
		if are_in_line(
				station_x, station_y,
				polar_coordinates[keys[i]][0][0], polar_coordinates[keys[i]][0][1],
				polar_coordinates[keys[i + 1]][0][0], polar_coordinates[keys[i + 1]][0][1]):
			polar_coordinates[keys[i + 1]].extend(polar_coordinates[keys[i]])
			del polar_coordinates[keys[i]]
	keys = sorted(polar_coordinates.keys())
	for key in keys:
		if key < 180:
			polar_coordinates[key] = sorted(polar_coordinates[key], key=lambda coords: coords[0] - 0.0001 * coords[1])
		else:
			polar_coordinates[key] = sorted(polar_coordinates[key], key=lambda coords: -coords[0] + 0.0001 * coords[1])

	count = 0
	while count < 299:
		for key in keys:
			print(key, polar_coordinates[key])
			if len(polar_coordinates[key]) == 0:
				continue

			count += 1
			print(str(count) + ": " + str(polar_coordinates[key][0]))
#			if count == 200:
#				print(polar_coordinates[key][0])
#				break
#			else:
			polar_coordinates[key] = polar_coordinates[key][1:]
			print("remaining: " + str(reduce(lambda acc, val: acc + len(val), polar_coordinates.values(), 0)))
