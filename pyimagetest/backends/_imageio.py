from typing import Type, cast

import imageio
import numpy as np

from . import ImageBackend

__all__ = ["ImageioBackend"]


class ImageioBackend(ImageBackend):
    r"""Backend for `imageio <https://imageio.github.io/>`_ ."""

    @property
    def native_image_type(self) -> Type[np.ndarray]:
        return np.ndarray

    def import_image(self, file: str) -> np.ndarray:
        return imageio.imread(file)

    def export_image(self, image: np.ndarray) -> np.ndarray:
        return cast(np.ndarray, image.astype(np.float32) / 255.0)
