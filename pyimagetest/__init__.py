from typing import Any, Optional, Union

import numpy as np

from .backends import *

try:
    from ._version import version as __version__  # type: ignore[import]
except ImportError:
    __version__ = "UNKNOWN"


image_backends = builtin_image_backends()

try:
    import pytest

    _PYTEST_AVAILABLE = True
except ImportError:
    _PYTEST_AVAILABLE = False


if _PYTEST_AVAILABLE:
    _internal_error_cls = pytest.UsageError
else:
    _internal_error_cls = RuntimeError


def add_image_backend(
    name: str, backend: ImageBackend, allow_duplicate_type: bool = False
) -> None:
    """Adds custom backend to the available backends.

    Args:
        name: Name of the backend
        backend: Backend
        allow_duplicate_type: If ``True``, no check for duplicate
         :attr:`~pyimagetest.ImageBackend.native_image_type` s is performed. Defaults
         to ``False``.

    Raises:
        RuntimeError: If another :class:`~pyimagetest.ImageBackend` with the same
            :attr:`~pyimagetest.ImageBackend.native_image_type` already present and
            ``allow_duplicate_type`` is ``False``.

    .. note::
        If you add an :class:`~pyimagetest.ImageBackend` with a duplicate
        :attr:`~pyimagetest.ImageBackend.native_image_type`, the automatic backend
        inference with :func:`infer_image_backend` might not work correctly.
    """
    native_image_types = [
        backend.native_image_type for backend in image_backends.values()
    ]
    if not allow_duplicate_type and backend.native_image_type in native_image_types:
        msg = (
            f"Another backend with native_image_type {backend.native_image_type} "
            f"is already present."
        )
        raise _internal_error_cls(msg)
    image_backends[name] = backend


def remove_image_backend(name: str) -> None:
    """Removes a backend from the known backends.

    Args:
        name: Name of the backend to be removed
    """
    del image_backends[name]


def infer_image_backend(image: Any) -> ImageBackend:
    """Infers the corresponding backend from the ``image``.

    Args:
        image: Image with type of any known backend

    Raises:
        RuntimeError: If type of image does not correspond to any known
            image backend
    """
    for backend in image_backends.values():
        if image in backend:
            return backend
    else:
        msg = f"No backend with native_image_type {type(image)} is known."
        raise _internal_error_cls(msg)


def assert_images_almost_equal(
    image1: Any,
    image2: Any,
    mae: float = 1e-2,
    backend1: Optional[Union[ImageBackend, str]] = None,
    backend2: Optional[Union[ImageBackend, str]] = None,
) -> None:
    """Image equality assertion.

    Args:
        image1: Image 1
        image2: Image 2
        mae: Maximum acceptable `mean absolute error (MAE)
            <https://en.wikipedia.org/wiki/Mean_absolute_error>`_. Defaults to ``1e-2``.
        backend1:
            :class:`~pyimagetest.ImageBackend` or its name for ``image1``. If omitted,
            the backend is inferred from ``image1`` with :func:`~infer_image_backend`.
        backend2:
            :class:`~pyimagetest.ImageBackend` or its name for ``image2``. If omitted,
            the backend is inferred from ``imag2`` with :func:`~infer_image_backend`.

    Raises:
        AssertionError: If `image1` and `image2` are not equal up to the
            acceptable MAE.
    """

    def parse_backend(
        backend: Optional[Union[ImageBackend, str]], image: Any
    ) -> ImageBackend:
        if isinstance(backend, ImageBackend):
            return backend
        elif isinstance(backend, str):
            return image_backends[backend]
        elif backend is None:
            return infer_image_backend(image)
        else:
            raise _internal_error_cls

    backend1 = parse_backend(backend1, image1)
    backend2 = parse_backend(backend2, image2)

    image1 = backend1.export_image(image1)
    image2 = backend2.export_image(image2)

    actual = np.mean(np.abs(image1 - image2))  # item?

    if _PYTEST_AVAILABLE:
        assert actual == pytest.approx(0.0, abs=mae)
    else:
        assert actual <= mae
