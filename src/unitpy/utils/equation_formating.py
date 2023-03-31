
from unitpy.config import config


def equation_formater(dict_: dict) -> str:

    if config.units.format_symbols:
        string = format_with_symbols(dict_)
    else:
        string = format_with_power(dict_)

    return string


def format_with_power(dict_: dict) -> str:
    return "pp"


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
        string += "/" + format_integer_denominator(denominator)

    return string


def format_integer_numerator(numerator) -> str:
    string = config.units.multiplication_seperator.join(format_term(k, power) for k, power in numerator)

    if config.units.integer_format_numerator_parenthesis and len(numerator) > 1:
        string = "(" + string + ")"

    return string


def format_integer_denominator(denominator) -> str:
    string = config.units.multiplication_seperator.join(format_term(k, power * -1) for k, power in denominator)

    if config.units.integer_format_denominator_parenthesis and len(denominator) > 1:
        string = "(" + string + ")"

    return string


def format_term(key, power: int | float) -> str:
    if config.units.abbr:
        string = key.abbr
    else:
        string = key.label

    if power != 1:
        string += "**" + str(power)

    return string



