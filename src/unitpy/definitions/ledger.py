from __future__ import annotations

import itertools

from unitpy.errors import AmbiguousUnitSymbolError
from unitpy.definitions.constants import constants
import unitpy.definitions.dimensions as dim_
import unitpy.definitions.prefix as prefix_
from unitpy.definitions.entry import Entry

import unitpy.definitions.unit_base as bases
import unitpy.definitions.unit_derived as unit_derived
import unitpy.definitions.unit_NIST as unit_NIST
import unitpy.definitions.unit_extra as unit_extra


class DuplicateEntry:
    def __init__(self, symbol: str, entries: list[Entry]) -> None:
        self.entries = entries
        self.symbol = symbol

    def list_str(self) -> list[str]:
        return [str(e) for e in self.entries]


class Ledger:
    """ The leger is a grouping all units. """
    _cache = False
    dimensions = dim_.dimensions
    prefixes = prefix_.prefixes
    constants = constants
    bases = bases.bases
    classes = dim_.classes

    def __init__(self):
        self.units: list[Entry] = list()
        self._duplicate_symbols: dict[str, DuplicateEntry] = dict()
        self._lookup: dict[str, Entry] = dict()

    def __str__(self):
        return f"Ledger(units: {len(self.units)}, symbols: {len(self.symbols)})"

    __repr__ = __str__

    def __contains__(self, item: str):
        return item in self.symbols

    @property
    def symbols(self) -> set[str]:
        return set(self._lookup.keys())

    def get_entry(self, unit: str) -> Entry | None:
        if unit in self._lookup:
            return self._lookup[unit]
        if unit in self._duplicate_symbols:
            duplicate_entry = self._duplicate_symbols[unit]
            raise AmbiguousUnitSymbolError(
                f"Unit '{unit}' is ambiguous. It could correspond to the following units:"
                "\n\t".join(duplicate_entry.list_str()) +
                "Try another approach to entering your desired unit.(use full name, prefix*unit, etc.)"
            )

        return None

    def add_unit(self, entry: Entry):
        self.units.append(entry)

        if entry.label in self._lookup or entry.label in self._duplicate_symbols:
            self._duplicate(entry, entry.label)
        else:
            self._lookup[entry.label] = entry

        if entry.abbr is not None and entry.abbr != entry.label:
            if entry.abbr in self._lookup or entry.abbr in self._duplicate_symbols:
                self._duplicate(entry, entry.abbr)
            else:
                self._lookup[entry.abbr] = entry

        if entry.additional_labels:
            for label in entry.additional_labels:
                if label in self._lookup or label in self._duplicate_symbols:
                    self._duplicate(entry, label)
                else:
                    self._lookup[label] = entry

    def _duplicate(self, entry: Entry, symbol: str):
        if symbol in self._lookup:
            lookup_entry = self._lookup.pop(symbol)
            duplicate_entry = DuplicateEntry(symbol, [entry, lookup_entry])
            self._duplicate_symbols[symbol] = duplicate_entry
        else:
            duplicate_entry = self._duplicate_symbols[symbol]
            duplicate_entry.entries.append(entry)

    def add_in_main_duplicates(self):
        """ For duplicates keep the none prefix value. """
        for symbol, duplicate in self._duplicate_symbols.items():
            # if only one entry has no prefix
            if [entry.prefix is None for entry in duplicate.entries].count(True) == 1:
                for entry in duplicate.entries:
                    if entry.prefix is None:
                        self._lookup[symbol] = entry
                        break

    def _save_cache(self):
        a = self.symbols  # cause it to build

        import pathlib
        file = pathlib.Path(__file__).parent / pathlib.Path("_ledger_cache.pickle")
        import pickle
        with open(file, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @classmethod
    def _load_cache(cls):
        import pathlib
        file = pathlib.Path(__file__).parent / pathlib.Path("_ledger_cache.pickle")
        if file.exists():
            cls._cache = True
            import pickle
            with open(file, 'rb') as f:
                return pickle.load(f)

        return None


ledger = Ledger()


def add_bases():
    for base in bases.bases.values():
        if base.label == "kilogram":
            continue  # add separately

        base_entry = Entry(label=base.label, abbr=base.abbr, base_unit=bases.BaseSet(**{base.label: 1}), multiplier=1)
        ledger.add_unit(base_entry)
        add_with_prefix(base_entry)


def add_kilogram():
    base_entry = Entry(label="gram", abbr="g", base_unit=bases.BaseSet(kilogram=1), multiplier=0.001)
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
                label=pre.label + entry.label,
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
            entry = Entry(
                label=label,
                abbr=value["abbr"],
                base_unit=base_unit,
                multiplier=value["multiplier"],
                offset=value["offset"] if "offset" in value else None,
                additional_labels=value["additional_labels"] if "additional_labels" in value else [],
            )
            ledger.add_unit(entry)
            add_with_prefix(entry)


def get_additional_labels(pre: list[str, ...], labels: list[str, ...]) -> list:
    if labels is None or len(labels) == 1:
        return []
    # if len(labels) == 1:
    #     return [pre + labels[0]]

    return ["".join(i) for i in itertools.product(pre, labels)]


add_bases()
add_kilogram()
add_derived_quantities()
add_core()


## add unofficial NIST units ## noqa
#######################################################################################################################

def add_extra_quantities():
    for entry in unit_extra.extra_quantities.values():
        ledger.add_unit(entry)


add_extra_quantities()


ledger.add_in_main_duplicates()