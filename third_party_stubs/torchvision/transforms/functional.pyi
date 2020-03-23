from typing import Union
from PIL import Image
import numpy as np
import torch

def to_tensor(pic: Union[Image.Image, np.ndarray]) -> torch.Tensor: ...
