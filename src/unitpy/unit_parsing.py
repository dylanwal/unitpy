import re

from unitpy.ledger import ledger


class Parser:
    def __init__(self, expression):
        self.expression = expression
        self.pos = 0
        self.unit_dict = dict()

    def parse(self) -> dict[str, float | int]:
        result = self.parse_expression()
        if self.pos != len(self.expression):
            raise ValueError('Unexpected character at position ' + str(self.pos))
        return result

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
                res = self.parse_factor()
                add
            elif self.consume('/'):
                res = self.parse_factor()
                subb
            else:
                return result

    def parse_factor(self, neg: bool = False) -> dict[str, float | int]:
        result = self.parse_base()

        while True:
            if self.consume('^'):
                super_script = self.parse_base()
                if "number" not in super_script and len(super_script.keys()) != 1:
                    raise ValueError("power must be numbers.")

                self.add_to_unit_dict(result, -1 * super_script["number"])
            else:
                return result

    def add_to_unit_dict(self, dict_, value):
        for k, v in dict_:
            if unit in self.unit_dict:
                self.unit_dict[unit] += value
            else:
                self.unit_dict[unit] = value

    def parse_base(self) -> dict[str, float | int]:
        if self.consume('('):
            result = self.parse_expression()
            self.expect(')')
        elif self.is_number():
            result = dict(number=float(self.consume_regex(r'\d+(\.\d*)?')))
        elif self.is_variable():
            result = {self.parse_variable(): 1}
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

    def parse_variable(self):
        var_name = self.consume_regex(r'[a-zA-Z]')
        return ledger.get_unit(var_name)

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
        if match and self.expression[self.pos:] in ledger.ledger:
            return True
        return False
