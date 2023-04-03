
import pytest

import unitpy


def test_unit_define_abbr():
    u = unitpy.Unit("m")
    assert u.abbr == "m"


def test_unit_define_word():
    u = unitpy.Unit("meter")
    assert u.label == "meter"


def test_unit_define_abbr_short():
    u = unitpy.Unit.m
    assert u.abbr == "m"


def test_unit_define_word_short():
    u = unitpy.Unit.meter
    assert u.label == "meter"


def test_unit_define_abbr2():
    u = unitpy.Unit("W")
    assert u.abbr == "W"


def test_unit_define_word2():
    u = unitpy.Unit("watt")
    assert u.label == "watt"


def test_unit_define_abbr_short2():
    u = unitpy.Unit.W
    assert u.abbr == "W"


def test_unit_define_word_short2():
    u = unitpy.Unit.watt
    assert u.label == "watt"


def test_unit_copy():
    import copy
    a = unitpy.U.meter
    b = copy.copy(a)
    a *= unitpy.U.meter
    assert b.label == "meter"
    assert b != a


def test_unit_deepcopy():
    import copy
    a = unitpy.U.meter
    b = copy.deepcopy(a)
    a *= unitpy.U.meter
    assert b.label == "meter"
    assert b != a

