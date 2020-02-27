from os import path
from itertools import combinations
from pyimagetest import ImageTestCase
from pyimagetest import builtin_image_backends
from pyimagetest.backends.builtin import BUILTIN_IMAGE_BACKENDS_META


class Tester(ImageTestCase):
    def default_image_file(self) -> str:
        # The test image was downloaded from
        # http://www.r0k.us/graphics/kodak/kodim15.html
        # and is cleared for unrestricted usage
        here = path.abspath(path.dirname(__file__))
        return path.join(here, "test_image.png")

    def test_backend_availability(self) -> None:
        backend_names = [meta.name for meta in BUILTIN_IMAGE_BACKENDS_META]
        available_backend_names = builtin_image_backends().keys()
        not_available_backend_names = set(backend_names) - set(available_backend_names)
        if not_available_backend_names:
            msg = "The following backends are not available for testing: {}"
            raise RuntimeError(msg.format(", ".join(not_available_backend_names)))

    def test_io(self) -> None:
        for backend1, backend2 in combinations(self.backends.values(), 2):
            image1 = self.load_image(backend=backend1)
            image2 = self.load_image(backend=backend2)
            self.assertImagesAlmostEqual(image1, image2)
