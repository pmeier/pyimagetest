from abc import ABC, abstractmethod
from typing import Any, Optional
from collections import OrderedDict
import numpy as np
from .backend import ImageBackend, builtin_image_backends

__all__ = ["ImageTester"]


class ImageTester(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backends = OrderedDict()
        self._add_builtin_image_backends()

    def add_image_backend(self, name: str, backend: ImageBackend) -> None:
        self.backends[name] = backend

    def _add_builtin_image_backends(self) -> None:
        self.backends.update(builtin_image_backends())

    @property
    @abstractmethod
    def default_test_image_file(self) -> str:
        pass

    def load_image(self, backend: ImageBackend, file: Optional[str] = None) -> Any:
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
        if image1_backend is None:
            image1_backend = self.infer_image_backend(image1)
        if image2_backend is None:
            image2_backend = self.infer_image_backend(image2)

        image1 = image1_backend.export_image(image1)
        image2 = image2_backend.export_image(image2)

        actual = np.mean(np.abs(image1 - image2))
        desired = 0.0
        np.testing.assert_allclose(actual, desired, atol=mean_abs_tolerance, rtol=0.0)

    def infer_image_backend(self, image: Any) -> str:
        for name, backend in self.backends.items():
            if image in backend:
                return name
        raise RuntimeError
