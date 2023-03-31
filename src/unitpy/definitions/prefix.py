from __future__ import annotations


class Prefix:
    """

    Only applied to base and derived units and metric
    """
    __slots__ = ("multiplier", "name", "abbr")

    def __init__(self, name: str, multiplier: float, abbr: tuple[str, ...]):
        self.name = name
        self.multiplier = multiplier
        self.abbr = abbr

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


yocto = Prefix("yocto", 1e-24, ("y",))
zepto = Prefix("zepto", 1e-21, ("z",))
atto = Prefix("atto", 1e-18, ("a",))
femto = Prefix("femto", 1e-15, ("f",))
pico = Prefix("pico", 1e-12, ("p",))
nano = Prefix("nano", 1e-9, ("n",))
micro = Prefix("micro", 1e-6, ("u", "µ"))
milli = Prefix("milli", 1e-3, ("m",))
centi = Prefix("centi", 1e-2, ("c",))
deci = Prefix("deci", 1e-1, ("d",))
deca = Prefix("deca", 1e1, ("da",))
hecto = Prefix("hecto", 1e2, ("h",))
kilo = Prefix("kilo", 1e3, ("k",))
mega = Prefix("mega", 1e6, ("M",))
giga = Prefix("giga", 1e9, ("G",))
tera = Prefix("tera", 1e12, ("T",))
peta = Prefix("peta", 1e15, ("P",))
exa = Prefix("exa", 1e18, ("E",))
zetta = Prefix("zetta", 1e21, ("Z",))
yotta = Prefix("yotta", 1e24, ("Y",))

prefixes = {
    "yocto": yocto,
    "zepto": zepto,
    "atto": atto,
    "femto": femto,
    "pico": pico,
    "nano": nano,
    "micro": micro,
    "milli": milli,
    "centi": centi,
    "deci": deci,
    "deca": deca,
    "hecto": hecto,
    "kilo": kilo,
    "mega": mega,
    "giga": giga,
    "tera": tera,
    "peta": peta,
    "exa": exa,
    "zetta": zetta,
    "yotta": yotta,
}
