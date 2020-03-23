from typing import Type
import numpy as np
from PIL import Image
from .backend import ImageBackend


class PILBackend(ImageBackend):
    """:class:`~pyimagetest.backends.backend.ImageBackend` for the
    `Pillow package <https://python-pillow.org/>`_ .
    """

    @property
    def native_image_type(self) -> Type[Image.Image]:
        return Image.Image

    def import_image(self, file: str) -> Image.Image:
        return Image.open(file)

    def export_image(self, image: Image.Image) -> np.ndarray:
        mode = image.mode
        image = np.asarray(image, dtype=np.float32)
        if mode in ("L", "RGB"):
            image /= 255.0
        if mode in ("1", "L"):
            image = np.expand_dims(image, 2)
        return image
