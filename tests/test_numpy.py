
import pytest

import numpy as np

from unitpy import Unit, Quantity


def test_np_creation():
    assert (np.linspace(0, 4, 5) * Unit.m).unit == Unit.m
    assert np.all((np.linspace(0, 4, 5) * Unit.m).value == np.linspace(0, 4, 5))

## Addition and Subtraction ######################################################################
# numpy + int
def test_addition_int_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1 * Unit.ft
    assert np.all((a+b).v == np.array([0.3048, 1.3048, 2.3048, 3.3048, 4.3048]))
    assert (a+b).u == Unit.m


def test_subtraction_int_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1 * Unit.ft
    assert np.all((a-b).v == np.array([-0.3048,  0.6952,  1.6952,  2.6952,  3.6952]))


def test_addition_int_np_inplace():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1 * Unit.ft
    a += b
    assert np.all(a.v == np.array([0.3048, 1.3048, 2.3048, 3.3048, 4.3048]))


# numpy + float
def test_addition_float_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1.1 * Unit.ft
    assert np.all((a+b).v == np.array([0.33528, 1.33528, 2.33528, 3.33528, 4.33528]))


def test_subtraction_float_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1.1 * Unit.ft
    assert np.all((a-b).v == np.array([-0.33528,  0.66472,  1.66472,  2.66472,  3.66472]))


def test_addition_float_np_inplace():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1.1 * Unit.ft
    a += b
    assert np.all(a.v == np.array([0.33528, 1.33528, 2.33528, 3.33528, 4.33528]))


# numpy + numpy
def test_addition_np_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = np.linspace(0, 4, 5) * Unit.ft
    assert np.all((a+b).v == np.array([0.,     1.3048, 2.6096, 3.9144, 5.2192]))


def test_subtraction_np_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = np.linspace(0, 4, 5) * Unit.ft
    assert np.all((a-b).v == np.array([0.,     0.6952, 1.3904, 2.0856, 2.7808]))


def test_addition_np_np_inplace():
    a = np.linspace(0, 4, 5) * Unit.m
    b = np.linspace(0, 4, 5) * Unit.ft
    a += b
    assert np.all(a.v == np.array([0.,     1.3048, 2.6096, 3.9144, 5.2192]))

## Multiplication and Division ######################################################################
# numpy + float
def test_multi_np_float():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1.2 * Unit.s
    assert np.allclose((a * b).v, np.array([0., 1.2, 2.4, 3.6, 4.8]), atol=1E-9)
    assert (a*b).u == (Unit.m * Unit.s)


def test_div_np_float():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1.2 * Unit.s
    assert np.allclose((a/b).v, np.array([0., 0.83333333, 1.66666667, 2.5,   3.33333333]), atol=1E-9)
    assert (a / b).u == (Unit.m / Unit.s)


def test_multi_np_float_inplace():
    a = np.linspace(0, 4, 5) * Unit.m
    b = 1.2 * Unit.s
    a *= b
    assert np.allclose(a.v, np.array([0.,  1.2, 2.4, 3.6, 4.8]), atol=1E-9)
    assert a.u == (Unit.m * Unit.s)


# numpy + numpy
def test_multi_np_np():
    a = np.linspace(0, 4, 5) * Unit.m
    b = np.linspace(0, 4, 5) * Unit.s
    assert np.all((a*b).v == np.array([0.,  1.,  4.,  9., 16.]))
    assert (a*b).u == (Unit.m * Unit.s)


def test_div_np_np():
    a = np.linspace(1, 5, 5) * Unit.m
    b = np.linspace(1, 5, 5) * Unit.s
    assert np.all((a/b).v == np.array([1, 1.,  1.,  1.,  1.]))
    assert (a / b).u == (Unit.m / Unit.s)


def test_multi_np_np_inplace():
    a = np.linspace(0, 4, 5) * Unit.m
    b = np.linspace(0, 4, 5) * Unit.s
    a *= b
    assert np.all(a.v == np.array([0.,  1.,  4.,  9., 16.]))
    assert a.u == (Unit.m * Unit.s)


## Functions ######################################################################
def test_np_func_sum():
    a = np.linspace(-2, 4, 5) * Unit.m
    b: Quantity = np.sum(a)
    assert b.v == 5
    assert b.u == Unit.m


def test_np_func_max():
    a = np.linspace(-2, 4, 5) * Unit.m
    b: Quantity = np.max(a)
    assert b.v == 4
    assert b.u == Unit.m


def test_np_func_abs():
    a = np.linspace(-2, 4, 5) * Unit.m
    b: Quantity = np.abs(a)
    assert np.all(b.v == np.array([2.,  0.5, 1.,  2.5, 4.]))
    assert b.u == Unit.m


