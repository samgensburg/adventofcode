from collections import defaultdict
import re

def sgn(i):
	if i > 0:
		return 1
	elif i == 0:
		return 0
	else:
		return -1

def gcd(a, b):
    while b > 0:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b / gcd(a, b)

pattern = re.compile(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>')
positions = []
velocities = [[0] * 3 for i in range(4)]
with open('12.dat', 'r') as file:
	for line in file:
		match = pattern.match(line.strip())
		assert match
		positions.append([int(match.group(1)), int(match.group(2)), int(match.group(3))])

repeat_info = []
for index in range(3):
	visited = defaultdict(list)
	cycle = -1
	while True:
		cycle += 1
		key = (positions[0][index], positions[1][index], positions[2][index], positions[3][index],
				velocities[0][index], velocities[1][index], velocities[2][index], velocities[3][index])
		if len(visited[key]) > 0:
			repeat_info.append((visited[key][0], cycle))
			break
		visited[key].append(cycle)
		for moon in range(4):
			for other_moon in range(4):
				velocities[moon][index] += sgn(positions[other_moon][index] - positions[moon][index])

		for moon in range(4):
			positions[moon][index] += velocities[moon][index]

assert repeat_info[0][0] == 0
assert repeat_info[1][0] == 0
assert repeat_info[2][0] == 0

print(lcm(lcm(repeat_info[0][1], repeat_info[1][1]), repeat_info[2][1]))
