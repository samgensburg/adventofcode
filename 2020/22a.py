from collections import deque



def main():
	player1 = deque()
	player2 = deque()
	with open('22.dat', 'r') as file:
		state = 0
		for line in file:
			line = line.strip()
			if state == 0:
				assert line == 'Player 1:'
				state += 1
			elif state == 1 and line:
				player1.append(int(line))
			elif not line:
				state = 2
			elif state == 2:
				assert line == 'Player 2:'
				state += 1
			else:
				assert state == 3
				player2.append(int(line))

	while len(player1) and len(player2):
		print(player1)
		print(player2)
		print('')

		value1 = player1.popleft()
		value2 = player2.popleft()
		if value1 > value2:
			player1.append(value1)
			player1.append(value2)
		else:
			player2.append(value2)
			player2.append(value1)

	if len(player1):
		winner = player1
	else:
		winner = player2
	total = 0
	multiplier = 1
	while len(winner):
		total += multiplier * winner.pop()
		multiplier += 1

	return total

print(main())
