import unittest
from solution import *

class FifthHomeworkSimpleTests(unittest.TestCase):
    def test_tokenize(self):
        self.assertEqual(
            ['(', 'times', '3', '"spam"', ')'],
            tokenize('(times 3 "spam")'))

    def test_identifiers(self):
        self.assertEqual(
            {'sum', 'number'},
            identifiers(['(', 'sum', '42', 'number', 'NUMBER', ')']))

    def test_case_sensitive(self):
        self.assertEqual('(spam "SPAM")', case_sensitive('(Spam "SPAM")', {'spam'}))

if __name__ == "__main__":
    unittest.main()
