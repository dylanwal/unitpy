from __future__ import annotations

from unitpy.definitions.dimensions import BaseDimension, Dimension, dimensions
from unitpy.utils.equation_formating import equation_formater


class BaseUnit:
    __slots__ = ("label", "abbr", "dimension")

    def __init__(self, label: str, abbr: str, dimension: BaseDimension):
        self.label = label
        self.abbr = abbr
        self.dimension = dimension

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"BaseUnit({self.label}, {self.abbr}, {self.dimension})"


bases = {
    "second": BaseUnit(
        label="second",
        abbr="s",
        dimension=dimensions["time"],
        # definition=lambda x: 9_192_631_770/constants["hyperfine_transition_frequency_Cs_133"]
    ),
    "meter": BaseUnit(
        label="meter",
        abbr="m",
        dimension=dimensions["length"],
        # definition=lambda x: constants["speed_of_light"] / 299_792_458
    ),
    "kilogram": BaseUnit(
        label="kilogram",
        abbr="kg",
        dimension=dimensions["mass"],
        # definition=lambda x: constants["planck_constant"]/6.626_070_15e-34
    ),
    "ampere": BaseUnit(
        label="ampere",
        abbr="A",
        dimension=dimensions["electric_current"],
        # definition=lambda x: constants["elementary_charge"]/1.602_176_634e-19
    ),
    "kelvin": BaseUnit(
        label="kelvin",
        abbr="K",
        dimension=dimensions["temperature"],
        # definition=lambda x: constants["boltzmann_constant"]/1.380_649e-23
    ),
    "mole": BaseUnit(
        label="mole",
        abbr="mol",
        dimension=dimensions["amount_of_substance"],
        # definition=lambda x: constants["avogadro_number"] / 6.022_140_76e23
    ),
    "candela": BaseUnit(
        label="candela",
        abbr="cd",
        dimension=dimensions["luminous_intensity"],
        # definition=lambda x: constants["luminous_efficacy"] / 683
    )
}


class BaseSet:
    __slots__ = ("meter", "second", "mole", "kelvin", "candela", "kilogram", "ampere")  # DON'T change order
    _bases = bases

    def __init__(self,
                 meter: int | float = 0,
                 second: int | float = 0,
                 mole: int | float = 0,
                 kelvin: int | float = 0,
                 candela: int | float = 0,
                 kilogram: int | float = 0,
                 ampere: int | float = 0,
                 ):
        # DON'T change order
        self.meter = meter
        self.second = second
        self.mole = mole
        self.kelvin = kelvin
        self.candela = candela
        self.kilogram = kilogram
        self.ampere = ampere

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label

    def __eq__(self, other: BaseSet):
        if not isinstance(other, BaseSet):
            raise TypeError("Equality can only be done between BaseSets.")

        for base in self.__slots__:
            if getattr(self, base) != getattr(other, base):
                return False

        return True

    def __hash__(self):
        return hash(tuple([type(self).__name__] + [getattr(self, base) for base in self.__slots__]))

    def __mul__(self, other: BaseSet) -> BaseSet:
        if not isinstance(other, BaseSet):
            raise TypeError("Can only add 'BaseSet' with 'BaseSet'.")

        return BaseSet(**{base: getattr(self, base) + getattr(other, base) for base in self.__slots__})

    def __imul__(self, other: BaseSet) -> BaseSet:
        if not isinstance(other, BaseSet):
            raise TypeError("Can only add 'BaseSet' with 'BaseSet'.")

        for base in self.__slots__:
            setattr(self, base, getattr(self, base) + getattr(other, base))
        return self

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, BaseSet):
            raise TypeError("Can only subtract 'BaseSet' with 'BaseSet'.")

        return BaseSet(**{base: getattr(self, base) - getattr(other, base) for base in self.__slots__})

    def __itruediv__(self, other):
        if not isinstance(other, BaseSet):
            raise TypeError("Can only subtract 'BaseSet' with 'BaseSet'.")

        for base in self.__slots__:
            setattr(self, base, getattr(self, base) - getattr(other, base))
        return self

    def __rtruediv__(self, other):
        if not isinstance(other, BaseSet):
            raise TypeError("Can only subtract 'BaseSet' with 'BaseSet'.")

        return BaseSet(**{base: getattr(other, base) - getattr(self, base) for base in self.__slots__})

    def __pow__(self, power: int | float) -> BaseSet:
        if isinstance(power, int) or isinstance(power, float):
            return BaseSet(**{base: getattr(self, base) * power for base in self.__slots__})
        else:
            raise TypeError("Power must be a 'int' or 'float'.")

    def __ipow__(self, power: int | float) -> BaseSet:
        if isinstance(power, int) or isinstance(power, float):
            for base in self.__slots__:
                setattr(self, base, getattr(self, base) * power)
            return self
        else:
            raise TypeError("Power must be a 'int' or 'float'.")

    @property
    def label(self) -> str:
        return equation_formater({k.label: v for k, v in self.as_dict().items()})

    @property
    def abbr(self) -> str:
        return equation_formater({k.abbr: v for k, v in self.as_dict().items()})

    @property
    def dimensionality(self) -> Dimension:
        return Dimension(**{k.dimension.label: v for k, v in self.as_dict().items()})

    @property
    def dimensionless(self) -> bool:
        return self.dimensionality.dimensionless

    def as_dict(self) -> dict[BaseUnit, int | float]:
        return {self._bases[attr_name]: getattr(self, attr_name) for attr_name in self.__slots__}

    # @classmethod
    # def from_string(cls, unit: str) -> BaseSet:
    #     return BaseSet(**parse_base(unit, set(BaseSet.__slots__)))
