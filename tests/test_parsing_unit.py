import pytest

from unitpy.definitions.ledger import ledger
from unitpy.utils.parsing import Parser


cases = [
    # base
    ["m", {ledger.get_unit("m"): 1}],
    ["s", {ledger.get_unit("s"): 1}],
    ["K", {ledger.get_unit("K"): 1}],
    ["g", {ledger.get_unit("g"): 1}],

    # prefix
    ["km", {ledger.get_unit("km"): 1}],
    ["ns", {ledger.get_unit("ns"): 1}],
    ["mK", {ledger.get_unit("mK"): 1}],
    ["Gg", {ledger.get_unit("Gg"): 1}],

    # division
    ["g/ml", {ledger.get_unit("g"): 1, ledger.get_unit("ml"): -1}],
    ["g/ml/s", {ledger.get_unit("g"): 1, ledger.get_unit("ml"): -1, ledger.get_unit("s"): -1}],

    # multiplication
    ["g*ml", {ledger.get_unit("g"): 1, ledger.get_unit("ml"): 1}],
    ["g*ml*s", {ledger.get_unit("g"): 1, ledger.get_unit("ml"): 1, ledger.get_unit("s"): 1}],

    # powers
    ["g**2", {ledger.get_unit("g"): 2}],
    ["g**-2", {ledger.get_unit("g"): -2}],
    ["g*cm**-3", {ledger.get_unit("g"): 1, ledger.get_unit("cm"): -3}],
    ["g**2cm**-3", {ledger.get_unit("g"): 2, ledger.get_unit("cm"): -3}],
    ["cm**3/mol", {ledger.get_unit("cm"): 3, ledger.get_unit("mol"): -1}],

    # parenthesis
    ["g/(mol * s)", {ledger.get_unit("g"): 1, ledger.get_unit("mol"): -1, ledger.get_unit("s"): -1}],
    ["g/(ml*s)", {ledger.get_unit("g"): 1, ledger.get_unit("ml"): -1, ledger.get_unit("s"): -1}],
    ["(g*K)/(ml*s)",
     {ledger.get_unit("g"): 1, ledger.get_unit("K"): 1, ledger.get_unit("ml"): -1, ledger.get_unit("s"): -1}
     ],

    # multiple same unit
    ["m/(s/m)", {ledger.get_unit("m"): 2, ledger.get_unit("s"): -1}]
]


@pytest.mark.parametrize("case", cases)
def test_prefix(case):
    unit_str, answer = case
    parser = Parser(unit_str)
    result = parser.parse()
    for k in answer:
        assert k in result
        assert answer[k] == result[k]
