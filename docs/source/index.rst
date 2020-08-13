Welcome to pyimagetest's documentation!
=======================================

If you have ever worked with multiple image backends at the same time you know
that it can cumbersome to check images from different backends for equality.
``pyimagetest`` is a Python library that provides utilities for unit testing
with images. It provides :class:`~pyimagetest.image_test_case.ImageTestCase`
that enables convenient image loading and comparison.

.. _builtin_image_backends:

As of now the following image backends are builtin:

- `imageio <https://imageio.github.io/>`_
- `Pillow <https://python-pillow.org/>`_
- `torchvision <https://pytorch.org/docs/stable/torchvision/index.html>`_

``pyimagetest`` requires Python 3.6 or later and is based on
`numpy <https://numpy.org/>`_. The code lives on `GitHub <https://github
.com/pmeier/pyimagetest>`_ and is licensed under the `3-Clause BSD License
<https://opensource.org/licenses/BSD-3-Clause>`_.

.. toctree::
  :maxdepth: 2

  Getting Started <getting_started>
  Contributing <contributing>
  Reference <api>
