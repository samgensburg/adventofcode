import re

def sgn(i):
	if i > 0:
		return 1
	elif i == 0:
		return 0
	else:
		return -1

pattern = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
positions = []
velocities = [[0] * 3 for i in range(4)]
with open('12.dat', 'r') as file:
	for line in file:
		match = pattern.match(line.strip())
		assert match
		positions.append([int(match.group(1)), int(match.group(2)), int(match.group(3))])

for cycle in range(1000):
	for moon in range(4):
		for other_moon in range(4):
			for index in range(3):
				velocities[moon][index] += sgn(positions[other_moon][index] - positions[moon][index])

	for moon in range(4):
		for index in range(3):
			positions[moon][index] += velocities[moon][index]

energy = 0
for moon in range(4):
	energy += (abs(positions[moon][0]) + abs(positions[moon][1]) + abs(positions[moon][2])) * (
				abs(velocities[moon][0]) + abs(velocities[moon][1]) + abs(velocities[moon][2]))

print(energy)
