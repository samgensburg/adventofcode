from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

class Monkey:
	def __init__(self, lines, divisor):
		assert re.match(r'Monkey \d:', lines[0])
		self.id = lines[0][7]

		##########################################

		assert lines[1][:18] == '  Starting items: '
		self.items = Queue()
		for item in lines[1][18:].split(', '):
			self.items.put(int(item))

		##########################################

		assert lines[2][:23] == '  Operation: new = old '
		add = False
		if lines[2][23] == '+':
			add = True
		else:
			assert lines[2][23] == '*'

		if lines[2][25:].strip() == 'old':
			assert not add
			self.operation = lambda x: x * x
		else:
			val = int(lines[2][25:])
			if add:
				self.operation = lambda x, val=val: x + val
			else:
				self.operation = lambda x, val=val: x * val
		
		##########################################

		assert lines[3][:21] == '  Test: divisible by '
		self.test_base = int(lines[3][21:])

		##########################################

		assert lines[4][:29] == '    If true: throw to monkey '
		self.true_target = int(lines[4][29:])

		##########################################

		assert lines[5][:30] == '    If false: throw to monkey '
		self.false_target = int(lines[5][30:])

		##########################################

		self.throws = 0
		self.divisor = divisor

	def __str__(self):
		return 'Monkey ' + str(self.id) + '\nItems: ' + str(self.items) + \
			'\nTest: ' + str(self.test_base) + ' -> [ ' + str(self.true_target) + ' / ' + str(self.false_target) + ' ]'

	def has_items(self):
		return not self.items.empty()

	def throw(self):
		self.throws += 1
		item = self.items.get()
		item = self.operation(item) // self.divisor
		if item % self.test_base == 0:
			return self.true_target, item
		return self.false_target, item
	
	def add_item(self, item):
		self.items.put(item)

def main(text):
	return get_monkey_business(text, 3, 20), get_monkey_business(text, 1, 10000)

def get_monkey_business(text, divisor, rounds):
	monkeys = []
	for i in range(0, len(text), 7):
		monkeys.append(Monkey(text[i:i+6], divisor))
		assert i + 6 == len(text) or text[i+6].strip() == ''

	base = 1
	for monkey in monkeys:
		base *= monkey.test_base

	for i in range(rounds):
		for j in range(len(monkeys)):
			while monkeys[j].has_items():
				destination, value = monkeys[j].throw()
				value %= base
				monkeys[destination].add_item(value)
	
	throws = [monkeys[i].throws for i in range(len(monkeys))]
	max1, max2 = 0, 0
	for count in throws:
		if count > max1:
			max1, max2 = count, max1
		elif count > max2:
			max1, max2 = max1, count

	return max1 * max2

with open(DATA_FILE, 'r') as file:
	print(main(file.read().strip().split('\n')))
