import re

def main():
	with open('08.dat', 'r') as file:
		records = []
		count = 0
		for line in file:
			match = re.match(r'([a-g\ ]+) \| ([a-g\ ]+)', line[:-1])
			assert match
			characters = match.group(1).split()
			output = match.group(2).split()
			assert len(characters) == 10
			assert len(output) == 4
			for character in output:
				s = len(character)
				if s == 2 or s == 3 or s == 4 or s == 7:
					count += 1
		return count

print(main())
