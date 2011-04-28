import unittest
from solution import gt, lt, pred, for_any, for_all, present, eq, oftype

class PredicatesTest(unittest.TestCase):
    def test_simple_gt(self):
        self.assertTrue(gt(2)(4))

    def test_combining_gt_and_lt(self):
        self.assertTrue((gt(2) & lt(4))(3))

    def test_combining_lt_and_gt(self):
        self.assertTrue((lt(4) & gt(2))(3))

    def test_pred(self):
        self.assertTrue(pred(lambda x: x > 2)(4))

if __name__ == '__main__':
    unittest.main()
