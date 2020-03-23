from abc import ABC, abstractmethod
from typing import Any, Type
import numpy as np

__all__ = ["ImageBackend"]


class ImageBackend(ABC):
    """ABC for image backends. Each subclass has to implement the
    :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type` as
    well as the basic I/O methods
    :meth:`~pyimagetest.backends.backend.ImageBackend.import_image`
    and :meth:`~pyimagetest.backends.backend.ImageBackend.export_image`.
    """

    @property
    @abstractmethod
    def native_image_type(self) -> Type[Any]:
        """Native image type of the backend. This is used to infer the
        :class:`~pyimagetest.backends.backend.ImageBackend` from a given image.
        """
        pass

    def __contains__(self, image: Any) -> bool:
        """Checks if the given ``image`` is native for the
        :class:`~pyimagetest.backends.backend.ImageBackend`

        Args:
            image: Image to be checked
        """
        return isinstance(image, self.native_image_type)

    @abstractmethod
    def import_image(self, file: str) -> Any:
        """Imports an image form ``file`` into the
        :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type` of
        the backend.

        Args:
            file: Path to the file that should be imported.
        """
        pass

    @abstractmethod
    def export_image(self, image: Any) -> np.ndarray:
        """Exports an image of the
        :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type`
        into a
        `numpy.ndarray <https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html>`_
        The output is of ``shape == (height, width, channels)`` and of
        ``dtype == numpy.float32``.

        Args:
            image: Image to be exported.
        """
        pass
