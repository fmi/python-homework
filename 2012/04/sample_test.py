import unittest
import solution

class PrimesTest(unittest.TestCase):
    def test_first_few_primes(self):
        primes = solution.primes()
        self.assertEqual(2, next(primes))
        self.assertEqual(3, next(primes))
        self.assertEqual(5, next(primes))
        self.assertEqual(7, next(primes))
        self.assertEqual(11, next(primes))
        self.assertEqual(13, next(primes))

    def test_first_few_semi_primes(self):
        semiprimes = solution.semiprimes()
        self.assertEqual(4, next(semiprimes))
        self.assertEqual(6, next(semiprimes))
        self.assertEqual(9, next(semiprimes))
        self.assertEqual(10, next(semiprimes))
        self.assertEqual(14, next(semiprimes))
        self.assertEqual(15, next(semiprimes))

if __name__ == '__main__':
    unittest.main()
