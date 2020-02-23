from abc import ABC, abstractmethod
from typing import Any, Type
import numpy as np

__all__ = ["ImageBackend"]


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
