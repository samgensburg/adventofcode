from collections import defaultdict
from functools import reduce
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

		valid_tickets = [my_ticket]
		for ticket in nearby_tickets:
			valid = True
			for value in ticket:
				found = False
				for key in value_dict:
					v1, v2, v3, v4 = value_dict[key]
					if valid_value(value, value_dict[key]):
						found = True
						break
					if value >= v3 and value <= v4:
						found = True
						break
				if not found:
					valid = False
					break
			if valid:
				valid_tickets.append(ticket)

		cache = defaultdict(dict)
		for key in value_dict:
			tuple = value_dict[key]
			for i in range(len(value_dict)):
				cache[key][i] = True
				for ticket in valid_tickets:
					value = ticket[i]
					if not valid_value(value, tuple):
						cache[key][i] = False
						break

		found = True
		while found:
			found = False
			for i in range(len(cache)):
				if only_one_true([cache[key][i] for key in cache]):
					for key in cache:
						if cache[key][i]:
							for j in range(len(cache)):
								if i != j and cache[key][j]:
									cache[key][j] = False
									found = True
			for key in cache:
				if only_one_true(cache[key]):
					for i in range(len(cache)):
						if cache[key][i]:
							for key2 in cache:
								if key != key2 and cache[key2][i]:
									cache[key2][i] = False
									found = True

		sequence = find_valid_sequence(set(value_dict.keys()), 0, valid_tickets, value_dict, cache)
		product = 1
		for i in range(len(sequence)):
			key = sequence[i]
			if key[:9] == 'departure':
				product *= my_ticket[i]
		return product

def only_one_true(bools):
	count = reduce(lambda count, bool: count + 1 if bool else count, bools, 0)
	return count == 1

def find_valid_sequence(key_set, index, tickets, value_dict, cache):
	out = None
	if len(key_set) == 0:
		return []

	for key in key_set:
		if index < 3:
			print(str(index) + ': ' + key)
		if not cache[key][index]:
			continue

		sub = find_valid_sequence(key_set - {key}, index + 1, tickets, value_dict, cache)
		if sub is not None:
			assert out is None
			sub.insert(0, key)
			out = sub
	return out

def valid_value(value, tuple):
	v1, v2, v3, v4 = tuple
	if value >= v1 and value <= v2:
		return True
	if value >= v3 and value <= v4:
		return True
	return False

print(main())
