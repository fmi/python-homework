import unittest
from solution import *

from numbers import Number

class OperatorAppliedError(Exception):
    pass

class ErrorRaisingNumber(Number):
    def __init__(self):
        pass
    
    def raising_operator(*args):
        raise OperatorAppliedError

    __add__ = __radd__ = raising_operator

class ThirdHomeworkSimpleTests(unittest.TestCase):
    def test_operator_is_delayed_when_applied(self):
        error_raising_number = ErrorRaisingNumber()
        lazy_number = Lazy(error_raising_number) + 8 # shouldn't raise an error

    def test_operator_is_applied_when_forced(self):
        error_raising_number = ErrorRaisingNumber()
        lazy_number = Lazy(error_raising_number) + 8
        with self.assertRaises(OperatorAppliedError):
            lazy_number.force() # should raise an error

    def test_operator_evaluation_works_correctly(self):
        number = Lazy(42)
        number += 8
        self.assertEqual(number.force(), 50)

if __name__ == "__main__":
    unittest.main()
