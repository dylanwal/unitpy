
import pytest

import unitpy

cases = (
    # length
    ("1 m", "100 cm"),
    ("1 m", "0.001 km"),
    ("1 m", "3.28084 ft"),
    ("1 m", "0.000621371 mi"),

    # area
    ("1 m**2", "1550 in**2"),
    ("3.2 mi**2", "8.28796 km**2"),

    # volume
    ("1 gallon", "4 quart"),
    ("1 gallon", "3785.41 cm**3"),
    ("1 ft**3", "0.0283168 m**3"),
    ("1 ml", "1 cm**3"),

    # energy
    ("10234 J", "9.6999604851119 Btu_IT"),
    ("10234 J", "2.8427778 W*h"),
    ("12342356 J", "3.42843222 kW*h"),

    # pressure
    ("123124 Pa", "1.23124 bar"),

    # mass
    ("1 kg", "2.20462 lb"),
    ("1 kg", "35.274 oz"),
    ("1 kg", "0.000984207 ton_long"),

    # temperature
    ("0 degC", "32 degF"),
    ("50 degF", "10 degC"),
    ("0 degK", "-273.15 degC"),
    ("-459.67 degF", "0 degK"),

)


@pytest.mark.parametrize("case", cases)
def test_equal(case):
    q1 = unitpy.Q(case[0])
    q2 = unitpy.Q(case[1])
    assert q1.is_close(q2, rel_tol=1e-5)
