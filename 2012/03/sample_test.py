import unittest
from solution import *

class BiDictTestCase(unittest.TestCase):
    def setUp(self):
        self.person = BiDict({'name': 'Кънчо', 'age': 18, 'sex': 'M'})

    def test_get_a_key(self):
        self.assertEqual(self.person['name'], 'Кънчо')

    def test_inverse(self):
        self.person.invert()
        self.assertIn('Кънчо', self.person.keys())

    def test_invalid_value(self):
        self.assertRaises(TypeError, self.person.update, {'sports': ['boxing',]})

    def test_has_dict_attrs(self):
        self.assertIn('keys', dir(self.person))
        self.assertIn('pop', dir(self.person))
        self.assertIn('copy', dir(self.person))


if __name__ == '__main__':
    unittest.main()
