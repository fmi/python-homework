import unittest
import solution


class TestSigns(unittest.TestCase):
    def test_chinese_signs(self):
        self.assertEqual(solution.interpret_chinese_sign(1986), 'tiger')
        self.assertEqual(solution.interpret_chinese_sign(1987), 'rabbit')
        self.assertEqual(solution.interpret_chinese_sign(1988), 'dragon')
        self.assertEqual(solution.interpret_chinese_sign(1989), 'snake')
        self.assertEqual(solution.interpret_chinese_sign(1990), 'horse')
        self.assertEqual(solution.interpret_chinese_sign(1991), 'sheep')
        self.assertEqual(solution.interpret_chinese_sign(1992), 'monkey')

    def test_western_signs(self):
        self.assertEqual(solution.interpret_western_sign(1, 5), 'taurus')
        self.assertEqual(solution.interpret_western_sign(9, 9), 'virgo')
        self.assertEqual(solution.interpret_western_sign(10, 10), 'libra')

    def test_intersect(self):
        self.assertEqual(
            solution.interpret_both_signs(8, 5, 1989),
            ('taurus', 'snake')
        )

    def test_negative_years(self):
        self.assertEqual(solution.interpret_chinese_sign(-23), 'rooster')

    def test_zeroth_year(self):
        self.assertEqual(solution.interpret_chinese_sign(0), 'monkey')

    def test_leap_year(self):
        self.assertEqual(solution.interpret_western_sign(29, 2), 'pisces')

if __name__ == '__main__':
    unittest.main()
