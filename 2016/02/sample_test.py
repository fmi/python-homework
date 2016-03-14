import unittest

import solution


class SampleTest(unittest.TestCase):
    def test_five_plus_three(self):
        plus = solution.create_operator('+', lambda lhs, rhs: lhs + rhs)
        x = solution.create_variable('x')
        y = solution.create_variable('y')
        added_expression = solution.create_expression((x, plus, y))
        self.assertEqual(added_expression.evaluate(x=5, y=3), 8)

    def test_operators(self):
        y = solution.create_variable('y')
        twelve = solution.create_constant(12)
        expression = y + twelve
        self.assertEqual(expression.evaluate(y=3), 15)

    def test_constant_evaluation(self):
        self.assertEqual(solution.create_variable('x').evaluate(x=42), 42)
        self.assertEqual(solution.create_constant(5).evaluate(), 5)

if __name__ == '__main__':
    unittest.main()
