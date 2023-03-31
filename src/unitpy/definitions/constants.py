class Constant:
    """

    https://www.nist.gov/pml/special-publication-330/sp-330-section-2#2.2
    """
    def __init__(self, name: str, value: int | float, unit: str | None, abbr: str, description: str):
        self.name = name
        self.value = value
        self.unit = unit
        self.abbr = abbr
        self.description = description

    def __add__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __mul__(self, other):
        return self.value * other

    def __truediv__(self, other):
        return self.value / other

    def __pow__(self, power, modulo=None):
        return self.value**power


constants = {
    # Mathematical Constants
    "pi": Constant(
        name="pi",
        value=3.141_592_653_589_793_238_462_643_383_279_502_884_197_169_399_375_1,
        unit=None,
        abbr="pi",
        description="pi"
    ),
    # Measured Constants
    "hyperfine_transition_frequency_Cs_133": Constant(
        name="hyperfine_transition_frequency_Cs_133",
        value=9_192_631_770,
        unit="Hz",
        abbr="delta_v_Cs",
        description="hyperfine transition frequency of cesium-133"
    ),
    "speed_of_light": Constant(
        name="speed_of_light",
        value=299_792_458,
        unit="m/s",
        abbr="c",
        description="The meter is defined by taking the fixed numerical value of the speed of light in vacuum c to be "
                    "299,792,458 when expressed in the unit m s−1"
    ),
    "avogadro_number": Constant(
        name="avogadro_number",
        value=6.022_140_76e23,
        unit="count",
        abbr="Na",
        description="number of particles in a mole"
    ),
    "planck_constant": Constant(
        name="planck_constant",
        value=6.626_070_15e-34,
        unit="J*s",
        abbr="h",
        description="The smallest size of energy that can be exchanged"
    ),
    "elementary_charge": Constant(
        name="elementary_charge",
        value=1.602_176_634e-19,
        unit="C",
        abbr="e",
        description="Amount of charge in an electron."
    ),
    "boltzmann_constant": Constant(
        name="boltzmann_constant",
        value=1.380_649e-23,
        unit="J/K",
        abbr="k",
        description="Relates an object’s energy to its temperature."
    ),
    "luminous_efficacy": Constant(
        name="luminous_efficacy",
        value=683,
        unit="lm/W",
        abbr="K_cd",
        description="The total amount of visible light that a source produces using a certain amount of power."
    )
}
