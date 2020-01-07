import re

stack = re.compile('deal into new stack')
increment = re.compile('deal with increment (\d+)')
cut = re.compile('cut (-?\d+)')

length = 119315717514047
iterations = 101741582076661

# test data
#length = 10007
#iterations = 1

with open('22.dat', 'r') as file:
#	file = ['deal with increment 7',
#'deal into new stack',
#'deal into new stack']
	first = 0
	iterator = 1
	for line in file:
		line = line.strip()
		print(first, iterator)
		print(line)
		if stack.match(line) is not None:
			first = first - iterator
			iterator = -iterator
		elif (match := increment.match(line)) is not None:
			n = int(match.group(1))
			local_iterator = None
			for multiplier in range(n):
				if (multiplier * length + 1) % n == 0:
					local_iterator = ((multiplier * length) + 1) // n
			assert local_iterator is not None
			iterator = local_iterator * iterator
		elif (match := cut.match(line)) is not None:
			n = int(match.group(1))
			first += n * iterator
		else:
			print(line)
			assert False
		first %= length
		iterator %= length

current_power = 1
current_first = first
current_iterator = iterator
cache = dict()
while current_power * 2 <= iterations:
	cache[current_power] = (current_first, current_iterator)
	current_power *= 2
	current_first = current_first * current_iterator + current_first
	current_first %= length
	current_iterator *= current_iterator
	current_iterator %= length
# don't need last cache

try_add = int(current_power / 2)
while try_add >= 1:
	if try_add + current_power <= iterations:
		current_power += try_add
		cached_first, cached_iterator = cache[try_add]
		current_first = cached_first * current_iterator + current_first
		current_first %= length
		current_iterator = cached_iterator * current_iterator
		current_iterator %= length
	try_add = int(try_add / 2)

answer = current_first + current_iterator * 2020
answer %= length
print(answer)

"""print(current_first, current_iterator, current_power)
current = int(current_first)
for i in range(1, length):
	current += int(current_iterator)
	current %= length
	if current == 2019:
		print(i)
"""
