def main():
	with open('13.dat', 'r') as file:
		line_number = 0
		for line in file:
			if line_number == 0:
				_ = int(line.strip())
			else:
				values = line.strip().split(',')
			line_number += 1

		offset = -1
		current_lcm = 1
		output = 0
		for value in values:
			offset += 1
			if value == 'x':
				continue
			else:
				value = int(value)
				assert is_prime(value)

			print('output: %d' % output)
			print('current_lcm: %d' % current_lcm)
			print('value: %d' % value)
			print('offset: %d' % offset)
			print('*********************')
			while ((output + offset) % value):
				output += current_lcm

			current_lcm *= value
		return output

prime_cache = {1: False, 2: True, 3: True}
def is_prime(n):
	if n in prime_cache:
		return prime_cache[n]
	for i in range(2, n):
		if (n // i) * i == n:
			prime_cache[n] = False
			return False
		if i * i > n:
			prime_cache[n] = True
			return True


print(main())
