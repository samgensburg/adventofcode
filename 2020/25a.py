
def main():
	base = 20201227
	a = 3469259
	b = 13170438
	subject = 7
	value = 1
	loop_a = None
	loop_b = None
	for i in range(1, base):
		#print(value)
		value = (value * subject) % base
		if value == a:
			loop_a = i
			print(loop_a)
		if value == b:
			loop_b = i
			print(loop_b)
		if loop_a and loop_b:
			break
	subject = a
	value = 1
	for i in range(loop_b):
		value = (value * subject) % base
	return value

print(main())
