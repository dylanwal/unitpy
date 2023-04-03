
import pytest

import unitpy


def test_quantity_unit():
    q = 1 * unitpy.U("kilometer")
    assert q.v == 1
    assert q.u.label == "kilometer"


def test_quantity_unit_short():
    q = 2.1 * (unitpy.U.kilometer / unitpy.U.hour)
    assert q.v == 2.1


def test_quantity_parse():
    q = unitpy.Quantity("1.1 km/h")
    assert q.v == 1.1


def test_quantity_copy():
    import copy
    a = 1 * unitpy.U.meter
    b = copy.copy(a)
    a *= 2.2
    assert b.v == 1
    assert b.v != a.v


def test_quantity_deepcopy():
    import copy
    a = 1 * unitpy.U.meter
    b = copy.deepcopy(a)
    a *= 2.2
    assert b.v == 1
    assert b.v != a.v

