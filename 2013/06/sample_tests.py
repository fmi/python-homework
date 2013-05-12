import unittest
from random import randint, shuffle, choice
from solution import *


class PythonTest(unittest.TestCase):
    def test_python_placement(self):
        directions = [Python.UP, Python.DOWN, Python.LEFT, Python.DOWN]
        direction = choice(directions)

        world = World(25)
        py_size = 3
        py = Python(world, Vec2D(10, 10), py_size, direction)
        self.assertIsInstance(world[10][10].contents, PythonHead)

    def test_python_movement_basic(self):
        directions = [Python.UP, Python.DOWN, Python.LEFT, Python.DOWN]
        direction = choice(directions)

        world = World(25)
        py_size = randint(3, 5)
        py = Python(world, Vec2D(10, 10), py_size, direction)
        old_direction = py.direction
        py.move(direction)
        x, y = Vec2D(10, 10) + direction

        self.assertIsInstance(world[x][y].contents, PythonHead)

    def test_wallpunch_death(self):
        world = World(20)
        py = Python(world, Vec2D(5, 5), 3, Python.LEFT)

        with self.assertRaises(Death):
            {py.move(Python.LEFT) for repeat in range(0, 10)}


class WorldTest(unittest.TestCase):
    def test_bigbang(self):
        world = World(10)
        self.assertEqual(len(world), 10)

        bigworld = World(100)
        self.assertEqual(len(bigworld), 100)

    def test_world_indexing(self):
        world = World(10)
        with self.assertRaises(IndexError):
            cell = world[5][1337]

        row, col = randint(0, 9), randint(0, 9)
        self.assertIsInstance(world[row][col], Cell)

    def test_cell(self):
        cell = Cell(Food(energy=5))
        self.assertFalse(cell.is_empty())

    def test_cell_empty(self):
        emptycell = Cell()
        self.assertTrue(emptycell.is_empty())

    def test_cell_invalid(self):
        with self.assertRaises(TypeError):
            badcell = Cell("snakesandladders")

if __name__ == '__main__':
    unittest.main()
