from abc import ABC, abstractmethod
from typing import Any, Union, Optional
from collections import OrderedDict
import numpy as np
from .backend import ImageBackend, builtin_image_backends

__all__ = ["ImageTestcase"]


class ImageTestcase(ABC):
    """Utility class for unit testing with images. This class is meant for double
    inheritance together with unittest.Testcase.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backends = OrderedDict()
        self._add_builtin_image_backends()

    def add_image_backend(self, name: str, backend: ImageBackend) -> None:
        """Adds custom image backend to the list of available backends.

        Args:
            name (str): Name of the backend
            backend (ImageBackend): Backend
        """
        self.backends[name] = backend

    def _add_builtin_image_backends(self) -> None:
        self.backends.update(builtin_image_backends())

    @property
    @abstractmethod
    def default_test_image_file(self) -> str:
        """Returns the path to the default test image file
        Returns:
            str
        """
        pass

    def load_image(
        self, backend: Union[ImageBackend, str], file: Optional[str] = None
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
        if isinstance(backend, str):
            backend = self.backends[backend]
        if file is None:
            file = self.default_test_image_file
        return backend.import_image(file)

    def assertImagesAlmostEqual(
        self,
        image1: Any,
        image2: Any,
        mean_abs_tolerance: float = 1e-2,
        image1_backend: Optional[ImageBackend] = None,
        image2_backend: Optional[ImageBackend] = None,
    ):
        """This test verifies that the two images are almost equal.

        Args:
            image1 (Any): Image 1
            image2 (Any): Image 2
            mean_abs_tolerance: Acceptable mean absolute tolerance (MAE)
            image1_backend (Union[ImageBackend, str]): Backend or backend name for
                image 1. If None, the backend is inferred automatically from the image.
            image2_backend (Union[ImageBackend, str]): Backend or backend name for
                image 2. If None, the backend is inferred automatically from the image.
        """
        if isinstance(image1_backend, str):
            image1_backend = self.backends[image1_backend]
        elif image1_backend is None:
            image1_backend = self.infer_image_backend(image1)

        if isinstance(image2_backend, str):
            image2_backend = self.backends[image2_backend]
        elif image2_backend is None:
            image2_backend = self.infer_image_backend(image2)

        image1 = image1_backend.export_image(image1)
        image2 = image2_backend.export_image(image2)

        actual = np.mean(np.abs(image1 - image2))
        desired = 0.0
        np.testing.assert_allclose(actual, desired, atol=mean_abs_tolerance, rtol=0.0)

    def infer_image_backend(self, image: Any) -> str:
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
