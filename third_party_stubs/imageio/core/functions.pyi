from typing import Any, Union, Optional
import pathlib
from io import FileIO
import numpy as np

def imread(
    uri: Union[str, pathlib.Path, bytes, FileIO],
    format: Optional[str] = ...,
    **kwargs: Any
) -> np.ndarray: ...
