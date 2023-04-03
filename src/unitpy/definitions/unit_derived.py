from unitpy.definitions.unit_base import BaseSet
from unitpy.definitions.entry import Entry

derived_quantities = {
    "radian": Entry(
        label="radian",
        abbr="rad",
        base_unit=BaseSet(),
        multiplier=1,
    ),
    "steradian": Entry(
        label="steradian",
        abbr="sr",
        base_unit=BaseSet(),
        multiplier=1,
    ),
    "hertz": Entry(
        label="hertz",
        abbr="Hz",
        base_unit=BaseSet(second=-1),
        multiplier=1,
    ),
    "newton": Entry(
        label="newton",
        abbr="N",
        base_unit=BaseSet(kilogram=1, meter=1, second=-2),
        multiplier=1,
    ),
    "pascal": Entry(
        label="pascal",
        abbr="Pa",
        base_unit=BaseSet(kilogram=1, meter=-1, second=-2),
        multiplier=1,
    ),
    "joule": Entry(
        label="joule",
        abbr="J",
        base_unit=BaseSet(kilogram=1, meter=2, second=-2),
        multiplier=1,
    ),
    "watt": Entry(
        label="watt",
        abbr="W",
        base_unit=BaseSet(kilogram=1, meter=2, second=-3),
        multiplier=1,
    ),
    "coulomb": Entry(
        label="coulomb",
        abbr="C",
        base_unit=BaseSet(ampere=1, second=1),
        multiplier=1,
    ),
    "volt": Entry(
        label="volt",
        abbr="V",
        base_unit=BaseSet(kilogram=1, meter=2, second=-3, ampere=-1),
        multiplier=1,
    ),
    "farad": Entry(
        label="farad",
        abbr="F",
        base_unit=BaseSet(kilogram=-1, meter=-2, second=4, ampere=2),
        multiplier=1,
    ),
    "ohm": Entry(
        label="ohm",
        abbr="Ω",
        base_unit=BaseSet(kilogram=1, meter=2, second=-3, ampere=-2),
        multiplier=1,
    ),
    "siemens": Entry(
        label="siemens",
        abbr="S",
        base_unit=BaseSet(kilogram=-1, meter=-2, second=3, ampere=2),
        multiplier=1,
    ),
    "weber": Entry(
        label="weber",
        abbr="Wb",
        base_unit=BaseSet(kilogram=1, meter=2, second=-2, ampere=-1),
        multiplier=1,
    ),
    "tesla": Entry(
        label="tesla",
        abbr="T",
        base_unit=BaseSet(kilogram=1, second=-2, ampere=-1),
        multiplier=1,
    ),
    "henry": Entry(
        label="henry",
        abbr="H",
        base_unit=BaseSet(kilogram=1, meter=2, second=-2, ampere=-2),
        multiplier=1,
    ),
    "celsius": Entry(
        label="Celsius",
        abbr="degC",
        base_unit=BaseSet(kelvin=1),
        multiplier=1,
        offset=273.15,
        additional_labels=["centigrade", "celsius"],
    ),
    "lumen": Entry(
        label="lumen",
        abbr="lm",
        base_unit=BaseSet(candela=1),  # "cd*sr"
        multiplier=1,
    ),
    "lux": Entry(
        label="lux",
        abbr="lx",
        base_unit=BaseSet(candela=1, meter=-2),  # "cd*sr*m**−2"
        multiplier=1,
    ),
    "becquerel": Entry(
        label="becquerel",
        abbr="Bq",
        base_unit=BaseSet(second=-1),
        multiplier=1,
    ),
    "gray": Entry(
        label="gray",
        abbr="Gy",
        base_unit=BaseSet(meter=2, second=-2),
        multiplier=1,
    ),
    "sievert": Entry(
        label="sievert",
        abbr="Sv",
        base_unit=BaseSet(meter=2, second=-2),
        multiplier=1,
    ),
    "katal": Entry(
        label="katal",
        abbr="kat",
        base_unit=BaseSet(mole=1, second=-1),
        multiplier=1,
    )
}
