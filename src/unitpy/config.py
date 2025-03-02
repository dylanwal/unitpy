from __future__ import annotations

import enum

env_flag = False

try:
    from dotenv import dotenv_values
    env_flag = True
except ImportError:
    pass


def convert_string_to_number(value: str) -> int | float | None:
    try:
        value = float(value)
        value_int = int(value)
        if value_int == value:
            return value_int
        return value
    except ValueError:
        return None


def convert_string_to_bool(value: str) -> bool | None:
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    return None


type_converters = {
        'number': convert_string_to_number,
        'bool': convert_string_to_bool,
    }


def convert_string_to_types(value) -> int | float | bool | str:
    for converter in type_converters.values():
        new_value = converter(value)
        if new_value is not None:
            return new_value

    return value  # str


class Config:
    class StringFormat(enum.Enum):
        symbols = 0
        power = 1
        # latex = 2
        # html = 3

    def __init__(self, precision: int | None = None):
        """"""
        self.precision = precision
        self.format_symbols = Config.StringFormat.symbols
        self.integer_format_numerator_parenthesis = False
        self.integer_format_denominator_parenthesis = True
        self.abbr = False  # false is full word
        self.multiplication_seperator = " "  #  " " or " * "
        self.division_seperator = "/"

        if env_flag:
            self.get_config_from_env()

    def get_config_from_env(self):
        variables = self.__dict__
        config_ = {k.strip('unitpy_'): convert_string_to_types(v) for k, v in dotenv_values().items()}
        for k, v in config_.items():
            if k in variables:
                if k == "format_symbols":
                    if isinstance(v, int):
                        v = self.StringFormat(v)
                    else:
                        v = self.StringFormat[v]  # str
                setattr(self, k, v)


CONFIG = Config()
