from __future__ import annotations

import unitpy.definitions.dimensions as dim_
import unitpy.definitions.prefix as prefix_


class Entry:
    """
    representation of a fundamental unit

    """
    __slots__ = ("label", 'abbr', 'dim', "prefix", "additional_labels", "func", "class_", "base_unit")
    classes = dim_.classes

    def __init__(self,
                 label: str,
                 abbr: str | None,
                 dim: dim_.Dimension | None,
                 func,
                 base_unit=None,  # Unit | None
                 prefix: prefix_.Prefix = None,
                 additional_labels: list[str, ...] = None,
                 class_: str = None,
                 ):
        self.label = label
        self.abbr = abbr
        self.dim = dim
        self.prefix = prefix
        self.additional_labels = additional_labels
        self.func = func
        self.class_ = class_
        self.base_unit = base_unit

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


second = Entry(
    label="second",
    abbr="s",
    dim=dim_.classes["time"],
    func=lambda x: x,
    class_="time"
    # definition=lambda x: 9_192_631_770/constants["hyperfine_transition_frequency_Cs_133"]
)
meter = Entry(
    label="meter",
    abbr="m",
    dim=dim_.classes["length"],
    func=lambda x: x,
    class_="length",
    # definition=lambda x: constants["speed_of_light"] / 299_792_458
)
kilogram = Entry(
    label="kilogram",
    abbr="kg",
    prefix=prefix_.kilo,
    dim=dim_.classes["mass"],
    func=lambda x: x * prefix_.kilo.multiplier,
    class_="mass",
    # definition=lambda x: constants["planck_constant"]/6.626_070_15e-34
)
ampere = Entry(
    label="ampere",
    abbr="A",
    dim=dim_.classes["electric_current"],
    func=lambda x: x,
    # definition=lambda x: constants["elementary_charge"]/1.602_176_634e-19
)
kelvin = Entry(
    label="kelvin",
    abbr="K",
    dim=dim_.classes["temperature"],
    func=lambda x: x,
    # definition=lambda x: constants["boltzmann_constant"]/1.380_649e-23
)
mole = Entry(
    label="mole",
    abbr="mol",
    dim=dim_.classes["amount_of_substance"],
    func=lambda x: x,
    # definition=lambda x: constants["avogadro_number"] / 6.022_140_76e23
)
candela = Entry(
    label="candela",
    abbr="cd",
    dim=dim_.classes["luminous_intensity"],
    func=lambda x: x,
    additional_labels=["candle"],
    # definition=lambda x: constants["luminous_efficacy"] / 683
)


bases = (meter, second, mole, kelvin, candela, kilogram, ampere)


radian = Entry(
    label="radian",
    abbr="rad",
    base_unit=None,
    dim=None,
    func=lambda x: x,
    class_="angle"
)
steradian = Entry(
    label="steradian",
    abbr="sr",
    base_unit=None,
    dim=None,
    func=lambda x: x,
    class_="solid_angle"
)
hertz = Entry(
    label="hertz",
    abbr="Hz",
    base_unit="s**-1",
    dim=dim_.classes["frequency"],
    func=lambda x: x,
)
newton = Entry(
    label="newton",
    abbr="N",
    base_unit="kg*m*s**-2",
    dim=dim_.classes["force"],
    func=lambda x: x,
)
pascal = Entry(
    label="pascal",
    abbr="Pa",
    base_unit="kg*m**-1*s**-2",
    dim=dim_.classes["stress"],
    func=lambda x: x,
)
joule = Entry(
    label="joule",
    abbr="J",
    base_unit="kg*m**2*s**-2",
    dim=dim_.classes["energy"],
    func=lambda x: x,
)
watt = Entry(
    label="watt",
    abbr="W",
    base_unit="kg*m**2*s**-3",
    dim=dim_.classes["power"],
    func=lambda x: x,
)
coulomb = Entry(
    label="coulomb",
    abbr="C",
    base_unit="A*s",
    dim=dim_.classes["electric_charge"],
    func=lambda x: x,
)
volt = Entry(
    label="volt",
    abbr="V",
    base_unit="kg*m**2*s**−3*A**−1",
    dim=dim_.classes["electric_potential_difference"],
    func=lambda x: x,
)
farad = Entry(
    label="farad",
    abbr="F",
    base_unit="kg**−1*m**−2*s**4*A**2",
    dim=dim_.classes["capacitance"],
    func=lambda x: x,
)
ohm = Entry(
    label="ohm",
    abbr="Ω",
    base_unit="kg*m**2*s**-3*A**−2",
    dim=dim_.classes["electric_resistance"],
    func=lambda x: x,
)
siemens = Entry(
    label="siemens",
    abbr="S",
    base_unit="kg**−1*m**−2*s**3*A**2",
    dim=dim_.classes["electric_conductance"],
    func=lambda x: x,
)
weber = Entry(
    label="weber",
    abbr="Wb",
    base_unit="kg*m**2*s**−2*A*−1",
    dim=dim_.classes["magnetic_flux"],
    func=lambda x: x,
)
tesla = Entry(
    label="tesla",
    abbr="T",
    base_unit="kg*s**−2*A**−1",
    dim=dim_.classes["magnetic_flux_density"],
    func=lambda x: x,
)
henry = Entry(
    label="henry",
    abbr="H",
    base_unit="kg*m**2*s**−2*A**−2",
    dim=dim_.classes["inductance"],
    func=lambda x: x,
)
celsius = Entry(
    label="Celsius",
    abbr="degC",
    base_unit="K",
    dim=dim_.classes["temperature"],
    func=lambda x: x - 273.15,
    additional_labels=["centigrade", "celsius"],
)
lumen = Entry(
    label="lumen",
    abbr="lm",
    base_unit="cd*sr",
    dim=dim_.classes["luminous_flux"],
    func=lambda x: x,
)
lux = Entry(
    label="lux",
    abbr="lx",
    base_unit="cd*sr*m**−2",
    dim=dim_.classes["illuminance"],
    func=lambda x: x,
)
becquerel = Entry(
    label="becquerel",
    abbr="Bq",
    base_unit="s**-1",
    dim=dim_.classes["activity_radionuclide"],
    func=lambda x: x,
)
gray = Entry(
    label="gray",
    abbr="Gy",
    base_unit="m**2*s**-2",
    dim=dim_.classes["absorbed_dose"],
    func=lambda x: x,
)
sievert = Entry(
    label="sievert",
    abbr="Sv",
    base_unit="m**2*s**-2",
    dim=dim_.classes["dose"],
    func=lambda x: x,
)
katal = Entry(
    label="katal",
    abbr="kat",
    base_unit="mol*s**-1",
    dim=dim_.classes["catalytic_activity"],
    func=lambda x: x,
)

derived_quantities = (radian, steradian, hertz, newton, pascal, joule, watt, coulomb, volt, farad, ohm,
                      siemens, weber, tesla, henry, celsius, lumen, lux, becquerel, gray, sievert, katal)
