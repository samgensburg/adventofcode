from pathlib import Path
import re

DATA_FILE = Path(__file__).stem + '.dat'

RED_TARGET = 12
GREEN_TARGET = 13
BLUE_TARGET = 14

def main():
	with open(DATA_FILE, 'r') as file:
		sum_a = 0
		sum_b = 0
		for line in file:
			line = line.strip()
			match = re.search(r'Game (\d+):', line)
			assert match
			id = int(match.group(1))
			i = match.end()
			
			allowed = True
			red_max = blue_max = green_max = 0
			while True:
				match = re.search(r'(\d+) (red|blue|green)', line[i:])
				if not match:
					break
				n = int(match.group(1))
				if match.group(2) == 'red':
					red_max = max(red_max, n)
					if n > RED_TARGET:
						allowed = False
				if match.group(2) == 'blue':
					blue_max = max(blue_max, n)
					if n > BLUE_TARGET:
						allowed = False
				if match.group(2) == 'green':
					green_max = max(green_max, n)
					if n > GREEN_TARGET:
						allowed = False
				
				i += match.end()
			if allowed:
				sum_a += id
			sum_b += red_max * green_max * blue_max





		return sum_a, sum_b


print(main())
