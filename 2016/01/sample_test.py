import unittest

import solution


class TestImages(unittest.TestCase):
    image = [
        [(0, 0, 255), (0, 255, 0), (0, 0, 255)],
        [(255, 0, 0), (0, 0, 255), (0, 255, 0)],
        [(0, 255, 0), (0, 255, 0), (255, 0, 0)]]

    def test_rotate_left(self):
        rotated = solution.rotate_left(self.image)
        expected = [[(0, 0, 255), (0, 255, 0), (255, 0, 0)],
                    [(0, 255, 0), (0, 0, 255), (0, 255, 0)],
                    [(0, 0, 255), (255, 0, 0), (0, 255, 0)]]

        for i in range(len(rotated)):
            for j in range(len(rotated[0])):
                self.assertEqual(expected[i][j], rotated[i][j])

    def test_lighten(self):
        lighten = solution.lighten(self.image, 0.5)
        expected = [[(127, 127, 255), (127, 255, 127), (127, 127, 255)],
                    [(255, 127, 127), (127, 127, 255), (127, 255, 127)],
                    [(127, 255, 127), (127, 255, 127), (255, 127, 127)]]

        for i in range(len(lighten)):
            for j in range(len(lighten[0])):
                self.assertEqual(expected[i][j], lighten[i][j])

    def test_invert(self):
        inverted = solution.invert(self.image)
        expected = [[(255, 255, 0), (255, 0, 255), (255, 255, 0)],
                    [(0, 255, 255), (255, 255, 0), (255, 0, 255)],
                    [(255, 0, 255), (255, 0, 255), (0, 255, 255)]]

        for i in range(len(inverted)):
            for j in range(len(inverted[0])):
                self.assertEqual(expected[i][j], inverted[i][j])

    def test_create_histogram(self):
        self.assertEqual(
            solution.create_histogram(self.image),
            {'blue': {0: 6, 255: 3},
             'green': {0: 5, 255: 4},
             'red': {0: 7, 255: 2}})


if __name__ == '__main__':
    unittest.main()
