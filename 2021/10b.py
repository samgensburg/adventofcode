PAREN = 1
SQUARE = 2
BRACE = 3
TRIANGLE = 4

def main():
	open_close_map = {'(': ')', '{': '}', '[': ']', '<': '>'}
	points_map = {')': PAREN, ']': SQUARE, '}': BRACE, '>': TRIANGLE}
	with open('10.dat', 'r') as file:
		last = -1
		points_list = []
		for line in file:
			#import pdb; pdb.set_trace()
			line = line.strip()
			if not line:
				continue
			opens = []
			discard = False
			for c in line:
				if c in '([{<':
					opens.append(c)
				elif c == open_close_map[opens[-1]]:
					opens = opens[:-1]
				else:
					discard = True
					break
			if not discard:
				round_points = 0
				for i in range(len(opens)):
					round_points *= 5
					c = opens[len(opens) - 1 - i]
					round_points += points_map[open_close_map[c]]
				points_list.append(round_points)
		points_list.sort()
		return points_list[(len(points_list) - 1) / 2]

print(main())
