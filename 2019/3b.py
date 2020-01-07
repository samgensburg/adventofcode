def loop_instructions(instructions, action):
	directions = {
		'U': lambda loc: (loc[0], loc[1] + 1),
		'D': lambda loc: (loc[0], loc[1] - 1),
		'R': lambda loc: (loc[0] + 1, loc[1]),
		'L': lambda loc: (loc[0] - 1, loc[1])
	}

	loc = (0, 0)
	d = 0
	for instruction in instructions:
		direction = directions[instruction[0]]
		distance = int(instruction[1:])
		for i in range(distance):
			d += 1
			loc = direction(loc)
			action(loc, d)

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

	locations = {}
	overlaps = {}

	def set_locations(loc, d):
		if not loc in locations:
			locations[loc] = d

	def set_overlap(loc, d):
		if loc in locations:
			overlaps[loc] = d + locations[loc]

	loop_instructions(instructions1, set_locations)
	loop_instructions(instructions2, set_overlap)

	min = -1
	for loc in overlaps:
		distance = overlaps[loc]
		if min == -1 or distance < min:
			min = distance
	print(min)
