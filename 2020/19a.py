import re

class Rule:
	def __init__(self, input):
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

def main():
	rules = {}
	with open('19.dat', 'r') as file:
		in_messages = False
		count = 0
		for line in file:
			line = line.strip()
			if in_messages:
				if line in strings:
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
				strings = get_strings(rules, 0)
		return count

cache = {}
def get_strings(rules, number):
	if number in cache:
		return cache[number]

	rule = rules[number]
	out = get_strings_for_rule(rules, rule)
	cache[number] = out
	return out

def get_strings_for_rule(rules, rule):
	if rule.is_char:
		return {rule.char}
	if rule.is_sequence:
		if len(rule.subrules) == 1:
			return get_strings(rules, rule.subrules[0])

		out = set()
		set0 = get_strings(rules, rule.subrules[0])
		set1 = get_strings(rules, rule.subrules[1])
		for string0 in set0:
			for string1 in set1:
				out.add(string0 + string1)
		return out
	return get_strings_for_rule(rules, rule.subrules[0]).union(
		get_strings_for_rule(rules, rule.subrules[1]))

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
