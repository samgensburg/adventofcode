import re
from functools import reduce

class Rule:
	def __init__(self, input):
		self.text = input
		self.is_branch = False
		self.is_sequence = False
		self.is_char = False
		self.subrules = []
		self.char = None

		index = input.find('|')
		if index != -1:
			self.is_branch = True
			self.subrules.append(Rule(input[:index - 1]))
			self.subrules.append(Rule(input[index + 2:]))
		elif input[0].isdigit():
			self.is_sequence = True
			self.subrules = [int(rule_number) for rule_number in input.split()]
		else:
			assert len(input) == 3
			assert input[0] == '"'
			assert input[2] == '"'
			self.is_char = True
			self.char = input[1]

	def __str__(self):
		return self.text

def main():
	rules = {}
	counts = []
	with open('19.dat', 'r') as file:
		in_messages = False
		count = 0
		for line in file:
			line = line.strip()
			if in_messages:
				if is_valid(line, strings42, strings31):
					count += 1
			elif line:
				match = re.match(r'^(\d+):.*$', line)
				assert match
				rule_number = int(match.group(1))
				offset = len(match.group(1)) + 2
				rules[rule_number] = Rule(line[offset:])
			else:
				assert not in_messages
				in_messages = True
				cache = {}
				strings42 = get_strings(rules, cache, 42, 0)
				strings31 = get_strings(rules, cache, 31, 0)

		return count

def is_valid(string, strings42, strings31):
	#import pdb; pdb.set_trace()
	assert len(string) % 8 == 0
	chunk_count = len(string) // 8
	chunks = [string[i*8:i*8 + 8] for i in range(chunk_count)]
	state = 1
	for i in range(chunk_count):
		chunk = chunks[i]
		if state == 2:
			if chunk in strings31:
				continue
			return False

		if chunk in strings42:
			continue

		if chunk not in strings31 or i <= chunk_count // 2:
			return False

		state = 2
	return chunks[-1] in strings31


def get_strings(rules, cache, number, depth):
	if depth <= 5:
		print('  ' * depth + str(number))
	if number == 2001:
		import pdb; pdb.set_trace()
	if number in cache:
		return cache[number]

	rule = rules[number]
	out = get_strings_for_rule(rules, cache, rule, depth)
	cache[number] = out
	return out

def get_strings_for_rule(rules, cache, rule, depth):
	if rule.is_char:
		return {rule.char}
	if rule.is_sequence:
		if len(rule.subrules) == 1:
			return get_strings(rules, cache, rule.subrules[0], depth + 1)

		out = set()
		set0 = get_strings(rules, cache, rule.subrules[0], depth + 1)
		set1 = get_strings(rules, cache, rule.subrules[1], depth + 1)
		c = 0
		for string0 in set0:
			for string1 in set1:
				c += 1
				out.add(string0 + string1)
		return out
	return get_strings_for_rule(rules, cache, rule.subrules[0], depth).union(
		get_strings_for_rule(rules, cache, rule.subrules[1], depth))

def get_count(rules, number):
	if number in cache:
		return cache[number]
	rule = rules[number]
	out = get_count_for_rule(rules, rule)
	cache[number] = out
	return out

def get_count_for_rule(rules, rule):
	if rule.is_char:
		return 1
	elif rule.is_sequence:
		print(rule.subrules)
		assert len(rule.subrules) <= 2
		if len(rule.subrules) == 1:
			return get_count(rules, rule.subrules[0])
		else:
			return get_count(rules, rule.subrules[0]) * get_count(rules, rule.subrules[1])
	elif rule.is_branch:
		assert len(rule.subrules) == 2
		return get_count_for_rule(rules, rule.subrules[0]) + get_count_for_rule(rules, rule.subrules[1])
	else:
		assert False

print(main())
