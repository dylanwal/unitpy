from __future__ import annotations

from unitpy.utils.equation_formating import equation_formater


class BaseDimension:
    __slots__ = ("name", "abbr")

    def __init__(self, name: str, abbr: str):
        self.name = name
        self.abbr = abbr

    def __str__(self):
        return f"[{self.name}]"

    def __repr__(self):
        return f"[{self.abbr}]"


length = BaseDimension("length", "l")
time = BaseDimension("time", "t")
amount_of_substance = BaseDimension("amount_of_substance", "n")
temperature = BaseDimension("temperature", "T")
luminous_intensity = BaseDimension("luminous_intensity", "lum")
mass = BaseDimension("mass", "m")
electric_current = BaseDimension("electric_current", "I")

dimensions = {
    "length": length,
    "time": time,
    "amount_of_substance": amount_of_substance,
    "temperature": temperature,
    "luminous_intensity": luminous_intensity,
    "mass": mass,
    "electric_current": electric_current
}


class Dimension:
    """

    dim\,Q = T^\alpha L^\beta M^\gamma I^\delta \Theta^\epsilon N^\zeta J^\eta

    α, β, γ, δ, ε, ζ and η,  dimensional exponents
    https://www.nist.gov/pml/special-publication-330/sp-330-section-2#2.3.3
    """
    dimensions = dimensions
    __slots__ = ('length', 'time', 'amount_of_substance', 'temperature', 'luminous_intensity',
                 'mass', 'electric_current')

    def __init__(self, dim_dict: dict[BaseDimension, int | float] = None):
        self.length = 0
        self.time = 0
        self.amount_of_substance = 0
        self.temperature = 0
        self.luminous_intensity = 0
        self.mass = 0
        self.electric_current = 0

        if dim_dict is not None:
            self.process_dim_dict(dim_dict)

    def __str__(self):
        return equation_formater(self.as_dict())

    def as_dict(self) -> dict[BaseDimension, int | float]:
        return {self.dimensions[attr_name]: getattr(self, attr_name) for attr_name in self.__slots__}

    def process_dim_dict(self, dim_dict: dict[BaseDimension | str, int | float]):
        for k, v in dim_dict.items():
            self.add_dimension(k, v)

    def add_dimension(self, dim: BaseDimension | str, value: int | float):
        if isinstance(dim, BaseDimension):
            attr = getattr(self, dim.name)
        elif dim in self.__slots__:
            attr = getattr(self, dim)
        else:
            raise ValueError(f" '{dim}' is an invalid dimension. \n Accepted values are: {self.__slots__}")

        attr += value


classes = {
    # base
    "time": Dimension({time: 1}),
    "length": Dimension({length: 1}),
    "mass": Dimension({mass: 1}),
    "electric_current": Dimension({electric_current: 1}),
    "temperature": Dimension({temperature: 1}),
    "amount_of_substance": Dimension({amount_of_substance: 1}),
    "luminous_intensity": Dimension({luminous_intensity: 1}),

    # derived_quantities
    "angle": None,
    "solid_angle": None,
    "frequency": Dimension({time: -1}),
    "force": Dimension({time: -2, mass: 1, length: 1}),
    "stress": Dimension({time: -2, mass: 1, length: -1}),
    "energy": Dimension({time: -2, mass: 1, length: 2}),
    "power": Dimension({time: -3, mass: 1, length: 2}),
    "electric_charge": Dimension({electric_current: 1, time: 1}),
    "electric_potential_difference": Dimension({electric_current: -1, time: -3, mass: 1, length: 2}),
    "capacitance": Dimension({electric_current: 2, time: 4, mass: -1, length: -2}),
    "electric_resistance": Dimension({electric_current: -2, time: -3, mass: 1, length: 2}),
    "electric_conductance": Dimension({electric_current: 2, time: 3, mass: -1, length: -2}),
    "magnetic_flux": Dimension({electric_current: -1, time: -2, mass: 1, length: 2}),
    "magnetic_flux_density": Dimension({electric_current: -1, time: -2, mass: 1}),
    "inductance": Dimension({electric_current: -2, time: -2, mass: 1, length: 2}),
    "luminous_flux": Dimension({mass: 1, length: 2, time: -3}),
    "illuminance": Dimension({mass: 1, time: -3}),
    "activity_radionuclide": Dimension({time: -1}),
    "absorbed_dose": Dimension({length: 2, time: 2}),
    "dose": Dimension({length: 2, time: 2}),
    "catalytic_activity": Dimension({amount_of_substance: 1, time: -1}),

    # coherent derived units
    "area": Dimension({length: 2}),
    "volume": Dimension({length: 3}),
    "velocity": Dimension({length: 1, time: -1}),
    "acceleration": Dimension({length: 1, time: -2}),
    "wavenumber": Dimension({length: -1}),
    "density": Dimension({mass: 1, length: -3}),
    "surface_density": Dimension({mass: 1, length: -2}),
    "specific_volume": Dimension({mass: -1, length: 3}),
    "current_density": Dimension({electric_current: 1, length: -2}),
    "magnetic_field_strength": Dimension({electric_current: 1, length: -1}),
    "molar_concentration": Dimension({amount_of_substance: 1, length: -3}),
    "mass_concentration": Dimension({mass: 1, length: -3}),
    "luminance": Dimension({luminous_intensity: 1, length: -2}),

    # SI coherent derived units
    "dynamic_viscosity": Dimension({mass: 1, length: -1, time: -1}),
    "moment_of_force": Dimension({mass: 1, length: 2, time: -2}),
    "surface_tension": Dimension({mass: 1, time: -2}),
    "angular_velocity": Dimension({time: -1}),
    "angular_acceleration": Dimension({time: -2}),
    'irradiance': Dimension({mass: 1, time: -3}),
    "entropy": Dimension({mass: 1, time: -2, length: 2, temperature: -1}),
    "specific_entropy": Dimension({time: -2, length: 2, temperature: -1}),
}
