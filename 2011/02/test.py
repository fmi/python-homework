import unittest
import homework

from itertools import repeat

class SecondHomeworkTests(homework.Test):

    def test_groupby_empty(self):
        expected = {}
        actual = self.solution.groupby(lambda x: x, [])
        self.assertEqual(expected, actual)
    
    def test_groupby_no_repetitions(self):
        expected = {1:[1], 2:[2], 3:[3], 5:[5], 'se7en':['se7en']}
        actual = self.solution.groupby(lambda x: x, [1, 2, 3, 5,'se7en'], )
        self.assertEqual(expected, actual)

    def test_groupby_simple_types(self):
        expected = {'even':[2, 8, 10, 12], 'odd':[1, 3, 5, 9]}
        actual = self.solution.groupby(lambda x: 'odd' if x%2 else 'even', [1, 2, 3, 5, 8, 9, 10, 12])
        self.assertEqual(expected, actual)

    def test_groupby_with_generator(self):
        expected = {'big': [35, 40, 45], 'small': [0, 5, 10, 15, 20, 25, 30]}
        actual = self.solution.groupby(lambda x: 'big' if x > 30 else 'small', range(0, 50, 5))
        self.assertEqual(expected, actual)

    def test_groupby_nonequalty(self):
        actual = self.solution.groupby(lambda x: 'odd' if x%2 else 'even', [1, 2, 3, 4])
        self.assertNotEquals({'even': 42}, actual)

    def test_iterate_start_with_identity_function(self):
        bracketisers = self.solution.iterate(lambda x: '(' + x + ')') # there's no such word, really
        no_brackets = next(bracketisers)
        self.assertEqual('hello world', no_brackets('hello world'))

    def test_iterate_ordered_calls(self):
        powers_of_two = self.solution.iterate(lambda x: x*2)
        f = next(powers_of_two)
        self.assertEqual(1 * 'eggs', f('eggs'))
        f = next(powers_of_two)
        self.assertEqual(2 * 'ham', f('ham'))
        f = next(powers_of_two)
        self.assertEqual(4 * 'spam', f('spam'))
        f = next(powers_of_two)
        self.assertEqual(8 * 'spameggs', f('spameggs'))

    def test_iterate_out_of_order_calls(self):
        powers_of_two = self.solution.iterate(lambda x: x*2)
        f0 = next(powers_of_two)
        f1 = next(powers_of_two)
        f2 = next(powers_of_two)
        f3 = next(powers_of_two)
        self.assertEqual(1 * 'eggs', f0('eggs'))
        self.assertEqual(2 * 'ham', f1('ham'))
        self.assertEqual(4 * 'spam', f2('spam'))
        self.assertEqual(8 * 'spameggs', f3('spameggs'))

    test_iterate_out_of_order_calls_again = \
        test_iterate_out_of_order_calls

    test_iterate_out_of_order_calls_yet_again = \
        test_iterate_out_of_order_calls

    def test_zip_with_empty(self):
        expected = []
        actual = self.solution.zip_with(lambda x: x)
        self.assertEqual(expected, list(actual))

    def test_zip_with_one_shorter_seqence(self):
        first_names = ['Charlie', 'Dizzy']
        last_names = ['Parker', 'Gillespie', 'Monk']
        expected = ['CharlieParker', 'DizzyGillespie']
        actual = self.solution.zip_with(str.__add__, first_names, last_names)
        self.assertEqual(expected, list(actual))

    def test_zip_with_infinite_sequence(self):
        first_names = ['John', 'Miles']
        last_names = ['Coltrane', 'Davis']
        spaces = repeat(' ')
        expected = ['John Coltrane', 'Miles Davis']
        actual = self.solution.zip_with(lambda x, y, z: x + y + z, first_names, spaces, last_names)
        self.assertEqual(expected, list(actual))

    def test_zip_with_vargs_function(self):
        expected = [1 + 2 + 3 + 5 + 8]
        actual = self.solution.zip_with(lambda *x: sum(x), [1], [2], [3], [5], [8])
        self.assertEqual(expected, list(actual))

    def test_zip_with_nonequalty(self):
        numbers1 = [1, 3]
        numbers2 = [2, 4]
        actual = self.solution.zip_with(int.__add__, numbers1, numbers2)
        self.assertNotEquals([3, 5, 8], list(actual))

    def test_cache_no_cache(self):

        call_count = 0
        def double(x):
            nonlocal call_count
            call_count += 1
            return 2 * x
        
        cached_double = self.solution.cache(double, 0)
        self.assertEqual(42 * 2, cached_double(42))
        self.assertEqual(5 * 2, cached_double(5))
        self.assertEqual(2, call_count)

    def test_cache_call_is_cached(self):

        call_count = 0
        def double(x):
            nonlocal call_count
            call_count += 1
            return 2 * x
        
        cached_double = self.solution.cache(double, 10)
        self.assertEqual(256, cached_double(128))
        self.assertEqual(256, cached_double(128))
        self.assertEqual(1, call_count)

    def test_cache_cache_is_not_global(self):
        
        call_count = 0
        def double(x):
            nonlocal call_count
            call_count += 1
            return 2 * x

        cached_double1 = self.solution.cache(double, 3)
        cached_double2 = self.solution.cache(double, 3)
        self.assertEqual(42 * 2, cached_double1(42))
        self.assertEqual(42 * 2, cached_double2(42))
        self.assertEqual(2, call_count)

    def test_cache_size_is_respected(self):

        call_count = 0
        def double(x):
            nonlocal call_count
            call_count += 1
            return 2 * x

        cached_double = self.solution.cache(double, 2)
        self.assertEqual(2, cached_double(1))
        self.assertEqual(4, cached_double(2))
        self.assertEqual(6, cached_double(3))
        self.assertEqual(2, cached_double(1))

        self.assertEqual(4, call_count)

    def test_cache_function_with_vargs(self):
        
        call_count = 0
        def sum_varargs(*x):
            nonlocal call_count
            call_count += 1
            return sum(x)

        cached_sum = self.solution.cache(sum_varargs, 10)
        self.assertEqual(6, cached_sum(1, 2, 3))
        self.assertEqual(9, cached_sum(4, 5))
        self.assertEqual(6, cached_sum(1, 2, 3))
        self.assertEqual(6, cached_sum(3, 2, 1, 0))

        self.assertEqual(3, call_count)

if __name__ == '__main__':
    SecondHomeworkTests.main()

