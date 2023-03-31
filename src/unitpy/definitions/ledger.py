from __future__ import annotations

import unitpy.definitions.dimensions as dim_
import unitpy.definitions.prefix as prefix_
from unitpy.definitions.constants import constants
from unitpy.definitions.entry import Entry, bases, derived_quantities


class Ledger:
    """ The leger is a grouping all units. """
    dimensions = dim_.dimensions
    prefixes = prefix_.prefixes
    constants = constants
    bases = bases
    classes = dim_.classes

    def __init__(self):
        self.units: list[Entry] = []
        self._lookup = {}

    # def __getattr__(self, item):
    #     return self.Unit(item)

    def get_unit(self, unit: str) -> Entry | None:
        if unit in self._lookup:
            return self._lookup[unit]

        return None
        # raise errors.UndefinedUnitError(f"{unit} is not a recognized unit.")

    def unit_in_ledger(self, unit: str) -> bool:
        return unit in self._lookup

    def add_unit(self, entry: Entry):
        self.units.append(entry)

        if entry.class_ not in self.classes:
            self.classes[entry.class_] = self.dimensions

        if entry.label in self._lookup:
            raise ValueError(f"duplicate ledger entry.\nexisting: {self._lookup[entry.label]} \nsecond one: {entry}")
        self._lookup[entry.label] = entry

        if entry.abbr is not None:
            if entry.abbr in self._lookup:
                raise ValueError(f"duplicate ledger entry.\nexisting: {self._lookup[entry.abbr]} \nsecond one: {entry}")
            self._lookup[entry.abbr] = entry

        # TODO make other combinations


def add_bases():
    for base in ledger.bases:
        if base.label == "kilogram":
            add_kilogram_and_prefix(base)
            continue

        ledger.add_unit(base)
        for pre in ledger.prefixes.values():
            add_with_prefix(base, pre)


def add_kilogram_and_prefix(base):
    ledger.add_unit(base)
    for pre in ledger.prefixes.values():
        if pre.name == "kilo":
            ledger.add_unit(
                Entry(
                    label="gram",
                    abbr="g",
                    dim=base.dim,
                    func=lambda x: x,
                    class_=base.class_
                )
            )
        add_with_prefix(base, pre)


def add_with_prefix(base, pre):
    ledger.add_unit(
        Entry(
            label=pre.name + base.label,
            abbr=pre.abbr[0] + base.abbr,
            dim=base.dim,
            prefix=pre,
            func=lambda x: x * pre.multiplier,
            class_=base.class_
        )  # TODO add additional abbr, label combinations
    )


def add_derived_quantities():
    for base in derived_quantities:
        ledger.add_unit(base)
        for pre in ledger.prefixes.values():
            add_with_prefix(base, pre)


def add_core():
    groups_names = [item for item in dir(core) if not item.startswith("__")]
    # for group in groups_names:
    name = "volume"
    group = getattr(core, name)

    # base
    base = group.pop("base")
    base_unit = Unit(base)

    for entry in group:
        additional_labels = None
        abbr = group[entry]['abbr']
        if abbr is not None:
            if len(abbr) > 1:
                additional_labels = abbr[1:]
            abbr = abbr[0]

        ledger.add_unit(
            Entry(
                label=entry,
                abbr=abbr,
                dim=base_unit.dim,
                base_unit=base_unit,
                func=group[entry]["ratio"],
                additional_labels=additional_labels,
                class_=name
            )
        )


ledger = Ledger()
add_bases()
add_derived_quantities()
