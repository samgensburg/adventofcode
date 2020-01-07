import re

stack = re.compile('deal into new stack')
increment = re.compile('deal with increment (\d+)')
cut = re.compile('cut (-?\d+)')

length = 10007
with open('22.dat', 'r') as file:
	list = [i for i in range(length)]
	for line in file:
		line = line.strip()
		if stack.match(line) is not None:
			list = [list[length - 1 - i] for i in range(length)]
		elif (match := increment.match(line)) is not None:
			n = int(match.group(1))
			new_list = [0 for i in range(length)]
			for i in range(length):
				new_list[(i * n) % length] = list[i]
			list = new_list
		elif (match := cut.match(line)) is not None:
			n = int(match.group(1))
			new_list = [0 for i in range(length)]
			for i in range(length):
				new_list[(i - n) % length] = list[i]
			list = new_list
		else:
			print(line)
			assert False

for i in range(length):
	if list[i] == 2019:
		print(i)

print(list)
