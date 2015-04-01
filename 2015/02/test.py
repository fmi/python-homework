import unittest

import solution as s


class ExtractTypeTest(unittest.TestCase):
    def test_string_and_list(self):
        fizzbuzz_input = [('f', 1), ([], 0), ('i', 1),
                          ('z', 2), ('bu', 1), ('z', 2)]
        self.assertEqual("fizzbuzz", s.extract_type(fizzbuzz_input, str))

    def test_string_with_different_types(self):
        fizzbuzz_input = [('f', 1), (5, 10), ('i', 1), (0.3, 100),
                          ('z', 2), ('bu', 1), ('z', 2)]
        self.assertEqual("fizzbuzz", s.extract_type(fizzbuzz_input, str))

    def test_with_ints_and_floats(self):
        self.assertEqual("42.151.3", s.extract_type(
            [(1, 1), (42.15, 1), (0, 0), (1.3, 1)],
            float))

    def test_with_no_symbols_of_given_type(self):
        self.assertEqual('', s.extract_type([('a', 1), ('b', 1)], int))

    def test_with_empty_list(self):
        self.assertEqual('', s.extract_type([], type))


class ReversedDictTest(unittest.TestCase):
    def test_capitals(self):
        input = {
            "Israel": "Jerusalem",
            "Austria": "Vienna",
            "Palestine": "Jerusalem",
            "Sweden": "Stockholm"
        }
        self.assertEqual(s.reversed_dict(input)['Stockholm'], 'Sweden')
        self.assertEqual(s.reversed_dict(input)['Vienna'], 'Austria')
        self.assertIn('Jerusalem', s.reversed_dict(input))

    def test_empty_dict(self):
        self.assertEqual({}, s.reversed_dict({}))

    def test_with_duplicated_values(self):
        result = s.reversed_dict({'foo': 'bar', 'baz': 'bar', 'fizz': 'buzz'})
        self.assertIn('bar', result.keys())
        self.assertIn('buzz', result.keys())
        self.assertIn('fizz', result.values())
        self.assertIn(result['bar'], ['foo', 'baz'])


class UnflattenDictTest(unittest.TestCase):
    def test_with_already_unflatten_dict(self):
        unflatten = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(unflatten, s.unflatten_dict(unflatten))

    def test_with_two_levels_of_nesting(self):
        self.assertEqual(
            {'a': 1, 'b': {'a': 2}},
            s.unflatten_dict({'a': 1, 'b.a': 2})
        )

    def test_with_three_levels_of_nesting(self):
        self.assertEqual(
            {'a': 1, 'b': {'a': 2, 'b': {'a': 1}}},
            s.unflatten_dict({'a': 1, 'b.a': 2, 'b.b.a': 1})
        )

    def test_example(self):
        self.assertEqual(
            {'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y': 9, }}, 'd': [1, 2, 3]},
            s.unflatten_dict({'a': 1, 'c.a': 2, 'c.b.x': 5, 'c.b.y': 9, 'd': [1, 2, 3]})
        )


class FlattenDictTest(unittest.TestCase):
    def test_with_already_flatten_dict(self):
        flatten = {'a': 1, 'b': 2, 'c': 3}
        self.assertEqual(flatten, s.flatten_dict(flatten))

    def test_with_two_levels_of_nesting(self):
        self.assertEqual(
            {'a': 1, 'b.a': 2},
            s.flatten_dict({'a': 1, 'b': {'a': 2}})
        )

    def test_with_three_levels_of_nesting(self):
        self.assertEqual(
            {'a': 1, 'b.a': 2, 'b.b.a': 1},
            s.flatten_dict({'a': 1, 'b': {'a': 2, 'b': {'a': 1}}})
        )

    def test_example_case(self):
        self.assertEqual(
            s.flatten_dict({'a': 1, 'c': {'a': 2, 'b': {'x': 5, 'y': 9}}, 'd': [1, 2, 3]}),
            {'a': 1, 'c.a': 2, 'c.b.x': 5, 'c.b.y': 9, 'd': [1, 2, 3]},
        )


class RepsTest(unittest.TestCase):
    def test_with_uniques_only(self):
        self.assertEqual(tuple(), s.reps([1, 2, 3, 4]))

    def test_with_reps_only(self):
        self.assertEqual((1, 2, 1, 2, 1, 2), s.reps((1, 2, 1, 2, 1, 2)))

    def test_example_case(self):
        self.assertEqual(
            (1, 4, 2, 2, 4, 1, 2, 1),
            s.reps([1, 4, 2, 6, 7, 2, 4, 11, 1, 9, 0, 2, 5, 3, 1])
        )


if __name__ == '__main__':
    unittest.main()
