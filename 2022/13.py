from pathlib import Path
from queue import Queue
import re

DATA_FILE = Path(__file__).stem + '.dat'

class Elf_List():
	def __init__(self, text):
		assert len(text) > 0
		self._is_int = False
		if text[0] != '[':
			self._is_int = True
			self._int = int(text)
			return
		self.elements = []
		i = 0
		start_i = 1
		depth = 0
		while True:
			i += 1
			c = text[i]
			if i == start_i and c == ']':
				assert depth == 0
				break
			assert not (i == start_i and c == ',')
			if c == '[':
				depth += 1
			elif c == ']' and depth != 0:
				depth -= 1
			elif c == ']':
				self.elements.append(Elf_List(text[start_i:i]))
				break
			elif c == ',' and depth == 0:
				self.elements.append(Elf_List(text[start_i:i]))
				start_i = i + 1

	def __str__(self):
		if self._is_int:
			return str(self.int)
		return '[' + ','.join([str(self.element(i)) for i in range(self.len)]) + ']'

	def __repr__(self) -> str:
		return self.__str__()

	def is_int(self):
		return self._is_int

	@property
	def int(self):
		assert self.is_int()
		return self._int

	@property
	def len(self):
		assert not self.is_int()
		return len(self.elements)	

	def element(self, i):
		assert not self.is_int()
		return self.elements[i]

def compare(left_list, right_list):
	#import pdb; pdb.set_trace()
	if left_list.is_int() and right_list.is_int():
		left_int = left_list.int
		right_int = right_list.int
		return right_int - left_int

	if not left_list.is_int() and right_list.is_int():
		return compare(left_list, Elf_List('[' + str(right_list.int) + ']'))

	if left_list.is_int() and not right_list.is_int():
		return compare(Elf_List('[' + str(left_list.int) + ']'), right_list)

	for i in range(left_list.len):
		if i >= right_list.len:
			return -1
		
		compare_value = compare(left_list.element(i), right_list.element(i))
		if compare_value != 0:
			return compare_value
	
	if left_list.len == right_list.len:
		return 0
	return 1

def main(text):
	return (main_a(text), main_b(text))

def main_a(text):
	total = 0
	for i in range(0, (len(text) + 1) // 3):
		left_list = Elf_List(text[i * 3])
		right_list = Elf_List(text[i * 3 + 1])
		assert i * 3 + 2 == len(text) or text[i * 3 + 2].strip() == ''
		compare_value = compare(left_list, right_list)
		assert compare_value != 0
		if compare_value > 0:
			total += i + 1
	return total

def main_b(text):
	lists = []
	decoder_a = Elf_List('[[2]]')
	decoder_b = Elf_List('[[6]]')
	for line in text:
		if line.strip():
			lists.append(Elf_List(line))
	
	lists.append(decoder_a)
	lists.append(decoder_b)

	for i in range(len(lists)):
		for j in range(len(lists) - 1):
			if compare(lists[j], lists[j + 1]) < 0:
				lists[j], lists[j + 1] = lists[j + 1], lists[j]

	product = 1
	for i in range(len(lists)):
		print (lists[i])
		if compare(decoder_a, lists[i]) == 0:
			product *= i + 1
		if compare(decoder_b, lists[i]) == 0:
			product *= i + 1

	return product


with open(DATA_FILE, 'r') as file:
	print(main(file.read().strip().split('\n')))
