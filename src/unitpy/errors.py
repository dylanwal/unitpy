
class UnitpyError(Exception):
    ...


class UnSupportedUnitError(UnitpyError):
    """ This error is raised when a unit is not supported."""
    ...


class AmbiguousUnitSymbolError(UnitpyError):
    """ This error is raised when a unit is corresponds to two or more supported units."""
    ...


class UnitDimensionError(UnitpyError):
    """ This error is raised when a mathematical operation is not supported between the two dimensions. """
    ...
