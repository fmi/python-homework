import unittest

import solution

class HoroscopeTest(unittest.TestCase):

    def test_aries(self):
        self.assertEqual(solution.what_is_my_sign(1, 4), 'Овен')

    def test_taurus(self):
        self.assertEqual(solution.what_is_my_sign(6, 5), 'Телец')

    def test_gemini(self):
        self.assertEqual(solution.what_is_my_sign(16, 6), 'Близнаци')

    def test_cancer(self):
        self.assertEqual(solution.what_is_my_sign(8, 7), 'Рак')

    def test_leo(self):
        self.assertEqual(solution.what_is_my_sign(1, 8), 'Лъв')

    def test_virgo(self):
        self.assertEqual(solution.what_is_my_sign(2, 9), 'Дева')

    def test_libra(self):
        self.assertEqual(solution.what_is_my_sign(5, 10), 'Везни')

    def test_scorpio(self):
        self.assertEqual(solution.what_is_my_sign(7, 11), 'Скорпион')

    def test_sagittarius(self):
        self.assertEqual(solution.what_is_my_sign(11, 12), 'Стрелец')

    def test_capricorn(self):
        self.assertEqual(solution.what_is_my_sign(1, 1), 'Козирог')

    def test_aquaris(self):
        self.assertEqual(solution.what_is_my_sign(2, 2), 'Водолей')

    def test_pisces(self):
        self.assertEqual(solution.what_is_my_sign(9, 3), 'Риби')

    def test_living_on_the_edge(self):
        self.assertEqual(solution.what_is_my_sign(20, 6), 'Близнаци')

    def test_sludge(self):
        self.assertEqual(solution.what_is_my_sign(21, 5), 'Близнаци')

    def test_named_arguments(self):
        self.assertEqual(solution.what_is_my_sign(month=6, day=20), 'Близнаци')

if __name__ == '__main__':
    unittest.main()
