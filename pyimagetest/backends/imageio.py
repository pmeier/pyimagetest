from typing import Type
import numpy as np
import imageio
from .backend import ImageBackend

__all__ = ["imageioBackend"]


class imageioBackend(ImageBackend):
    """
    `ImageBackend for the `imageio <https://imageio.github.io/>`_ package.
    """

    @property
    def native_image_type(self) -> Type[np.ndarray]:
        return np.ndarray

    def import_image(self, file: str) -> np.ndarray:
        return imageio.imread(file)

    def export_image(self, image: np.ndarray) -> np.ndarray:
        return image.astype(np.float32) / 255.0
