from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

def print_stacks(stacks):
	m = max([len(stack) for stack in stacks])
	for i in range(m - 1, -1, -1):
		line = ''
		for j in range(9):
			if len(stacks[j]) > i:
				line += '[' + stacks[j][i] + '] '
			else:
				line += '    '
		print(line)
	print(' 1   2   3   4   5   6   7   8   9 ')

def main_a():
	with open(DATA_FILE, 'r') as file:
		stacks = [[] for i in range(9)]
		boxes = True
		blank = True
		for line in file:
			if boxes:
				if line[1] == '1':
					assert line.strip() == '1   2   3   4   5   6   7   8   9'
					boxes = False
					continue
				for i in range(9):
					if line[i * 4] == '[':
						assert line[i * 4 + 2] == ']'
						stacks[i].insert(0, line[i * 4 + 1])
				continue
			
			if blank:
				assert line.strip() == ''
				blank = False
				continue


			match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
			assert match
			vals = [int(match.group(i)) for i in range(1, 4)]
			for i in range (vals[0]):
				crate = stacks[vals[1] - 1].pop()
				stacks[vals[2] - 1].append(crate)
		
		return ''.join([stacks[i].pop() for i in range(9)])

def main_b():
	with open(DATA_FILE, 'r') as file:
		stacks = [[] for i in range(9)]
		boxes = True
		blank = True
		for line in file:
			if boxes:
				if line[1] == '1':
					assert line.strip() == '1   2   3   4   5   6   7   8   9'
					boxes = False
					continue
				for i in range(9):
					if line[i * 4] == '[':
						assert line[i * 4 + 2] == ']'
						stacks[i].insert(0, line[i * 4 + 1])
				continue
			
			if blank:
				assert line.strip() == ''
				blank = False
				continue


			match = re.match(r'move (\d+) from (\d+) to (\d+)', line)
			assert match
			vals = [int(match.group(i)) for i in range(1, 4)]
			n = vals[0]
			source = vals[1] - 1
			crates = stacks[source][-n:]
			stacks[source] = stacks[source][:-n]
			stacks[vals[2] - 1].extend(crates)
		
		return ''.join([stacks[i].pop() for i in range(9)])


print(main_a(), main_b())
