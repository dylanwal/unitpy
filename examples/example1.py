
import unitpy


print(unitpy.ledger)
# a = 2 * unitpy.U("m*2") # TypeError: Can only multiply Unit by Unit

a = unitpy.Q("1 bar")
print(a.dimensionality)

b = unitpy.Q("2.8427778 W*h")
b.unit.multiplier
print(b.to("J"))

print(a.is_close(b, 1e-6))

