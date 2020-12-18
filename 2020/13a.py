def main():
	with open('13.dat', 'r') as file:
		line_number = 0
		for line in file:
			if line_number == 0:
				offset = int(line.strip())
			else:
				values = line.strip().split(',')
			line_number += 1

		best_difference = -1
		best_value = -1
		for value in values:
			if value == 'x':
				continue
			else:
				value = int(value)
			assert offset // value != 0
			times = ((offset - 1) // value) + 1
			difference = times * value - offset
			if best_difference < 0 or difference < best_difference:
				best_difference = difference
				best_value = value
		return best_difference * best_value

print(main())
