from __future__ import annotations

import itertools
import math
import copy
import typing
from datetime import timedelta

from unitpy.config import config
from unitpy.definitions.dimensions import Dimension
from unitpy.definitions.unit_base import BaseSet
from unitpy.definitions.entry import Entry
from unitpy.definitions.ledger import ledger
from unitpy.utils.equation_formating import equation_formater


_precision = 10


def get_base_unit(unit: dict[Entry, int | float]) -> BaseSet:
    base = BaseSet()
    for k, v in unit.items():
        base *= k.base_unit**v
    return base


def get_unit_from_base(base_set: BaseSet) -> dict[Entry, int | float]:
    dict_ = dict()

    for base in base_set.__slots__:
        value = getattr(base_set, base)
        if value != 0:
            dict_[ledger.get_entry(base)] = value

    return dict_


class MetaUnit(type):
    def __getattr__(self, item):
        return Unit(item)

np = None

class Unit(metaclass=MetaUnit):
    _ledger = ledger

    __slots__ = ("_unit", "_base_unit", "_multiplier", "_offset")

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method != "__call__":
            # Only handle ufuncs as callables
            return NotImplemented

        # Check types and return NotImplemented when upcast type encountered
        # types = {
        #     type(arg)
        #     for arg in list(inputs) + list(kwargs.values())
        #     if hasattr(arg, "__array_ufunc__")
        # }

        # Act on limited implementations by conversion to multiplicative identity
        # Quantity
        if ufunc.__name__ in ("multiply"):
            return Unit.__mul__(self, inputs[0])
        if ufunc.__name__ in ("true_divide", "divide", "floor_divide"):
            return Unit.__truediv__(self, inputs[0])

        return NotImplemented

    def __new__(cls, unit:  str | dict[Entry, int | float] | BaseSet = None):
        if isinstance(unit, str):
            from unitpy.utils.parsing import parse_unit
            a = parse_unit(unit)
            return a
        elif isinstance(unit, BaseSet):
            return Unit(get_unit_from_base(unit))

        return super().__new__(cls)

    def __init__(self, unit: str | dict[Entry, int | float] | BaseSet = None):
        if hasattr(self, "_unit"):
            return

        self._unit: dict[Entry, int | float] | None = unit if unit is not None else dict()
        self._base_unit: BaseSet | None = None
        self._multiplier: int | float | None = None
        self._offset: int | float | None = None

    def __str__(self):
        if config.abbr:
            return self.abbr
        return self.label

    def __repr__(self):
        return self.__str__()

    def __hash__(self) -> int:
        return self._base_unit.__hash__()

    def __copy__(self) -> Unit:
        unit = Unit()
        unit._unit = copy.copy(self._unit)
        return unit

    def __deepcopy__(self, memo) -> Unit:
        unit = Unit()
        unit._unit = copy.deepcopy(self._unit)
        return unit

    def __eq__(self, other: Unit) -> bool:
        """
        This matches to 'base units'; not 'units'
        """
        if not isinstance(other, Unit):
            raise ValueError(f"'Unit' equality can only be done between 'Unit' objects. \n{self} == {other}")

        return self.base_unit == other.base_unit

    def __lt__(self, other):
        raise ArithmeticError(f"Units can't be compared.\n{self} + {other}")

    __le__ = __lt__
    __gt__ = __lt__
    __ge__ = __lt__

    def __add__(self, other):
        raise ArithmeticError(f'Units can be added or subtracted.\n{self} + {other}')

    __iadd__ = __add__
    __radd__ = __add__
    __sub__ = __add__
    __isub__ = __add__
    __rsub__ = __add__

    def __mul__(self, other: int | float | Unit) -> Unit | Quantity:
        if isinstance(other, Unit):
            unit = Unit()
            for k in set(itertools.chain(self._unit.keys(), other._unit.keys())):
                unit._unit[k] = self._unit.get(k, 0) + other._unit.get(k, 0)
            return unit
        elif isinstance(other, int) or isinstance(other, float):
            return Quantity(other, self)
        else:
            global np
            if np is None:
                try:
                    import numpy
                    np = numpy
                    if isinstance(other, np.ndarray):
                        return Quantity(other, self)
                except ImportError:
                    pass
            else:
                if isinstance(other, np.ndarray):
                    return Quantity(other, self)
        raise TypeError(f"Can only multiply Unit by Unit.\n{self} * {other}")

    def __imul__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            raise TypeError(f"Can only multiply Unit by Unit.\n{self} * {other}")

        for k in set(itertools.chain(self._unit.keys(), other._unit.keys())):
            self._unit[k] = self._unit.get(k, 0) + other._unit.get(k, 0)
        return self

    __rmul__ = __mul__

    def __truediv__(self, other: int | float | Unit) -> Unit | Quantity:
        if isinstance(other, Unit):
            unit = Unit()
            for k in set(itertools.chain(self._unit.keys(), other._unit.keys())):
                unit._unit[k] = self._unit.get(k, 0) - other._unit.get(k, 0)
            return unit
        elif isinstance(other, int) or isinstance(other, float):
            return Quantity(1 / other, self)
        raise TypeError(f"Can only divide 'Unit' by 'Unit'.\n{self} / {other}")

    def __itruediv__(self, other: Unit) -> Unit:
        if not isinstance(other, Unit):
            raise TypeError(f"Can only divide 'Unit' by 'Unit'.\n{self} / {other}")

        for k in set(itertools.chain(self._unit.keys(), other._unit.keys())):
            self._unit[k] = self._unit.get(k, 0) - other._unit.get(k, 0)
        return self

    def __rtruediv__(self, other: int | float | Unit) -> Unit | Quantity:
        if isinstance(other, Unit):
            unit = Unit()
            for k in set(itertools.chain(self._unit.keys(), other._unit.keys())):
                unit._unit[k] = other._unit.get(k, 0) - self._unit.get(k, 0)
            return unit
        elif isinstance(other, int) or isinstance(other, float):
            return Quantity(other, self ** -1)
        raise TypeError(f"Can only divide 'Unit' by 'Unit'.\n{self} + {other}")

    def __pow__(self, power: int | float) -> Unit:
        if isinstance(power, int) or isinstance(power, float):
            unit = Unit()
            for k in self._unit:
                unit._unit[k] = self._unit[k] * power
            return unit

        raise TypeError(f"Power must be a 'int' or 'float'.\n{self} + {power}")

    def __ipow__(self, power: int | float) -> Unit:
        if isinstance(power, int) or isinstance(power, float):
            for k in self._unit:
                self._unit[k] = self._unit[k] * power
            return self

        raise TypeError(f"Power must be a 'int' or 'float'.\n{self} + {power}")

    @property
    def label(self) -> str:
        return equation_formater({k.label: v for k, v in self._unit.items()})

    @property
    def abbr(self) -> str:
        return equation_formater({k.abbr: v for k, v in self._unit.items()})

    @property
    def multiplier(self) -> int | float:
        if self._multiplier is None:
            try:
                self._multiplier = math.prod([k.multiplier ** v for k, v in self._unit.items()])
            except AttributeError:
                # math.prod added in python 3.8
                # will be removed when support for python 3.7 is over
                multipliers = [k.multiplier ** v for k, v in self._unit.items()]
                prod = 1
                for multi in multipliers:
                    prod *= multi
                self._multiplier = prod

        return self._multiplier

    @property
    def offset(self) -> int | float:
        if self._offset is None:
            self._offset = sum([k.offset for k, v in self._unit.items()])

        return self._offset

    @property
    def dimensionality(self) -> Dimension:
        return self.base_unit.dimensionality

    @property
    def dim(self) -> Dimension:
        return self.base_unit.dimensionality

    @property
    def dimensionless(self) -> bool:
        return self.base_unit.dimensionless

    @property
    def base_unit(self) -> BaseSet:
        if self._base_unit is None:
            self._base_unit = get_base_unit(self._unit)

        return self._base_unit

    def to_base_value(self, value: int | float) -> int | float:
        return self.multiplier * ( value + self.offset )

    def from_base_value(self, value: int | float) -> int | float:
        value = value / self.multiplier - self.offset
        return value


## Quantity ## noqa
#######################################################################################################################
#######################################################################################################################
np_wrap = None
class Quantity(typing.SupportsRound):
    compact_pickle = True
    # full pickle 624 bytes -> compact pickle 98 bytes
    # full 0.20 -> compact 0.31 create time
    _ledger = ledger

    __slots__ = ("_unit", "_base_value")

    def load_numpy(self):
        global np_wrap
        if np_wrap is None:
            from unitpy.numpy_funcs import numpy_wrap
            np_wrap = numpy_wrap

    def __array_function__(self, func, types, args, kwargs):
        self.load_numpy()
        return np_wrap("function", func, args, kwargs, types)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        self.load_numpy()
        types = set(
            type(arg)
            for arg in list(inputs) + list(kwargs.values())
            if hasattr(arg, "__array_ufunc__")
        )
        return np_wrap("ufunc", ufunc, inputs, kwargs, types)

    def __new__(cls, value: str | int | float = None, unit: Unit | BaseSet | str = None):
        if isinstance(value, str):
            from unitpy.utils.parsing import parse_quantity
            return parse_quantity(value)

        return super().__new__(cls)

    def __init__(self, value: str | int | float, unit: Unit | BaseSet | str = None):
        if hasattr(self, "_unit"):
            return
        if isinstance(unit, str) or isinstance(unit, BaseSet):
            unit = Unit(unit)

        self._unit = unit
        self._base_value = unit.to_base_value(value)

    def __str__(self):
        return f"{self.value} {self.unit}"

    def __repr__(self):
        return f"Quantity({self.value}, '{self.unit}')"

    def __format__(self, format_spec):
        return f"{format(self.v, format_spec)} {self.unit}"

    def __hash__(self) -> int:
        if self.dimensionless:
            return hash(self.value)
        else:
            return hash((self._base_value, self._unit))

    def __getstate__(self):
        if self.compact_pickle:
            return str(self)
        return self._base_value, self._unit.abbr

    def __setstate__(self, state):
        if isinstance(state, str):
            from unitpy.utils.parsing import parse_quantity
            qant = parse_quantity(state)
            self._base_value = qant._base_value
            self._unit = qant._unit
        else:
            self._base_value = state[0]
            self._unit = state[1]

    def __copy__(self) -> Quantity:
        return self.__class__(copy.copy(self._base_value), copy.copy(self._unit))

    def __deepcopy__(self, memo) -> Quantity:
        return self.__class__(copy.deepcopy(self._base_value), copy.deepcopy(self._unit))

    def _comparison_check(self, other: Quantity):
        if not isinstance(other, Quantity) or self.base_unit != other.base_unit:
            raise ValueError("'Quantity' comparison can only happen between quantities with same units."
                             f"\n{self} <--> {other}")

    def __eq__(self, other: Quantity) -> bool:
        self._comparison_check(other)
        return self.base_value == other.base_value

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

    def __add__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            base_value = self.base_value + other.base_value
            quant = Quantity(base_value, self.base_unit)
            return quant.to(self.unit)
        if other == 0:
            return self
        raise TypeError(f"Cannot add quantities with different units.\n{self} + {other}")

    def __iadd__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            self._base_value += other._base_value
            return self
        if other == 0:
            return self
        raise TypeError(f"Cannot add quantities with different units.\n{self} + {other}")

    __radd__ = __add__

    def __isub__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            self._base_value -= other._base_value
            return self
        if other == 0:
            return self
        raise TypeError(f"Cannot subtract quantities with different units.\n{self} - {other}")

    def __sub__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            base_value = self.base_value - other.base_value
            quant = Quantity(base_value, self.base_unit)
            return quant.to(self.unit)
        if isinstance(other, int) and other == 0:
            return self
        raise TypeError(f"Cannot subtract quantities with different units.\n{self} - {other}")

    def __rsub__(self, other: Quantity) -> Quantity:
        if isinstance(other, Quantity) and self.unit == other.unit:
            base_value = other.base_value - self.base_value
            quant = Quantity(base_value, self.base_unit)
            return quant.to(self.unit)
        else:
            raise TypeError(f"Cannot subtract quantities with different units.\n{self} + {other}")

    def __mul__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self._value * other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self._value * other._value, self.unit * other.unit)
        else:
            raise TypeError(f"Can only multiply Quantity by scalar.\n{self} * {other}\n"
                            f"This error can is commonly caused by missing parenthesis.")

    def __imul__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value *= other
            self._base_value = self._base_value
            return self
        elif isinstance(other, Quantity):
            self._base_value *= other._value
            self._unit *= other.unit
            return self
        else:
            raise TypeError(f"Can only multiply Quantity by scalar.\n{self} + {other}")

    __rmul__ = __mul__

    def __truediv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self._value / other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self._value / other._value, self.unit / other.unit)
        else:
            raise TypeError(f"Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.\n{self} / {other}")

    def __itruediv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value /= other
            return self
        elif isinstance(other, Quantity):
            self._base_value /= other._base_value
            self._unit /= other._unit
            return self
        else:
            raise TypeError(f"Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.\n{self} / {other}")

    def __rtruediv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(other / self._value, Unit("") / self.unit)
        elif isinstance(other, Quantity):
            return Quantity(other._value / self._value, Unit("") / self.unit)
        else:
            raise TypeError(f"Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.\n{self} / {other}")

    def __floordiv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self._value // other, self.unit)
        elif isinstance(other, Quantity):
            return Quantity(self._value // other._value, self.unit / other.unit)
        else:
            raise TypeError(f"Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.\n{self} / {other}")

    def __ifloordiv__(self, other: int | float | Quantity) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value //= other
            return self
        elif isinstance(other, Quantity):
            self._base_value //= other._base_value
            self._unit /= other._unit
            return self
        else:
            raise TypeError(f"Can only divide 'Quantity' by 'int', 'float' or 'Quantity'.\n{self} / {other}")

    def __pow__(self, power: int | float) -> Quantity:
        if isinstance(power, int) or isinstance(power, float):
            return Quantity(self._value ** power, self.unit ** power)
        else:
            raise TypeError(f"Power must be a 'int' or 'float'.\n{self} ** {power}")

    def __ipow__(self, power: int | float) -> Quantity:
        if isinstance(power, (int, float)):
            self._base_value **= power
            self._unit **= power
            return self
        else:
            raise TypeError(f"Power must be a 'int' or 'float'.\n{self} ** {power}")

    def __int__(self) -> Quantity:
        return Quantity(int(self._value), self.unit)

    def __float__(self) -> Quantity:
        return Quantity(float(self._value), self.unit)

    def __floor__(self) -> Quantity:
        return Quantity(math.floor(self._value), self.unit)

    def __mod__(self, other: int | float) -> Quantity:
        if isinstance(other, (int, float)):
            return Quantity(self._value % other, self.unit)
        else:
            raise TypeError("Can only perform the modulo operation of a 'Quantity' with an 'int' or 'float'."
                            f"\n{self} % {other}")

    def __imod__(self, other: int | float) -> Quantity:
        if isinstance(other, (int, float)):
            self._base_value %= other
            return self
        else:
            raise TypeError("Can only perform the modulo operation of a 'Quantity' with an 'int' or 'float'."
                            f"\n{self} % {other}")

    def __abs__(self) -> Quantity:
        return Quantity(abs(self._value), self.unit)

    def __ceil__(self) -> Quantity:
        return Quantity(math.ceil(self._value), self.unit)

    def __round__(self, n: int = 0) -> Quantity:
        return Quantity(round(self._value, n), self.unit)

    @property
    def _value(self):
        return self.unit.from_base_value(self._base_value)

    @property
    def v(self) -> int | float:
        return self.value

    @property
    def value(self) -> int | float:
        value = self._value
        if isinstance(value, float):
            value = round(value, _precision)
            if value.is_integer():
                value = int(value)

        return value

    @property
    def u(self) -> Unit:
        return self._unit

    @property
    def unit(self) -> Unit:
        return self._unit

    @property
    def base_value(self) -> int | float:
        value = self._base_value
        if isinstance(value, float):
            value = round(value, _precision)
            if value.is_integer():
                value = int(value)

        return value

    @property
    def base_unit(self) -> BaseSet:
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

    def to(self, unit: str | Unit) -> Quantity:
        if isinstance(unit, str):
            unit = Unit(unit)

        if self.unit != unit:
            raise ValueError(f"Units are not compatible.\n{self} --> {unit}")

        return Quantity(unit.from_base_value(self._base_value), unit)

    def is_close(self, other: Quantity, rel_tol: int | float = 1e-9, abs_tol: Quantity = None) -> bool:
        """ Return True if the other quantity is close to this quantity and False otherwise. """
        self._comparison_check(other)
        if abs_tol is None:
            abs_tol = 0
        else:
            abs_tol = abs_tol.base_value
        return math.isclose(self.base_value, other.base_value, rel_tol=rel_tol, abs_tol=abs_tol)

    def add_relative(self, other: Quantity) -> Quantity:
        """ Only need for temperature conversion """
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(self.value + other.to(self.unit).value, self.unit)
        else:
            raise TypeError(f"Cannot add quantities with different units.\n{self} + {other}")

    def add_rel(self, other: Quantity) -> Quantity:
        return self.add_relative(other)

    def sub_relative(self, other: Quantity) -> Quantity:
        """ Only need for temperature conversion """
        if isinstance(other, Quantity) and self.unit == other.unit:
            return Quantity(self.value - other.to(self.unit).value, self.unit)
        else:
            raise TypeError(f"Cannot subtract quantities with different units.\n{self} - {other}")

    def sub_rel(self, other: Quantity) -> Quantity:
        return self.sub_relative(other)

    def to_timedelta(self) -> timedelta:
        if self.unit.dimensionality != Dimension(time=1):
            raise TypeError(f"Must be a time dimension to convert to 'timedelta'.\n{self}")

        return timedelta(seconds=self.to("s").v)
