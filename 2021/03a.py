WIDTH = 12

def main():
	with open('03.dat', 'r') as file:
		row_count = 0
		one_counts = [0] * WIDTH
		for line in file:
			row_count += 1
			for i in range(WIDTH):
				if line[i] == '1':
					one_counts[i] += 1
				else:
					assert line[i] == '0'

		gamma = 0
		epsilon = 0
		for i in range(WIDTH):
			gamma *= 2
			epsilon *= 2
			one_count = one_counts[i]
			zero_count = row_count - one_count
			if one_count > zero_count:
				gamma += 1
			else:
				assert zero_count > one_count
				epsilon += 1
		return gamma * epsilon
print(main())
