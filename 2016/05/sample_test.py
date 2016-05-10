import unittest

import solution


class TestCritic(unittest.TestCase):
    def test_indentation(self):
        code = ('def ugly(indent):\n'
                '     return indent')
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[2]), {'indentation is 5 instead of 4'})

    def test_two_statements_on_one_line(self):
        code = 'a = 5; b = 6'
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[1]),
                            {'multiple expressions on the same line'})

    def test_too_deep_nesting(self):
        code = ("def some_func():\n"
                "    for char in a_variable:\n"
                "        if char != 'a':\n"
                "            for _ in range(10):\n"
                "                print('SOOOO MUUUCH INDENTATION')\n")
        issues = solution.critic(code, max_nesting=3)
        print(issues)
        self.assertSetEqual(set(issues[5]), {'nesting too deep (4 > 3)'})


    def test_long_line_with_several_statements(self):
        code = ("def some_func():\n"
                "    a_variable = 'some text';"
                " another_variable = 'some more text';"
                " even_moar_variables = 'just for to pass the time'")
        issues = solution.critic(code)
        self.assertSetEqual(set(issues[2]), {
            'line too long (116 > 79)',
            'multiple expressions on the same line'
        })


if __name__ == '__main__':
    unittest.main()
