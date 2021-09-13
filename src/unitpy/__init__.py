import pkg_resources

from src.unitpy.ledger import Ledger
from src.unitpy.unit import Unit
from src.unitpy.quantity import Quantity
from src.unitpy.measurement import Measurement

ledger = Ledger()
U = Unit
Q = Quantity
M = Measurement

__all__ = ("ledger", "Unit", "Quantity", "Measurement", "U", "Q", "M")

# single-sourcing the package version
__version__ = pkg_resources.require("unitpy")[0].version

VERSION = __version__
__short_version__ = __version__.rpartition(".")[0]

