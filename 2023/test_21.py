import unittest
import importlib

module_21 = importlib.import_module("21")

BLANK_3X3 = [
	"...",
	".S.",
	"..."
]

BLANK_5X5 = [
	".....",
	".....",
	"..S..",
	".....",
	"....."
]

BLANK_7X7 = [
	".......",
	".......",
	".......",
	"...S...",
	".......",
	".......",
	".......",
]

BLANK_9X9 = [
	".........",
	".........",
	".........",
	".........",
	"....S....",
	".........",
	".........",
	".........",
	"........."
] 
ONE_WALL = [
	".....",
	"...#.",
	"..S..",
	".....",
	"....."
]


BLOCKING_GRID = [
	".......",
	"....#..",
	".##.#..",
	"...S...",
	".##.##.",
	".##..#.",
	".......",
]

class Tests(unittest.TestCase):
	def test_extended_walk(self):
		extended_walk = module_21.extended_walk
		for n in range(9, 15):
			self.assertEqual(extended_walk(BLANK_3X3, n - 1), n*n)

		for n in range(15, 21):
			self.assertEqual(extended_walk(BLANK_3X3, n - 1), n*n)
			self.assertEqual(extended_walk(BLANK_5X5, n - 1), n*n)
		
		for n in range(21, 27):
			self.assertEqual(extended_walk(BLANK_3X3, n - 1), n*n)
			self.assertEqual(extended_walk(BLANK_5X5, n - 1), n*n)
			self.assertEqual(extended_walk(BLANK_7X7, n - 1), n*n)
		
		for n in range(27, 100):
			self.assertEqual(extended_walk(BLANK_3X3, n - 1), n*n)
			self.assertEqual(extended_walk(BLANK_5X5, n - 1), n*n)
			self.assertEqual(extended_walk(BLANK_7X7, n - 1), n*n)
			self.assertEqual(extended_walk(BLANK_9X9, n - 1), n*n)

		self.assertEqual(extended_walk(ONE_WALL, 4), 5*5 - 1)
		self.assertEqual(extended_walk(ONE_WALL, 5), 6*6 - 2)
		self.assertEqual(extended_walk(ONE_WALL, 6), 7*7 - 1)
		self.assertEqual(extended_walk(ONE_WALL, 7), 8*8 - 4)
		self.assertEqual(extended_walk(ONE_WALL, 8), 9*9 - 2)
		self.assertEqual(extended_walk(ONE_WALL, 9), 10*10 - 4)
		self.assertEqual(extended_walk(ONE_WALL, 10), 11*11 - 6)
		self.assertEqual(extended_walk(ONE_WALL, 11), 12*12 - 4)
		self.assertEqual(extended_walk(ONE_WALL, 12), 13*13 - 9)

# 2 Start
# 5 Left
# 5 Down
# 7 Right
# 7 Up
# 8 Down-Left
# 10 Left-Left, Down-Down, Left-Up, Dwon-Right
# 12 Up-Right, Up-Up, Right-Right


	def test_distances_from_start(self):
		distances_from_start = module_21.distances_from_start

		from_top_left = distances_from_start(BLOCKING_GRID, (0, 0))
		self.assertEqual(len(from_top_left[0]), 1)
		self.assertEqual(len(from_top_left[1]), 2)
		self.assertEqual(len(from_top_left[2]), 3)
		self.assertEqual(len(from_top_left[3]), 3)
		self.assertEqual(len(from_top_left[4]), 4)

		from_bottom_left = distances_from_start(BLOCKING_GRID, (6, 0))
		self.assertEqual(len(from_bottom_left[0]), 1)
		self.assertEqual(len(from_bottom_left[1]), 2)
		self.assertEqual(len(from_bottom_left[2]), 2)
		self.assertEqual(len(from_bottom_left[3]), 2)
		self.assertEqual(len(from_bottom_left[4]), 4)

		from_bottom_right = distances_from_start(BLOCKING_GRID, (6, 6))
		self.assertEqual(len(from_bottom_right[0]), 1)
		self.assertEqual(len(from_bottom_right[1]), 2)
		self.assertEqual(len(from_bottom_right[2]), 2)
		self.assertEqual(len(from_bottom_right[3]), 3)
		self.assertEqual(len(from_bottom_right[4]), 4)
"""
...---|||+++|||---...
...---|||+O+|||---...
...---|||++O|||---...
###===...~O~O..===###
###===...~~O...===###
###===...~O~O..===###
...---|||++O|||---...
...---|||+O+O||---...
...---|||++O|||---...
###===...~O~O..===###
###===...~~O...===###
###===...~O~O..===###
...---|||++O|||---...
.S.---|||+O+O||---...
...---|||++O|||---...
###===...~O~...===###
###===...~~O...===###
###===...~O~...===###
...---|||++O|||---...
...---|||+O+|||---...
...---|||+++|||---...

16 * 5 = 80           9 * 5 = 45
 9 * 4 = 36           4 * 4 = 16
 4 * 1 =  4
12 * 2 = 24
----------
        144

...3...    3
..444..   12
.44544.   21
3454543   28
.44544    21
..444..   12
...3...    3
------------
         100

		 
....1....
....5....
....4....
...454...
..45454..
...454...
....4....
.........
.........

9 * 4 = 36
4 * 5 = 20
4 * 3 = 12
8 * 4 = 32
----------
     = 100

.....-----|||||-----.....
.....-----|||||-----.....
.....-----|||||-----.....
.....-----|||||-----.....
.....-----||O||-----.....
#####=====.O...=====#####
#####=====O.O..=====#####
#####=====.....=====#####
#####=====..O..=====#####
#####=====.....=====#####
.....-----||O||-----.....
.....-----|||||-----.....
.....-----||O||-----.....
.....-----|||||-----.....
.....-----|||||-----.....
#####=====.....=====#####
#####=====.....=====#####
#####=====.....=====#####
#####=====.....=====#####
#####=====.....=====#####
.....-----|||||-----.....
.....-----|||||-----.....
.....-----|||||-----.....
.....-----|||||-----.....
.....-----|||||-----.....

 4 * 12 =  48 ~
 9 * 13 = 117 ~
 4 * 12 =  48
 4 *  1 =   4
12 *  6 =  72
 8 * 12 =  96
-------------
          385

.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
#######=======.......=======#######
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......
.......-------|||||||-------.......

 9 * 25 = 225
 4 * 24 =  96
 4 *  6 =  24
 8 * 12 =  96
-------------
          441



	> 615,951,807,148,161
	< 616,951,807,148,161 - output
"""



