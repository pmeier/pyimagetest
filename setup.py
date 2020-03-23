from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "pyimagetest", "__about__.py"), "r") as fh:
    exec(fh.read(), about)

with open(path.join(here, "README.md"), "r") as fh:
    long_description = fh.read()

install_requires = ("numpy",)

builtin_backends_requires = (
    "imageio",
    "pillow",
    "torchvision",
)

type_check_requires = (
    "mypy",
    # TODO: move to a released version if available
    # FIXME: fix this for PyPI upload
    # "numpy-stubs@https://github.com/numpy/numpy-stubs/archive/f3c6315738489983f5f37e1477ac68373d71b470.zip",
)

test_requires = ("pytest",)

doc_requires = (
    "sphinx",
    "sphinx_autodoc_typehints",
    "sphinx_rtd_theme",
)

dev_requires = (
    *builtin_backends_requires,
    *type_check_requires,
    *test_requires,
    *doc_requires,
)

extras_require = {
    "builtin_backends": builtin_backends_requires,
    "type_check": type_check_requires,
    "test": test_requires,
    "doc": doc_requires,
    "dev": dev_requires,
}

classifiers = (
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: BSD License",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Testing :: Unit",
)

setup(
    name=about["__name__"],
    description=about["__description__"],
    version=about["__version__"],
    url=about["__url__"],
    license=about["__license__"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where=here, exclude=("third_party_stubs", "test", "docs")),
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.6",
    classifiers=classifiers,
)
