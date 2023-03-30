
from unitpy.ledger import ledger, UnitEntry
from unitpy.unit_parsing import Parser


class Unit:
    def __init__(self, unit_str: str):
        parser = Parser(unit_str)
        self._dimensionality: dict[UnitEntry, int | float] = parser.parse()

    def __str__(self):
        return "1"

    @property
    def dimensionless(self) -> bool:
        if self._dimensionality:
            return False
        return True


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