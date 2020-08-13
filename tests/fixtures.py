import pytest

from . import assets


@pytest.fixture(scope="session")
def test_image_file():
    return assets.get_test_image_file()
