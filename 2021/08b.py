import re

def main():
	with open('08.dat', 'r') as file:
		records = []
		count = 0
		for line in file:
			print(line)
			match = re.match(r'([a-g\ ]+) \| ([a-g\ ]+)', line.strip())
			assert match
			characters = match.group(1).split()
			output = match.group(2).split()
			assert len(characters) == 10
			assert len(output) == 4
			characters = [set(list(c)) for c in characters]
			output = [set(list(c)) for c in output]

			sets = [0] * 10
			sets[1] = [c for c in characters if len(c) == 2][0]
			sets[7] = [c for c in characters if len(c) == 3][0]
			sets[4] = [c for c in characters if len(c) == 4][0]
			sets[8] = [c for c in characters if len(c) == 7][0]

			mid_and_top_left = sets[4] - sets[7]
			sets[0] = [c for c in characters if len(c) == 6 and not mid_and_top_left.issubset(c)][0]

			mid = mid_and_top_left - sets[0]
			top_left = mid_and_top_left - mid
			mid_and_right = mid.union(sets[1])
			sets[9] = [c for c in characters if len(c) == 6 and mid_and_right.issubset(c)][0]
			sets[6] = [c for c in characters if len(c) == 6 and not sets[1].issubset(c)][0]
			sets[3] = [c for c in characters if len(c) == 5 and mid_and_right.issubset(c)][0]
			sets[5] = [c for c in characters if len(c) == 5 and top_left.issubset(c)][0]
			sets[2] = [c for c in characters if len(c) == 5 and c != sets[5] and c != sets[3]][0]
			value = 0
			for c in output:
				value *= 10
				found = False
				for i in range(10):
					if c == sets[i]:
						assert not found
						found = True
						value += i
				assert found
			count += value

		return count
"""
abcdfg, ac, adefg, acdef, abce, bcdef, bcdefg, acf, abcdefg, abcdef
 f
b a
 e
g c
 d
 """
print(main())
