from typing import Any, Union, Optional
from collections import OrderedDict
import unittest
import numpy as np
from .backends import ImageBackend, builtin_image_backends

__all__ = ["ImageTestCase"]


class ImageTestCase(unittest.TestCase):
    """Testcase for unit testing with images.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backends = OrderedDict(())
        for name, backend in builtin_image_backends().items():
            self.add_image_backend(name, backend)

    def add_image_backend(
        self, name: str, backend: ImageBackend, allow_duplicate_type: bool = False
    ) -> None:
        """Adds custom :class:`~pyimagetest.backends.backend.ImageBackend` to
        the available backends.

        Args:
            name: Name of the backend
            backend: Backend
            allow_duplicate_type: If ``True``, no check for duplicate
             :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type` s
             is performed. Defaults to ``False``.

        Raises:
            RuntimeError: If another :class:`~pyimagetest.backends.backend.ImageBackend`
                with the same
                :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type`
                already present and ``allow_duplicate_type`` is ``False``.

        .. note::
            If you add an :class:`~pyimagetest.backends.backend.ImageBackend`
            with a duplicate
            :attr:`~pyimagetest.backends.backend.ImageBackend.native_image_type`,
            the automatic backend inference with
            :meth:`~pyimagetest.image_test_case.ImageTestCase.infer_image_backend`
            might not work correctly.
        """
        native_image_types = [
            backend.native_image_type for backend in self.backends.values()
        ]
        if not allow_duplicate_type and backend.native_image_type in native_image_types:
            msg = (
                f"Another backend with native_image_type {backend.native_image_type} "
                f"is already present."
            )
            raise RuntimeError(msg)
        self.backends[name] = backend

    def remove_image_backend(self, name: str) -> None:
        """Removes an :class:`~pyimagetest.backends.backend.ImageBackend` from
        the known backends.

        Args:
            name: Name of the backend to be removed
        """
        del self.backends[name]

    def infer_image_backend(self, image: Any) -> ImageBackend:
        """Infers the corresponding :class:`~pyimagetest.backends.backend.ImageBackend`
        from ``image``.

        Args:
            image: Image with type of any known backend

        Raises:
            RuntimeError: If type of image does not correspond to any known
                image backend
        """
        for backend in self.backends.values():
            if image in backend:
                return backend
        msg = f"No backend with native_image_type {type(image)} is known."
        raise RuntimeError(msg)

    def default_image_file(self) -> str:
        """If overwritten, should return the default image file.

        .. note::
            Override this if you mainly work with a single image. If you do,
            :meth:`~pyimagetest.image_test_case.ImageTestCase.load_image` will
            use the value returned by this method if the ``file`` parameter is
            omitted.

        Raises:
            RuntimeError: If not overridden
        """
        raise RuntimeError

    def default_image_backend(self) -> Union[ImageBackend, str]:
        """If overwritten, should return the default
        :class:`~pyimagetest.backends.backend.ImageBackend` or its name.

        .. note::
            Override this if you mainly work with a single backend. If you do,
            :meth:`~pyimagetest.image_test_case.ImageTestCase.load_image` will
            use the value returned by this method if the ``backend`` parameter
            is omitted.

        Raises:
            RuntimeError: If not overridden
        """
        raise RuntimeError

    def load_image(
        self,
        file: Optional[str] = None,
        backend: Optional[Union[ImageBackend, str]] = None,
    ) -> Any:
        """Loads the image from ``file`` with ``backend``. If no ``file`` or
        ``backend`` is given the default values from
        :meth:`~pyimagetest.image_test_case.ImageTestCase.default_image_file`
        and
        :meth:`~pyimagetest.image_test_case.ImageTestCase.default_image_backend`
        are used.

        Args:
            backend: Backend or backend name. If ``None``,
                :meth:`~pyimagetest.image_test_case.ImageTestCase.default_image_backend`
                is used. Defaults to ``None``.
            file: Path to image file. If ``None``,
                :meth:`~pyimagetest.image_test_case.ImageTestCase.default_image_file`
                is used. Defaults to ``None``.
        """

        def parse_file(file: Optional[str]) -> str:
            if isinstance(file, str):
                return file
            elif file is None:
                try:
                    return self.default_image_file()
                except RuntimeError:
                    msg = (
                        "Override ImageTestCase.default_image_file() to be able "
                        "to call ImageTestCase.load_image() without file parameter."
                    )
                    raise RuntimeError(msg)
            else:
                raise TypeError

        def parse_backend(backend: Optional[Union[ImageBackend, str]]) -> ImageBackend:
            if isinstance(backend, ImageBackend):
                return backend

            if backend is None:
                try:
                    backend = self.default_image_backend()
                except RuntimeError:
                    msg = (
                        "Override ImageTestCase.default_image_backend() to be able "
                        "to call ImageTestCase.load_image() without backend."
                        "parameter"
                    )
                    raise RuntimeError(msg)

            if isinstance(backend, str):
                return self.backends[backend]
            else:
                raise TypeError

        file = parse_file(file)
        backend = parse_backend(backend)
        return backend.import_image(file)

    def assertImagesAlmostEqual(
        self,
        image1: Any,
        image2: Any,
        tolerance: float = 1e-2,
        backend1: Optional[Union[ImageBackend, str]] = None,
        backend2: Optional[Union[ImageBackend, str]] = None,
    ):
        """Image equality assertion.

        Args:
            image1: Image 1
            image2: Image 2
            tolerance: Acceptable `mean absolute error (MAE)
                <https://en.wikipedia.org/wiki/Mean_absolute_error>`_. Defaults
                to ``1e-2``.
            backend1:
                :class:`~pyimagetest.backends.backend.ImageBackend` or its name
                for ``image1``. If ``None``, the backend is inferred from
                ``image1`` with
                :meth:`~pyimagetest.image_test_case.ImageTestCase.infer_image_backend`.
                Defaults to ``None``.
            backend2:
                :class:`~pyimagetest.backends.backend.ImageBackend` or its name
                for ``image2``. If ``None``, the backend is inferred from
                ``image2`` with
                :meth:`~pyimagetest.image_test_case.ImageTestCase.infer_image_backend`.
                Defaults to ``None``.

        Raises:
            AssertionError: If `image1` and `image2` are not equal up to the
                desired tolerance.
        """

        def parse_backend(
            backend: Optional[Union[ImageBackend, str]], image: Any
        ) -> ImageBackend:
            if isinstance(backend, ImageBackend):
                return backend
            elif isinstance(backend, str):
                return self.backends[backend]
            elif backend is None:
                return self.infer_image_backend(image)
            else:
                raise RuntimeError

        backend1 = parse_backend(backend1, image1)
        backend2 = parse_backend(backend2, image2)

        image1 = backend1.export_image(image1)
        image2 = backend2.export_image(image2)

        actual = np.mean(np.abs(image1 - image2))
        desired = 0.0
        np.testing.assert_allclose(actual, desired, atol=tolerance, rtol=0.0)
