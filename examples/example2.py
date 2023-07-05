from unitpy import U

a = 1.234 * U.min
print(a)
b = a.to_timedelta()
print(b)
print(type(b))
