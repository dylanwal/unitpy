from __future__ import annotations

from unitpy.core import Unit, Quantity


def get_html(obj: Unit | Quantity) -> str:
    """ kilogram * meter / second ** 2 --> kilogram meter/second<sup>2</sup> """
    pass


def get_latex(obj: Unit | Quantity) -> str:
    """ kilogram * meter / second ** 2 --> \frac{\mathrm{kilogram} \cdot \mathrm{meter}}{\mathrm{second}^{2}} """
    pass
