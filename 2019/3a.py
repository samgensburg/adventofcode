def loop_instructions(instructions, action):
	directions = {
		'U': lambda loc: (loc[0], loc[1] + 1),
		'D': lambda loc: (loc[0], loc[1] - 1),
		'R': lambda loc: (loc[0] + 1, loc[1]),
		'L': lambda loc: (loc[0] - 1, loc[1])
	}

	loc = (0, 0)
	for instruction in instructions:
		direction = directions[instruction[0]]
		distance = int(instruction[1:])
		for i in range(distance):
			loc = direction(loc)
			action(loc)

with open('3.dat', 'r') as file:
	i = 0
	for line in file:
		if i == 0:
			line1 = line
		elif i == 1:
			line2 = line
		i += 1
	instructions1 = line1.split(',')
	instructions2 = line2.split(',')

	locations = set()
	overlaps = set()

	loop_instructions(instructions1, lambda loc: locations.add(loc))
	loop_instructions(instructions2, lambda loc: overlaps.add(loc) if loc in locations else None)

	min = -1
	for overlap in overlaps:
		distance = abs(overlap[0]) + abs(overlap[1])
		if min == -1 or distance < min:
			min = distance
	print(min)
