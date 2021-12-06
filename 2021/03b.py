WIDTH = 12

def main():
	with open('03.dat', 'r') as file:
		oxygen_list = []
		co2_list = []

		for line in file:
			line = line.strip()
			oxygen_list.append(line)
			co2_list.append(line)

		for i in range(WIDTH):
			if len(oxygen_list) > 1:
				oxygen_list = [item for item in oxygen_list
					if item[i] == most_common(oxygen_list, i)]
			if len(co2_list) > 1:
				co2_list = [item for item in co2_list
					if item[i] != most_common(co2_list, i)]
		return to_decimal(oxygen_list[0]) * to_decimal(co2_list[0])

def to_decimal(binary):
	out = 0
	for i in range(WIDTH):
		out *= 2
		if binary[i] == '1':
			out += 1
	return out

def most_common(items, position):
	count_0 = 0
	count_1 = 0
	for item in items:
		if item[position] == '1':
			count_1 += 1
		else:
			assert item[position] == '0'
			count_0 += 1

	if count_1 >= count_0:
		return '1'
	else:
		return '0'


print(main())
