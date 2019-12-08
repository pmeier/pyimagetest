from abc import ABC, abstractmethod
from typing import Type, Union
from collections import OrderedDict
import numpy as np

try:
    import imageio

    imageioImageType = np.ndarray
except ImportError:
    imageio = None
    imageioImageType = None

try:
    from PIL import Image

    PILImageType = Image.Image
except ImportError:
    Image = None
    PILImageType = None

ImageType = Union[imageioImageType, PILImageType]

__all__ = ["ImageBackend", "ImageioBackend", "PILBackend", "builtin_image_backends"]


class ImageBackend(ABC):
    @property
    @abstractmethod
    def native_image_type(self) -> Type[ImageType]:
        pass

    def __contains__(self, image) -> bool:
        return isinstance(image, self.native_image_type)

    @abstractmethod
    def import_image(self, file: str) -> ImageType:
        pass

    @abstractmethod
    def export_image(self, image: ImageType) -> np.ndarray:
        pass


class ImageioBackend(ImageBackend):
    @property
    def native_image_type(self) -> Type[imageioImageType]:
        return imageioImageType

    def import_image(self, file: str) -> imageioImageType:
        return imageio.imread(file)

    def export_image(self, image: imageioImageType) -> np.ndarray:
        return image.astype(np.float32) / 255.0


class PILBackend(ImageBackend):
    @property
    def native_image_type(self) -> Type[PILImageType]:
        return PILImageType

    def import_image(self, file: str) -> PILImageType:
        return Image.open(file)

    def export_image(self, image: PILImageType) -> np.ndarray:
        mode = image.mode
        image = np.asarray(image, dtype=np.float32)
        if mode in ("L", "RGB"):
            image /= 255.0
        if mode in ("1", "L"):
            image = np.expand_dims(image, 2)
        return image


BUILTIN_IMAGE_BACKENDS = OrderedDict(
    [
        ("imageio", ImageioBackend() if imageioImageType is not None else None),
        ("PIL", PILBackend() if PILImageType is not None else None),
    ]
)


def builtin_image_backends():
    return OrderedDict(
        [
            (name, backend)
            for name, backend in BUILTIN_IMAGE_BACKENDS.items()
            if backend is not None
        ]
    )
