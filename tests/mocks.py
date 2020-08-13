import builtins
import sys
import unittest.mock

__all__ = [
    "make_mock_target",
    "attach_method_mock",
    "attach_property_mock",
    "patch_imports",
]

DEFAULT_MOCKER = unittest.mock


def make_mock_target(*args, pkg="pyimagetest"):
    return ".".join((pkg, *args))


def attach_method_mock(mock, method, mocker=DEFAULT_MOCKER, **attrs):
    if "name" not in attrs:
        attrs["name"] = f"{mock.name}.{method}()"

    method_mock = mocker.Mock(**attrs)
    mock.attach_mock(method_mock, method)


def attach_property_mock(mock, property, mocker=DEFAULT_MOCKER, **attrs):
    if "name" not in attrs:
        attrs["name"] = f"{mock.name}.{property}"

    setattr(type(mock), property, mocker.PropertyMock(**attrs))


def patch_imports(
    names,
    clear=True,
    retain_condition=None,
    import_error_condition=None,
    mocker=DEFAULT_MOCKER,
):
    if retain_condition is None:

        def retain_condition(name):
            return not any(name.startswith(name_) for name_ in names)

    if import_error_condition is None:

        def import_error_condition(name, globals, locals, fromlist, level):
            direct = name in names
            indirect = fromlist is not None and any(
                from_ in names for from_ in fromlist
            )
            return direct or indirect

    __import__ = builtins.__import__

    def patched_import(name, globals=None, locals=None, fromlist=(), level=0):
        if import_error_condition(name, globals, locals, fromlist, level):
            raise ImportError

        return __import__(name, globals, locals, fromlist, level)

    mocker.patch.object(builtins, "__import__", new=patched_import)
    if clear:
        values = {
            name: module
            for name, module in sys.modules.items()
            if retain_condition(name)
        }
    else:
        values = {}
    mocker.patch.dict(
        sys.modules, clear=clear, values=values,
    )
