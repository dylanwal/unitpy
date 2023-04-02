import re


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


def parse_quantity(quantity, symbols: set[str, ...]) -> tuple[int | float, dict[str, float | int]]:
    result = parse_unit(quantity, symbols)
    return result.pop("number"), result


def parse_unit(unit: str, symbols: set[str, ...]) -> dict[str, float | int]:
    parser = Parser(unit, symbols)
    return parser.parse()


def parse_base(unit: str, symbols: set[str, ...]) -> dict[str, float | int]:
    parser = Parser(unit, symbols)
    return parser.parse()


class Parser:
    def __init__(self, expression: str, symbols: set[str, ...]):
        self.expression = expression
        self.symbols = symbols
        self.pos = 0

    def parse(self) -> dict[str, float | int]:
        self.syntax_fix()
        result = self.parse_expression()
        if self.pos != len(self.expression):
            raise ValueError('Unexpected character at position ' + str(self.pos))
        return result

    def syntax_fix(self):
        self.expression = self.expression.replace("   ", " ")
        self.expression = self.expression.replace("  ", " ")
        self.expression = self.expression.replace(" ", "*")
        self.expression = self.expression.replace("**", "^")
        # self.expression = self.expression.replace(" per ", "/")
        # self.expression = self.expression.replace("squared", "^2")
        # self.expression = self.expression.replace("cubed", "^3")

    def parse_expression(self) -> dict[str, float | int]:
        result = self.parse_term()
        while True:
            if self.consume('+'):
                result += self.parse_term()
            elif self.consume('-'):
                result -= self.parse_term()
            else:
                return result

    def parse_term(self) -> dict[str, float | int]:
        result = self.parse_factor()
        while True:
            if self.consume('*'):
                result_ = self.parse_factor()
                add_to_unit_dict(result, result_)
            elif self.consume('/'):
                result_ = self.parse_factor()
                apply_multiplier(result_, -1)
                add_to_unit_dict(result, result_)
            else:
                return result

    def parse_factor(self) -> dict[str, float | int]:
        result = self.parse_base()

        while True:
            if self.consume('^'):
                super_script = self.parse_base()
                if "number" not in super_script and len(super_script.keys()) != 1:
                    raise ValueError("power must be numbers.")

                apply_multiplier(result, super_script["number"])
            else:
                return result

    def parse_base(self) -> dict[str, float | int]:
        if self.consume('('):
            result = self.parse_expression()
            self.expect(')')
        elif self.is_number():
            num = float(self.consume_regex(r'\d+(\.\d*)?'))
            if num.is_integer():
                num = int(num)
            result = dict(number=num)
        elif self.is_variable():
            result = {self.consume_regex(r'[a-zA-Z]+'): 1}
        else:
            raise ValueError('Unexpected character at position ' + str(self.pos))

        return result

    # def parse_metric_unit(self):
    #     result = {}
    #     while True:
    #         if self.consume_regex(r'[a-z]'):
    #             unit = self.expression[self.pos - 1]
    #             if unit in metric_units:
    #                 result[unit] = metric_units[unit]
    #             else:
    #                 raise ValueError('Unexpected metric unit "' + unit + '" at position ' + str(self.pos - 1))
    #         elif self.consume('^'):
    #             power = int(self.consume_regex(r'\d+'))
    #             for unit in result.keys():
    #                 result[unit] *= power
    #         else:
    #             return result

    def parse_operator(self):
        if self.consume('+'):
            return '+'
        elif self.consume('-'):
            return '-'
        elif self.consume('*'):
            return '*'
        elif self.consume('/'):
            return '/'
        elif self.consume('^'):
            return '^'
        else:
            raise ValueError('Expected an operator at position ' + str(self.pos))

    def consume(self, char):
        if self.pos < len(self.expression) and self.expression[self.pos] == char:
            self.pos += 1
            return True
        else:
            return False

    def consume_regex(self, pattern):
        match = re.match(pattern, self.expression[self.pos:])
        if match:
            self.pos += match.end()
            return match.group(0)
        else:
            raise ValueError('Expected a pattern at position ' + str(self.pos))

    def expect(self, char):
        if not self.consume(char):
            raise ValueError('Expected "' + char + '" at position ' + str(self.pos))

    def is_number(self):
        return re.match(r'\d+(\.\d*)?', self.expression[self.pos:])

    def is_variable(self):
        match = re.match(r'[a-zA-Z]+', self.expression[self.pos:])
        if match and self.expression[self.pos:self.pos+match.end()] in self.symbols:
            return True
        return False
