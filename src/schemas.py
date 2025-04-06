"""Project schemas."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Car:
    description: str = ""
    url: str = ""
    price: int = 0
    year: int = 0
