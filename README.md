# UnitPy (Unit Python)

---
---

![PyPI](https://img.shields.io/pypi/v/unitpy)
![downloads](https://static.pepy.tech/badge/unitpy)
![license](https://img.shields.io/github/license/dylanwal/unitpy)

UnitPy is a Python package for defining, converting, and working with units. 

The goal of the package is to be simple, straightforward, and performant. 

This package directly implements [NIST (National Institute of Standards and Technology)](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-1-introduction) 
official unit definitions. 

---

## Installation

Pip installable package:

`pip install unitpy`

[pypi: unitpy](https://pypi.org/project/unitpy/)


---

## Requirements / Dependencies

Python 3.7 and up

---

## Basic Usage

### Defining Unit

```python
from unitpy import U, Q, Unit, Quantity
# U = Unit

u = Unit("kilometer")
u = U("kilometer")
u = U("km")
u = U.kilometer
u = U.km

u = U("kilometer/hour")
u = U("km/h")
u = U.kilometer / U.hour
u = U.km / U.h

# properties
u.dimensionality  # [length] / [time]
u.dimensionless  # False
u.base_unit  # meter / second
```


### Defining Quantity

** Quantity = Value + Unit **

```python
from unitpy import U, Q , Unit, Quantity
# Q = Quantity

q = 1 * U("kilometer/hour") 
q = 1 * (U.kilometer / U.hour)
q = Quantity("1 km/h")
q = Q("1 kilometer per hour")
q = Q("1*kilometer/hour")


# properties
print(q.unit) # kilometer / hour
print(q.dimensionality)  # [length] / [time]
print(q.dimensionless)  # False
print(q.base_unit)  # meter / second
```


### Unit Conversion

```python
from unitpy import U, Q , Unit, Quantity
# Q = Quantity

q = 1 * U("km/h") 
q2 = q.to("mile per hour")
print(q2)  # 0.6213711922373341 mile / hour
```


### Mathematical operation

```python
from unitpy import U, Q 

q = 1 * U("km/h") 
q2 = 2.2 * U("mile per hour")
print(q2 + q)  # 3.2 mile / hour
print(q2 - q)  # 1.2000000000000002 mile / hour
print(q2 * q)  # 2.2 kilometer mile / hour**2
print(q2 / q) # 2.2 mile / kilometer
print((q2 / q).dimensionless) # True
```

### Temperature








Note: this package utilizes the American spellings "meter," "liter," and "ton"