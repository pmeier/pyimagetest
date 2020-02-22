from abc import ABC, abstractmethod
from typing import Any, Type
from collections import OrderedDict
import numpy as np

try:
    import imageio
except ImportError:
    pass

try:
    from PIL import Image
except ImportError:
    pass

try:
    import torch
except ImportError:
    pass


__all__ = ["ImageBackend", "builtin_image_backends"]


class ImageBackend(ABC):
    """ABC for ImageBackends. Each subclass has to implement the native ImageType and
    basic I/O methods.
    """

    @property
    @abstractmethod
    def native_image_type(self) -> Type[Any]:
        """Returns the native ImageType of the backend. This is used to infer the
        specific `ImageBackend` for a given `ImageType`

        Returns:
            Type[ImageType]
        """
        pass

    def __contains__(self, image) -> bool:
        return isinstance(image, self.native_image_type)

    @abstractmethod
    def import_image(self, file: str) -> Any:
        """Imports an image into the specific image type of the backend.

        Args:
            file (str): Path to the file that should be imported.

        Returns:
            ImageType
        """
        pass

    @abstractmethod
    def export_image(self, image: Any) -> np.ndarray:
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

    def __init__(self):
        import imageio

        self._imageio = imageio

    @property
    def native_image_type(self) -> Type[np.ndarray]:
        return np.ndarray

    def import_image(self, file: str) -> np.ndarray:
        return self._imageio.imread(file)

    def export_image(self, image: np.ndarray) -> np.ndarray:
        return image.astype(np.float32) / 255.0


class PILBackend(ImageBackend):
    """
    `ImageBackend for the `PIL (Pillow) <https://python-pillow.org/`_ package.
    """

    def __init__(self):
        from PIL import Image

        self._Image = Image

    @property
    def native_image_type(self) -> Type[Image.Image]:
        return self._Image.Image

    def import_image(self, file: str) -> Image.Image:
        return self._Image.open(file)

    def export_image(self, image: Image.Image) -> np.ndarray:
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

    def __init__(self):
        from torchvision.transforms import functional as F

        self._F = F

    @property
    def native_image_type(self) -> Type[torch.Tensor]:
        return torch.Tensor

    def import_image(self, file: str) -> torch.Tensor:
        pil_image = Image.open(file)
        return self._F.to_tensor(pil_image)

    def export_image(self, image: torch.Tensor) -> np.ndarray:
        return image.detach().cpu().permute((1, 2, 0)).numpy()


BUILTIN_IMAGE_BACKENDS = (
    ("imageio", ImageioBackend),
    ("PIL", PILBackend),
    ("torchvision", TorchvisionBackend),
)


def builtin_image_backends():
    """Returns all builtin image backends, which are available.

    Returns:
        OrderedDict[str, Backend]
    """
    backends = OrderedDict(())
    for name, backend_class in BUILTIN_IMAGE_BACKENDS:
        try:
            backends[name] = backend_class()
        except ImportError:
            pass

    return backends
