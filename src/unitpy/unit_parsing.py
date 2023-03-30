import re

from unitpy.ledger import ledger


class Parser:
    """
    The parser uses a recursive descent parsing technique, where each method corresponds to a
    nonterminal symbol in the grammar of the algebraic equation language. The parse_expression()
    method corresponds to the top-level expression, which can be a sum or difference of terms.
    The parse_term() method corresponds to a term, which can be a product or quotient of factors.
    The parse_factor() method corresponds to a factor, which can be a base raised to a power.
    The parse_base() method corresponds to a base, which can be a number, a variable, or a
    parenthesized expression. The parse_operator() method corresponds to an operator,
    which can be +, -, *, /, or ^.

    """
    def __init__(self, expr):
        self.expr = expr
        self.pos = 0
        self.variables = {}

    def parse(self):
        """
        main method of the parser
        Returns
        -------

        """

        result = self.parse_expression()
        if self.pos != len(self.expr):
            raise ValueError('Invalid input')
        return result

    def parse_expression(self):
        """
        parses a sum or difference of terms

        Returns
        -------

        """
        terms = [self.parse_term()]
        while self.pos < len(self.expr):
            op = self.parse_operator()
            term = self.parse_term()
            if op == '+':
                terms.append(term)
            elif op == '-':
                terms.append(-term)
            else:
                raise ValueError('Invalid operator')
        return sum(terms)

    def parse_term(self):
        """
        parses a product or quotient of factors

        Returns
        -------

        """
        factors = [self.parse_factor()]
        while self.pos < len(self.expr):
            op = self.parse_operator()
            if op == '*' or op == '/':
                factor = self.parse_factor()
                if op == '*':
                    factors.append(factor)
                elif op == '/':
                    factors.append(1/factor)
            else:
                self.pos -= 1
                break
        result = 1
        for factor in factors:
            result *= factor
        return result

    def parse_factor(self):
        """ parses a base raised to a power """
        base = self.parse_base()
        while self.pos < len(self.expr):
            op = self.parse_operator()
            if op == '^':
                exponent = self.parse_factor()
                base **= exponent
            else:
                self.pos -= 1
                break
        return base

    def parse_base(self):
        """parses either a number, a variable or a parenthesized expression"""
        if self.consume('('):
            result = self.parse_expression()
            self.expect(')')
            return result
        else:
            match = ledger.get_unit(self.expr[self.pos:])  # re.match(r'[a-zA-Z]', self.expr[self.pos:])
            if match:
                self.pos += 1
                return match
            else:
                match = re.match(r'\d+(\.\d+)?', self.expr[self.pos:])
                if match:
                    self.pos += match.end()
                    return float(match.group(0))
                else:
                    raise ValueError('Invalid input')

    def parse_operator(self):
        """
        parses an operator (+, -, *, /, ^)

        Returns
        -------

        """
        match = re.match(r'[+\-*/^]', self.expr[self.pos:])
        if match:
            self.pos += 1
            return match.group(0)
        else:
            raise ValueError('Invalid input')

    def consume(self, char):
        """consumes a character from the input """
        if self.pos < len(self.expr) and self.expr[self.pos] == char:
            self.pos += 1
            return True
        else:
            return False

    def expect(self, char):
        """consumes a character from the input if it matches the given argument"""
        if not self.consume(char):
            raise ValueError('Expected %s' % char)

    def set_variable(self, var, value):
        self.variables[var] = value

