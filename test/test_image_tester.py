import unittest
from os import path
from itertools import combinations
from pyimagetest import ImageTester


class Tester(ImageTester, unittest.TestCase):
    @property
    def default_test_image_file(self) -> str:
        # The test image was downloaded from
        # http://www.r0k.us/graphics/kodak/kodim15.html
        # and is cleared for unrestricted usage
        return path.join(path.dirname(__file__), "test_image.png")

    def test_io(self) -> None:
        for backend1, backend2 in combinations(self.backends.values(), 2):
            image1 = self.load_image(backend1)
            image2 = self.load_image(backend2)
            self.assertImagesAlmostEqual(
                image1, image2, image1_backend=backend1, image2_backend=backend2
            )


if __name__ == "__main__":
    unittest.main()
