import unitpy.definitions.core as core
import unitpy.definitions.dimensions as dim_


class UnitEntry:
    __slots__ = ("label", 'abv', 'dim', "prefix", "additional_labels", "func")

    def __init__(self,
                 label: str,
                 abv: str,
                 dim: tuple[type],
                 prefix: str = None,
                 additional_labels: list[str, ...] = None,
                 func: callable = None
                 ):
        self.label = label
        self.abv = abv
        self.dim = dim
        self.prefix = prefix
        self.additional_labels = additional_labels
        self.func = func


class Ledger:
    dimensions = dim_.dimensions

    def __init__(self):
        self.core_units = {}
        self.ledger = {}

    def lookup(self, unit: str):
        pass


groups = [item for item in dir(core) if not item.startswith("__")]


def create_base():
    meter = UnitEntry(
        label="meter",
        abv="m",
        dim=(dim_.Length,)
    )
    second = UnitEntry(
        label="second",
        abv="s",
        dim=(dim_.Time,)
    )
    mole = UnitEntry(
        label="mole",
        abv="mol",
        dim=(dim_.AmountOfSubstance,)
    )
    kelvin = UnitEntry(
        label="kelvin",
        abv="K",
        dim=(dim_.Temperature,)
    )
    candela = UnitEntry(
        label="candela",
        abv="cd",
        dim=(dim.LuminousIntensity,),
        additional_labels=["candle"]
    )
    kilogram = UnitEntry(
        label="gram",
        abv="g",
        prefix='k',
        dim=(dim_.Mass,),
    )


def create_other():
    for group_name in groups:
        group = getattr(core, group_name)
        base = group["base"]
        get
