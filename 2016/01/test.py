import unittest

import solution


class TestImages(unittest.TestCase):
    image = [
        [(0, 0, 255), (0, 255, 0), (0, 0, 255)],
        [(255, 0, 0), (0, 0, 255), (0, 255, 0)],
        [(0, 255, 0), (0, 255, 0), (255, 0, 0)]]

    rectangle_image = [
        [(100, 0, 255), (0, 255, 0), (0, 12, 255), (90, 0, 255)],
        [(255, 0, 4), (0, 42, 255), (0, 54, 0), (1, 255, 0)],
        [(0, 255, 1), (72, 255, 0), (255, 0, 0), (255, 60, 1)]]

    def test_rotate_left(self):
        rotated = solution.rotate_left(self.image)
        expected = [[(0, 0, 255), (0, 255, 0), (255, 0, 0)],
                    [(0, 255, 0), (0, 0, 255), (0, 255, 0)],
                    [(0, 0, 255), (255, 0, 0), (0, 255, 0)]]

        for i in range(len(rotated)):
            for j in range(len(rotated[i])):
                self.assertEqual(expected[i][j], rotated[i][j])

    def test_rotate_left_rectangle(self):
        rotated = solution.rotate_left(self.rectangle_image)
        expected = [[(90, 0, 255), (1, 255, 0), (255, 60, 1)],
                    [(0, 12, 255), (0, 54, 0), (255, 0, 0)],
                    [(0, 255, 0), (0, 42, 255), (72, 255, 0)],
                    [(100, 0, 255), (255, 0, 4), (0, 255, 1)]]

        for i in range(len(rotated)):
            for j in range(len(rotated[i])):
                self.assertEqual(expected[i][j], rotated[i][j])

    def test_rotate_right(self):
        rotated = solution.rotate_right(self.image)
        expected = [[(0, 255, 0), (255, 0, 0), (0, 0, 255)],
                    [(0, 255, 0), (0, 0, 255), (0, 255, 0)],
                    [(255, 0, 0), (0, 255, 0), (0, 0, 255)]]

        for i in range(len(rotated)):
            for j in range(len(rotated[i])):
                self.assertEqual(expected[i][j], rotated[i][j])

    def test_rotate_right_rectangle(self):
        rotated = solution.rotate_right(self.rectangle_image)
        expected = [[(0, 255, 1), (255, 0, 4), (100, 0, 255)],
                    [(72, 255, 0), (0, 42, 255), (0, 255, 0)],
                    [(255, 0, 0), (0, 54, 0), (0, 12, 255)],
                    [(255, 60, 1), (1, 255, 0), (90, 0, 255)]]

        for i in range(len(rotated)):
            for j in range(len(rotated[i])):
                self.assertEqual(expected[i][j], rotated[i][j])

    def test_lighten(self):
        lighten = solution.lighten(self.image, 0.5)
        expected = [[(127, 127, 255), (127, 255, 127), (127, 127, 255)],
                    [(255, 127, 127), (127, 127, 255), (127, 255, 127)],
                    [(127, 255, 127), (127, 255, 127), (255, 127, 127)]]

        for i in range(len(lighten)):
            for j in range(len(lighten[i])):
                for k in range(len(lighten[i][j])):
                    self.assertLessEqual(
                        abs(expected[i][j][k]-lighten[i][j][k]), 1)

    def test_lighten_rectangle(self):
        lighten = solution.lighten(self.rectangle_image, 0.5)
        expected = [[(177, 127, 255), (127, 255, 127),
                     (127, 133, 255), (172, 127, 255)],
                    [(255, 127, 129), (127, 148, 255),
                     (127, 154, 127), (128, 255, 127)],
                    [(127, 255, 128), (163, 255, 127),
                     (255, 127, 127), (255, 157, 128)]]

        for i in range(len(lighten)):
            for j in range(len(lighten[i])):
                for k in range(len(lighten[i][j])):
                    self.assertLessEqual(
                        abs(expected[i][j][k]-lighten[i][j][k]), 1)

    def test_darken(self):
        darken = solution.darken(self.image, 0.5)
        expected = [[(0, 0, 127), (0, 127, 0), (0, 0, 127)],
                    [(127, 0, 0), (0, 0, 127), (0, 127, 0)],
                    [(0, 127, 0), (0, 127, 0), (127, 0, 0)]]

        for i in range(len(darken)):
            for j in range(len(darken[i])):
                for k in range(len(darken[i][j])):
                    self.assertLessEqual(
                        abs(expected[i][j][k]-darken[i][j][k]), 1)

    def test_darken_rectangle(self):
        darken = solution.darken(self.rectangle_image, 0.5)
        expected = [[(50, 0, 127), (0, 127, 0), (0, 6, 127), (45, 0, 127)],
                    [(127, 0, 2), (0, 21, 127), (0, 27, 0), (0, 127, 0)],
                    [(0, 127, 0), (36, 127, 0), (127, 0, 0), (127, 30, 0)]]

        for i in range(len(darken)):
            for j in range(len(darken[i])):
                for k in range(len(darken[i][j])):
                    self.assertLessEqual(
                        abs(expected[i][j][k]-darken[i][j][k]), 1)

    def test_invert(self):
        inverted = solution.invert(self.image)
        expected = [[(255, 255, 0), (255, 0, 255), (255, 255, 0)],
                    [(0, 255, 255), (255, 255, 0), (255, 0, 255)],
                    [(255, 0, 255), (255, 0, 255), (0, 255, 255)]]

        for i in range(len(inverted)):
            for j in range(len(inverted[i])):
                self.assertEqual(expected[i][j], inverted[i][j])

    def test_invert_rectangle(self):
        inverted = solution.invert(self.rectangle_image)
        expected = [
            [(155, 255, 0), (255, 0, 255), (255, 243, 0), (165, 255, 0)],
            [(0, 255, 251), (255, 213, 0), (255, 201, 255), (254, 0, 255)],
            [(255, 0, 254), (183, 0, 255), (0, 255, 255), (0, 195, 254)]]

        for i in range(len(inverted)):
            for j in range(len(inverted[i])):
                self.assertEqual(expected[i][j], inverted[i][j])

    def test_create_histogram(self):
        self.assertEqual(
            solution.create_histogram(self.image),
            {'blue': {0: 6, 255: 3},
             'green': {0: 5, 255: 4},
             'red': {0: 7, 255: 2}})

    def test_create_histogram_rectangle(self):
        self.assertEqual(
            solution.create_histogram(self.rectangle_image),
            {'green': {0: 4, 255: 4, 54: 1, 60: 1, 42: 1, 12: 1},
             'red': {0: 5, 255: 3, 1: 1, 100: 1, 72: 1, 90: 1},
             'blue': {0: 5, 255: 4, 1: 2, 4: 1}},
        )


if __name__ == '__main__':
    unittest.main()
