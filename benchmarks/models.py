"""
Models for test data
"""
import dataclasses
from typing import List


@dataclasses.dataclass
class MyClass:
    a: int
    b: int
    c: 'Nested1'


@dataclasses.dataclass
class Nested1:
    aa: int
    bb: List['Nested2']


@dataclasses.dataclass
class Nested2:
    x: int
