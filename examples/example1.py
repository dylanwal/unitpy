
import unitpy


print(unitpy.ledger)
# a = 2 * unitpy.U("m*2") # TypeError: Can only multiply Unit by Unit

a = 2 * unitpy.U("g**-2")
a.dimensionality
print(a)

b = a.to("cm**2")
print(b)
