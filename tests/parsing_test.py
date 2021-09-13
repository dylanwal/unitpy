

import pytest

from src.unitpy.unit import Unit


def test_prefix():
    x = Unit("ml")
    assert x._unit == "ml"
