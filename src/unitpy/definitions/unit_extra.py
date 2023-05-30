from unitpy.definitions.unit_base import BaseSet
from unitpy.definitions.entry import Entry


extra_quantities = {
    "molar": Entry(
        label="molar",
        abbr="M",
        base_unit=BaseSet(mole=1, meter=-3),
        multiplier=1000,
        additional_labels=["molarity"]
    ),
    "pound per square inch": Entry(
        label="pound / inch**2",
        abbr="psi",
        base_unit=BaseSet(kilogram=1, meter=-1, second=-2),
        multiplier=6894.76,
        additional_labels=["pound per square inch"]
    ),
    "mile per hour": Entry(
        label="mile / hour",
        abbr="mph",
        base_unit=BaseSet(meter=1, second=-1),
        multiplier=0.44704,
        additional_labels=["mile per hour"]
    ),
    "debye": Entry(
        label="debye",
        abbr="D",
        base_unit=BaseSet(ampere=1, meter=1, second=1),
        multiplier=3.33564095e-30,
    ),
}
