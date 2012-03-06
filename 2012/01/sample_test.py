import unittest
from solution import *

class FirstHomeworkSimpleTests(unittest.TestCase):
    def test_not_making_any_spam(self):
        self.assertEqual(prepare_meal(7), '')

    def test_prepare_single_spam(self):
        self.assertEqual(prepare_meal(3), 'spam')

    def test_prepare_triple_spam(self):
        self.assertEqual(prepare_meal(27), 'spam spam spam')

    def test_prepare_eggs(self):
        self.assertEqual(prepare_meal(5), 'eggs')

    def test_prepare_spam_and_eggs(self):
        self.assertEqual(prepare_meal(15), 'spam and eggs')

    def test_prepare_two_spams_with_one_egg(self):
        self.assertEqual(prepare_meal(45), 'spam spam and eggs')

if __name__ == "__main__":
    unittest.main()
