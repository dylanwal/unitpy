"""
The following is derived from NIST(National Institute of Standards) Special Publication 811.
https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9

Conversions are listed by kind of quantity (dimensionality).
Within a quantity, conversions are listed alphabetically.
Ratio is defined with respect to base

"""

from unitpy.definitions.unit_base import BaseSet
from unitpy.definitions.unit_derived import derived_quantities

units_NIST = {
    "acceleration": {
        "base": BaseSet(meter=1, second=2),
        "standard_gravity": {
            "multiplier": 9.806_65,
            "abbr": "g0",
            "additional_labels": ["g_0", "g_n", "gravity"]
        },
        "galileo": {
            "multiplier": 1e-02,
            "abbr": "Gal"
        },
    },

    "angle": {
        "base": derived_quantities["radian"].base_unit,
        "arcminute": {
            "multiplier": 2.908_882e-4,
            "abbr": "arcmin",
            "additional_labels": ["arc_minute", "angular_minute"]
        },
        "arcsecond": {
            "multiplier": 4.848_137e-6,
            "abbr": "arcsec",
            "additional_labels": ["arc_second", "angular_second"]
        },
        "degree": {
            "multiplier": 1.745_329e-2,
            "abbr": "deg",
            "additional_labels": ["arcdeg", "angular_degree"]
        },
        "grade": {
            "multiplier": 1.570_796e-2,
            "abbr": "gon"
        },
        "angle_mil": {  # mil
            "multiplier": 9.817_477e-4,
            "abbr": None
        },
        "revolution": {
            "multiplier": 6.283_185,
            "abbr": "r"
        }
    },

    "area": {
        "base": BaseSet(meter=2),
        "acre": {
            "multiplier": 4.046_873e3,
            "abbr": "acre_survey"
        },
        "are": {
            "multiplier": 1e2,
            "abbr": "a"
        },
        "barn": {
            "multiplier": 1e-28,
            "abbr": "b"
        },
        "circular_mil": {
            "multiplier": 5.067_075e-10,
            "abbr": None
        },
        "hectare": {
            "multiplier": 1e4,
            "abbr": "ha"
        }
    },

    "energy": {
        "base": derived_quantities["joule"].base_unit,
        "british_thermal_unit_IT": {  # IT : International Table
            "multiplier": 1.055_056e3,
            "abbr": "Btu_IT"
        },
        "british_thermal_unit_th": {  # th : thermochemical
            "multiplier": 1.054_350e3,
            "abbr": "Btu",
            "additional_labels": ["Btu_th", "british_thermal_unit", "BTU", "btu"]
        },
        "calorie_IT": {  # IT : International Table
            "multiplier": 4.1868,
            "abbr": "cal_IT"
        },
        "calorie_th": {  # th : thermochemical
            "multiplier": 4.184,
            "abbr": "cal",
            "additional_labels": ["cal_th", "calorie"]
        },
        "electronvolt": {
            "multiplier": 1.602_177e-19,
            "abbr": "eV"
        },
        "erg": {
            "multiplier": 1e-7,
            "abbr": None
        },
        "foot_poundal": {
            "multiplier": 4.214_011e-2,
            "abbr": None
        },
        "quad": {
            "multiplier": 1.055_056e18,
            "abbr": None
        },
        "therm_EC": {  # EC : Council of the European Communities (now the European Union, EU)
            "multiplier": 1.055_06e8,
            "abbr": None
        },
        "therm_US": {  # US : United States
            "multiplier": 1.054_804e8,
            "abbr": None
        },
        "ton_TNT": {
            "multiplier": 4.184e9,
            "abbr": "tTNT"
        }
    },

    "force": {
        "base": derived_quantities["newton"].base_unit,
        "dyne": {
            "multiplier": 1e-5,
            "abbr": "dyn"
        },
        "kip": {
            "multiplier": 4.448_222e3,
            "abbr": "kp"
        },
        "ounce_force": {
            "multiplier": 2.780_139e-1,
            "abbr": "ozf"
        },
        "poundal": {
            "multiplier": 1.382_550e-1,
            "abbr": None
        },
        "pound_force": {
            "multiplier": 4.448_222,
            "abbr": "lbf"
        },
        "ton-force": {
            "multiplier": 8.896_443e3,
            "abbr": None
        }
    },

    "length": {
        "base": BaseSet(meter=1),
        "angstrom": {
            "multiplier": 1e-10,
            "abbr": "Å",
        },
        "astronomical unit ": {
            "multiplier": 1.495_979e11,
            "abbr": "ua"
        },
        "chain": {
            "multiplier": 2.011_684e1,
            "abbr": None
        },
        "fathom": {
            "multiplier": 1.828_804,
            "abbr": None
        },
        "foot": {
            "multiplier": 3.048e-1,
            "abbr": "ft",
            "additional_labels": ["feet"]
        },
        "foot_survey": {
            "multiplier": 3.280_833e-1,
            "abbr": None
        },
        "inch": {
            "multiplier": 2.54e-2,
            "abbr": "in"
        },
        "light_year": {
            "multiplier": 9.460_73e15,
            "abbr": "l_y"
        },
        "link": {
            "multiplier": 0.201_168_4,
            "abbr": None,  # "l" conflict with liter
            "additional_labels": ["li"]
        },
        "micron": {
            "multiplier": 1e-6,
            "abbr": "u",
            "additional_labels": ["μ"]
        },
        "mil": {
            "multiplier": 2.54e-5,
            "abbr": None  # "u", "μ"
        },
        "mile": {
            "multiplier": 1.609_344e3,
            "abbr": "mi"
        },
        "mile_survey": {
            "multiplier": 1.609_347e3,
            "abbr": "mi_s"
        },
        "mile_nautical": {
            "multiplier": 1.852e3,
            "abbr": "mi_n"
        },
        "parsec": {
            "multiplier": 3.085_678e16,
            "abbr": "pc"
        },
        "pica_computer": {
            "multiplier": 4.233_333e-3,
            "abbr": None
        },
        "pica_printer": {
            "multiplier": 4.217_518e-3,
            "abbr": None
        },
        "point_computer": {
            "multiplier": 3.527_778e-3,
            "abbr": None
        },
        "point_printer": {
            "multiplier": 3.514_598e-3,
            "abbr": None
        },
        "rod": {
            "multiplier": 5.029_210,
            "abbr": None
        },
        "yard": {
            "multiplier": 9.144e-1,
            "abbr": "yd"
        }
    },

    "illuminance": {
        "base": derived_quantities["lux"].base_unit,
        "footcandle": {
            "multiplier": 1.076_391e1,
            "abbr": None
        },
        "phot": {
            "multiplier": 1e4,
            "abbr": "ph"
        }

    },

    "luminance": {
        "base": derived_quantities["lux"].base_unit,
        "footlambert": {
            "multiplier": 3.426_259,
            "abbr": None
        },
        "lambert": {
            "multiplier": 3.183_099e3,
            "abbr": None
        },
        "stilb": {
            "multiplier": 1e4,
            "abbr": "sb"
        }
    },

    "mass": {
        "base": BaseSet(kilogram=1),
        "carat": {
            "multiplier": 2e-4,
            "abbr": None
        },
        "grain": {
            "multiplier": 6.479_891e-5,
            "abbr": "gr"
        },
        "hundredweight_long": {
            "multiplier": 5.080_235e1,
            "abbr": None
        },
        "hundredweight_short": {
            "multiplier": 4.535_924e1,
            "abbr": None
        },
        "ounce": {  # avoirdupois
            "multiplier": 2.834_952e-2,
            "abbr": "oz"
        },
        "ounce_troy": {  # troy or apothecary
            "multiplier": 3.110_348e-2,
            "abbr": "oz_t"
        },
        "pennyweight": {
            "multiplier": 1.555_174e-3,
            "abbr": "dwt"
        },
        "pound": {  # avoirdupois
            "multiplier": 4.535_924e-1,
            "abbr": "lb"
        },
        "pound_troy": {  # troy or apothecary
            "multiplier": 3.732_417e-2,
            "abbr": "lb_t"
        },
        "ton": {
            "multiplier": 1e3,
            "abbr": "t",
            "additional_labels": ["tonne"]
        },
        "ton_assay": {
            "multiplier": 2.916_667e-2,
            "abbr": "AT"
        },
        "ton_long": {
            "multiplier": 1.016_047e3,
            "abbr": None
        },
        "ton_short": {
            "multiplier": 9.071_847e2,
            "abbr": None
        }
    },

    "mass_d_length": {
        "base": BaseSet(kilogram=1, meter=-1),
        "denier": {
            "multiplier": 1.111_111e-7,
            "abbr": None
        },
        "tex": {
            "multiplier": 1e-6,
            "abbr": None
        }
    },

    "power": {
        "base": derived_quantities["watt"].base_unit,
        "horsepower": {
            "multiplier": 7.46e2,
            "abbr": "hp"
        },
        "horsepower_english": {
            "multiplier": 7.456_999e2,
            "abbr": None
        },
        "horsepower_boiler": {
            "multiplier": 9.809_50e3,
            "abbr": None
        },
        "horsepower_metric": {
            "multiplier": 7.354_988e2,
            "abbr": None
        },
        "horsepower_UK": {
            "multiplier": 7.4570e2,
            "abbr": None
        },
        "horsepower_water": {
            "multiplier": 7.460_43e2,
            "abbr": None
        }
    },

    "stress": {
        "base": derived_quantities["pascal"].base_unit,
        "atmosphere": {
            "multiplier": 1.013_25e5,
            "abbr": "atm"
        },
        "bar": {
            "multiplier": 1e5,
            "abbr": None
        },
        "centimeter_mercury": {
            "multiplier": 1.333_224e3,
            "abbr": "cmHg",
            "additional_labels": ["centimeter_Hg"]
        },
        "centimeter_water": {
            "multiplier": 9.806_65e1,
            "abbr": "cmH2O",
            "additional_labels": ["cm_water"]
        },
        "foot_mercury": {
            "multiplier": 4.063_666e1,
            "abbr": "ftHg",
            "additional_labels": ["foot_Hg"]
        },
        "foot_water": {
            "multiplier": 2.989_067,
            "abbr": "ftH2O",
            "additional_labels": ["ft_water"]
        },
        "inch_mercury": {
            "multiplier": 3.386_389e3,
            "abbr": "inHg",
            "additional_labels": ["inch_Hg"]
        },
        "inch_water": {
            "multiplier": 2.490_889e2,
            "abbr": "inH2O",
            "additional_labels": ["in_water"]
        },
        "millimeter_Hg": {
            "multiplier": 1.333_224e2,
            "abbr": "mmHg"
        },
        "torr": {
            "multiplier": 1.333_224e2,
            "abbr": "Torr"
        }
    },

    "temperature": {
        "base": BaseSet(kelvin=1),
        "Fahrenheit": {
            "multiplier": 1.8,
            "offset": -459.67,
            "abbr": "degF",
            "additional_labels": ["fahrenheit"]
        },
        "Rankine": {
            "multiplier": 1.8,
            "abbr": "degR",
            "additional_labels": ["rankine"]
        }
    },

    "time": {
        "base": BaseSet(second=1),
        "day": {
            "multiplier": 8.64e4,
            "abbr": "d"
        },
        "day_sidereal": {
            "multiplier": 8.616_409e4,
            "abbr": None
        },
        "hour": {
            "multiplier": 3.6e3,
            "abbr": "h"
        },
        "hour_sidereal": {
            "multiplier": 3.590_170e3,
            "abbr": None
        },
        "minute": {
            "multiplier": 6.0e1,
            "abbr": "min"
        },
        "minute_sidereal": {
            "multiplier": 5.983_617e1,
            "abbr": None
        },
        "shake": {
            "multiplier": 1e-8,
            "abbr": None
        },
        "year": {  # 365 days
            "multiplier": 3.153_6e7,
            "abbr": None
        },
        "year_sidereal": {
            "multiplier": 3.155_815e7,
            "abbr": None
        },
        "year_tropical": {
            "multiplier": 3.155_693e7,
            "abbr": None
        },

        # Unofficial NIST units
        "century": {
            "multiplier": 3.155_693e9,
            "abbr": "centuries"
        },
        "decade": {
            "multiplier": 3.155_693e8,
            "abbr": None
        },
        "millennium": {
            "multiplier": 3.155_693e10,
            "abbr": None
        },
        "eon": {
            "multiplier": 3.155_693e16,
            "abbr": None
        },
        "year_leap": {  # 366 days
            "multiplier": 3.156_22e7,
            "abbr": None
        }
    },

    "dynamic_viscosity": {
        "base": BaseSet(kilogram=1, meter=-1, second=-1),
        "poise": {
            "multiplier": 1e-1,
            "abbr": "P"
        }
    },

    "viscosity_kinematic": {
        "base": BaseSet(meter=2, second=-1),
        "stokes": {
            "multiplier": 1e-4,
            "abbr": "St"
        }
    },

    "volume": {
        "base": BaseSet(meter=3),
        "acre_foot": {
            "multiplier": 1.233_489e3,
            "abbr": None
        },
        "barrel": {
            "multiplier": 1.589_873e-1,
            "abbr": "bbl"
        },
        "bushel": {
            "multiplier": 3.523_907e-2,
            "abbr": "bu"
        },
        "cord": {
            "multiplier": 3.624_556,
            "abbr": None
        },
        "cup": {
            "multiplier": 2.365_882e-4,
            "abbr": None
        },
        "gallon_UK": {  # UK : Canadian and U.K. (Imperial)
            "multiplier": 4.546_09e-3,
            "abbr": "gal_UK"
        },
        "gallon": {  # US : United States
            "multiplier": 3.785_412e-3,
            "abbr": "gal",
            "additional_labels": ["gal_US"]
        },
        "gill_UK": {  # UK : Canadian and U.K. (Imperial)
            "multiplier": 1.420_653e-4,
            "abbr": "gi_UK"
        },
        "gill": {  # US : United States
            "multiplier": 1.182_941e-4,
            "abbr": "gi",
            "additional_labels": ["gi_US"]
        },
        "liter": {  # US : United States
            "multiplier": 1e-3,
            "abbr": "L",
            "additional_labels": ["l"]
        },
        "ounce_fluid_UK": {  # UK : Canadian and U.K. (Imperial)
            "multiplier": 2.841_306e-5,
            "abbr": "fl_oz_UK",
            "additional_labels": ["oz_fl_UK"]
        },
        "ounce_fluid": {
            "multiplier": 2.957_353e-5,
            "abbr": "fl_oz",
            "additional_labels": ["oz_fl"]
        },
        "peck": {
            "multiplier": 8.809_768e-3,
            "abbr": "pk"
        },
        "pint_dry": {
            "multiplier": 5.506_105e-4,
            "abbr": "dry_pt",
            "additional_labels": ["pt_dry"]
        },
        "pint": {
            "multiplier": 4.731_765e-4,
            "abbr": "pt"
        },
        "quart_dry": {
            "multiplier": 1.101_221e-3,
            "abbr": "dry_qt",
            "additional_labels": ["qt_dry"]
        },
        "quart": {
            "multiplier": 9.463_529e-4,
            "abbr": "qt"
        },
        "stere": {
            "multiplier": 1,
            "abbr": "st"
        },
        "tablespoon": {
            "multiplier": 1.478_676e-5,
            "abbr": "tbsp"
        },
        "teaspoon": {
            "multiplier": 4.928_922e-6,
            "abbr": "tsp"
        },
        "ton_liquid": {
            "multiplier": 2.831_685,
            "abbr": None
        }
    }

}
