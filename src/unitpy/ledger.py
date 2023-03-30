from __future__ import annotations

import unitpy.errors as errors
import unitpy.definitions.core as core
import unitpy.definitions.dimensions as dim_
import unitpy.definitions.prefix as prefix_


class UnitEntry:
    __slots__ = ("label", 'abbr', 'dim', "prefix", "additional_labels", "func")

    def __init__(self,
                 label: str,
                 abbr: str,
                 dim: tuple[type],
                 func,
                 prefix: prefix_.Prefix = None,
                 additional_labels: list[str, ...] = None,
                 ):
        self.label = label
        self.abbr = abbr
        self.dim = dim
        self.prefix = prefix
        self.additional_labels = additional_labels
        self.func = func

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label


meter = UnitEntry(
    label="meter",
    abbr="m",
    dim=(dim_.length,),
    func=lambda x: x
)
second = UnitEntry(
    label="second",
    abbr="s",
    dim=(dim_.time,),
    func=lambda x: x
)
mole = UnitEntry(
    label="mole",
    abbr="mol",
    dim=(dim_.amount_of_substance,),
    func=lambda x: x
)
kelvin = UnitEntry(
    label="kelvin",
    abbr="K",
    dim=(dim_.temperature,),
    func=lambda x: x
)
candela = UnitEntry(
    label="candela",
    abbr="cd",
    dim=(dim_.luminous_intensity,),
    func=lambda x: x,
    additional_labels=["candle"]
)
gram = UnitEntry(
    label="gram",
    abbr="g",
    dim=(dim_.mass,),
    func=lambda x: x
)

bases = (meter, second, mole, kelvin, candela, gram)


class Ledger:
    dimensions = dim_.dimensions
    prefixes = prefix_.prefixes
    bases = bases

    def __init__(self):
        self.units: list[UnitEntry] = []
        self.ledger = {}

    # def __getattr__(self, item):
    #     return self.Unit(item)

    def get_unit(self, unit: str) -> UnitEntry | None:
        if unit in self.ledger:
            return self.ledger[unit]

        return None
        # raise errors.UndefinedUnitError(f"{unit} is not a recognized unit.")


ledger = Ledger()


def add_bases():
    for base in ledger.bases:
        ledger.units.append(base)
        for pre in ledger.prefixes:
            ledger.units.append(
                UnitEntry(
                    label=pre.name + base.label,
                    abbr=pre.abbr[0] + base.abbr,
                    dim=base.dim,
                    prefix=pre,
                    func=lambda x: x * pre.multiplier,
                )  # TODO add additional abbr, label combinations
            )


def build_ledger():
    for unit in ledger.units:
        ledger.ledger[unit.label] = unit
        ledger.ledger[unit.abbr] = unit
        #TODO make other combinations


groups = [item for item in dir(core) if not item.startswith("__")]

# build ledger
add_bases()

build_ledger()