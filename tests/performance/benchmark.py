from __future__ import annotations

import sys
import time
import datetime
import platform
from collections import deque

time.sleep(0.2)

start_import = time.perf_counter()
import unitpy

end_import = time.perf_counter()

ZERO_DEPTH_BASES = (str, bytes, int, float, bytearray)


def total_size(object_, verbose: bool = False) -> int:
    """
    Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

    Parameters
    ----------
    object_: Any
        Object you want to get the size of
    verbose: bool
        print out results

    Returns
    -------
    size: int
        size of object in bytes

    """
    seen = set()  # track which object id's have already been seen
    default_size = sys.getsizeof(0)  # estimate sizeof object without __sizeof__

    def sizeof(obj, name: str):
        if id(obj) in seen:  # do not double count the same object
            return 0

        seen.add(id(obj))
        size = sys.getsizeof(obj, default_size)

        if verbose:
            print(size, name)

        if isinstance(obj, ZERO_DEPTH_BASES):
            pass  # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, set, deque)):
            size += sum(sizeof(item, name + f"_{i}") for i, item in enumerate(obj))
        elif isinstance(obj, dict):
            size += sum(sizeof(k, name + f".{k}") + sizeof(v, name + f".key{i}")
                        for i, (k, v) in enumerate(getattr(obj, 'items')()))

            # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += sizeof(vars(obj), "  " + name + ".")
        if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
            size += sum(sizeof(getattr(obj, s), "  " + name + f".{s}") for s in obj.__slots__ if hasattr(obj, s))

        return size

    return sizeof(object_, name=type(object_).__name__)


def get_unit_memory() -> int:
    U = unitpy.U
    data = [
        U.m,
        U("m/s"),
        U("mi/h"),
        U.W,
        U.J,
        U.bar,
        U("psi")
    ]

    return int(total_size(data) / len(data))  # bytes


def get_quantity_memory() -> int:
    Q = unitpy.Q
    data = [
        Q("1 m/s"),
        Q("1 psi"),
        Q("12 bar"),
        Q("23.3 W"),
        Q("1.23424 J"),
    ]

    return int(total_size(data) / len(data))  # bytes


def _time_defining_quantity():
    data = [
        unitpy.Q("1 m/s"),
        unitpy.Q("1 psi"),
        unitpy.Q("12 bar"),
        unitpy.Q("23.3 W"),
        unitpy.Q("1.23424 J"),
    ]


def time_defining_quantity() -> float:
    n = 10_000
    start_time = time.perf_counter()
    for i in range(n):
        _time_defining_quantity()
    run_time = time.perf_counter() - start_time

    return run_time / n * 1000  # micro-seconds


def _time_convert():
    data = [
        unitpy.Q("1 m/s").to("m/h"),
        unitpy.Q("1 psi").to("kPa"),
        unitpy.Q("12 bar").to("atm"),
        unitpy.Q("23.3 W").to("J/s"),
        unitpy.Q("1.23424 J").to("W*s"),
    ]


def time_convert() -> float:
    n = 10_000
    start_time = time.perf_counter()
    for i in range(n):
        _time_convert()
    run_time = time.perf_counter() - start_time

    return run_time / n * 1000  # micro-seconds


def _time_math():
    data = [
        unitpy.Q("1 m/s") + unitpy.Q("1 mph"),
        unitpy.Q("1 psi") - unitpy.Q("2.21 kPa"),
        unitpy.Q("1 m") * unitpy.Q("2 s"),
        unitpy.Q("23.3 W") / unitpy.Q("20 J/s"),
        unitpy.Q("1.23424 J") + unitpy.Q("24.21 W*s"),
    ]


def time_math() -> float:
    n = 10_000
    start_time = time.perf_counter()
    for i in range(n):
        _time_math()
    run_time = time.perf_counter() - start_time

    return run_time / n * 1000  # micro-seconds


def main():
    python_ = sys.version_info
    data = (
        ("date/time (UTF)", str(datetime.datetime.utcnow())),
        ("platform.processor", str(platform.processor().replace(',', ''))),
        ("python version", str(f"{python_.major}.{python_.minor}.{python_.micro}")),
        ("package version", unitpy.__version__),
        ("time import(us)", str(f"{end_import - start_import:2.5f}")),
        ("memory uniot (bytes)", f"{get_unit_memory():6.0f}"),
        ("quantity_memory (bytes)", f"{get_quantity_memory():6.0f}"),
        ("time define (us)", str(f"{time_defining_quantity():2.5f}")),
        ("time convert (us)", str(f"{time_convert():2.5f}")),
        ("time math (us)", str(f"{time_math():2.5f}")),
        ("notes", "")
    )

    print(", ".join(col[0] for col in data), ", ".join(col[1] for col in data))
    with open("performance.csv", "a", encoding="UTF-8") as file:
        # file.write(", ".join(col[0] for col in data))
        file.write("\n")
        file.write(", ".join(col[1] for col in data))


def print_memory_breakdown():
    result = unitpy.Q("1.2 J")
    print("total", total_size(result, verbose=True))


if __name__ == "__main__":
    main()
    # print_memory_breakdown()
