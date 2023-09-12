
import pytest

from unitpy import U, Q


def test_quantity_unit():
    q = 1 * U("kilometer")
    assert q.v == 1
    assert q.u.label == "kilometer"


def test_quantity_unit_short():
    q = 2.1 * (U.kilometer / U.hour)
    assert q.v == 2.1


def test_quantity_parse():
    q = Q("1.1 km/h")
    assert q.v == 1.1


def test_quantity_copy():
    import copy
    a = 1 * U.meter
    b = copy.copy(a)
    a *= 2.2
    assert b.v == 1
    assert b.v != a.v


def test_quantity_deepcopy():
    import copy
    a = 1 * U.meter
    b = copy.deepcopy(a)
    a *= 2.2
    assert b.v == 1
    assert b.v != a.v


def test_format_str():
    q = Q("100.123 km/h")
    string = f"{q:.2f}"
    assert string == "100.12 kilometer/hour"


def test_format_str2():
    q = Q("10000.123 km/h")
    string = f"{q:,}"
    assert string == "10,000.123 kilometer/hour"


def test_format_str3():
    q = Q("100 km/h")
    string = f"{q:04}"
    assert string == "0100 kilometer/hour"


def test_format_str4():
    q = Q("100 km/h")
    string = f"{q:4}"
    assert string == " 100 kilometer/hour"
