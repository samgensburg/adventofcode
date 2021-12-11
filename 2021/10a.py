PAREN = 3
SQUARE = 57
BRACE = 1197
TRIANGLE = 25137

def main():
	open_close_map = {'(': ')', '{': '}', '[': ']', '<': '>'}
	points_map = {')': PAREN, ']': SQUARE, '}': BRACE, '>': TRIANGLE}
	with open('10.dat', 'r') as file:
		last = -1
		points = 0
		for line in file:
			line = line.strip()
			opens = []
			for c in line:
				if c in '([{<':
					opens.append(c)
				elif c == open_close_map[opens[-1]]:
					opens = opens[:-1]
				else:
					points += points_map[c]
					break
		return points

print(main())
