import unittest
import importlib

module_12 = importlib.import_module("12")

class Tests(unittest.TestCase):
	def test_get_counts(self):
		get_counts = module_12.get_counts
		self.assertEqual(get_counts('#.#.#'), [1,1,1])
		self.assertEqual(get_counts('###'), [3])
		self.assertEqual(get_counts('###..##'), [3,2])
		self.assertEqual(get_counts('....###..##...'), [3,2])
		self.assertEqual(get_counts('....###..##...######'), [3,2,6])
    
	def test_is_valid_prefix(self):
		is_valid_prefix = module_12.is_valid_prefix
		self.assertTrue(is_valid_prefix('#.#.#', [1,1,1]))
		self.assertTrue(is_valid_prefix('#.#.#', [1,1,2]))
		self.assertTrue(is_valid_prefix('#.##', [1,2]))
		self.assertTrue(is_valid_prefix('#.##', [1,7]))
		self.assertTrue(is_valid_prefix('#.##', [1,7,6]))
		self.assertTrue(is_valid_prefix('#.##', [1,7,6,3]))

		self.assertFalse(is_valid_prefix('#.##', [1,1,1]))
		self.assertFalse(is_valid_prefix('#.##', [2,2,1]))
		self.assertFalse(is_valid_prefix('#.##', [2,1,2]))
		self.assertFalse(is_valid_prefix('#.##.', [1,3]))
	
	def test_n_possible_arrangements(self):
		n_possible_arrangements = module_12.n_possible_arrangements
		self.assertEqual(n_possible_arrangements('#??', [1, 1]), 1)
		self.assertEqual(n_possible_arrangements('?#??', [1, 1]), 1)
		self.assertEqual(n_possible_arrangements('?###????????', [3]), 1)
		self.assertEqual(n_possible_arrangements('?###????????', [4]), 2)
		self.assertEqual(n_possible_arrangements('?###????', [3, 1]), 3)
		self.assertEqual(n_possible_arrangements('?###????????', [3, 2, 1]), 10)
	
	def test_n_possible_arrangements_unfolded(self):
		n_possible_arrangements_unfolded = module_12.n_possible_arrangements_unfolded
		self.assertEqual(n_possible_arrangements_unfolded('#??', [1, 1]), 1)

		


if __name__ == '__main__':
    unittest.main()