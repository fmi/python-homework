import unittest
from solution import *

class BiDictTestCase(unittest.TestCase):
    def setUp(self):
        self.person = BiDict({'name': 'Кънчо', 'age': 18, 'sex': 'M'})

    def test_get_a_key(self):
        self.assertEqual(self.person['name'], 'Кънчо')

    def test_assign_value(self):
        self.person['last_name'] = 'Кънчов'
        self.assertEqual(self.person['last_name'], 'Кънчов')

    def test_assign_value_and_reverse(self):
        self.person['last_name'] = 'Кънчов'
        self.person.inverse()
        self.assertEqual(self.person['Кънчов'], 'last_name')

    def test_double_inverse(self):
        self.person.inverse()
        self.person.inverse()
        self.assertEqual(self.person['name'], 'Кънчо')

    def test_lots_of_even_inverses(self):
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.assertEqual(self.person['name'], 'Кънчо')

    def test_lots_of_odd_inverses(self):
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.person.inverse()
        self.assertEqual(self.person['Кънчо'], 'name')

    def test_inverse(self):
        self.person.inverse()
        self.assertIn('Кънчо', self.person.keys())

    def test_circular_values(self):
        circular = BiDict({1: 2, 2: 3, 3: 1})
        inversed_circular = BiDict({1: 3, 2: 1, 3: 2})
        circular.inverse()
        self.assertEqual(circular, inversed_circular)

    def test_copied_circular_values(self):
        circular = BiDict({1: 2, 2: 3, 3: 1})
        inversed_circular = circular.copy()
        inversed_circular.inverse()
        inversed_circular.inverse()
        self.assertEqual(circular, inversed_circular)

    def test_invalid_value(self):
        self.assertRaises(TypeError, self.person.update, {'sports': ['boxing',]})

    def test_hashing_self(self):
        self.assertRaises(TypeError, self.person.update, {'clone': self.person})

    def test_has_dict_attrs(self):
        self.assertIn('keys', dir(self.person))
        self.assertIn('pop', dir(self.person))
        self.assertIn('copy', dir(self.person))

if __name__ == '__main__':
    unittest.main()
