import unittest
from solution import *

class FirstHomeworkSimpleTests(unittest.TestCase):
    def test_make_multiset_syntax(self):
        x = make_multiset([1, 2])
        self.assertEqual(x, {1: 1, 2: 1})
        self.assertNotEqual(x, {1: 'spam', 2: 'eggs'})

    def test_ordered_dict_syntax(self):
        x = ordered_dict({1: 'i', 2: 'ii', 3: 'iii'})
        self.assertEqual(x, [(1, 'i'), (2, 'ii'), (3, 'iii')])
        self.assertNotEqual(x, [(4, 'iv')])

    def test_reversed_dict_syntax(self):
        x = reversed_dict({'Nibbler': 3, 'Fillip': 2, 'Turanga': 1})
        self.assertEqual(x, {3: 'Nibbler', 2: 'Fillip', 1: 'Turanga'})
        self.assertNotEqual(x, {2: 'Amy'})

    def test_unique_objects_syntax(self):
        x = unique_objects([1, 2, 3, 2, 1, 5, 42, None, 'asd'])
        self.assertEqual(x, 7)
        self.assertNotEqual(x, 1337)

if __name__ == "__main__":
    unittest.main()
