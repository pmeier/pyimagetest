import itertools

import pyimagetest


def test_io(subtests, test_image_file):
    for backend1, backend2 in itertools.combinations(
        pyimagetest.image_backends.values(), 2
    ):
        with subtests.test(backend1=backend1, backend2=backend2):
            image1 = backend1.import_image(test_image_file)
            image2 = backend2.import_image(test_image_file)
            pyimagetest.assert_images_almost_equal(image1, image2)
