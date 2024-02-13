import unittest
import importlib

module_17 = importlib.import_module("17")

GRID_TINY = [
	[1,2],
	[3,4]
]

GRID = [
	[1,2,3],
	[4,5,6],
	[7,8,9]
]

GRID_2 = [
	[1,1,9],
	[9,1,1],
	[9,9,1]
]

GRID_LARGE = [
	[1,2,3,1,2,3],
	[4,5,6,4,5,6],
	[7,8,9,4,5,6],
	[1,1,1,1,1,1]
]

GRID_LARGE_2 = [
	[1,2,3,1,2,3],
	[4,5,6,4,5,6],
	[7,8,9,4,5,6],
	[9,9,9,9,9,9]
]

ZIG_ZAG = [
	[1,9,1,1,1],
	[1,9,1,9,1],
	[1,9,1,9,1],
	[1,1,1,9,1]
]

RIGHT = module_17.RIGHT
DOWN = module_17.DOWN
LEFT = module_17.LEFT
UP = module_17.UP

class Tests(unittest.TestCase):
	def test_list_options(self):
		list_options = module_17.list_options
		self.assertEqual(set(list_options(GRID, (RIGHT, 0, 0))),
			set([(2, (DOWN, 0, 1)), (5, (DOWN, 0, 2)), (5, (UP, 0, 2)), (2, (UP, 0, 1))]))
		self.assertEqual(set(list_options(GRID, (DOWN, 0, 0))),
			set([(4, (RIGHT, 1, 0)), (11, (RIGHT, 2, 0)), (11, (LEFT, 2, 0)), (4, (LEFT, 1, 0))]))
	
	def test_low_heat(self):
		low_heat = module_17.low_heat
		self.assertEqual(low_heat([[0]]), 0)
		self.assertEqual(low_heat(GRID_TINY), 6)
		self.assertEqual(low_heat(GRID_2), 4)
		self.assertEqual(low_heat(GRID), 20)
		self.assertEqual(low_heat(GRID_LARGE), 17)
		self.assertEqual(low_heat(GRID_LARGE_2), 34)
		self.assertEqual(low_heat(ZIG_ZAG), 13)

	def test_find_low_heat_unrestricted_paths(self):
		f = module_17.find_low_heat_unrestricted_paths
		v = f(GRID)
		self.assertEqual(v[(0, 0)], 20)
		self.assertEqual(v[(2, 2)], 0)

		v = f(ZIG_ZAG)
		self.assertEqual(v[(0, 0)], 13)

