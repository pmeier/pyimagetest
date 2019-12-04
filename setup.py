from setuptools import setup, find_packages

requirements = ("numpy",)

setup(
    name="pyimagetest",
    version="0.1",
    author="Philip Meier",
    author_email="github.pmeier@posteo.de",
    url="https://github.com/pmeier/pyimagetest",
    description="ADDME",
    license="BSD-3",
    packages=find_packages(exclude=("test",)),
    install_requires=requirements,
)
