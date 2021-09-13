
from typing import Union

from src.unitpy.unit import Unit
from src.unitpy.quantity import Quantity


class Measurement(Quantity):

    def __init__(self, value: Union[int, float, Quantity], error: Union[int, float, Quantity], unit: Unit):
        super().__init__(value, unit)
        self._error = error