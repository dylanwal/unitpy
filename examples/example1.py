from unitpy import U, Q , Unit, Quantity
# Q = Quantity

q = 1 * U("kilometer/hour")
q = 1 * (U.kilometer / U.hour)
q = Quantity("1 km/h")
q = Q("1 kilometer per hour")
q = Q("1*kilometer/hour")


# properties
print(q.unit)  # kilometer / hour
print(q.dimensionality)  # [length] / [time]
print(q.dimensionless)  # False
print(q.base_unit)  # meter / second


print("")


from unitpy import U, Q , Unit, Quantity
# Q = Quantity

q = 1 * U("km/h")
q2 = q.to("mile per hour")
print(q2)  # 0.621371 mi/h


print("")


from unitpy import U, Q

q = 1 * U("km/h")
q2 = 2.2 * U("mile per hour")
print(q2 + q)
print(q2 - q)
print(q2 * q)
print(q2 / q)
print((q2 / q).dimensionless)


print("")


from unitpy import U, Q

q = 10 * U("degC")
q2 = 5 * U("degC")

# absolute
print(q.to("K"))         # 283.15 kelvin
print(q + q2)            # 288.15 Celsius
print((q + q2).to("K"))  # 561.3 kelvin
print(q - q2)            # -268.15 Celsius
print((q - q2).to("K"))  # 5.0 kelvin

# relative
print(q.add_rel(q2))      # 15 Celsius
print(q.sub_rel(q2))      # 5 Celsius
print(abs(-10 * U.degC))  # 10 Celsius
