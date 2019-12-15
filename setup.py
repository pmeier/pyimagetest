from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ("numpy",)

testing_requires = ("imageio", "pillow", "torchvision")

classifiers = (
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development :: Testing :: Unit",
)

setup(
    name="pyimagetest",
    description="Utilities for unit testing with images.",
    version="0.1",
    url="https://github.com/pmeier/pyimagetest",
    license="GPLv3",
    author="Philip Meier",
    author_email="github.pmeier@posteo.de",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("test",)),
    install_requires=install_requires,
    extras_require={"testing": testing_requires},
    python_requires=">=3.6",
    classifiers=classifiers,
)
