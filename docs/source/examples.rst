Usage examples
==============

The following examples showcase the functionality of ``pyimagetest``. This requires some
backends to be installed. You can either install them for each example individually
or simply :ref:`install all builtin backends <install_builtin_image_backends>`.

General usage
-------------

- Requirements: ``pip install imageio Pillow``

:class:`~pyimagetest.image_test_case.ImageTestCase` provides two convenience methods
to ease unit testing with images:

  1. :meth:`~pyimagetest.image_test_case.ImageTestCase.load_image` loads and image from
     a ``file`` with a given ``backend``.
  2. :meth:`~pyimagetest.image_test_case.ImageTestCase.assertImagesAlmostEqual`
     compares two images of possible different backends on equality.

A simple I/O test that compares ``imageio`` and ``Pillow`` could look like this::

  import pyimagetest
  from os import path

  class ImageTester(pyimagetest.ImageTestCase):
      def test_io(self):
          file = path.join("path", "to", "test", "image")

          imageio_image = self.load_image(file, backend="imageio")
          pil_image = self.load_image(file, backend="PIL")

          self.assertImagesAlmostEqual(imageio_image, pil_image)


Working with a single backend and / or file
-------------------------------------------

- Requirements: ``pip install imageio``

If you mainly work with a single image backend and / or a file, you can ease up your
workflow by overwriting
:meth:`~pyimagetest.image_test_case.ImageTestCase.default_image_backend` and / or
:meth:`~pyimagetest.image_test_case.ImageTestCase.default_image_file`.
The return values are then used in
:meth:`~pyimagetest.image_test_case.ImageTestCase.load_image`
if no ``backend`` and / or ``file`` is given::

  import pyimagetest
  from os import path

  class ImageTester(pyimagetest.ImageTestCase):
      def default_image_backend(self):
          return "imageio"

      def default_image_file(self):
          return path.join("path", "to", "test", "image")

      def test_io(self):
          file = path.join("path", "to", "test", "image")
          backend = "imageio"

          specific_image = self.load_image(file, backend)
          default_image = self.load_image()

          self.assertImagesAlmostEqual(specific_image, default_image)


Creating a custom backend
-------------------------

- Requirements: ``pip install imageio``

If you want to work with an backend not included in ``pyimagetest`` you can create
your own by subclassing :class:`~pyimagetest.backends.backend.ImageBackend`::

  from pyimagetest.backends import ImageBackend
  import imageio


  class MyImage:
      @staticmethod
      def from_numpy(data):
          ...

      def to_numpy(self):
          ...


  class MyBackend(ImageBackend):
      def native_image_type(self):
          return MyImage

      def import_image(self, file):
          return MyImage.from_numpy(imageio.imread(file))

      def export_image(self, image):
          return image.to_numpy()

To able to access ``MyBackend`` at runtime you can add it within the constructor of
the test case::

  import pyimagetest
  from os import path


  class ImageTester(pyimagetest.ImageTestCase):
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.add_image_backend("MyBackend", MyBackend())

      def test_my_backend(self):
          file = path.join("path", "to", "test", "image")

          my_image = self.load_image(file, backend="MyBackend")

.. note::
  If you add a custom backend with the same :meth:`~pyimagetest.backends.backend
  .native_image_type` as a builtin backend, you can remove the builtin one with
  :meth:`~pyimagetest.image_test_case.ImageTestCase.remove_image_backend`. Otherwise
  the automatic backend inference of
  :meth:`~pyimagetest.image_test_case.ImageTestCase.assertImagesAlmostEqual` might not
  work as intended.

.. note::
  If you create a custom backend based on an open-source Python package, consider
  contributing it to ``pyimagetest``.
