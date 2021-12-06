START = 0
AWAITING_BLANK = 1
IN_BOARD = 2

def main():
	with open('04.dat', 'r') as file:
		status = START
		boards = []
		for line in file:
			line = line[:-1]
			if status == START:
				plays = line.split(',')
				plays = [int(play) for play in plays]
				status = AWAITING_BLANK
			elif status == AWAITING_BLANK:
				assert line == ''
				new_board = []
				status = IN_BOARD
			elif status == IN_BOARD:
				board_line = [int(line[x * 3:x * 3 + 2]) for x in range(5)]
				new_board.append(board_line)
				if len(new_board) == 5:
					boards.append(new_board)
					status = AWAITING_BLANK
			else:
				assert False

		for n in plays:
			boards = [make_move(n, board) for board in boards]
			new_boards = [board for board in boards if not is_winning(board)]
			if len(new_boards) > 0:
				boards = new_boards
			else:
				return score(n, boards[0])

def make_move(n, board):
	for i in range(5):
		for j in range(5):
			if board[i][j] == n:
				board[i][j] = 'X'
				return board
	return board

def is_winning(board):
	for i in range(5):
		horizontal_win = True
		vertical_win = True
		for j in range(5):
			if board[i][j] != 'X':
				horizontal_win = False
			if board[j][i] != 'X':
				vertical_win = False
		if horizontal_win or vertical_win:
			return True
	return False

def score(n, board):
	sum = 0
	for i in range(5):
		for j in range(5):
			if board[i][j] != 'X':
				sum += board[i][j]
	return sum * n

print(main())
