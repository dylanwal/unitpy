from __future__ import annotations

from unitpy.utils.equation_formating import equation_formater


class BaseDimension:
    __slots__ = ("label", "abbr")

    def __init__(self, label: str, abbr: str):
        self.label = label
        self.abbr = abbr

    def __str__(self):
        return f"[{self.label}]"

    def __repr__(self):
        return f"[{self.abbr}]"


dimensions = {
    "length": BaseDimension("length", "l"),
    "time": BaseDimension("time", "t"),
    "amount_of_substance": BaseDimension("amount_of_substance", "n"),
    "temperature": BaseDimension("temperature", "T"),
    "luminous_intensity": BaseDimension("luminous_intensity", "lum"),
    "mass": BaseDimension("mass", "m"),
    "electric_current": BaseDimension("electric_current", "I")
}


class Dimension:
    r"""
    
    dim\,Q = T^\alpha L^\beta M^\gamma I^\delta \Theta^\epsilon N^\zeta J^\eta
    
    α, β, γ, δ, ε, ζ and η,  dimensional exponents
    
    https://www.nist.gov/pml/special-publication-330/sp-330-section-2#2.3.3
    """
    dimensions = dimensions
    __slots__ = ('length', 'time', 'amount_of_substance', 'temperature', 'luminous_intensity',
                 'mass', 'electric_current')

    def __init__(self,
                 length: int | float = 0,
                 time: int | float = 0,
                 amount_of_substance: int | float = 0,
                 temperature: int | float = 0,
                 luminous_intensity: int | float = 0,
                 mass: int | float = 0,
                 electric_current: int | float = 0,
                 ):
        self.length = length
        self.time = time
        self.amount_of_substance = amount_of_substance
        self.temperature = temperature
        self.luminous_intensity = luminous_intensity
        self.mass = mass
        self.electric_current = electric_current

    def __str__(self):
        return self.label

    def __hash__(self):
        return hash(tuple([type(self).__name__] + [getattr(self, base) for base in self.__slots__]))

    def __eq__(self, other: Dimension):
        if not isinstance(other, Dimension):
            raise TypeError("Equality can only be done between Dimension.")

        for base in self.__slots__:
            if getattr(self, base) != getattr(other, base):
                return False

        return True

    @property
    def label(self) -> str:
        return equation_formater({f"[{k.label}]": v for k, v in self.as_dict().items()})

    @property
    def abbr(self) -> str:
        return equation_formater({f"[{k.abbr}]": v for k, v in self.as_dict().items()})

    @property
    def dimensionless(self) -> bool:
        for dim in self.__slots__:
            if getattr(self, dim) != 0:
                return False

        return True

    def as_dict(self, key_str: bool = False) -> dict[BaseDimension, int | float]:
        if key_str:
            return {attr_name: getattr(self, attr_name) for attr_name in self.__slots__}
        return {self.dimensions[attr_name]: getattr(self, attr_name) for attr_name in self.__slots__}

    def process_dim_dict(self, dim_dict: dict[BaseDimension | str, int | float]):
        for k, v in dim_dict.items():
            self.add_dimension(k, v)

    def add_dimension(self, dim: BaseDimension | str, value: int | float):
        if isinstance(dim, BaseDimension):
            attr = getattr(self, dim.label)
        elif dim in self.__slots__:
            attr = getattr(self, dim)
        else:
            raise ValueError(f" '{dim}' is an invalid dimension. \n Accepted values are: {self.__slots__}")

        attr += value


classes = {
    # base
    Dimension(time=1): {
        "class": ("time",),
        "preferred_unit": "s"
    },
    "length": Dimension(**{"length": 1}),
    "mass": Dimension(**{"mass": 1}),
    "electric_current": Dimension(**{"electric_current": 1}),
    "temperature": Dimension(**{"temperature": 1}),
    "amount_of_substance": Dimension(**{"amount_of_substance": 1}),
    "luminous_intensity": Dimension(**{"luminous_intensity": 1}),

    # derived_quantities
    Dimension():
        {"class": ("angle",),
         "preferred_unit": "radian"
         },
    "solid_angle": None,
    "frequency": Dimension(**{"time": -1}),
    "force": Dimension(**{"time": -2, "mass": 1, "length": 1}),
    "stress": Dimension(**{"time": -2, "mass": 1, "length": -1}),
    "energy": Dimension(**{"time": -2, "mass": 1, "length": 2}),
    "power": Dimension(**{"time": -3, "mass": 1, "length": 2}),
    "electric_charge": Dimension(**{"electric_current": 1, "time": 1}),
    "electric_potential_difference": Dimension(**{"electric_current": -1, "time": -3, "mass": 1, "length": 2}),
    "capacitance": Dimension(**{"electric_current": 2, "time": 4, "mass": -1, "length": -2}),
    "electric_resistance": Dimension(**{"electric_current": -2, "time": -3, "mass": 1, "length": 2}),
    "electric_conductance": Dimension(**{"electric_current": 2, "time": 3, "mass": -1, "length": -2}),
    "magnetic_flux": Dimension(**{"electric_current": -1, "time": -2, "mass": 1, "length": 2}),
    "magnetic_flux_density": Dimension(**{"electric_current": -1, "time": -2, "mass": 1}),
    "inductance": Dimension(**{"electric_current": -2, "time": -2, "mass": 1, "length": 2}),
    "luminous_flux": Dimension(**{"mass": 1, "length": 2, "time": -3}),
    "illuminance": Dimension(**{"mass": 1, "time": -3}),
    "activity_radionuclide": Dimension(**{"time": -1}),
    "absorbed_dose": Dimension(**{"length": 2, "time": 2}),
    "dose": Dimension(**{"length": 2, "time": 2}),
    "catalytic_activity": Dimension(**{"amount_of_substance": 1, "time": -1}),

    # coherent derived units
    "area": Dimension(**{"length": 2}),
    "volume": Dimension(**{"length": 3}),
    "velocity": Dimension(**{"length": 1, "time": -1}),
    "acceleration": Dimension(**{"length": 1, "time": -2}),
    "wavenumber": Dimension(**{"length": -1}),
    "density": Dimension(**{"mass": 1, "length": -3}),
    "surface_density": Dimension(**{"mass": 1, "length": -2}),
    "specific_volume": Dimension(**{"mass": -1, "length": 3}),
    "current_density": Dimension(**{"electric_current": 1, "length": -2}),
    "magnetic_field_strength": Dimension(**{"electric_current": 1, "length": -1}),
    "molar_concentration": Dimension(**{"amount_of_substance": 1, "length": -3}),
    "mass_concentration": Dimension(**{"mass": 1, "length": -3}),
    "luminance": Dimension(**{"luminous_intensity": 1, "length": -2}),

    # SI coherent derived units
    "dynamic_viscosity": Dimension(**{"mass": 1, "length": -1, "time": -1}),
    "moment_of_force": Dimension(**{"mass": 1, "length": 2, "time": -2}),
    "surface_tension": Dimension(**{"mass": 1, "time": -2}),
    "angular_velocity": Dimension(**{"time": -1}),
    "angular_acceleration": Dimension(**{"time": -2}),
    'irradiance': Dimension(**{"mass": 1, "time": -3}),
    "entropy": Dimension(**{"mass": 1, "time": -2, "length": 2, "temperature": -1}),
    "specific_entropy": Dimension(**{"time": -2, "length": 2, "temperature": -1}),
}
