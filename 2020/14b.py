import re

def main():
	with open('14.dat', 'r') as file:
		mem = {'value': 0}
		for i in range(36):
			mem = {'X': mem}

		for line in file:
			line = line.strip()
			match = re.match(r'mask = ([10X]{36})', line)
			if match:
				mask_string = match.group(1)
				mask = dict()
				for i in range(36):
					c = mask_string[35 - i]
					mask[i] = c
			else:
				match = re.match(r'mem\[(\d+)\] = (\d+)', line)
				assert match
				loc = int(match.group(1))
				value = int(match.group(2))
				address = []
				for i in range(36):
					if mask[i] == 'X':
						address.append('X')
					elif mask[i] == '1':
						address.append('1')
					else:
						assert mask[i] == '0'
						if loc & (1 << i):
							address.append('1')
						else:
							address.append('0')
				set_mem(mem, address, value)

	return sum_mem(mem)

def set_mem(mem, address, value):
	if 'value' in mem:
		assert len(address) == 0
		mem['value'] = value
		return

	one_address = address[0]
	if one_address == 'X':
		if 'X' in mem:
			set_mem(mem['X'], address[1:], value)
		else:
			set_mem(mem['1'], address[1:], value)
			set_mem(mem['0'], address[1:], value)
	else:
		assert one_address == '1' or one_address == '0'
		other_address = '1' if one_address == '0' else '0'
		if 'X' in mem:
			mem['1'] = duplicate_mem(mem['X'])
			mem['0'] = mem['X']
			del mem['X']

		set_mem(mem[one_address], address[1:], value)

def sum_mem(mem):
	if 'value' in mem:
		return mem['value']

	if 'X' in mem:
		return 2 * sum_mem(mem['X'])

	return sum_mem(mem['0']) + sum_mem(mem['1'])

def duplicate_mem(mem):
	if is_int(mem):
		return mem
	new = {}
	for key in mem:
		new[key] = duplicate_mem(mem[key])
	return new

def is_int(x):
	return isinstance(x, int)

print(main())
