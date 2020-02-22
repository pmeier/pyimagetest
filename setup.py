from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, "pyimagetest", "__about__.py"), "r") as fh:
    exec(fh.read(), about)

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ("numpy",)

testing_requires = ("imageio", "pillow", "torchvision")

classifiers = (
    "Development Status :: 3 - Alpha",
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
    packages=find_packages(exclude=("test",)),
    install_requires=install_requires,
    extras_require={"testing": testing_requires},
    python_requires=">=3.6",
    classifiers=classifiers,
)
