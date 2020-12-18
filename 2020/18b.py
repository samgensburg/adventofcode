def main():
	with open('18.dat', 'r') as file:
		sum = 0
		for line in file:
			line = line.strip()
			#import pdb; pdb.set_trace()
			value, i = get_value(line, 0)
			assert i == len(line)
			sum += value
			print(line)
			print(value)
		return sum

def get_value(line, i):
	product = 1
	if line[i] == '(':
		acc, i = get_value(line, i + 1)
	else:
		acc, i = get_number(line, i)

	while i < len(line) and line[i] != ')':
		assert line[i] == ' '
		assert line[i + 2] == ' '
		if line[i + 1] == '+':
			plus = True
		else:
			assert line[i + 1] == '*'
			plus = False

		i += 3
		if line[i] == '(':
			n, i = get_value(line, i + 1)
		else:
			n, i = get_number(line, i)

		if plus:
			acc += n
		else:
			product *= acc
			acc = n

	product *= acc
	if i == len(line):
		return product, i
	if line[i] == ')':
		return product, i + 1
	assert False

def get_number(line, i):
	assert line[i].isdigit()
	end = i + 1
	while end < len(line) and line[end].isdigit():
		end += 1
	return int(line[i:end]), end

print(main())
