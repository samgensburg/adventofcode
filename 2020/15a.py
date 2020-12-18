import re

def main():
	input = [11,18,0,20,1,7,16]
	last_index = {}
	for i in range(30000000):
		if i % 10000 == 0:
			print(i)
		if len(input):
			current = input[0]
			input = input[1:]
		else:
			current = next

		if current in last_index:
			next = i - last_index[next]
			last_index[current] = i
		else:
			next = 0
			last_index[current] = i

	return current

print(main())
