from __future__ import annotations


class Dimension:
    __slots__ = ("name", "abbr")

    def __init__(self, name: str, abbr: str):
        self.name = name
        self.abbr = abbr

    def __str__(self):
        return f"[{self.name}]"

    def __repr__(self):
        return f"[{self.abbr}]"


length = Dimension("length", "len")
time = Dimension("time", "time")
amount_of_substance = Dimension("amount_of_substance", "sub")
temperature = Dimension("temperature", "temp")
luminous_intensity = Dimension("luminous_intensity", "lum")
mass = Dimension("mass", "mass")


dimensions = (
    length, time, amount_of_substance, temperature, luminous_intensity, mass
)
