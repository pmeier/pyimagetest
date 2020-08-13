try:
    from ._version import version as __version__  # type: ignore[import]
except ImportError:
    __version__ = "UNKNOWN"

from .image_test_case import *
from .backends import *
