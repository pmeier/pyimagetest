from abc import ABC, abstractmethod
from collections import OrderedDict
from importlib import import_module
from typing import Any, Dict, Type

import numpy as np

__all__ = ["ImageBackend", "builtin_image_backends"]


class ImageBackend(ABC):
    r"""ABC for image backends. Each subclass has to implement the
    :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type` as
    well as the basic I/O methods
    :meth:`~pyimagetest.backends.backend.ImageBackend.import_image`
    and :meth:`~pyimagetest.backends.backend.ImageBackend.export_image`.
    """

    @property
    @abstractmethod
    def native_image_type(self) -> Type[Any]:
        r"""Native image type of the backend. This is used to infer the
        :class:`~pyimagetest.backends.backend.ImageBackend` from a given image.
        """
        pass

    def __contains__(self, image: Any) -> bool:
        r"""Checks if the given ``image`` is native for the
        :class:`~pyimagetest.backends.backend.ImageBackend`

        Args:
            image: Image to be checked
        """
        return isinstance(image, self.native_image_type)

    @abstractmethod
    def import_image(self, file: str) -> Any:
        r"""Imports an image form ``file`` into the
        :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type` of
        the backend.

        Args:
            file: Path to the file that should be imported.
        """
        pass

    @abstractmethod
    def export_image(self, image: Any) -> np.ndarray:
        r"""Exports an image of the
        :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type`
        into a
        `numpy.ndarray <https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html>`_
        The output is of ``shape == (height, width, channels)`` and of
        ``dtype == numpy.float32``.

        Args:
            image: Image to be exported.
        """
        pass


class BackendMeta:
    def __init__(
        self, name: str,
    ):
        self.name = name
        self.module = f"_{name.lower()}"
        self.class_name = f"{name[0].upper()}{name[1:]}Backend"


BUILTIN_IMAGE_BACKENDS_META = (
    BackendMeta("imageio"),
    BackendMeta("PIL"),
    BackendMeta("torchvision"),
)


def builtin_image_backends() -> Dict[str, ImageBackend]:
    r"""Returns all available builtin image backends.
    """
    available_backends = OrderedDict()
    for meta in BUILTIN_IMAGE_BACKENDS_META:
        try:
            exec(f"import {meta.name}")
        except ImportError:
            pass
        else:
            backend_class = getattr(
                import_module(f"pyimagetest.backends.{meta.module}"), meta.class_name
            )
            available_backends[meta.name] = backend_class()

    return available_backends
