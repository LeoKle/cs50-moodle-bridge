from add import add

from ._marker import pytestmark  # noqa: F401


def test_add():
    assert add(1, 2) == 3
