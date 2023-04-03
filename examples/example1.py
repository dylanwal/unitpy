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



from unitpy import U, Q , Unit, Quantity
# Q = Quantity

q = 1 * U("km/h")
q2 = q.to("mile per hour")
print(q2)  # 0.621371 mi/h



from unitpy import U, Q

q = 1 * U("km/h")
q2 = 2.2 * U("mile per hour")
print(q2 + q)
print(q2 - q)
print(q2 * q)
print(q2 / q)
print((q2 / q).dimensionless)



from unitpy import U, Q

q = 300 * U("K")
q2 = 200 * U("K")

print(q + q2)
print(q.to("degC"))
print(q.to("degF"))
print(q.to("degR"))

q = 10 * U("degC")
q2 = 5 * U("degC")

print(q + q2)
print(q - q2)
