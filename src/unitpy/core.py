from __future__ import annotations

import math
import copy

from unitpy.definitions.dimensions import Dimension
from unitpy.definitions.entry import Entry
from unitpy.utils.parsing import parse_unit, parse_quantity
from unitpy.utils.equation_formating import equation_formater


def get_dimensionality(unit_entries: dict[Entry | str, int | float]) -> Dimension:
    return Dimension({entry.dim: num for entry, num in unit_entries.items()})


class Unit:
    def __init__(self, unit_str: str = None):
        self._unit: dict[Entry | str, int | float] | None = None
        self._base_unit: dict[Entry | str, int | float] | None = None

        if unit_str is not None:
            self._unit = parse_unit(unit_str)
            self._base_unit = get_base_unit(self._unit)

    def __str__(self):
        return equation_formater(self._unit)

    def __repr__(self):
        return self.__str__()

    def __hash__(self) -> int:
        return self._base_unit.__hash__()

    def __copy__(self) -> Unit:
        unit = Unit()
        unit._unit = self._unit
        unit._base_unit = self._base_unit
        return unit

    def __deepcopy__(self, memo) -> Unit:
        unit = Unit()
        unit._unit = self._unit
        unit._base_unit = self._base_unit
        return unit

    def __contains__(self, other: Unit) -> bool:
        if isinstance(other, Unit):
            return False

        for entry in self._base_unit:
            if entry not in other._base_unit:
                return False

        return True

    def __eq__(self, other: Unit) -> bool:
        """
        This matches to 'base units'; not 'units'
        """
        if not isinstance(other, Unit):
            raise ValueError("'Unit' equality can only be done between 'Unit' objects")

        return self._base_unit == self._base_unit

    def __lt__(self, other):
        raise ArithmeticError("Units can't be compared.")

    __le__ = __lt__
    __gt__ = __lt__
    __ge__ = __lt__

    def __add__(self, other):
        raise ArithmeticError('Units can be added or subtracted.')

    __iadd__ = __add__
    __radd__ = __add__
    __sub__ = __add__
    __isub__ = __add__
    __rsub__ = __add__

    # def __mul__(self, other: Unit) -> Unit:
    #     if isinstance(other, Unit):
    #         return Unit()
    #     else:
    #         return Unit(f"{self.name}*{other}", self.factor * other)
    #
    # def __imul__(self, other):
    #     pass
    #
    #  __rmul__ = __mul__
    #
    # def __truediv__(self, other):
    #     if isinstance(other, Unit):
    #         return Unit(f"{self.name}/{other.name}", self.factor / other.factor)
    #     else:
    #         return Unit(f"{self.name}/{other}", self.factor / other)
    #
    # def __itruediv__(self, other: int | float | Quantity) -> Quantity:
    #     pass
    #
    # def __rtruediv__(self, other):
    #     pass
    #
    # def __pow__(self, power: int | float) -> Unit:
    #     if isinstance(power, int) or isinstance(power, float):
    #         unit = Unit()
    #         unit._unit = self._unit**power
    #         return unit
    #     else:
    #         raise TypeError("Power must be a 'int' or 'float'.")
    #
    # def __ipow__(self,power):
    #     pass

    @property
    def dimensionality(self) -> Dimension:
        return self._base_unit.dimensionality

    @property
    def dim(self) -> Dimension:
        return self._base_unit.dimensionality

    @property
    def dimensionless(self) -> bool:
        if self._base_unit.dimensionaless:
            return False
        return True

    @property
    def base_unit(self) -> Unit:
        unit = Unit()
        unit._unit = self._base_unit
        unit._base_unit = self._base_unit
        return unit

    def from_base_value(self, value: int | float) -> int | float:
        return self._unit.multiplier * value + self._unit.offset

    def to_base_value(self, value: int | float) -> int | float:
        return value / self._unit.multiplier - self._unit.offset


## Quantity ## noqa
#######################################################################################################################
#######################################################################################################################
class Quantity:

    def __init__(self, value: str | int | float, unit: Unit | str = None):
        if isinstance(value, str):
            value, unit = parse_quantity(value)
        if isinstance(unit, str):
            unit = Unit(unit)
        self._unit = unit
        self._base_value = unit.to_base_value(value)

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return f"Quantity({self.value}, '{self.unit}')"

    def __hash__(self) -> int:
        if self.dimensionless:
            return hash(self.value)
        else:
            return hash((self._base_value, self._unit))

    def __copy__(self) -> Quantity:
        return self.__class__(copy.copy(self._base_value), self._unit)

    def __deepcopy__(self, memo) -> Quantity:
        return self.__class__(copy.deepcopy(self._base_value), self._unit)

    def _comparison_check(self, other: Quantity):
        if not isinstance(other, Quantity) or self.base_unit is not other.base_unit:
            raise ValueError("'Quantity' comparison can only happen between quantities with same units.")

    def __eq__(self, other: Quantity) -> bool:
        self._comparison_check(other)
        return self.base_unit is other.base_unit and self.base_value == other.base_value

    def __lt__(self, other: Quantity) -> bool:
        self._comparison_check(other)
        return self.base_value < other.base_value

    def __le__(self, other: Quantity) -> bool:
        self._comparison_check(other)
        return self.base_value <= other.base_value

    def __gt__(self, other: Quantity) -> bool:
        self._comparison_check(other)
        return self.base_value > other.base_value

    def __ge__(self, other: Quantity) -> bool:
        self._comparison_check(other)
        return self.base_value >= other.base_value

    def __iadd__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            self._base_value += other._base_value
            return self
        else:
            raise TypeError("Cannot add quantities with different units")

    def __add__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(self.value + other.value, self.unit)
        else:
            raise TypeError("Cannot add quantities with different units")

    __radd__ = __add__

    def __isub__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            self._base_value -= other._base_value
            return self
        else:
            raise TypeError("Cannot subtract quantities with different units")

    def __sub__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(self.value - other.value, self.unit)
        else:
            raise TypeError("Cannot subtract quantities with different units")

    def __rsub__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(other.value - self.value, self.unit)
        else:
            raise TypeError("Cannot subtract quantities with different units")

    def __mul__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value * other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        else:
            raise TypeError("Can only multiply Quantity by scalar")

    def __imul__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value *= other
            return self
        elif isinstance(other, Quantity):
            self._base_value *= other.value
            self._unit *= other.unit
            return self
        else:
            raise TypeError("Can only multiply Quantity by scalar")

    __rmul__ = __mul__

    def __truediv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value / other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        else:
            raise TypeError("Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.")

    def __itruediv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value /= other
            return self
        elif isinstance(other, Quantity):
            self._base_value /= other._base_value
            self._unit /= other._unit
            return self
        else:
            raise TypeError("Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.")

    def __rtruediv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(other / self.value, Unit("") / self.unit)
        elif isinstance(other, Quantity):
            return Quantity(other.value / self.value, Unit("") / self.unit)
        else:
            raise TypeError("Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.")

    def __floordiv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value // other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self.value // other.value, self.unit / other.unit)
        else:
            raise TypeError("Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.")

    def __ifloordiv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value //= other
            return self
        elif isinstance(other, Quantity):
            self._base_value //= other._base_value
            self._unit /= other._unit
            return self
        else:
            raise TypeError("Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.")

    def __pow__(self, power: int | float) -> Quantity:
        if isinstance(power, int) or isinstance(power, float):
            return Quantity(self.value**power, self.unit)
        else:
            raise TypeError("Power must be a 'int' or 'float'.")

    def __ipow__(self, other: int | float) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value **= other
            return self
        else:
            raise TypeError("Power must be a 'int' or 'float'.")

    def __int__(self) -> Quantity:
        return Quantity(int(self.value), self.unit)

    def __float__(self) -> Quantity:
        return Quantity(float(self.value), self.unit)

    def __floor__(self) -> Quantity:
        return Quantity(math.floor(self.value), self.unit)

    def __mod__(self, other: int | float) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self.value % other, self.unit)
        else:
            raise TypeError("Can only perform the modulo operation of a 'Quantity' with an 'int' or 'float'.")

    def __imod__(self, other: int | float) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value %= other
            return self
        else:
            raise TypeError("Can only perform the modulo operation of a 'Quantity' with an 'int' or 'float'.")

    def __abs__(self) -> Quantity:
        return Quantity(abs(self.value), self.unit)

    def __ceil__(self) -> Quantity:
        return Quantity(math.ceil(self.value), self.unit)

    @property
    def v(self) -> int | float:
        return self.unit.from_base_value(self._base_value)

    @property
    def value(self) -> int | float:
        return self.unit.from_base_value(self._base_value)

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
