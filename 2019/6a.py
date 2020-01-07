from collections import defaultdict

data = defaultdict(list)

def get_orbits(planet):
	satellites = data[planet]
	total = 0
	satellite_count = 0
	for satellite in satellites:
		satellite_total, satellite_satellite_count = get_orbits(satellite)
		satellite_count += 1 + satellite_satellite_count
		total += satellite_total + satellite_satellite_count + 1
	return total, satellite_count

with open('6.dat', 'r') as file:
	planets = set()
	for line in file:
		objects = line.split(")")
		data[objects[0]].append(objects[1].strip())
		planets.add(objects[0])

	max = 0
	for key in planets:
		value, _ = get_orbits(key)
		if value > max:
			max = value

	print(max)
