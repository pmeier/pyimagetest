from typing import Any, Union, Optional
from collections import OrderedDict
import unittest
import numpy as np
from .backends import ImageBackend, builtin_image_backends

__all__ = ["ImageTestcase"]


class ImageTestcase(unittest.TestCase):
    """Utility class for unit testing with images. This class is meant for double
    inheritance together with unittest.Testcase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backends = OrderedDict(())
        for name, backend in builtin_image_backends().items():
            self.add_image_backend(name, backend)

    def add_image_backend(
        self, name: str, backend: ImageBackend, allow_duplicate_type: bool = False
    ) -> None:
        """Adds custom image backend to the list of available backends.

        Args:
            name (str): Name of the backend
            backend (ImageBackend): Backend
        """
        native_image_types = [
            backend.native_image_type for backend in self.backends.values()
        ]
        if not allow_duplicate_type and backend.native_image_type in native_image_types:
            raise RuntimeError
        self.backends[name] = backend

    def remove_image_backend(self, name: str) -> None:
        """Removes an image backend from the known backends

        Args:
            name(str): Name of the backend
        """
        del self.backends[name]

    def default_image_backend(self) -> Optional[Union[ImageBackend, str]]:
        return None

    @property
    def has_default_image_backend(self) -> bool:
        return self.default_image_backend() is not None

    def default_image_file(self) -> Optional[str]:
        """Returns the path to the default test image file
        Returns:
            str
        """
        return None

    @property
    def has_default_image_file(self) -> bool:
        return self.default_image_file() is not None

    def load_image(
        self, backend: Optional[Union[ImageBackend, str]], file: Optional[str] = None
    ) -> Any:
        """Loads an image with the given image backend. If no file is given, the
        default test image is loaded.

        Args:
            backend (Union[ImageBackend, str]): Backend or backend name
            file (Optional[str]): Path to image file. If None is given, the default
            test image is used.

        Returns:
            Any
        """

        def parse_backend(backend: Optional[Union[ImageBackend, str]]) -> ImageBackend:
            if isinstance(backend, ImageBackend):
                return backend
            elif backend is None:
                default_backend = self.default_image_backend()
                if default_backend is None:
                    raise RuntimeError
                backend = default_backend

            if isinstance(backend, str):
                return self.backends[backend]
            else:
                raise TypeError

        def parse_file(file: Optional[str]) -> str:
            if isinstance(file, str):
                return file
            elif file is None:
                default_file = self.default_image_file()
                if default_file is None:
                    raise RuntimeError
                return default_file
            else:
                raise TypeError

        backend = parse_backend(backend)
        file = parse_file(file)
        return backend.import_image(file)

    def assertImagesAlmostEqual(
        self,
        image1: Any,
        image2: Any,
        mean_abs_tolerance: float = 1e-2,
        backend1: Optional[Union[ImageBackend, str]] = None,
        backend2: Optional[Union[ImageBackend, str]] = None,
    ):
        """This test verifies that the two images are almost equal.

        Args:
            image1 (Any): Image 1
            image2 (Any): Image 2
            mean_abs_tolerance: Acceptable mean absolute tolerance (MAE)
            backend1 (Union[ImageBackend, str]): Backend or backend name for
                image 1. If None, the backend is inferred automatically from the image.
            backend2 (Union[ImageBackend, str]): Backend or backend name for
                image 2. If None, the backend is inferred automatically from the image.
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
        np.testing.assert_allclose(actual, desired, atol=mean_abs_tolerance, rtol=0.0)

    def infer_image_backend(self, image: Any) -> ImageBackend:
        """Infers the corresponding backend from the image.

        Args:
            image: Image with type of any known backend

        Returns:
            ImageBackend
        """
        for backend in self.backends.values():
            if image in backend:
                return backend
        raise RuntimeError
