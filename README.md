# pyimagetest

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`pyimagetest` provides utilities for unit testing with images. 

`pyimagetest.ImageTestcase` is an `ABC` meant for double inheritance with `unittest.Testcase`. It adds the `assertImagesAlmostEqual` method. The compared image objects do not have to be from the same `pyimagetest.ImageBackend`. As long as the backend is known to `pyimagetest.ImageTestcase` it is inferred automatically.

Currently the following `ImageBackend`s are supported off-the-shelf:
- `imageio` 
- `PIL`

Custom backends can be added by subclassing `ImageBackend`.

## Example usage

```python
import unittest
import pyimagetest


class Tester(pyimagetest.ImageTestcase, unittest.TestCase):
    @property
    def default_test_image_file(self):
        return "path/to/default/test/image/file"
    
    def simple_test(self):
        imageio_image = self.load_image("imageio")
        pil_image = self.load_image("PIL")
        self.assertImagesAlmostEqual(imageio_image, pil_image)

if __name__ == "__main__":
    unittest.main()
```
