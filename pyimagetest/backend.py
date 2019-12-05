from abc import ABC, abstractmethod
from typing import Type, Union
from collections import OrderedDict
import numpy as np

try:
    import imageio

    IMAGEIO_AVAILABLE = True
except ImportError:
    imageio = None
    IMAGEIO_AVAILABLE = False

try:
    from PIL import Image, ImageFile as _ImageFile

    PILImageFile = _ImageFile.ImageFile
    PIL_AVAILABLE = True
except ImportError:
    PILImageFile = None
    PIL_AVAILABLE = False

ImageType = Union[np.ndarray, PILImageFile]

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
    def native_image_type(self) -> Type[np.ndarray]:
        return np.ndarray

    def import_image(self, file: str) -> np.ndarray:
        return imageio.imread(file)

    def export_image(self, image: np.ndarray) -> np.ndarray:
        return image.astype(np.float32) / 255.0


class PILBackend(ImageBackend):
    @property
    def native_image_type(self) -> Type[PILImageFile]:
        return PILImageFile

    def import_image(self, file: str) -> PILImageFile:
        return Image.open(file)

    def export_image(self, image: PILImageFile) -> np.ndarray:
        mode = image.mode
        image = np.asarray(image, dtype=np.float32)
        if mode in ("L", "RGB"):
            image /= 255.0
        if mode in ("1", "L"):
            image = np.expand_dims(image, 2)
        return image


BUILTIN_IMAGE_BACKENDS = OrderedDict(
    [
        ("imageio", ImageioBackend() if IMAGEIO_AVAILABLE else None),
        ("PIL", PILBackend() if PIL_AVAILABLE else None),
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
