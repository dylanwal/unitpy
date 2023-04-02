from __future__ import annotations

import itertools

from unitpy.definitions.constants import constants
import unitpy.definitions.dimensions as dim_
import unitpy.definitions.prefix as prefix_
from unitpy.definitions.entry import Entry

import unitpy.definitions.unit_base as bases
import unitpy.definitions.unit_derived as unit_derived
import unitpy.definitions.unit_NIST as unit_NIST


class Ledger:
    """ The leger is a grouping all units. """
    dimensions = dim_.dimensions
    prefixes = prefix_.prefixes
    constants = constants
    bases = bases.bases
    classes = dim_.classes

    def __init__(self):
        self.units: list[Entry] = []
        self._lookup = {}
        self._symbols = set()

    def __str__(self):
        return f"Ledger(units: {len(self.units)}, symbols: {len(self._symbols)})"

    __repr__ = __str__

    def __contains__(self, item: str):
        return item in self.symbols

    @property
    def symbols(self) -> set[str, ...]:
        if len(self._symbols) == 0:
            self._symbols = set(self._lookup.keys())

        return self._symbols

    def get_entry(self, unit: str) -> Entry | None:
        if unit in self._lookup:
            return self._lookup[unit]

        return None

    def unit_in_ledger(self, unit: str) -> bool:
        return unit in self._lookup

    def add_unit(self, entry: Entry):
        if entry.label in self._lookup:
            raise ValueError(f"Duplicate ledger entry."
                             f"\nexisting: {repr(self._lookup[entry.label])} "
                             f"\nsecond one: {repr(entry)}")
        if entry.abbr is not None:
            if entry.abbr in self._lookup:
                raise ValueError(f"Duplicate ledger entry."
                                 f"\nexisting: {repr(self._lookup[entry.abbr])} "
                                 f"\nsecond one: {repr(entry)}")

            self.units.append(entry)
            self._lookup[entry.label] = entry
            self._lookup[entry.abbr] = entry
            for label in entry.additional_labels:
                if label in self._lookup:
                    raise ValueError(f"Duplicate ledger entry."
                                     f"\nexisting: {repr(self._lookup[entry.label])} "
                                     f"\nsecond one: {repr(entry)}")
                self._lookup[label] = entry


ledger = Ledger()


def add_bases():
    for base in bases.bases.values():
        if base.label == "kilogram":
            continue  # add separately

        base_entry = Entry(label=base.label, abbr=base.abbr, base_unit=bases.BaseSet(**{base.label: 1}), multiplier=1)
        ledger.add_unit(base_entry)
        add_with_prefix(base_entry)


def add_kilogram():
    base_entry = Entry(label="gram", abbr="g", base_unit=bases.BaseSet(kilogram=1), multiplier=1)
    ledger.add_unit(base_entry)
    add_with_prefix(base_entry)


def add_derived_quantities():
    for entry in unit_derived.derived_quantities.values():
        ledger.add_unit(entry)
        add_with_prefix(entry)


def add_with_prefix(entry: Entry):
    for pre in ledger.prefixes.values():
        ledger.add_unit(
            Entry(
                label=pre.name + entry.label,
                abbr=pre.abbr[0] + entry.abbr,
                base_unit=entry.base_unit,
                multiplier=entry.multiplier,
                prefix=pre,
                additional_labels=get_additional_labels(pre.abbr, entry.additional_labels)
            )
        )


def add_core():
    # for group in groups_names:
    for group in unit_NIST.units_NIST.values():
        # base
        base_unit = group.pop("base")

        for label, value in group.items():
            ledger.add_unit(
                Entry(
                    label=label,
                    abbr=value["abbr"],
                    base_unit=base_unit,
                    multiplier=value["multiplier"],
                    offset=value["offset"] if "offset" in value else None,
                    additional_labels=value["additional_labels"] if "additional_labels" in value else [],
                )
            )


def get_additional_labels(pre: list[str, ...], labels: list[str, ...]) -> list:
    if labels is None or len(labels) < 1:
        return []
    if len(labels) < 1:
        return pre + labels

    return ["".join(i) for i in itertools.product(pre, labels)]


add_bases()
add_kilogram()
add_derived_quantities()
add_core()


## add unofficial NIST units ## noqa
#######################################################################################################################

additional_units_with_prefix = {
    "liter"
}


def add_additional_units_with_prefix():
    for unit in additional_units_with_prefix:
        entry = ledger.get_entry(unit)
        add_with_prefix(entry)


add_additional_units_with_prefix()
