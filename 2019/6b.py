data = dict()
with open('6.dat', 'r') as file:
	for line in file:
		objects = line.split(")")
		data[objects[1].strip()] = objects[0]

	transfers = 0
	loc = "YOU"
	transfers_required = dict()
	while loc in data:
		orbitting = data[loc]
		transfers_required[orbitting] = transfers
		loc = orbitting
		transfers += 1

	loc = "SAN"
	transfers = 0
	while loc in data:
		orbitting = data[loc]
		if orbitting in transfers_required:
			print(transfers_required[orbitting] + transfers)
			break
		transfers += 1
		loc = orbitting
