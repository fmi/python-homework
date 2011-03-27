import unittest
import homework

class FirstHomeworkTests(homework.Test):
    def test_make_multiset_empty(self):
        self.assertEquals({}, self.solution.make_multiset([]))

    def test_make_multiset_no_duplicates(self):
        self.assertEquals({1: 1, 2: 1}, self.solution.make_multiset([1, 2]))

    def test_make_multiset_only_duplicates(self):
        self.assertEquals({'spam': 42}, self.solution.make_multiset(['spam'] * 42))

    def test_make_multiset_with_duplicates(self):
        self.assertEquals(
          {'spam': 4, 'bacon': 2, 'eggs': 1},
          self.solution.make_multiset(['spam', 'bacon', 'spam', 'spam', 'eggs', 'bacon', 'spam'])
        )

    test_make_multiset_with_duplicates_again = test_make_multiset_with_duplicates



    def test_ordered_dict_empty(self):
        self.assertEquals([], self.solution.ordered_dict({}))

    def test_ordered_dict_homogeneous_keys(self):
        self.assertEquals(
          [(1, 'i'), (2, 'ii'), (3, 'iii')],
          self.solution.ordered_dict({1: 'i', 2: 'ii', 3: 'iii'})
        )

    test_ordered_dict_homogeneous_keys_again = test_ordered_dict_homogeneous_keys

    def test_ordered_dict_heterogeneous_keys(self):
        self.assertEquals(
          [(1, 'i'), (2.0, 'ii'), (2 ** 70, 'wait, what?')],
          self.solution.ordered_dict({1: 'i', 2.0: 'ii', 2 ** 70: 'wait, what?'})
        )

    test_ordered_dict_heterogeneous_keys_again = test_ordered_dict_heterogeneous_keys



    def test_reversed_dict_empty(self):
        self.assertEquals({}, self.solution.reversed_dict({}))

    def test_reversed_dict_no_repeating_values(self):
        self.assertEquals(
          {3: 'Nibbler', 2: 'Fillip', 1: 'Turanga'},
          self.solution.reversed_dict({'Nibbler': 3, 'Fillip': 2, 'Turanga': 1})
        )

    def test_reversed_dict_repeating_values_only(self):
        value = self.solution.reversed_dict({'Amy': 2, 'Zapp': 2, 'Kif': 2})[2]
        self.assertTrue(any(_ is value for _ in ['Amy', 'Zapp', 'Kif']))

    def test_reversed_dict_repeating_values(self):
        answer = self.solution.reversed_dict({'Nibbler': 3, 'Fillip': 2, 'Turanga': 1, 'Amy': 2})

        self.assertEquals(answer[1], 'Turanga')
        self.assertTrue(answer[2] is 'Amy' or answer[2] is 'Fillip')
        self.assertTrue(answer[3] is 'Nibbler')
        self.assertEquals(len(answer), 3)

    test_reversed_dict_repeating_values_again = test_reversed_dict_repeating_values



    def test_unique_objects_empty(self):
        self.assertEquals(0, self.solution.unique_objects([]))

    def test_unique_objects_unique_only(self):
        self.assertEquals(3, self.solution.unique_objects([1, 2, 3]))

    def test_unique_objects_identical_immutables(self):
        self.assertEquals(7, self.solution.unique_objects([1, 2, 3, 2, 1, 5, 42, None, 'asd']))

    def test_unique_objects_identical_mutables(self):
        empty1, empty2 = [], []
        objects = [empty1, empty2, empty1, empty1, {}, [empty1], [empty1]]

        answer = self.solution.unique_objects(objects)

        self.assertEquals(5, answer)

    def test_unique_objects_mutables_and_immutables(self):
        list1, list2 = [1, 2, 3], [1, 2, 3]
        objects = [42, list1, list2, list1, list2, {}, [list2], (list2,), (list2,), 42]
        answer = self.solution.unique_objects(objects)

        self.assertEquals(answer, 7)

if __name__ == '__main__':
    FirstHomeworkTests.main()

