from typing import Type
import numpy as np
import torch
from PIL import Image
from torchvision.transforms import functional as F
from .backend import ImageBackend

__all__ = ["torchvisionBackend"]


class torchvisionBackend(ImageBackend):
    """:class:`~pyimagetest.backends.backend.ImageBackend` for the
    `torchvision package <https://pytorch.org/docs/stable/torchvision/index.html>`_ .
    """

    @property
    def native_image_type(self) -> Type[torch.Tensor]:
        return torch.Tensor

    def import_image(self, file: str) -> torch.Tensor:
        return F.to_tensor(Image.open(file))

    def export_image(self, image: torch.Tensor) -> np.ndarray:
        return image.detach().cpu().permute((1, 2, 0)).numpy()
