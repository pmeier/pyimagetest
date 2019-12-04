import unittest
from os import path
from pyimagetest import ImageTester


class Tester(ImageTester, unittest.TestCase):
    @property
    def default_test_image_file(self) -> str:
        return path.join(path.dirname(__file__), "test_image.png")


if __name__ == "__main__":
    unittest.main()
