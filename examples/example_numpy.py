
import numpy as np

from unitpy import Unit, Quantity

print("numpy + int")
a = np.linspace(0, 4, 5) * Unit.m
b = 1 * Unit.ft
c = a+b
print(a+b)
print(a-b)
a += b
print(a)

print("numpy + numpy")
a = np.linspace(0, 4, 5) * Unit.m
b = np.linspace(0, 4, 5) * Unit.ft
print(a+b)
print(a-b)
a += b
print(a)

print("numpy * int")
a = np.linspace(0, 4, 5) * Unit.m
b = 1.2 * Unit.s
print(a*b)
print(a/b)
a *= b
print(a)

print("numpy * numpy")
a = np.linspace(0, 4, 5) * Unit.m
b = np.linspace(0, 4, 5) * Unit.s
print(a*b)
print(a/b)
a *= b
print(a)


print("numpy functions")
a = np.linspace(-2, 4, 5) * Unit.m
print(np.sum(a))
print(np.max(a))
print(np.abs(a))
print(np.linspace(1*Unit.mm, 2*Unit.ft, 4))