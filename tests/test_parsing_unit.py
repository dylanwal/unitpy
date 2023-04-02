import pytest

from unitpy.definitions.ledger import ledger
from unitpy.utils.parsing import Parser


cases = [
    # base
    ["m", {ledger.get_entry("m"): 1}],
    ["s", {ledger.get_entry("s"): 1}],
    ["K", {ledger.get_entry("K"): 1}],
    ["g", {ledger.get_entry("g"): 1}],

    # prefix
    ["km", {ledger.get_entry("km"): 1}],
    ["ns", {ledger.get_entry("ns"): 1}],
    ["mK", {ledger.get_entry("mK"): 1}],
    ["Gg", {ledger.get_entry("Gg"): 1}],

    # division
    ["g/ml", {ledger.get_entry("g"): 1, ledger.get_entry("ml"): -1}],
    ["g/ml/s", {ledger.get_entry("g"): 1, ledger.get_entry("ml"): -1, ledger.get_entry("s"): -1}],

    # multiplication
    ["g*ml", {ledger.get_entry("g"): 1, ledger.get_entry("ml"): 1}],
    ["g*ml*s", {ledger.get_entry("g"): 1, ledger.get_entry("ml"): 1, ledger.get_entry("s"): 1}],

    # powers
    ["g**2", {ledger.get_entry("g"): 2}],
    ["g**-2", {ledger.get_entry("g"): -2}],
    ["g*cm**-3", {ledger.get_entry("g"): 1, ledger.get_entry("cm"): -3}],
    ["g**2*cm**-3", {ledger.get_entry("g"): 2, ledger.get_entry("cm"): -3}],
    ["cm**3/mol", {ledger.get_entry("cm"): 3, ledger.get_entry("mol"): -1}],

    # parenthesis
    ["g/(mol * s)", {ledger.get_entry("g"): 1, ledger.get_entry("mol"): -1, ledger.get_entry("s"): -1}],
    ["g/(ml*s)", {ledger.get_entry("g"): 1, ledger.get_entry("ml"): -1, ledger.get_entry("s"): -1}],
    ["(g*K)/(ml*s)",
     {ledger.get_entry("g"): 1, ledger.get_entry("K"): 1, ledger.get_entry("ml"): -1, ledger.get_entry("s"): -1}
     ],

    # multiple same unit
    ["m/(s/m)", {ledger.get_entry("m"): 2, ledger.get_entry("s"): -1}]
]


@pytest.mark.parametrize("case", cases)
def test_prefix(case):
    unit_str, answer = case
    parser = Parser(unit_str)
    result = parser.parse()
    for k in answer:
        assert k in result._unit
        assert answer[k] == result._unit[k]
