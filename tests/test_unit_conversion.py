
import pytest

import unitpy

cases = (
    ("1 m", "100 cm"),
    ("1 m", "0.001 km"),

)


@pytest.mark.parametrize("case", cases)
def test_equal(case):
    q1 = unitpy.Q(case[0])
    q2 = unitpy.Q(case[1])
    assert q1 == q2
