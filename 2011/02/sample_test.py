import unittest
from solution import *

class SecondHomeworkSimpleTests(unittest.TestCase):

    def test_groupby_simple_types(self):
        expected = {'even':[2, 8, 10, 12], 'odd':[1, 3, 5, 9]}
        actual = groupby(lambda x: 'odd' if x%2 else 'even', [1, 2, 3, 5, 8, 9, 10, 12])
        self.assertEqual(expected, actual)

    def test_iterate_start_with_identity_function(self):
        bracketisers = iterate(lambda x: '(' + x + ')') # there's no such word, really
        no_brackets = next(bracketisers)
        self.assertEqual('hello world', no_brackets('hello world'))

    def test_iterate_ordered_calls(self):
        powers_of_two = iterate(lambda x: x*2)
        f = next(powers_of_two)
        self.assertEqual(1 * 'eggs', f('eggs'))
        f = next(powers_of_two)
        self.assertEqual(2 * 'ham', f('ham'))
        f = next(powers_of_two)
        self.assertEqual(4 * 'spam', f('spam'))
        f = next(powers_of_two)
        self.assertEqual(8 * 'spameggs', f('spameggs'))

    def test_zip_with_simple(self):
        first_names = ['Charlie', 'Dizzy']
        last_names = ['Parker', 'Gillespie']
        expected = ['CharlieParker', 'DizzyGillespie']
        actual = zip_with(str.__add__, first_names, last_names)
        self.assertEqual(expected, list(actual))

    def test_cache_call_is_cached(self):

        call_count = 0
        def double(x):
            nonlocal call_count
            call_count += 1
            return 2 * x
        
        cached_double = cache(double, 10)
        self.assertEqual(256, cached_double(128))
        self.assertEqual(256, cached_double(128))
        self.assertEqual(1, call_count)

if __name__ == "__main__":
    unittest.main()
