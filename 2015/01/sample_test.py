import unittest
import solution


class TestSigns(unittest.TestCase):
    def test_chinese_signs(self):
        self.assertEqual(solution.interpret_chinese_sign(1986), 'tiger')

    def test_western_signs(self):
        self.assertEqual(solution.interpret_western_sign(1, 5), 'taurus')

    def test_intersect(self):
        self.assertEqual(
            solution.interpret_both_signs(8, 5, 1989),
            ('taurus', 'snake')
        )

if __name__ == '__main__':
    unittest.main()
