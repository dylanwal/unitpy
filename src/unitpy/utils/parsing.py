from __future__ import annotations

import re

from unitpy.definitions.ledger import ledger
from unitpy.core import Unit, Quantity


def apply_multiplier(dict_, multiplier: int | float):
    for k in dict_:
        value = multiplier * dict_[k]
        dict_[k] = value


def add_to_unit_dict(dict1, dict2):
    for k in dict2:
        if k in dict1:
            dict1[k] += dict2[k]
        else:
            dict1[k] = dict2[k]


def parse_quantity(quantity: str) -> Quantity:
    parser = Parser(quantity)
    result = parser.parse()
    if not isinstance(result, Quantity):
        raise ValueError(f"Provided string is not a quantity: {quantity}")
    return result


def parse_unit(unit: str) -> Unit:
    parser = Parser(unit)
    result = parser.parse()
    if not isinstance(result, Unit):
        raise ValueError(f"Provided string is not a quantity: {unit}")
    return result


def parse_base(unit: str, symbols: set[str, ...]) -> dict[str, float | int]:
    pass
    # parser = Parser(unit, symbols)
    # return parser.parse()


class Parser:
    def __init__(self, expression: str):
        self.expression = expression
        self.pos = 0

    def parse(self) -> int | float | Unit | Quantity:
        self.syntax_fix()
        result = self.parse_expression()
        if self.pos != len(self.expression):
            raise ValueError('Unexpected character at position ' + str(self.pos))
        return result

    def syntax_fix(self):
        self.expression = self.expression.replace("   ", " ")
        self.expression = self.expression.replace("  ", " ")
        self.expression = self.expression.replace("**", "^")
        self.expression = re.sub(r'(?<=[a-zA-Z0-9]) +(?=[a-zA-Z0-9])', "*", self.expression)
        self.expression = self.expression.replace(" ", "")
        # self.expression = self.expression.replace(" per ", "/")
        # self.expression = self.expression.replace("squared", "^2")
        # self.expression = self.expression.replace("cubed", "^3")

    def parse_expression(self) -> int | float | Unit | Quantity:
        result = self.parse_term()
        while True:
            if self.consume('+'):
                result += self.parse_term()
            elif self.consume('-'):
                result -= self.parse_term()
            else:
                return result

    def parse_term(self) -> int | float | Unit | Quantity:
        result = self.parse_factor()
        while True:
            if self.consume('*'):
                result *= self.parse_factor()
            elif self.consume('/'):
                result /= self.parse_factor()
            else:
                return result

    def parse_factor(self) -> int | float | Unit | Quantity:
        result = self.parse_base()

        while True:
            if self.consume('^'):
                super_script = self.parse_base()
                if not (isinstance(super_script, int) or isinstance(super_script, float)):
                    raise ValueError("Power must be numbers.")

                result = result**super_script
            else:
                return result

    def parse_base(self) -> int | float | Unit | Quantity:
        if self.consume('('):
            result = self.parse_expression()
            self.expect(')')
            return result

        num = self.get_number()
        if num:
            return num

        unit = self.get_unit()
        if unit is not None:
            return unit

        raise ValueError('Unexpected character at position ' + str(self.pos) +
                         f"\ntext: {self.expression}\n      {' '*self.pos}^")

    def consume(self, char: str):
        if self.pos < len(self.expression) and self.expression[self.pos] == char:
            self.pos += 1
            return True
        else:
            return False

    def expect(self, char: str):
        if not self.consume(char):
            raise ValueError('Expected "' + char + '" at position ' + str(self.pos))

    def get_number(self) -> int | float | None:
        match = re.match(r'-?\d+(\.\d*)?', self.expression[self.pos:])
        if match:
            self.pos += match.end()
            num = float(match.group(0))
            if num.is_integer():
                num = int(num)
            return num

        return None

    def get_unit(self) -> Unit | None:
        match = re.match(r'[a-zA-Z]+', self.expression[self.pos:])
        if match:
            value = self.expression[self.pos:self.pos+match.end()]
            if value in ledger:
                self.pos += match.end()
                return Unit({ledger.get_entry(value): 1})

        return None
