from typing import Union, Optional, Collection, Dict
from importlib import import_module
from collections import OrderedDict
from .backend import ImageBackend


class BackendMeta:
    def __init__(
        self,
        requires: Union[Collection[str], str],
        module: str,
        name: Optional[str] = None,
        class_name: Optional[str] = None,
    ):
        if isinstance(requires, str):
            requires = (requires,)
        self.requires = requires

        self.module = module

        if name is None:
            name = module
        self.name = name

        if class_name is None:
            class_name = f"{name}Backend"
        self.class_name = class_name


BUILTIN_IMAGE_BACKENDS_META = (
    BackendMeta(requires="imageio", module="imageio"),
    BackendMeta(requires="PIL", module="Pillow", name="PIL"),
    BackendMeta(requires=("torch", "PIL", "torchvision"), module="torchvision"),
)


def builtin_image_backends() -> Dict[str, ImageBackend]:
    """Returns all available builtin image backends.

    ReturnType:
        OrderedDict[str, ImageBackend]
    """
    available_backends = OrderedDict(())
    for meta in BUILTIN_IMAGE_BACKENDS_META:
        try:
            for package in meta.requires:
                exec(f"import {package}")
        except ImportError:
            pass
        else:
            backend_class = getattr(
                import_module(f"pyimagetest.backends.{meta.module}"), meta.class_name
            )
            available_backends[meta.name] = backend_class()

    return available_backends
