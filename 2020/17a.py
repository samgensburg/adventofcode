import re

def main():
	with open('17.dat', 'r') as file:
		state = [[]]
		nearby_tickets = []

		for line in file:
			line = line.strip()
			state[0].append([c == '#' for c in line])

		for _ in range(6):
			print_state(state)
			new_state = []
			for i in range(len(state) + 2):
				new_state.append([])
				for j in range(len(state[0]) + 2):
					new_state[i].append([])
					for k in range(len(state[0][0]) + 2):
						count = get_count(i, j, k, state)
						if (i == 0 or j == 0 or k == 0 or
							i == len(state) + 1 or j == len(state[0]) + 1 or k == len(state[0][0]) + 1):
							old_value = False
						else:
							old_value = state[i - 1][j - 1][k - 1]

						if old_value and count == 2:
							new_value = True
						elif count == 3:
							new_value = True
						else:
							new_value = False
						new_state[i][j].append(new_value)
			state = new_state

		count = 0
		for i in range(len(state)):
			for j in range(len(state[0])):
				for k in range(len(state[0][0])):
					if state[i][j][k]:
						count += 1
		return count

def get_count(x, y, z, state):
	count = 0
	a_cap = len(state)
	b_cap = len(state[0])
	c_cap = len(state[0][0])
#	from pdb import set_trace; set_trace()
	for i in range(3):
		for j in range(3):
			for k in range(3):
				if i == 1 and j == 1 and k == 1:
					continue
				a = x + i - 2
				b = y + j - 2
				c = z + k - 2
				if a < 0 or b < 0 or c < 0:
					continue
				if a >= a_cap or b >= b_cap or c >= c_cap:
					continue

				if state[a][b][c]:
					count += 1
#	set_trace()
	return count

def print_state(state):
	for layer in state:
		for row in layer:
			text = ''.join([('#' if b else '.') for b in row])
			print(text)
		print()

print(main())
