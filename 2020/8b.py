import re

ACC = 1
NOP = 2
JMP = 3

def main():
	with open('8.dat', 'r') as file:
		commands = []
		for line in file:
			line = line.strip()
			parts = line.split()
			if parts[0] == 'acc':
				operation = ACC
			if parts[0] == 'nop':
				operation = NOP
			if parts[0] == 'jmp':
				operation = JMP

			value = int(parts[1])
			commands.append((operation, value))

		end_command = len(commands)
		for flip in range(len(commands)):
			accumulator = 0
			loc = 0
			visited = set()
			while True:
				visited.add(loc)
				operation, value = commands[loc]
				if flip == loc:
					if operation == ACC:
						break
					if operation == NOP:
						operation = JMP
					if operation == JMP:
						operation = NOP
				if operation == ACC:
					accumulator += value
					loc += 1
				if operation == NOP:
					loc += 1
				if operation == JMP:
					loc += value

				if loc in visited:
					break
				if loc == end_command:
					return accumulator


print(main())
