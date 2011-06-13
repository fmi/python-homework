import unittest
from solution import gt, lt, pred, for_any, for_all, present, eq, oftype

class PredicatesTest(unittest.TestCase):
    def test_simple_gt(self):
        self.assertTrue(gt(2)(4))
        self.assertFalse(gt(2)(0))

    def test_simple_lt(self):
        self.assertTrue(lt(2)(0))
        self.assertFalse(lt(2)(4))

    def test_combining_gt_and_lt(self):
        self.assertTrue((gt(2) & lt(4))(3))
        self.assertFalse((gt(2) & lt(4))(0))
        self.assertFalse((gt(2) & lt(4))(6))

    def test_combining_lt_and_gt(self):
        self.assertTrue((lt(4) & gt(2))(3))
        self.assertFalse((lt(4) & gt(2))(0))

    def test_pred(self):
        self.assertTrue(pred(lambda x: x > 2)(4))
        self.assertFalse(pred(lambda x: x > 2)(0))

    def test_combiding_pred_with_gt(self):
        self.assertTrue((pred(lambda x: x > 2) & lt(4))(3))

    def test_disjunction(self):
        self.assertTrue((gt(10) | lt(5))(0))
        self.assertTrue((gt(10) | lt(5))(15))

        self.assertFalse((gt(10) | lt(5))(7))

    def test_negation(self):
        self.assertTrue((~gt(10))(5))
        self.assertFalse((~gt(10))(15))

    def test_simple_eq(self):
        self.assertTrue(eq(10)(10))
        self.assertFalse(eq(10)(5))

    def test_implication(self):
        self.assertTrue((gt(10) >> eq(20))(20))
        self.assertTrue((gt(10) >> eq(20))(0))
        self.assertTrue((gt(10) >> eq(0))(0))

        self.assertFalse((gt(10) >> eq(20))(15))

    def test_oftype(self):
        self.assertTrue(oftype(complex)(1j))
        self.assertTrue(oftype(object)(1j))

        self.assertFalse(oftype(int)(1j))

    def test_for_any(self):
        self.assertTrue(for_any(eq(10), eq(5))(10))
        self.assertTrue(for_any(eq(10), eq(5), eq(0))(0))

        self.assertFalse(for_any(eq(10), eq(5), eq(0))(1))

    def test_for_all(self):
        self.assertTrue(for_all(gt(0), lt(10))(5))
        self.assertTrue(for_all(gt(0), lt(10), eq(5))(5))

        self.assertFalse(for_all(gt(0), lt(10), eq(5))(7))
        self.assertFalse(for_all(eq(0), eq(1))(0))

    def test_present(self):
        self.assertTrue(present()(0))
        self.assertFalse(present()(None))

if __name__ == '__main__':
    unittest.main()
