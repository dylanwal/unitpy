import pkg_resources

from unitpy.config import CONFIG
import unitpy.errors as errors
from unitpy.definitions.ledger import ledger
from unitpy.core import Unit, Quantity

U = Unit
Q = Quantity
# M = Measurement

__all__ = ("Unit", "Quantity", "U", "Q")

# single-sourcing the package version
__version__ = pkg_resources.require("unitpy")[0].version
