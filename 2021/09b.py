from collections import defaultdict

def main():
	with open('09.dat', 'r') as file:
		grid = []
		for line in file:
			line = line.strip()
			grid_line = [int(c) for c in line]
			grid.append(grid_line)

		total = 0
		basins = defaultdict(int)
		basin_lookup = dict()
		nine_count = 0
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				v = grid[i][j]
				if v == 9:
					nine_count += 1

				is_min = True
				is_min = is_min and (i <= 0 or v < grid[i-1][j])
				is_min = is_min and (j <= 0 or v < grid[i][j-1])
				is_min = is_min and (i >= len(grid) - 1 or v < grid[i+1][j])
				is_min = is_min and (j >= len(grid[0]) - 1 or v < grid[i][j+1])

				if is_min:
					b = (i, j)
					basins[b] += 1
					basin_lookup[b] = b

		def find_basin(l):
			i, j = l
			v = grid[i][j]
			if v == 9:
				return None

			if l in basin_lookup:
				return basin_lookup[l]

			if i > 0 and v > grid[i-1][j]:
				return find_basin((i - 1, j))

			if j > 0 and v > grid[i][j-1]:
				return find_basin((i, j - 1))

			if i < len(grid) - 1 and v > grid[i+1][j]:
				return find_basin((i + 1, j))

			if j < len(grid[0]) - 1 and v > grid[i][j+1]:
				return find_basin((i, j + 1))

			assert False

		for i in range(len(grid)):
			for j in range(len(grid[0])):
				l = (i, j)
				b = find_basin(l)
				if b is not None and b != l:
					basin_lookup[l] = b
					basins[b] += 1

		top3 = [-1, -1, -1]
		print (basins)
		total = 0
		for b in basins:
			v = basins[b]
			total += v
			if top3[0] == -1 or v > top3[0]:
				top3[2] = top3[1]
				top3[1] = top3[0]
				top3[0] = v
			elif top3[1] == -1 or v > top3[1]:
				top3[2] = top3[1]
				top3[1] = v
			elif top3[2] == -1 or v > top3[2]:
				top3[2] = v
		print (total)
		print(nine_count)
		return top3[2] * top3[1] * top3[0]

print(main())
