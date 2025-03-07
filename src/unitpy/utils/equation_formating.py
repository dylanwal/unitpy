from __future__ import annotations

from unitpy.config import CONFIG


def equation_formater(dict_: dict[str, int | float]) -> str:
    if CONFIG.format_symbols == CONFIG.StringFormat.symbols:
        string = format_with_symbols(dict_)
    elif CONFIG.format_symbols == CONFIG.StringFormat.power:
        string = format_with_power(dict_)
    else:
        raise ValueError("Invalid value for 'CONFIG.format_symbols'.")

    return string


def format_with_power(dict_: dict[str, int | float]) -> str:
    return CONFIG.multiplication_seperator.join([f"{k}**{v}" for k, v in dict_.items() if v != 0])


def format_with_symbols(dict_: dict) -> str:
    numerator = []
    denominator = []
    for k, v in dict_.items():
        if v >= 0:
            numerator.append((k, v))
        else:
            denominator.append((k, v))

    if numerator:
        string = format_integer_numerator(numerator)
    else:
        return format_with_power(dict_)

    if denominator:
        string += CONFIG.division_seperator + format_integer_denominator(denominator)

    return string


def format_integer_numerator(numerator) -> str:
    string = CONFIG.multiplication_seperator.join(format_term(k, power) for k, power in numerator if power != 0)

    if CONFIG.integer_format_numerator_parenthesis and len(numerator) > 1:
        string = "(" + string + ")"

    if string == "":
        string = "1"

    return string


def format_integer_denominator(denominator) -> str:
    string = CONFIG.multiplication_seperator.join(format_term(k, -1 * power) for k, power in denominator if
                                                  power != 0)

    if CONFIG.integer_format_denominator_parenthesis and len(denominator) > 1:
        string = "(" + string + ")"

    return string


def format_term(label: str, power: int | float) -> str:
    if power == 0:
        return ""

    if abs(power) == 1:
        return label

    return f"{label}**{power}"
