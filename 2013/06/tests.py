import unittest
from random import randint, shuffle, choice
from solution import *


class PythonTest(unittest.TestCase):
    def test_python_placement(self):
        directions = [Python.UP, Python.DOWN, Python.LEFT, Python.DOWN]
        direction = choice(directions)

        world = World(25)
        py_size = randint(3, 5)
        py = Python(world, Vec2D(10, 10), py_size, direction)
        self.assertIsInstance(world[10][10].contents, PythonHead)

        position = Vec2D(10, 10)
        for part_num in range(py_size):
            x, y = position - direction
            self.assertIsInstance(world[x][y].contents, PythonPart)

    def test_python_movement_basic(self):
        directions = [Python.UP, Python.DOWN, Python.LEFT, Python.DOWN]
        direction = choice(directions)

        world = World(25)
        py_size = randint(3, 5)
        py = Python(world, Vec2D(10, 10), py_size, direction)

        py.move(direction)
        x, y = Vec2D(10, 10) + direction

        self.assertIsInstance(world[x][y].contents, PythonHead)
        for part_no in range(0, py_size):
            x, y = Vec2D(10, 10) - direction * part_no
            self.assertIsInstance(world[x][y].contents, PythonPart)

    def test_ouroboros_death(self):
        world = World(25)
        py = Python(world, Vec2D(10, 10), 5, Python.LEFT)
        py.move(Python.LEFT)
        py.move(Python.UP)
        py.move(Python.UP)
        py.move(Python.RIGHT)

        with self.assertRaises(Death):
            py.move(Python.DOWN)
            py.move(Python.DOWN)

    def test_wallpunch_death(self):
        world = World(20)
        py = Python(world, Vec2D(5, 5), 3, Python.LEFT)

        with self.assertRaises(Death):
            {py.move(Python.LEFT) for repeat in range(0, 10)}

    def test_snake_death(self):
        world = World(20)
        py1 = Python(world, Vec2D(5, 5), 3, Python.UP)
        py2 = Python(world, Vec2D(8, 5), 3, Python.UP)

        cartesian_coord = False

        try:
            {py2.move(Python.LEFT) for repeat in range(0, 5)}
        except Death:
            cartesian_coord = True

        py2 = Python(world, Vec2D(5, 8), 3, Python.UP)
        screen_coord = False

        try:
            {py2.move(Python.LEFT) for repeat in range(0, 5)}
        except Death:
            cartesian_coord = True

        self.assertTrue(cartesian_coord or screen_coord)

    def test_growth(self):
        world = World(20)
        py = Python(world, Vec2D(10, 10), 3, Python.LEFT)
        food = Food(energy=5)
        world[8][10] = Cell(food)
        world[10][8] = Cell(food)

        py.move(Python.LEFT)
        self.assertEqual(py.size, 3)

        py.move(Python.LEFT)

        cartesian_coord = isinstance(world[8][10].contents, PythonHead)
        screen_coord = isinstance(world[10][8].contents, PythonHead)
        self.assertTrue(cartesian_coord or screen_coord)

        self.assertEqual(py.size, 4)

    def test_move_backwards(self):
        world = World(20)
        py = Python(world, Vec2D(10, 10), 3, Python.LEFT)

        directions = [Python.UP, Python.DOWN, Python.LEFT, Python.DOWN]
        direction = choice(directions)

        py.move(direction)
        with self.assertRaises(ValueError):
            py.move(-direction)


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
        with self.assertRaises(IndexError):
            cell = world[1337]
        with self.assertRaises(IndexError):
            cell = world[1337][1337]

        row, col = randint(0, 9), randint(0, 9)
        self.assertIsInstance(world[row][col], Cell)

    def test_world_manipulation(self):
        world = World(10)
        row, col = randint(0, 9), randint(0, 9)
        world[row][col] = Cell(Food(energy=5))

        self.assertFalse(world[row][col].is_empty())
        self.assertEqual(world[row][col].contents.energy, 5)

    def test_cell(self):
        cell = Cell(Food(energy=5))
        self.assertFalse(cell.is_empty())
        self.assertEqual(cell.contents.energy, 5)

    def test_cell_empty(self):
        emptycell = Cell()
        self.assertTrue(emptycell.is_empty())

    def test_cell_invalid(self):
        with self.assertRaises(TypeError):
            badcell = Cell("snakesandladders")

if __name__ == '__main__':
    unittest.main()
