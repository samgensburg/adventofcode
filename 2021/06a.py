def main():
	with open('06.dat', 'r') as file:
		line = file.read()
	numbers = line.split(',')
	numbers = [int(n) for n in numbers]
	values = [0] * 9
	for n in numbers:
		values[n] += 1
	for i in range(80):
		print(sum(values))
		values = [
			values[1],
			values[2],
			values[3],
			values[4],
			values[5],
			values[6],
			values[7] + values[0],
			values[8],
			values[0]
		]

	return sum(values)

def total(values):
	count = 0
	for i in range(9):
		count += i * values[i]
	return count

print(main())
