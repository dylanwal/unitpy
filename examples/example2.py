from unitpy import U

a = U.s * U.min
c1 = 12.3 * U.s
c2 = (123 * U.min)**2

c = c1/c2
print(c.dim)
d = 12.3 * U('ml/s') / (123 * U('cm**3/min'))

a = 1.234 * U.min
print(a)
b = a.to_timedelta()
print(b)
print(type(b))
