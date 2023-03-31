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



class Quantity:

    def __init__(self, value: str | int | float, unit: Unit = None):
        if isinstance(value, str):
            parse(value)
        self._unit = unit
        self._value = value
        self._multipler = multipler

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

    @property
    def base_value(self) -> int | float:
        return self._value

    @property
    def base_unit(self) -> Unit:
        return self._unit

    def __str__(self):
        return str(self._value) + " " + str(self._unit)

    def __repr__(self):
        return self.__str__()

    def __hash__(self) -> int:
        if self._unit.dimensionless:
            return hash(self.value)
        else:
            return hash((self._value, self._unit))

    def __copy__(self) -> Quantity:
        return self.__class__(copy.copy(self._value), self._unit)

    def __deepcopy__(self, memo) -> Quantity:
        return self.__class__(copy.deepcopy(self._value), self._unit)

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
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")
        if self.base_unit is not other.base_unit:
            raise errors.QuantityError("Comparision must have same units")

        self._value += self._value + other._value

    def __add__(self, other):
        if not isinstance(other, Quantity):
            raise errors.QuantityError("Comparision can't happen")
        if self.base_unit is not other.base_unit:
            raise errors.QuantityError("Comparision must have same units")

        return self.__class__(self._value + self._value, self._unit)

    __radd__ = __add__

    def __isub__(self, other):
        if is_duck_array_type(type(self._magnitude)):
            return self._iadd_sub(other, operator.isub)
        else:
            return self._add_sub(other, operator.sub)

    def __sub__(self, other):
        return self._add_sub(other, operator.sub)

    def __rsub__(self, other):
        if isinstance(other, datetime.datetime):
            return other - self.to_timedelta()
        else:
            return -self._add_sub(other, operator.sub)

    def __sub__(self, other):
        raise errors.UnitError("no subtraction")

    def __imul__(self, other):
    def __mul__(self, other):
        if isinstance(other, Unit):
            return Unit()
        elif isinstance(other, int) or isinstance(other, float):
            return self.value * other
     __rmul__ = __mul__

    def __truediv__(self, other):
        return self.value / other

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
    # def __copy__(self) -> Unit:
    #     ret = self.__class__(self._units)
    #     ret.__used = self.__used
    #     return ret
    #
    # def __deepcopy__(self, memo) -> Unit:
    #     ret = self.__class__(copy.deepcopy(self._units, memo))
    #     ret.__used = self.__used
    #     return ret
    #
    # def __str__(self) -> str:
    #     return format(self)
    #
    # def __bytes__(self) -> bytes:
    #     return str(self).encode(locale.getpreferredencoding())
    #
    # def __repr__(self) -> str:
    #     return "<Unit('{}')>".format(self._units)
    #
    # def __format__(self, spec) -> str:
    #     spec = spec or self.default_format
    #     # special cases
    #     if "Lx" in spec:  # the LaTeX siunitx code
    #         return r"\si[]{%s}" % siunitx_format_unit(self)
    #
    #     if "~" in spec:
    #         if not self._units:
    #             return ""
    #         units = UnitsContainer(
    #             dict(
    #                 (self._REGISTRY._get_symbol(key), value)
    #                 for key, value in self._units.items()
    #             )
    #         )
    #         spec = spec.replace("~", "")
    #     else:
    #         units = self._units
    #
    #     return format(units, spec)
    #
    # def __mul__(self, other):
    #     if self._check(other):
    #         if isinstance(other, self.__class__):
    #             return self.__class__(self._units * other._units)
    #         else:
    #             qself = self._REGISTRY.Quantity(1, self._units)
    #             return qself * other
    #
    #     if isinstance(other, Number) and other == 1:
    #         return self._REGISTRY.Quantity(other, self._units)
    #
    #     return self._REGISTRY.Quantity(1, self._units) * other
    #
    # def __truediv__(self, other):
    #     if self._check(other):
    #         if isinstance(other, self.__class__):
    #             return self.__class__(self._units / other._units)
    #         else:
    #             qself = 1 * self
    #             return qself / other
    #
    #     return self._REGISTRY.Quantity(1 / other, self._units)
    #
    # @property
    # def dimensionality(self):
    #     """
    #     Returns
    #     -------
    #     dict
    #         Dimensionality of the Unit, e.g. ``{length: 1, time: -1}``
    #     """
    #     return self._dimensionality

    # def parse(self, input: str):
    #     """ Pares string into Units."""
    #     seperate = self._parse_muliple_units()
    #     prefix, base = self._parse_prefix()
    #
    # def _parse_muliple_units(self, input: str): list