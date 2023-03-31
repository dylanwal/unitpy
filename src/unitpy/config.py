
class ConfigUnit:
    def __init__(self):
        self.format_symbols = True
        self.integer_format_numerator_parenthesis = False
        self.integer_format_denominator_parenthesis = True
        self.abbr = True  # false is full word
        self.multiplication_seperator = " "  #  " " or " * "


class Config:
    def __init__(self):
        self.units = ConfigUnit()


config = Config()
