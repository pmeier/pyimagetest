from typing import Any, Union, Optional
from io import FileIO
import pathlib

class Image:
    mode: str
    def save(
        self,
        fp: Union[str, pathlib.Path, FileIO],
        format: Optional[str] = ...,
        **params: Any
    ) -> None: ...
    def show(self, title: Optional[str] = ..., command: Optional[str] = ...) -> None: ...

def open(fp: Union[str, pathlib.Path, FileIO]) -> Image: ...
