from typing import Type
import numpy as np
import torch
from PIL import Image
from torchvision.transforms import functional as F
from .backend import ImageBackend

__all__ = ["torchvisionBackend"]


class torchvisionBackend(ImageBackend):
    """
    `ImageBackend for the `torchvision <https://pytorch.org/`_ package.
    """

    @property
    def native_image_type(self) -> Type[torch.Tensor]:
        return torch.Tensor

    def import_image(self, file: str) -> torch.Tensor:
        pil_image = Image.open(file)
        return F.to_tensor(pil_image)

    def export_image(self, image: torch.Tensor) -> np.ndarray:
        return image.detach().cpu().permute((1, 2, 0)).numpy()
