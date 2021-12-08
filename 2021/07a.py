def main():
	with open('07.dat', 'r') as file:
		line = file.read()
	numbers = line.split(',')
	numbers = [int(n) for n in numbers]
	MAX = max(numbers)
	best = -1
	for i in range(MAX + 1):
		value = sum([abs(n - i) for n in numbers])
		best = best if best != -1 else value
		best = best if best < value else value

	return best

print(main())
