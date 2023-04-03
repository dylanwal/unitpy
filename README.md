# UnitPy (Unit Python)

---
---

![PyPI](https://img.shields.io/pypi/v/unitpy)
![downloads](https://static.pepy.tech/badge/unitpy)
![license](https://img.shields.io/github/license/dylanwal/unitpy)

UnitPy is a Python package for defining, converting, and working with units. 

The goal of the package is to be simple, straightforward, and performant. 

This package directly implements  
[NIST (National Institute of Standards and Technology)](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-1-introduction) 
official unit definitions. 

---

## Installation

Pip installable package:

`pip install bigsmiles`

[pypi: bigsmiles](https://pypi.org/project/bigsmiles/)


---

## Requirements / Dependencies

Python 3.7 and up

---

## Basic Usage

### Defining Unit

```python
from unitpy import U, Q, Unit, Quantity
# U = Unit

u = Unit("meter")
u = U("meter")
u = U("m")
u = U.meter
u = U.m

u = U("meter/second")
u = U("m/s")
u = U.meter / U.second
u = U.m / U.s

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

q = 1 * U("meter/second") 
q = 1 * (U.meter / U.second)
q = Quantity("1 m/s")
q = Q("1 meter/second")
q = Q("1*meter/second")


# properties
q.unit # meter / second
q.dimensionality  # [length] / [time]
q.dimensionless  # False
q.base_unit  # meter / second
```


### Unit Conversion

```python
from unitpy import U, Q , Unit, Quantity
# Q = Quantity

q = 1 * U("meter/second") 
q2 = q.to("mph")
print(q2)
```


### Mathematical operation


### Temperature








Note: this package utilizes the American spellings "meter," "liter," and "ton"