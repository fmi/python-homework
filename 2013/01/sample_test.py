import unittest

import solution

class HoroscopeTest(unittest.TestCase):

    def test_aries(self):
        self.assertEqual(solution.what_is_my_sign(1, 4), 'Овен')

    def test_taurus(self):
        self.assertEqual(solution.what_is_my_sign(6, 5), 'Телец')

    def test_living_on_the_edge(self):
        self.assertEqual(solution.what_is_my_sign(20, 6), 'Близнаци')

    def test_named_arguments(self):
        self.assertEqual(solution.what_is_my_sign(month=6, day=20), 'Близнаци')

if __name__ == '__main__':
    unittest.main()
