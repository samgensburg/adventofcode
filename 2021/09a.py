def main():
	with open('09.dat', 'r') as file:
		grid = []
		for line in file:
			line = line.strip()
			grid_line = [int(c) for c in line]
			grid.append(grid_line)

		total = 0
		for i in range(len(grid)):
			for j in range(len(grid[0])):
				v = grid[i][j]
				is_min = True
				is_min = is_min and (i <= 0 or v < grid[i-1][j])
				is_min = is_min and (j <= 0 or v < grid[i][j-1])
				is_min = is_min and (i >= len(grid) - 1 or v < grid[i+1][j])
				is_min = is_min and (j >= len(grid[0]) - 1 or v < grid[i][j+1])

				if is_min:
					total += v + 1
		return total

print(main())
