import unittest
from os import path
from itertools import combinations
from pyimagetest import ImageTestcase
from pyimagetest.backend import BUILTIN_IMAGE_BACKENDS


class Tester(ImageTestcase, unittest.TestCase):
    def default_image_file(self) -> str:
        # The test image was downloaded from
        # http://www.r0k.us/graphics/kodak/kodim15.html
        # and is cleared for unrestricted usage
        return path.join(path.dirname(__file__), "test_image.png")

    def test_backend_availability(self) -> None:
        not_available_backends = [
            name for name, backend in BUILTIN_IMAGE_BACKENDS.items() if backend is None
        ]
        if not_available_backends:
            msg = "The following backends are not available for testing: {}"
            raise RuntimeError(msg.format(", ".join(not_available_backends)))

    def test_io(self) -> None:
        for backend1, backend2 in combinations(self.backends.values(), 2):
            image1 = self.load_image(backend1)
            image2 = self.load_image(backend2)
            self.assertImagesAlmostEqual(
                image1, image2, image1_backend=backend1, image2_backend=backend2
            )


if __name__ == "__main__":
    unittest.main()
