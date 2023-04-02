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
        self.units.append(entry)

        if entry.label in self._lookup:
            raise ValueError(f"Duplicate ledger entry."
                             f"\nexisting: {repr(self._lookup[entry.label])} "
                             f"\nsecond one: {repr(entry)}")
        self._lookup[entry.label] = entry

        if entry.abbr is not None:
            if entry.abbr in self._lookup:
                raise ValueError(f"Duplicate ledger entry."
                                 f"\nexisting: {repr(self._lookup[entry.abbr])} "
                                 f"\nsecond one: {repr(entry)}")
            self._lookup[entry.abbr] = entry

        # TODO make other combinations


ledger = Ledger()


def add_bases():
    for base in bases.bases.values():
        ledger.add_unit(
            Entry(
                    label=base.label,
                    abbr=base.abbr,
                    base_unit=bases.BaseSet(**{base.label: 1}),
                    multiplier=1,
                )
        )

        if base.label == "kilogram":
            add_kilogram_and_prefix(base)
        else:
            for pre in ledger.prefixes.values():
                add_with_prefix(base, pre)


def add_kilogram_and_prefix(base: bases.BaseUnit):
    for pre in ledger.prefixes.values():
        if pre.name == "kilo":
            ledger.add_unit(
                Entry(
                    label="gram",
                    abbr="g",
                    base_unit=bases.BaseSet(**{base.label: 1}),
                    multiplier=1,
                    prefix=pre,
                )
            )
        add_with_prefix(base, pre)


def add_with_prefix(base: bases.BaseUnit, pre: prefix_.Prefix):
    ledger.add_unit(
        Entry(
            label=pre.name + base.label,
            abbr=pre.abbr[0] + base.abbr,
            base_unit=bases.BaseSet(**{base.label: 1}),
            multiplier=pre.multiplier,
            prefix=pre,
        )
    )


def add_derived_quantities():
    for base in unit_derived.derived_quantities.values():
        ledger.add_unit(base)
        for pre in ledger.prefixes.values():
            ledger.add_unit(
                Entry(
                    label=pre.name + base.label,
                    abbr=pre.abbr[0] + base.abbr,
                    base_unit=base.base_unit,
                    multiplier=pre.multiplier,
                    prefix=pre,
                    additional_labels=get_additional_labels(pre.abbr, base.additional_labels)
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
            if "prefix" in value and value["prefix"] is True:
                for pre in ledger.prefixes.values():
                    ledger.add_unit(
                        Entry(
                            label=pre.name + label,
                            abbr=pre.abbr[0] + value["abbr"],
                            base_unit=base_unit,
                            multiplier=value["multiplier"] * pre.multiplier,
                            prefix=pre,
                            additional_labels=get_additional_labels(pre.abbr, value["additional_labels"] if "additional_labels" in value else []),
                        )
                    )


def get_additional_labels(pre: list[str, ...], labels: list[str, ...]) -> list:
    if labels is None:
        return []
    if len(labels) < 1:
        return labels

    return ["".join(i) for i in itertools.product(pre, labels)]


add_bases()
add_derived_quantities()
add_core()
