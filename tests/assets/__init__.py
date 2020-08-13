from os import path


def get_test_image_file():
    # The tests image was downloaded from http://www.r0k.us/graphics/kodak/kodim15.html
    # and is cleared for unrestricted usage
    return path.join(path.dirname(__file__), "test_image.png")
