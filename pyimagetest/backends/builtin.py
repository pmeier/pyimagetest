from typing import Union, Optional, Collection
from importlib import import_module
from collections import OrderedDict


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


def builtin_image_backends():
    """Returns all builtin image backends, which are available.

    Returns:
        OrderedDict[str, Backend]
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
