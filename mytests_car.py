import unittest


class MyTests(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(5, 3), 8)

    def test_substract(self):
        self.assertEqual(substract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(multiply(5, 3), 15)

    def test_divide(self):
        self.assertEqual(divide(9, 3), 3)


if __name__ == '__main__':
    unittest.main()
