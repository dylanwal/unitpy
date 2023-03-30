
from __future__ import annotations


class UnitPyError(Exception):
    """ base UnitPy error """

    def __init__(self, text: str):
        self.text = text

    def __str__(self):
        return self.text


class UndefinedUnitError(UnitPyError):
    """ raise for unrecognized units """
