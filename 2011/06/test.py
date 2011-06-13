import unittest
from solution import *

class MultiDispatchTest(unittest.TestCase):
    def test_vanilla_case(self):
        class Spam:
            def multiplier(self): return 2

            @multimethod
            def eggs(self, arg: int):
                return arg * self.multiplier()

        self.assertEqual(4, Spam().eggs(2))

    def test_single_argument_two_independant_types(self):
        class Spam:
            def __init__(self, value): self.value = value

            @multimethod
            def eggs(self, arg: int):
                return self.value * arg

            @eggs.multimethod
            def eggs(self, arg: str):
                return self.value + arg

        self.assertEqual(10, Spam(2).eggs(5))
        self.assertEqual('spam!',  Spam('spam').eggs('!'))

    def test_invoking_a_default(self):
        class Spam:
            @multimethod
            def eggs(self, arg: object):
                return 'object'

        self.assertEqual('object', Spam.eggs(12))

    def test_unspecified_types_default_to_object(self):
        class Spam:
            @multimethod
            def eggs(self, arg: int):
                return 'integer'
            
            @eggs.multimethod
            def eggs(self, arg):
                return 'object'

    def test_cannot_dispatch(self):
        class Spam:
            @multimethod
            def eggs(self, arg: int): pass

        with self.assertRaises(LookupError):
            Spam().eggs('')


    def test_does_not_interfere_with_varargs(self):
        class Spam:
            @multimethod
            def eggs(self, arg: int, *args, **kwargs):
                return 'integer'

        self.assertEqual('integer', Spam().eggs(10, 'baba', 'dyado'))

if __name__ == '__main__':
    unittest.main()
