import unittest
import solution


class TestFileSystem(unittest.TestCase):
    def test_minimal(self):
        fs = solution.FileSystem(10)
        self.assertEqual(fs.size, 10)
        self.assertEqual(fs.available_size, 9)

    def test_create_directory(self):
        fs = solution.FileSystem(16)
        fs.create('/home', directory=True)
        home = fs.get_node('/home')
        self.assertTrue(home.is_directory)

    def test_create_file(self):
        fs = solution.FileSystem(32)
        content = 'Nineteen characters'
        fs.create('/data', content=content)
        file = fs.get_node('/data')
        self.assertFalse(file.is_directory)
        self.assertEqual(file.content, content)

    def test_overwrite(self):
        fs = solution.FileSystem(32)
        fs.create('/i_was_here_first')
        with self.assertRaises(solution.DestinationNodeExistsError):
            fs.create('/i_was_here_first')


if __name__ == '__main__':
    unittest.main()
