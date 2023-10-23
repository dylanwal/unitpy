from inspect import signature
from itertools import chain

try:
    import numpy as np
except ImportError:
    raise ImportError("Must install numpy to use. `pip install numpy`")

from unitpy.core import Quantity, Unit

HANDLED_UFUNCS = {}
HANDLED_FUNCTIONS = {}


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def _get_first_input_units(args, kwargs=None) -> Unit:
    """Obtain the first valid unit from a collection of args and kwargs."""
    kwargs = kwargs or {}
    for arg in chain(args, kwargs.values()):
        if isinstance(arg, Quantity):
            return arg.unit
        # elif _is_sequence_with_quantity_elements(arg):
        #     return next(arg_i.units for arg_i in arg if isinstance(arg_i, Quantity))
    raise TypeError("Expected at least one Quantity; found none")


def convert_to_consistent_units(*args: Quantity, unit_: Unit, **kwargs):  # -> tuple[tuple[Quantity], dict]:
    if kwargs:
        kwargs = {k: v.to(unit_).v for k, v in kwargs.items()}
    return tuple(arg.to(unit_).v for arg in args), kwargs


def unwrap_and_wrap_consistent_units(*args):
    """Strip units from args while providing a rewrapping function.

    Returns the given args as parsed by convert_to_consistent_units assuming units of
    first arg with units, along with a wrapper to restore that unit to the output.

    """
    if all(not isinstance(arg, Quantity) for arg in args):
        return args, lambda x: x

    first_input_units = args[0].unit
    args, _ = convert_to_consistent_units(*args, unit_=first_input_units)
    return (
        args,
        lambda value: Quantity(value, first_input_units)
    )


def get_op_output_unit(unit_op: str, first_input_units: Unit, all_args=None, size=None) -> Unit:
    """Determine resulting unit from given operation.

    Options for `unit_op`:

    - "sum": `first_input_units`, unless non-multiplicative, which raises
      OffsetUnitCalculusError
    - "mul": product of all units in `all_args`
    - "delta": `first_input_units`, unless non-multiplicative, which uses delta version
    - "delta,div": like "delta", but divided by all units in `all_args` except the first
    - "div": unit of first argument in `all_args` (or dimensionless if not a Quantity) divided
      by all following units
    - "variance": square of `first_input_units`, unless non-multiplicative, which raises
      OffsetUnitCalculusError
    - "square": square of `first_input_units`
    - "sqrt": square root of `first_input_units`
    - "reciprocal": reciprocal of `first_input_units`
    - "size": `first_input_units` raised to the power of `size`
    - "invdiv": inverse of `div`, product of all following units divided by first argument unit

    Parameters
    ----------
    unit_op :

    first_input_units :

    all_args :
         (Default value = None)
    size :
         (Default value = None)

    Returns
    -------

    """
    all_args = all_args or []

    if unit_op == "sum":
        return first_input_units
    elif unit_op == "mul":
        product = first_input_units
        for x in all_args:
            if hasattr(x, "units"):
                product *= x.units
        return product
    elif unit_op == "delta":
        return first_input_units
    elif unit_op == "delta,div":
        product = first_input_units
        for x in all_args[1:]:
            if hasattr(x, "units"):
                product /= x.units
        return product
    elif unit_op == "div":
        # Start with first arg in numerator, all others in denominator
        product = first_input_units
        for x in all_args[1:]:
            if hasattr(x, "units"):
                product /= x.units
        return product
    elif unit_op == "variance":
        return first_input_units ** 2
    elif unit_op == "square":
        return first_input_units ** 2
    elif unit_op == "sqrt":
        return first_input_units ** 0.5
    elif unit_op == "cbrt":
        return first_input_units ** (1 / 3)
    elif unit_op == "reciprocal":
        return first_input_units ** -1
    elif unit_op == "size":
        if size is None:
            raise ValueError('size argument must be given when unit_op=="size"')
        return first_input_units ** size
    elif unit_op == "invdiv":
        # Start with first arg in numerator, all others in denominator
        product = first_input_units
        for x in all_args[1:]:
            if hasattr(x, "units"):
                product /= x.units
        return product ** -1

    raise ValueError("Output unit method {} not understood".format(unit_op))


def implements(numpy_func_string, func_type):
    """Register an __array_function__/__array_ufunc__ implementation for Quantity
    objects.

    """

    def decorator(func):
        if func_type == "function":
            HANDLED_FUNCTIONS[numpy_func_string] = func
        elif func_type == "ufunc":
            HANDLED_UFUNCS[numpy_func_string] = func
        else:
            raise ValueError("Invalid func_type {}".format(func_type))
        return func

    return decorator


def implement_func(func_type, func_str, input_units=None, output_unit=None):
    """Add default-behavior NumPy function/ufunc to the handled list.

    Parameters
    ----------
    func_type : str
        "function" for NumPy functions, "ufunc" for NumPy ufuncs
    func_str : str
        String representing the name of the NumPy function/ufunc to add
    input_units : pint.Unit or str or None
        Parameter to control how the function downcasts to magnitudes of arguments. If
        `pint.Unit`, converts all args and kwargs to this unit before downcasting to
        magnitude. If "all_consistent", converts all args and kwargs to the unit of the
        first Quantity in args and kwargs before downcasting to magnitude. If some
        other string, the string is parsed as a unit, and all args and kwargs are
        converted to that unit. If None, units are stripped without conversion.
    output_unit : pint.Unit or str or None
        Parameter to control the unit of the output. If `pint.Unit`, output is wrapped
        with that unit. If "match_input", output is wrapped with the unit of the first
        Quantity in args and kwargs. If a string representing a unit operation defined
        in `get_op_output_unit`, output is wrapped by the unit determined by
        `get_op_output_unit`. If some other string, the string is parsed as a unit,
        which becomes the unit of the output. If None, the bare magnitude is returned.


    """
    # If NumPy is not available, do not attempt implement that which does not exist
    if np is None:
        return

    # Handle functions in submodules
    func_str_split = func_str.split(".")
    func = getattr(np, func_str_split[0], None)
    # If the function is not available, do not attempt to implement it
    if func is None:
        return
    for func_str_piece in func_str_split[1:]:
        func = getattr(func, func_str_piece)

    @implements(func_str, func_type)
    def implementation(*args, **kwargs):
        first_input_units = _get_first_input_units(args, kwargs)
        if input_units == "all_consistent":
            # Match all input args/kwargs to same units
            stripped_args, stripped_kwargs = convert_to_consistent_units(
                *args, unit_=first_input_units, **kwargs
            )
        else:
            pre_calc_units = first_input_units

            # Match all input args/kwargs to input_units, or if input_units is None,
            # simply strip units
            stripped_args, stripped_kwargs = convert_to_consistent_units(
                *args, unit_=pre_calc_units, **kwargs
            )

        # Determine result through base numpy function on stripped arguments
        result_magnitude = func(*stripped_args, **stripped_kwargs)

        if output_unit is None:
            # Short circuit and return magnitude alone
            return result_magnitude
        elif output_unit == "match_input":
            result_unit = first_input_units
        elif output_unit in [
            "sum",
            "mul",
            "delta",
            "delta,div",
            "div",
            "invdiv",
            "variance",
            "square",
            "sqrt",
            "cbrt",
            "reciprocal",
            "size",
        ]:
            result_unit = get_op_output_unit(
                output_unit, first_input_units, tuple(chain(args, kwargs.values()))
            )
        else:
            result_unit = output_unit

        return Quantity(result_magnitude, result_unit)


"""
Define ufunc behavior collections.
"""
strip_unit_input_output_ufuncs = ["isnan", "isinf", "isfinite", "signbit", "sign"]
matching_input_bare_output_ufuncs = [
    "equal",
    "greater",
    "greater_equal",
    "less",
    "less_equal",
    "not_equal",
]
matching_input_set_units_output_ufuncs = {"arctan2": "radian"}
set_units_ufuncs = {
    "cumprod": ("", ""),
    "arccos": ("", "radian"),
    "arcsin": ("", "radian"),
    "arctan": ("", "radian"),
    "arccosh": ("", "radian"),
    "arcsinh": ("", "radian"),
    "arctanh": ("", "radian"),
    "exp": ("", ""),
    "expm1": ("", ""),
    "exp2": ("", ""),
    "log": ("", ""),
    "log10": ("", ""),
    "log1p": ("", ""),
    "log2": ("", ""),
    "sin": ("radian", ""),
    "cos": ("radian", ""),
    "tan": ("radian", ""),
    "sinh": ("radian", ""),
    "cosh": ("radian", ""),
    "tanh": ("radian", ""),
    "radians": ("degree", "radian"),
    "degrees": ("radian", "degree"),
    "deg2rad": ("degree", "radian"),
    "rad2deg": ("radian", "degree"),
    "logaddexp": ("", ""),
    "logaddexp2": ("", ""),
}

matching_input_copy_units_output_ufuncs = [
    "compress",
    "conj",
    "conjugate",
    "copy",
    "diagonal",
    "max",
    "mean",
    "min",
    "ptp",
    "ravel",
    "repeat",
    "reshape",
    "round",
    "squeeze",
    "swapaxes",
    "take",
    "trace",
    "transpose",
    "ceil",
    "floor",
    "hypot",
    "rint",
    "copysign",
    "nextafter",
    "trunc",
    "absolute",
    "negative",
    "maximum",
    "minimum",
    "fabs",
]
copy_units_output_ufuncs = ["ldexp", "fmod", "mod", "remainder"]
op_units_output_ufuncs = {
    "var": "square",
    "multiply": "mul",
    "true_divide": "div",
    "divide": "div",
    "floor_divide": "div",
    "sqrt": "sqrt",
    "cbrt": "cbrt",
    "square": "square",
    "reciprocal": "reciprocal",
    "std": "sum",
    "sum": "sum",
    "cumsum": "sum",
    "matmul": "mul",
}

# Perform the standard ufunc implementations based on behavior collections

for ufunc_str in strip_unit_input_output_ufuncs:
    # Ignore units
    implement_func("ufunc", ufunc_str, input_units=None, output_unit=None)

for ufunc_str in matching_input_bare_output_ufuncs:
    # Require all inputs to match units, but output base ndarray/duck array
    implement_func("ufunc", ufunc_str, input_units="all_consistent", output_unit=None)

for ufunc_str, out_unit in matching_input_set_units_output_ufuncs.items():
    # Require all inputs to match units, but output in specified unit
    implement_func(
        "ufunc", ufunc_str, input_units="all_consistent", output_unit=out_unit
    )

# for ufunc_str, (in_unit, out_unit) in set_units_ufuncs.items():
#     # Require inputs in specified unit, and output in specified unit
#     implement_func("ufunc", ufunc_str, input_units=in_unit, output_unit=out_unit)

for ufunc_str in matching_input_copy_units_output_ufuncs:
    # Require all inputs to match units, and output as first unit in arguments
    implement_func(
        "ufunc", ufunc_str, input_units="all_consistent", output_unit="match_input"
    )

for ufunc_str in copy_units_output_ufuncs:
    # Output as first unit in arguments, but do not convert inputs
    implement_func("ufunc", ufunc_str, input_units=None, output_unit="match_input")

for ufunc_str, unit_op in op_units_output_ufuncs.items():
    implement_func("ufunc", ufunc_str, input_units=None, output_unit=unit_op)


# Define custom ufunc implementations for atypical cases


@implements("modf", "ufunc")
def _modf(x, *args, **kwargs):
    (x,), output_wrap = unwrap_and_wrap_consistent_units(x)
    return tuple(output_wrap(y) for y in np.modf(x, *args, **kwargs))


@implements("frexp", "ufunc")
def _frexp(x, *args, **kwargs):
    (x,), output_wrap = unwrap_and_wrap_consistent_units(x)
    mantissa, exponent = np.frexp(x, *args, **kwargs)
    return output_wrap(mantissa), exponent


@implements("power", "ufunc")
def _power(x1, x2):
    if isinstance(x1, Quantity):
        return x1 ** x2
    else:
        return x2.__rpow__(x1)


@implements("add", "ufunc")
def _add(x1, x2, *args, **kwargs):
    (x1, x2), output_wrap = unwrap_and_wrap_consistent_units(x1, x2)
    return output_wrap(np.add(x1, x2, *args, **kwargs))


@implements("subtract", "ufunc")
def _subtract(x1, x2, *args, **kwargs):
    (x1, x2), output_wrap = unwrap_and_wrap_consistent_units(x1, x2)
    return output_wrap(np.subtract(x1, x2, *args, **kwargs))


# Define custom function implementations


@implements("meshgrid", "function")
def _meshgrid(*xi, **kwargs):
    # Simply need to map input units to onto list of outputs
    input_units = (x.units for x in xi)
    res = np.meshgrid(*(x.m for x in xi), **kwargs)
    return [out * unit for out, unit in zip(res, input_units)]


@implements("full_like", "function")
def _full_like(a, fill_value, dtype=None, order="K", subok=True, shape=None):
    # Make full_like by multiplying with array from ones_like in a
    # non-multiplicative-unit-safe way
    if hasattr(fill_value, "_REGISTRY"):
        return fill_value._REGISTRY.Quantity(
            (
                    np.ones_like(a, dtype=dtype, order=order, subok=subok, shape=shape)
                    * fill_value.m
            ),
            fill_value.units,
        )
    else:
        return (
                np.ones_like(a, dtype=dtype, order=order, subok=subok, shape=shape)
                * fill_value
        )


@implements("interp", "function")
def _interp(x, xp, fp, left=None, right=None, period=None):
    # Need to handle x and y units separately
    (x, xp, period), _ = unwrap_and_wrap_consistent_units(x, xp, period)
    (fp, right, left), output_wrap = unwrap_and_wrap_consistent_units(fp, left, right)
    return output_wrap(np.interp(x, xp, fp, left=left, right=right, period=period))


@implements("where", "function")
def _where(condition, *args):
    args, output_wrap = unwrap_and_wrap_consistent_units(*args)
    return output_wrap(np.where(condition, *args))


@implements("concatenate", "function")
def _concatenate(sequence, *args, **kwargs):
    sequence, output_wrap = unwrap_and_wrap_consistent_units(*sequence)
    return output_wrap(np.concatenate(sequence, *args, **kwargs))


@implements("stack", "function")
def _stack(arrays, *args, **kwargs):
    arrays, output_wrap = unwrap_and_wrap_consistent_units(*arrays)
    return output_wrap(np.stack(arrays, *args, **kwargs))


@implements("unwrap", "function")
def _unwrap(p, discont=None, axis=-1):
    # np.unwrap only dispatches over p argument, so assume it is a Quantity
    discont = np.pi if discont is None else discont
    return p._REGISTRY.Quantity(np.unwrap(p.m_as("rad"), discont, axis=axis), "rad").to(
        p.units
    )


# @implements("copyto", "function")
# def _copyto(dst, src, casting="same_kind", where=True):
#     if isinstance(dst, Quantity):
#         if isinstance(src, Quantity):
#             src = src.m_as(dst.units)
#         np.copyto(dst.v, src, casting=casting, where=where)
#     else:
#         warnings.warn(
#             "The unit of the quantity is stripped when copying to non-quantity",
#             UnitStrippedWarning,
#             stacklevel=2,
#         )
#         np.copyto(dst, src.m, casting=casting, where=where)


# @implements("einsum", "function")
# def _einsum(subscripts, *operands, **kwargs):
#     operand_magnitudes, _ = convert_to_consistent_units(*operands, pre_calc_units=None)
#     output_unit = get_op_output_unit("mul", _get_first_input_units(operands), operands)
#     return np.einsum(subscripts, *operand_magnitudes, **kwargs) * output_unit


@implements("isin", "function")
def _isin(element: Quantity, test_elements: Quantity, assume_unique=False, invert=False):
    if not isinstance(element, Quantity):
        raise ValueError(
            "Cannot test if unit-aware elements are in not-unit-aware array"
        )

    if not isinstance(test_elements, Quantity) or not isinstance(test_elements.v, np.ndarray):
        raise ValueError("test elements must be a np.ndarray")

    return np.isin(element.base_value, test_elements.base_value, assume_unique=assume_unique, invert=invert)

    # if isinstance(test_elements, Quantity):
    #     try:
    #         test_elements = test_elements.to(element.units).value
    #     except ValueError:
    #         # Incompatible unit test elements cannot be in element
    #         return np.full(element.shape, False)
    # elif _is_sequence_with_quantity_elements(test_elements):
    #     compatible_test_elements = []
    #     for test_element in test_elements:
    #         if not isinstance(test_element, Quantity):
    #             pass
    #         try:
    #             compatible_test_elements.append(test_element.m_as(element.units))
    #         except ValueError:
    #             # Incompatible unit test elements cannot be in element, but others in
    #             # sequence may
    #             pass
    #     test_elements = compatible_test_elements
    # else:
    #     # Consider non-quantity like dimensionless quantity
    #     if not element.dimensionless:
    #         # Unit do not match, so all false
    #         return np.full(element.shape, False)
    #     else:
    #         # Convert to units of element
    #         element._REGISTRY.Quantity(test_elements).m_as(element.units)
    #
    # return np.isin(element.v, test_elements, assume_unique=assume_unique, invert=invert)


@implements("pad", "function")
def _pad(array, pad_width, mode="constant", **kwargs):
    def _recursive_convert(arg, unit):
        if is_iterable(arg):
            return tuple(_recursive_convert(a, unit=unit) for a in arg)
        elif not isinstance(arg, Quantity):
            if arg == 0 or np.isnan(arg):
                arg = unit._REGISTRY.Quantity(arg, unit)
            else:
                arg = unit._REGISTRY.Quantity(arg, "dimensionless")

        return arg.m_as(unit)

    # pad only dispatches on array argument, so we know it is a Quantity
    units = array.units

    # Handle flexible constant_values and end_values, converting to units if Quantity
    # and ignoring if not
    for key in ("constant_values", "end_values"):
        if key in kwargs:
            kwargs[key] = _recursive_convert(kwargs[key], units)

    return units._REGISTRY.Quantity(
        np.pad(array._magnitude, pad_width, mode=mode, **kwargs), units
    )


@implements("any", "function")
def _any(a, *args, **kwargs):
    # Only valid when multiplicative unit/no offset
    if a._is_multiplicative:
        return np.any(a._magnitude, *args, **kwargs)
    else:
        raise ValueError("Boolean value of Quantity with offset unit is ambiguous.")


@implements("all", "function")
def _all(a, *args, **kwargs):
    # Only valid when multiplicative unit/no offset
    if a._is_multiplicative:
        return np.all(a._magnitude, *args, **kwargs)
    else:
        raise ValueError("Boolean value of Quantity with offset unit is ambiguous.")


@implements("prod", "function")
def _prod(a, *args, **kwargs):
    arg_names = ("axis", "dtype", "out", "keepdims", "initial", "where")
    all_kwargs = dict(**dict(zip(arg_names, args)), **kwargs)
    axis = all_kwargs.get("axis", None)
    where = all_kwargs.get("where", None)

    registry = a.units._REGISTRY

    if axis is not None and where is not None:
        _, where_ = np.broadcast_arrays(a._magnitude, where)
        exponents = np.unique(np.sum(where_, axis=axis))
        if len(exponents) == 1 or (len(exponents) == 2 and 0 in exponents):
            units = a.units ** np.max(exponents)
        else:
            units = registry.dimensionless
            a = a.to(units)
    elif axis is not None:
        units = a.units ** a.shape[axis]
    elif where is not None:
        exponent = np.sum(where)
        units = a.units ** exponent
    else:
        units = a.units ** a.size

    result = np.prod(a._magnitude, *args, **kwargs)

    return registry.Quantity(result, units)


# Implement simple matching-unit or stripped-unit functions based on signature


def implement_consistent_units_by_argument(func_str, unit_arguments, wrap_output=True):
    # If NumPy is not available, do not attempt implement that which does not exist
    if np is None:
        return

    if "." not in func_str:
        func = getattr(np, func_str, None)
    else:
        parts = func_str.split(".")
        module = np
        for part in parts[:-1]:
            module = getattr(module, part, None)
        func = getattr(module, parts[-1], None)

    # if NumPy does not implement it, do not implement it either
    if func is None:
        return

    @implements(func_str, "function")
    def implementation(*args, **kwargs):
        # Bind given arguments to the NumPy function signature
        bound_args = signature(func).bind(*args, **kwargs)

        # Skip unit arguments that are supplied as None
        valid_unit_arguments = [
            label
            for label in unit_arguments
            if label in bound_args.arguments and bound_args.arguments[label] is not None
        ]

        # Unwrap valid unit arguments, ensure consistency, and obtain output wrapper
        unwrapped_unit_args, output_wrap = unwrap_and_wrap_consistent_units(
            *(bound_args.arguments[label] for label in valid_unit_arguments)
        )

        # Call NumPy function with updated arguments
        for i, unwrapped_unit_arg in enumerate(unwrapped_unit_args):
            bound_args.arguments[valid_unit_arguments[i]] = unwrapped_unit_arg
        ret = func(*bound_args.args, **bound_args.kwargs)

        # Conditionally wrap output
        if wrap_output:
            return output_wrap(ret)
        else:
            return ret


for func_str, unit_arguments, wrap_output in [
    ("expand_dims", "a", True),
    ("squeeze", "a", True),
    ("rollaxis", "a", True),
    ("moveaxis", "a", True),
    ("around", "a", True),
    ("diagonal", "a", True),
    ("mean", "a", True),
    ("ptp", "a", True),
    ("ravel", "a", True),
    ("round_", "a", True),
    ("sort", "a", True),
    ("median", "a", True),
    ("nanmedian", "a", True),
    ("transpose", "a", True),
    ("copy", "a", True),
    ("average", "a", True),
    ("nanmean", "a", True),
    ("swapaxes", "a", True),
    ("nanmin", "a", True),
    ("nanmax", "a", True),
    ("percentile", "a", True),
    ("nanpercentile", "a", True),
    ("quantile", "a", True),
    ("nanquantile", "a", True),
    ("flip", "m", True),
    ("fix", "x", True),
    ("trim_zeros", ["filt"], True),
    ("broadcast_to", ["array"], True),
    ("amax", ["a", "initial"], True),
    ("amin", ["a", "initial"], True),
    ("searchsorted", ["a", "v"], False),
    ("isclose", ["a", "b"], False),
    ("nan_to_num", ["x", "nan", "posinf", "neginf"], True),
    ("clip", ["a", "a_min", "a_max"], True),
    ("append", ["arr", "values"], True),
    ("compress", "a", True),
    ("linspace", ["start", "stop"], True),
    ("tile", "A", True),
    ("lib.stride_tricks.sliding_window_view", "x", True),
    ("rot90", "m", True),
    ("insert", ["arr", "values"], True),
    ("resize", "a", True),
    ("reshape", "a", True),
    ("allclose", ["a", "b"], False),
    ("intersect1d", ["ar1", "ar2"], True),
]:
    implement_consistent_units_by_argument(func_str, unit_arguments, wrap_output)


# Handle atleast_nd functions


# def implement_atleast_nd(func_str):
#     # If NumPy is not available, do not attempt implement that which does not exist
#     if np is None:
#         return
#
#     func = getattr(np, func_str)
#
#     @implements(func_str, "function")
#     def implementation(*arrays):
#         stripped_arrays, _ = convert_to_consistent_units(*arrays)
#         arrays_magnitude = func(*stripped_arrays)
#         if len(arrays) > 1:
#             return [
#                 array_magnitude
#                 if not hasattr(original, "_REGISTRY")
#                 else original._REGISTRY.Quantity(array_magnitude, original.units)
#                 for array_magnitude, original in zip(arrays_magnitude, arrays)
#             ]
#         else:
#             output_unit = arrays[0].units
#             return output_unit._REGISTRY.Quantity(arrays_magnitude, output_unit)
#
#
# for func_str in ["atleast_1d", "atleast_2d", "atleast_3d"]:
#     implement_atleast_nd(func_str)


# # Handle cumulative products (which must be dimensionless for consistent units across
# # output array)
# def implement_single_dimensionless_argument_func(func_str):
#     # If NumPy is not available, do not attempt implement that which does not exist
#     if np is None:
#         return
#
#     func = getattr(np, func_str)
#
#     @implements(func_str, "function")
#     def implementation(a, *args, **kwargs):
#         (a_stripped,), _ = convert_to_consistent_units(
#             a, unit_=a._REGISTRY.parse_units("dimensionless")
#         )
#         return a._REGISTRY.Quantity(func(a_stripped, *args, **kwargs))
#
#
# for func_str in ["cumprod", "cumproduct", "nancumprod"]:
#     implement_single_dimensionless_argument_func(func_str)

# Handle single-argument consistent unit functions
for func_str in ["block", "hstack", "vstack", "dstack", "column_stack"]:
    implement_func(
        "function", func_str, input_units="all_consistent", output_unit="match_input"
    )

# Handle functions that ignore units on input and output
for func_str in [
    "size",
    "isreal",
    "iscomplex",
    "shape",
    "ones_like",
    "zeros_like",
    "empty_like",
    "argsort",
    "argmin",
    "argmax",
    "alen",
    "ndim",
    "nanargmax",
    "nanargmin",
    "count_nonzero",
    "nonzero",
    "result_type",
]:
    implement_func("function", func_str, input_units=None, output_unit=None)

# Handle functions with output unit defined by operation
for func_str in ["std", "nanstd", "sum", "nansum", "cumsum", "nancumsum"]:
    implement_func("function", func_str, input_units=None, output_unit="sum")
for func_str in ["cross", "trapz", "dot"]:
    implement_func("function", func_str, input_units=None, output_unit="mul")
for func_str in ["diff", "ediff1d"]:
    implement_func("function", func_str, input_units=None, output_unit="delta")
for func_str in ["gradient"]:
    implement_func("function", func_str, input_units=None, output_unit="delta,div")
for func_str in ["linalg.solve"]:
    implement_func("function", func_str, input_units=None, output_unit="invdiv")
for func_str in ["var", "nanvar"]:
    implement_func("function", func_str, input_units=None, output_unit="variance")


def numpy_wrap(func_type, func, args, kwargs, types):
    """Return the result from a NumPy function/ufunc as wrapped by Pint."""

    if func_type == "function":
        handled = HANDLED_FUNCTIONS
        # Need to handle functions in submodules
        name = ".".join(func.__module__.split(".")[1:] + [func.__name__])
    elif func_type == "ufunc":
        handled = HANDLED_UFUNCS
        # ufuncs do not have func.__module__
        name = func.__name__
    else:
        raise ValueError("Invalid func_type {}".format(func_type))

    if name not in handled:
        raise NotImplementedError("Not Implemented")
    return handled[name](*args, **kwargs)
