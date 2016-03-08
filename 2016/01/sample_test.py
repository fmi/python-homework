import unittest

import solution


class TestImages(unittest.TestCase):
    image = [
        [(0, 0, 255), (0, 255, 0), (0, 0, 255)],
        [(255, 0, 0), (0, 0, 255), (0, 255, 0)],
        [(0, 255, 0), (0, 255, 0), (255, 0, 0)]]

    def test_rotate_left(self):
        self.assertEqual(
            solution.rotate_left(self.image),
            [[(0, 0, 255), (0, 255, 0), (255, 0, 0)],
             [(0, 255, 0), (0, 0, 255), (0, 255, 0)],
             [(0, 0, 255), (255, 0, 0), (0, 255, 0)]])

    def test_lighten(self):
        self.assertEqual(
            solution.lighten(self.image, 0.5),
            [[(127, 127, 255), (127, 255, 127), (127, 127, 255)],
             [(255, 127, 127), (127, 127, 255), (127, 255, 127)],
             [(127, 255, 127), (127, 255, 127), (255, 127, 127)]])

    def test_invert(self):
        self.assertEqual(
            solution.invert(self.image),
            [[(255, 255, 0), (255, 0, 255), (255, 255, 0)],
             [(0, 255, 255), (255, 255, 0), (255, 0, 255)],
             [(255, 0, 255), (255, 0, 255), (0, 255, 255)]])

    def test_create_histogram(self):
        self.assertEqual(
            solution.create_histogram(self.image),
            {'blue': {0: 6, 255: 3},
             'green': {0: 5, 255: 4},
             'red': {0: 7, 255: 2}})


if __name__ == '__main__':
    unittest.main()
