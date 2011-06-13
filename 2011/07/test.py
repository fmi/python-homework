import unittest
from solution import *

class InterfaceTest(unittest.TestCase):
    def test_add_missing_docstring(self):
        class stack(metaclass=interface):
            def pop(self):
                """Pops the stack head"""

        @stack
        class MyStack:
            def pop(self):
                pass

        self.assertEqual("Pops the stack head", MyStack.pop.__doc__)

    def test_does_not_touch_existing_docstring(self):
        class stack(metaclass=interface):
            def pop(self):
                """Interface doc"""

        @stack
        class MyStack:
            def pop(self):
                """Implementor doc"""

        self.assertEqual("Implementor doc", MyStack.pop.__doc__)

    def test_complains_for_different_number_of_arguments(self):
        class spec(metaclass=interface):
            def foo(self, a): pass

        with self.assertRaises(AssertionError):
            @spec
            class MyStack:
                def foo(self, a, b): pass

    def test_complains_if_arguments_have_different_names(self):
        class spec(metaclass=interface):
            def foo(self, a): pass

        with self.assertRaises(AssertionError):
            @spec
            class MyStack:
                def foo(self, b): pass

    def test_complains_if_arguments_have_different_defaults(self):
        class spec(metaclass=interface):
            def foo(self, a=1): pass

        with self.assertRaises(AssertionError):
            @spec
            class MyStack:
                def foo(self, a=2): pass

    def test_complains_if_there_are_additional_varargs(self):
        class spec(metaclass=interface):
            def foo(self, a): pass

        with self.assertRaises(AssertionError):
            @spec
            class MyStack:
                def foo(self, a, *args): pass

    def test_complains_if_there_are_additional_kwargs(self):
        class spec(metaclass=interface):
            def foo(self, a): pass

        with self.assertRaises(AssertionError):
            @spec
            class MyStack:
                def foo(self, a, **kwargs): pass

    def test_complains_if_there_are_different_keyword_only_args(self):
        class spec(metaclass=interface):
            def foo(self, *, a, b): pass

        with self.assertRaises(AssertionError):
            @spec
            class MyStack:
                def foo(self, *, a, c): pass

    def test_does_not_complain_when_same_kwonly_args_but_in_different_order(self):
        class spec(metaclass=interface):
            def foo(self, *, a, b): pass

        @spec
        class MyStack:
            def foo(self, *, b, a): pass

    def test_does_not_complain_when_different_annotations(self):
        class spec(metaclass=interface):
            def foo(self, arg): pass

        @spec
        class MyStack:
            def foo(self, arg: int): pass


if __name__ == '__main__':
    unittest.main()
