import math

import pytest

from unitpy import Q, U

cases = (
    # expression, answer_unit, answer_value(plus), answer_value(minus)
    (("1 ft", "1 in"), "in", 13, 11),
    (("1.1 cm**3", "1 ml"), "L", 0.0021, 0.0001),
    (("1 degC", "1 K"), "K", 275.15, 273.15),

)


@pytest.mark.parametrize("case", cases)
def test_math_add(case: tuple):
    text, unit, value, _ = case
    quantities = [Q(t) for t in text]
    sum_ = quantities[0]
    for quant in quantities[1:]:
        sum_ = sum_ + quant

    assert math.isclose(sum_.to(unit).v, value, rel_tol=1e-5)


@pytest.mark.parametrize("case", cases)
def test_math_add_inplace(case: tuple):
    text, unit, value, _ = case
    quantities = [Q(t) for t in text]
    sum_ = quantities[0]
    for quant in quantities[1:]:
        sum_ += quant

    assert math.isclose(sum_.to(unit).v, value, rel_tol=1e-5)


@pytest.mark.parametrize("case", cases)
def test_math_sub(case: tuple):
    text, unit, _, value = case
    quantities = [Q(t) for t in text]
    sum_ = quantities[0]
    for quant in quantities[1:]:
        sum_ -= quant

    assert math.isclose(sum_.to(unit).v, value, rel_tol=1e-5)


@pytest.mark.parametrize("case", cases)
def test_math_sub_inplace(case: tuple):
    text, unit, _, value = case
    quantities = [Q(t) for t in text]
    sum_ = quantities[0]
    for quant in quantities[1:]:
        sum_ = sum_ - quant

    assert math.isclose(sum_.to(unit).v, value, rel_tol=1e-5)


def test_math_temperature_rel_add():
    q = 10 * U("degC")
    q2 = 5 * U("degC")
    assert q.add_rel(q2) == (15 * U("degC"))


def test_math_temperature_rel_sub():
    q = 10 * U("degC")
    q2 = 5 * U("degC")
    assert q.sub_rel(q2) == (5 * U("degC"))


def test_math_temperature_abs():
    assert abs(-10 * U.degC).v == 10


def test_compare_gt():
    assert Q("1 m") > Q("1 ft")


def test_compare_lt():
    assert Q("1 ft") < Q("1 m")


def test_compare_gte():
    assert Q("1 m") >= Q("1 ft")


def test_compare_lte():
    assert Q("1 ft") <= Q("1 m")


def test_compare_e():
    assert (Q("1 ft") == Q("1 m")) is False


def test_compare_e2():
    assert (Q("1 ft") == Q("12 in")) is True


def test_compare_error_gt():
    with pytest.raises(ValueError) as _:
        Q("1 m") > Q("1 s")


def test_compare_error_lt():
    with pytest.raises(ValueError) as _:
        Q("1 m") < Q("1 s")


def test_compare_error_gte():
    with pytest.raises(ValueError) as _:
        Q("1 m") >= Q("1 s")


def test_compare_error_lte():
    with pytest.raises(ValueError) as _:
        Q("1 m") <= Q("1 s")


def test_compare_error_e():
    with pytest.raises(ValueError) as _:
        Q("1 m") == Q("1 s")


def test_round():
    q = Q("1.2345 ft")
    assert (round(q) == Q("1 ft")) is True
