import re

def main():
	with open('16.dat', 'r') as file:
		section = 1
		value_dict = {}
		nearby_tickets = []

		for line in file:
			line = line.strip()
			if not line:
				section += 1
			elif section == 1:
				match = re.match(r'^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$', line)
				assert match
				value_dict[match.group(1)] = (int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5)))
			elif section == 2:
				assert line == 'your ticket:'
				section += 1
			elif section == 3:
				my_ticket = [int(n) for n in line.split(',')]
			elif section == 4:
				assert line == 'nearby tickets:'
				section += 1
			else:
				assert section == 5
				nearby_tickets.append([int(n) for n in line.split(',')])

		total = 0
		for ticket in nearby_tickets:
			for value in ticket:
				found = False
				for key in value_dict:
					v1, v2, v3, v4 = value_dict[key]
					if value >= v1 and value <= v2:
						found = True
						break
					if value >= v3 and value <= v4:
						found = True
						break
				if not found:
					total += value
		return total

print(main())
