from pathlib import Path

DATA_FILE = Path(__file__).stem + '.dat'

def main():
	top = [0, 0, 0]
	with open(DATA_FILE, 'r') as file:
		working = 0
		for line in file:
			if line.strip():
				item = int(line)
				working += item
			else:
				if working > top[0]:
					top[0], top[1], top[2] = working, top[0], top[1]
				elif working > top[1]:
					top[0], top[1], top[2] = top[0], working, top[1]
				elif working > top[2]:
					top[0], top[1], top[2] = top[0], top[1], working
				working = 0
		return top[0], sum(top)

			


print(main())
