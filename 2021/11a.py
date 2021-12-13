data = [
'2566885432',
'3857414357',
'6761543247',
'5477332114',
'3731585385',
'1716783173',
'1277321612',
'3371176148',
'1162578285',
'6144726367']

def main():
	grid = [[int(c) for c in row] for row in data]
	flash_count = 0
	for iteration in range(100):
		for i in range(10):
			for j in range(10):
				grid[i][j] += 1

		flash_locs = set()
		has_flashed = True
		while has_flashed == True:
			has_flashed = False
			for i in range(10):
				for j in range(10):
					if grid[i][j] >= 10 and (i, j) not in flash_locs:
						#import pdb; pdb.set_trace()
						flash_locs.add((i, j))
						has_flashed = True
						flash_count += 1
						left = (j > 0)
						right = (j < 9)
						top = (i > 0)
						bottom = (i < 9)
						if top and left:
							grid[i-1][j-1] += 1
						if top:
							grid[i-1][j] += 1
						if top and right:
							grid[i-1][j+1] += 1
						if right:
							grid[i][j+1] += 1
						if bottom and right:
							grid[i+1][j+1] += 1
						if bottom:
							grid[i+1][j] += 1
						if bottom and left:
							grid[i+1][j-1] += 1
						if left:
							grid[i][j-1] += 1
		for (i, j) in flash_locs:
			grid[i][j] = 0
	return flash_count


print(main())
