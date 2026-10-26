def main() -> None:
    print("Welcome to quantlab!")


"""Scalar root-finding algorithms."""

from .bisection import bisection_method
from .false_position import false_position_method
from .newton_raphson import newton_raphson_method
from .secant import secant_method

__all__ = [
    "bisection_method",
    "false_position_method",
    "newton_raphson_method",
    "secant_method",
]
