from __future__ import annotations

import copy

from unitpy.errors import errors
from unitpy.definitions.dimensions import Dimension
from unitpy.definitions.entry import Entry
from unitpy.unit_parsing import Parser
from unitpy.utils.equation_formating import equation_formater


def get_dimensionality(unit_entries: dict[Entry | str, int | float]) -> Dimension:
    return Dimension({entry.dim: num for entry, num in unit_entries.items()})


class Unit:
    def __init__(self, unit_str: str):
        parser = Parser(unit_str)
        self._unit_entries: dict[Entry | str, int | float] = parser.parse()
        self._dimensionality: Dimension = get_dimensionality(self._unit_entries)

    def __str__(self):
        return equation_formater(self._unit_entries)

    def __repr__(self):
        return self.__str__()

    def __hash__(self) -> int:
        return self._units.__hash__()

    def __copy__(self) -> PlainUnit:
        ret = self.__class__(self._units)
        return ret

    def __deepcopy__(self, memo) -> PlainUnit:
        ret = self.__class__(copy.deepcopy(self._units, memo))
        return ret

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit(f"{self.name}*{other.name}", self.factor * other.factor)
        else:
            return Unit(f"{self.name}*{other}", self.factor * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            return Unit(f"{self.name}/{other.name}", self.factor / other.factor)
        else:
            return Unit(f"{self.name}/{other}", self.factor / other)

    def __rtruediv__(self, other):
        return Unit(f"{other}/{self.name}", other / self.factor)

    def __repr__(self):
        return f"Unit({self.name}, {self.factor})"

    def __eq__(self, other) -> bool:

    def __lt__(self, other):

    def __le__

    def __add__(self, other):
        raise errors.UnitError("no addition")

    def __sub__(self, other):
        raise errors.UnitError("no subtraction")

    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit()
        elif isinstance(other, int) or isinstance(other, float):
            return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __pow__(self, power, modulo=None):
        if isinstance(power, int) or isinstance(power, float):
            return Unit() self.value**power

    @property
    def dimensionality(self) -> Dimension:
        return self._dimensionality

    @property
    def dim(self) -> Dimension:
        return self._dimensionality

    @property
    def dimensionless(self) -> bool:
        if self._dimensionality:
            return False
        return True

    @property
    def base_unit(self) -> Unit:
        return self._base_unit


class Quantity:

    def __init__(self, value: str | int | float, unit: Unit | str = None):
        if isinstance(value, str):
            value, unit = parse(value)
        if isinstance(unit, str):
            unit = Unit(unit)
        self._unit = unit
        self._base_value = value
        self._multiplier = unit.multiplier

    @property
    def v(self) -> int | float:
        return self._base_value * self._multiplier

    @property
    def value(self) -> int | float:
        return self._base_value * self._multiplier

    @property
    def u(self) -> Unit:
        return self._unit

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def base_value(self) -> int | float:
        return self._base_value

    @property
    def base_unit(self) -> Unit:
        return self._unit.base_unit

    @property
    def dimensionality(self) -> Dimension:
        return self.unit.dimensionality

    @property
    def dim(self) -> Dimension:
        return self.unit.dimensionality

    @property
    def dimensionless(self) -> bool:
        return self.unit.dimensionless

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return f"Quantity({self.value}, '{self.unit}')"

    def __hash__(self) -> int:
        if self._unit.dimensionless:
            return hash(self.value)
        else:
            return hash((self._base_value, self._unit))

    def __copy__(self) -> Quantity:
        return self.__class__(copy.copy(self._base_value), self._unit)

    def __deepcopy__(self, memo) -> Quantity:
        return self.__class__(copy.deepcopy(self._base_value), self._unit)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")

        if self.base_unit is other.base_unit and self.base_value == other.base_value:
            return True

        return False

    def __lt__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")

        if self.base_unit is not other.base_unit:
            raise errors.QuantityError("Comparision must have same units")

        return self.base_value < other.base_value

    def __le__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")

        if self.base_unit is not other.base_unit:
            raise errors.QuantityError("Comparision must have same units")

        return self.base_value <= other.base_value

    def __gt__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")

        if self.base_unit is not other.base_unit:
            raise errors.QuantityError("Comparision must have same units")

        return self.base_value > other.base_value

    def __ge__(self, other: Quantity) -> bool:
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")

        if self.base_unit is not other.base_unit:
            raise errors.QuantityError("Comparision must have same units")

        return self.base_value >= other.base_value

    def __iadd__(self, other):
        if isinstance(other, Quantity) and self.unit == other.unit:
            self._base_value += other._base_value
            return self
        else:
            raise TypeError("Cannot add quantities with different units")

    def __add__(self, other):
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(self.value + other.value, self.unit)
        else:
            raise TypeError("Cannot add quantities with different units")

    __radd__ = __add__

    def __isub__(self, other):
        if isinstance(other, Quantity) and self.unit == other.unit:
            self._base_value -= other._base_value
            return self
        else:
            raise TypeError("Cannot subtract quantities with different units")

    def __sub__(self, other):
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(self.value - other.value, self.unit)
        else:
            raise TypeError("Cannot subtract quantities with different units")

    def __rsub__(self, other):
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(other.value - self.value, self.unit)
        else:
            raise TypeError("Cannot subtract quantities with different units")

    def __imul__(self, other):
        if isinstance(other, (int, float)):
            self._base_value *= other
            return self
        elif isinstance(other, Quantity):
            self._base_value *= other.value
            self._unit *= other.unit
            return self
        else:
            raise TypeError("Can only multiply Quantity by scalar")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        else:
            raise TypeError("Can only multiply Quantity by scalar")

     __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Quantity(self.value / other, self.unit)
        else:
            raise TypeError("Can only divide Quantity by scalar")

    def __itruediv__(self, other):
        if isinstance(other, (int, float)):
            self.value /= other
            return self
        else:
            raise TypeError("Can only divide Quantity by scalar")

    def __pow__(self, power, modulo=None):
        if isinstance(power, int) or isinstance(power, float):
            return Unit() self.value**power

    def __int__(self) -> int:
        return Quantity(int())

    def __float__(self) -> int:
        return Quantity(float())

    def __floor__(self):
        return Quantity

    def __mod__(self, other):

