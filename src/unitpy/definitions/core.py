"""
The following is derived from NIST(National Institute of Standards) Special Publication 811.
https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b9

"""

######################################### Prefixes ############################################################
###############################################################################################################

prefixes = {
    "yocto": {
        "value": 1e-24,
        "abbr": ["y"]
    },
    "zepto": {
        "value": 1e-21,
        "abbr": ["z"]
    },
    "atto": {
        "value": 1e-18,
        "abbr": ["a"]
    },
    "femto": {
        "value": 1e-15,
        "abbr": ["f"]
    },
    "pico": {
        "value": 1e-12,
        "abbr": ["p"]
    },
    "nano": {
        "value": 1e-9,
        "abbr": ["n"]
    },
    "micro": {
        "value": 1e-6,
        "abbr": ["u", "µ"]
    },
    "milli": {
        "value": 1e-3,
        "abbr": ["m"]
    },
    "centi": {
        "value": 1e-2,
        "abbr": ["c"]
    },
    "deci": {
        "value": 1e-1,
        "abbr": ["d"]
    },
    "deca": {
        "value": 1e1,
        "abbr": ["da"]
    },
    "hecto": {
        "value": 1e2,
        "abbr": ["h"]
    },
    "kilo": {
        "value": 1e3,
        "abbr": ["k"]
    },
    "mega": {
        "value": 1e6,
        "abbr": ["M"]
    },
    "giga": {
        "value": 1e9,
        "abbr": ["G"]
    },
    "tera": {
        "value": 1e12,
        "abbr": ["T"]
    },
    "peta": {
        "value": 1e15,
        "abbr": ["P"]
    },
    "exa": {
        "value": 1e18,
        "abbr": ["E"]
    },
    "zetta": {
        "value": 1e21,
        "abbr": ["Z"]
    },
    "yotta": {
        "value": 1e24,
        "abbr": ["Y"]
    },
}

######################################### Constants ###########################################################
###############################################################################################################

constants = {
    # Mathematical Constants
    "pi": {
        "value": 3.141_592_653_589_793_238_462_643_383_279_502_884_197_169_399_375_1,
        "units": "",
        "abbr": ["pi", "π"],
        "descr": "pi"
    },

    # Measured Constants
    "hyperfine_transition_frequency_Cs_133": {
        "value": 9_192_631_770,
        "units": "Hz",
        "abbr": ["delta_v_Cs"],
        "descr": "hyperfine transition frequency of cesium-133"
    },
    "speed_of_light": {
        "value": 299_792_458,
        "units": "m/s",
        "abbr": ["c"],
        "descr": "The meter is defined by taking the fixed numerical value of the speed of light in vacuum c to be "
                 "299,792,458 when expressed in the unit m s−1"
    },
    "avogadro_number": {
        "value": 6.022_140_76e23,
        "units": "count",
        "abbr": ["N", "Na"],
        "descr": "number of particles in a mole"
    },
    "planck_constant": {
        "value": 6.626_070_15e10 - 34,
        "units": "J s",
        "abbr": ["h"],
        "descr": "The smallest size of energy that can be exchanged"
    },
    "elementary_charge": {
        "value": 1.602_176_634e-19,
        "units": "C",
        "abbr": ["e"],
        "descr": "Amount of charge in an electron."
    },
    "boltzmann_constant": {
        "value": 1.380_649e-23,
        "units": "J/K",
        "abbr": ["k"],
        "descr": "Relates an object’s energy to its temperature."
    },
    "luminous efficacy": {
        "value": 683,
        "units": "lm/W",
        "abbr": ["K_cd"],
        "descr": "The total amount of visible light that a source produces using a certain amount of power."
    }
}

######################################### Core Units #########################################################
###############################################################################################################

core_unit = {
    "meter": {
        "dimension": "length",
        "abbr": ["m"]
    },
    "second": {
        "dimension": "time",
        "abbr": ["t"]
    },
    "mole": {
        "dimension": "amount_of_substance",
        "abbr": ["mol"]
    },
    "kelvin": {
        "dimension": "temperature",
        "abbr": ["K"]
    },
    "candela": {
        "dimension": "luminous_intensity",
        "abbr": ["cd", "candle"]
    },
    "kilogram": {
        "dimension": "mass",
        "abbr": ["kg"]
    }
}

######################################### Conversions #########################################################
###############################################################################################################
"""
Conversions are listed by kind of quantity (dimensionality). 
Within a quantity, conversions are listed alphabetically.
Ratio is defined with respect to base
"""

acceleration = {
    "base": "meter per second squared",
    "standard_gravity": {
        "ratio": lambda x: x / 9.806_65,
        "abbr": ["g_0", "g0", "g_n", "gravity"]
    },
    "galileo": {
        "ratio": lambda x: x / 1e-02,
        "abbr": ["Gal"]
    },
}

angle = {
    "base": "radian",
    "arcminute": {
        "ratio": lambda x: x / 2.908_882e-4,
        "abbr": ["arcmin", "arc_minute", "angular_minute"]
    },
    "arcsecond": {
        "ratio": lambda x: x / 4.848_137e-6,
        "abbr": ["arcsec", "arc_second", "angular_second"]
    },
    "degree": {
        "ratio": lambda x: x / 1.745_329e-2,
        "abbr": ["deg", "arcdeg", "angular_degree"]
    },
    "grade": {
        "ratio": lambda x: x / 1.570_796e-2,
        "abbr": ["gon"]
    },
    "mil": {
        "ratio": lambda x: x / 9.817_477e-4,
        "abbr": []
    },
    "revolution": {
        "ratio": lambda x: x / 6.283_185,
        "abbr": ["r"]
    }
}

area = {
    "base": "square meter",
    "acre": {
        "ratio": lambda x: x / 4.046_873e3,
        "abbr": ["acre_survey"]
    },
    "are": {
        "ratio": lambda x: x / 1e2,
        "abbr": ["a"]
    },
    "barn": {
        "ratio": lambda x: x / 1e-28,
        "abbr": ["b"]
    },
    "circular_mil": {
        "ratio": lambda x: x / 5.067_075e-10,
        "abbr": []
    },
    "hectare": {
        "ratio": lambda x: x / 1e4,
        "abbr": ["ha"]
    }
}


energy = {
    "base": "joule",
    "british_thermal_unit_IT": {  # IT = International Table
        "ratio": lambda x: x / 1.055_056e3,
        "abbr": ["Btu_IT"]
    },
    "british_thermal_unit_th": {    # th = thermochemical
        "ratio": lambda x: x / 1.054_350e3,
        "abbr": ["Btu", "Btu_th", "british_thermal_unit"]
    },
    "calorie_IT": {  # IT = International Table
        "ratio": lambda x: x / 4.1868,
        "abbr": ["cal_IT"]
    },
    "calorie_th": {  # th = thermochemical
        "ratio": lambda x: x / 4.184,
        "abbr": ["cal", "cal_th", "calorie"]
    },
    "electronvolt": {
        "ratio": lambda x: x / 1.602_177e-19,
        "abbr": ["eV"]
    },
    "erg": {
        "ratio": lambda x: x / 1e-7,
        "abbr": ["erg"]
    },
    "foot_poundal": {
        "ratio": lambda x: x / 4.214_011e-2,
        "abbr": []
    },
    "quad": {
        "ratio": lambda x: x / 1.055_056e18,
        "abbr": []
    },
    "therm_EC": {   # EC = Council of the European Communities (now the European Union, EU)
        "ratio": lambda x: x / 1.055_06e8,
        "abbr": []
    },
    "therm_US": {  # US = United States
        "ratio": lambda x: x / 1.054_804e8,
        "abbr": []
    },
    "ton_TNT": {
        "ratio": lambda x: x / 4.184e9,
        "abbr": ["tTNT"]
    }
}


force = {
    "base": "newton",
    "dyne": {
        "ratio": lambda x: x / 1e-5,
        "abbr": ["dyn"]
    },
    "kip": {
        "ratio": lambda x: x / 4.448_222e3,
        "abbr": ["kp"]
    },
    "ounce_force": {
        "ratio": lambda x: x / 2.780_139e-1,
        "abbr": ["ozf"]
    },
    "poundal": {
        "ratio": lambda x: x / 1.382_550e-1,
        "abbr": []
    },
    "pound_force": {
        "ratio": lambda x: x / 4.448_222,
        "abbr": ["lbf"]
    },
    "ton-force": {
        "ratio": lambda x: x / 8.896_443e3,
        "abbr": ["dyn"]
    }
}


length = {
    "base": "meter",
    "angstrom": {
        "ratio": lambda x: x / 1e-10,
        "abbr": ["Å"]
    },
    "astronomical unit ": {
        "ratio": lambda x: x / 1.495_979e11,
        "abbr": ["ua"]
    },
    "chain": {
        "ratio": lambda x: x / 2.011_684e1,
        "abbr": []
    },
    "fathom": {
        "ratio": lambda x: x / 1.828_804,
        "abbr": []
    },
    "foot": {
        "ratio": lambda x: x / 3.048e-1,
        "abbr": ["feet", "ft"]
    },
    "foot_survey": {
        "ratio": lambda x: x / 3.280_833e-1,
        "abbr": []
    },
    "inch": {
        "ratio": lambda x: x / 2.54e-2,
        "abbr": ["mi"]
    },
    "light_year": {
        "ratio": lambda x: x / 9.460_73e15,
        "abbr": ["l_y"]
    },
    "link": {
        "ratio": lambda x: x / 0.201_168_4,
        "abbr": ["l", "li"]
    },
    "micron": {
        "ratio": lambda x: x / 1e-6,
        "abbr": ["u", "μ"]
    },
    "mil": {
        "ratio": lambda x: x / 2.54e-5,
        "abbr": ["u", "μ"]
    },
    "mile": {
        "ratio": lambda x: x * 1.609_344e3,
        "abbr": ["mi"]
    },
    "mile_survey": {
        "ratio": lambda x: x / 1.609_347e3,
        "abbr": ["mi_s"]
    },
    "mile_nautical": {
        "ratio": lambda x: x / 1.852e3,
        "abbr": ["mi_n"]
    },
    "parsec": {
        "ratio": lambda x: x / 3.085_678e16,
        "abbr": ["pc"]
    },
    "pica_computer": {
        "ratio": lambda x: x / 4.233_333e-3,
        "abbr": []
    },
    "pica_printer": {
        "ratio": lambda x: x / 4.217_518e-3,
        "abbr": []
    },
    "point_computer": {
        "ratio": lambda x: x / 3.527_778e-3,
        "abbr": []
    },
    "point_printer": {
        "ratio": lambda x: x / 3.514_598e-3,
        "abbr": []
    },
    "rod": {
        "ratio": lambda x: x / 5.029_210,
        "abbr": []
    },
    "yard": {
        "ratio": lambda x: x / 9.144e-1,
        "abbr": ["mi"]
    }
}


illuminance = {
    "base": "lux",
    "footcandle": {
        "ratio": lambda x: x / 1.076_391e1,
        "abbr": []
    },
    "phot": {
        "ratio": lambda x: x / 1e4,
        "abbr": ["ph"]
    }

}

luminance = {
    "base": "candela per square meter",
    "footlambert": {
        "ratio": lambda x: x / 3.426_259,
        "abbr": []
    },
    "lambert": {
        "ratio": lambda x: x / 3.183_099e3,
        "abbr": []
    },
    "stilb": {
        "ratio": lambda x: x / 1e4,
        "abbr": ["sb"]
    }
}


mass = {
    "base": "kilogram",
    "carat": {
        "ratio": lambda x: x / 2e-4,
        "abbr": []
    },
    "grain": {
        "ratio": lambda x: x / 6.479_891e-5,
        "abbr": ["gr"]
    },
    "hundredweight_long": {
        "ratio": lambda x: x / 5.080_235e1,
        "abbr": []
    },
    "hundredweight_short": {
        "ratio": lambda x: x / 4.535_924e1,
        "abbr": []
    },
    "ounce": {  # avoirdupois
        "ratio": lambda x: x / 2.834_952e-2,
        "abbr": ["oz"]
    },
    "ounce_troy": {  # troy or apothecary
        "ratio": lambda x: x / 3.110_348e-2,
        "abbr": ["oz_t"]
    },
    "pennyweight": {
        "ratio": lambda x: x / 1.555_174e-3,
        "abbr": ["dwt"]
    },
    "pound": {  # avoirdupois
        "ratio": lambda x: x / 4.535_924e-1,
        "abbr": ["lb"]
    },
    "pound_troy": {  # troy or apothecary
        "ratio": lambda x: x / 3.732_417e-2,
        "abbr": ["lb_t"]
    },
    "ton": {
        "ratio": lambda x: x / 1e3,
        "abbr": ["t", "tonne"]
    },
    "ton_assay": {
        "ratio": lambda x: x / 2.916_667e-2,
        "abbr": ["AT"]
    },
    "ton_long": {
        "ratio": lambda x: x / 1.016_047e3,
        "abbr": []
    },
    "ton_short": {
        "ratio": lambda x: x / 9.071_847e2,
        "abbr": []
    }
}

mass_d_length = {
    "base": "kilogram per meter",
    "denier": {
        "ratio": lambda x: x / 1.111_111e-7,
        "abbr": []
    },
    "tex": {
        "ratio": lambda x: x / 1e-6,
        "abbr": []
    }
}

power = {
    "base": "watt",
    "horsepower": {
        "ratio": lambda x: x / 7.46e2,
        "abbr": ["hp"]
    },
    "horsepower_english": {
        "ratio": lambda x: x / 7.456_999e2,
        "abbr": []
    },
    "horsepower_boiler": {
        "ratio": lambda x: x / 9.809_50e3,
        "abbr": []
    },
    "horsepower_metric": {
        "ratio": lambda x: x / 7.354_988e2,
        "abbr": []
    },
    "horsepower_UK": {
        "ratio": lambda x: x / 7.4570e2,
        "abbr": []
    },
    "horsepower_water": {
        "ratio": lambda x: x / 7.460_43e2,
        "abbr": []
    }
}

stress = {
    "base": "pascal",
    "atmosphere": {
        "ratio": lambda x: x / 1.013_25e5,
        "abbr": ["atm"]
    },
    "bar": {
        "ratio": lambda x: x / 1e5,
        "abbr": []
    },
    "centimeter_mercury": {
        "ratio": lambda x: x / 1.333_224e3,
        "abbr": ["cmHg", "centimeter_Hg"]
    },
    "centimeter_water": {
        "ratio": lambda x: x / 9.806_65e1,
        "abbr": ["cmH2O", "cm_water"]
    },
    "foot_mercury": {
        "ratio": lambda x: x / 4.063_666e1,
        "abbr": ["ftHg", "foot_Hg"]
    },
    "foot_water": {
        "ratio": lambda x: x / 2.989_067,
        "abbr": ["ftH2O", "ft_water"]
    },
    "inch_mercury": {
        "ratio": lambda x: x / 3.386_389e3,
        "abbr": ["inHg", "inch_Hg"]
    },
    "inch_water": {
        "ratio": lambda x: x / 2.490_889e2,
        "abbr": ["inH2O", "in_water"]
    },
    "millimeter_Hg": {
        "ratio": lambda x: x / 1.333_224e2,
        "abbr": ["mmHg"]
    },
    "torr": {
        "ratio": lambda x: x / 1.333_224e2,
        "abbr": ["Torr"]
    }
}


temperature = {
    "base": "kevin",
    "Celsius": {
        "ratio": lambda x: x - 273.15,
        "abbr": ["degC", "centigrade", "celsius"]
    },
    "Fahrenheit": {
        "ratio": lambda x: x * 1.8 - 459.67,
        "abbr": ["degF", "fahrenheit"]
    },
    "Rankine": {
        "ratio": lambda x: x * 1.8,
        "abbr": ["degR", "rankine"]
    }
}

time = {
    "base": "second",
    "day": {
        "ratio": lambda x: x / 8.64e4,
        "abbr": ["d"]
    },
    "day_sidereal": {
        "ratio": lambda x: x / 8.616_409e4,
        "abbr": []
    },
    "hour": {
        "ratio": lambda x: x / 3.6e3,
        "abbr": ["h"]
    },
    "hour_sidereal": {
        "ratio": lambda x: x / 3.590_170e3,
        "abbr": []
    },
    "minute": {
        "ratio": lambda x: x / 6.0e1,
        "abbr": ["min"]
    },
    "minute_sidereal": {
        "ratio": lambda x: x / 5.983_617e1,
        "abbr": []
    },
    "shake": {
        "ratio": lambda x: x / 1e-8,
        "abbr": []
    },
    "year": {  # 365 days
        "ratio": lambda x: x / 3.153_6e7,
        "abbr": []
    },
    "year_sidereal": {
        "ratio": lambda x: x / 3.155_815e7,
        "abbr": []
    },
    "year_tropical": {
        "ratio": lambda x: x / 3.155_693e7,
        "abbr": []
    },

    # Unofficial NIST units
    "century": {
        "ratio": lambda x: x / 3.155_693e9,
        "abbr": ["centuries"]
    },
    "decade": {
        "ratio": lambda x: x / 3.155_693e8,
        "abbr": []
    },
    "millennium": {
        "ratio": lambda x: x / 3.155_693e10,
        "abbr": []
    },
    "eon": {
        "ratio": lambda x: x / 3.155_693e16,
        "abbr": []
    },
    "year_leap": {  # 366 days
        "ratio": lambda x: x / 3.156_22e7,
        "abbr": []
    }
}


velocity = {
    "base": "meter per second",
}


viscosity_dynamic = {
    "base": "pascal second",
    "poise": {
        "ratio": lambda x: x / 1e-1,
        "abbr": ["P"]
    }
}


viscosity_kinematic = {
    "base": "meter squared per second",
    "stokes": {
        "ratio": lambda x: x / 1e-4,
        "abbr": ["St"]
    }
}


volume = {
    "base": "cubic meter",
    "acre_foot": {
        "ratio": lambda x: x / 1.233_489e3,
        "abbr": []
    },
    "barrel": {
        "ratio": lambda x: x / 1.589_873e-1,
        "abbr": ["bbl"]
    },
    "bushel": {
        "ratio": lambda x: x / 3.523_907e-2,
        "abbr": ["bu"]
    },
    "cord": {
        "ratio": lambda x: x / 3.624_556,
        "abbr": []
    },
    "cup": {
        "ratio": lambda x: x / 2.365_882e-4,
        "abbr": []
    },
    "gallon_UK": {  # UK = Canadian and U.K. (Imperial)
        "ratio": lambda x: x / 4.546_09e-3,
        "abbr": ["gal_UK"]
    },
    "gallon": {  # US = United States
        "ratio": lambda x: x / 3.785_412e-3,
        "abbr": ["gal", "gal_US"]
    },
    "gill_UK": {  # UK = Canadian and U.K. (Imperial)
        "ratio": lambda x: x / 1.420_653e-4,
        "abbr": ["gi_UK"]
    },
    "gill": {  # US = United States
        "ratio": lambda x: x / 1.182_941e-4,
        "abbr": ["gi", "gi_US"]
    },
    "liter": {  # US = United States
        "ratio": lambda x: x / 1e-3,
        "abbr": ["L"]
    },
    "ounce_fluid_UK": {  # UK = Canadian and U.K. (Imperial)
        "ratio": lambda x: x / 2.841_306e-5,
        "abbr": ["fl_oz_UK", "oz_fl_UK"]
    },
    "ounce_fluid": {
        "ratio": lambda x: x / 2.957_353e-5,
        "abbr": ["fl_oz", "oz_fl"]
    },
    "peck": {
        "ratio": lambda x: x / 8.809_768e-3,
        "abbr": ["pk"]
    },
    "pint_dry": {
        "ratio": lambda x: x / 5.506_105e-4,
        "abbr": ["dry_pt", "pt_dry"]
    },
    "pint": {
        "ratio": lambda x: x / 4.731_765e-4,
        "abbr": ["pt"]
    },
    "quart_dry": {
        "ratio": lambda x: x / 1.101_221e-3,
        "abbr": ["dry_qt", "qt_dry"]
    },
    "quart": {
        "ratio": lambda x: x / 9.463_529e-4,
        "abbr": ["qt"]
    },
    "stere": {
        "ratio": lambda x: x / 1,
        "abbr": ["st"]
    },
    "tablespoon": {
        "ratio": lambda x: x / 1.478_676e-5,
        "abbr": ["st"]
    },
    "teaspoon": {
        "ratio": lambda x: x / 4.928_922e-6,
        "abbr": ["st"]
    },
    "ton_liquid": {
        "ratio": lambda x: x / 2.831_685,
        "abbr": []
    }
}







