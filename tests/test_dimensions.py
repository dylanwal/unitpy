
import pytest

import unitpy
import unitpy.definitions.dimensions as dim_

cases = (
    ("meter", dim_.Dimension(length=1)),
    ("meter/second", dim_.Dimension(length=1, time=-1)),
    ("bar", dim_.Dimension(mass=1, length=-1, time=-2)),
    ("J", dim_.Dimension(mass=1, length=2, time=-2))

)


@pytest.mark.parametrize("case", cases)
def test_dimensions(case):
    text, answer = case
    result = unitpy.Unit(text)
    assert result.dimensionality == answer


def test_dimensionless():
    result = unitpy.Unit("m")
    assert result.dimensionless is False


def test_dimensionless_true():
    result = unitpy.Unit("m/m")
    assert result.dimensionless is True
