from collections import deque

def main():
	player1 = []
	player2 = []
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

	_, deck = play(player1, player2, 0)

	multiplier = 1
	total = 0
	while len(deck):
		total += multiplier * deck[-1]
		deck = deck[:-1]
		multiplier += 1

	return total

def play(player1, player2, depth):
	print(player1)
	print(player2)
	print(depth)
	print('')

	seen = set()
	while len(player1) and len(player2):
		hash = ''
		for n in player1:
			hash += format(n, '03d')
		hash += ' '
		for n in player2:
			hash += format(n, '03d')

		if hash in seen:
			return 1, player1
		else:
			seen.add(hash)

		value1 = player1[0]
		player1 = player1[1:]
		value2 = player2[0]
		player2 = player2[1:]

		if value1 <= len(player1) and value2 <= len(player2):
			winner, _ = play(player1[:value1], player2[:value2], depth + 1)
			if winner == 1:
				player1.append(value1)
				player1.append(value2)
			else:
				player2.append(value2)
				player2.append(value1)
		elif value1 > value2:
			player1.append(value1)
			player1.append(value2)
		else:
			player2.append(value2)
			player2.append(value1)

	if len(player1):
		return 1, player1
	return 2, player2


print(main())
