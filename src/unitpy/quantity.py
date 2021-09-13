
from typing import Union

from src.unitpy.unit import Unit


class Quantity(Unit):

    def __init__(self, value: Union[int, float], unit: Unit):
        super().__init__(unit)
        self._value = value

    @property
    def v(self):
        return self._value

    @property
    def value(self):
        return self._value

    @property
    def u(self):
        return self._unit

    @property
    def unit(self):
        return self._unit