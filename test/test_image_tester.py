import unittest
from os import path
from pyimagetest import ImageTester


class Tester(ImageTester, unittest.TestCase):
    @property
    def default_test_image_file(self) -> str:
        # The test image was downloaded from
        # http://www.r0k.us/graphics/kodak/kodim15.html
        # and is cleared for unrestricted usage
        return path.join(path.dirname(__file__), "test_image.png")


if __name__ == "__main__":
    unittest.main()
