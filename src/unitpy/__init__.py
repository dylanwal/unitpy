import pkg_resources

from unitpy.definitions.ledger import ledger
from unitpy.unit import Unit
# from src.unitpy.quantity import Quantity
# from src.unitpy.measurement import Measurement

U = Unit
# Q = Quantity
# M = Measurement
#
# __all__ = ("ledger", "Unit", "Quantity", "Measurement", "U", "Q", "M", "u")

# single-sourcing the package version
__version__ = pkg_resources.require("unitpy")[0].version



