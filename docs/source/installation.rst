Installation
============

``pyimagetest`` is a proper Python package and listed on
`PyPI <https://pypi.org/project/pyimagetest/>`_. To install the latest stable version
run

.. code-block:: sh

  pip install pyimagetest

To install the latest unreleased version from source run

.. code-block:: sh

  git clone https://github.com/pmeier/pyimagetest
  cd pyimagetest
  pip install .

.. _install_builtin_image_backends:

Installation with builtin backends
----------------------------------

Although ``pyimagetest`` has support for some
:ref:`image backends built in <builtin_image_backends>`,
by default none are installed. To install the requirements for all builtin backends,
run the pip command with the ``[builtin_backends]`` extra.

.. code-block:: sh

  pip install pyimagetest[builtin_backends]


Installation for developers
---------------------------

If you want to contribute to ``pyimagetest`` please install from source with the
``[dev]`` extra in order to install all required development tools.

.. code-block:: sh

  git clone https://github.com/pmeier/pyimagetest
  cd pyimagetest
  pip install .[dev]
