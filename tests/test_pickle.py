
import pickle
import pytest

from unitpy import Unit, Quantity


def test_pickling():
    q = 123.2 * Unit.cm
    dumps = pickle.dumps(q)
    loads = pickle.loads(dumps)
    assert q == loads
