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

try:
    import torch
    import torchvision

    torchvisionImageType = torch.FloatTensor
except ImportError:
    torchvisionImageType = None


ImageType = Union[imageioImageType, PILImageType, torchvisionImageType]

__all__ = ["ImageBackend", "builtin_image_backends"]


class ImageBackend(ABC):
    """ABC for ImageBackends. Each subclass has to implement the native ImageType and
    basic I/O methods.
    """

    @property
    @abstractmethod
    def native_image_type(self) -> Type[ImageType]:
        """Returns the native ImageType of the backend. This is used to infer the
        specific `ImageBackend` for a given `ImageType`

        Returns:
            Type[ImageType]
        """
        pass

    def __contains__(self, image) -> bool:
        return isinstance(image, self.native_image_type)

    @abstractmethod
    def import_image(self, file: str) -> ImageType:
        """Imports an image into the specific image type of the backend.

        Args:
            file (str): Path to the file that should be imported.

        Returns:
            ImageType
        """
        pass

    @abstractmethod
    def export_image(self, image: ImageType) -> np.ndarray:
        """Exports an image of the specific image type of the backend into a
        numpy.ndarray. The array should be of size height x width x channels (HxWxC) and
        be of type np.float32.

        Args:
            image (ImageType): Image object

        Returns:
            np.ndarray
        """
        pass


class ImageioBackend(ImageBackend):
    """
    `ImageBackend for the `imageio <https://imageio.github.io/>`_ package.
    """

    @property
    def native_image_type(self) -> Type[imageioImageType]:
        return imageioImageType

    def import_image(self, file: str) -> imageioImageType:
        return imageio.imread(file)

    def export_image(self, image: imageioImageType) -> np.ndarray:
        return image.astype(np.float32) / 255.0


class PILBackend(ImageBackend):
    """
    `ImageBackend for the `PIL (Pillow) <https://python-pillow.org/`_ package.
    """

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


class TorchvisionBackend(ImageBackend):
    """
    `ImageBackend for the `torchvision <https://pytorch.org/`_ package.
    """

    @property
    def native_image_type(self) -> Type[torchvisionImageType]:
        return torchvisionImageType

    def import_image(self, file: str) -> torchvisionImageType:
        pil_image = Image.open(file)
        return torchvision.transforms.functional.to_tensor(pil_image)

    def export_image(self, image: torchvisionImageType) -> np.ndarray:
        return image.detach().cpu().permute((1, 2, 0)).numpy()


BUILTIN_IMAGE_BACKENDS = OrderedDict(
    [
        ("imageio", ImageioBackend() if imageioImageType is not None else None),
        ("PIL", PILBackend() if PILImageType is not None else None),
        (
            "torchvision",
            TorchvisionBackend() if torchvisionImageType is not None else None,
        ),
    ]
)


def builtin_image_backends():
    """Returns all builtin image backends, which are available.

    Returns:
        OrderedDict[str, Backend]
    """
    return OrderedDict(
        [
            (name, backend)
            for name, backend in BUILTIN_IMAGE_BACKENDS.items()
            if backend is not None
        ]
    )
