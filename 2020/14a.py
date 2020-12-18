import re

def main():
	with open('14.dat', 'r') as file:
		mem = {}
		for line in file:
			line = line.strip()
			match = re.match(r'mask = ([10X]{36})', line)
			if match:
				mask_string = match.group(1)
				mask = dict()
				for i in range(36):
					c = mask_string[35 - i]
					if c != 'X':
						mask[i] = int(c)
			else:
				match = re.match(r'mem\[(\d+)\] = (\d+)', line)
				assert match
				loc = int(match.group(1))
				value = int(match.group(2))
				for i in mask:
					if mask[i]:
						value |= (1 << i)
					else:
						value &=  ~(1 << i)
				mem[loc] = value

	sum = 0
	for loc in mem:
		sum += mem[loc]
	return sum

print(main())
