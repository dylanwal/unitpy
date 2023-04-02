from __future__ import annotations

import unitpy.definitions.dimensions as dim_
import unitpy.definitions.unit_base as base
import unitpy.definitions.prefix as prefix_


class Entry:
    """
    representation of a fundamental unit

    """
    __slots__ = ("label", 'abbr', 'base_unit', "_multiplier", "offset", "prefix", "additional_labels")

    def __init__(self,
                 label: str,
                 abbr: str | None,
                 base_unit: base.BaseSet,
                 multiplier: int | float,
                 offset: int | float = 0,
                 prefix: prefix_.Prefix = None,
                 additional_labels: list[str, ...] = None,
                 ):
        self.label = label
        self.abbr = abbr
        self.prefix = prefix
        self.additional_labels = additional_labels
        self.base_unit = base_unit
        self._multiplier = multiplier
        self.offset = offset if offset is not None else 0

    def __str__(self):
        return self.label

    def __repr__(self):
        return f"Entry({self.label}, {self.abbr}, {self.prefix}, {self.base_unit})"

    def details(self):
        text = ""
        text = self.label


    @property
    def multiplier(self) -> int | float:
        if self.prefix:
            return self.prefix.multiplier * self._multiplier
        return self._multiplier

    @property
    def dimensionality(self) -> dim_.Dimension:
        return self.base_unit.dimensionality
