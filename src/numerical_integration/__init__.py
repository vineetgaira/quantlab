"""Composite numerical integration methods."""

from .simpsons import simpsons_one_third, simpsons_three_eighths
from .trapezoidal import trapezoidal_rule

__all__ = [
    "simpsons_one_third",
    "simpsons_three_eighths",
    "trapezoidal_rule",
]
