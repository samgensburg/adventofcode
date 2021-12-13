from collections import defaultdict
import re

def main():
	with open('12.dat', 'r') as file:
		caves = defaultdict(set)
		for line in file:
			line = line.strip()
			match = re.match(r'(\w+)-(\w+)', line)
			assert match
			first = match.group(1)
			second = match.group(2)
			caves[first].add(second)
			caves[second].add(first)

	paths = [['start']]
	count = 0
	while len(paths):
		path = paths.pop()
		current = path[-1]
		if path[-1] == 'end':
			count += 1
			continue

		for next in caves[current]:
			if is_small(next) and next in path:
				continue
			new_path = [c for c in path]
			new_path.append(next)
			paths.append(new_path)

	return count

def is_small(cave):
	return cave.islower()

print(main())
