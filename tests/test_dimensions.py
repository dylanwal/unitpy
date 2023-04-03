
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


def test_as_dict():
    dict_ = {"mass": 1, "length": 2, "time": -1, "amount_of_substance": 0, "luminous_intensity": 0,
             "electric_current": 0, "temperature": 0}
    result = dim_.Dimension(**dict_)
    result = result.as_dict()
    for k, v in result.items():
        assert v == dict_[k.label]


def test_as_dict_str():
    dict_ = {"mass": 1, "length": 3, "time": -2, "amount_of_substance": 0, "luminous_intensity": 1,
             "electric_current": 0, "temperature": 1}
    result = dim_.Dimension(**dict_)
    result = result.as_dict(True)
    for k, v in dict_.items():
        assert v == result[k]

